from collections.abc import Iterator
import networkx as nx
from map import Map, GridCell
from constants import TILE_SIZE

type path = list[Node]
type Node = tuple[int,int]

SUBDIVISIONS = 3

def build_tiles_subnodes(i: int, j: int) -> Iterator[Node]:
    for k in range(SUBDIVISIONS):
        for p in range(SUBDIVISIONS):
            x = i * (2 * SUBDIVISIONS) + (2 * k + 1)
            y = j * (2 * SUBDIVISIONS) + (2 * p + 1)
            yield(x,y)


def is_near_bush(node: Node, tile_i: int, tile_j: int, map: Map) -> bool:
    x, y = node
    for i in (-1, 0, 1):
        for j in (-1, 0, 1):
            di, dj = tile_i + i, tile_j + j
            if 0 <= di < map.width and 0 <= dj < map.height:
                if map.get(di, dj) == GridCell.Bush:
                    lx = di * 2 * SUBDIVISIONS + SUBDIVISIONS
                    ly = dj * 2 * SUBDIVISIONS + SUBDIVISIONS
                    dist = (x - lx) ** 2 + (y - ly) ** 2
                    if dist < (2 * SUBDIVISIONS) ** 2:
                        return True
    return False

def collect_walkable_nodes(map: Map) -> set[Node]:
    walkables: set[Node] = set()
    for i in range(map.width):
        for j in range(map.height):
            if not map.get(i, j).is_walkable:
                continue
            for node in build_tiles_subnodes(i, j):
                if not is_near_bush(node, i, j, map):
                    walkables.add(node)
    return walkables

def add_edges(graph: nx.Graph[Node], walkables: set[Node]) -> None:
    for node in walkables:
        x, y = node
        for k in (-2, 0, 2):
            for p in (-2, 0, 2):
                neighbor_node = (x + k, y + p)
                if neighbor_node in walkables:
                    weight = 1.414 if k != 0 and p != 0 else 1
                    graph.add_edge(node, neighbor_node, weight = weight)


def create_graph(map: Map) -> nx.Graph[Node]:
    graph : nx.Graph[Node] = nx.Graph()

    walkables = collect_walkable_nodes(map)
    graph.add_nodes_from(walkables)
    add_edges(graph, walkables)

    return graph

def octile_heuristic(node_A: Node, node_B: Node) -> float:
    """Heuristique A* optimisée pour les 8 directions : favorise les diagonales."""
    dx, dy = abs(node_A[0] - node_B[0]), abs(node_A[1] - node_B[1])
    return max(dx,dy) + (1.414 - 1) * min(dx,dy)

def get_path(graph : nx.Graph[Node], current_pos: Node, destination: Node) -> path:
    try :
        return nx.astar_path(graph, current_pos, destination, octile_heuristic, weight="weight")
    except (nx.NetworkXNoPath, nx.NodeNotFound, KeyError):
        return []


def build_patrol_sub_graph(map_graph: nx.Graph[Node], center_tile: Node) -> nx.Graph[Node]:
    cx = center_tile[0] * 2 * SUBDIVISIONS + SUBDIVISIONS
    cy = center_tile[1] * 2 * SUBDIVISIONS + SUBDIVISIONS
    radius = 3 * 2 * SUBDIVISIONS
    patrol_nodes = [node for node in map_graph.nodes if abs(node[0] - cx) <= radius and abs(node[1] - cy) <= radius]
    return map_graph.subgraph(patrol_nodes)

def subnode_to_pixel(x: int) -> float:
    return x * TILE_SIZE / (2 * SUBDIVISIONS)

def pixel_to_subnode(x: float) -> int:
    return round(x * (2 * SUBDIVISIONS) / TILE_SIZE)
