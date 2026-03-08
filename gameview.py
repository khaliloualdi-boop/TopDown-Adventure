from arcade import PhysicsEngineSimple
from typing import Final
import arcade

from map import *
from constants import *
from textures import *
from spinner import *




def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)

class Spinner(arcade.TextureAnimationSprite):

    def __init__(self, x: int, y: int, is_horizontal: bool, limits) -> None:

        super().__init__(
            animation = ANIMATION_SPINNER,
            scale=SCALE,
            center_x = grid_to_pixels(x),
            center_y = grid_to_pixels(y),
        )

        self.is_horizontal = is_horizontal
        self.limits = limits

        if is_horizontal:
            self.change_x = SPINNER_SPEED
            self.change_y = 0
        else:
            self.change_x = 0
            self.change_y = SPINNER_SPEED

class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Final[arcade.TextureAnimationSprite]
    wall: arcade.SpriteList
    ground: arcade.SpriteList
    crystals: arcade.SpriteList
    spinners: arcade.SpriteList

    physics_engine: Final[PhysicsEngineSimple]
    camera: Final[arcade.camera.Camera2D]

    def __init__(self, map: Map) -> None:
        super().__init__()

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.world_width = map.width * TILE_SIZE
        self.world_height = map.height * TILE_SIZE

        
        self.player = arcade.TextureAnimationSprite(
            animation=ANIMATION_PLAYER_IDLE_DOWN,
            scale=SCALE,
            center_x=grid_to_pixels(map.player_center_x),
            center_y=grid_to_pixels(map.player_center_y),
        )

        
        self.wall = arcade.SpriteList(use_spatial_hash=True)
        self.ground = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)
        self.spinners = arcade.SpriteList(use_spatial_hash=True)

        
        for i in range(map.width):
            for j in range(map.height):

                self.ground.append(
                    arcade.Sprite(
                        TEXTURE_GRASS,
                        scale=SCALE,
                        center_x=grid_to_pixels(i),
                        center_y=grid_to_pixels(j),
                    )
                )

                cell = map.get(i, j)

                if cell == GridCell.Bush:
                    self.wall.append(
                        arcade.Sprite(
                            TEXTURE_BUSH,
                            scale=SCALE,
                            center_x=grid_to_pixels(i),
                            center_y=grid_to_pixels(j),
                        )
                    )

                elif cell == GridCell.Cristal:
                    self.crystals.append(
                        arcade.TextureAnimationSprite(
                            animation=ANIMATION_CRISTAUX,
                            scale=SCALE,
                            center_x=grid_to_pixels(i),
                            center_y=grid_to_pixels(j),
                        )
                    )

                elif cell == GridCell.SpinnerH:
                    limits = compute_horizontal_limits(map, i, j)
                    spinner = Spinner(i, j, True, limits)
                    self.spinners.append(spinner)

                elif cell == GridCell.SpinnerV:
                    limits = compute_vertical_limits(map, i, j)
                    spinner = Spinner(i, j, False, limits)
                    self.spinners.append(spinner)

     
        self.physics_engine = PhysicsEngineSimple(self.player, self.wall)

        
        self.camera = arcade.camera.Camera2D()



    def on_show_view(self) -> None:
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)



    def on_draw(self) -> None:
        self.clear()

        with self.camera.activate():
            self.ground.draw()
            self.wall.draw()
            self.crystals.draw()
            self.spinners.draw()
            arcade.draw_sprite(self.player)



    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT:
                self.player.change_x = PLAYER_MOVEMENT_SPEED
            case arcade.key.LEFT:
                self.player.change_x = -PLAYER_MOVEMENT_SPEED
            case arcade.key.UP:
                self.player.change_y = PLAYER_MOVEMENT_SPEED
            case arcade.key.DOWN:
                self.player.change_y = -PLAYER_MOVEMENT_SPEED
            case arcade.key.SPACE:
                from main import MAP_DECOUVERTE
                self.window.show_view(GameView(MAP_DECOUVERTE))

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.RIGHT | arcade.key.LEFT:
                self.player.change_x = 0
            case arcade.key.UP | arcade.key.DOWN:
                self.player.change_y = 0



    def on_update(self, delta_time: float) -> None:

        self.physics_engine.update()
        self.player.update_animation()

        self.crystals.update_animation()
        collisions = arcade.check_for_collision_with_list(self.player, self.crystals)
        self.spinners.update_animation()
        for crystal in collisions:
            crystal.remove_from_sprite_lists()
        self.camera.position = self.player.position

        for spinner in self.spinners:

            spinner.center_x += spinner.change_x
            spinner.center_y += spinner.change_y

            # Horizontal
            if spinner.is_horizontal:
                if spinner.center_x < grid_to_pixels(spinner.limits.min_pos):
                    spinner.center_x = grid_to_pixels(spinner.limits.min_pos)
                    spinner.change_x *= -1

                if spinner.center_x > grid_to_pixels(spinner.limits.max_pos):
                    spinner.center_x = grid_to_pixels(spinner.limits.max_pos)
                    spinner.change_x *= -1

            # Vertical
            else:
                if spinner.center_y < grid_to_pixels(spinner.limits.min_pos):
                    spinner.center_y = grid_to_pixels(spinner.limits.min_pos)
                    spinner.change_y *= -1

                if spinner.center_y > grid_to_pixels(spinner.limits.max_pos):
                    spinner.center_y = grid_to_pixels(spinner.limits.max_pos)
                    spinner.change_y *= -1

        if arcade.check_for_collision_with_list(self.player, self.spinners):
            from main import MAP_DECOUVERTE
            self.window.show_view(GameView(MAP_DECOUVERTE))