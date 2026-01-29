# constants.py

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
SCREEN_TITLE = "Аркадные Гонки"


CAMERA_LERP = 0.1  # Плавность камеры (меньше = плавнее)


PLAYER_SPEED = 6.0
PLAYER_SCALE = 0.5
# TRACK 1
PLAYER_START_X_TRACK_1 = 1056
PLAYER_START_Y_TRACK_1 = 80
# TRACK 2
PLAYER_START_X_TRACK_2 = 482
PLAYER_START_Y_TRACK_2 = 883

MIN_ZOOM = 1.2   # На максимальной скорости (отдаление)
MAX_ZOOM = 2   # В покое (приближение)
ZOOM_LERP = 0.02 # Плавность изменения зума (меньше = медленнее)


LEVELS = [
    {
        "map_path": "tmx_files/track1.tmx",
        "track_id": 1,
        "world_width": 3200,
        "world_height": 1920
    },
    {
        "map_path": "tmx_files/track2.tmx",
        "track_id": 2,
        "world_width": 3200,
        "world_height": 1920
    }
]