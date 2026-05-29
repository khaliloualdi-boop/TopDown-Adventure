import sys
import arcade
from map import load_map, InvalidMapFileException
from constants import MAX_WINDOW_HEIGHT, MAX_WINDOW_WIDTH, WINDOW_TITLE
from gameview import GameView

def main() -> None:
    path = sys.argv[1] if len(sys.argv) > 1 else "maps/map1.txt"
    try:
        game_map = load_map(path)
    except InvalidMapFileException as e:
        print(f"Erreur dans le fichier de carte '{path}' : {e}")
        return

    # Create the (unique) Window, setup our GameView, and launch
    window = arcade.Window(MAX_WINDOW_WIDTH, MAX_WINDOW_HEIGHT, WINDOW_TITLE)
    game_view = GameView(game_map)
    window.show_view(game_view)
    arcade.run()

if __name__ == "__main__":
    main()
