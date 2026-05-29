from textures import TEXTURE_GATE_OPEN, TEXTURE_GATE_CLOSED
from constants import SCALE
from wall_obstacle import WallObstacle
from switch import Switch

class Gate(WallObstacle):
    """Obstacle qui s'ouvre ou se ferme selon une condition logique portant sur l'état des switches."""
    def __init__(self, x : int, y : int, open_if: dict | None = None) -> None:
        super().__init__(TEXTURE_GATE_CLOSED, scale=SCALE, center_x=x, center_y=y)
        self.__is_open = False
        self.open_if = open_if  # formule YAML de la config

    @property
    def is_open(self) -> bool:
        return self.__is_open

    @is_open.setter
    def is_open(self, val: bool) -> None:
        self.__is_open = val

    def update_state(self, switches_dict: dict[str, "Switch"]) -> None:
        if self.open_if is None:
            self.is_open = False
        else:
            self.is_open = self.evaluate_condition(self.open_if, switches_dict)

        self.texture = TEXTURE_GATE_OPEN if self.is_open else TEXTURE_GATE_CLOSED

    def evaluate_condition(self, cond: dict, switches_dict: dict[str, "Switch"]) -> bool:
        """Évalue récursivement la condition open_if"""

        match cond:
            case {"switch_is_on": switch_id}:
                switch = switches_dict.get(switch_id)
                return switch is not None and switch.is_on
            case {"and": conditions}:
                return all(self.evaluate_condition(c, switches_dict) for c in conditions)
            case {"or": conditions}:
                return any(self.evaluate_condition(c, switches_dict) for c in conditions)
            case {"not": [condition]}:
                return not self.evaluate_condition(condition, switches_dict)
            case _:
                raise ValueError(f"Condition inconnue: {cond}")
