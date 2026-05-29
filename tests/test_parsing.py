import pytest
from parsing import parse_map_doc
from map import InvalidMapFileException


# Vérifie qu'une map valide minimale est acceptée
def test_valid_map() -> None:
    doc = "width: 3\nheight: 1\ntheme: overworld\n---\nxPx\n"
    m = parse_map_doc(doc)
    assert m.width == 3


# Vérifie que l'absence de theme lève une exception
def test_missing_theme() -> None:
    doc = "width: 3\nheight: 1\n---\nxPx\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie qu'un theme invalide lève une exception
def test_invalid_theme() -> None:
    doc = "width: 3\nheight: 1\ntheme: unknown\n---\nxPx\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie qu'une grille trop large lève une exception
def test_grid_width_mismatch() -> None:
    doc = "width: 2\nheight: 1\ntheme: overworld\n---\nxPx\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie qu'un caractère inconnu lève une exception
def test_unknown_character() -> None:
    doc = "width: 3\nheight: 1\ntheme: overworld\n---\nxPZ\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie que l'absence de joueur P lève une exception
def test_missing_player() -> None:
    doc = "width: 3\nheight: 1\ntheme: overworld\n---\nxxx\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie que deux joueurs P lèvent une exception
def test_multiple_players() -> None:
    doc = "width: 3\nheight: 1\ntheme: overworld\n---\nPPx\n"
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)


# Vérifie que deux switches avec le même id lèvent une exception
def test_duplicate_switch_id() -> None:
    doc = (
        "width: 3\nheight: 1\ntheme: overworld\n"
        "switches:\n"
        "  - id: sw1\n    x: 0\n    y: 0\n"
        "  - id: sw1\n    x: 2\n    y: 0\n"
        "---\n^P^\n"
    )
    with pytest.raises(InvalidMapFileException):
        parse_map_doc(doc)
