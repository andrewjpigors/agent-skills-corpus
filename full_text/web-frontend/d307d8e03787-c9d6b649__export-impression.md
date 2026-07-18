---
name: export-impression
description: Préparer un fichier pour l'impression d'une planche A1 ou A0 (PDF, traceur, résolution, fond perdu). Déclenche sur impression, plotter, traceur, PDF, A0, A1, DPI, résolution, fond perdu, marges, repro.
---

# `export-impression` : préparer un fichier pour l'impression

## Vue d'ensemble

Une planche bien faite à l'écran peut s'imprimer mal : couleurs ternes, traits invisibles, échelles fausses. Ce skill évite les pièges.

## Formats pour l'impression

- **PDF (vectoriel)** : à privilégier. Les traits restent nets à toute taille.
- **JPEG, PNG** : seulement si la planche contient beaucoup d'images ou de rendus.
- **TIFF haute résolution** : pour la photo, peu utile en archi étudiante.

## Résolution

- **Vectoriel** (PDF, AI) : pas de résolution, le trait reste net.
- **Image (raster)** : pour une impression A1 lue à 50 cm, viser **150 dpi**. Pour une lecture rapprochée, **300 dpi**.

Conversion : un A1 (594 × 841 mm) à 150 dpi = 3508 × 4965 pixels.

## Couleurs

- **RGB** : couleurs écran (rouge, vert, bleu). Gamme large, mais l'imprimante ne peut pas tout reproduire.
- **CMJN (CMYK)** : couleurs imprimerie (cyan, magenta, jaune, noir). Pour un rendu fidèle, **convertir en CMJN avant impression** ou demander une simulation à l'imprimeur.
- **Noir** : en CMJN, le "noir 100% noir uniquement" (K=100) est plus fin et net que le "noir riche" (C+M+J+K).

## Épaisseurs de trait

- **Plus petite épaisseur imprimable** : 0,1 mm (en pratique, viser 0,15 mm).
- En CTB AutoCAD ou en stylo Archicad, vérifier que les traits "fins" ne sont pas en dessous de 0,1 mm.
- Pour une planche A1, recommandation :
  - trait fin : 0,18 mm
  - trait moyen : 0,35 mm
  - trait épais : 0,7 mm
  - trait très épais (silhouette extérieure) : 1 mm ou plus

## Marges et fond perdu

- **Fond perdu** (5 mm autour) : si la planche a un fond coloré qui doit aller jusqu'au bord, le prolonger de 5 mm au-delà du format final.
- **Marges de sécurité** (5 mm à l'intérieur) : ne rien mettre d'important dans les 5 mm extérieurs (risque d'être rogné).
- **Marges techniques** du traceur : variable selon machine, généralement 5 à 10 mm de chaque côté impossibles à imprimer.

## PDF

### Depuis AutoCAD

1. `CTRL+P`.
2. Imprimante : `DWG To PDF.pc3`.
3. Format papier : ISO A1.
4. Aire : Agencement (espace papier) ou Fenêtre.
5. CTB : associé aux couleurs et épaisseurs.
6. Cocher "Mettre à l'échelle linéique" = 1:1.

### Depuis Archicad

1. Fichier -> Sauvegarder sous -> PDF.
2. Sélectionner la mise en page (Layout).
3. Cocher haute qualité, hachures vectorielles.

### Depuis Illustrator / InDesign

1. Fichier -> Exporter / Sauvegarder sous PDF.
2. Preset "Impression haute qualité".
3. Cocher fond perdu (5 mm) si nécessaire.
4. Activer les "repères de coupe" si l'imprimeur va rogner.

## Impression A1 / A0

### En école d'archi

Traceurs HP DesignJet (ou équivalents). Choses à vérifier :
- format papier réglé en A1 ou A0 (selon imprimante).
- orientation (paysage souvent par défaut en A1 archi).
- échelle (1:1 dans le PDF, déjà mis à l'échelle).
- couleurs (CMJN).
- coût : se renseigner sur le tarif à la planche (généralement 3 à 8 € l'A1).

### Chez un imprimeur

- Apporter un **PDF aplati** (toutes les transparences fusionnées).
- Préciser le grammage du papier (90 g/m² standard, 200 g/m² pour rendu rigide).
- Mat ou brillant : **mat** quasi toujours préférable pour l'archi (pas de reflets).

## Astuces

- **Imprimer un test A4** avant l'A1 : vérifier les couleurs, les épaisseurs, l'échelle.
- Garder une **version "écran"** (RGB) et une **version "impression"** (CMJN) du fichier.
- **Ne pas faire un assemblage de PDF** : exporter directement à la bonne taille.
- Pour les **dessins à la main scannés**, viser 600 dpi en niveau de gris.

## Procédure d'aide

1. **Identifier le logiciel source** et le format de sortie demandé.
2. **Donner les réglages** précis.
3. **Anticiper les pièges** (mode couleur, épaisseur min, marges).

## Notes pédagogiques

- Une **bonne impression vaut le rendu** : un projet brillant peut être ruiné par une impression médiocre.
- **Vérifier sur papier**, pas seulement sur écran.

## Limites

- Les traceurs varient : se renseigner sur ceux de l'école.
- Les couleurs peuvent dériver, demander une calibration ou faire un test.
