---
name: autocad-bases
description: Aide-mémoire des commandes AutoCAD essentielles pour faire un plan, une coupe ou une élévation 2D. Déclenche sur autocad, DAO, dessin 2D, ligne, polyligne, calque, layer, hachure, cotation, espace papier.
---

# `autocad-bases` : prise en main d'AutoCAD

## Vue d'ensemble

AutoCAD est le standard de la DAO 2D depuis les années 80. Toujours utilisé en école pour le dessin précis. Toutes les commandes se tapent au clavier (raccourci à 1 ou 2 lettres).

## Configurer son espace de travail

- **Limites** : `LIMITS` pour définir l'étendue (utile en travers de mise en page).
- **Unités** : `UNITS` pour passer en millimètres (recommandé en archi française).
- **Calques** : `LA` pour ouvrir le gestionnaire. Convention :
  - `00-CONTEXTE` (existant, voisinage)
  - `01-STRUCTURE` (murs porteurs, poteaux)
  - `02-CLOISONS`
  - `03-MENUISERIES`
  - `04-MOBILIER`
  - `05-COTES`
  - `06-TEXTE`
  - `07-HACHURES`
  - `08-CONSTRUCTION` (lignes de construction, à masquer au rendu)

Chaque calque a une **couleur** (1 à 255) qui détermine son épaisseur d'impression via le **CTB** (Color Table).

## Commandes essentielles

### Dessin

| Raccourci | Commande | Usage |
|---|---|---|
| `L` | LIGNE | Tracer un segment |
| `PL` | POLYLIGNE | Ligne continue (mieux que LIGNE pour les contours) |
| `REC` | RECTANGLE | Rectangle par 2 points |
| `C` | CERCLE | Cercle |
| `A` | ARC | Arc de cercle |
| `H` | HACHURE | Remplissage |
| `T` | TEXTEMULT | Texte multiligne |
| `DLI` | COTLIN | Cote linéaire |

### Modification

| Raccourci | Commande | Usage |
|---|---|---|
| `E` | EFFACER | Supprimer |
| `M` | DEPLACER | Déplacer |
| `CO` | COPIER | Copier |
| `RO` | ROTATION | Rotation |
| `SC` | ECHELLE | Échelle |
| `TR` | AJUSTER | Couper à une limite |
| `EX` | PROLONGER | Prolonger à une limite |
| `O` | DECALER | Offset (parallèle) |
| `F` | RACCORD | Raccord (arrondi) |
| `MI` | MIROIR | Symétrie |
| `AR` | RESEAU | Réseau (matrice) |

### Saisie précise

- **Coordonnées absolues** : `0,0` puis `Entrée`.
- **Coordonnées relatives** : `@1000,0` (1 m à droite).
- **Coordonnées polaires** : `@3000<45` (3 m à 45°).
- **Saisie dynamique** : taper directement la longueur en tirant la ligne.
- **OSNAP** (accrochage objet) : extrémité, milieu, intersection, perpendiculaire, parallèle... Toujours activé.
- **ORTHO** (F8) : contraint à l'horizontale ou la verticale.
- **POLAR** (F10) : accroche à des angles précis (15°, 30°, 45°).

## Espace objet et espace papier

AutoCAD a deux modes :
- **Objet (Model Space)** : tu dessines à l'échelle 1:1 (un mur de 5 m fait 5000 mm).
- **Papier (Paper Space)** : tu mets en page sur une feuille. Chaque vue (fenêtre) a une **échelle** (1/100, 1/50...).

Workflow recommandé :
1. Dessiner dans l'espace objet à l'échelle 1:1, en mm.
2. Aller dans l'espace papier, créer un format A1.
3. Insérer des **fenêtres** sur le dessin, régler l'échelle (commande `Z` puis `1/100xp`).
4. Ajouter cartouche, légendes, cotes hors fenêtre.

## Cotations

- `DLI` : cote linéaire.
- `DAL` : cote alignée.
- `DCO` : cote continue.
- **Style de cote** : `D`, créer un style "100" (échelle 100 = facteur 100), "50", etc.

## Impression / export

- `CTRL+P` ouvre la boîte d'impression.
- Choisir l'imprimante (ou `DWG to PDF`).
- Format de papier (A1).
- Aire à imprimer : "fenêtre" pour choisir un cadre, ou "agencement" pour l'espace papier.
- **CTB** (color table) pour les épaisseurs.
- Cocher "Mettre à l'échelle linéique".

## Procédure d'aide

1. **Comprendre la difficulté** : commande qui ne marche pas, mise en page, calques ?
2. **Donner la commande exacte**.
3. **Expliquer le raccourci**.
4. **Donner un exemple chiffré**.

## Notes pédagogiques

- L'**OSNAP** est la base. Sans accrochage, le dessin est faux à 1 mm près partout.
- Toujours **dessiner à l'échelle 1:1** dans l'espace objet. L'échelle se règle à l'impression.
- Les **calques** sont l'organisation du dessin. Une fois bien faits, tout est plus facile.
- **Sauvegarde** : `CTRL+S` souvent. AutoCAD plante parfois.

## Limites

- AutoCAD ne fait pas du BIM (pas de modèle paramétrique). Pour du BIM, voir Archicad ou Revit.
- L'interface évolue souvent ; les raccourcis restent stables.
