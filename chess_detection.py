import os
import argparse
import cv2
import pathlib

from chessai.dnn.yolox import YOLOXObjectDetector


if __name__ == "__main__":
    parser = argparse.ArgumentParser("YOLOX detector demo")
    parser.add_argument(
        "--model",
        type=str,
        default="data/dnn/chessai-det.onnx",
        help="Input your onnx model.",
    )
    parser.add_argument(
        "--class_names",
        type=str,
        default="data/dnn/chessai-det.names",
        help="Input your class names.",
    )
    parser.add_argument(
        "--score_thr",
        type=float,
        default=0.3,
        help="Score threshould to filter the result.",
    )
    parser.add_argument(
        "--with_p6",
        action="store_true",
        help="Whether your model uses p6 in FPN/PAN.",
    )
    parser.add_argument(
        "--input",
        type=str,
        default=None,
        help="Input your video path or input device id.",
    )
    parser.add_argument(
        "--input_folder",
        type=str,
        default=None,
        help="Input your image folder path.",
    )
    parser.add_argument(
        "--output_folder",
        type=str,
        default=None,
        help="Output your image folder path.",
    )
    args = parser.parse_args()

    with open(args.class_names, "rt") as f:
        class_names = f.read().rstrip("\n").split("\n")
    net = YOLOXObjectDetector(
        args.model, class_names=class_names, p6=args.with_p6, conf_threshold=args.score_thr
    )

    if args.input_folder is not None:
        for img in os.listdir(args.input_folder):
            img_path = os.path.join(args.input_folder, img)
            srcimg = cv2.imread(img_path)
            srcimg = net.detect(srcimg)
            if args.output_folder is None:
                cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
                cv2.imshow("Result", srcimg)
                cv2.waitKey(0)
            else:
                pathlib.Path(args.output_folder).mkdir(parents=True, exist_ok=True)
                cv2.imwrite(os.path.join(args.output_folder, img), srcimg)

    if args.input is not None:
        if args.input.isdigit():
            cap = cv2.VideoCapture(int(args.input))
        else:
            cap = cv2.VideoCapture(args.input)
        while True:
            ret, srcimg = cap.read()
            if not ret:
                break
            srcimg = net.detect(srcimg)
            cv2.namedWindow("Result", cv2.WINDOW_NORMAL)
            cv2.imshow("Result", srcimg)
            cv2.waitKey(1)

