import cv2
import numpy as np

from chessai.common import *
from chessai.config import *
from chessai.dnn.yolox import YOLOXObjectDetector


class PieceDetector:
    def __init__(self, model_path=None, class_names_path=None, class_names=None, score_thr=0.3, with_p6=False):
        if not class_names_path and not class_names:
            raise ValueError("Either `class_names_path` or `class_names` must be provided")
        if class_names_path:
            with open(class_names_path, "rt") as f:
                self.class_names = f.read().rstrip("\n").split("\n")
        else:
            self.class_names = class_names
        self.model = YOLOXObjectDetector(
            model_path,
            class_names=self.class_names,
            p6=with_p6,
            conf_threshold=score_thr,
        )

    @staticmethod
    def iou(box1, box2):
        # Calculate intersection area
        x1 = max(box1[0], box2[0])
        y1 = max(box1[1], box2[1])
        x2 = min(box1[2], box2[2])
        y2 = min(box1[3], box2[3])
        intersection = max(0, x2 - x1) * max(0, y2 - y1)

        # Calculate union area
        area1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
        area2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
        union = area1 + area2 - intersection

        # Calculate IoU
        return intersection / union

    @staticmethod
    def is_red_piece(image, visualize=False):
        if image.shape[0] == 0 or image.shape[1] == 0:
            return False
        img_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

        lower_red = np.array([0, 50, 50])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

        lower_red = np.array([170, 50, 50])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

        lower_red = np.array([114, 34, 116])
        upper_red = np.array([134, 54, 196])
        mask2 = cv2.inRange(img_hsv, lower_red, upper_red)

        lower_red = np.array([113, 37, 129])
        upper_red = np.array([133, 57, 209])
        mask3 = cv2.inRange(img_hsv, lower_red, upper_red)

        lower_red = np.array([114, 42, 36])
        upper_red = np.array([163, 82, 196])
        mask4 = cv2.inRange(img_hsv, lower_red, upper_red)

        mask = mask0 + mask1 + mask2 + mask3 + mask4
        num_red_pixels = np.count_nonzero(mask)

        if visualize:
            cv2.imshow("mask", mask)
            cv2.waitKey(0)

        return num_red_pixels > 350

    def detect(self, image, visualize=None):
        # Detect pieces
        boxes, scores, cls_inds = self.model.detect(image, visualize)

        # Align pieces
        board = []
        for rect in CELL_RECTANGLES:
            is_found = False
            for i, box in enumerate(boxes):
                if self.iou(rect, box) > 0.1:
                    piece_crop = image[
                        int(box[1]) : int(box[3]), int(box[0]) : int(box[2])
                    ]
                    if piece_crop.shape[0] == 0 or piece_crop.shape[1] == 0:
                        continue
                    color = "r" if self.is_red_piece(piece_crop) else "b"
                    board.append(color + self.class_names[int(cls_inds[i])])
                    is_found = True
                    break
            if not is_found:
                board.append("")

        # Reshape to 10x9
        board = np.array(board).reshape(10, 9)
        return board
