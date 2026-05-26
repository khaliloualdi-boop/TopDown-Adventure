from boomerang import Direction
from arcade import TextureAnimationSprite
from weapons import *
from enum import Enum
from textures import SWORD_ATTACK_LIST, IDLE_SPRITELIST
from constants import SCALE, TILE_SIZE, SWORD_ATTACK_DURATION, Direction
from player import Player
import arcade

SWORD_OFFSET = TILE_SIZE  # Dash du player

class SwordState(Enum):
    inactive = 0
    active = 1

class Sword(Weapons):
    player: Player
    state: SwordState
    direction: Direction
    elapsed_time: float

    def __init__(self, player: Player) -> None:
        super().__init__(animation = SWORD_ATTACK_LIST[0], scale = SCALE, cx = 0, cy = 0)
        self.player = player
        self.state = SwordState.inactive
        self.elapsed_time = 0

    @property
    def collects_crystals(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return self.state != SwordState.inactive

    def attack(self) -> None:
        if self.is_active:
            return
        self.elapsed_time = 0
        self.player.is_attacking = True
        self.state = SwordState.active
        self.direction = self.player.direction

        self.animation = SWORD_ATTACK_LIST[self.direction.value]

        match self.direction:
            case Direction.NORD:
                self.center_x = self.player.center_x
                self.center_y = self.player.center_y + SWORD_OFFSET
            case Direction.SUD:
                self.center_x = self.player.center_x
                self.center_y = self.player.center_y - SWORD_OFFSET
            case Direction.EST:
                self.center_x = self.player.center_x + SWORD_OFFSET
                self.center_y = self.player.center_y
            case _:
                self.center_x = self.player.center_x - SWORD_OFFSET
                self.center_y = self.player.center_y

    def update_weapon(self, delta: float) -> None:
        self.update_animation()
        self.elapsed_time += delta
        if self.elapsed_time >= SWORD_ATTACK_DURATION:
            self.deactivate()

    def deactivate(self) -> None:
        self.state = SwordState.inactive
        self.player.is_attacking = False
        self.elapsed_time = 0
        self.player.update_movement()
        self.player.update__animation()
