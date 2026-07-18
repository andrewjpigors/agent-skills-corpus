---
name: monuments-historiques
description: Vérifie si un site est protégé au titre des monuments historiques, ou s'il est dans le périmètre de 500 m autour d'un MH. Déclenche sur monument historique, MH, base Mérimée, classé, inscrit, ABF, abords MH, périmètre de protection, site patrimonial.
---

# `monuments-historiques` : protection patrimoniale d'un site

## Vue d'ensemble

En France, un projet à proximité d'un **monument historique** ou dans un **site patrimonial remarquable** (SPR) déclenche des obligations supplémentaires : avis de l'**Architecte des Bâtiments de France** (ABF), règles spécifiques, parfois interdiction de modifier l'aspect extérieur.

Ce skill aide à vérifier le statut patrimonial d'un site.

## Entrées attendues

- adresse précise du site,
- ou nom d'un bâtiment à vérifier.

## Sources officielles

- **Base Mérimée** (patrimoine architectural) : https://www.pop.culture.gouv.fr/search/mosaic?base=%5B%22Patrimoine%20architectural%20%28M%C3%A9rimée%29%22%5D
- **POP** (Plateforme Ouverte du Patrimoine) : https://www.pop.culture.gouv.fr/
- **Atlas des patrimoines** : https://atlas.patrimoines.culture.fr/
- **Géoportail** couche Monuments Historiques

## Procédure

1. **Vérifier le bâtiment lui-même** sur la base Mérimée : est-il classé, inscrit, ou non protégé ?
2. **Chercher les MH dans un rayon de 500 m** : tout MH génère un périmètre de protection des abords par défaut.
3. **Vérifier s'il y a un PDA** (Périmètre Délimité des Abords) qui remplace le périmètre par défaut, ou un SPR (Site Patrimonial Remarquable).
4. **Identifier les obligations** :
   - **Co-visibilité** : le projet est-il visible en même temps que le MH ? Si oui, avis conforme de l'ABF.
   - **Site Patrimonial Remarquable** : règles spécifiques (PVAP ou PSMV).
5. **Récupérer la fiche Mérimée** des MH concernés (numéro PA, date de protection, descriptif).

## Sortie attendue

```
Site : 5 rue de Béthune, Lille
Statut du bâtiment : non protégé
MH dans un rayon de 500 m :
  - Beffroi de Lille (classé MH, PA59000079, classement 2005)
    distance : 280 m
    en co-visibilité : oui (vue dégagée par la place Rihour)
  - Église Saint-Maurice (classée MH, PA00107740, 1840)
    distance : 410 m
    en co-visibilité : à vérifier sur site

Statut SPR : Lille a un SPR (anciennement ZPPAUP) qui couvre tout le centre.
Obligations : avis conforme de l'ABF pour toute autorisation d'urbanisme.
Contact : UDAP Nord (Lille).
```

## Notes pédagogiques

- **Classé** : niveau de protection maximal.
- **Inscrit** : protection moindre mais réelle.
- Le **périmètre de 500 m** date d'une loi de 1943. La loi LCAP de 2016 a créé les **PDA** (périmètres adaptés) qui remplacent souvent le rayon de 500 m.
- **ABF** = Architecte des Bâtiments de France, en France métropolitaine il y en a un par département (UDAP).
- L'avis ABF peut être **conforme** (obligatoire à suivre) ou **simple** (consultatif).

## Limites

- Tous les SPR ne sont pas encore numérisés ni à jour sur Géoportail.
- L'avis ABF est imprévisible : le skill ne peut pas le simuler, juste signaler qu'il sera requis.
