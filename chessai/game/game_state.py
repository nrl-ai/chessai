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
        return game_engine.check_move(move)

