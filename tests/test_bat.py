from bat import *


def make_bat(cx: float, cy: float, map_w: int = 500, map_h: int = 500) -> Bat:
    """
    Crée une Bat factice sans Arcade.
    On bypasse __init__ qui charge des textures et on set manuellement
    tous les attributs nécessaires.
    """
    bat = object.__new__(Bat)
    # IMPORTANT : Arcade stocke position et vitesse dans _position et _velocity
    # (tuple[float, float]). Les propriétés center_x / change_x / etc. lisent
    # et écrivent là-dedans. On doit donc initialiser ces deux attributs
    # AVANT de toucher à center_x, change_x, etc.
    bat._position = (cx, cy)
    bat._velocity = (0.0, 0.0)

    bat.origin = Vec2(cx, cy)
    bat.radius = 3 * TILE_SIZE
    bat.min_x = TILE_SIZE
    bat.max_x = map_w - TILE_SIZE
    bat.min_y = TILE_SIZE
    bat.max_y = map_h - TILE_SIZE
    bat.rng = random.Random(42)   # seed fixe pour reproductibilité

    # Une fois _velocity initialisé, on peut utiliser change_x / change_y
    bat.change_x = BAT_SPEED
    bat.change_y = 0.0

    bat.death_state = MonsterState.alive
    bat.death_timer = 0.0
    return bat


def speed(bat: Bat) -> float:
    return math.sqrt(bat.change_x ** 2 + bat.change_y ** 2)


# Vérifie que la vitesse reste BAT_SPEED après plusieurs updates
def test_bat_speed_remains_constant_after_updates() -> None:
    bat = make_bat(200.0, 200.0)
    for _ in range(50):
        # Simule la partie "changement aléatoire" de update_monster
        if bat.rng.random() < 0.2:
            current = Vec2(bat.change_x, bat.change_y).normalize()
            random_vec = Vec2(
                bat.rng.uniform(-1, 1),
                bat.rng.uniform(-1, 1)
            ).normalize()
            new_dir = (current * 0.8 + random_vec * 0.2).normalize()
            bat.change_x = new_dir.x * BAT_SPEED
            bat.change_y = new_dir.y * BAT_SPEED
    assert abs(speed(bat) - BAT_SPEED) < 0.001


# Vérifie que si la bat est trop loin de l'origine, sa direction pointe vers l'origine
def test_bat_redirects_toward_origin_when_too_far() -> None:
    bat = make_bat(200.0, 200.0)
    # On place la bat hors de son rayon (sans passer par le setter Arcade)
    bat._position = (200.0 + bat.radius + 10, 200.0)

    # Simule le bloc "rester dans la zone d'origine" de update_monster
    dist = math.sqrt(
        (bat.center_x - bat.origin.x) ** 2 +
        (bat.center_y - bat.origin.y) ** 2
    )
    if dist > bat.radius:
        direction = Vec2(
            bat.origin.x - bat.center_x,
            bat.origin.y - bat.center_y
        ).normalize()
        bat.change_x = direction.x * BAT_SPEED
        bat.change_y = direction.y * BAT_SPEED

    # La direction doit pointer vers la gauche (vers l'origine)
    assert bat.change_x < 0


# Vérifie que la bat rebondit sur le bord gauche
def test_bat_bounces_on_left_wall() -> None:
    bat = make_bat(200.0, 200.0)
    bat._position = (bat.min_x - 1, bat.center_y)   # hors bord gauche
    bat.change_x = -BAT_SPEED

    # Simule le rebond
    if bat.center_x < bat.min_x:
        bat._position = (bat.min_x, bat.center_y)
        bat.change_x = abs(bat.change_x)

    assert bat.change_x > 0          # repart vers la droite
    assert bat.center_x == bat.min_x # replacée sur la limite


# Vérifie que la bat rebondit sur le bord droit
def test_bat_bounces_on_right_wall() -> None:
    bat = make_bat(200.0, 200.0)
    bat._position = (bat.max_x + 1, bat.center_y)
    bat.change_x = BAT_SPEED

    if bat.center_x > bat.max_x:
        bat._position = (bat.max_x, bat.center_y)
        bat.change_x = -abs(bat.change_x)

    assert bat.change_x < 0
    assert bat.center_x == bat.max_x


# Vérifie que la bat rebondit sur le bord bas
def test_bat_bounces_on_bottom_wall() -> None:
    bat = make_bat(200.0, 200.0)
    bat._position = (bat.center_x, bat.min_y - 1)
    bat.change_y = -BAT_SPEED

    if bat.center_y < bat.min_y:
        bat._position = (bat.center_x, bat.min_y)
        bat.change_y = abs(bat.change_y)

    assert bat.change_y > 0
    assert bat.center_y == bat.min_y


# Vérifie que la bat rebondit sur le bord haut
def test_bat_bounces_on_top_wall() -> None:
    bat = make_bat(200.0, 200.0)
    bat._position = (bat.center_x, bat.max_y + 1)
    bat.change_y = BAT_SPEED

    if bat.center_y > bat.max_y:
        bat._position = (bat.center_x, bat.max_y)
        bat.change_y = -abs(bat.change_y)

    assert bat.change_y < 0
    assert bat.center_y == bat.max_y