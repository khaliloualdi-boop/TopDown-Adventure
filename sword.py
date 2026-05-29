from weapons import Weapons
from constants import SCALE, TILE_SIZE, SWORD_ATTACK_DURATION, Direction
from player import Player
from textures import SWORD_ATTACK_LIST
from enum import Enum
import arcade


SWORD_HITBOX_OFFSET = TILE_SIZE // 2

class SwordState(Enum):
    """États possibles de l'épée"""
    inactive = 0
    active = 1

class Sword(Weapons):
    """Épée qui attaque dans la direction du joueur pendant une durée fixe."""
    player: Player
    state: SwordState
    direction: Direction
    elapsed_time: float
    hitbox: arcade.SpriteSolidColor

    def __init__(self, player: Player) -> None:
        super().__init__(animation=SWORD_ATTACK_LIST[0], scale=SCALE, center_x=0, center_y=0)
        self.player = player
        self.state = SwordState.inactive
        self.elapsed_time = 0
        self.hitbox = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE, color=arcade.color.RED)

    @property
    def collision_sprite(self) -> arcade.Sprite:
        return self.hitbox

    @property
    def collects_crystals(self) -> bool:
        return True

    @property
    def is_active(self) -> bool:
        return self.state != SwordState.inactive

    def attack(self) -> None:
        if self.is_active:
            return
        self.elapsed_time = 0
        self.player.is_attacking = True
        self.player._update_movement()  # Stoppe immédiatement la vélocité si le joueur se déplaçait au moment de l'attaque
        self.state = SwordState.active
        self.direction = self.player.direction
        self.animation = SWORD_ATTACK_LIST[self.direction.value]

        # Sword sprite centered on player
        self.center_x = self.player.center_x
        self.center_y = self.player.center_y

        self.hitbox = self._get_hitbox()

    def _get_hitbox(self) -> arcade.SpriteSolidColor:
        # Rectangle étroit dans l'axe perpendiculaire pour limiter les frappes latérales et permettre aux ennemis de le toucher par d'autres directions
        match self.direction:
            case Direction.NORD:
                hitbox = arcade.SpriteSolidColor(TILE_SIZE // 2, TILE_SIZE, color=arcade.color.RED)
                hitbox.center_x = self.player.center_x
                hitbox.center_y = self.player.center_y + SWORD_HITBOX_OFFSET
            case Direction.SUD:
                hitbox = arcade.SpriteSolidColor(TILE_SIZE // 2, TILE_SIZE, color=arcade.color.RED)
                hitbox.center_x = self.player.center_x
                hitbox.center_y = self.player.center_y - SWORD_HITBOX_OFFSET
            case Direction.EST:
                hitbox = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE // 2, color=arcade.color.RED)
                hitbox.center_x = self.player.center_x + SWORD_HITBOX_OFFSET
                hitbox.center_y = self.player.center_y
            case Direction.OUEST:
                hitbox = arcade.SpriteSolidColor(TILE_SIZE, TILE_SIZE // 2, color=arcade.color.RED)
                hitbox.center_x = self.player.center_x - SWORD_HITBOX_OFFSET
                hitbox.center_y = self.player.center_y
        return hitbox

    def update_weapon(self, delta: float) -> None:
        if not self.is_active:
            return
        self.elapsed_time += delta
        if self.elapsed_time >= SWORD_ATTACK_DURATION:
            self.deactivate()
            return
        self.update_animation()

    def deactivate(self) -> None:
        self._toggled_switches.clear()
        self.state = SwordState.inactive
        self.player.is_attacking = False
        self.elapsed_time = 0
        self.player._update_movement()
        self.player._select_animation()
