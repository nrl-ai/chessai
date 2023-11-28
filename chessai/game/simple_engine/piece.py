class Piece:
    def __init__(self, position, team, board, type):
        self.team = team
        self.type = type
        self.has_moved = False

    def get_possible_moves(self, board):
        pass

    """ Only valid moves are taken into account
    To sort moves that are valid, perform a fake move first and check if team's king 
    is in check or not"""

    def get_valid_moves(self, board):
        valid_moves = []
        possible_moves = self.get_possible_moves(board)
        for goal_x, goal_y in possible_moves:
            captured = board.get_piece((goal_x, goal_y))
            board.set_piece((goal_x, goal_y), self)
            board.set_piece((self.x, self.y), None)
            if (
                not board.is_in_check(self.team)
                and not board.king_face_each_other()
            ):
                valid_moves.append((goal_x, goal_y))
            board.set_piece((goal_x, goal_y), captured)
            board.set_piece((self.x, self.y), self)
        return valid_moves

    def move(self, board, coords: tuple):
        captured = board.get_piece((coords[0], coords[1]))
        board.set_piece((coords[0], coords[1]), self)
        board.set_piece((self.x, self.y), None)
        self.x, self.y = coords
        return captured
