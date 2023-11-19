import io

from fastapi import APIRouter, Response
from starlette.responses import StreamingResponse

from chessai import globals
from chessai.utils import encode_image, original_frame_stream
from chessai.config import DEFAULT_VISUALIZATION_FRAME


router = APIRouter(
    prefix="/api/xiangqi",
    tags=["Run services"],
)


@router.get("/original_frame", response_class=Response)
async def original_frame():
    return StreamingResponse(original_frame_stream(), media_type="multipart/x-mixed-replace;boundary=frame")

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

