from fastapi import APIRouter, Response

from chessai import globals
import cv2


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
        if globals.original_frame is None:
            return ""
        else:
            encoded_frame = encode_image(globals.original_frame)
            return Response(
                content=encoded_frame,
                media_type="image/jpg",
            )


@router.get("/debug_frame", response_class=Response)
async def debug_frame():
    with globals.frame_lock:
        if globals.debug_frame is None:
            return ""
        else:
            encoded_frame = encode_image(globals.debug_frame)
            return Response(
                content=encoded_frame,
                media_type="image/jpg",
            )


@router.get("/visualization_frame", response_class=Response)
async def visualization_frame():
    with globals.frame_lock:
        if globals.visualization_frame is None:
            return ""
        else:
            encoded_frame = encode_image(globals.visualization_frame)
            return Response(
                content=encoded_frame,
                media_type="image/jpg",
            )

