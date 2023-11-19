import sys

import cv2
import numpy as np

image_hsv = None
pixel = (0, 0, 0)


def check_boundaries(value, tolerance, ranges, upper_or_lower):
    if ranges == 0:
        boundary = 180
    elif ranges == 1:
        boundary = 255

    if value + tolerance > boundary:
        value = boundary
    elif value - tolerance < 0:
        value = 0
    else:
        if upper_or_lower == 1:
            value = value + tolerance
        else:
            value = value - tolerance
    return value


def pick_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        pixel = image_hsv[y, x]

        hue_upper = check_boundaries(pixel[0], 10, 0, 1)
        hue_lower = check_boundaries(pixel[0], 10, 0, 0)
        saturation_upper = check_boundaries(pixel[1], 10, 1, 1)
        saturation_lower = check_boundaries(pixel[1], 10, 1, 0)
        value_upper = check_boundaries(pixel[2], 40, 1, 1)
        value_lower = check_boundaries(pixel[2], 40, 1, 0)

        upper = np.array([hue_upper, saturation_upper, value_upper])
        lower = np.array([hue_lower, saturation_lower, value_lower])
        print(lower, upper)

        image_mask = cv2.inRange(image_hsv, lower, upper)
        cv2.imshow("Mask", image_mask)


def main():
    global image_hsv, pixel

    if len(sys.argv) < 2:
        print("Usage: python pick_color.py <image_path>")
        sys.exit()
    image_path = sys.argv[1]

    image_src = cv2.imread(image_path)
    cv2.imshow("BGR", image_src)

    image_hsv = cv2.cvtColor(image_src, cv2.COLOR_BGR2HSV)
    cv2.imshow("HSV", image_hsv)

    cv2.setMouseCallback("HSV", pick_color)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
