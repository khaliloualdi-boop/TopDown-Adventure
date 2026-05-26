from abc import ABC, abstractmethod
from enum import Enum, auto
from player import Player
import arcade

class MonsterState(Enum):
    alive = auto()
    dying = auto()
    dead = auto()

class Monster(ABC, arcade.TextureAnimationSprite):
    """
    Classe parent pour tous les monstres.
    """

    def __init__(self, animation: arcade.TextureAnimation, scale: float, center_x: float, center_y: float) -> None:
        super().__init__(animation=animation, scale=scale, center_x=center_x, center_y=center_y)
        self.death_state: MonsterState = MonsterState.alive
        self.death_timer: float = 0.0

    @property
    @abstractmethod
    def death_animation(self) -> arcade.TextureAnimation:
        ...

    @property
    @abstractmethod
    def death_duration(self) -> float:
        ...

    @abstractmethod
    def update_monster(self, delta_time: float) -> None:
        """
        Méthode à override dans les enfants.
        """
        ...

    def update_death(self, delta_time: float) -> None:
        if self.death_state != MonsterState.dying:
            return

        self.death_timer += delta_time

        if self.death_timer >= self.death_duration:
            self.death_state = MonsterState.dead

    def take_hit(self) -> None:
        self.start_dying()

    def start_dying(self) -> None:
        if self.death_state != MonsterState.alive:
            return

        self.death_state = MonsterState.dying
        self.death_timer = 0.0
        self.change_x = 0
        self.change_y = 0
        self.animation = self.death_animation

    def on_death(self) -> None:
        pass

    def draw_extras(self) -> None:
        pass

    def projectile_hits_player(self, player: Player) -> bool:
        return False
