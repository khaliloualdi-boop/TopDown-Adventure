from textures import DEATH_ANIMATION_BAT
import arcade
import random
from arcade import Vec2
from constants import *
import math
from monster import Monster

class Bat(Monster):

    Death_animation = DEATH_ANIMATION_BAT
    Death_duration = MONSTER_DEATH_DURATION

    def __init__(self, x: int, y: int, animation: arcade.TextureAnimation, map_width: int, map_height: int) -> None:
        super().__init__(
            animation=animation,
            scale=SCALE,
            center_x=x,
            center_y=y
        )

        # Position d'origine
        self.origin = Vec2(x, y)

        # Rayon du champ d'action
        self.radius = 3 * TILE_SIZE

        # Limites de la map en pixels (on exclut la tuile de bord, comme les spinners)
        self.min_x = TILE_SIZE
        self.max_x = map_width - TILE_SIZE
        self.min_y = TILE_SIZE
        self.max_y = map_height - TILE_SIZE

        # Générateur aléatoire
        self.rng = random.Random()

        # Direction initiale aléatoire
        angle = self.rng.uniform(0, 2 * math.pi)
        self.change_x = BAT_SPEED * math.cos(angle)
        self.change_y = BAT_SPEED * math.sin(angle)


    def update_monster(self, delta_time : float) -> None:

        # 1. Mouvement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # 2. Rebond sur les bords de la map (comme les spinners sur leurs limites)
        if self.center_x < self.min_x:
            self.center_x = self.min_x
            self.change_x = abs(self.change_x)
        elif self.center_x > self.max_x:
            self.center_x = self.max_x
            self.change_x = -abs(self.change_x)

        if self.center_y < self.min_y:
            self.center_y = self.min_y
            self.change_y = abs(self.change_y)
        elif self.center_y > self.max_y:
            self.center_y = self.max_y
            self.change_y = -abs(self.change_y)

        # 3. Rester dans la zone d'origine
        dist = arcade.math.get_distance(
            self.center_x, self.center_y,
            self.origin.x, self.origin.y
        )

        if dist > self.radius:
            # demi-tour vers centre
            direction = Vec2(
                self.origin.x - self.center_x,
                self.origin.y - self.center_y
            ).normalize()

            self.change_x = direction.x * BAT_SPEED
            self.change_y = direction.y * BAT_SPEED

        # 4. Petit changement aléatoire
        if self.rng.random() < 0.2:  # 20% de chance par frame

            # biais vers direction actuelle
            current = Vec2(self.change_x, self.change_y).normalize()

            random_vec = Vec2(
                self.rng.uniform(-1, 1),
                self.rng.uniform(-1, 1)
            ).normalize()

            new_dir = (current * 0.8 + random_vec * 0.2).normalize()

            self.change_x = new_dir.x * BAT_SPEED
            self.change_y = new_dir.y * BAT_SPEED
