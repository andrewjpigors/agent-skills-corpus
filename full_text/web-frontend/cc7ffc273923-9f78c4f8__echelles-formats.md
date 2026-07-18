---
name: echelles-formats
description: Conseille la bonne échelle de dessin et le bon format papier selon le type de représentation. Déclenche sur échelle, 1/100, 1/50, 1/200, 1/20, format papier, A0, A1, A2, A3, A4, norme NF.
---

# `echelles-formats` : échelles et formats papier

## Vue d'ensemble

Choisir une échelle et un format adaptés est la première décision graphique d'un projet. Trop petit = illisible. Trop grand = vide ou détaillé en excès.

## Échelles usuelles en architecture

| Échelle | Usage typique |
|---|---|
| 1/5000, 1/2000 | Plan de situation, contexte urbain large |
| 1/1000, 1/500 | Plan masse, quartier |
| 1/200 | Plan masse rapproché, grand bâtiment |
| 1/100 | Plan, coupe, élévation **standard** pour un bâtiment |
| 1/50 | Plan, coupe détaillés (logement, intérieur) |
| 1/20 | Détail constructif courant |
| 1/10, 1/5 | Détail technique précis (assemblage menuiserie) |
| 1/2, 1/1 | Détail à grandeur réelle (profil de cadre) |

### Règle pratique

- Pour un rendu de bâtiment : **1/200 pour le plan masse, 1/100 pour les plans/coupes, 1/50 pour un détail logement, 1/20 pour un détail constructif**.
- L'échelle doit être **lisible** : à 1/200, on ne dessine pas les joints entre carreaux.

## Formats papier (norme ISO 216, série A)

| Format | Dimensions (mm) | Usage typique |
|---|---|---|
| A4 | 210 × 297 | Croquis, notes, fiche |
| A3 | 297 × 420 | Croquis large, rapport |
| A2 | 420 × 594 | Petit projet, planche d'analyse |
| A1 | 594 × 841 | **Planche standard L1** |
| A0 | 841 × 1189 | Grande planche, rendu final |

Chaque format est le double du précédent (en surface).

### Orientation

- **Portrait** : hauteur > largeur (typique A4 texte)
- **Paysage** : largeur > hauteur (typique pour planches d'archi)

En architecture, l'A1 est presque toujours en **paysage** pour les planches de rendu.

## Norme NF EN ISO 5457

Définit les marges, le cartouche, le repère de pliage. À retenir :
- marge gauche : 20 mm (pour reliure)
- autres marges : 10 mm
- cartouche en bas à droite, normalisé

Voir aussi le skill `cartouche-planche`.

## Procédure

1. **Comprendre la demande** (que veut représenter l'utilisateur ?).
2. **Recommander une échelle** et le format papier qui va avec.
3. **Vérifier la cohérence** : un plan d'un bâtiment de 50 × 30 m au 1/50 = 1 m × 0,60 m sur la planche, donc A1 minimum.

## Sortie attendue

```
Tu veux représenter ton bâtiment de 30 m × 20 m sur 3 niveaux ?

Recommandation :
- plan masse : 1/500 sur A3 ou en cartouche
- plans, coupes, élévations : 1/100 sur A1 paysage
  -> chaque dessin fait 30 cm × 20 cm, on peut en mettre plusieurs par planche
- détail logement : 1/50 sur A2 ou A1
- détail constructif (acrotère, menuiserie) : 1/20 sur A3

Marges et cartouche selon NF EN ISO 5457.
```

## Notes pédagogiques

- L'**échelle graphique** (barre dessinée) est obligatoire : si la planche est réduite à la photocopie, le 1/100 indiqué devient faux mais la barre reste juste.
- Toujours indiquer l'**orientation Nord** sur un plan masse.
- Une planche bien composée a un **rythme** : pas tout au centre, pas tout collé.

## Limites

- Le skill ne fait pas la mise en page (voir `mise-en-page-planche`).
- Les normes NF varient pour certains documents officiels (permis de construire).
