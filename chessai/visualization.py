import cv2
import numpy as np

from chessai.config import CELL_RECTANGLES

pieces = [
    "rr",
    "rn",
    "rb",
    "ra",
    "rk",
    "rc",
    "rp",
    "br",
    "bn",
    "bb",
    "ba",
    "bk",
    "bc",
    "bp",
]

ref_board_image = cv2.imread("data/board.png")
ref_piece_images = {}
for p in pieces:
    ref_piece_images[p] = cv2.imread(f"data/pieces/{p}.png", cv2.IMREAD_UNCHANGED)


def overlay(background, overlay, x, y):
    background_width = background.shape[1]
    background_height = background.shape[0]

    if x >= background_width or y >= background_height:
        return background

    h, w = overlay.shape[0], overlay.shape[1]

    if x + w > background_width:
        w = background_width - x
        overlay = overlay[:, :w]

    if y + h > background_height:
        h = background_height - y
        overlay = overlay[:h]

    if overlay.shape[2] < 4:
        overlay = np.concatenate(
            [
                overlay,
                np.ones((overlay.shape[0], overlay.shape[1], 1), dtype=overlay.dtype)
                * 255,
            ],
            axis=2,
        )

    overlay_image = overlay[..., :3]
    mask = overlay[..., 3:] / 255.0

    background[y : y + h, x : x + w] = (1.0 - mask) * background[
        y : y + h, x : x + w
    ] + mask * overlay_image

    return background


def draw_board_canvas(board, hint_move=None):
    draw = ref_board_image.copy()
    for i in range(10):
        for j in range(9):
            x = j * 110 + 30
            y = i * 110 + 30
            if board[i][j]:
                draw = overlay(draw, ref_piece_images[board[i][j]], x, y)

    if hint_move:
        # Draw a hint move on the board
        from_x = (ord(hint_move[0]) - ord("a")) * 110 + 60
        from_y = (9 - int(hint_move[1])) * 110 + 60
        to_x = (ord(hint_move[2]) - ord("a")) * 110 + 60
        to_y = (9 - int(hint_move[3])) * 110 + 60
        draw = cv2.arrowedLine(
            draw,
            (from_x, from_y),
            (to_x, to_y),
            (255, 0, 0),
            10,
            tipLength=20.0/np.sqrt((to_x-from_x)**2+(to_y-from_y)**2),
        )
        draw = cv2.circle(draw, (to_x, to_y), 10, (0, 255, 0), -1)

    return draw
