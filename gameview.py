from typing import Final
import arcade

from constants import *
from textures import *

def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)

class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Final[arcade.Sprite]
    wall = arcade.SpriteList(use_spatial_hash = True)
    ground = arcade.SpriteList(use_spatial_hash = True)

    def __init__(self) -> None:
        # Magical incantion: initialize the Arcade view
        super().__init__()

        # Choose a nice comfy background color
        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        # Setup our game
        self.world_width = 40 * TILE_SIZE
        self.world_height = 20 * TILE_SIZE

        self.player = arcade.Sprite(
            TEXTURE_PLAYER_IDLE_DOWN,
            scale=SCALE, center_x=grid_to_pixels(2), center_y=grid_to_pixels(2)
        )

        for i in range(20):
            for j in range(40):
                self.ground.append(arcade.Sprite(TEXTURE_GRASS, scale = SCALE, center_x = grid_to_pixels(i) , center_y = grid_to_pixels(j)))

        grass_coord = [(3,6),(7,2),(2,10),(3,8)]

        for x, y in grass_coord:
            self.wall.append(arcade.Sprite(TEXTURE_BUSH, scale = SCALE, center_x = grid_to_pixels(x), center_y = grid_to_pixels(y)))

    def on_show_view(self) -> None:
        """Called automatically by 'window.show_view(game_view)' in main.py."""
        # When we show the view, adjust the window's size to our world size.
        # If the world size is smaller than the maximum window size, we should
        # limit the size of the window.
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)

    def on_draw(self) -> None:
        """Render the screen."""
        self.clear() # always start with self.clear()
        self.ground.draw()
        self.wall.draw()
        arcade.draw_sprite(self.player)
