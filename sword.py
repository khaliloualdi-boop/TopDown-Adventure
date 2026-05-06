from arcade import TextureAnimationSprite
from weapons import *
from enum import Enum
from textures import SWORD_ATTACK_LIST, IDLE_SPRITELIST
from constants import SCALE
from player import Direction, Player
import arcade

class Sword_State(Enum):
    inactive = 0
    active = 1

class Sword(Weapons):
    player: Player
    state: Sword_State
    direction: Direction
    elapsed_time: float

    def __init__(self, player: Player) -> None:
        super().__init__(animation = SWORD_ATTACK_LIST[0], scale = SCALE, cx = 0, cy = 0)
        self.player = player
        self.state = Sword_State.inactive
        self.elapsed_time = 0

    @property
    def is_active(self) -> bool:
        return self.state != Sword_State.inactive

    def attack(self) -> None:
        if self.is_active:
            return
        self.elapsed_time = 0
        self.player.is_attacking = True
        self.state = Sword_State.active
        self.direction = self.player.direction

        self.animation = SWORD_ATTACK_LIST[self.direction.value]
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y

    def update_weapon(self, delta: float) -> None:
        self.update_animation()
        self.elapsed_time += delta
        if self.elapsed_time >= 0.3: # ??
            self.deactivate()

    def deactivate(self) -> None:
        self.state = Sword_State.inactive
        self.player.is_attacking = False
        self.elapsed_time = 0
        self.player.animation = IDLE_SPRITELIST[self.player.direction.value]
