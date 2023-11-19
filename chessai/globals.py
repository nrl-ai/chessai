from threading import Lock

environment = "local" # local or extension
data_root = None

camera_thread = None
frame_lock = Lock()
original_frame = None
debug_frame = None
visualization_frame = None
