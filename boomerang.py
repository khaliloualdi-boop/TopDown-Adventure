from weapons import Weapons
from math import sqrt
from enum import Enum
import arcade
from constants import *
from arcade import Vec2
from player import *

class BoomerangState(Enum):
    inactive = 0
    launching = 1
    returning = 2

class Boomerang(Weapons, arcade.TextureAnimationSprite):
    state: BoomerangState
    origin: Vec2
    direction: Direction
    player: Player

    def __init__(self, Anim: arcade.TextureAnimation, Scale: float, Center_x: int | float, Center_y: int | float, player: Player) -> None:
        super().__init__(animation = Anim, scale = Scale, center_x = Center_x, center_y = Center_y)
        self.state = BoomerangState.inactive
        self.player = player

    @property
    def is_active(self) -> bool:
        return self.state != BoomerangState.inactive

    def launch(self) -> None:
        if not self.is_active:
            self.state = BoomerangState.launching
            self.origin = Vec2(self.player.center_x, self.player.center_y)
            self.center_x, self.center_y = self.origin.x, self.origin.y
            self.direction = self.player.direction
            self.set_change(self.direction)

    def update_boomerang(self) -> None:
        match self.state:
            case BoomerangState.inactive:
                return

            case BoomerangState.launching:
                self.center_x += self.change_x
                self.center_y += self.change_y
                if self.distance_from_point(self.origin) >= 8 * TILE_SIZE:
                    self.start_returning()

            case BoomerangState.returning:
                self.return_to_player()
                self.center_x += self.change_x
                self.center_y += self.change_y

                if self.distance_from_point(Vec2(self.player.center_x, self.player.center_y)) <= TILE_SIZE/2:
                    self.deactivate()


    def distance_from_point(self, vec: Vec2) -> float:
        return sqrt((self.center_x - vec.x)**2 + (self.center_y - vec.y)**2)

    def set_change(self, direction: Direction) -> None:
        self.change_x = 0
        self.change_y = 0
        match direction:
            case Direction.NORD:
                self.change_y = BOOMERANG_SPEED
            case Direction.SUD:
                self.change_y = - BOOMERANG_SPEED
            case Direction.EST:
                self.change_x = BOOMERANG_SPEED
            case Direction.OUEST:
                self.change_x = - BOOMERANG_SPEED

    def start_returning(self) -> None:
        self.state = BoomerangState.returning
        self.change_x = 0
        self.change_y = 0

    def return_to_player(self) -> None:
        btc_vector = Vec2(self.player.center_x - self.center_x, self.player.center_y - self.center_y)

        if btc_vector == (0,0):
            self.change_x, self.change_y = 0, 0
            return
        else:
            new_direction = btc_vector.normalize()
            self.change_x = new_direction.x * BOOMERANG_SPEED
            self.change_y = new_direction.y * BOOMERANG_SPEED

    def deactivate(self) -> None:
        self.state = BoomerangState.inactive
        self.change_x = 0
        self.change_y = 0
