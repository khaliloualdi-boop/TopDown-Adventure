# bomb.py
from __future__ import annotations
import arcade
from arcade import Vec2
from constants import TILE_SIZE, SCALE
from enum import Enum
from textures import (
    ANIMATION_BOMB_UP,
    ANIMATION_BOMB_DOWN,
    ANIMATION_BOMB_EXPLOSION,
    ANIMATION_BOMB_MARKER,
)


BOMB_SPEED = 3
BOMB_EXPLOSION_RADIUS = TILE_SIZE * 1.5
EXPLOSION_DURATION = 0.4   # fractions de secondes pendant lesquelles l'explosion tue


class BombState(Enum):
    flying   = 0   # la bombe monte puis descend vers la cible
    exploding = 1  # explosion en cours (peut tuer le joueur)
    done     = 2   # à retirer de la liste


class Bomb(arcade.TextureAnimationSprite):
    """
    Bombe lancée par la BomberPlant vers la position du joueur.
    Trajectoire : monte vers un point haut, puis redescend sur la cible.
    """

    state: BombState
    target: Vec2          # position au sol visée
    peak: Vec2            # point culminant (milieu de la trajectoire)
    elapsed: float        # temps écoulé dans l'état actuel
    marker: arcade.TextureAnimationSprite  # croix au sol indiquant l'impact

    def __init__(self, start: Vec2, target: Vec2) -> None:
        super().__init__(
            animation=ANIMATION_BOMB_UP,
            scale=SCALE,
            center_x=start.x,
            center_y=start.y,
        )
        self.state = BombState.flying
        self.target = target
        self.elapsed = 0.0

        # Le pic est directement au-dessus de la cible
        self.peak = Vec2(target.x, target.y + TILE_SIZE * 4)
        self._going_up = True   # première moitié du vol

        # Marqueur au sol
        self.marker = arcade.TextureAnimationSprite(
            animation=ANIMATION_BOMB_MARKER,
            scale=SCALE,
            center_x=target.x,
            center_y=target.y,
        )

    @property
    def is_done(self) -> bool:
        return self.state == BombState.done

    @property
    def is_exploding(self) -> bool:
        return self.state == BombState.exploding

    def update_bomb(self, delta: float) -> None:
        self.elapsed += delta

        match self.state:
            case BombState.flying:
                self._move_arc()
                self.update_animation()
                self.marker.update_animation()

            case BombState.exploding:
                self.update_animation()
                if self.elapsed >= EXPLOSION_DURATION:
                    self.state = BombState.done

            case BombState.done:
                pass

    def _move_arc(self) -> None:
        """Déplace la bombe : montée vers le pic, puis descente vers la cible."""
        if self._going_up:
            dest = self.peak
        else:
            dest = self.target

        direction = Vec2(dest.x - self.center_x, dest.y - self.center_y)
        dist = (direction.x ** 2 + direction.y ** 2) ** 0.5

        if dist <= BOMB_SPEED:
            # On atteint le point intermédiaire
            self.center_x = dest.x
            self.center_y = dest.y
            if self._going_up:
                self._going_up = False
                self.animation = ANIMATION_BOMB_DOWN
            else:
                # Impact au sol → explosion
                self._start_explosion()
        else:
            move = direction.normalize()
            self.center_x += move.x * BOMB_SPEED
            self.center_y += move.y * BOMB_SPEED

    def _start_explosion(self) -> None:
        self.state = BombState.exploding
        self.elapsed = 0.0
        self.animation = ANIMATION_BOMB_EXPLOSION

    def hits_player(self, player: arcade.Sprite) -> bool:
        """Retourne True si l'explosion touche le joueur."""
        if self.state != BombState.exploding:
            return False
        dist = (
            (self.center_x - player.center_x) ** 2
            + (self.center_y - player.center_y) ** 2
        ) ** 0.5
        return dist <= BOMB_EXPLOSION_RADIUS