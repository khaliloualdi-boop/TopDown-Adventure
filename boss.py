# boss.py
from __future__ import annotations
import arcade
from arcade import Vec2
from constants import SCALE, TILE_SIZE
from monster import Monster
from player import Player
from bomb import Bomb
from textures import *
from enum import Enum


BOSS_MAX_HP = 10
INVINCIBILITY_DURATION = 0.5  # secondes d'invincibilité après un hit
BOMB_COOLDOWN = 2.5 # secondes entre deux bombes
BOSS_SIGHT_RANGE = 9 * TILE_SIZE


class BossState(Enum):
    idle     = 0
    attacking = 1
    hit      = 2
    dead     = 3


class Boss(Monster):
    """
    Plante boss immobile qui lance des bombes vers le joueur
    lorsqu'il est dans sa ligne de vue.
    """

    hp: int
    state: BossState
    player: Player
    obstacles: arcade.SpriteList
    bombs: list[Bomb]
    _cooldown: float      # temps restant avant la prochaine bombe
    _state_timer: float   # temps passé dans l'état actuel (hit/attack)
    is_alive: bool

    def __init__(
        self,
        cx: float,
        cy: float,
        player: Player,
        obstacles: arcade.SpriteList,
    ) -> None:
        super().__init__(
            animation=ANIMATION_BOMBERPLANT_IDLE,
            scale=SCALE,
            center_x=cx,
            center_y=cy,
        )
        self.hp = BOSS_MAX_HP
        self.state = BossState.idle
        self.player = player
        self.obstacles = obstacles
        self.bombs = []
        self._cooldown = BOMB_COOLDOWN
        self._state_timer = 0.0
        self.is_alive = True
        self._invincibility_timer = 0.0


    def take_hit(self) -> None:
        if not self.is_alive or self._invincibility_timer > 0:
            return
        self._invincibility_timer = INVINCIBILITY_DURATION
        self.hp -= 1
        if self.hp <= 0:
            self._enter_state(BossState.dead)
        else:
            self._enter_state(BossState.hit)



    def update_monster(self, delta_time: float) -> None:
        # Ne fait rien si mort (gameview retirera le sprite)
        if self.state == BossState.dead:
            return

    def update_boss(self, delta: float) -> None:
        if self._invincibility_timer > 0:
            self._invincibility_timer -= delta

        if not self.is_alive:
            return

        self._state_timer += delta

        match self.state:
            case BossState.hit:
                if self._state_timer >= 0.3:
                    self._enter_state(BossState.idle)

            case BossState.attacking:
                if self._state_timer >= 0.5:
                    self._enter_state(BossState.idle)

            case BossState.dead:
                if self._state_timer >= 0.8:
                    self.is_alive = False
                    return

            case BossState.idle:
                self._try_attack(delta)

        # Mise à jour des bombes en vol
        for bomb in self.bombs:
            bomb.update_bomb(delta)
        self.bombs = [b for b in self.bombs if not b.is_done]

        self.update_animation()


    def draw_extras(self) -> None:
        """Dessine les bombes et le marqueur au sol, puis la barre de vie."""
        for bomb in self.bombs:
            arcade.draw_sprite(bomb.marker)
            arcade.draw_sprite(bomb)

        self._draw_health_bar()

    def _draw_health_bar(self) -> None:

        BAR_FULL_WIDTH = TILE_SIZE * 6
        BAR_HEIGHT = TILE_SIZE

        # Position : au-dessus du boss
        hub_x = self.center_x
        hub_y = self.center_y + TILE_SIZE * 2

        #Cadre décoratif
        arcade.draw_texture_rect(
            TEXTURE_HEALTH_HUB,
            arcade.XYWH(hub_x, hub_y, BAR_FULL_WIDTH + TILE_SIZE, BAR_HEIGHT * 1.5),
        )

        #Barre de vie remplie proportionnellement
        fill_ratio = max(self.hp / BOSS_MAX_HP, 0)
        fill_width = BAR_FULL_WIDTH * fill_ratio

        if fill_width > 0:
            arcade.draw_texture_rect(
                TEXTURE_HEALTH_BAR,
                arcade.XYWH(
                    hub_x - (BAR_FULL_WIDTH - fill_width) / 2,
                    hub_y,
                    fill_width,
                    BAR_HEIGHT,
                ),
        )
    def _enter_state(self, new_state: BossState) -> None:
        self.state = new_state
        self._state_timer = 0.0
        match new_state:
            case BossState.idle:
                self.animation = ANIMATION_BOMBERPLANT_IDLE
            case BossState.attacking:
                self.animation = ANIMATION_BOMBERPLANT_ATTACK
            case BossState.hit:
                self.animation = ANIMATION_BOMBERPLANT_HIT
            case BossState.dead:
                self.animation = ANIMATION_BOMBERPLANT_DEATH

    def _can_see_player(self) -> bool:
        dist = (
            (self.center_x - self.player.center_x) ** 2
            + (self.center_y - self.player.center_y) ** 2
        ) ** 0.5
        if dist > BOSS_SIGHT_RANGE:
            return False
        return arcade.has_line_of_sight(
            self.position, self.player.position, self.obstacles
        )

    def _try_attack(self, delta: float) -> None:
        self._cooldown -= delta
        if self._cooldown <= 0 and self._can_see_player():
            self._cooldown = BOMB_COOLDOWN
            self._enter_state(BossState.attacking)
            # Lance la bombe vers la position actuelle du joueur
            bomb = Bomb(
                start=Vec2(self.center_x, self.center_y),
                target=Vec2(self.player.center_x, self.player.center_y),
            )
            self.bombs.append(bomb)
