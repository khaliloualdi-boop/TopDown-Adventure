from map import MAP_DECOUVERTE
from constants import MAX_WINDOW_HEIGHT, MAX_WINDOW_WIDTH, WINDOW_TITLE
import arcade
from gameview import GameView

def main() -> None:
    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = GameView(MAP_DECOUVERTE)
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
