from abc import ABC, abstractmethod
import arcade

class WallObstacle(ABC, arcade.Sprite):
    """Sprite obstacle abstrait qui peut s'ouvrir ou se fermer et se synchronise avec la liste de murs physiques."""

    @property
    @abstractmethod
    def is_open(self) -> bool:
        ...

    def sync_wall(self, walls: arcade.SpriteList) -> None:
        if self.is_open and self in walls:
            walls.remove(self)
        elif not self.is_open and not self in walls:
            walls.append(self)

