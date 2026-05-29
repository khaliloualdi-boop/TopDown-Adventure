from weapons import Weapons
from constants import Direction, PLAYER_MOVEMENT_SPEED, PLAYER_MAX_HP
from textures import RUNNING_SPRITELIST, IDLE_SPRITELIST
from healthbar import HealthBar
import arcade

class Player(arcade.TextureAnimationSprite):
    """Sprite du joueur : gère le mouvement, l'animation, le changement d'armes et les points de vie."""
    _direction: Direction
    _horizontal_stack: list[int]
    _vertical_stack: list[int]
    equipped_weapons: list[Weapons]
    current_weapon: int
    is_attacking: bool

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: int, center_y: int) -> None:
        super().__init__(animation=animation, scale=scale, center_x=center_x, center_y=center_y)
        self._direction = Direction.SUD
        self._horizontal_stack = []
        self._vertical_stack = []
        self.equipped_weapons = []
        self.current_weapon = 0
        self.is_attacking = False
        self.health_bar = HealthBar(PLAYER_MAX_HP)

    @property
    def direction(self) -> Direction:
        return self._direction

    def _add_key(self, stack: list[int], key: int) -> None:
        if key in stack:
            stack.remove(key)
        stack.append(key)

    def on_key_press(self, symbol: int, modifiers: int) -> None:

        match symbol:
            case arcade.key.RIGHT | arcade.key.LEFT:
                self._add_key(self._horizontal_stack, symbol)
            case arcade.key.UP | arcade.key.DOWN:
                self._add_key(self._vertical_stack, symbol)
            case arcade.key.R:
                if not self.equipped_weapons[self.current_weapon].is_active:
                    self.current_weapon = (self.current_weapon + 1) % len(self.equipped_weapons)
            case _:
                return

        self._update_movement()
        self._select_animation()

    def on_key_release(self, symbol: int, modifiers: int) -> None:

        if symbol in self._horizontal_stack:
            self._horizontal_stack.remove(symbol)
        if  symbol in self._vertical_stack:
            self._vertical_stack.remove(symbol)

        self._update_movement()
        self._select_animation()

    def _update_movement(self) -> None:
        if self.is_attacking:
            self.change_x = 0
            self.change_y = 0
            return

        match self._horizontal_stack[-1] if self._horizontal_stack else None:
            case arcade.key.RIGHT:
                self.change_x = PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                self.change_x = -PLAYER_MOVEMENT_SPEED
            case _:
                self.change_x = 0

        match self._vertical_stack[-1] if self._vertical_stack else None:
            case arcade.key.UP:
                self.change_y = PLAYER_MOVEMENT_SPEED
            case arcade.key.DOWN:
                self.change_y = -PLAYER_MOVEMENT_SPEED
            case _:
                self.change_y = 0

    def _select_animation(self) -> None:
        match (self.change_x, self.change_y):
            case (_, y) if y > 0:
                self._direction = Direction.NORD
            case (_, y) if y < 0:
                self._direction = Direction.SUD
            case (x, _) if x > 0:
                self._direction = Direction.EST
            case (x, _) if x < 0:
                self._direction = Direction.OUEST

        if not self.is_attacking:
            if self.change_x != 0 or self.change_y != 0:
                self.animation = RUNNING_SPRITELIST[self._direction.value]
            else:
                self.animation = IDLE_SPRITELIST[self._direction.value]

    def take_hit(self) -> bool:
        return self.health_bar.take_hit()
