import arcade
from textures import TEXTURE_GATE_OPEN, TEXTURE_GATE_CLOSED
from constants import SCALE


class CrystalGate(arcade.Sprite):
    """
    Portail spécial qui s'ouvre automatiquement quand tous les cristaux
    ont été ramassés. Ne dépend d'aucun interrupteur.
    """

    is_open: bool

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