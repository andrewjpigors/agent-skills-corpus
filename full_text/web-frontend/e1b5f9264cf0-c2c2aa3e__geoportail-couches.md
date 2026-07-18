---
name: geoportail-couches
description: Conseille les bonnes couches Géoportail à activer pour une analyse de site. Déclenche sur géoportail, couches, IGN, carte IGN, orthophoto, courbes de niveau, hydrographie, occupation du sol.
---

# `geoportail-couches` : choisir les bonnes couches IGN

## Vue d'ensemble

**Géoportail** (IGN) est l'outil cartographique de référence en France. Le plus puissant pour les étudiants en archi, et gratuit. Mais sa richesse intimide : plus de 1000 couches disponibles.

Ce skill conseille les couches les plus utiles selon ce qu'on cherche.

## Entrées attendues

- localisation (adresse ou commune),
- type d'analyse souhaité : relief, hydrographie, occupation du sol, patrimoine, transports, etc.

## Source

https://www.geoportail.gouv.fr/

## Couches recommandées par usage

### Voir le terrain tel qu'il est

- **Photographies aériennes** (orthophotos IGN) : voir le bâti, la végétation, l'usage des sols
- **Photographies aériennes 1950-1965** : voir comment c'était avant, super utile pour comprendre l'évolution d'un quartier
- **Carte IGN classique** : couche de référence pour comprendre la structure

### Comprendre le relief

- **Courbes de niveau** (équidistance 5 m, 10 m selon zone)
- **Estompage du relief**
- **Modèle Numérique de Terrain (MNT) ombré**

### Comprendre l'eau

- **Hydrographie** : cours d'eau, lacs
- **Zones humides probables**
- **PPRI** (zones inondables) : voir aussi skill `risques-naturels`

### Occupation du sol

- **Corine Land Cover** : usage du sol à grande échelle (urbain, agricole, forêt, eau)
- **OCS GE** (Occupation du Sol à Grande Échelle) : plus fin, disponible sur les régions couvertes
- **Registre Parcellaire Graphique** : usage agricole

### Patrimoine

- **Monuments historiques** : voir aussi skill `monuments-historiques`
- **Sites classés et inscrits**
- **AVAP, SPR** (sites patrimoniaux remarquables)

### Transports et mobilité

- **Réseau routier** (classement, sens)
- **Voies ferrées**
- **Pistes cyclables** (selon disponibilité régionale)

### Risques

- **Aléa retrait-gonflement des argiles**
- **Zones sismiques**
- voir aussi le skill `risques-naturels` pour Géorisques (plus complet)

## Procédure

1. **Comprendre ce que cherche l'utilisateur** (analyse complète ? juste le relief ?).
2. **Recommander 3 à 6 couches** selon le besoin, pas plus, sinon la carte devient illisible.
3. **Indiquer l'ordre d'empilement** (ortho en fond, vecteurs au-dessus).
4. **Fournir le lien Géoportail** déjà centré et zoomé si possible.

## Sortie attendue

```
Pour ton analyse de site à Roubaix, j'active dans cet ordre :
1. Photographies aériennes (fond)
2. Courbes de niveau (lisibilité du relief)
3. Hydrographie (rivière du Trichon en sous-sol)
4. Monuments historiques (école nationale des arts visuels classée)
5. Plan cadastral (pour les limites de parcelles)

Lien : https://www.geoportail.gouv.fr/carte?c=3.16,50.69&z=18
```

## Notes pédagogiques

- **Échelle pertinente** : pour une analyse de parcelle, viser le 1:1000 à 1:2000 sur l'écran.
- L'**ortho 1950** est un classique pour les jurys, elle montre l'évolution du tissu.
- Géoportail permet aussi des **profils altimétriques** (outil règle), très utile pour comprendre une pente.

## Limites

- Toutes les couches ne sont pas dispo partout en France (l'OCS GE par exemple).
- L'ortho la plus récente a souvent 2 à 3 ans de décalage.
