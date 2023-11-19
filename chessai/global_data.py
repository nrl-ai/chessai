from threading import Lock

environment = "local" # local or extension
data_root = None

working_camera_ports = []
camera_id = 1
camera_thread = None
camera_is_running = False
camera_shutdown_signal = False
frame_lock = Lock()
original_frame = None
debug_frame = None
visualization_frame = None

board_lock = Lock()
board_array = None
