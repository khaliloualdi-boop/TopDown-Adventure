from map import Map, GridCell
from parsing import parse_map_doc
from spinner import *
from monster import *


def make_spinner(cx: float, cy: float, is_horizontal: bool,
                  min_pos: int = 1, max_pos: int = 5) -> Spinner:
    """Crée un Spinner factice sans Arcade."""
    s = object.__new__(Spinner)
    s._position = (cx, cy)
    s._velocity = (0.0, 0.0)
    s.is_horizontal = is_horizontal
    s.limits = SpinnerLimits(min_pos, max_pos)
    s.death_state = MonsterState.alive
    s.death_timer = 0.0
    if is_horizontal:
        s.change_x = SPINNER_SPEED
        s.change_y = 0
    else:
        s.change_x = 0
        s.change_y = SPINNER_SPEED
    return s


# Vérifie les limites d'un spinner horizontal entre deux buissons
def test_horizontal_limits() -> None:
    doc = (
        "width: 5\n"
        "height: 3\n"
        "theme: overworld\n"
        "---\n"
        "xxxxx\n"
        "xPs x\n"
        "xxxxx\n"
    )
    game_map = parse_map_doc(doc)
    limits = compute_limits(game_map, 2, 1, True)
    assert limits.min_pos == 1
    assert limits.max_pos == 3


# Vérifie les limites d'un spinner vertical entre deux buissons
def test_vertical_limits() -> None:
    doc = (
        "width: 3\n"
        "height: 5\n"
        "theme: overworld\n"
        "---\n"
        "xxx\n"
        "xSx\n"
        "xPx\n"
        "x x\n"
        "xxx\n"
    )
    game_map = parse_map_doc(doc)
    limits = compute_limits(game_map, 1, 3, False)
    assert limits.min_pos == 1
    assert limits.max_pos == 3


# Vérifie que le spinner horizontal rebondit sur la limite gauche
def test_spinner_horizontal_bounces_on_left_limit() -> None:
    s = make_spinner(
        cx=grid_to_pixels(1) - 1,
        cy=100.0,
        is_horizontal=True,
        min_pos=1, max_pos=5
    )
    s.change_x = -SPINNER_SPEED
    s._position = (s.center_x + s.change_x, s.center_y + s.change_y)
    if s.center_x < grid_to_pixels(s.limits.min_pos):
        s._position = (grid_to_pixels(s.limits.min_pos), s.center_y)
        s.change_x *= -1
    assert s.change_x == SPINNER_SPEED
    assert s.center_x == grid_to_pixels(1)


# Vérifie que le spinner horizontal rebondit sur la limite droite
def test_spinner_horizontal_bounces_on_right_limit() -> None:
    s = make_spinner(
        cx=grid_to_pixels(5) + 1,
        cy=100.0,
        is_horizontal=True,
        min_pos=1, max_pos=5
    )
    s.change_x = SPINNER_SPEED
    s._position = (s.center_x + s.change_x, s.center_y)
    if s.center_x > grid_to_pixels(s.limits.max_pos):
        s._position = (grid_to_pixels(s.limits.max_pos), s.center_y)
        s.change_x *= -1
    assert s.change_x == -SPINNER_SPEED
    assert s.center_x == grid_to_pixels(5)


# Vérifie que le spinner vertical rebondit sur la limite basse
def test_spinner_vertical_bounces_on_bottom_limit() -> None:
    s = make_spinner(
        cx=100.0,
        cy=grid_to_pixels(1) - 1,
        is_horizontal=False,
        min_pos=1, max_pos=5
    )
    s.change_y = -SPINNER_SPEED
    s._position = (s.center_x, s.center_y + s.change_y)
    if s.center_y < grid_to_pixels(s.limits.min_pos):
        s._position = (s.center_x, grid_to_pixels(s.limits.min_pos))
        s.change_y *= -1
    assert s.change_y == SPINNER_SPEED
    assert s.center_y == grid_to_pixels(1)


# Vérifie que le spinner vertical rebondit sur la limite haute
def test_spinner_vertical_bounces_on_top_limit() -> None:
    s = make_spinner(
        cx=100.0,
        cy=grid_to_pixels(5) + 1,
        is_horizontal=False,
        min_pos=1, max_pos=5
    )
    s.change_y = SPINNER_SPEED
    s._position = (s.center_x, s.center_y + s.change_y)
    if s.center_y > grid_to_pixels(s.limits.max_pos):
        s._position = (s.center_x, grid_to_pixels(s.limits.max_pos))
        s.change_y *= -1
    assert s.change_y == -SPINNER_SPEED
    assert s.center_y == grid_to_pixels(5)

