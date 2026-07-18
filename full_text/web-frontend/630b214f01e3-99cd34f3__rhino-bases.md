---
name: rhino-bases
description: Aide-mémoire des bases de Rhinoceros 3D pour la modélisation libre. Déclenche sur rhino, rhinoceros, NURBS, modélisation 3D libre, surface complexe, grasshopper.
---

# `rhino-bases` : prise en main de Rhinoceros 3D

## Vue d'ensemble

**Rhino** (édité par McNeel) est l'outil de modélisation 3D **libre** par excellence. Idéal pour les formes complexes, les surfaces (NURBS), les courbes. Souvent associé à **Grasshopper** pour la modélisation paramétrique.

## Quand utiliser Rhino

- Volumes complexes, formes courbes.
- Modélisation analytique d'un bâtiment existant.
- Préparation à la **découpe laser** (export .dxf 2D).
- Préparation à l'**impression 3D** (export .stl).
- Préparation à la **fabrication numérique** (CNC).

## Concepts

### Univers 3D

- **3 vues orthographiques** : Top, Front, Right.
- **1 vue Perspective**.
- **Axes** : X (rouge), Y (vert), Z (bleu).
- **CPlan** (Construction Plane) : plan de référence pour les opérations courantes.

### NURBS et polygones

- Rhino travaille en **NURBS** : surfaces lisses définies mathématiquement.
- À la fin, on peut exporter en **maillage** (mesh) pour SketchUp, Blender, impression 3D.

## Commandes essentielles

### Création

| Commande | Effet |
|---|---|
| `Line` | Ligne |
| `Curve` | Courbe libre |
| `Rectangle` | Rectangle |
| `Circle` | Cercle |
| `Polyline` | Polyligne |
| `Box` | Boîte 3D |
| `ExtrudeCrv` | Extruder une courbe en surface |
| `ExtrudeSrf` | Extruder une surface en volume |
| `Loft` | Surface entre plusieurs courbes |
| `Sweep1`, `Sweep2` | Surface balayée |
| `Revolve` | Révolution |

### Modification

| Commande | Effet |
|---|---|
| `Move` | Déplacer |
| `Copy` | Copier |
| `Rotate` | Rotation |
| `Scale` | Échelle |
| `Mirror` | Miroir |
| `Trim` | Couper |
| `Split` | Diviser |
| `BooleanUnion`, `BooleanDifference`, `BooleanIntersection` | Opérations booléennes |
| `Offset` | Parallèle (2D) |
| `OffsetSrf` | Décaler une surface |
| `Cap` | Fermer une surface ouverte |

### Sélection

- **Calques** : panneau de droite, organiser comme en AutoCAD.
- **SelLayer** : sélectionner tout sur un calque.
- **SelDup** : sélectionner les doublons.

## Astuces

- **Verrouiller un calque** pour ne pas le modifier sans le voir.
- **Hide / Show** (`HH`, `SH`) pour cacher temporairement.
- **Make2D** : génère un dessin 2D vectoriel à partir d'une vue 3D. Très utilisé pour produire un plan, une coupe ou une axonométrie depuis le modèle 3D.

## Grasshopper

**Grasshopper** est un **éditeur visuel** intégré à Rhino. Permet de créer des modèles paramétriques en branchant des "boîtes" entre elles. Utile pour :
- répétitions complexes (façades à pattern)
- optimisation
- formes générées par algorithme

À voir en L2/L3 plutôt qu'en L1.

## Workflow type pour analyser une référence

1. **Importer** le plan (image, DWG, scan) sur un calque dédié.
2. **Caler à l'échelle** (commande `Scale1D` ou `Scale`).
3. **Modéliser les volumes** à partir du plan (Box, ExtrudeCrv).
4. **Vues** : créer plusieurs vues (perspective, axonométrie, coupe).
5. **Make2D** pour produire les dessins 2D exportables vers Illustrator ou InDesign.

## Export

- **DWG** : pour AutoCAD, ne garde que la 2D.
- **3DM** : format natif.
- **OBJ, FBX, IGES** : autres logiciels 3D.
- **STL** : impression 3D.
- **PDF** : depuis Print.

## Procédure d'aide

1. **Identifier l'objectif** : analyse de référence, projet libre, fabrication ?
2. **Donner les commandes** précises.
3. **Renvoyer aux tutos** McNeel ou aux chaînes YouTube spécialisées.

## Notes pédagogiques

- Rhino a une **license étudiante** très accessible (~200 €`an` ou gratuite selon école).
- L'apprentissage est progressif : maîtriser la 2D et les opérations booléennes avant le Loft.
- Pour les **maquettes découpées au laser**, Rhino est l'outil de référence en école : aplatir les pièces (Unroll) puis exporter en DXF.

## Limites

- Rhino n'est pas BIM : pas de calcul de surfaces réglementaires, pas de paramétrage de mur composite.
- Le rendu nécessite un plug-in (V-Ray, Enscape) ou un logiciel externe.
