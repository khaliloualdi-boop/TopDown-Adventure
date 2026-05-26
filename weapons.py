from abc import ABC ,abstractmethod
from dataclasses import dataclass
import arcade
from enum import Enum

class Weapons(ABC, arcade.TextureAnimationSprite):

    def __init__(self, animation : arcade.TextureAnimation, scale : float, cx : float, cy: float) -> None:
        super().__init__(animation = animation, scale = scale, center_x = cx, center_y = cy)

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
