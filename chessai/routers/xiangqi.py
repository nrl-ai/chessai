from fastapi import APIRouter, Response
from pydantic import BaseModel

from chessai import global_data
from chessai.game.game_state import GameState, Player
from chessai.game.move import Move

router = APIRouter(
    prefix="/api/xiangqi",
    tags=["XiangQi APIs"],
)

@router.get("/current_game")
async def current_game():
    return {
        "is_playing": global_data.game_state is not None,
        "next_player": global_data.game_state.next_player if global_data.game_state is not None else None,
    }

class NewGameRequest(BaseModel):
    next_player: str

@router.post("/new_game", response_class=Response)
async def new_game(data: NewGameRequest):
    with global_data.game_lock:
        global_data.game_state = GameState(global_data.board_array, Player.RED if data.next_player == "r" else Player.BLACK)
        global_data.prev_game_state = global_data.game_state
    return Response(
        content="OK",
        media_type="text/plain",
    )

@router.post("/play")
async def play():
    if global_data.game_state is None:
        return {
            "success": False,
            "message": "Game not started",
        }
    if global_data.game_state.is_checkmate():
        return {
            "success": False,
            "message": "Checkmate",
        }
    with global_data.game_lock:
        prev_game_state = global_data.prev_game_state.copy()
        game_state = global_data.game_state.copy()
    move = Move.from_game_states(prev_game_state, game_state)
    if move is None:
        return {
            "success": False,
            "message": "Invalid move",
        }
    with global_data.game_lock:
        global_data.prev_game_state = game_state
        global_data.game_state.hint_move = None
    return {
        "success": True,
        "move": str(move),
    }

@router.get("/get_hint")
async def get_hint():
    if global_data.game_state is None:
        return {
            "success": False,
            "message": "Game not started",
        }
    if global_data.game_state.is_checkmate():
        return {
            "success": False,
            "message": "Checkmate",
        }
    best_move = global_data.chess_engine.get_move(global_data.game_state)
    global_data.game_state.hint_move = best_move
    print("Hint move:", best_move)
    return {
        "best_move": best_move,
    }
