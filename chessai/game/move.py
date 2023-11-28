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

    @staticmethod
    def from_game_states(prev_game_state, game_state):
        player = prev_game_state.next_player
        prev_board = prev_game_state.board
        board = game_state.board
        from_pos = None
        to_pos = None
        for y in range(10):
            for x in range(9):
                if prev_board[y][x] and prev_board[y][x][0] == player and not board[y][x]:
                    from_pos = (x, y)
                elif (not prev_board[y][x] or prev_board[y][x][0] != player) and board[y][x] and board[y][x][0] == player:
                    to_pos = (x, y)
        print(from_pos, to_pos)
        if from_pos is None or to_pos is None:
            return None
        if not game_state.check_move(Move(from_pos, to_pos)):
            return None
        return Move(from_pos, to_pos)

    def __str__(self):
        return chr(ord("a") + self.from_pos[0]) + str(self.from_pos[1]) + chr(ord("a") + self.to_pos[0]) + str(self.to_pos[1])
