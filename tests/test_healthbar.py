from healthbar import*


# Vérifie que les HP diminuent bien d'un point après un coup
def test_healthbar_hp_decreases_after_hit() -> None:
    hb = HealthBar(5)
    hb.take_hit()
    assert hb.hp == 4
 
 
# Vérifie que l'invincibilité empêche un deuxième coup immédiat
def test_healthbar_invincibility_blocks_second_hit() -> None:
    hb = HealthBar(5)
    hb.take_hit()          # premier coup déclenche l'invincibilité
    hb.take_hit()          # deuxième coup immédiat censé etre bloqué
    assert hb.hp == 4      # HP n'a pas diminué une deuxième fois
 
 
# Vérifie que take_hit retourne True quand les HP tombent à 0
def test_healthbar_take_hit_returns_true_when_dead() -> None:
    hb = HealthBar(1)
    result = hb.take_hit()
    assert result is True
    assert hb.hp == 0
 
 
# Vérifie que take_hit retourne False quand il reste des HP
def test_healthbar_take_hit_returns_false_when_alive() -> None:
    hb = HealthBar(3)
    result = hb.take_hit()
    assert result is False
    assert hb.hp == 2
 
 
# Vérifie que update réduit bien le timer d'invincibilité
def test_healthbar_update_reduces_invincibility_timer() -> None:
    hb = HealthBar(5)
    hb.take_hit()                        # déclenche l'invincibilité
    hb.update(INVINCIBILITY_DURATION)    # fait écouler tout le timer
    hb.take_hit()                        # devrait fonctionner maintenant
    assert hb.hp == 3                    # deux coups ont bien été pris