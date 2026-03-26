import arcade

class Monster(arcade.TextureAnimationSprite):
    """
    Classe parent pour tous les monstres.
    """

    def update_monster(self) -> None:
        """
        Méthode à override dans les enfants.
        """
        pass