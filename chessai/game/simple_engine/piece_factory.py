from .rook import Rook
from .knight import Knight
from .king import King
from .cannon import Cannon
from .pawn import Pawn
from .advisor import Advisor
from .bishop import Bishop

class PieceFactory:

    @staticmethod
    def get_piece_class(notation):
        if notation == "r":
            return Rook
        elif notation == "n":
            return Knight
        elif notation == "b":
            return Bishop
        elif notation == "a":
            return Advisor
        elif notation == "k":
            return King
        elif notation == "c":
            return Cannon
        elif notation == "p":
            return Pawn
        else:
            return None
