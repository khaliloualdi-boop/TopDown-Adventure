from platform import node
from constants import *
from typing import Final
from monster import Monster
from navmesh import *
import random
from player import Player
from math import sqrt
import arcade


class Blob(Monster):

    patrol_graph: Final[nx.Graph[tuple[int, int]]]
    current_path: path
    current_destination: tuple[int,int]
    player: Final[Player]
    obstacles: Final[arcade.SpriteList]
    __attack: bool

    def __init__(self, Animation: arcade.TextureAnimation, cx: int, cy: int, map_graph: nx.Graph[tuple[int, int]], player: Player, Obstacles: arcade.SpriteList) -> None:
        super().__init__(animation = Animation, scale = SCALE, center_x = grid_to_pixels(cx), center_y = grid_to_pixels(cy))
        self.patrol_graph = build_patrol_sub_graph(map_graph, (cx, cy))
        self.current_path = []
        self.player = player
        self.obstacles = Obstacles
        self.__attack = False
        self.last_known_player_node: tuple[int, int] | None = None

    @property
    def player_is_in_patroll_area(self) -> bool:
        player_node = (pixel_to_subnode(self.player.center_x), pixel_to_subnode(self.player.center_y))
        nearest_node = self.nearest_node(self.player.center_x, self.player.center_y)
        return abs(player_node[0] - nearest_node[0]) <=2 and abs(player_node[1] - nearest_node[1]) <=2

    @property
    def is_attacking(self) -> bool:
        return self.__attack

    @is_attacking.setter
    def is_attacking(self, val: bool) -> None:
        self.__attack = val

    def nearest_node(self, px: float, py: float) -> tuple[int, int]:
        sn_x = pixel_to_subnode(px)
        sn_y = pixel_to_subnode(py)
        return min(self.patrol_graph.nodes, key=lambda n: (n[0] - sn_x)**2 + (n[1] - sn_y)**2)

    def choose_random_destination(self) -> None:
        nodes = list(self.patrol_graph.nodes)
        self.current_destination = random.choice(nodes)
        current_node = self.nearest_node(self.center_x, self.center_y)
        self.current_path = get_path(self.patrol_graph, current_node, self.current_destination)

    def move_to_next_node(self, next_node : tuple[int, int]) -> None:
        new_direction = Vec2(subnode_to_pixel(next_node[0]) - self.center_x, subnode_to_pixel(next_node[1]) - self.center_y).normalize()
        self.change_x = new_direction[0] * BLOB_SPEED
        self.change_y = new_direction[1] * BLOB_SPEED

    def attack_player(self) -> None:
        current_node = self.nearest_node(self.center_x, self.center_y)
        player_node = self.nearest_node(self.player.center_x, self.player.center_y)
        path = get_path(self.patrol_graph, current_node, player_node)
        self.current_path = path[1:] if len(path) > 1 else path


    def update_monster(self) -> None:

        if arcade.has_line_of_sight(self.position, self.player.position, self.obstacles) and self.player_is_in_patroll_area:
            player_node = self.nearest_node(self.player.center_x, self.player.center_y)
            if player_node != self.last_known_player_node:
                self.last_known_player_node = player_node
                self.attack_player()
            self.is_attacking = True

        elif self.is_attacking:
            self.is_attacking = False
            self.last_known_player_node = None
            self.current_path = []
            return

        if self.current_path == []:
            self.choose_random_destination()
            return

        if self.distance_from_point(Vec2(subnode_to_pixel(self.current_path[0][0]),subnode_to_pixel(self.current_path[0][1]))) <= TILE_SIZE / (2 * SUBDIVISIONS):
            self.current_path.pop(0)
            return

        else :
            self.move_to_next_node(self.current_path[0])
            self.center_x += self.change_x
            self.center_y += self.change_y


    def distance_from_point(self, vec: Vec2) -> float:
        return sqrt((self.center_x - vec.x)**2 + (self.center_y - vec.y)**2)
