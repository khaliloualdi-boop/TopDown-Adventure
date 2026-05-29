from boss import*
from healthbar import INVINCIBILITY_DURATION


# Vérifie que take_hit ne tue pas le boss si HP > 1
def test_boss_take_hit_does_not_kill_if_hp_above_1() -> None:
    hb = HealthBar(BOSS_MAX_HP)
    for _ in range(BOSS_MAX_HP - 1):
        hb.update(INVINCIBILITY_DURATION)  # lève l'invincibilité
        result = hb.take_hit()
        assert result is False             # pas encore mort
    assert hb.hp == 1
 
 
# Vérifie que le boss meurt exactement au dernier coup
def test_boss_take_hit_kills_at_last_hp() -> None:
    hb = HealthBar(BOSS_MAX_HP)
    for _ in range(BOSS_MAX_HP - 1):
        hb.update(INVINCIBILITY_DURATION)
        hb.take_hit()
    hb.update(INVINCIBILITY_DURATION)
    result = hb.take_hit()               # dernier coup
    assert result is True
    assert hb.hp == 0