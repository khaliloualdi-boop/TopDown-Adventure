from bat import TILE_SIZE
from arcade import Vec2
import networkx as nx
from map import Map, GridCell


type path = list[tuple[int, int]]

SUBDIVISIONS = 3

def build_tiles_subnodes(i: int, j: int) -> list[tuple[int, int]]:
    positions = []
    for k in range(SUBDIVISIONS):
        for p in range(SUBDIVISIONS):
            x = i * (2 * SUBDIVISIONS) + (2 * k + 1)
            y = j * (2 * SUBDIVISIONS) + (2 * p + 1)
            positions.append((x,y))

    return positions

def create_graph(map: Map) -> nx.Graph[tuple[int, int]]:
    graph: nx.Graph[tuple[int, int]] = nx.Graph()
    walkables: set[tuple[int, int]] = set()

    non_walkable_centers = [(i * 2 * SUBDIVISIONS + SUBDIVISIONS, j * 2 * SUBDIVISIONS + SUBDIVISIONS) for i in range(map.width) for j in range(map.height) if not map.get(i , j).is_walkable]

    for i in range(map.width):
        for j in range(map.height):
            if map.get(i,j).is_walkable:
                for node in build_tiles_subnodes(i, j):
                    if not any(abs(node[0] - bush_x) < 2 * SUBDIVISIONS and abs(node[1] - bush_y) < 2 * SUBDIVISIONS for bush_x, bush_y in non_walkable_centers):
                        graph.add_node(node)
                        walkables.add(node)

    for node in walkables:
        x , y = node
        for k in [-2, 0, 2]:
            for p in [-2, 0, 2]:
                if k == 0 and p == 0:
                    continue
                neighbor = (x + k, y + p)
                if neighbor in walkables:
                    Weight = 1.414 if k != 0 and p != 0 else 1
                    graph.add_edge((x,y), neighbor, weight = Weight)

    return graph

def subnode_to_pixel(x: int) -> float:
    return x * TILE_SIZE / (2 * SUBDIVISIONS)

def pixel_to_subnode(x: float) -> int:
    return round(x * (2 * SUBDIVISIONS) / TILE_SIZE)

def get_path(graph : nx.Graph[tuple[int, int]], current_pos: tuple[int,int], destination: tuple[int, int]) -> path:
    try :
        paths = nx.single_source_dijkstra_path(graph, current_pos, weight="weight")
        return paths[destination]
    except (nx.NetworkXNoPath, nx.NodeNotFound, KeyError):
        return []


def build_patrol_sub_graph(map_graph: nx.Graph[tuple[int, int]], center_tile: tuple[int, int]) -> nx.Graph[tuple[int, int]]:
    cx = center_tile[0] * 2 * SUBDIVISIONS + SUBDIVISIONS
    cy = center_tile[1] * 2 * SUBDIVISIONS + SUBDIVISIONS
    radius = 3 * 2 * SUBDIVISIONS
    patrol_nodes = [node for node in map_graph.nodes if abs(node[0] - cx) <= radius and abs(node[1] - cy) <= radius]
    return map_graph.subgraph(patrol_nodes)
