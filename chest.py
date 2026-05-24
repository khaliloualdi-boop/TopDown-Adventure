# chest.py
from __future__ import annotations
from enum import Enum
import arcade
from constants import SCALE
from textures import (
    ANIMATION_CHEST_OPENING,
    ANIMATION_CHEST_IDLE,
    TEXTURE_CHEST_OPEN,
)


class ChestState(Enum):
    closed  = 0   # animation idle en boucle
    opening = 1   # animation d'ouverture (une seule fois)
    open    = 2   # texture statique, le joueur peut "gagner"


class Chest(arcade.TextureAnimationSprite):
    """
    Coffre animé à trois états.
    - Fermé : animation idle en boucle.
    - Ouverture : déclenchée quand le boss meurt, animation one-shot.
    - Ouvert : texture statique, collision avec le joueur = victoire.
    """

    state: ChestState
    _elapsed: float

    def __init__(self, x: float, y: float) -> None:
        super().__init__(
            animation=ANIMATION_CHEST_IDLE,
            scale=SCALE,
            center_x=x,
            center_y=y,
        )
        self.state = ChestState.closed
        self._elapsed = 0.0

    @property
    def is_open(self) -> bool:
        return self.state == ChestState.open

    def open(self) -> None:
        """Appelé quand le boss meurt."""
        if self.state == ChestState.closed:
            self.state = ChestState.opening
            self._elapsed = 0.0
            self.animation = ANIMATION_CHEST_OPENING

    def update_chest(self, delta: float) -> None:
        match self.state:
            case ChestState.closed:
                self.update_animation()
            case ChestState.opening:
                self._elapsed += delta
                self.update_animation()
                if self._elapsed >= 0.75:
                    self.state = ChestState.open
                    self.texture = TEXTURE_CHEST_OPEN
            case ChestState.open:
                pass  # rien, texture statique