from constants import Direction, PLAYER_MOVEMENT_SPEED
from textures import RUNNING_SPRITELIST, IDLE_SPRITELIST
from weapons import Weapons
import arcade

class Player(arcade.TextureAnimationSprite):
    __direction: Direction
    pressed_keys: set[int]
    horizontal_stack: list[int]
    vertical_stack: list[int]
    equipped_weapons: list[Weapons]
    current_weapon: int
    is_attacking: bool

    def __init__(self, Anim: arcade.TextureAnimation, Scale: float, Center_x: int, Center_y: int) -> None:
        super().__init__(animation = Anim, scale = Scale, center_x = Center_x, center_y = Center_y)
        self.__direction = Direction.SUD
        self.pressed_keys = set()
        self.horizontal_stack = []
        self.vertical_stack = []
        self.equipped_weapons = []
        self.current_weapon = 0
        self.is_attacking = False

    @property
    def direction(self) -> Direction:
        return self.__direction


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
            case arcade.key.R:
                if not self.equipped_weapons[self.current_weapon].is_active:
                    self.current_weapon = (self.current_weapon + 1) % len(self.equipped_weapons)

        self.update_movement()
        self.update__animation()

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.pressed_keys.discard(symbol)
        if symbol in self.horizontal_stack:
            self.horizontal_stack.remove(symbol)
        if  symbol in self.vertical_stack:
            self.vertical_stack.remove(symbol)

        self.update_movement()
        self.update__animation()

    def update_movement(self) -> None:
        if self.is_attacking:
            self.change_x = 0
            self.change_y = 0
            return

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

    def update__animation(self) -> None:
        if self.change_y > 0:
            self.__direction = Direction.NORD
            if not self.is_attacking:
                self.animation = RUNNING_SPRITELIST[Direction.NORD.value]
        elif self.change_y < 0:
            self.__direction = Direction.SUD
            if not self.is_attacking:
                self.animation = RUNNING_SPRITELIST[Direction.SUD.value]
        elif self.change_x > 0:
            self.__direction = Direction.EST
            if not self.is_attacking:
                self.animation = RUNNING_SPRITELIST[Direction.EST.value]
        elif self.change_x < 0:
            self.__direction = Direction.OUEST
            if not self.is_attacking:
                self.animation = RUNNING_SPRITELIST[Direction.OUEST.value]
        else:
            if not self.is_attacking:
                self.animation = IDLE_SPRITELIST[self.__direction.value]
