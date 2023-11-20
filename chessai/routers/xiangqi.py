import io

from fastapi import APIRouter, Response

from chessai import global_data
from chessai.game_state import GameState, Player


router = APIRouter(
    prefix="/api/xiangqi",
    tags=["XiangQi APIs"],
)


@router.post("/new_game", response_class=Response)
async def new_game():
    with global_data.game_lock:
        global_data.game_state = GameState(global_data.board_array, Player.RED)
    return Response(
        content="OK",
        media_type="text/plain",
    )


@router.get("/get_hint")
async def get_hint():
    best_move = global_data.chess_engine.get_move(global_data.board_array)
    global_data.hint_move = best_move
    print("Hint move:", best_move)
    return {
        "best_move": best_move,
    }
