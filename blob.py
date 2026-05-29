from textures import DEATH_ANIMATION_BLOB
from constants import SCALE, TILE_SIZE, BLOB_SPEED, MONSTER_DEATH_DURATION, grid_to_pixels, pixel_to_grid
from monster import Monster
from navmesh import get_path, pixel_to_subnode, subnode_to_pixel, SUBDIVISIONS, path, Node, build_tiles_subnodes
from player import Player
from typing import Final
from map import Map
import arcade
import random
import networkx as nx
from arcade import Vec2

PATROL_RADIUS = 3
MAX_SIGHT_DISTANCE = 5 * TILE_SIZE
CLOSE_DIST = TILE_SIZE/(2*SUBDIVISIONS)


class Blob(Monster):
    """Monstre à pathfinding : patrouille aléatoirement et poursuit le joueur en ligne de vue."""

    death_animation = DEATH_ANIMATION_BLOB
    death_duration = MONSTER_DEATH_DURATION

    def __init__(self, animation: arcade.TextureAnimation, center_x: int, center_y: int, map: Map, map_graph: nx.Graph[tuple[int, int]], player: Player, obstacles: arcade.SpriteList) -> None:
        super().__init__(animation=animation, scale=SCALE, center_x=grid_to_pixels(center_x), center_y=grid_to_pixels(center_y))
        self.map_graph: Final[nx.Graph[Node]] = map_graph
        self.player: Final[Player] = player
        self.obstacles: Final[arcade.SpriteList] = obstacles
        self.possible_destinations: Final[list[Node]] = self.compute_destinations(map, center_x, center_y)
        self.current_destination : Node = (center_x * 2 * SUBDIVISIONS + SUBDIVISIONS, center_y * 2 * SUBDIVISIONS + SUBDIVISIONS)
        self.current_path: path = []
        self._last_player_tile: tuple[int, int] = (-1, -1)


    def compute_destinations(self, map: Map, start_x: int, start_y: int) -> list[Node]:
        destinations = []
        for dx in range(-PATROL_RADIUS, PATROL_RADIUS + 1):
            for dy in range(-PATROL_RADIUS, PATROL_RADIUS + 1):
                center_x, center_y = start_x + dx, start_y + dy
                if 0 <= center_x < map.width and 0 <= center_y < map.height:
                    for node in build_tiles_subnodes(center_x, center_y):
                        if node in self.map_graph:
                            destinations.append(node)
        return destinations


    def can_see_player(self) -> bool:
        return arcade.has_line_of_sight(self.position, self.player.position, self.obstacles, MAX_SIGHT_DISTANCE)

    def _is_at_destination(self) -> bool:
        x = subnode_to_pixel(self.current_destination[0])
        y = subnode_to_pixel(self.current_destination[1])
        dx, dy = x - self.center_x, y - self.center_y
        return dx ** 2 + dy ** 2 <= CLOSE_DIST ** 2

    def _nearest_node(self, px: float, py: float) -> Node:
        sn_x = pixel_to_subnode(px)
        sn_y = pixel_to_subnode(py)
        return min(self.map_graph.nodes,key=lambda n: (n[0] - sn_x) ** 2 + (n[1] - sn_y) ** 2)

    def _set_destination(self, destination: Node) -> None:
        self.current_destination = destination
        source = self._nearest_node(self.center_x, self.center_y)
        full_path = get_path(self.map_graph, source, destination)
        self.current_path = full_path[1:] if len(full_path) > 1 else full_path

    def _choose_random_destination(self) -> None:
        if not self.possible_destinations:
            return
        self._set_destination(random.choice(self.possible_destinations))

    def update_monster(self, delta_time: float) -> None:
        if self.can_see_player():
            player_tile = (pixel_to_grid(self.player.center_x), pixel_to_grid(self.player.center_y))
            if player_tile != self._last_player_tile:
                self._last_player_tile = player_tile
                self._set_destination(self._nearest_node(self.player.center_x, self.player.center_y))
        else:
            self._last_player_tile = (-1, -1)
            if self._is_at_destination() or not self.current_path:
                self._choose_random_destination()

        self.follow_path()

    def follow_path(self) -> None:
        while self.current_path:
            target_x = subnode_to_pixel(self.current_path[0][0])
            target_y = subnode_to_pixel(self.current_path[0][1])

            if arcade.math.get_distance(self.center_x, self.center_y, target_x, target_y) <= CLOSE_DIST:
                self.current_path.pop(0)
            else:
                break

        if not self.current_path:
            return

        target_x = subnode_to_pixel(self.current_path[0][0])
        target_y = subnode_to_pixel(self.current_path[0][1])
        direction = Vec2(target_x - self.center_x, target_y - self.center_y).normalize()
        self.center_x += direction.x * BLOB_SPEED
        self.center_y += direction.y * BLOB_SPEED
