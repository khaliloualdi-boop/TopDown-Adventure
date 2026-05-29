from ruamel.yaml import YAML
from typing import cast
from map import Map, GridCell, MapTheme, SwitchConfig, GateConfig, conversion, InvalidMapFileException

_yaml = YAML(typ='safe')
_yaml.allow_duplicate_keys = False

def _expect_dict(value: object, label: str) -> dict[str, object]:
    if not isinstance(value, dict):
        raise InvalidMapFileException(f"{label} doit être un dictionnaire")
    return cast(dict[str, object], value)

def _expect_list(value: object, label: str) -> list[object]:
    if not isinstance(value, list):
        raise InvalidMapFileException(f"{label} doit être une liste")
    return cast(list[object], value)

def _expect_type[T](value: object, t: type[T], label: str) -> T:
    if not isinstance(value, t):
        raise InvalidMapFileException(f"{label} doit être {t.__name__}, obtenu {type(value).__name__}")
    return value

def _load_yaml(text: str) -> dict[str, object]:
    try:
        result = _yaml.load(text)
    except Exception as e:
        raise InvalidMapFileException(f"YAML invalide : {e}") from e
    if not isinstance(result, dict):
        raise InvalidMapFileException("L'en-tête YAML doit être un dictionnaire")
    if not all(isinstance(k, str) for k in result):
        raise InvalidMapFileException("Les clés YAML doivent être des chaînes")
    return cast(dict[str, object], result)

def _parse_header(config: dict[str, object]) -> tuple[int, int, MapTheme]:
    for key in ("width", "height", "theme"):
        if key not in config:
            raise InvalidMapFileException(f"Champ obligatoire manquant : '{key}'")

    width  = _expect_type(config["width"], int,  "'width'")
    height = _expect_type(config["height"], int, "'height'")

    try:
        theme = MapTheme(_expect_type(config["theme"], str, "'theme'"))
    except ValueError:
        raise InvalidMapFileException(f"Thème inconnu : '{config['theme']}'")

    return (width, height, theme)

def _get_cell(grid: tuple[tuple[GridCell, ...], ...], height: int, x: int, y: int) -> GridCell:
    return grid[height - 1 - y][x]

def _parse_grid(grid_doc: str, width: int, height: int) -> tuple[tuple[tuple[GridCell, ...], ...], int, int]:

    lines = [line.rstrip("\n") for line in grid_doc.splitlines() if line.strip() and line.strip() != "---"]

    if len(lines) != height:
        raise InvalidMapFileException(f"Nombre de lignes attendu : {height}, obtenu : {len(lines)}")
    grid: list[tuple[GridCell, ...]] = []
    player_x: int | None = None
    player_y: int | None = None

    for row, line in enumerate(lines):
        if len(line) != width:
            raise InvalidMapFileException(
                f"Largeur attendue {width} ligne {height - 1 - row}, obtenue {len(line)}"
            )
        chars: list[GridCell] = []
        for column, char in enumerate(line):
            if char == "P":
                if player_x is not None:
                    raise InvalidMapFileException(f"Plusieurs points de départ 'P' trouvés")
                player_x, player_y = column, height - 1 - row
                chars.append(conversion[" "])
            elif char not in conversion:
                raise InvalidMapFileException(f"Caractère inconnu '{char}' à ({column}, {height - 1 - row})")
            else:
                chars.append(conversion[char])
        grid.append(tuple(chars))

    if player_x is None or player_y is None:
        raise InvalidMapFileException("Aucun point de départ 'P' trouvé")

    return tuple(grid), player_x, player_y


def _parse_switches(switches: object, width: int, height: int, grid: tuple[tuple[GridCell, ...], ...],) -> tuple[tuple[SwitchConfig, ...], set[str]]:

    s_list = _expect_list(switches, "'switches'")

    seen_ids: set[str] = set()
    configs: list[SwitchConfig] = []

    for i, elem in enumerate(s_list):
        sw = _expect_dict(elem, f"switch {i}")

        for key in ("id", "x", "y"):
            if key not in sw:
                raise InvalidMapFileException(f"Switch {i} : champ obligatoire manquant '{key}'")

        sid = _expect_type(sw["id"], str, f"Switch {i} : 'id'")

        if sid in seen_ids:
            raise InvalidMapFileException(f"Switch : id en double '{sid}'")

        sx  = _expect_type(sw["x"], int,  f"Switch '{sid}' : 'x'")

        sy  = _expect_type(sw["y"], int,  f"Switch '{sid}' : 'y'")

        if not (0 <= sx < width and 0 <= sy < height):
            raise InvalidMapFileException(f"Switch '{sid}' : position ({sx},{sy}) hors limites")

        if _get_cell(grid, height, sx, sy) != GridCell.Switch:
            raise InvalidMapFileException(f"Switch '{sid}' : pas de case '^' à ({sx},{sy})")

        state = _expect_type(sw.get("state", "off"), str, f"Switch '{sid}' : 'state'")

        if state not in ("on", "off"):
            raise InvalidMapFileException(f"Switch '{sid}' : 'state' doit être 'on' ou 'off', obtenu '{state}'")

        seen_ids.add(sid)
        configs.append(SwitchConfig(id=sid, x=sx, y=sy, state=(state  == "on")))

    return tuple(configs), seen_ids

__OPERATORS : frozenset[str] = frozenset({"switch_is_on", "and", "or", "not"})

def _validate_condition(cond: object, switch_ids: set[str], gate_index: int, _depth: int = 50) -> None:
    if _depth == 0:
        raise InvalidMapFileException(f"Gate {gate_index} : imbrication de conditions trop profonde (max 50)")

    d = _expect_dict(cond, f"Gate {gate_index} : condition")

    if len(d) != 1:
        raise InvalidMapFileException(f"Gate {gate_index} : une condition doit avoir exactement une clé, obtenu {list(d.keys())}")

    key = _expect_type(next(iter(d)), str, f"Gate {gate_index} : opérateur")

    if key not in __OPERATORS:
        raise InvalidMapFileException(f"Gate {gate_index} : opérateur inconnu '{key}', attendu parmi {set(__OPERATORS)}")

    if key == "switch_is_on":
        sid = _expect_type(d["switch_is_on"], str, f"Gate {gate_index} : 'switch_is_on'")
        if sid not in switch_ids:
            raise InvalidMapFileException(f"Gate {gate_index} : switch inconnu '{sid}'")

    elif key in ("and", "or"):
        sub = _expect_list(d[key], f"Gate {gate_index} : '{key}'")
        if len(sub) == 0:
            raise InvalidMapFileException(f"Gate {gate_index} : '{key}' doit être une liste non vide")
        for c in sub:
            _validate_condition(c, switch_ids, gate_index, _depth - 1)

    else:
        sub = _expect_list(d["not"], f"Gate {gate_index} : 'not'")
        if len(sub) != 1:
            raise InvalidMapFileException(f"Gate {gate_index} : 'not' doit contenir exactement 1 condition")
        _validate_condition(sub[0], switch_ids, gate_index, _depth - 1)


def _parse_gates(r_gates: object, width: int, height: int, grid: tuple[tuple[GridCell, ...], ...], switch_ids: set[str],) -> tuple[GateConfig, ...]:

    gates = _expect_list(r_gates, "'gates'")
    configs: list[GateConfig] = []

    for i, entry in enumerate(gates):
        gt = _expect_dict(entry, f"Gate {i}")

        for key in ("x", "y", "open_if"):
            if key not in gt:
                raise InvalidMapFileException(f"Gate {i} : champ obligatoire manquant '{key}'")

        gx = _expect_type(gt["x"], int, f"Gate {i} : 'x'")
        gy = _expect_type(gt["y"], int, f"Gate {i} : 'y'")

        if not (0 <= gx < width and 0 <= gy < height):
            raise InvalidMapFileException(f"Gate {i} : position ({gx},{gy}) hors limites")

        if _get_cell(grid, height, gx, gy) != GridCell.Gate:
            raise InvalidMapFileException(f"Gate {i} : pas de case '|' à ({gx},{gy})")

        open_if_raw = gt["open_if"]
        if open_if_raw is None:
            open_if: dict[str, object] | None = None
        else:
            open_if = _expect_dict(open_if_raw, f"Gate {i} : 'open_if'")
            _validate_condition(open_if, switch_ids, i)

        configs.append(GateConfig(x=gx, y=gy, open_if=open_if))

    return tuple(configs)


def parse_map_doc(doc: str) -> Map:
    if "---" not in doc:
        raise InvalidMapFileException("Séparation '---' manquante entre l'en-tête et la grille")

    config_doc, grid_doc = doc.split("---", 1)

    config = _load_yaml(config_doc)
    width, height, theme = _parse_header(config)
    grid, player_x, player_y = _parse_grid(grid_doc, width, height)
    switches, switch_ids = _parse_switches(config.get("switches", []), width, height, grid)
    gates = _parse_gates(config.get("gates", []), width, height, grid, switch_ids)

    return Map(
        width=width,
        height=height,
        player_center_x=player_x,
        player_center_y=player_y,
        grid=grid,
        switches_config = switches,
        gates_config = gates,
        theme=theme,
    )
