from map import map_extract, Map, GridCell
from spinner import compute_horizontal_limits, compute_vertical_limits
from gate import Gate
from switch import Switch
from navmesh import pixel_to_subnode, subnode_to_pixel, SUBDIVISIONS, create_graph, get_path, build_patrol_sub_graph
from constants import TILE_SIZE

# Vérifie les limites d'un spinner horizontal entre deux buissons
def test_horizontal_limits() -> None:
    doc = (
        "width: 5\n"
        "height: 3\n"
        "---\n"
        "xxxxx\n"
        "xPs x\n"
        "xxxxx\n"
    )
    game_map = map_extract(doc)
    limits = compute_horizontal_limits(game_map, 2, 1)
    assert limits.min_pos == 1
    assert limits.max_pos == 3


# Vérifie les limites d'un spinner vertical entre deux buissons
def test_vertical_limits() -> None:
    doc = (
        "width: 3\n"
        "height: 5\n"
        "---\n"
        "xxx\n"
        "xSx\n"
        "xPx\n"
        "x x\n"
        "xxx\n"
    )
    game_map = map_extract(doc)
    limits = compute_vertical_limits(game_map, 1, 3)
    assert limits.min_pos == 1
    assert limits.max_pos == 3


# Vérifie qu'une map minimale valide est correctement parsée
def test_map_extract_basic() -> None:
    doc = (
        "width: 3\n"
        "height: 3\n"
        "---\n"
        "xxx\n"
        "xPx\n"
        "xxx\n"
    )
    m = map_extract(doc)
    assert m.width == 3
    assert m.height == 3


# Vérifie que le point de départ P est bien détecté et converti en herbe
def test_map_extract_player_position() -> None:
    doc = (
        "width: 3\n"
        "height: 3\n"
        "---\n"
        "xxx\n"
        "xPx\n"
        "xxx\n"
    )
    m = map_extract(doc)
    assert m.player_center_x == 1
    assert m.player_center_y == 1
    assert m.get(1, 1) == GridCell.Grass

# Vérifie que l'axe Y est bien inversé (première ligne fichier = y max)
def test_map_y_axis_inversion() -> None:
    doc = (
        "width: 1\n"
        "height: 3\n"
        "---\n"
        "*\n"
        "P\n"
        "x\n"
    )
    m = map_extract(doc)
    assert m.get(0, 2) == GridCell.Cristal
    assert m.get(0, 1) == GridCell.Grass
    assert m.get(0, 0) == GridCell.Bush


# Vérifie que les switches sont bien lus depuis le YAML
def test_map_switches_config_parsed() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "switches:\n"
        "  - id: sw1\n"
        "    x: 0\n"
        "    y: 0\n"
        "    state: on\n"
        "gates: []\n"
        "---\n"
        "^Px\n"
    )
    m = map_extract(doc)
    assert len(m.switches_config) == 1
    assert m.switches_config[0]["id"] == "sw1"
    assert m.switches_config[0]["x"] == 0
    assert m.switches_config[0]["y"] == 0
    assert m.switches_config[0]["state"] == True


# Vérifie que l'herbe est walkable
def test_grass_is_walkable() -> None:
    assert GridCell.Grass.is_walkable is True


# Vérifie que les buissons ne sont pas walkables
def test_bush_is_not_walkable() -> None:
    assert GridCell.Bush.is_walkable is False


# Vérifie que les trous ne sont pas walkables
def test_hole_is_not_walkable() -> None:
    assert GridCell.Hole.is_walkable is False


# Vérifie que les cristaux sont walkables
def test_crystal_is_walkable() -> None:
    assert GridCell.Cristal.is_walkable is True


# Vérifie que les spinners sont walkables
def test_spinner_is_walkable() -> None:
    assert GridCell.SpinnerH.is_walkable is True
    assert GridCell.SpinnerV.is_walkable is True
