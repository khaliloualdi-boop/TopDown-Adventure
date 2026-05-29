import arcade
from wall_obstacle import WallObstacle
from textures import TEXTURE_GATE_OPEN, TEXTURE_GATE_CLOSED
from constants import SCALE


class CrystalGate(WallObstacle):
    """Portail qui s'ouvre automatiquement quand tous les cristaux de la carte ont été ramassés."""

    __is_open: bool

    @property
    def is_open(self) -> bool:
        return self.__is_open

    @is_open.setter
    def is_open(self, val: bool) -> None:
        self.__is_open = val

    def __init__(self, x: float, y: float) -> None:
        super().__init__(TEXTURE_GATE_CLOSED, scale=SCALE, center_x=x, center_y=y)
        self.is_open = False

    def update_state(self, crystal_count: int) -> None:
        """
        Appelé à chaque frame dans on_update().
        crystal_count : nombre de cristaux restants sur la map.
        """
        self.is_open = (crystal_count == 0)
        self.texture = TEXTURE_GATE_OPEN if self.is_open else TEXTURE_GATE_CLOSED
