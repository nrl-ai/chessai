import subprocess
from chessai.game_state import GameState, Player


class ChessEngine:
    MAX_RESTART_TIMES = 10
    def __init__(self, engine_path):
        self.engine_path = engine_path
        self._engine_process = self.open_engine(engine_path)
        self.current_fen = "startpos"
        self.current_time_limit = 2000
        self.engine_restart_times = 0

    @property
    def engine_process(self):
        """Returns the engine process. If it is not running, it will be started."""
        if self._engine_process is None or self._engine_process.poll() is not None:
            if self._engine_process.poll() is not None:
                print("There was an error with the engine or there was a wrong move.")
                # error = self._engine_process.stderr.read().decode()
                # print(error)
            print("Engine is not running, starting it...")
            if self.engine_restart_times >= self.MAX_RESTART_TIMES:
                raise Exception("Engine is not running.")
            self._engine_process = self.open_engine(self.engine_path)
            self._engine_process.stdin.write(f"position fen {self.current_fen}\n".encode())
            self._engine_process.stdin.write(f"go movetime {self.current_time_limit}\n".encode())
            self._engine_process.stdin.flush()
            self.engine_restart_times += 1
        return self._engine_process

    @staticmethod
    def open_engine(engine_path):
        """Prepares the engine for use."""
        engine_process = subprocess.Popen(
            engine_path, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        return engine_process

    def engine_write(self, command):
        """Sends a command to the engine."""
        command = f"{command}\n".encode()
        self.engine_process.stdin.write(command)
        self.engine_process.stdin.flush()

    def engine_read(self, timeout=1000):
        """Reads the engine output."""
        text = ""
        while True:
            if self.engine_process.poll() is None:
                text = self.engine_process.stdout.read().decode()
                if text != "":
                    break
        return text

    @staticmethod
    def board_array_to_fen(board_array, next_player):
        """Converts a board array to a FEN string."""
        fen = ""
        for row in board_array:
            empty = 0
            for square in row:
                if square == "":
                    empty += 1
                else:
                    if empty != 0:
                        fen += str(empty)
                        empty = 0
                    is_red = square[0] == "r"
                    fen += square[1].upper() if is_red else square[1].lower()
            if empty != 0:
                fen += str(empty)
            fen += "/"

        player_str = "w" if next_player == Player.RED else "b"
        return fen[:-1] + f" {player_str} - - 0 1"

    def get_move(self, game_state, time_limit=2000):
        """Returns the best move for the given board array."""
        board_array = game_state.board
        next_player = game_state.next_player
        fen = self.board_array_to_fen(board_array, next_player)
        self.engine_write(f"position fen {fen}")
        self.engine_write(f"go movetime {time_limit}")
        self.current_fen = fen
        self.current_time_limit = time_limit

        best_move = None
        while True:
            if self.engine_process.poll() is None:
                text = self.engine_process.stdout.readline().decode()
                if text.startswith("bestmove"):
                    best_move = text.split(" ")[1]
                    break
            else:
                print("Engine is not running...")
                break

        return best_move
