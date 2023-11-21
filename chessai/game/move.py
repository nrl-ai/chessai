class Move:
    def __init__(self, from_pos: tuple, to_pos: tuple):
        self.from_pos = from_pos
        self.to_pos = to_pos

    @staticmethod
    def from_str(move_str):
        if len(move_str) != 4:
            raise ValueError("Invalid move string")
        from_x = ord(move_str[0]) - ord("a")
        from_y = int(move_str[1])
        to_x = ord(move_str[2]) - ord("a")
        to_y = int(move_str[3])
        return Move((from_x, from_y), (to_x, to_y))
