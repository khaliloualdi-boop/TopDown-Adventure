import arcade
from healthbar import HealthBar

WEAPON_NAMES = ["BOOMERANG", "SWORD"]


def _make_text(text: str, color: tuple) -> arcade.Text:
    return arcade.Text(text, 0, 0, color, 15, font_name="Arial", bold=True, italic=True, anchor_y="top")


class Overlay:
    """Affiche le HUD : score, arme active et message de victoire."""

    def __init__(self, weapons_icons: list[arcade.Texture]) -> None:
        self.weapons_icons = weapons_icons
        self._score_text  = _make_text("SCORE: 0", arcade.color.ANDROID_GREEN)
        self._weapon_text = _make_text("", arcade.color.DARK_GRAY)

    def draw(self, score: int, current_weapon: int, health_bar: HealthBar,
             window_width: int, window_height: int) -> None:
        self._score_text.text = f"SCORE: {score}"
        self._score_text.x = 20
        self._score_text.y = window_height - 15
        self._score_text.draw()

        weapon_name = WEAPON_NAMES[current_weapon]
        icon = self.weapons_icons[current_weapon]
        icon_w = icon_h = 24
        self._weapon_text.text = weapon_name
        text_x = window_width - 20 - self._weapon_text.content_width
        icon_x = text_x - 8 - icon_w
        arcade.draw_texture_rect(icon, arcade.LBWH(icon_x, window_height - 12 - icon_h, icon_w, icon_h))
        self._weapon_text.x = text_x
        self._weapon_text.y = window_height - 15
        self._weapon_text.draw()

        health_bar.draw(window_width - 58, 15, scale=0.6)
