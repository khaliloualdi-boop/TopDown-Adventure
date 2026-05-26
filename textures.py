from typing import Final
import arcade

ORIG_TILE_SIZE = (16, 16)

def _load_grid(
    file: str,
    columns: int,
    rows: int,
    tile_size: tuple[int, int] = ORIG_TILE_SIZE
) -> list[arcade.Texture]:
    """
    Loads a texture grid from a spritesheet.

    Args:
        file:
            Path to the spritesheet file name.
        columns:
            The number of columns in the grid.
        rows:
            The number of rows in the grid.
        tile_size (optional):
            The size in pixels of one element of the grid. Defaults to the
            standard tile size of `(16, 16)` that we use in our assets.

    Returns:
        A list of the loaded textures, flattened by row. The texture at grid
        coordinates `(x, y)` is at index `(y * columns) + x` in the list.
    """
    spritesheet = arcade.load_spritesheet(file)
    return spritesheet.get_texture_grid(tile_size, columns, columns * rows)

def _load_animation_strip(
    file: str,
    frame_count: int,
    frame_duration: int = 100,
    tile_size: tuple[int, int] = ORIG_TILE_SIZE,
) -> arcade.TextureAnimation:
    """
    Loads an animation strip from a line-oriented spritesheet.

    Args:
        file:
            Path to the spritesheet file name.
        frame_count:
            The number of frames in the animation, which should also be the
            number of sub-images in the file.
        frame_duration (optional):
            The duration of each frame in ms (defaults to 100).
        tile_size (optional):
            The size in pixels of one element of the grid, i.e.,  of a frame.
            Defaults to the standard tile size of `(16, 16)` that we use in our
            assets.

    Returns:
        An `arcade.TextureAnimation` representing the full animation.
    """
    grid = _load_grid(file, columns=frame_count, rows=1, tile_size=tile_size)
    keyframes = [arcade.TextureKeyframe(frame, frame_duration) for frame in grid]
    return arcade.TextureAnimation(keyframes)

_overworld_grid = _load_grid("assets/Top_Down_Adventure_Pack_v.1.0/Overworld_Tileset.png", 18, 13)

_dungeon_grid = _load_grid("assets/Top_Down_Adventure_Pack_v.1.0/Dungeon_Tileset.png",13, 12)

TEXTURE_GRASS: Final[arcade.Texture] = _overworld_grid[18*1 + 6]
TEXTURE_BUSH: Final[arcade.Texture] = _overworld_grid[18*3 + 5]
TEXTURE_HOLE: Final[arcade.Texture] = _overworld_grid[18*4 + 8]
TEXTURE_GATE_OPEN: Final[arcade.Texture] = _dungeon_grid[13*4 + 8]
TEXTURE_GATE_CLOSED: Final[arcade.Texture] = _dungeon_grid[13*7 + 8]
TEXTURE_DUNGEON_FLOOR: Final[arcade.Texture] = _dungeon_grid[13*11 + 4]
TEXTURE_DUNGEON_WALL:  Final[arcade.Texture] = _dungeon_grid[13*1 + 2]

# Idle animations :

ANIMATION_PLAYER_IDLE_DOWN: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_down_anim_strip_6.png", 6)

ANIMATION_PLAYER_IDLE_UP: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_up_anim_strip_6.png", 6)

ANIMATION_PLAYER_IDLE_RIGHT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_right_anim_strip_6.png", 6)

ANIMATION_PLAYER_IDLE_LEFT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_idle_left_anim_strip_6.png", 6)

IDLE_SPRITELIST = [
    ANIMATION_PLAYER_IDLE_DOWN,
    ANIMATION_PLAYER_IDLE_UP,
    ANIMATION_PLAYER_IDLE_RIGHT,
    ANIMATION_PLAYER_IDLE_LEFT
]


ANIMATION_CRISTAUX: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Props_Items_(animated)/crystal_item_anim_strip_6.png", 6)

# Running animations :

ANIMATION_PLAYER_RUN_DOWN: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_run_down_anim_strip_6.png", 6)
ANIMATION_PLAYER_RUN_UP: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_run_up_anim_strip_6.png", 6)
ANIMATION_PLAYER_RUN_RIGHT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_run_right_anim_strip_6.png", 6)
ANIMATION_PLAYER_RUN_LEFT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_run_left_anim_strip_6.png", 6)

ANIMATION_SPINNER: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Spinner_Sprites/spinner_run_attack_anim_all_dir_strip_8.png", 3)

DEATH_ANIMATION_SPINNER: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Spinner_Sprites/spinner_death_anim_all_dir_strip_8.png", 8)

RUNNING_SPRITELIST = [
    ANIMATION_PLAYER_RUN_DOWN,
    ANIMATION_PLAYER_RUN_UP,
    ANIMATION_PLAYER_RUN_RIGHT,
    ANIMATION_PLAYER_RUN_LEFT
]

ANIMATION_BOOMERANG: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/provided/boomerang-sheet.png", 8, 25)

ANIMATION_BAT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Pinkbat_Sprites/pinkbat_idle_left_anim_strip_5.png", 5)

DEATH_ANIMATION_BAT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Pinkbat_Sprites/pinkbat_death_anim_left_strip_8.png", 8)

# Sword attack animation:

ANIMATION_PLAYER_ATTACK_DOWN:Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_down_anim_strip_6.png", 6, 50, (48,48))
ANIMATION_PLAYER_ATTACK_UP:Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_up_anim_strip_6.png",6 ,50,(48,48))
ANIMATION_PLAYER_ATTACK_RIGHT:Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_right_anim_strip_6.png",6 ,50, (48,48))
ANIMATION_PLAYER_ATTACK_LEFT:Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Char_Sprites/char_attack48_left_anim_strip_6.png",6, 50, (48,48))

SWORD_ATTACK_LIST = [
    ANIMATION_PLAYER_ATTACK_DOWN,
    ANIMATION_PLAYER_ATTACK_UP,
    ANIMATION_PLAYER_ATTACK_RIGHT,
    ANIMATION_PLAYER_ATTACK_LEFT
]
ICON_BOOMERANG: Final[arcade.Texture] = _load_grid("assets/provided/boomerang-sheet.png", 8, 1)[0]
ICON_SWORD: Final[arcade.Texture] = arcade.load_texture("assets/Sword Icon from Project Plan.png")
ICON_ITEM_BOX: Final[arcade.Texture] = arcade.load_texture("assets/Top_Down_Adventure_Pack_v.1.0/Hud_Ui/item_box_hud.png")

ANIMATION_BLOB:  Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Pinkslime_Sprites/pinkslime_run_anim_anim_all_dir_strip_6.png", 6)


#textures de l'extension
ANIMATION_CHEST_OPENING: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Props_Items_(animated)/lootchest_item_anim_opening_strip_5.png", 5, 150)

ANIMATION_CHEST_IDLE: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Props_Items_(animated)/lootchest_item_anim_strip_8.png", 8, 100)

TEXTURE_CHEST_OPEN: Final[arcade.Texture] = \
    arcade.load_texture("assets/Top_Down_Adventure_Pack_v.1.0/Props_Items_(animated)/lootchest_item_static_open.png")


TEXTURE_HEALTH_BAR: Final[arcade.Texture] = \
    arcade.load_texture("assets/Top_Down_Adventure_Pack_v.1.0/Hud_Ui/health_bar_hud.png")

TEXTURE_HEALTH_HUB: Final[arcade.Texture] = \
    arcade.load_texture("assets/Top_Down_Adventure_Pack_v.1.0/Hud_Ui/health_hud.png")


ANIMATION_BOMBERPLANT_IDLE: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomberplant_idle_anim_all_dir_strip_5.png", 5)

ANIMATION_BOMBERPLANT_ATTACK: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomberplant_attack_anim_all_dir_strip_10.png", 10)

ANIMATION_BOMBERPLANT_HIT: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomberplant_hit_anim_all_dir_strip_4.png", 4)

ANIMATION_BOMBERPLANT_DEATH: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomberplant_death_anim_all_dir_strip_8.png", 8)

# Bomb animations
ANIMATION_BOMB_UP: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomb_going_up_anim_strip_4.png", 4)

ANIMATION_BOMB_DOWN: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomb_going_down_anim_strip_4.png", 4)

ANIMATION_BOMB_EXPLOSION: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomb_explosion_anim_strip_8.png", 8)

ANIMATION_BOMB_MARKER: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Bomberplant_Sprites/bomb_hit_marker_fx_anim_strip_4.png", 4)

DEATH_ANIMATION_BLOB: Final[arcade.TextureAnimation] = \
    _load_animation_strip("assets/Top_Down_Adventure_Pack_v.1.0/Enemies_Sprites/Pinkslime_Sprites/pinkslime_death_anim_all_dir_strip_8.png", 8)
