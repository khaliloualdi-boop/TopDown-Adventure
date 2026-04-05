import arcade
import random
from arcade import Vec2
from constants import *
import math
from monster import Monster

class Bat(Monster):

    def __init__(self, x: int, y: int, animation) -> None:
        super().__init__(
            animation=animation,
            scale=SCALE,
            center_x=x,
            center_y=y
        )

        # Position d'origine
        self.origin = Vec2(x, y)

        # Rayon du champ d’action
        self.radius = 3 * TILE_SIZE

        # Générateur aléatoire
        self.rng = random.Random()

        # Direction initiale aléatoire
        angle = self.rng.uniform(0, 2 * math.pi)
        self.change_x = BAT_SPEED * math.cos(angle)
        self.change_y = BAT_SPEED * math.sin(angle)

    def update_monster(self) -> None:

        # 1. Mouvement
        self.center_x += self.change_x
        self.center_y += self.change_y

        # 2. Rester dans la zone
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

        # 3. Petit changement aléatoire
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