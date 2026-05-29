from map import Map, GridCell
from parsing import parse_map_doc


# Vérifie qu'une map minimale valide est correctement parsée
def test_map_extract_basic() -> None:
    doc = (
        "width: 3\n"
        "height: 3\n"
        "theme: overworld\n"
        "---\n"
        "xxx\n"
        "xPx\n"
        "xxx\n"
    )
    m = parse_map_doc(doc)
    assert m.width == 3
    assert m.height == 3


# Vérifie que le point de départ P est bien détecté et converti en herbe
def test_map_extract_player_position() -> None:
    doc = (
        "width: 3\n"
        "height: 3\n"
        "theme: overworld\n"
        "---\n"
        "xxx\n"
        "xPx\n"
        "xxx\n"
    )
    m = parse_map_doc(doc)
    assert m.player_center_x == 1
    assert m.player_center_y == 1
    assert m.get(1, 1) == GridCell.Grass

# Vérifie que l'axe Y est bien inversé (première ligne fichier = y max)
def test_map_y_axis_inversion() -> None:
    doc = (
        "width: 1\n"
        "height: 3\n"
        "theme: overworld\n"
        "---\n"
        "*\n"
        "P\n"
        "x\n"
    )
    m = parse_map_doc(doc)
    assert m.get(0, 2) == GridCell.Cristal
    assert m.get(0, 1) == GridCell.Grass
    assert m.get(0, 0) == GridCell.Bush
