from constants import *
from textures import *
from pycparser.c_ast import Enum
import arcade


class Direction (Enum):
    SUD = 0
    NORD = 1
    OUEST = 2
    EST = 3

class player(arcade.TextureAnimationSprite):
    __direction: int
    player_animation_list: Final[arcade.SpriteList]

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: int, center_y: int) -> None:
        super().__init__(center_x, center_y, scale, animation)
        self.__direction = Direction.SUD
        self.player_animation_list = arcade.SpriteList()
        self.player_animation_list.extend([arcade.TextureAnimationSprite(animation = ANIMATION_PLAYER_IDLE_DOWN, scale = SCALE, center_x = self.center_x, center_y = self.center_y), arcade.TextureAnimationSprite(animation = ANIMATION_PLAYER_IDLE_UP, scale = SCALE, center_x = self.center_x, center_y = self.center_y), arcade.TextureAnimationSprite(animation = ANIMATION_PLAYER_IDLE_RIGHT, scale = SCALE, center_x = self.center_x, center_y = self.center_y), arcade.TextureAnimationSprite(animation = ANIMATION_PLAYER_IDLE_LEFT, scale = SCALE, center_x = self.center_x, center_y = self.center_y)])

    def updt(self) -> None:
        ...

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.change_x = PLAYER_MOVEMENT_SPEED
                self.animation = self.player_animation_list[Direction.EST]
            case arcade.key.LEFT:
                self.change_x = - PLAYER_MOVEMENT_SPEED
                self.animation = self.player_animation_list[Direction.OUEST]
            case arcade.key.UP:
                self.change_y = PLAYER_MOVEMENT_SPEED
                self.animation = self.player_animation_list[Direction.NORD]
            case arcade.key.DOWN:
                self.change_y = - PLAYER_MOVEMENT_SPEED
                self.animation = self.player_animation_list[Direction.SUD]

    @property
    def get_direction(self) -> int:
        return self.__direction
