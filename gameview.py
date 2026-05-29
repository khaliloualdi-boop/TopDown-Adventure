from __future__ import annotations
from weapons import Weapons
from typing import Final, assert_never
from arcade.math import clamp
from arcade import PhysicsEngineSimple, TextureAnimationSprite, SpriteList, Rect, TextureAnimation, Texture
import arcade
import networkx as nx

from map import Map, GridCell, MapTheme, MAP_DECOUVERTE, MAP_BOSS
from constants import SCALE, TILE_SIZE, MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, grid_to_pixels, HOLE_FALL_DISTANCE
from textures import (
    TEXTURE_GRASS, TEXTURE_BUSH, TEXTURE_HOLE,
    ANIMATION_CRISTAUX, ICON_BOOMERANG, ICON_SWORD,
    ANIMATION_PLAYER_IDLE_DOWN,
    ANIMATION_BOOMERANG, ANIMATION_BLOB, ANIMATION_BAT, TEXTURE_DUNGEON_FLOOR, TEXTURE_DUNGEON_WALL,
    SOUND_CRYSTAL
)
from spinner import Spinner, compute_limits
from player import Player
from boomerang import Boomerang, BoomerangState
from bat import Bat
from blob import Blob
from sword import Sword
from monster import Monster, MonsterState
from switch import Switch
from gate import Gate
from navmesh import create_graph
from boss import Boss
from chest import Chest, ChestState
from crystal_gate import CrystalGate
from overlay import Overlay
from gameover import GameOverView
from gamewon import GameWonView

class GameView(arcade.View):
    """Vue principale du jeu : orchestre tous les sprites, la physique, les monstres et les interactions."""

    world_width: Final[int]
    world_height: Final[int]

    player: Player
    boomerang: Boomerang
    sword: Sword
    weapons_icons : list[Texture]
    wall: arcade.SpriteList
    ground: arcade.SpriteList
    crystals: arcade.SpriteList
    map_graph: Final[nx.Graph[tuple[int, int]]]
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

        self.sword = Sword(self.player)

        self.player.equipped_weapons = [self.boomerang, self.sword]

        self.weapons_icons = [ICON_BOOMERANG, ICON_SWORD]
        self.overlay = Overlay(self.weapons_icons)

        # Construit une seule fois : le calcul du graphe est coûteux
        self.map_graph = create_graph(map)

        self.wall = arcade.SpriteList(use_spatial_hash=True)
        self.ground = arcade.SpriteList(use_spatial_hash=True)
        self.crystals = arcade.SpriteList(use_spatial_hash=True)
        self.player_list = arcade.SpriteList()
        self.monsters = arcade.SpriteList(use_spatial_hash=True)
        self.holes = arcade.SpriteList(use_spatial_hash=True)
        self.switches = arcade.SpriteList(use_spatial_hash=True)
        self.gates = arcade.SpriteList(use_spatial_hash=True)
        self.chests = arcade.SpriteList(use_spatial_hash=True)
        self.crystal_gates = arcade.SpriteList(use_spatial_hash=True)
        self.score = 0
        self.boss_room_entered = (map is MAP_BOSS)

        floor_texture = TEXTURE_DUNGEON_FLOOR if map.theme == MapTheme.Dungeon else TEXTURE_GRASS
        wall_texture  = TEXTURE_DUNGEON_WALL  if map.theme == MapTheme.Dungeon else TEXTURE_BUSH

        for i in range(map.width):
            for j in range(map.height):

                self.ground.append(arcade.Sprite(floor_texture, scale=SCALE, center_x=grid_to_pixels(i), center_y=grid_to_pixels(j),))
                cell = map.get(i, j)

                match cell:
                    case GridCell.Grass:
                        pass
                    case GridCell.Bush:
                        self.wall.append(arcade.Sprite(
                                wall_texture,
                                scale=SCALE,
                                center_x=grid_to_pixels(i),
                                center_y=grid_to_pixels(j),
                            )
                        )
                    case GridCell.Cristal:
                        self.crystals.append(arcade.TextureAnimationSprite(
                                animation=ANIMATION_CRISTAUX,
                                scale=SCALE,
                                center_x=grid_to_pixels(i),
                                center_y=grid_to_pixels(j),
                            )
                        )
                    case GridCell.SpinnerH:
                        limits = compute_limits(map, i, j, True)
                        self.monsters.append(Spinner(i, j, True, limits))

                    case GridCell.SpinnerV:
                        limits = compute_limits(map, i, j, False)
                        self.monsters.append(Spinner(i, j, False, limits))

                    case GridCell.Hole:
                        self.holes.append(arcade.Sprite(TEXTURE_HOLE, scale=SCALE, center_x=grid_to_pixels(i), center_y=grid_to_pixels(j)))

                    case GridCell.Bat:
                        self.monsters.append(Bat(grid_to_pixels(i), grid_to_pixels(j), ANIMATION_BAT, self.world_width, self.world_height))

                    case GridCell.Blob:
                        self.monsters.append(Blob(ANIMATION_BLOB, i, j, map, self.map_graph, self.player, self.wall))

                    case GridCell.Switch:
                        switch_conf = next((s for s in map.switches_config if s.x == i and s.y == j), None)
                        switch_id = switch_conf.id if switch_conf else None
                        initial_state = switch_conf.state if switch_conf else False
                        self.switches.append(Switch(grid_to_pixels(i), grid_to_pixels(j), initial_state, switch_id))

                    case GridCell.Gate:
                        gate_conf = next((g for g in map.gates_config if g.x == i and g.y == j), None)
                        open_if = gate_conf.open_if if gate_conf else None
                        gate = Gate(grid_to_pixels(i), grid_to_pixels(j), open_if)
                        self.gates.append(gate)
                        self.wall.append(gate)

                    case GridCell.CrystalGate:
                        cgate = CrystalGate(grid_to_pixels(i), grid_to_pixels(j))
                        self.crystal_gates.append(cgate)
                        self.wall.append(cgate)

                    case GridCell.Chest:
                        self.chests.append(Chest(grid_to_pixels(i), grid_to_pixels(j)))

                    case GridCell.Boss:
                        self.monsters.append(Boss(
                            center_x=grid_to_pixels(i),
                            center_y=grid_to_pixels(j),
                            player=self.player,
                            obstacles=self.wall,
                            chests=self.chests
                        ))
                    case _:
                        assert_never(cell)

        self.physics_engine = arcade.PhysicsEngineSimple(self.player, self.wall)

        # Deux caméras : une suit le monde (joueur), l'autre est fixe pour le HUD
        self.camera = arcade.camera.Camera2D()
        self.ui_camera = arcade.camera.Camera2D()

    def on_show_view(self) -> None:
        self.window.width = min(MAX_WINDOW_WIDTH, self.world_width)
        self.window.height = min(MAX_WINDOW_HEIGHT, self.world_height)



    def on_draw(self) -> None:
        self.clear()
        with self.camera.activate():
            self.ground.draw(pixelated=True)
            self.holes.draw(pixelated=True)
            self.wall.draw(pixelated=True)
            self.switches.draw(pixelated=True)
            self.gates.draw(pixelated=True)
            self.crystals.draw(pixelated=True)
            self.monsters.draw(pixelated=True)
            self.crystal_gates.draw(pixelated=True)
            self.chests.draw(pixelated=True)

            for monster in self.monsters:
                monster.draw_extras()    # bombes + marqueurs + barre de vie


            if not self.sword.is_active:
                arcade.draw_sprite(self.player, pixelated=True)

            current = self.player.equipped_weapons[self.player.current_weapon]
            if current.is_active:
                arcade.draw_sprite(current, pixelated=True)

        with self.ui_camera.activate():
            self.overlay.draw(self.score, self.player.current_weapon, self.player.health_bar, self.window.width, self.window.height)

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        match symbol:
            case arcade.key.SPACE:
                self.window.show_view(GameView(MAP_DECOUVERTE))
            case arcade.key.D:
                self.player.equipped_weapons[self.player.current_weapon].attack()
            case _:
                self.player.on_key_press(symbol, modifiers)

    def on_key_release(self, symbol: int, modifiers: int) -> None:
        self.player.on_key_release(symbol, modifiers)

    def on_update(self, delta_time: float) -> None:
        current = self.player.equipped_weapons[self.player.current_weapon]
        self._update_player(delta_time, current)
        self._update_monsters(delta_time)
        self._collect_crystals(current)
        self._update_combat(current)
        self._update_switch_and_gate(current)
        if self._update_chest_and_crystal_gate(delta_time):
            return
        self.pan_camera_to_player(delta_time)

    def _update_player(self, delta_time: float, current: Weapons) -> None:
        self.physics_engine.update()
        if not self.player.is_attacking:
            self.player.update_animation()
        self.crystals.update_animation()
        current.update_weapon(delta_time)
        self.player.health_bar.update(delta_time)

    def _update_monsters(self, delta_time: float) -> None:
        to_remove = []
        for monster in self.monsters:
            if monster.death_state == MonsterState.alive:
                monster.update_monster(delta_time)
            monster.update_death(delta_time)
            if monster.death_state == MonsterState.dead:
                to_remove.append(monster)
            else:
                monster.update_animation()
        for monster in to_remove:
            monster.on_death()
            self.monsters.remove(monster)

    def _collect_crystals(self, current: Weapons) -> None:
        for x in arcade.check_for_collision_with_list(self.player, self.crystals):
            x.remove_from_sprite_lists()
            self.score += 1
            arcade.play_sound(SOUND_CRYSTAL)
        if current.is_active and current.collects_crystals:
            for x in arcade.check_for_collision_with_list(current.collision_sprite, self.crystals, 3):
                x.remove_from_sprite_lists()
                self.score += 1
                arcade.play_sound(SOUND_CRYSTAL)

    def _update_combat(self, current: Weapons) -> None:
        if current.is_active:
            for monster in arcade.check_for_collision_with_list(current.collision_sprite, self.monsters, 3):
                if monster.death_state == MonsterState.alive:
                    monster.take_hit()

        if any(monster.death_state == MonsterState.alive for monster in arcade.check_for_collision_with_list(self.player, self.monsters)):
            if self.player.take_hit():
                self.window.show_view(GameOverView())

        for monster in self.monsters:
            if monster.projectile_hits_player(self.player):
                if self.player.take_hit():
                    self.window.show_view(GameOverView())

        if self.boomerang.state == BoomerangState.launching:
            for wall in arcade.check_for_collision_with_list(self.boomerang, self.wall):
                self.boomerang.start_returning()

        for hole in self.holes:
            if arcade.math.get_distance(self.player.center_x, self.player.center_y, hole.center_x, hole.center_y) <= HOLE_FALL_DISTANCE:
                self.window.show_view(GameOverView())

    def _update_switch_and_gate(self, current: Weapons) -> None:
        for switch in arcade.check_for_collision_with_list(current, self.switches):
            # Évite de toggler le même switch plusieurs fois lors d'un seul passage de l'arme
            if switch not in current._toggled_switches:
                current._toggled_switches.add(switch)
                switch.toggle()
            if self.boomerang.state == BoomerangState.launching:
                self.boomerang.start_returning()

        switches_dict = {s.switch_id: s for s in self.switches if s.switch_id is not None}
        for gate in self.gates:
            gate.update_state(switches_dict)
            gate.sync_wall(self.wall)

    def _update_chest_and_crystal_gate(self, delta_time: float) -> bool:
        for chest in self.chests:
            chest.update_chest(delta_time)
            if chest.is_open and arcade.check_for_collision(self.player, chest):
                self.window.show_view(GameWonView())
                return True

        crystal_count = len(self.crystals)
        for cgate in self.crystal_gates:
            cgate.update_state(crystal_count)
            cgate.sync_wall(self.wall)

        if not self.boss_room_entered and len(self.crystals) == 0:
            for cgate in self.crystal_gates:
                if arcade.math.get_distance(self.player.center_x, self.player.center_y, cgate.center_x, cgate.center_y) <= TILE_SIZE * 0.5:
                    self.window.show_view(GameView(MAP_BOSS))
                    return True

        return False

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
