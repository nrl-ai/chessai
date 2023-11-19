import cv2
import numpy as np

def draw_message_box(width, height, message):
    """Draws a message box with the given width, height and message"""
    message_frame = np.zeros((height, width, 3), dtype=np.uint8)
    cv2.putText(
        message_frame,
        message,
        (50, 50),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 0, 255),
        2,
        cv2.LINE_AA,
    )
    return message_frame
