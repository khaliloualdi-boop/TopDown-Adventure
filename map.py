from dataclasses import dataclass
from enum import Enum

class InvalidMapFileException(Exception):
    """Levée lorsqu'un fichier de carte est malformé ou ne passe pas la validation."""
    pass

class MapTheme(Enum):
    """ Thème visuel d'une carte """
    Overworld = "overworld"
    Dungeon = "dungeon"

class GridCell(Enum):
    """Type d'une cellule dans la grille"""
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
        return self != GridCell.Hole and self != GridCell.Bush

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
class SwitchConfig:
    """Représentation immuable de la configuration d'un switch"""
    id: str
    x: int
    y: int
    state: bool


@dataclass(frozen=True)
class GateConfig:
    """Représentation immuable de la configuration d'un gate"""
    x: int
    y: int
    open_if: dict | None


@dataclass(frozen=True)
class Map:
    """Représentation immuable d'une carte de jeu chargée depuis un fichier."""
    width: int
    height: int
    player_center_x: int
    player_center_y: int
    grid: tuple[tuple[GridCell,...],...]
    switches_config: tuple[SwitchConfig,...]
    gates_config: tuple[GateConfig,...]
    theme: MapTheme

    def get(self, x: int, y: int) -> GridCell:
        return self.grid[self.height - 1 - y][x]

# Fonction qui utilise le protocole établit dans le module parsing afin de charger une Map d'un fichier .txt

def load_map(file: str) -> Map:
    from parsing import parse_map_doc
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    return parse_map_doc(text)



MAP_DECOUVERTE = load_map("maps/map1.txt")
MAP_BOSS = load_map("maps/map2.txt")
