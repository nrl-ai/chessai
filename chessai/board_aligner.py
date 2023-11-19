import cv2
import numpy as np
import time

from chessai.common import *
from chessai.config import *

class BoardAligner:
    def __init__(
        self,
        ref_image_path,
        smooth=False,
        debug=False,
        output_video_path=None,
    ):
        self.smooth = smooth
        self.debug = debug
        self.output_video_path = output_video_path

        # Transform matrices
        self.last_M_update = time.time()
        self.M = None
        self.M_inv = None
        self.h_array = []

        self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_250)
        parameters = cv2.aruco.DetectorParameters()
        parameters.cornerRefinementMethod = 5
        parameters.errorCorrectionRate = 0.3
        self.parameters = parameters
        self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, parameters)

        # Load reference image
        self.ref_image = cv2.imread(ref_image_path, cv2.IMREAD_GRAYSCALE)

        # Detect markers in reference image
        self.ref_corners, self.ref_ids, self.ref_rejected = self.detector.detectMarkers(
            self.ref_image
        )

        # Create bounding box from reference image dimensions
        self.rect = np.array(
            [
                [
                    [0, 0],
                    [self.ref_image.shape[1], 0],
                    [self.ref_image.shape[1], self.ref_image.shape[0]],
                    [0, self.ref_image.shape[0]],
                ]
            ],
            dtype="float32",
        )

        if self.output_video_path:
            self.output_video = cv2.VideoWriter(
                "output.avi",
                cv2.VideoWriter_fourcc("M", "J", "P", "G"),
                10,
                (self.ref_image.shape[1], self.ref_image.shape[0]),
            )
        else:
            self.output_video = None

    def get_output_size(self):
        return self.ref_image.shape[1], self.ref_image.shape[0]

    def process(self, image, visualize=None):
        """Transform image"""

        # Convert frame to gray scale
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find new transform matrices
        if time.time() - self.last_M_update > 1 or self.M is None:
            is_aruco_detected = self._process_aruco(gray, update_transform_matrices=True)
            self.last_M_update = time.time()
        else:
            is_aruco_detected = self._process_aruco(gray, update_transform_matrices=False)

        # Draw detected markers in frame with their ids
        if self.debug and is_aruco_detected:
            if visualize is not None:
                cv2.aruco.drawDetectedMarkers(visualize, self.res_corners, self.res_ids)

        # Convert image using new transform matrices
        if is_aruco_detected or self.M_inv is not None:
            frame_warp = cv2.warpPerspective(
                image, self.M_inv, (self.ref_image.shape[1], self.ref_image.shape[0])
            )
            if self.output_video is not None:
                self.output_video.write(frame_warp)

            return True, frame_warp
        else:
            return False, image

    def _process_aruco(self, gray, update_transform_matrices=True):
        """Find aruco and update transformation matrices"""

        # Detect aruco markers in gray frame
        res_corners, res_ids, _ = cv2.aruco.detectMarkers(
            gray, self.aruco_dict, parameters=self.parameters
        )
        self.res_corners = res_corners
        self.res_ids = res_ids

        # If markers were not detected
        if res_ids is None:
            return False

        if not update_transform_matrices:
            return True

        # Find which markers in frame match those in reference image
        idx = which(self.ref_ids, res_ids)

        # If # of detected points is too small => ignore the result
        if len(idx) <= 2:
            return False

        # Flatten the array of corners in the frame and reference image
        these_res_corners = np.concatenate(res_corners, axis=1)
        these_ref_corners = np.concatenate([self.ref_corners[x] for x in idx], axis=1)

        # Estimate homography matrix
        try:
            h, s = cv2.findHomography(
                these_ref_corners, these_res_corners, cv2.RANSAC, 1000.0
            )
        except:
            return False

        # If we want smoothing
        if self.smooth:
            self.h_array.append(h)
            self.M = np.mean(self.h_array, axis=0)
        else:
            self.M = h

        self.M_inv, s = cv2.findHomography(
            these_res_corners, these_ref_corners, cv2.RANSAC, 1000.0
        )

        return True
