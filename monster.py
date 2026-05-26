from enum import Enum, auto
import arcade

class MonsterState(Enum):
    alive = auto()
    dying = auto()
    dead = auto()

class Monster(arcade.TextureAnimationSprite):
    """
    Classe parent pour tous les monstres.
    """
    Death_animation: arcade.TextureAnimation
    Death_duration: float

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.death_state: MonsterState = MonsterState.alive
        self.death_timer: float = 0.0

    def update_monster(self, delta_time: float) -> None:
        """
        Méthode à override dans les enfants.
        """
        pass

    def update_death(self, delta_time: float) -> None:
        if self.death_state != MonsterState.dying:
            return

        self.death_timer += delta_time

        if self.death_timer >= self.Death_duration:
            self.death_state = MonsterState.dead

    def start_dying(self) -> None:
        if self.death_state != MonsterState.alive:
            return

        self.death_state = MonsterState.dying
        self.death_timer = 0.0
        self.change_x = 0
        self.change_y = 0
        self.animation = self.Death_animation
