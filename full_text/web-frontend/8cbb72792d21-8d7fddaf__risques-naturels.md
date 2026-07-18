---
name: risques-naturels
description: Liste les risques naturels et technologiques connus sur un site français (Géorisques). Déclenche sur risque, inondation, PPRI, PPRT, sismicité, retrait gonflement argile, mouvement de terrain, radon, géorisques.
---

# `risques-naturels` : risques connus sur un site

## Vue d'ensemble

Avant de concevoir, on doit savoir si le site est exposé à un risque : inondation, mouvement de terrain, sismicité, argiles, retrait, radon, industries proches. Ces risques influencent les fondations, les niveaux, l'implantation.

## Entrées attendues

- adresse précise du site.

## Sources officielles

- **Géorisques** : https://www.georisques.gouv.fr/
  portail officiel, contient l'**État des Risques** (ERP) téléchargeable en PDF gratuit
- **Géoportail** couches risques
- Plans de prévention spécifiques :
  - **PPRI** (inondation)
  - **PPRT** (technologique)
  - **PPRN** (naturel)

## Procédure

1. **Lancer une recherche Géorisques** sur l'adresse, télécharger l'État des Risques (PDF officiel).
2. **Lister les risques actifs**, par catégorie :
   - inondation, submersion marine
   - mouvements de terrain, cavités, retrait-gonflement des argiles
   - sismicité (zone 1 à 5)
   - radon (potentiel 1, 2 ou 3)
   - feu de forêt
   - risques industriels (PPRT, Seveso)
   - sols pollués (BASOL, BASIAS)
3. **Indiquer les implications constructives** :
   - inondable -> rez-de-chaussée surélevé, pas de pièce à vivre en sous-sol, planchers techniques aérés
   - argiles -> fondations adaptées, joints, drainage
   - radon -> ventilation soignée, étanchéité du soubassement
   - sismicité -> règles parasismiques selon zone

## Sortie attendue

```
Site : 12 rue de la Marque, Villeneuve d'Ascq

Risques actifs :
  - Inondation : oui, zone bleue PPRI Marque
    -> RDC surélevé d'au moins 0,50 m / TN
  - Retrait-gonflement argiles : aléa moyen
    -> fondations adaptées (étude G2 recommandée)
  - Sismicité : zone 2 (faible)
  - Radon : potentiel 1 (faible)
  - Cavités : aucune connue
  - Industriels : non concerné
  - Pollution sols : BASIAS à 200 m (ancienne station-service)

État des Risques officiel : georisques.gouv.fr/.../ERP_xxxxx.pdf
```

## Notes pédagogiques

- L'**ERP** (État des Risques) est obligatoire pour la vente et la location. C'est un document standard, gratuit, fiable.
- **Aléa** = probabilité de survenue. **Enjeu** = ce qui est exposé. **Risque** = aléa × enjeu.
- Une **zone rouge** d'un PPRI interdit en général toute construction nouvelle.
- Le risque **radon** vient des sols granitiques (zones de potentiel 3 : Bretagne, Massif Central, Vosges, Corse).

## Limites

- Le skill ne remplace pas une étude géotechnique (G1, G2) à faire pour un vrai projet.
- Les risques émergents (canicule, recul du trait de côte) ne sont pas toujours cartographiés.
