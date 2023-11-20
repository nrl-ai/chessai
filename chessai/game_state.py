class Player:
    RED = "red"
    BLACK = "black"

class GameState:
    def __init__(self, board, next_player=Player.RED):
        self.board = board
        self.next_player = next_player
        self.moves = []
