from .piece import Piece


class Advisor(Piece):
    def __init__(self, position, team, board, type="a"):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.notation = "A"

    def get_possible_moves(self, board):
        moves = []
        # advisor can only move diagonally in palace
        positions = {
            "b": [(0, 3), (0, 5), (1, 4), (2, 3), (2, 5)],
            "r": [(9, 3), (9, 5), (8, 4), (7, 3), (7, 5)],
        }
        for x, y in positions[self.team]:
            if (
                (
                    board.get_piece((x, y)) == None
                    or board.get_piece((x, y)).team != self.team
                )
                and y != self.y
                and abs(self.y - y) == 1
            ):
                moves.append((x, y))
        return moves
