from abc import ABC ,abstractmethod
from dataclasses import dataclass
import arcade
from enum import Enum

class Weapons(ABC, arcade.TextureAnimationSprite):
    """Interface abstraite commune à toutes les armes du joueur."""

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(animation=animation, scale=scale, center_x=center_x, center_y=center_y)
        self._toggled_switches: set[arcade.Sprite] = set() # single underscore sinon le name mangling empeche l'acces pour les autres classes

    @property
    def collects_crystals(self) -> bool:
        return False

    @property
    def collision_sprite(self) -> arcade.Sprite:
        return self

    @property
    @abstractmethod
    def is_active(self) -> bool:
        ...

    @abstractmethod
    def attack(self) -> None:
        ...

    @abstractmethod
    def deactivate(self) -> None:
        ...

    @abstractmethod
    def update_weapon(self, delta: float) -> None:
        ...
