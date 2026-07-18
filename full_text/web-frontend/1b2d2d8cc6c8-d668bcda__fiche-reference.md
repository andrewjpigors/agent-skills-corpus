---
name: fiche-reference
description: Génère une fiche structurée d'un bâtiment de référence (analyse type ENSA L1). Déclenche sur fiche, référence, analyse de bâtiment, étude de cas, monographie.
---

# `fiche-reference` : fiche structurée d'un bâtiment

## Vue d'ensemble

Une fiche de référence est un exercice classique en école d'archi. Elle aide à comprendre un projet par l'analyse de ses caractéristiques principales.

Ce skill génère une fiche au format normalisé, prête à mettre en page.

## Entrées attendues

Au minimum : le **nom du bâtiment** ou **architecte + projet**. Exemples :
- "Villa Savoye"
- "Le Corbusier, couvent de la Tourette"
- "Maison à Bordeaux, Rem Koolhaas"

Optionnel : angle d'analyse demandé (structure, lumière, programme, contexte...).

## Structure de la fiche

1. **Identité**
   - nom du projet
   - architecte(s)
   - localisation
   - date de conception, date de livraison
   - maître d'ouvrage
   - programme
   - surface, hauteur, coût (si publics)

2. **Contexte**
   - site, ville, quartier
   - moment historique
   - contraintes (climat, terrain, réglementation)

3. **Parti pris**
   - intention principale de l'architecte
   - en 2-3 phrases

4. **Plan et organisation spatiale**
   - description du plan
   - hiérarchie des espaces
   - circulations

5. **Volumétrie et façades**
   - composition
   - rapport plein / vide
   - matériaux apparents

6. **Structure**
   - système porteur (poteaux, voiles, mur porteur, ossature bois...)
   - matériau principal
   - travée, trame

7. **Lumière et ambiances**
   - sources de lumière
   - orientations
   - matérialité intérieure

8. **Détails marquants**
   - 2-3 détails qui caractérisent le projet
   - innovation technique éventuelle

9. **Postérité, critique**
   - prix, reconnaissance
   - influence
   - critiques formulées

10. **Sources** (à citer obligatoirement)
    - monographies, revues, sites officiels

## Procédure

1. **Vérifier l'existence du bâtiment** (Wikipédia + recherche web).
2. **Croiser au moins 2 sources** pour les données factuelles (dates, surfaces).
3. **Remplir chaque section**, dire "non documenté" plutôt qu'inventer.
4. **Ajouter en fin une liste d'images de référence** à chercher (plan, coupe, façade, photo, axonométrie).

## Sortie attendue

Document Markdown structuré, prêt à être collé dans un traitement de texte ou mis en page sur InDesign.

## Notes pédagogiques

- Une fiche n'est pas une **fiche Wikipédia** : on cherche l'**intention**, pas seulement les faits.
- Un bon parti pris tient en une phrase.
- Une bonne fiche se relit, et on doit "voir" le bâtiment sans le connaître.

## Limites

- Pour les bâtiments très récents ou peu publiés, certaines sections resteront vides.
- Le skill ne génère pas les images, il indique lesquelles aller chercher.
