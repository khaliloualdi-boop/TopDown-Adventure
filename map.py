from dataclasses import dataclass
from enum import Enum
from typing import Final
import yaml

class MapTheme(Enum):
    Overworld = "overworld"
    Dungeon = "dungeon"

class GridCell(Enum):
    Bush = "X"
    Grass = " "
    Cristal = "*"
    SpinnerH = "s"
    SpinnerV = "S"
    Hole = "O"
    Bat = "v"
    Switch = "^"
    Gate = "|"
    Blob = "B"
    CrystalGate = "G"
    Chest = "C"
    Boss = "F"

    @property
    def is_walkable(self) -> bool:
        return not (self == GridCell.Hole or self == GridCell.Bush)

conversion = {
    " ": GridCell.Grass,
    "X": GridCell.Bush,
    "x": GridCell.Bush,
    "*": GridCell.Cristal,
    "s": GridCell.SpinnerH,
    "S": GridCell.SpinnerV,
    "O": GridCell.Hole,
    "v": GridCell.Bat,
    "^": GridCell.Switch,
    "|": GridCell.Gate,
    "B": GridCell.Blob,
    "G": GridCell.CrystalGate,
    "C": GridCell.Chest,
    "F": GridCell.Boss,
}

@dataclass(frozen=True)
class Map:
    width: int
    height: int
    player_center_x: int
    player_center_y: int
    grid: tuple[tuple[GridCell,...],...]
    switches_config: tuple[dict]
    gates_config: tuple[dict]
    theme: MapTheme

    def get(self, x: int, y:int) -> GridCell:
        return self.grid[self.height - 1 - y][x]

def map_extract(doc: str) -> Map:
    # definition des variables à utiliser
    height: int
    width: int
    player_center_x: int | None = None
    player_center_y: int | None = None
    grid: list[tuple[GridCell,...]] = []

    if "---" not in doc:
        raise Exception("Format de carte invalide : absence de séparation")

    config_doc: Final[str]
    grid_doc: Final[str]

    config_doc, grid_doc = doc.split("---", 1)

    config = yaml.safe_load(config_doc)

    width = config["width"]
    height = config["height"]

    switches_config = config.get("switches", [])
    gates_config = config.get("gates", [])

    theme = MapTheme(config.get("theme", "overworld"))

    lines = [line.rstrip("\n") for line in grid_doc.splitlines()]
    lines = [line for line in lines if line.strip() and line.strip() != "---"]

    if len(lines) != height:
        raise ValueError(f"Format de carte invalide : nombre de ligne attendu : {height} nombre obtenu : {len(lines)}.")

    for y, line in enumerate(lines):
        if len(line) != width:
            raise ValueError(f"Format de carte invalide : largeur attendue {width} sur la ligne {y}, obtenue {len(line)}.")

        characters: list[GridCell] = []

        for x, char in enumerate(line):
            if char == "P":
                player_center_x, player_center_y = x, height - 1 - y
                characters.append(conversion[" "])  # le point d'apparition est traité comme de l'herbe
            else:
                if char not in conversion:
                    raise ValueError(f"Caractère inconnu '{char}' à la position ({x}, {y}).")
                characters.append(conversion[char])
        grid.append(tuple(characters))

    if player_center_x is None or player_center_y is None:
        raise Exception("Format de carte invalide : aucun point de départ 'P' trouvé.")

    return Map(
        width,
        height,
        player_center_x,
        player_center_y,
        tuple(grid),
        switches_config = tuple(switches_config),
        gates_config = tuple(gates_config),
        theme = theme
    )

def load_map(file: str) -> Map:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    return map_extract(text)

MAP_DECOUVERTE = load_map("maps/map1.txt")
MAP_BOSS = load_map("maps/map2.txt")
