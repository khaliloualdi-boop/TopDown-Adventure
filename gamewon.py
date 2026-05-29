from __future__ import annotations
import arcade

ZELDA_FONT = "The Wild Breath of Zelda"


class GameWonView(arcade.View):
    """Écran de victoire."""

    def on_show_view(self) -> None:
        arcade.load_font("assets/The Wild Breath of Zelda.otf")
        self.background_color = arcade.color.BLACK
        cx = self.window.width / 2
        cy = self.window.height / 2
        self._title  = arcade.Text("YOU WIN !", cx, cy + 30, arcade.color.GREEN, 52,
                                   font_name=ZELDA_FONT, anchor_x="center", anchor_y="center")
        self._prompt = arcade.Text("PRESS SPACE TO PLAY AGAIN", cx, cy - 40, arcade.color.WHITE, 16,
                                   font_name="Arial", anchor_x="center", anchor_y="center")

    def on_draw(self) -> None:
        self.clear()
        self._title.draw()
        self._prompt.draw()

    def on_key_press(self, symbol: int, modifiers: int) -> None:
        if symbol == arcade.key.SPACE:
            from gameview import GameView
            from map import MAP_DECOUVERTE
            self.window.show_view(GameView(MAP_DECOUVERTE))
