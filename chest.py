# chest.py
from __future__ import annotations
from enum import Enum
import arcade
from constants import SCALE, CHEST_OPENING_DURATION
from textures import (
    ANIMATION_CHEST_OPENING,
    ANIMATION_CHEST_IDLE,
    TEXTURE_CHEST_OPEN,
)


class ChestState(Enum):
    """États du coffre : fermé, en cours d'ouverture, ou ouvert."""
    closed  = 0
    opening = 1
    open    = 2


class Chest(arcade.TextureAnimationSprite):
    """Coffre animé à trois états ; s'ouvre à la mort du boss et déclenche la victoire au contact du joueur."""

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
                if self._elapsed >= CHEST_OPENING_DURATION:
                    self.state = ChestState.open
                    self.texture = TEXTURE_CHEST_OPEN
            case ChestState.open:
                pass  # rien, texture statique
