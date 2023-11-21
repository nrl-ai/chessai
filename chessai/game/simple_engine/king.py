from .piece import Piece


class King(Piece):
    def __init__(self, position, team, board, type="k"):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.notation = "G"

    def get_possible_moves(self, board):
        moves = []
        # King can only move orthogonally in palace
        positions = {
            "b": [
                (0, 3),
                (0, 4),
                (0, 5),
                (1, 3),
                (1, 4),
                (1, 5),
                (2, 3),
                (2, 4),
                (2, 5),
            ],
            "r": [
                (9, 3),
                (9, 4),
                (9, 5),
                (8, 3),
                (8, 4),
                (8, 5),
                (7, 3),
                (7, 4),
                (7, 5),
            ],
        }
        for x, y in positions[self.team]:
            if (
                board.get_piece((x, y)) == None
                or board.get_piece((x, y)).team != self.team
            ) and (self.x - x) ** 2 + (self.y - y) ** 2 == 1:
                moves.append((x, y))

        return moves
