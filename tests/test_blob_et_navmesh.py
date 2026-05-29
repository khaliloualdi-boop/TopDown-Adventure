from map import Map, GridCell, MapTheme
from navmesh import create_graph, collect_walkable_nodes, get_path, build_tiles_subnodes, SUBDIVISIONS


def make_open_map(W: int = 5, H: int = 5) -> Map:
    """Carte W×H avec murs en bordure et intérieur ouvert."""
    B, G = GridCell.Bush, GridCell.Grass
    grid = tuple(
        tuple(B if (col == 0 or col == W - 1 or row == 0 or row == H - 1) else G
              for col in range(W))
        for row in range(H)
    )
    return Map(width=W, height=H, player_center_x=W // 2, player_center_y=H // 2,
               grid=grid, switches_config=(), gates_config=(), theme=MapTheme.Overworld)


# Vérifie que les cases Bush ne génèrent pas de nœuds walkables
def test_walkable_nodes_excludes_walls() -> None:
    m = make_open_map()
    nodes = collect_walkable_nodes(m)
    for node in build_tiles_subnodes(0, 0):  # coin Bush
        assert node not in nodes


# Vérifie que le graphe contient des nœuds pour l'intérieur ouvert
def test_create_graph_has_nodes() -> None:
    m = make_open_map()
    g = create_graph(m)
    assert g.number_of_nodes() > 0


# Vérifie qu'un chemin existe entre deux tuiles intérieures
def test_get_path_finds_route() -> None:
    m = make_open_map()
    g = create_graph(m)
    start_nodes = [n for n in build_tiles_subnodes(1, 1) if n in g]
    end_nodes   = [n for n in build_tiles_subnodes(3, 3) if n in g]
    assert start_nodes and end_nodes
    path = get_path(g, start_nodes[0], end_nodes[0])
    assert len(path) > 0


# Vérifie qu'une map entièrement fermée (aucune case walkable) donne un graphe vide
def test_full_wall_map_gives_empty_graph() -> None:
    B = GridCell.Bush
    grid = tuple(tuple(B for _ in range(3)) for _ in range(3))
    m = Map(width=3, height=3, player_center_x=1, player_center_y=1,
            grid=grid, switches_config=(), gates_config=(), theme=MapTheme.Overworld)
    g = create_graph(m)
    assert g.number_of_nodes() == 0
