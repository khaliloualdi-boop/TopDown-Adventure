from sword import Sword
from abc import abstractmethod
from boomerang import Boomerang
from player import Player
from dataclasses import dataclass
import arcade
from enum import Enum

class Weapon_State(Enum):
    active = 0
    inactive = 1

class active_weapon(Enum):
    boomerang = Boomerang
    sword = Sword

class Weapons:
    icon: ...
    state: Weapon_State
    player: Player

    @abstractmethod
    def attack(self, player: Player) -> None:
        ...

    @abstractmethod
    def deactivate(self) -> None:
        ...

    @abstractmethod
    def update_weapon(self, delta_time: float) -> None:
        ...
