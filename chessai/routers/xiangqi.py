from fastapi import APIRouter, Response

from chessai import globals
import cv2


DEFAULT_VISUALIZATION_FRAME = cv2.imread(
    "data/default_visualization_frame.jpeg"
)

router = APIRouter(
    prefix="/api/xiangqi",
    tags=["Run services"],
)


def encode_image(image):
    _, buffer = cv2.imencode(".jpg", image)
    return buffer.tobytes()


@router.get("/original_frame", response_class=Response)
async def original_frame():
    with globals.frame_lock:
        frame = None
        if globals.original_frame is None:
            frame = DEFAULT_VISUALIZATION_FRAME
        else:
            frame = globals.original_frame
        encoded_frame = encode_image(frame)
        return Response(
            content=encoded_frame,
            media_type="image/jpg",
        )


@router.get("/debug_frame", response_class=Response)
async def debug_frame():
    with globals.frame_lock:
        frame = None
        if globals.debug_frame is None:
            frame = DEFAULT_VISUALIZATION_FRAME
        else:
            frame = globals.debug_frame
        encoded_frame = encode_image(frame)
        return Response(
            content=encoded_frame,
            media_type="image/jpg",
        )


@router.get("/visualization_frame", response_class=Response)
async def visualization_frame():
    with globals.frame_lock:
        frame = None
        if globals.visualization_frame is None:
            frame = DEFAULT_VISUALIZATION_FRAME
        else:
            frame = globals.visualization_frame
        encoded_frame = encode_image(frame)
        return Response(
            content=encoded_frame,
            media_type="image/jpg",
        )
