---
name: cartouche-planche
description: Génère un cartouche normalisé étudiant pour une planche d'architecture (info ENSA, projet, étudiante, échelle, date). Déclenche sur cartouche, bloc titre, title block, signature, ENSAPL.
---

# `cartouche-planche` : cartouche étudiant standard

## Vue d'ensemble

Le cartouche est le bloc d'informations en bas à droite de chaque planche. Il identifie le document : qui, quoi, quand, à quelle échelle.

## Contenu obligatoire

- **École** : ENSAPL (École Nationale Supérieure d'Architecture et de Paysage de Lille)
- **Année** : Licence 1, semestre (S1 ou S2)
- **Studio / enseignement** : nom du studio, nom de l'enseignant
- **Étudiante** : prénom NOM
- **Projet** : titre du projet ou du rendu
- **Document** : nature de la planche (analyse, plans, axonométrie...)
- **Numéro de planche** : 1/4, 2/4, etc.
- **Échelle** : 1:100, 1:50, etc. avec barre graphique
- **Date** : jour mois année
- **Orientation Nord** : flèche sur les plans (à mettre dans le dessin, pas dans le cartouche)

## Dimensions recommandées

Bloc de **180 × 40 mm** pour A1, **240 × 50 mm** pour A0.

## Mise en forme

- **Trait de bordure** fin (0,25 mm) autour du cartouche.
- **Lignes intérieures** fines pour séparer les sections.
- Texte en **majuscules** pour les titres de section, **minuscules** pour les valeurs.
- **Police** sans empattement, taille 8 à 10 pt.

## Gabarit type

```
+----------------------------------------------------------------+
| ENSAPL  Licence 1 . S2 . Studio "Habiter le sol"               |
| Enseignant : Mme Y. Durand                                     |
+-------------------------+--------------------+-----------------+
| ÉTUDIANTE               | ÉCHELLE            | DATE            |
| Prénom NOM              | 1/100              | 12 mars 2026    |
+-------------------------+--------------------+-----------------+
| PROJET                  | DOCUMENT           | PLANCHE         |
| Maison à Wambrechies    | Plans + coupes     | 2 / 4           |
+-------------------------+--------------------+-----------------+
| Barre d'échelle 1/100   :  0   1   2   3   4   5 m            |
+----------------------------------------------------------------+
```

## Variantes

### Cartouche minimal (planche d'étude)
Une seule ligne : ENSAPL Licence 1, Prénom NOM, projet, date, échelle.

### Cartouche logo (planche jury)
Avec le logo ENSAPL en haut à gauche du bloc. À récupérer en SVG vectoriel.

### Cartouche bilingue (rendu international)
Doubler les libellés en anglais (Project, Student, Scale, Date).

## Procédure

1. **Demander les infos** manquantes (nom, projet, échelle, date).
2. **Générer le cartouche** au format ASCII (modèle ci-dessus) ou en description précise pour reproduction en InDesign / Illustrator / Archicad / AutoCAD.
3. **Rappeler de l'inclure** sur **chaque planche** et de mettre à jour la numérotation et l'échelle.

## Sortie attendue

Bloc ASCII du cartouche complété, plus optionnellement un fichier `cartouche.txt` à conserver.

## Notes pédagogiques

- Le cartouche est **obligatoire** dans les rendus officiels d'école.
- Un cartouche bien fait fait gagner du temps en jury (le jury sait toujours qui regarde, à quelle échelle).
- Garder un **template cartouche** dans Archicad / AutoCAD pour ne pas le refaire chaque fois.

## Limites

- Le skill ne fait pas le dessin vectoriel, il décrit le contenu et la structure.
