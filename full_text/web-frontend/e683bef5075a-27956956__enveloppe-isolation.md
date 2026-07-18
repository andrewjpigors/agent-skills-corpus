---
name: enveloppe-isolation
description: Bases sur l'enveloppe thermique d'un bâtiment, RE2020, isolation, ITE / ITI, pare-vapeur, ponts thermiques. Déclenche sur enveloppe, isolation, ITE, ITI, RE2020, RT2012, thermique, pont thermique, étanchéité à l'air.
---

# `enveloppe-isolation` : bases thermiques et enveloppe

## Vue d'ensemble

L'enveloppe thermique sépare l'intérieur chauffé de l'extérieur. Bien la concevoir réduit fortement les consommations.

## Concepts clés

### Conductivité thermique λ (lambda)
Capacité d'un matériau à conduire la chaleur. Unité : W/m·K.
- Plus c'est faible, mieux ça isole.
- Air immobile : 0,025
- Laine minérale, biosourcés : 0,032 à 0,040
- Bois : 0,12 à 0,15
- Béton : 1,5 à 2
- Métal : 50 à 400

### Résistance thermique R
Résistance d'une couche à laisser passer la chaleur. R = épaisseur (m) / λ. Unité : m²·K/W.
- Pour une bonne isolation logement RE2020 : R total mur ~5, R toiture ~8.

### Coefficient U
Inverse de la résistance totale, exprime la perte thermique. Unité : W/m²·K.
- Plus c'est faible, mieux ça isole.
- Mur isolé performant : U ≤ 0,2 W/m²·K
- Fenêtre double vitrage : U ~1,4 W/m²·K
- Fenêtre triple vitrage : U ~0,8 W/m²·K

### Étanchéité à l'air
Une enveloppe peut être isolée mais "fuyarde". Test du **blower door** mesure les infiltrations. Une bonne enveloppe a un n50 ≤ 0,6 vol/h (passivhaus).

### Pont thermique
Endroit où l'isolation est interrompue (jonction dalle/façade, encadrement de baie, balcon traversant). Source de pertes et de condensation.

## Isolation par l'extérieur (ITE)

- Isolant placé **sur l'extérieur** du mur porteur.
- Avantages : pas de pont thermique au plancher, inertie du mur conservée.
- Limites : modifie l'aspect (sauf bardage), épaisseur extérieure.
- **ITE bardée** : bardage bois, métal, terre cuite, etc.
- **ITE enduite** : enduit sur isolant.

## Isolation par l'intérieur (ITI)

- Isolant placé **côté intérieur** du mur porteur.
- Avantages : ne modifie pas la façade (utile en SPR, monuments historiques).
- Limites : ponts thermiques aux planchers, mur extérieur reste froid (condensation possible).

## Isolation en âme (sandwich)

- Mur double avec isolant au milieu (mur creux).
- Tradition de la brique en Belgique et Pays-Bas, courant en France pour ossature bois.

## RE2020 (Réglementation Environnementale)

Depuis 2022, remplace la RT2012. Exigences principales :
- **Bbio** : besoin bioclimatique (compacité, orientation, surface vitrée).
- **Cep** : consommation primaire (chauffage, ECS, ventilation, éclairage, climatisation, mobilier).
- **DH** : confort d'été (degrés-heures d'inconfort).
- **Carbone** : indicateurs IC énergie et IC construction (cycle de vie).
- **Bois** et **biosourcés** encouragés par les seuils carbone.

## Procédure

1. **Identifier la question** : choix ITE vs ITI ? épaisseur d'isolant ? RE2020 ?
2. **Expliquer le principe**.
3. **Donner les ordres de grandeur** (R, U, épaisseurs).
4. **Recommander** selon le contexte.

## Sortie attendue

```
Tu veux isoler un mur béton de 20 cm en logement neuf, climat lillois ?

Options
- ITE laine de bois 200 mm sous bardage ventilé : R = 5,3
- ITE laine de roche 180 mm sous enduit : R = 5,1
- ITI laine de verre 140 mm + plaque de plâtre : R = 4,0

Recommandation RE2020 : ITE biosourcée pour le bénéfice carbone.

Détails à soigner
- pont thermique nez de dalle : rupteur ou ITE qui descend en pied
- linteaux de baies : isolant en retour
- pose tellement importante que le choix d'isolant
```

## Notes pédagogiques

- En L1, retenir les **ordres de grandeur** plutôt que les chiffres exacts.
- L'**inertie** est aussi importante que l'isolation : un mur en pierre absorbe la chaleur le jour, la restitue la nuit (confort d'été).
- Un bon dessin de **coupe technique** identifie chaque couche : ossature, isolant, pare-pluie, frein-vapeur, plaque de finition.

## Limites

- Le calcul réglementaire RE2020 demande un logiciel agréé (Pleiades, Climawin, etc.).
- Le skill ne fait pas de bilan thermique, il pose les concepts.
