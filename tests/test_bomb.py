from bomb import *


def make_bomb(state: BombState, cx: float, cy: float) -> Bomb:
    """Crée une bombe factice sans Arcade."""
    b = object.__new__(Bomb)
    # IMPORTANT : on initialise d'abord _position (storage interne d'Arcade),
    # PAS center_x (qui est une property et qui appellerait des setters
    # qui touchent à _hit_box, lequel n'existe pas).
    b._position = [cx, cy]
    b._velocity = [0.0, 0.0]
    b.state = state
    return b


def make_player(cx: float, cy: float) -> arcade.Sprite:
    """Crée un faux joueur avec juste les coordonnées nécessaires."""
    p = object.__new__(arcade.Sprite)
    # Même chose : on bypasse center_x en écrivant directement dans _position.
    p._position = [cx, cy]
    p._velocity = [0.0, 0.0]
    return p


# Vérifie que hits_player retourne False si la bombe est encore en vol
def test_bomb_hits_player_false_when_flying() -> None:
    bomb = make_bomb(BombState.flying, 100.0, 100.0)
    player = make_player(100.0, 100.0)
    assert bomb.hits_player(player) is False


# Vérifie que hits_player retourne False si la bombe est done
def test_bomb_hits_player_false_when_done() -> None:
    bomb = make_bomb(BombState.done, 100.0, 100.0)
    player = make_player(100.0, 100.0)
    assert bomb.hits_player(player) is False


# Vérifie que hits_player retourne True si explosion et joueur dans le rayon
def test_bomb_hits_player_true_when_exploding_close() -> None:
    bomb = make_bomb(BombState.exploding, 100.0, 100.0)
    player = make_player(105.0, 100.0)
    assert bomb.hits_player(player) is True


# Vérifie que hits_player retourne False si explosion mais joueur trop loin
def test_bomb_hits_player_false_when_exploding_far() -> None:
    bomb = make_bomb(BombState.exploding, 100.0, 100.0)
    player = make_player(100.0 + BOMB_EXPLOSION_RADIUS + 10, 100.0)
    assert bomb.hits_player(player) is False