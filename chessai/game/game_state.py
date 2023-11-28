from copy import deepcopy
from .simple_engine.simple_engine import SimpleEngine


class Player:
    RED = "r"
    BLACK = "b"

class GameState:
    def __init__(self, board, next_player=Player.RED):
        self.board = board
        self.next_player = next_player
        self.moves = []
        self.hint_move = None

    def is_checkmate(self):
        game_engine = SimpleEngine(self.board, self.next_player)
        return game_engine.is_checkmate()

    def check_move(self, move):
        game_engine = SimpleEngine(self.board, self.next_player)
        print("Checking move: ", move.from_pos, move.to_pos)
        return game_engine.check_move(move.from_pos, move.to_pos)

    def copy(self):
        new_state = GameState(deepcopy(self.board), self.next_player)
        new_state.moves = self.moves.copy()
        new_state.hint_move = self.hint_move
        return new_state
