# Adventure

Un jeu d'aventure en vue du dessus inspiré de Zelda, développé en Python avec la bibliothèque arcade.


## Lancer le jeu

```bash
uv run main.py
```

## Comment jouer

### Contrôles

| Touche | Action |
|--------|--------|
| Flèches directionnelles | Déplacer le personnage |
| Espace | Attaquer avec l'arme équipée |
| R | Changer d'arme (Boomerang / Épée) |

### Objectif

Explorez le monde, éliminez les ennemis et atteignez la salle du boss. Collectez les cristaux pour ouvrir la porte de cristal. Activez les interrupteurs pour débloquer les portes verrouillées. Battez le boss final pour gagner.

### Ennemis

- **Blob** — ennemi lent qui se déplace aléatoirement
- **Chauve-souris** — ennemi rapide qui pourchasse le joueur
- **Spinner** — patrouille sur un chemin fixe
- **Boss** — ennemi puissant gardant la salle finale

### Objets

- **Coffre** — marchez dessus pour l'ouvrir et gagner la partie
- **Cristal** — collectez-les tous pour déverrouiller la porte de cristal
- **Interrupteur** — marchez dessus pour ouvrir ou fermer les gates

### Vie

Vous démarrez avec 3 coeurs. Toucher un ennemi vous inflige des dégâts. Si votre vie tombe à zéro, c'est game over.
