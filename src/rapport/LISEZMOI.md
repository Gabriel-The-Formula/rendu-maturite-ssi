# Projet LaTeX · Rapport d'audit MEDICA-SERVICES

## Importer dans Overleaf

1. Sur Overleaf, cliquer sur **Nouveau projet > Importer un projet (Upload Project)** et choisir l'archive ZIP telle quelle, sans la décompresser.
2. Ouvrir **Menu**, régler **Compilateur** sur **XeLaTeX** et **Document principal** sur `main.tex`.
3. Cliquer sur **Recompiler**. Le rapport compte une page de garde, un sommaire, 13 pages de la synthèse à la conclusion, puis les annexes.

Le moteur de référence est **XeLaTeX**. Le fichier `latexmkrc` demande aussi XeLaTeX. La compilation a été vérifiée avec XeTeX (Tectonic). Le préambule prévoit le cas pdfLaTeX, mais ce moteur n'a pas été testé.

## Contenu

| Fichier ou dossier | Rôle |
|---|---|
| `main.tex` | Document principal du rapport |
| `codir.tex` | Présentation CODIR de 6 diapositives (Beamer). Pour la compiler, la choisir comme document principal |
| `equipe.tex` | Noms du groupe, formation, université, encadrant (vide = bloc masqué), année. C'est le seul fichier à modifier pour la page de garde |
| `images/` | Logo de l'université pour la page de garde |
| `preambule.tex` | Mise en page, palette, polices (Libertinus) |
| `sections/` | Synthèse, introduction, une partie par question du TD, conclusion et annexes. Le texte se modifie ici |
| `figures/` | Figures vectorielles TikZ et pgfplots : organigramme, notes Q01 à Q12, grille des exigences, zones et flux, MFA, vulnérabilités, chronologie, sauvegardes, corrélation, matrice des risques, budget, feuille de route, maturité, Gantt, Kanban |
| `donnees/` | Tableaux et chiffres générés depuis `scripts/donnees.py` (dépôt GitHub) |

## Modifier le texte, les chiffres et les graphiques

- **Texte** : éditer les fichiers de `sections/`.
- **Informations du groupe** : éditer `equipe.tex`.
- **Notes, niveaux, risques, budget, tâches du Gantt et colonnes du Kanban** : la source unique est `scripts/donnees.py` dans le dépôt GitHub. Lancer `python3 scripts/generer.py` régénère `donnees/` et la grille Excel en même temps, ce qui garde le rapport et l'Excel identiques. Sur Overleaf seul, on peut éditer directement les fichiers de `donnees/`. Il faut alors reporter la même modification dans l'Excel.
- **Graphiques** : les figures lisent leurs valeurs dans `donnees/`. Pour l'apparence (couleurs, tailles), éditer `figures/` et les couleurs de `preambule.tex`.
- **Avancement réel** : le Kanban montre l'état attesté au 30 octobre 2026 (version 1 des livrables à relire). Pour le faire évoluer, changer la colonne de chaque tâche dans le dictionnaire `KANBAN` de `scripts/donnees.py`, puis régénérer.
