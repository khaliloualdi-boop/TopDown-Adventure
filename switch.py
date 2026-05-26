from constants import SWITCH_SCALE
import arcade

TEXTURE_SWITCH_OFF = arcade.load_texture(":resources:/images/tiles/leverLeft.png")
TEXTURE_SWITCH_ON = arcade.load_texture(":resources:/images/tiles/leverRight.png")

class Switch(arcade.Sprite):
    def __init__(self, x: int, y: int, initial_state: bool = False, switch_id: str | None = None) -> None :
        texture = TEXTURE_SWITCH_ON if initial_state else TEXTURE_SWITCH_OFF
        super().__init__(
            texture,
            scale=SWITCH_SCALE,
            center_x=x,
            center_y=y
        )
        self.is_on = initial_state
        self.switch_id = switch_id

    def toggle(self) -> None :
        self.is_on = not self.is_on

        if self.is_on:
            self.texture = TEXTURE_SWITCH_ON
        else:
            self.texture = TEXTURE_SWITCH_OFF
