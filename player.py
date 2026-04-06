from math import sqrt
from arcade import Vec2
from constants import *
from textures import *
from enum import Enum
from typing import Final
import arcade


class Direction (Enum):
    SUD = 0
    NORD = 1
    EST = 2
    OUEST = 3

class Player(arcade.TextureAnimationSprite):
    __direction: Direction
    pressed_keys: set[int]
    horizontal_stack: list[int]
    vertical_stack: list[int]
    equiped_weapons: list[int]
    current_weapon: int

    def __init__(self, Anim: arcade.TextureAnimation, Scale: float, Center_x: int, Center_y: int) -> None:
        super().__init__(animation = Anim, scale = Scale, center_x = Center_x, center_y = Center_y)
        self.__direction = Direction.SUD
        self.pressed_keys = set()
        self.horizontal_stack = []
        self.vertical_stack = []
        self.equiped_weapons = [0,1]
        self.current_weapon = 0


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        self.pressed_keys.add(symbol)
        match symbol:
            case arcade.key.RIGHT | arcade.key.LEFT:
                if symbol in self.horizontal_stack:
                    self.horizontal_stack.remove(symbol)
                self.horizontal_stack.append(symbol)
            case arcade.key.UP | arcade.key.DOWN:
                if symbol in self.vertical_stack:
                    self.vertical_stack.remove(symbol)
                self.vertical_stack.append(symbol)

        self.updt_movement()
        self.updt_animation()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.pressed_keys.discard(symbol)
        if symbol in self.horizontal_stack:
            self.horizontal_stack.remove(symbol)
        if  symbol in self.vertical_stack:
            self.vertical_stack.remove(symbol)

        self.updt_movement()
        self.updt_animation()

    def updt_movement(self) -> None:
        if self.horizontal_stack: #check si la liste est non vide
            horz = self.horizontal_stack[-1] #last element
            if horz == arcade.key.RIGHT:
                self.change_x = PLAYER_MOVEMENT_SPEED
            else:
                self.change_x = - PLAYER_MOVEMENT_SPEED
        else:
            self.change_x = 0

        if self.vertical_stack:
            vert = self.vertical_stack[-1]
            if vert == arcade.key.UP:
                self.change_y = PLAYER_MOVEMENT_SPEED
            else:
                self.change_y = - PLAYER_MOVEMENT_SPEED
        else:
            self.change_y = 0

    def updt_animation(self) -> None:
        if self.change_y > 0:
            self.animation = RUNNING_SPRITELIST[Direction.NORD.value]
            self.__direction = Direction.NORD
        elif self.change_y < 0:
            self.animation = RUNNING_SPRITELIST[Direction.SUD.value]
            self.__direction = Direction.SUD
        elif self.change_x > 0:
            self.animation = RUNNING_SPRITELIST[Direction.EST.value]
            self.__direction = Direction.EST
        elif self.change_x < 0:
            self.animation = RUNNING_SPRITELIST[Direction.OUEST.value]
            self.__direction = Direction.OUEST
        else:
            self.animation = IDLE_SPRITELIST[self.__direction.value]

    @property
    def direction(self) -> Direction:
        return self.__direction
