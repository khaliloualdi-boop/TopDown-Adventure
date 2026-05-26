# Journal

## Progression

* [x] Créer le LOG.md                                                  -
* [x] S'inscrire en binôme                                             -
* [x] Découverte d'Arcade                                              2h
* [x] Affichage initial (carte, joueur, sprites)                       3h15min
* [x] Extraction de la carte depuis un fichier externe                 2h
* [x] Amélioration caméra (dead zone, lerp)                            2h
* [x] Spinners (horizontal et vertical, limites automatiques)          1h30min
* [x] Trous (chute du joueur) et score cristaux                        1h15min
* [x] Classe Player (mouvement 4 directions, animations)               3h
* [x] Boomerang (lancer, retour, collision murs)                       3h30min
* [x] Épée (attaque directionnelle, hitbox)                            2h
* [x] Système d'armes abstrait (`Weapon`)                              1h
* [x] Classe Monster + Bats (rebonds sur les bords de la carte)        2h45min
* [x] Switches et Gates (portes commandées par leviers)                6h
* [x] Blobs (pathfinding A* via navmesh networkx)                      6h
* [x] Boss (BomberPlant, bombes, ligne de vue)                         2h
* [x] Coffre et condition de victoire                                  30min
* [x] Crystal Gate (porte ouverte quand tous les cristaux collectés)   30min
* [x] HealthBar partagée (joueur + boss, i-frames, HUD)                1h30min
* [x] Thème donjon (textures dungeon pour salle du boss)               1h
* [x] Tests unitaires (map, spinner, navmesh)                          3h10min
* [x] `README.md` à jour, expliquant comment jouer					   -

---

## À faire (prochaine étape)

* Khalil : finaliser README.md avec instructions de lancement
* Khalil : Ameliorer le design de la map et refactoriser Gameview.py
* Evan : relire, ajouter et valider les tests unitaires
* Evan : revoir le yaml et améliorer la détection d'erreurs

---

## Suivi

### Semaine 2 (26 fév. 2026)

**Khalil :**
- Mise en place initiale du projet (pyproject.toml, .gitignore, main.py) — 1h
- Prise en main d'arcade et premier design : ajout de tous les assets graphiques (sprites, tilesets, HUD) — 1h
- Affichage initial dans `gameview.py` avec la caméra et les textures — 30 min
- Mouvements et collisions de base (joueur contre murs) —30 min
- Animation du joueur et déplacement fluide de la caméra — 1h
- Cristaux collectables — 45 min
- Ajout du module `textures.py` centralisé — 30 min

### Semaine 3 (2–8 mars 2026)

**Khalil :**
- Extraction de la carte depuis un fichier texte (`map.py`, `maps/map1.txt`) — 2h
	(comprehension de l'extraction de fichier et de la manipulation des chaines de carcatères / fichiers)
- Amélioration de la caméra (dead zone, interpolation lerp) — 2h
	(recherche de ressources internet, inspiration de gameplay zelda 2D et étude de la bibliothèque arcade (gameview, camera, window, lerp))

**Evan :**
- Spinners horizontaux et verticaux avec détection automatique des limites — 1h30
- Tests unitaires pour les spinners (`test_spinner.py`) — 1h

### Semaine 4 (9–15 mars 2026)

**Evan :**
- Ajout des trous (cellule `Hole`, chute du joueur) — 45 min
- Amélioration du score cristaux — 30 min
- Mise à jour des textures et de la carte — 1h

### Semaine 5 (16–22 mars 2026)

**Khalil :**
- Création de la classe `Player` (mouvement 4 directions, animations par direction) — 2h
- Amélioration du mouvement (diagonales normalisées, état d'attaque) — 1h
- Finalisation du mouvement et création du `Boomerang` (lancer, retour automatique, collision murs) — 3h

### Semaine 6 (23–29 mars 2026)

**Evan :**
- Ajout des bats (`Bat`) et de la classe générale `Monster` (base commune pour les ennemis) — 2h
	(recherche d'un lagorthme aléatoire efficace)

**Khalil :**
- Petites améliorations du boomerang et du joueur — 30 min
	(collisions avec les monstres)

### Semaine 7 (30 mars – 6 avr. 2026)

**Evan :**
- Switches et Gates : portes commandées par leviers (`switch.py`, `gate.py`) — 5h
	(compréhension du format yaml et bonne gestion du fichier externe map)
- Bats rebondissent sur les bords de la carte — 45 min
	(réglage de cohérence du jeu)
- Mise à jour de `gameview.py` pour intégrer switches/gates — 1h

**Khalil :**
- Petites corrections et synchronisation des branches — 20 min

### Semaine 8 (Vacances de Pâques)

Pas de commits

### Semaine 9 (13–19 avr. 2026)

Pas de commits

### Semaine 10 (20–26 avr. 2026)

- Création de la classe `Sword` (attaque directionnelle) et du module `Weapon` abstrait — 3h
	(concept de classe abstraite, décision de la hierarchie utilisée)

### Semaine 11 (27 avr. – 3 mai 2026)

Pas de commits

### Semaine 12 (4–10 mai 2026)

**Khalil :**
- Implémentation des Blobs (pathfinding djikstra via navmesh avec networkx) : `blob.py`, `navmesh.py` — 6h
	(compression du navmesh, choix de la representation des nodes et comprehension de la bibliothèque NetworkX,...)
- Ajout des icônes d'armes dans les assets — 15 min
- Correction de bugs (boomerang, sword, player, gameview) — 1h30
	(utilisation du devermineur)

**Evan :**
- Bats : rebonds sur les bords de carte finalisés — 30 min
- Merge des branches — 20 min

### Semaine 13 (11–17 mai 2026)

Pas de commits enregistrés.

### Semaine 14 (18–26 mai 2026)

**Evan :**
- Extension Boss : `boss.py`, `bomb.py`, `chest.py`, `crystal_gate.py` — 3h
	(BomberPlant avec bombes et ligne de vue, coffre de victoire, porte à cristaux)
- Deuxième carte `maps/map2.txt` (salle du boss) — 30 min
- Mise à jour `gameview.py` et `textures.py` pour la transition de carte — 1h
- Tests unitaires `tests/test_map.py` (navmesh, map, switches) — 2h
	(etude des principaux aspects à tester et cibler)

**Khalil :**
- Extension HealthBar partagée : `healthbar.py` (HP, i-frames, HUD texture) intégrée dans `Player` et `Boss` — 1h30
- Thème donjon : `MapTheme` enum, textures dungeon floor/wall pour la salle du boss, modification du Yaml — 1h
- Correction des 4 tests échouants (marqueur P manquant, booléen YAML) — 10 min
- Refactoring global : constantes, types, nettoyage des imports — 8h
- Merge et synchronisation des branches — 15 min
