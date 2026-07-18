---
name: sketchup-bases
description: Aide-mémoire SketchUp pour la modélisation volumétrique rapide. Déclenche sur sketchup, modèle 3D rapide, volumétrie, push pull, groupe, composant, scène, sketchup web, layout.
---

# `sketchup-bases` : prise en main de SketchUp

## Vue d'ensemble

**SketchUp** est le logiciel 3D le plus simple à prendre en main. Travail en **polygones** (et non NURBS), idéal pour la **volumétrie rapide** et l'étude d'esquisse.

## Quand utiliser SketchUp

- Premier modèle volumétrique d'un projet.
- Étude de masse rapide.
- Maquette numérique pour étude solaire.
- Modélisation de mobilier, intérieur, présentation rapide.

## Versions

- **SketchUp Free** (web) : gratuit, fonctionne dans le navigateur.
- **SketchUp Pro** : payant, license étudiante disponible.

## Outils essentiels

| Outil | Raccourci | Effet |
|---|---|---|
| Sélection | `Espace` | Sélectionner |
| Ligne | `L` | Tracer un segment |
| Rectangle | `R` | Rectangle |
| Cercle | `C` | Cercle |
| Pousser/Tirer | `P` | Extruder une face |
| Décalage | `F` | Offset d'une face |
| Déplacer | `M` | Déplacer |
| Rotation | `Q` | Rotation |
| Échelle | `S` | Échelle |
| Suivez-moi | (rien) | Extruder le long d'un chemin |
| Mètre | `T` | Mesurer (et changer l'échelle) |
| Texte | (rien) | Annotation |

## Concepts fondamentaux

### Inférences

SketchUp **devine** où tu veux dessiner :
- **Vert, rouge, bleu** : axes X, Y, Z.
- **Magenta** : parallèle à une arête.
- **Cyan** : sur un plan de référence.
- **Point d'extrémité, milieu** : accrochages automatiques.

Forcer une direction : `Maj` enfoncé pendant le dessin.

### Groupes et composants

- **Groupe** : ensemble d'éléments figé. Évite que les arêtes se "soudent" entre elles.
- **Composant** : groupe **dupliqué** : modifier l'un modifie tous les autres. Utile pour les fenêtres, mobilier.
- **Règle d'or** : tout objet réel = un groupe ou un composant.

### Calques (Tags)

Comme dans AutoCAD ou Archicad : organiser les éléments. Convention :
- `00-contexte`
- `01-structure`
- `02-enveloppe`
- `03-ouvertures`
- `04-mobilier`

## Workflow type

1. **Régler les unités** : Fenêtre -> Préférences -> Unités, mètres ou millimètres.
2. **Importer le plan** d'arrière-plan (image ou DWG).
3. **Caler à l'échelle** avec l'outil Mètre : mesurer un segment connu, taper la longueur réelle, SketchUp redimensionne.
4. **Dessiner le contour** des murs au sol (rectangle ou ligne).
5. **Pousser/Tirer** pour faire monter les murs.
6. **Découper les ouvertures** (rectangle sur le mur, Pousser/Tirer vers l'intérieur).
7. **Étages** : groupes par niveau.
8. **Mobilier** : importer depuis 3D Warehouse (bibliothèque en ligne gratuite).
9. **Scènes** (Scenes) : enregistrer des vues (perspective, plan, axo) avec leurs réglages.
10. **Ombres** : Fenêtre -> Ombres, régler date et heure pour étude solaire.

## Exports

- **PNG, JPEG** : image (Fichier -> Exporter -> Image 2D).
- **DWG, DXF** : pour AutoCAD (Pro seulement).
- **STL** : impression 3D.

## Procédure d'aide

1. **Identifier l'étape** où l'utilisateur bloque.
2. **Donner l'outil** (raccourci).
3. **Donner les clics** dans l'ordre.

## Astuces

- **Touchez `Ctrl`** pendant le Pousser/Tirer pour créer une nouvelle face (utile pour décrocher une partie de toiture).
- **Touchez `Alt`** pour reproduire la dernière opération.
- **Triple-clic** : sélectionner tout un groupe connecté.
- **Sauvegarde** : `Ctrl+S` souvent. SketchUp ne sauvegarde pas automatiquement.

## Notes pédagogiques

- SketchUp est **trop simple** pour un grand projet en BIM (pas de paramétrage). Mais idéal pour comprendre la volumétrie en L1.
- Pour passer aux dessins 2D propres : **LayOut** (inclus dans Pro) ou export vers Illustrator/InDesign.
- **3D Warehouse** : bibliothèque gratuite de modèles. Utile pour le mobilier, attention à la qualité.

## Limites

- Pas adapté pour les **surfaces complexes** (préférer Rhino).
- Le **rendu réaliste** demande des plug-ins (V-Ray, Enscape, Twinmotion).
- L'export DWG/DXF n'est pas dispo en version web gratuite.
