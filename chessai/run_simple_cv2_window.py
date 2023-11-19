import sys
import cv2
import os
import imutils

sys.path.append(".")

from chessai import config, utils
from chessai.board_aligner import BoardAligner
from chessai.piece_detector import PieceDetector
from chessai.chess_engine import ChessEngine
from chessai.visualization import draw_board_canvas

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
chess_engine = ChessEngine(engine_path)

try:
    cap = cv2.VideoCapture(1)
except:
    print("Check camera connection")
    input()
    sys.exit(0)

global_message = "ChessAI - Development Version"
button_pos = None
while True:
    ret, frame = cap.read()
    frame = cv2.imread("test_board.png")
    if ret is False:
        print("Check camera connection")
        input()
        sys.exit(0)
    if frame is not None:
        original_frame_viz = frame.copy()
        is_cropped, board_image = aligner.process(frame, visualize=original_frame_viz)
        board_image_viz = board_image.copy()
        board_array = piece_detector.detect(board_image, visualize=board_image_viz)

        # Two images on the top
        target_height = 640
        original_frame_viz = imutils.resize(original_frame_viz, height=target_height)
        board_image_viz = imutils.resize(board_image_viz, height=target_height)
        top_row = cv2.hconcat([board_image_viz, original_frame_viz])

        # Visualize the board
        board_canvas = draw_board_canvas(board_array)
        board_canvas = imutils.resize(board_canvas, height=target_height)

        # Draw the message box (bottom right)
        message_frame = utils.draw_message_box(
            board_canvas.shape[1], board_canvas.shape[0], global_message
        )

        # Two images on the bottom
        bottom_row = cv2.hconcat([board_canvas, message_frame])

        # Combine the two rows
        bottom_row = imutils.resize(bottom_row, width=top_row.shape[1])
        viz_image = cv2.vconcat([top_row, bottom_row])
        viz_image = cv2.copyMakeBorder(
            viz_image, 0, 0, 200, 200, cv2.BORDER_CONSTANT, None, (0, 0, 0)
        )

        cv2.imshow("ChessAI", viz_image)
        k = cv2.waitKey(1)
        if k == 27:
            should_exit = True
            sys.exit(0)
        elif k == ord("m"):  # Move
            best_move = chess_engine.get_move(board_array)
            print(best_move)
    else:
        print("No frame")
        break

cap.release()
cv2.destroyAllWindows()
