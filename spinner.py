from dataclasses import dataclass
from map import Map, GridCell


@dataclass
class SpinnerLimits:
    min_pos: int
    max_pos: int



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



