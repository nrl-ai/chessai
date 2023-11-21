from .piece import Piece


class Bishop(Piece):
    def __init__(self, position, team, board, type="b"):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.notation = "B"

    def get_possible_moves(self, board):
        # Elephant's movement is restricted to only 7 board positions
        positions = {
            "b": [(0, 2), (0, 6), (2, 0), (2, 4), (2, 8), (4, 2), (4, 6)],
            "r": [(9, 2), (9, 6), (7, 0), (7, 4), (7, 8), (5, 2), (5, 6)],
        }
        moves = []
        for x, y in positions[self.team]:
            if (
                (
                    board.get_piece((x, y)) == None
                    or board.get_piece((x, y)).team != self.team
                )
                and x != self.x
                and y != self.y
                and abs(self.y - y) == 2
                and not board.get_piece(((self.x + x) // 2, (self.y + y) // 2))
            ):
                moves.append((x, y))

        return moves
