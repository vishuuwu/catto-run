# Configuration constants for Catto-Run game

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 793
FPS = 60

# Asset folders
ASSET_DIR = "./"
LAYER_DIR = "layers"
SPRITE_DIR = "sprite"
COIN_DIR = "coins"

# Gameplay constants
PLAYER_START_X = 100
PLAYER_START_Y = 473  # calculated from asset sizes
PLAYER_GRAVITY = 0.3
PLAYER_JUMP_STRENGTH = 10

COIN_SPAWN_DELAY_MS = 4000
COIN_SCORE_VALUE = 5

# Parallax
LAYER_SCROLL_VELOCITIES = [0, 0.1, 0.2, 0.25, 0.3, 0.35, 0.55, 0.7, 0.8, 0.8, 1, 1]
MAX_SCROLL_SPEED = 8
ACCELERATION = 0.2
