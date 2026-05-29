from typing import Final
import arcade
from constants import TILE_SIZE
from textures import TEXTURE_HEALTH_BAR, TEXTURE_HEALTH_HUB

INVINCIBILITY_DURATION = 1.5

class HealthBar:
    """Gère les points de vie, l'invincibilité temporaire après un coup, et l'affichage de la barre."""

    def __init__(self, max_hp: int) -> None:
        self.max_hp: Final[int] =  max_hp
        self.hp: int = max_hp
        self.__invincibility_timer: float = 0.0

    def take_hit(self) -> bool:
        if self.__invincibility_timer > 0:
            return False

        self.__invincibility_timer = INVINCIBILITY_DURATION
        self.hp -= 1
        return self.hp <= 0

    def update(self, delta_time: float) -> None:
        if self.__invincibility_timer > 0:
            self.__invincibility_timer -= delta_time


    def draw(self, center_x: float, center_y: float, scale: float = 1.0) -> None:
        frame_width = TILE_SIZE * 5 * scale
        bar_width   = TILE_SIZE * 4 * scale
        bar_height  = TILE_SIZE * scale

        fill_ratio = max(self.hp / self.max_hp, 0)
        if fill_ratio > 0:
            fill_width = bar_width * fill_ratio
            fill_cx = center_x - bar_width / 2 + fill_width / 2
            arcade.draw_texture_rect(
                TEXTURE_HEALTH_HUB,
                arcade.XYWH(fill_cx, center_y, fill_width, bar_height)
            )

        arcade.draw_texture_rect(
            TEXTURE_HEALTH_BAR,
            arcade.XYWH(center_x, center_y, frame_width, bar_height)
        )
