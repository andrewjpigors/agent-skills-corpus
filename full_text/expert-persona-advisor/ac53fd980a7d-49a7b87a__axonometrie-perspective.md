---
name: axonometrie-perspective
description: Explique les types de projections (axonométrie, isométrie, perspective conique 1 et 2 points) et quand les utiliser. Déclenche sur axonométrie, axo, isométrie, perspective, point de fuite, projection, vue 3D, éclaté.
---

# `axonometrie-perspective` : projections et vues 3D

## Vue d'ensemble

Plan, coupe et élévation décrivent un objet mais ne le donnent pas à voir en volume. L'axonométrie et la perspective complètent.

## Axonométrie (vue parallèle)

### Définition
Projection sur un plan où les lignes parallèles dans la réalité restent parallèles sur le dessin (pas de point de fuite). Les **angles et longueurs** sont préservés ou déformés selon un coefficient.

### Variantes courantes

| Type | Angles des axes | Caractéristique |
|---|---|---|
| **Isométrique** | 30° / 30° / 90° vertical | Tous les axes au même rapport (1:1:1). Très utilisé en archi. |
| **Dimétrique** | 2 angles égaux | Compromis entre lisibilité et naturel. |
| **Cabinet** | Face frontale + profondeur à 45° avec rapport 1:2 | Privilégie une façade frontale. |
| **Militaire** | Plan au sol vrai, vertical réel | Le plan reste lisible "comme un plan". Utile pour urbanisme. |

### Usage
- **Représenter un projet** sans déformation perspective : on peut mesurer.
- **Éclaté** : décomposer un bâtiment en couches (structure / enveloppe / second oeuvre).
- **Vue militaire** très utilisée en urbanisme et grands ensembles : on lit le plan et le volume en même temps.

## Perspective conique (vraie perspective)

### Définition
Les lignes parallèles convergent vers un ou plusieurs **points de fuite** (PF). C'est la perspective de la photo, de l'oeil humain.

### Types

| Type | Points de fuite | Effet |
|---|---|---|
| **1 point** | 1 PF central | Vue frontale, intérieur d'une pièce, rue droite |
| **2 points** | 2 PF horizontaux | Vue de coin, façade vue d'angle |
| **3 points** | 2 PF horizontaux + 1 vertical | Vue plongeante ou contre-plongée, gratte-ciel |

### Ligne d'horizon et hauteur d'oeil
La **ligne d'horizon** est à hauteur d'oeil de l'observateur. Convention archi : **1,60 m** (hauteur d'oeil d'un adulte debout).

### Usage
- **Image d'ambiance** : montrer l'ambiance d'un espace.
- **Vue piéton** : à hauteur d'oeil pour donner l'expérience réelle.
- **Vue oiseau** : ligne d'horizon haute, pour expliquer une volumétrie globale.

## Quand utiliser quoi ?

- **Axonométrie isométrique** : représentation pédagogique, claire, mesurable. Le classique de l'analyse de référence.
- **Axonométrie militaire** : urbanisme, grand ensemble.
- **Éclaté axonométrique** : pédagogique pour montrer les couches d'un projet.
- **Perspective 1 point** : intérieur d'une pièce, rue. Simple à construire.
- **Perspective 2 points** : extérieur d'un bâtiment, vu d'angle. Plus naturelle.
- **Perspective 3 points** : effet dramatique, plongée ou contre-plongée. À utiliser avec parcimonie.

## Procédure

1. **Comprendre l'intention** : analyse pédagogique ou ambiance ?
2. **Recommander une projection** parmi les variantes.
3. **Expliquer la construction** brièvement (axes, points de fuite, ligne d'horizon).

## Notes pédagogiques

- Une **axo isométrique** est l'outil le plus utile en analyse de référence : elle donne l'air sérieux et reste mesurable.
- Une **bonne perspective** n'est pas une image photoréaliste, c'est une image qui transmet **une intention**.
- Avant de générer en 3D, faire un croquis à la main : on choisit son cadrage, son point de vue, on évite la perspective générée par défaut.

## Limites

- Les logiciels (Rhino, Archicad, SketchUp) génèrent ces projections automatiquement, mais comprendre leur construction reste essentiel.
- L'axonométrie déforme légèrement la perception (sphère = ellipse).
