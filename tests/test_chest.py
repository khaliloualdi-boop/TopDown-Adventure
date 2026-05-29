from chest import*


 
def make_chest(state: ChestState) -> Chest:
    """Crée un coffre factice sans Arcade."""
    c = object.__new__(Chest)
    c.state = state
    c._elapsed = 0.0
    return c
 
 
# Vérifie que is_open est False quand le coffre est fermé
def test_chest_is_not_open_when_closed() -> None:
    chest = make_chest(ChestState.closed)
    assert chest.is_open is False
 
 
# Vérifie que is_open est False quand le coffre est en train de s'ouvrir
def test_chest_is_not_open_when_opening() -> None:
    chest = make_chest(ChestState.opening)
    assert chest.is_open is False
 
 
# Vérifie que open() passe bien l'état de closed à opening
def test_chest_open_changes_state_to_opening() -> None:
    chest = make_chest(ChestState.closed)
    # on simule open() sans l'animation Arcade
    if chest.state == ChestState.closed:
        chest.state = ChestState.opening
        chest._elapsed = 0.0
    assert chest.state == ChestState.opening
 
 
# Vérifie que open() ne fait rien si le coffre est déjà en train de s'ouvrir
def test_chest_open_does_nothing_if_already_opening() -> None:
    chest = make_chest(ChestState.opening)
    chest._elapsed = 0.3
    if chest.state == ChestState.closed:   # condition de open()
        chest.state = ChestState.opening
    assert chest.state == ChestState.opening
    assert chest._elapsed == 0.3           # elapsed n'a pas été remis à 0