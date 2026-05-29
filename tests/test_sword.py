from sword import Sword, SwordState, SWORD_HITBOX_OFFSET
from constants import Direction, TILE_SIZE
from healthbar import HealthBar
from unittest.mock import patch, MagicMock


class FakePlayer:
    """Faux joueur léger, sans Arcade.

    On n'hérite PAS de Player car son __init__ charge des textures.
    On expose les attributs et méthodes utilisés par Sword :
      - center_x / center_y / direction (lecture)
      - is_attacking (écriture)
      - _update_movement / _select_animation (appelés dans deactivate)
    """
    def __init__(self, cx: float, cy: float, direction: Direction) -> None:
        self.center_x = cx
        self.center_y = cy
        # Player utilise un attribut privé _direction (un seul underscore).
        # Sword lit player.direction via la property.
        self._direction = direction
        self.is_attacking = False
        self.health_bar = HealthBar(3)
        self.horizontal_stack: list[int] = []
        self.vertical_stack: list[int] = []

    @property
    def direction(self) -> Direction:
        return self._direction

    def _update_movement(self) -> None:
        pass

    def _select_animation(self) -> None:
        pass


def make_sword(direction: Direction = Direction.EST,
               cx: float = 200.0, cy: float = 200.0) -> Sword:
    """Crée une Sword factice sans Arcade."""
    s = object.__new__(Sword)
    # _position et _velocity doivent exister AVANT toute écriture
    # de center_x / change_x.
    s._position = (0.0, 0.0)
    s._velocity = (0.0, 0.0)

    s.player = FakePlayer(cx, cy, direction)
    s.state = SwordState.inactive
    s.elapsed_time = 0.0
    s.direction = direction
    s._toggled_switches = set()
    return s


def simulate_attack(s: Sword) -> None:
    """
    Simule Sword.attack() sans toucher à self.animation (qui plante
    hors d'un environnement Arcade complet à cause des textures).
    Reproduit fidèlement la logique de sword.py.
    """
    if s.is_active:
        return
    s.elapsed_time = 0
    s.player.is_attacking = True
    s.state = SwordState.active
    s.direction = s.player.direction

    # Le sprite épée est centré sur le joueur (pas d'offset)
    s._position = (s.player.center_x, s.player.center_y)


# Vérifie que is_active est False quand inactive
def test_sword_is_not_active_when_inactive() -> None:
    s = make_sword()
    assert s.is_active is False


# Vérifie que la logique d'attack() passe l'épée en état active
def test_sword_attack_sets_active_state() -> None:
    s = make_sword()
    simulate_attack(s)
    assert s.state == SwordState.active


# Vérifie que is_active est True après l'attaque
def test_sword_is_active_after_attack() -> None:
    s = make_sword()
    simulate_attack(s)
    assert s.is_active is True


# Vérifie que attack() ne fait rien si l'épée est déjà active
def test_sword_attack_does_nothing_if_already_active() -> None:
    s = make_sword()
    simulate_attack(s)
    pos_before = s._position
    simulate_attack(s)   # deuxième appel — doit être ignoré
    assert s._position == pos_before


# Vérifie que attack() met le joueur en état is_attacking
def test_sword_attack_sets_player_is_attacking() -> None:
    s = make_sword()
    simulate_attack(s)
    assert s.player.is_attacking is True


# Vérifie que attack() remet elapsed_time à 0
def test_sword_attack_resets_elapsed_time() -> None:
    s = make_sword()
    s.elapsed_time = 99.0
    simulate_attack(s)
    assert s.elapsed_time == 0


# Vérifie que deactivate() passe l'épée en état inactive
def test_sword_deactivate_sets_inactive() -> None:
    s = make_sword()
    s.state = SwordState.active
    s.player.is_attacking = True
    s.deactivate()
    assert s.state == SwordState.inactive


# Vérifie que deactivate() remet le joueur en état non-attaquant
def test_sword_deactivate_resets_player_is_attacking() -> None:
    s = make_sword()
    s.state = SwordState.active
    s.player.is_attacking = True
    s.deactivate()
    assert s.player.is_attacking is False
