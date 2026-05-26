from dataclasses import dataclass
from textures import ANIMATION_SPINNER, DEATH_ANIMATION_SPINNER
from monster import Monster
from map import Map, GridCell
from constants import SPINNER_SPEED, SCALE, grid_to_pixels, MONSTER_DEATH_DURATION


@dataclass
class SpinnerLimits:
    min_pos: int
    max_pos: int

class Spinner(Monster):

    Death_animation = DEATH_ANIMATION_SPINNER
    Death_duration = MONSTER_DEATH_DURATION

    def __init__(self, x: int, y: int, is_horizontal: bool, limits: SpinnerLimits) -> None:

        super().__init__(
            animation = ANIMATION_SPINNER,
            scale = SCALE,
            center_x = grid_to_pixels(x),
            center_y = grid_to_pixels(y),
        )

        self.is_horizontal = is_horizontal
        self.limits = limits

        if is_horizontal:
            self.change_x = SPINNER_SPEED
            self.change_y = 0
        else:
            self.change_x = 0
            self.change_y = SPINNER_SPEED

    def update_monster(self, delta_time : float) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.is_horizontal:
            if self.center_x < grid_to_pixels(self.limits.min_pos):
                self.center_x = grid_to_pixels(self.limits.min_pos)
                self.change_x *= -1

            if self.center_x > grid_to_pixels(self.limits.max_pos):
                self.center_x = grid_to_pixels(self.limits.max_pos)
                self.change_x *= -1

        else:
            if self.center_y < grid_to_pixels(self.limits.min_pos):
                self.center_y = grid_to_pixels(self.limits.min_pos)
                self.change_y *= -1

            if self.center_y > grid_to_pixels(self.limits.max_pos):
                self.center_y = grid_to_pixels(self.limits.max_pos)
                self.change_y *= -1

def compute_horizontal_limits(game_map: Map, x: int, y: int) -> SpinnerLimits:
    """
    Calcule les limites gauche/droite d’un spinner horizontal.
    """

    left = x
    while left - 1 >= 0 and game_map.get(left - 1, y) != GridCell.Bush:
        left -= 1

    right = x
    while right + 1 < game_map.width and game_map.get(right + 1, y) != GridCell.Bush:
        right += 1

    return SpinnerLimits(left, right)


def compute_vertical_limits(game_map: Map, x: int, y: int) -> SpinnerLimits:
    """
    Calcule les limites haut/bas d’un spinner vertical.
    """


    bottom = y
    while bottom - 1 >= 0 and game_map.get(x, bottom - 1) != GridCell.Bush:
        bottom -= 1


    top = y
    while top + 1 < game_map.height and game_map.get(x, top + 1) != GridCell.Bush:
        top += 1

    return SpinnerLimits(bottom, top)
