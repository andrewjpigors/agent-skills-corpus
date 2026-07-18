---
name: hachures-materiaux
description: Conventions graphiques des matériaux en coupe (hachures, motifs, normalisation NF). Déclenche sur hachures, matériaux en coupe, béton, brique, bois, isolant, terre, eau, hachurage.
---

# `hachures-materiaux` : représentation des matériaux en coupe

## Vue d'ensemble

Quand on coupe un mur dans une coupe technique, chaque matériau a sa convention graphique. Ces hachures permettent de "lire" la composition sans légende.

## Conventions usuelles (norme NF EN ISO 128-50 et usage)

| Matériau | Représentation graphique |
|---|---|
| Béton armé | Hachures fines à 45° + points (les points = armatures) |
| Béton (non armé) | Hachures fines à 45° |
| Béton banché | Trait + texture pointillée fine |
| Maçonnerie brique | Briques dessinées en élévation, ou hachures croisées |
| Pierre de taille | Texture irrégulière en forme de moellons appareillés |
| Bois (coupe transversale, fil visible) | Anneaux concentriques ou texture en cernes |
| Bois (coupe longitudinale, fil) | Lignes parallèles légèrement ondulées |
| Acier | Plein noir ou hachures serrées à 45° |
| Verre | Trois lignes parallèles fines |
| Isolant souple (laine minérale, laine de bois) | Vagues régulières |
| Isolant rigide (polystyrène, PIR) | Petits ronds ou bulles |
| Isolant biosourcé en vrac (ouate, paille) | Texture irrégulière |
| Terre / remblai | Petits triangles répétés, ou texture pointée |
| Terre cuite | Hachures croisées fines |
| Eau, nappe phréatique | Lignes horizontales ondulées |
| Étanchéité (membrane) | Trait épais ondulé |
| Pare-vapeur, pare-pluie | Trait épais avec petits points |
| Carrelage | Carrelage dessiné, ou hachures croisées orthogonales fines |

## Échelle et lisibilité

- À **1/100** : on ne hachure pas les murs (trop fin), on les **remplit en noir** ou en gris uni.
- À **1/50** : on commence à différencier les matériaux par hachures légères.
- À **1/20 et plus** : hachures détaillées, chaque couche identifiable.

## Conventions complémentaires

- **Épaisseur des couches** : à respecter à l'échelle (un isolant de 20 cm fait 4 mm sur un dessin au 1/50).
- **Légende obligatoire** : même avec des hachures normalisées, ajouter une légende sur la première coupe technique.
- **Couleur** : autorisée en rendu pédagogique pour rendre la coupe plus lisible (orange = brique, bleu = isolant, jaune = bois, etc.). Pas pour un document officiel.

## Procédure

1. **Identifier l'échelle de la coupe** pour savoir quel niveau de hachure produire.
2. **Lister les matériaux** présents dans la coupe.
3. **Donner les conventions** correspondantes.
4. **Recommander une légende type**.

## Sortie attendue

```
Coupe au 1/20, mur extérieur

De l'extérieur vers l'intérieur :
1. Bardage bois (lignes parallèles ondulées)
2. Lame d'air ventilée (vide, légende "lame d'air 22 mm")
3. Pare-pluie (trait épais ondulé)
4. Isolant laine de bois (vagues régulières, 200 mm)
5. Ossature bois (rectangles, fil visible : anneaux)
6. Frein-vapeur (trait fin pointillé)
7. Vide technique (vide, légende "vide 50 mm")
8. Plaque de plâtre (hachures croisées fines)

Légende à reporter en marge.
```

## Notes pédagogiques

- Les conventions sont des **conventions** : elles varient selon les écoles et les pays. Vérifier l'usage avec tes enseignants.
- Une coupe technique bien hachurée se lit comme un livre : on comprend le projet sans qu'on parle.
- Quelques bonnes références : *Detail*, *AMC*, *Architecture d'Aujourd'hui* (cahier détails).

## Limites

- La norme NF EN ISO 128-50 n'est pas toujours scrupuleusement appliquée, surtout en pédagogie.
- En BIM (Archicad, Revit), les hachures sont paramétrables, à régler une fois pour toutes.
