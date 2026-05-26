from abc import ABC ,abstractmethod
from dataclasses import dataclass
import arcade
from enum import Enum

class Weapons(ABC, arcade.TextureAnimationSprite):

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(animation=animation, scale=scale, center_x=center_x, center_y=center_y)

    @property
    def collects_crystals(self) -> bool:
        return False

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
