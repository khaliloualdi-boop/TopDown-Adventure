
from turtle import window_height, left
from arcade.math import clamp
from arcade import PhysicsEngineSimple, TextureAnimationSprite, SpriteList, Rect, TextureAnimation
from typing import Final
import arcade
from map import *
from constants import *
from textures import *
from spinner import *
from player import *
from boomerang import *
from bat import *
from monster import Monster
from switch import Switch
from gate import Gate


def grid_to_pixels(i: int) -> int:
    return i * TILE_SIZE + (TILE_SIZE // 2)

class Spinner(Monster):

    def __init__(self, x: int, y: int, is_horizontal: bool, limits: SpinnerLimits) -> None:

        super().__init__(
            animation = ANIMATION_SPINNER,
            scale = SCALE,
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

    def update_monster(self) -> None:
        self.center_x += self.change_x
        self.center_y += self.change_y

        if self.is_horizontal:
            if self.center_x < grid_to_pixels(self.limits.min_pos):
                self.center_x = grid_to_pixels(self.limits.min_pos)
                self.change_x *= -1

            if self.center_x > grid_to_pixels(self.limits.max_pos):
                self.center_x = grid_to_pixels(self.limits.max_pos)
                self.change_x *= -1

        else:
            if self.center_y < grid_to_pixels(self.limits.min_pos):
                self.center_y = grid_to_pixels(self.limits.min_pos)
                self.change_y *= -1

            if self.center_y > grid_to_pixels(self.limits.max_pos):
                self.center_y = grid_to_pixels(self.limits.max_pos)
                self.change_y *= -1


class GameView(arcade.View):
    """Main in-game view."""

    world_width: Final[int]
    world_height: Final[int]

    player: Player
    boomerang: Boomerang
    wall: arcade.SpriteList
    ground: arcade.SpriteList
    crystals: arcade.SpriteList

    physics_engine: Final[PhysicsEngineSimple]
    camera: Final[arcade.camera.Camera2D]


    def __init__(self, map: Map) -> None:
        super().__init__()

        self.background_color = arcade.csscolor.CORNFLOWER_BLUE

        self.world_width = map.width * TILE_SIZE
        self.world_height = map.height * TILE_SIZE


        self.player = Player(
            ANIMATION_PLAYER_IDLE_DOWN,
            SCALE,
            grid_to_pixels(map.player_center_x),
            grid_to_pixels(map.player_center_y),
        )

        self.boomerang = Boomerang(
            ANIMATION_BOOMERANG,
            SCALE,
            grid_to_pixels(map.player_center_x),
            grid_to_pixels(map.player_center_y),
            self.player
        )

        #Initialize Spritelists :
        self.wall = arcade.SpriteList(use_spatial_hash=True)
        self.ground = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        self.monsters = arcade.SpriteList(use_spatial_hash=True)
        self.holes = arcade.SpriteList(use_spatial_hash=True)
        self.switches = arcade.SpriteList(use_spatial_hash=True)
        self.gates = arcade.SpriteList(use_spatial_hash=True)

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
                    self.monsters.append(spinner)

                elif cell == GridCell.SpinnerV:
                    limits = compute_vertical_limits(map, i, j)
                    spinner = Spinner(i, j, False, limits)
                    self.monsters.append(spinner)

                elif cell == GridCell.Hole:
                    self.holes.append(
                        arcade.Sprite(TEXTURE_HOLE, scale=SCALE, center_x=grid_to_pixels(i), center_y=grid_to_pixels(j),
                        )
                    )             
                elif cell == GridCell.Bat:
                    bat = Bat(grid_to_pixels(i),grid_to_pixels(j),ANIMATION_BAT)
                    self.monsters.append(bat)
                
                elif cell == GridCell.Switch:
                    switch_conf = next(
                        (s for s in map.switches_config if s["x"] == i and s["y"] == j),
                        None
                    )
                    switch_id = switch_conf["id"] if switch_conf else None
                    initial_state = switch_conf.get("state", "off") == "on" if switch_conf else False

                    switch = Switch(
                        grid_to_pixels(i),
                        grid_to_pixels(j),
                        initial_state,
                        switch_id
                    )
                    self.switches.append(switch)

                elif cell == GridCell.Gate:
                    # retrouver le gate correspondant dans la config YAML
                    gate_conf = next((g for g in map.gates_config if g["x"] == i and g["y"] == j), None)
                    open_if = gate_conf["open_if"] if gate_conf else None
                    gate = Gate(grid_to_pixels(i), grid_to_pixels(j), open_if)
                    self.gates.append(gate)
                    self.wall.append(gate)
                

        # Physics Engine :
        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall)

        #Cameras :
        self.camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()

        #Score :
        self.score = 0


    def on_show_view(self) -> None:
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)



    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.ground.draw()
            self.holes.draw()
            self.wall.draw()
            self.switches.draw()
            self.gates.draw()
            self.crystals.draw()
            self.monsters.draw()

            arcade.draw_sprite(self.player)
            if self.boomerang.is_active:
                arcade.draw_sprite(self.boomerang)
        with self.ui_camera.activate():
            arcade.Text(text=f"Score : {self.score}",x=10,y=self.window.height - 30,color=arcade.color.WHITE,font_size=20).draw()


    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.SPACE:
            self.window.show_view(GameView(MAP_DECOUVERTE))
        elif symbol == arcade.key.D:
            self.boomerang.launch()
        else:
            self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.player.on_key_release(symbol, modifiers)



    def on_update(self, delta_time: float) -> None:

        self.physics_engine.update()
        self.player.update_animation()
        self.crystals.update_animation()

        self.boomerang.update_boomerang()
        self.boomerang.update_animation()
        switches_dict = {s.id: s for s in self.switches if s.id is not None}

        for monster in self.monsters:
            monster.update_monster()
            monster.update_animation()
            
        for x in arcade.check_for_collision_with_list(self.player, self.crystals):
            x.remove_from_sprite_lists()
            self.score += 1

        
        if arcade.check_for_collision_with_list(self.player, self.monsters):
            self.window.show_view(GameView(MAP_DECOUVERTE))

        for monster in arcade.check_for_collision_with_list(self.boomerang, self.monsters):
            self.monsters.remove(monster)

        for wall in arcade.check_for_collision_with_list(self.boomerang, self.wall):
            self.boomerang.start_returning()

        for hole in self.holes:
            distance = arcade.math.get_distance(self.player.center_x,self.player.center_y,hole.center_x,hole.center_y,)
            if distance <= 20:
                self.window.show_view(GameView(MAP_DECOUVERTE))

        for switch in arcade.check_for_collision_with_list(self.boomerang, self.switches):
            switch.toggle()
            if self.boomerang.state == BoomerangState.launching:
                self.boomerang.start_returning()
        
        switches_dict = {s.id: s for s in self.switches}  # il faut ajouter l'attribut `id` à Switch
        for gate in self.gates:
            gate.update_state(switches_dict)
            if gate.is_open and gate in self.wall:
                self.wall.remove(gate)
            if not gate.is_open and gate not in self.wall:
                self.wall.append(gate)

        self.pan_camera_to_player(delta_time)

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
