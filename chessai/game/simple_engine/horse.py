from .piece import Piece


class Horse(Piece):
    def __init__(self, position, team, board, type="h"):
        super().__init__(position, team, board, type)
        self.poistion = position
        self.x, self.y = position
        self.notation = "H"

    def get_possible_moves(self, board):
        moves = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if i**2 + j**2 == 5 and board.on_board(
                    (self.x + i, self.y + j)
                ):
                    if (
                        board.get_piece((self.x + i, self.y + j)) == None
                        or board.get_piece((self.x + i, self.y + j)).team
                        != self.team
                    ):
                        if i**2 == 4 and not board.get_piece(
                            (self.x + i // 2, self.y)
                        ):
                            moves.append((self.x + i, self.y + j))
                        elif j**2 == 4 and not board.get_piece(
                            (self.x, self.y + j // 2)
                        ):
                            moves.append((self.x + i, self.y + j))

        return moves
