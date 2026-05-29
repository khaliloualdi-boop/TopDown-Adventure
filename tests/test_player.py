import arcade
from constants import Direction, PLAYER_MOVEMENT_SPEED, PLAYER_MAX_HP
from healthbar import HealthBar, INVINCIBILITY_DURATION
from player import Player
 
def make_player() -> Player:
    """
    Crée un Player factice sans Arcade.
    On bypasse __init__ qui charge des textures, et on set manuellement
    tous les attributs nécessaires.
    """
    p = object.__new__(Player)
    p._velocity = [0.0, 0.0]
    p._position = [0.0, 0.0]
    # Attributs de Player.__init__
    p._direction = Direction.SUD
    p.pressed_keys = set()
    p._horizontal_stack = []
    p._vertical_stack = []
    p.equipped_weapons = []
    p.current_weapon = 0
    p.is_attacking = False
    p.health_bar = HealthBar(PLAYER_MAX_HP)
    p.change_x = 0.0
    p.change_y = 0.0
    return p
 

 
# Vérifie que le joueur regarde vers le sud au départ
def test_player_initially_faces_south() -> None:
    p = make_player()
    assert p.direction == Direction.SUD

# Vérifie que le joueur se déplace à droite quand RIGHT est dans la stack
def test_player_moves_right() -> None:
    p = make_player()
    p._horizontal_stack = [arcade.key.RIGHT]
    p._update_movement()
    assert p.change_x == PLAYER_MOVEMENT_SPEED
    assert p.change_y == 0.0
 
 
# Vérifie que le joueur se déplace à gauche quand LEFT est dans la stack
def test_player_moves_left() -> None:
    p = make_player()
    p._horizontal_stack = [arcade.key.LEFT]
    p._update_movement()
    assert p.change_x == -PLAYER_MOVEMENT_SPEED
    assert p.change_y == 0.0
 
 
# Vérifie que le joueur se déplace vers le haut quand UP est dans la stack
def test_player_moves_up() -> None:
    p = make_player()
    p._vertical_stack = [arcade.key.UP]
    p._update_movement()
    assert p.change_y == PLAYER_MOVEMENT_SPEED
    assert p.change_x == 0.0
 
 
# Vérifie que le joueur se déplace vers le bas quand DOWN est dans la stack
def test_player_moves_down() -> None:
    p = make_player()
    p._vertical_stack = [arcade.key.DOWN]
    p._update_movement()
    assert p.change_y == -PLAYER_MOVEMENT_SPEED
    assert p.change_x == 0.0
 
 
# Vérifie que le joueur peut se déplacer en diagonale
def test_player_moves_diagonally() -> None:
    p = make_player()
    p._horizontal_stack = [arcade.key.RIGHT]
    p._vertical_stack = [arcade.key.UP]
    p._update_movement()
    assert p.change_x == PLAYER_MOVEMENT_SPEED
    assert p.change_y == PLAYER_MOVEMENT_SPEED
 
 
# Vérifie que le joueur s'arrête quand les stacks sont vides
def test_player_stops_when_no_keys() -> None:
    p = make_player()
    p.change_x = PLAYER_MOVEMENT_SPEED
    p.change_y = PLAYER_MOVEMENT_SPEED
    p._horizontal_stack = []
    p._vertical_stack = []
    p._update_movement()
    assert p.change_x == 0.0
    assert p.change_y == 0.0

# Vérifie que si RIGHT et LEFT sont pressés, c'est la dernière pressée qui prime
def test_player_last_horizontal_key_has_priority() -> None:
    p = make_player()
    # RIGHT pressé en premier, LEFT en second → LEFT est la dernière
    p._horizontal_stack = [arcade.key.RIGHT, arcade.key.LEFT]
    p._update_movement()
    assert p.change_x == -PLAYER_MOVEMENT_SPEED
 
 
# Vérifie que si UP et DOWN sont pressés, c'est la dernière pressée qui prime
def test_player_last_vertical_key_has_priority() -> None:
    p = make_player()
    p._vertical_stack = [arcade.key.UP, arcade.key.DOWN]
    p._update_movement()
    assert p.change_y == -PLAYER_MOVEMENT_SPEED

# Vérifie que take_hit retourne False si le joueur a encore de la vie
def test_player_take_hit_returns_false_when_alive() -> None:
    p = make_player()
    result = p.take_hit()
    assert result is False
    assert p.health_bar.hp == PLAYER_MAX_HP - 1
 
 
# Vérifie que take_hit retourne True quand le joueur n'a plus de vie
def test_player_take_hit_returns_true_when_dead() -> None:
    p = make_player()
    p.health_bar = HealthBar(1)
    result = p.take_hit()
    assert result is True
    assert p.health_bar.hp == 0
 
 
# Vérifie que l'invincibilité bloque un deuxième coup immédiat
def test_player_invincibility_blocks_second_hit() -> None:
    p = make_player()
    p.take_hit()          # premier coup
    p.take_hit()          # bloqué par invincibilité
    assert p.health_bar.hp == PLAYER_MAX_HP - 1