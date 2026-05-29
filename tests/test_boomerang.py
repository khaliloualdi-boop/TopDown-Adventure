from boomerang import *
import math
from healthbar import HealthBar


class FakePlayer:
    """Faux joueur léger, sans Arcade ni textures.

    On n'hérite PAS de Player car son __init__ charge des textures.
    On expose juste les attributs et la propriété direction utilisés par
    Boomerang.
    """
    def __init__(self, cx: float, cy: float, direction: Direction) -> None:
        self.center_x = cx
        self.center_y = cy
        # Player utilise un attribut privé __direction (name-mangled en
        # _Player__direction). Le boomerang lit player.direction (property),
        # mais on garde le name-mangling au cas où d'autres bouts de code
        # accèdent à l'attribut privé directement.
        self._Player__direction = direction
        self.is_attacking = False
        self.health_bar = HealthBar(3)
        self.horizontal_stack: list[int] = []
        self.vertical_stack: list[int] = []

    @property
    def direction(self) -> Direction:
        return self._Player__direction


def make_boomerang(player_cx: float = 200.0, player_cy: float = 200.0,
                   direction: Direction = Direction.EST) -> Boomerang:
    """Crée un Boomerang factice sans Arcade."""
    b = object.__new__(Boomerang)
    # On initialise _position et _velocity (storage interne d'Arcade)
    # AVANT toute lecture/écriture de center_x ou change_x.
    b._position = (player_cx, player_cy)
    b._velocity = (0.0, 0.0)

    b.player = FakePlayer(player_cx, player_cy, direction)
    b.state = BoomerangState.inactive
    b.direction = direction
    b.origin = Vec2(player_cx, player_cy)
    return b


# Vérifie que is_active est False quand inactif
def test_boomerang_is_not_active_when_inactive() -> None:
    b = make_boomerang()
    assert b.is_active is False


# Vérifie que is_active est True quand en lancement
def test_boomerang_is_active_when_launching() -> None:
    b = make_boomerang()
    b.state = BoomerangState.launching
    assert b.is_active is True


# Vérifie que is_active est True quand le boomerang revient
def test_boomerang_is_active_when_returning() -> None:
    b = make_boomerang()
    b.state = BoomerangState.returning
    assert b.is_active is True


# Vérifie que attack() ne fait rien si déjà actif
def test_boomerang_attack_does_nothing_if_already_active() -> None:
    b = make_boomerang()
    b.state = BoomerangState.launching
    b._position = (999.0, b._position[1])
    b.attack()
    assert b.center_x == 999.0


# Vérifie que l'origine est bien la position du joueur au moment du lancement
def test_boomerang_origin_is_player_position_at_launch() -> None:
    b = make_boomerang(150.0, 300.0, Direction.NORD)
    b.attack()
    assert b.origin.x == 150.0
    assert b.origin.y == 300.0


# Vérifie que le boomerang part depuis la position du joueur
def test_boomerang_starts_at_player_position() -> None:
    b = make_boomerang(150.0, 300.0, Direction.NORD)
    b.attack()
    assert b.center_x == 150.0
    assert b.center_y == 300.0


# Vérifie que le boomerang part vers le nord quand le joueur regarde nord
def test_boomerang_set_change_nord() -> None:
    b = make_boomerang(200.0, 200.0, Direction.NORD)
    b.set_change(Direction.NORD)
    assert b.change_x == 0
    assert b.change_y == BOOMERANG_SPEED


# Vérifie que le boomerang part vers le sud quand le joueur regarde sud
def test_boomerang_set_change_sud() -> None:
    b = make_boomerang()
    b.set_change(Direction.SUD)
    assert b.change_x == 0
    assert b.change_y == -BOOMERANG_SPEED


# Vérifie que le boomerang part vers l'est quand le joueur regarde est
def test_boomerang_set_change_est() -> None:
    b = make_boomerang()
    b.set_change(Direction.EST)
    assert b.change_x == BOOMERANG_SPEED
    assert b.change_y == 0


# Vérifie que le boomerang part vers l'ouest quand le joueur regarde ouest
def test_boomerang_set_change_ouest() -> None:
    b = make_boomerang()
    b.set_change(Direction.OUEST)
    assert b.change_x == -BOOMERANG_SPEED
    assert b.change_y == 0


# Vérifie que return_to_player dirige le boomerang vers le joueur
def test_boomerang_return_to_player_direction() -> None:
    b = make_boomerang(200.0, 200.0)
    b.state = BoomerangState.returning
    b._position = (100.0, 200.0)
    b.return_to_player()
    assert b.change_x > 0
    assert abs(b.change_y) < 0.001


# Vérifie que la vitesse de retour est bien BOOMERANG_SPEED
def test_boomerang_return_to_player_speed() -> None:
    b = make_boomerang(200.0, 200.0)
    b.state = BoomerangState.returning
    b._position = (100.0, 150.0)
    b.return_to_player()
    speed = math.sqrt(b.change_x ** 2 + b.change_y ** 2)
    assert abs(speed - BOOMERANG_SPEED) < 0.001


# Vérifie que le boomerang suit le joueur s'il bouge
def test_boomerang_return_tracks_moving_player() -> None:
    b = make_boomerang(200.0, 200.0)
    b.state = BoomerangState.returning
    b._position = (100.0, 200.0)
    b.player.center_y = 300.0
    b.return_to_player()
    assert b.change_x > 0
    assert b.change_y > 0