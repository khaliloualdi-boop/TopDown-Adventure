from turtle import window_height
from arcade.math import clamp
from arcade import PhysicsEngineSimple, TextureAnimationSprite, SpriteList, Rect
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
        #Initialize Spritelists :
        self.wall = arcade.SpriteList(use_spatial_hash=True)
        self.ground = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        self.spinners = arcade.SpriteList(use_spatial_hash=True)


        for i in range(map.width):
            for j in range(map.height):

                self.ground.append(arcade.Sprite(TEXTURE_GRASS, scale=SCALE, center_x=grid_to_pixels(i), center_y=grid_to_pixels(j),))
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

        # Physics Engine :
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall)

        #Camera :
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
        self.spinners.update_animation()
        self.pan_camera_to_player(delta_time)

        for x in arcade.check_for_collision_with_list(self.player, self.crystals):
            x.remove_from_sprite_lists()

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

    def pan_camera_to_player(self, delta_time: float) -> None:
        dead_zone_width = self.camera.width*0.4
        dead_zone_height = self.camera.height*0.4
        dead_zone_right = self.camera.position.x + dead_zone_width/2
        dead_zone_left = self.camera.position.x - dead_zone_width/2
        dead_zone_top = self.camera.position.y + dead_zone_height/2
        dead_zone_bottom = self.camera.position.y - dead_zone_height/2

        target_x : float = self.camera.position.x
        target_y : float = self.camera.position.y

        if self.player.center_x < dead_zone_left:
            target_x -= dead_zone_left - self.player.center_x
        elif self.player.center_x > dead_zone_right:
            target_x += self.player.center_x - dead_zone_right

        if self.player.center_y < dead_zone_bottom:
            target_y -= dead_zone_bottom - self.player.center_y
        elif self.player.center_y > dead_zone_top:
            target_y += self.player.center_y - dead_zone_top

        target_x = clamp(target_x, MAX_WINDOW_WIDTH/2, self.world_width - (MAX_WINDOW_WIDTH/2))
        target_y = clamp(target_y, MAX_WINDOW_HEIGHT/2, self.world_height - (MAX_WINDOW_HEIGHT/2))
        next_pos = (target_x, target_y)
        self.camera.position = arcade.math.lerp_2d(self.camera.position, next_pos, delta_time * 6)
