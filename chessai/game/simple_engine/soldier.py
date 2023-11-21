from .piece import Piece


class Soldier(Piece):
    def __init__(self, position, team, board, type="s"):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.notation = "S"

    def get_possible_moves(self, board):
        moves = []

        # black and red Soldiers have different directions
        if self.team == "b":
            l = (
                [
                    (self.x + 1, self.y),
                    (self.x, self.y - 1),
                    (self.x, self.y + 1),
                ]
                if self.x >= 5
                else [(self.x + 1, self.y)]
            )
            for x, y in l:
                if board.on_board((x, y)) and (
                    board.get_piece((x, y)) == None
                    or board.get_piece((x, y)).team != self.team
                ):
                    moves.append((x, y))
        else:
            l = (
                [
                    (self.x - 1, self.y),
                    (self.x, self.y - 1),
                    (self.x, self.y + 1),
                ]
                if self.x <= 4
                else [(self.x - 1, self.y)]
            )
            for x, y in l:
                if board.on_board((x, y)) and (
                    board.get_piece((x, y)) == None
                    or board.get_piece((x, y)).team != self.team
                ):
                    moves.append((x, y))
        return moves
