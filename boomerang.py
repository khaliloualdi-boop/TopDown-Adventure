from weapons import Weapons
from constants import BOOMERANG_SPEED, TILE_SIZE, Direction
from player import Player
from enum import Enum
import arcade
from arcade import Vec2

class BoomerangState(Enum):
    """États possibles du boomerang"""
    inactive = 0
    launching = 1
    returning = 2

class Boomerang(Weapons):
    """Projectile lancé dans la direction du joueur qui revient automatiquement à son point d'origine même en cas de mouvement du joueur."""
    state: BoomerangState
    origin: Vec2
    direction: Direction
    player: Player

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: int | float, center_y: int | float, player: Player) -> None:
        super().__init__(animation=animation, scale=scale, center_x=center_x, center_y=center_y)
        self.state = BoomerangState.inactive
        self.player = player
        self.direction = self.player.direction

    @property
    def is_active(self) -> bool:
        return self.state != BoomerangState.inactive

    def attack(self) -> None:
        if not self.is_active:
            self.state = BoomerangState.launching
            self.origin = Vec2(self.player.center_x, self.player.center_y)
            self.center_x, self.center_y = self.origin.x, self.origin.y
            self.direction = self.player.direction
            self.set_change(self.direction)

    def update_weapon(self, delta: float) -> None:
        match self.state:
            case BoomerangState.inactive:
                return

            case BoomerangState.launching:
                self.center_x += self.change_x
                self.center_y += self.change_y
                if arcade.math.get_distance(self.center_x, self.center_y, self.origin.x, self.origin.y) >= 8 * TILE_SIZE:
                    self.start_returning()

            case BoomerangState.returning:
                self.return_to_player()
                self.center_x += self.change_x
                self.center_y += self.change_y

                if arcade.math.get_distance(self.center_x, self.center_y, self.player.center_x, self.player.center_y) <= TILE_SIZE/2:
                    self.deactivate()

        self.update_animation()

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
        btp_vector = Vec2(self.player.center_x - self.center_x, self.player.center_y - self.center_y)

        if btp_vector == (0,0):
            self.change_x, self.change_y = 0, 0
            return
        else:
            new_direction = btp_vector.normalize()
            self.change_x = new_direction.x * BOOMERANG_SPEED
            self.change_y = new_direction.y * BOOMERANG_SPEED

    def deactivate(self) -> None:
        self.state = BoomerangState.inactive
        self._toggled_switches.clear()
        self.change_x = 0
        self.change_y = 0
