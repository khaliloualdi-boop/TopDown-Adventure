from __future__ import annotations
from typing import assert_never
import arcade
from arcade import Vec2
from constants import SCALE, TILE_SIZE, BOSS_HIT_DURATION, BOSS_ATTACK_DURATION, BOSS_DEATH_DURATION
from monster import Monster, MonsterState
from player import Player
from bomb import Bomb
from healthbar import HealthBar
from textures import (
    ANIMATION_BOMBERPLANT_IDLE,
    ANIMATION_BOMBERPLANT_ATTACK,
    ANIMATION_BOMBERPLANT_HIT,
    ANIMATION_BOMBERPLANT_DEATH,
)
from enum import Enum


BOSS_MAX_HP = 10
BOMB_COOLDOWN = 2.5
BOSS_SIGHT_RANGE = 9 * TILE_SIZE


class BossState(Enum):
    """États du boss"""
    idle = 0
    attacking = 1
    hit = 2

class Boss(Monster):

    """Plante boss immobile qui lance des bombes vers le joueur lorsqu'il est dans sa ligne de vue."""
    death_animation = ANIMATION_BOMBERPLANT_DEATH
    death_duration = BOSS_DEATH_DURATION

    def __init__(self, center_x: float, center_y: float, player: Player, obstacles: arcade.SpriteList, chests: arcade.SpriteList) -> None:
        super().__init__(animation=ANIMATION_BOMBERPLANT_IDLE, scale=SCALE, center_x=center_x, center_y=center_y)
        self.state: BossState = BossState.idle
        self.player: Player = player
        self.obstacles: arcade.SpriteList = obstacles
        self.bombs: list[Bomb] = []
        self._cooldown: float = BOMB_COOLDOWN
        self._state_timer: float = 0.0
        self.__chests = chests
        self.health_bar = HealthBar(BOSS_MAX_HP)


    def take_hit(self) -> None:
        if self.death_state != MonsterState.alive:
            return
        if self.health_bar.take_hit():
            self.start_dying()
        else:
            self._enter_state(BossState.hit)


    def update_monster(self, delta_time: float) -> None:

        self.health_bar.update(delta_time)
        self._state_timer += delta_time

        match self.state:
            case BossState.hit:
                if self._state_timer >= BOSS_HIT_DURATION:
                    self._enter_state(BossState.idle)
            case BossState.attacking:
                if self._state_timer >= BOSS_ATTACK_DURATION:
                    self._enter_state(BossState.idle)
            case BossState.idle:
                self._try_attack(delta_time)

        for bomb in self.bombs:
            bomb.update_bomb(delta_time)
        self.bombs = [b for b in self.bombs if not b.is_done]


    def draw_extras(self) -> None:
        """Dessine les bombes et le marqueur au sol, puis la barre de vie."""
        for bomb in self.bombs:
            arcade.draw_sprite(bomb.marker)
            arcade.draw_sprite(bomb)
        if self.death_state == MonsterState.alive:
            self.health_bar.draw(self.center_x, self.center_y + 2*TILE_SIZE)

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
            case _:
                assert_never(new_state)

    def _can_see_player(self) -> bool:
        return arcade.has_line_of_sight(self.position, self.player.position, self.obstacles, max_distance=BOSS_SIGHT_RANGE)

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

    def projectile_hits_player(self, player: arcade.Sprite) -> bool:
        return any(bomb.hits_player(player) for bomb in self.bombs)

    def on_death(self) -> None:
        for chest in self.__chests:
            if not chest.is_open:
                chest.open()
