---
name: archicad-bases
description: Aide-mémoire des bases d'Archicad pour la modélisation BIM d'un projet d'architecture. Déclenche sur archicad, BIM, IFC, modèle paramétrique, dalle, mur, étage, calque archicad, cartouche archicad.
---

# `archicad-bases` : prise en main d'Archicad

## Vue d'ensemble

Archicad est un logiciel **BIM** (Building Information Modeling) édité par Graphisoft, très utilisé en France. On construit un **modèle 3D paramétrique** qui génère automatiquement plans, coupes, élévations.

## Différence avec AutoCAD

- AutoCAD : on dessine des **traits**. Une coupe est un nouveau dessin.
- Archicad : on construit un **bâtiment** (murs, dalles, toits, fenêtres). Toutes les vues sont des **extraits** du modèle, synchronisées.

## Outils principaux

### Modèle

- **Mur** : tracer un segment, le mur est un objet paramétrique (composition, hauteur, finition).
- **Dalle** : zone polygonale, épaisseur.
- **Poteau** : objet ponctuel.
- **Poutre** : segment.
- **Fenêtre / Porte** : posées sur un mur, paramétriques.
- **Escalier** : outil dédié, paramétrique.
- **Toit** : surface réglée, multi-pans possible.
- **Zone** : pièce, surface comptée automatiquement.

### Navigation

- **Étages** (Story) : on modélise étage par étage, élévations relatives.
- **Plan** : F2.
- **Coupe / Élévation** : créer un trait dans le modèle, Archicad génère la vue.
- **3D** : F3.
- **Détail** : zoom sur une partie pour la dessiner en plus grand.

## Calques et stylos

- **Calques** : organisation par usage. Plusieurs calques regroupés en "combinaisons" pour les vues (plan logement vs plan structure).
- **Stylos** : 1 à 255, chacun a une couleur et une épaisseur d'impression.

## Préférences à régler dès l'ouverture

- **Préférences du projet** -> unités en mm.
- **Préférences -> Cotation** -> mm pour les cotes (parfois cm en école française).
- **Vues enregistrées** : sauvegarder les vues clés (plan RDC, plan R+1, coupe AA, élévation sud).

## Mise en page (Layouts)

- **Carnet de calques** (book of layouts) : équivalent de l'espace papier d'AutoCAD.
- Insérer des vues dans une **planche A1** (format à créer).
- Échelle de chaque vue paramétrable.
- Cartouche : automatique, modifiable.

## Workflow type pour un projet L1

1. **Étages** : régler les altimétries des niveaux.
2. **Murs porteurs** au RDC, puis copier-coller aux étages.
3. **Dalles** à chaque niveau (faire les ouvertures pour escalier).
4. **Cloisons** intérieures.
5. **Ouvertures** (fenêtres, portes).
6. **Toit**.
7. **Escalier**.
8. **Zones** (pièces nommées, surfaces automatiques).
9. **Coupes et élévations** : tracer les traits de coupe.
10. **Mise en page** sur planches A1.
11. **PDF** d'export.

## Export

- **PDF** : Fichier -> Sauvegarder sous -> PDF. Choisir résolution et CTB.
- **DWG** : Fichier -> Sauvegarder sous -> DWG, pour échanger avec AutoCAD.
- **IFC** : norme BIM internationale, pour échanger avec Revit, Allplan.

## Procédure d'aide

1. **Identifier l'étape** où l'utilisateur bloque.
2. **Donner les clics ou les raccourcis** exacts.
3. **Renvoyer vers les tutos** Graphisoft Learn (https://learn.graphisoft.com/).

## Notes pédagogiques

- Archicad demande **plus de mise en place** au début qu'AutoCAD, mais paye ensuite : toute modification met à jour toutes les vues.
- **License étudiante gratuite** : disponible sur graphisoft.com avec adresse mail école.
- **Templates** : commencer avec le template français pour avoir les bonnes conventions.
- Garder les **murs composites** simples au début (1 ou 2 couches), pour ne pas se perdre.

## Limites

- Archicad est volumineux : ordinateur correct nécessaire (16 Go de RAM recommandés).
- Les rendus photoréalistes ne sont pas son fort, exporter vers Twinmotion ou Lumion pour ça.
