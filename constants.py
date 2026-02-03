# constants.py

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Аркадные Гонки"


CAMERA_LERP = 0.1  # Плавность камеры (меньше = плавнее)

TEXTURE_CHANGE_DELAY = 0.1


PLAYER_SPEED = 6.0
PLAYER_SCALE = 0.5
# TRACK 1
PLAYER1_START_X_TRACK_1 = 1024
PLAYER1_START_Y_TRACK_1 = 80

PLAYER2_START_X_TRACK_1 = 1088
PLAYER2_START_Y_TRACK_1 = 112
# TRACK 2
PLAYER1_START_X_TRACK_2 = 256
PLAYER1_START_Y_TRACK_2 = 851

PLAYER2_START_X_TRACK_2 = 320
PLAYER2_START_Y_TRACK_2 = 883
# TRACK 3
PLAYER1_START_X_TRACK_3 = 96
PLAYER1_START_Y_TRACK_3 = 80

PLAYER2_START_X_TRACK_3 = 160
PLAYER2_START_Y_TRACK_3 = 112

MIN_ZOOM = 1.2   # На максимальной скорости (отдаление)
MAX_ZOOM = 2   # В покое (приближение)
ZOOM_LERP = 0.01 # Плавность изменения зума (меньше = медленнее)


LEVELS = [
    {
        "map_path": "tmx_files/track1.tmx",
        "track_id": 1, 
        "start_x": 1056,
        "start_y": 80,
        "start_angle": 90,
        "finish_dir": (1, 0)
    },
    {
        "map_path": "tmx_files/track2.tmx",
        "track_id": 2,
        "start_x": 482, "start_y": 883, "start_angle": 90,
        "finish_dir": (1, 0), 
        "world_width": 3200,
        "world_height": 1920
    },
    {
        "map_path": "tmx_files/track3.tmx",
        "track_id": 3,
        "start_x": 112, "start_y": 80, "start_angle": 90,
        "finish_dir": (1, 0), 
        "world_width": 3200,
        "world_height": 1920
    },
]

