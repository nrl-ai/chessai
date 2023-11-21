from .piece import Piece


class Cannon(Piece):
    def __init__(self, position, team, board, type="c"):
        super().__init__(position, team, board, type)
        self.position = position
        self.x, self.y = position
        self.notation = "C"

    def get_possible_moves(self, board):
        moves = []

        cross = [
            [[self.x + i, self.y] for i in range(1, 10 - self.x)],
            [[self.x - i, self.y] for i in range(1, self.x + 1)],
            [[self.x, self.y + i] for i in range(1, 9 - self.y)],
            [[self.x, self.y - i] for i in range(1, self.y + 1)],
        ]

        for direction in cross:
            may_jump = False
            for positions in direction:
                if board.on_board(positions):
                    if (
                        board.get_piece((positions[0], positions[1])) == None
                        and not may_jump
                    ):
                        moves.append((positions[0], positions[1]))
                    elif (
                        board.get_piece((positions[0], positions[1]))
                        and not may_jump
                    ):
                        may_jump = True
                    elif (
                        board.get_piece((positions[0], positions[1]))
                        and may_jump
                    ):
                        if (
                            board.get_piece((positions[0], positions[1])).team
                            != self.team
                        ):
                            moves.append((positions[0], positions[1]))
                        break
        return moves
