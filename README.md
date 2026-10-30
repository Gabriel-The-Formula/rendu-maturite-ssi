# MEDICA-SERVICES · Audit de maturité SSI et audit technique (TD 2)

Rendu du groupe **Team, Marc, Matteo et Bernard**, Master 2 SSIR. Dépôt prévu le 10 novembre 2026.
Cas fictif pédagogique. La méthode SGDN/DCSSI de 2007 sert de référence historique et ne vaut ni certification ni preuve de conformité actuelle.

## Livrables (dossier `livrables/`)

| Fichier | Contenu |
|---|---|
| `MEDICA-SERVICES_Rapport_audit_SSI.pdf` | Rapport professionnel compilé, 14 pages (G1 à G4, T1 à T5, Gantt, Kanban, feuille de route) |
| `MEDICA-SERVICES_Projet_LaTeX_Overleaf.zip` | Projet LaTeX complet, importable tel quel dans Overleaf (moteur XeLaTeX), avec la présentation CODIR et sa notice `LISEZMOI.md` |
| `MEDICA-SERVICES_Guide_pedagogique.pdf` | Explication pas à pas des analyses, des calculs, des formules Excel et des choix discutables, avec une préparation à l'oral |
| `MEDICA-SERVICES_Grille_Audit_SSI_completee.xlsx` | Grille du TD complétée (onglets 01 à 05, onglet 06 laissé à l'enseignant) |
| `MEDICA-SERVICES_Presentation_CODIR.pdf` | Présentation CODIR de 6 diapositives : 3 risques majeurs, 3 constats décisifs, 3 décisions |

## Résultats clés

- Niveau adéquat **4** (maxima 3, 3, 2, 2, somme 10, sans ajustement, à valider par la DG).
- Niveaux démontrés : stratégie 1, risques 1, règles 2, supervision 1, conception 2, réalisation 1, exploitation 2 (niveau 2 indéterminé pour la stratégie et la réalisation).
- Kanban à son état initial : aucun avancement attesté n'a été fourni, l'équipe déplace les cartes au fil des preuves.
- 11 constats techniques, 6 scénarios de risque, 6 actions retenues pour **116 000 €** sur 120 000 € (marge 4 000 €).

## Régénérer

Toutes les valeurs (notes, niveaux, risques, budget, tâches du planning) viennent de `scripts/donnees.py`.

```bash
python3 scripts/generer.py             # grille Excel + fichiers src/*/donnees/
soffice --headless --calc --convert-to xlsx --outdir /tmp/recalc livrables/MEDICA-SERVICES_Grille_Audit_SSI_completee.xlsx  # puis recopier : stocke les valeurs calculées
cd src/rapport && tectonic -X compile main.tex && tectonic -X compile codir.tex
cd ../guide && tectonic -X compile guide.tex
```

Le modèle vierge de la grille est conservé dans `scripts/modele/`.

## Vérifications effectuées

- Compilation réelle du rapport, du guide et de la présentation avec XeTeX (Tectonic), sans erreur ni débordement signalé, puis contrôle visuel des pages.
- Archive ZIP décompressée dans un dossier vide et recompilée seule.
- Grille recalculée avec LibreOffice et livrée avec ses valeurs calculées : aucune erreur de formule, cible 4, écarts 3/3/2/3/2/3/2, scores 12/12/8/9/4/9, budget respecté.
- Relecture critique indépendante (33 points) intégrée : contenu des PV non inventé, AL-1048 « sans examen tracé », P17 distinguant affirmation contredite et non démontrée, scan WEB01 limité à la DMZ, critères G3 uniformes, risques résiduels de toutes les mesures différées, dépendances début-début.
- Concordance contrôlée par script entre rapport, guide, présentation et Excel, et absence de référence à une pièce inexistante.
- Non vérifié : la compilation avec pdfLaTeX et la compilation sur les serveurs Overleaf eux-mêmes.
