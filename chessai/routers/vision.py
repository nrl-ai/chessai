import io

from fastapi import APIRouter, Response
from starlette.responses import StreamingResponse

from chessai import global_data
from chessai.utils import encode_image, original_frame_stream
from chessai.config import DEFAULT_VISUALIZATION_FRAME


router = APIRouter(
    prefix="/api/vision",
    tags=["Vision APIs"],
)


@router.get("/original_frame", response_class=Response)
async def original_frame():
    return StreamingResponse(original_frame_stream(), media_type="multipart/x-mixed-replace;boundary=frame")

@router.get("/debug_frame", response_class=Response)
async def debug_frame():
    with global_data.frame_lock:
        frame = None
        if global_data.debug_frame is None:
            frame = DEFAULT_VISUALIZATION_FRAME
        else:
            frame = global_data.debug_frame
        encoded_frame = encode_image(frame)
        return Response(
            content=encoded_frame,
            media_type="image/jpg",
        )

@router.get("/visualization_frame", response_class=Response)
async def visualization_frame():
    with global_data.frame_lock:
        frame = None
        if global_data.visualization_frame is None:
            frame = DEFAULT_VISUALIZATION_FRAME
        else:
            frame = global_data.visualization_frame
        encoded_frame = encode_image(frame)
        return Response(
            content=encoded_frame,
            media_type="image/jpg",
        )

