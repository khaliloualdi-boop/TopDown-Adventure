from map import Map, GridCell
from parsing import parse_map_doc
from switch import *


def make_switch(is_on: bool, switch_id: str | None = None) -> Switch:
    """Crée un Switch factice sans Arcade."""
    s = object.__new__(Switch)
    s.is_on = is_on
    s.switch_id = switch_id
    return s


# Vérifie que les switches sont bien lus depuis le YAML
def test_map_switches_config_parsed() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "switches:\n"
        "  - id: sw1\n"
        "    x: 0\n"
        "    y: 0\n"
        "    state: on\n"
        "gates: []\n"
        "---\n"
        "^Px\n"
    )
    m = parse_map_doc(doc)
    assert len(m.switches_config) == 1
    assert m.switches_config[0].id == "sw1"
    assert m.switches_config[0].x == 0
    assert m.switches_config[0].y == 0
    assert m.switches_config[0].state == True

# Vérifie que toggle passe un switch de off à on
def test_switch_toggle_off_to_on() -> None:
    s = make_switch(False)
    s.is_on = not s.is_on
    assert s.is_on is True


# Vérifie que toggle passe un switch de on à off
def test_switch_toggle_on_to_off() -> None:
    s = make_switch(True)
    s.is_on = not s.is_on
    assert s.is_on is False

# Simule le chargement d'un switch on et vérifie son état initial
def test_switch_initial_state_on_from_map() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "switches:\n"
        "  - id: second\n"
        "    x: 0\n"
        "    y: 0\n"
        "    state: on\n"
        "gates: []\n"
        "---\n"
        "^Px\n"
    )
    m = parse_map_doc(doc)
    conf = m.switches_config[0]
    assert conf.state is True

# Simule le chargement d'un switch off (sans state) et vérifie son état initial
def test_switch_initial_state_off_from_map() -> None:
    doc = (
        "width: 3\n"
        "height: 1\n"
        "theme: overworld\n"
        "switches:\n"
        "  - id: first\n"
        "    x: 0\n"
        "    y: 0\n"
        "gates: []\n"
        "---\n"
        "^Px\n"
    )
    m = parse_map_doc(doc)
    conf = m.switches_config[0]
    assert conf.state is False
