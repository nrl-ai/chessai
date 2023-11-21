from fastapi import APIRouter, Response
from pydantic import BaseModel

from chessai import global_data
from chessai.game.game_state import GameState, Player


router = APIRouter(
    prefix="/api/xiangqi",
    tags=["XiangQi APIs"],
)

@router.get("/current_game")
async def current_game():
    return {
        "is_playing": global_data.game_state is not None,
        "next_player": global_data.game_state.next_player,
    }

class NewGameRequest(BaseModel):
    next_player: str

@router.post("/new_game", response_class=Response)
async def new_game(data: NewGameRequest):
    with global_data.game_lock:
        global_data.game_state = GameState(global_data.board_array, Player.RED if data.next_player == "r" else Player.BLACK)
    return Response(
        content="OK",
        media_type="text/plain",
    )

@router.get("/get_hint")
async def get_hint():
    best_move = global_data.chess_engine.get_move(global_data.game_state)
    global_data.game_state.hint_move = best_move
    print("Hint move:", best_move)
    return {
        "best_move": best_move,
    }
