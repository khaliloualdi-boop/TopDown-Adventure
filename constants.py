from enum import Enum


WINDOW_TITLE = "Adventure"
"""Title of the main window."""

SCALE = 2.0
"""The global scale for all textures."""

TILE_SIZE = 32
"""After scaling, the size of a tile."""

MAX_WINDOW_WIDTH = 14 * TILE_SIZE
MAX_WINDOW_HEIGHT = 14 * TILE_SIZE

PLAYER_MOVEMENT_SPEED = 4
"""Vitesse du joueur en pixel par frames."""

class Direction (Enum):
    SUD = 0
    NORD = 1
    EST = 2
    OUEST = 3

SPINNER_SPEED = 3

BOOMERANG_SPEED = 8

BAT_SPEED = 4

BLOB_SPEED = 1

MONSTER_DEATH_DURATION = 0.79

SWORD_ATTACK_DURATION = 0.3

HOLE_FALL_DISTANCE = TILE_SIZE//2

SWITCH_SCALE = 0.25



def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)

def pixel_to_grid(i: float) -> int:
    return int(i  // TILE_SIZE)
