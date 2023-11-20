import os
import sys
import argparse
import logging
import pathlib
import threading
import time

import cv2
import imutils

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from chessai.app_info import __appname__, __description__, __version__
from chessai import global_data
from chessai import config
from chessai.board_aligner import BoardAligner
from chessai.piece_detector import PieceDetector
from chessai.chess_engine import ChessEngine
from chessai.visualization import draw_board_canvas
from chessai.utils import list_camera_ports
from chessai.camera_manager import start_camera

aligner = BoardAligner(
    config.REFERENCE_ARUCO_IMAGE_PATH,
    debug=True,
    smooth=False,
)
piece_detector = PieceDetector(
    model_path=config.PIECE_DETECTION_MODEL_PATH,
    class_names_path=config.PIECE_DETECTION_CLASS_NAMES_PATH,
)

DEFAULT_ENGINE_PATH = "data/engines/godogpaw-macos-arm"
engine_path = os.environ.get("ENGINE_PATH", DEFAULT_ENGINE_PATH)
if not engine_path:
    print("ENGINE_PATH environment variable not set")
    sys.exit(0)
global_data.chess_engine = ChessEngine(engine_path)


def run_window():
    import webview
    webview.create_window("ChessAI - Chinese Chess Analyzer", 'http://127.0.0.1:3000', width=1200, height=800)
    webview.start()
    os._exit(0)

def chessai_process(frame):
    original_frame_viz = frame.copy()
    _, board_image = aligner.process(frame, visualize=original_frame_viz)
    board_image_viz = board_image.copy()
    board_array = piece_detector.detect(board_image, visualize=board_image_viz)
    with global_data.board_lock:
        global_data.board_array = board_array

    # Two images on the top
    target_height = 640
    original_frame_viz = imutils.resize(original_frame_viz, height=target_height)
    board_image_viz = imutils.resize(board_image_viz, height=target_height)
    top_row = cv2.hconcat([board_image_viz, original_frame_viz])
    with global_data.frame_lock:
        global_data.debug_frame = top_row

    # Visualize the board
    board_canvas = draw_board_canvas(board_array, global_data.hint_move)
    board_canvas = imutils.resize(board_canvas, height=target_height)
    with global_data.frame_lock:
        global_data.visualization_frame = board_canvas

def chessai_process_loop():
    while True:
        with global_data.frame_lock:
            frame = global_data.original_frame
        if frame is not None:
            chessai_process(frame)


def main():
    parser = argparse.ArgumentParser(
        description=__description__,
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Host to run the server on",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=5678,
        help="Port to run the server on",
    )
    parser.add_argument(
        "--version",
        action="store_true",
        help="Print version and exit",
    )
    parser.add_argument(
        "--data_root",
        default=os.path.abspath(
            os.path.join(os.path.expanduser("~"), "chessai-data")
        ),
    )
    parser.add_argument(
        "--environment",
        default="local",
    )
    parser.add_argument(
        "--run_app",
        default=False,
        action="store_true",
    )
    args = parser.parse_args()

    if args.version:
        print(f"{__appname__} v{__version__}")
        return

    logging.info(f"Starting {__appname__}...")
    logging.info(f"Version: {__version__}")

    logging.info(f"Environment: {args.environment}")
    global_data.environment = args.environment

    logging.info(f"Data root: {args.data_root}")
    global_data.data_root = args.data_root
    pathlib.Path(global_data.data_root).mkdir(parents=True, exist_ok=True)

    # Import these after setting data_root
    from chessai.routers import system_monitor, xiangqi, camera, vision
    from chessai.utils import extract_frontend_dist
    from chessai.database import engine, Base

    logging.info("Extracting frontend distribution...")
    static_folder = os.path.abspath(
        os.path.join(global_data.data_root, "frontend-dist")
    )
    extract_frontend_dist(static_folder)
    print(static_folder)


    logging.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)

    app = FastAPI(
        title=__appname__,
        description=__description__,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        expose_headers=["*"],
    )

    app.include_router(xiangqi.router)
    app.include_router(system_monitor.router)
    app.include_router(camera.router)
    app.include_router(vision.router)
    app.mount(
        "/", StaticFiles(directory=static_folder, html=True), name="static"
    )

    def run_webapp():
        uvicorn.run(app, host=args.host, port=args.port, workers=1)

    # Scan for available camera ports
    logging.info("Scanning for available camera ports...")
    _, global_data.working_camera_ports = list_camera_ports()
    if len(global_data.working_camera_ports) == 0:
        logging.error("No working camera ports found. Please check your camera.")
        return
    global_data.camera_id = global_data.working_camera_ports[0]

    # Start the chessai process loop
    thread = threading.Thread(target=chessai_process_loop)
    thread.start()

    # Start the capture loop
    start_camera()

    if args.run_app:
        # Run the app in a separate thread
        thread = threading.Thread(target=run_webapp)
        thread.start()
        time.sleep(3)

        # Run the window in the main thread
        run_window()
    else:
        run_webapp()



if __name__ == "__main__":
    main()
