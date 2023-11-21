from .piece_factory import PieceFactory
from .piece import Piece
from .rook import Rook
from .knight import Knight
from .king import King
from .cannon import Cannon
from .pawn import Pawn
from .advisor import Advisor
from .bishop import Bishop


class SimpleEngine:
    def __init__(self, board, current_turn="r"):
        self.current_turn = current_turn
        self.config = [[None for i in range(9)] for i in range(10)]
        if board:
            self.load_board(board)
        else:
            self.setup_new_board()

    def load_board(self, board):
        """Load board from board matrix"""
        for row in range(10):
            for col in range(9):
                piece = board[row][col]
                if piece:
                    piece_class = PieceFactory.get_piece_class(piece[1])
                    self.config[row][col] = piece_class(
                        (row, col), piece[0], self, piece[1]
                    )
                else:
                    self.config[row][col] = None

    def setup_new_board(self):
        self.config[0] = [
            Rook((0, 0), "b", self),
            Knight((0, 1), "b", self),
            Bishop((0, 2), "b", self),
            Advisor((0, 3), "b", self),
            King((0, 4), "b", self),
            Advisor((0, 5), "b", self),
            Bishop((0, 6), "b", self),
            Knight((0, 7), "b", self),
            Rook((0, 8), "b", self),
        ]
        self.config[2] = [
            None,
            Cannon((2, 1), "b", self),
            None,
            None,
            None,
            None,
            None,
            Cannon((2, 7), "b", self),
            None,
        ]

        self.config[9] = [
            Rook((9, 0), "r", self),
            Knight((9, 1), "r", self),
            Bishop((9, 2), "r", self),
            Advisor((9, 3), "r", self),
            King((9, 4), "r", self),
            Advisor((9, 5), "r", self),
            Bishop((9, 6), "r", self),
            Knight((9, 7), "r", self),
            Rook((9, 8), "r", self),
        ]
        self.config[7] = [
            None,
            Cannon((7, 1), "r", self),
            None,
            None,
            None,
            None,
            None,
            Cannon((7, 7), "r", self),
            None,
        ]

        for i in range(0, 9, 2):
            self.config[3][i] = Pawn((3, i), "b", self)
            self.config[6][i] = Pawn((6, i), "r", self)

    def get_piece(self, pos: tuple) -> Piece:
        return self.config[pos[0]][pos[1]]

    def set_piece(self, pos: tuple, piece: Piece):
        self.config[pos[0]][pos[1]] = piece

    def on_board(self, position: tuple) -> bool:
        if (
            position[0] > -1
            and position[1] > -1
            and position[0] < 10
            and position[1] < 9
        ):
            return True

    def is_in_check(self, team: str) -> bool:
        if team != self.current_turn:
            return False
        king_pos = self.find_king(team)
        # opponent's all possible moves:
        for row in self.config:
            for piece in row:
                if piece and piece.team != team:
                    if king_pos in piece.get_possible_moves(self):
                        return True
        return False

    def is_checkmate(self):
        for row in self.config:
            for piece in row:
                if piece and piece.team == self.current_turn:
                    if piece.get_valid_moves(self):
                        return False
        return True

    def find_king(self, team: str):
        for i in range(10):
            for j in range(9):
                piece = self.config[i][j]
                if piece and piece.team == team and piece.type == "k":
                    return (i, j)

    def king_face_each_other(self) -> bool:
        red_king_pos = self.find_king("r")
        black_king_pos = self.find_king("b")
        if red_king_pos[1] != black_king_pos[1]:
            return False
        return all(
            not self.config[x][red_king_pos[1]]
            for x in range(black_king_pos[0] + 1, red_king_pos[0])
        )

    def find_node(self, pos: tuple, WIDTH):
        interval = WIDTH // 9
        y, x = pos
        rows = y // interval
        columns = x // interval
        return int(rows), int(columns)

    def check_move(self, from_pos, to_pos):
        if self.is_checkmate():
            return False
        from_x, from_y = from_pos
        piece = self.config[from_x][from_y]
        if piece and piece.team != self.current_turn:
            return False
        possible_moves = piece.get_valid_moves(self)
        if to_pos in possible_moves:
            return True
        return False

    def move(self, from_pos, to_pos):
        if not self.check_move(from_pos, to_pos):
            return False
        from_x, from_y = from_pos
        chess_piece = self.config[from_x][from_y]
        chess_piece.move(self, to_pos)
        self.current_turn = "b" if self.current_turn == "r" else "r"
        return True

    def get_game_state(self):
        return [
            self.possible_moves,
            self.from_pos,
            self.last_pos,
        ]

    def convert_to_readable(self):
        output = ""
        for i in self.config:
            for j in i:
                try:
                    output += j.team + j.type + ", "
                except:
                    output += "  , "
            output += "\n"
        return output
