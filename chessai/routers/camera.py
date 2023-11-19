from fastapi import APIRouter
from pydantic import BaseModel

from chessai import global_data
from chessai.camera_manager import start_camera, stop_camera, switch_camera


router = APIRouter(
    prefix="/api/camera",
    tags=["Camera APIs"],
)


@router.get("/list")
async def list_camera_ports():
    return {
        "success": True,
        "is_camera_running": global_data.camera_is_running,
        "selected_camera_port": global_data.camera_id,
        "available_camera_ports": global_data.working_camera_ports
    }

class CameraSwitchRequest(BaseModel):
    camera_id: int

@router.post("/switch")
async def switch(data: CameraSwitchRequest):
    if data.camera_id not in global_data.working_camera_ports:
        return {
            "success": False,
            "message": "Camera port not found."
        }
    switch_camera(data.camera_id)
    return {
        "success": True,
        "message": "Camera switched."
    }


@router.post("/reset")
async def reset():
    stop_camera()
    start_camera()
    return {
        "success": True,
        "message": "Camera reset."
    }
