from textures import TEXTURE_GATE_OPEN, TEXTURE_GATE_CLOSED
from constants import SCALE
from switch import Switch
import arcade

class Gate(arcade.Sprite):
    def __init__(self, x : int, y : int, open_if: dict | None = None) -> None:
        super().__init__(TEXTURE_GATE_CLOSED, scale=SCALE, center_x=x, center_y=y)
        self.is_open = False
        self.open_if = open_if  # formule YAML de la config

    def update_state(self, switches_dict: dict[str, "Switch"]) -> None:
        if self.open_if is None:
            self.is_open = False
        else:
            self.is_open = self.evaluate_condition(self.open_if, switches_dict)

        self.texture = TEXTURE_GATE_OPEN if self.is_open else TEXTURE_GATE_CLOSED

    def evaluate_condition(self, cond: dict, switches_dict: dict[str, "Switch"]) -> bool:
        """Évalue récursivement la condition open_if"""

        if "switch_is_on" in cond:
            switch_id = cond["switch_is_on"]
            switch = switches_dict.get(switch_id)
            if switch is None:
                return False
            return switch.is_on
        if "and" in cond:
            return all(self.evaluate_condition(c, switches_dict) for c in cond["and"])
        if "or" in cond:
            return any(self.evaluate_condition(c, switches_dict) for c in cond["or"])
        if "not" in cond:
            return not self.evaluate_condition(cond["not"][0], switches_dict)
        raise ValueError(f"Condition inconnue: {cond}")
