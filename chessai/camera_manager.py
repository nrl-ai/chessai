import logging
import time
import threading

import cv2

from chessai import global_data


def capture_loop():
    try:
        cap = cv2.VideoCapture(global_data.camera_id)
    except Exception as e:
        logging.error(e)
        return
    global_data.camera_is_running = True
    while True:
        if global_data.camera_shutdown_signal:
            global_data.camera_is_running = False
            break
        ret, frame = cap.read()
        # frame = cv2.flip(frame, 1)
        # if int(time.time()) % 4 < 2:
        #     frame = cv2.imread("test_board.png")
        # else:
        #     frame = cv2.imread("test_board2.png")
        if ret is False:
            global_data.camera_is_running = False
            break
        if frame is not None:
            with global_data.frame_lock:
                global_data.original_frame = frame
    global_data.camera_is_running = False


def stop_camera():
    if not global_data.camera_is_running:
        return False
    global_data.camera_shutdown_signal = True
    while global_data.camera_is_running:
        pass


def start_camera():
    if global_data.camera_is_running:
        return False
    global_data.camera_shutdown_signal = False
    global_data.camera_thread = threading.Thread(target=capture_loop)
    global_data.camera_thread.start()


def switch_camera(camera_id: int):
    if camera_id not in global_data.working_camera_ports:
        return False
    stop_camera()
    global_data.camera_id = camera_id
    start_camera()
