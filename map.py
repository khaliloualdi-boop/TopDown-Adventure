from dataclasses import dataclass
from enum import Enum
from typing import Final

class GridCell(Enum):
    Bush = "X"
    Grass = " "
    Cristal = "*"
    SpinnerH = "s"
    SpinnerV = "S"
    Hole = "O"

conversion = {
    " ": GridCell.Grass,
    "X": GridCell.Bush,
    "x": GridCell.Bush,
    "*": GridCell.Cristal,
    "s": GridCell.SpinnerH,
    "S": GridCell.SpinnerV,
    "O": GridCell.Hole,
}

@dataclass(frozen=True)
class Map:
    width: int
    height: int
    player_center_x: int
    player_center_y: int
    grid: list[list[GridCell]]

    def get(self, x: int, y:int) -> GridCell:
        return self.grid[self.height - 1 - y][x]

def map_extract(doc: str) -> Map:
    # definition des variables à utiliser
    height: int
    width: int
    player_center_x: int | None = None
    player_center_y: int | None = None
    grid: list[list[GridCell]] = []

    if "---" not in doc:
        raise Exception("Format de carte invalide : absence de séparation")

    config_doc: Final[str]
    grid_doc: Final[str]

    config_doc, grid_doc = doc.split("---", 1)

    dimensions: dict[str, str] = {}
    for line in config_doc.splitlines():
        if not line.strip():  # ignore empty lines
            continue
        key, value = line.split(":", 1)
        dimensions[key.strip()] = value.strip()

    height = int(dimensions["height"])
    width = int(dimensions["width"])

    lines = [line.rstrip("\n") for line in grid_doc.splitlines()]
    lines = [line for line in lines if line.strip() and line.strip() != "---"]

    if len(lines) != height:
        raise Exception(f"Format de carte invalide : nombre de ligne attendu : {height} nombre obtenu : {len(lines)}.")

    for y, line in enumerate(lines):
        if len(line) != width:
            raise Exception(f"Format de carte invalide : largeur attendue {width} sur la ligne {y}, obtenue {len(line)}.")

        characters: list[GridCell] = []

        for x, char in enumerate(line):
            if char == "P":
                player_center_x, player_center_y = x, height - 1 - y
                characters.append(conversion[" "])  # le point d'apparition est traité comme de l'herbe
            else:
                if char not in conversion:
                    raise Exception(f"Caractère inconnu '{char}' à la position ({x}, {y}).")
                characters.append(conversion[char])
        grid.append(characters)

    if player_center_x is None or player_center_y is None:
        raise Exception("Format de carte invalide : aucun point de départ 'P' trouvé.")

    return Map(width, height, player_center_x, player_center_y, grid)

def load_map(file: str) -> Map:
    with open(file, "r", encoding="utf-8") as f:
        text = f.read()
    return map_extract(text)

MAP_DECOUVERTE = load_map("maps/map1.txt")

# 1. lire le fichier
# 2. separer la partie config et la partie map
# 3. determiner les dimensions de la carte
# 4. stocker les caracteres un par un sous a forme de vecteur (x, y , char)
# 5. methode de conversion char -> GridCell
# 6. Créer les erreurs possibles :
    # Height non respectée
    # Width non respectée
    # charactère non defini
    # non presence de 'P'
    # format non repsecté (ex: non presence de "---")
