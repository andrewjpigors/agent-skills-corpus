---
name: plu-urbanisme
description: Aide à trouver, lire et interpréter le PLU ou PLUi d'une commune française. Déclenche sur les mots PLU, PLUi, urbanisme, règlement, zonage, zone U, zone N, zone A, zone AU, Géoportail urbanisme, certificat d'urbanisme, droit à construire.
---

# `plu-urbanisme` : lire un Plan Local d'Urbanisme

## Vue d'ensemble

Le **PLU** (Plan Local d'Urbanisme) ou **PLUi** (intercommunal) est le document qui dit ce qu'on a le droit de construire sur un terrain en France. Pour la métropole lilloise (ENSAPL), c'est un **PLU2 de la MEL** (Métropole Européenne de Lille).

Ce skill aide à :
- localiser le PLU d'une commune,
- comprendre la zone d'une parcelle (U, AU, A, N),
- lire les règles principales (hauteur, emprise, recul, stationnement),
- repérer les servitudes et OAP.

## Entrées attendues

L'utilisateur fournit au moins un des éléments suivants :
- adresse précise ("12 rue de Paris, Lille"),
- nom de commune,
- numéro de parcelle cadastrale.

Si l'info manque, demander.

## Sources officielles

- **Géoportail de l'Urbanisme** : https://www.geoportail-urbanisme.gouv.fr/
  source nationale, contient la majorité des PLU numérisés
- **Site de la commune ou de l'intercommunalité** : pour les annexes graphiques de qualité
- Pour la MEL : https://www.lillemetropole.fr/votre-metropole/competences/urbanisme/plu

## Procédure

1. **Géolocaliser** : trouver la commune à partir de l'adresse.
2. **Ouvrir le Géoportail de l'Urbanisme** sur cette commune (vérifier la date d'opposabilité du document).
3. **Identifier la zone** où se trouve la parcelle, codes courants :
   - `U` : urbaine, constructible
   - `AU` : à urbaniser
   - `A` : agricole, très restrictif
   - `N` : naturelle, très restrictif
   - sous-zones : `UA`, `UB`, `UC`... avec des règles différentes
4. **Lire le règlement** de la zone, en cherchant :
   - destinations autorisées et interdites
   - hauteur maximale
   - emprise au sol
   - recul par rapport aux voies et limites séparatives
   - stationnement
   - aspect extérieur
5. **Vérifier les servitudes** (SUP) : monuments historiques, PPRI, lignes électriques, etc.
6. **Repérer les OAP** (Orientations d'Aménagement et de Programmation) si la parcelle est dans un secteur d'OAP.

## Sortie attendue

Tableau de synthèse :

| Élément | Valeur |
|---|---|
| Commune | Lille |
| Document | PLU2 MEL, approuvé 12/12/2019 |
| Zone | UA1 |
| Destinations autorisées | habitation, commerce, bureaux |
| Hauteur maximale | 18 m à l'égout |
| Emprise au sol | 70 % |
| Recul | alignement obligatoire sur voie |
| Stationnement | 1 place par logement, vélo obligatoire |
| Servitudes | périmètre MH (église Saint-Maurice) |
| OAP | non |

Puis un paragraphe en français clair "ce que ça veut dire pour ton projet".

## Notes pédagogiques

À expliquer en passant si pertinent :
- différence entre PLU et POS (POS = ancien document, abrogé)
- ce qu'est un **CU** (certificat d'urbanisme) et quand il est utile
- pourquoi on parle de **co-visibilité** près d'un monument historique
- les **OAP** sont opposables, pas seulement indicatives

## Limites

- Le PLU change. Toujours vérifier la date d'opposabilité sur Géoportail Urbanisme.
- Pour un projet réel, le PLU ne suffit pas : il faut aussi le RNU, le Code de l'urbanisme, parfois un règlement de lotissement.
- Le skill aide à comprendre, il ne remplace pas un avis juridique.
