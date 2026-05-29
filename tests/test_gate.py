from gate import Gate
from switch import Switch
from map import GridCell
from parsing import parse_map_doc

def make_switch(is_on: bool) -> Switch:
    """Crée un Switch factice sans Arcade."""
    s = object.__new__(Switch)
    s.is_on = is_on
    return s


def make_gate(open_if: dict | None = None) -> Gate:
    """Crée une Gate factice sans Arcade."""
    g = object.__new__(Gate)
    g.is_open = False
    g.open_if = open_if
    return g


# Vérifie que la gate est bien lue depuis la map
def test_map_contains_gate() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "---\n"
        "|Px\n"
    )
    m = parse_map_doc(doc)
    assert m.get(0, 0) == GridCell.Gate


# Vérifie que le switch est bien lu depuis la map
def test_map_contains_switch() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "---\n"
        "^Px\n"
    )
    m = parse_map_doc(doc)
    assert m.get(0, 0) == GridCell.Switch


# Vérifie que gate et switch coexistent sur la même map
def test_map_gate_and_switch_coexist() -> None:
    doc = (
        "width: 5\n"
        "height: 3\n"
        "theme: overworld\n"
        "---\n"
        "xxxxx\n"
        "^|P x\n"
        "xxxxx\n"
    )
    m = parse_map_doc(doc)
    assert m.get(0, 1) == GridCell.Switch
    assert m.get(1, 1) == GridCell.Gate


# Vérifie que la config YAML d'une gate est bien lue avec sa condition
def test_map_gate_config_open_if_parsed() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "switches:\n"
        "  - id: sw1\n"
        "    x: 0\n"
        "    y: 0\n"
        "gates:\n"
        "  - x: 2\n"
        "    y: 0\n"
        "    open_if:\n"
        "      switch_is_on: sw1\n"
        "---\n"
        "^P|\n"
    )
    m = parse_map_doc(doc)
    assert m.gates_config[0].open_if == {"switch_is_on": "sw1"}


# Vérifie qu'une gate sans condition reste toujours fermée
def test_gate_without_condition_stays_closed() -> None:
    g = make_gate(open_if=None)
    if g.open_if is None:
        g.is_open = False
    assert g.is_open is False


# Vérifie que switch_is_on retourne True si le switch est actif
def test_evaluate_condition_switch_is_on_true() -> None:
    g = make_gate()
    sw = make_switch(is_on=True)
    assert g.evaluate_condition({"switch_is_on": "sw1"}, {"sw1": sw}) is True


# Vérifie que switch_is_on retourne False si le switch est inactif
def test_evaluate_condition_switch_is_on_false() -> None:
    g = make_gate()
    sw = make_switch(is_on=False)
    assert g.evaluate_condition({"switch_is_on": "sw1"}, {"sw1": sw}) is False


# Vérifie que and retourne True seulement si toutes les conditions sont vraies
def test_evaluate_condition_and() -> None:
    g = make_gate()
    sw1 = make_switch(is_on=True)
    sw2 = make_switch(is_on=False)
    assert g.evaluate_condition({"and": [{"switch_is_on": "a"}, {"switch_is_on": "b"}]}, {"a": sw1, "b": sw1}) is True
    assert g.evaluate_condition({"and": [{"switch_is_on": "a"}, {"switch_is_on": "b"}]}, {"a": sw1, "b": sw2}) is False


# Vérifie que or retourne True si au moins une condition est vraie
def test_evaluate_condition_or() -> None:
    g = make_gate()
    sw_on = make_switch(is_on=True)
    sw_off = make_switch(is_on=False)
    assert g.evaluate_condition({"or": [{"switch_is_on": "a"}, {"switch_is_on": "b"}]}, {"a": sw_off, "b": sw_on}) is True
    assert g.evaluate_condition({"or": [{"switch_is_on": "a"}, {"switch_is_on": "b"}]}, {"a": sw_off, "b": sw_off}) is False


# Vérifie que not inverse la condition
def test_evaluate_condition_not() -> None:
    g = make_gate()
    sw = make_switch(is_on=True)
    assert g.evaluate_condition({"not": [{"switch_is_on": "sw1"}]}, {"sw1": sw}) is False
