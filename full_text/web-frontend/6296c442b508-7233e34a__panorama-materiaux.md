---
name: panorama-materiaux
description: Panorama des matériaux de construction courants en France, avec usages, qualités, limites. Déclenche sur matériau, brique, béton, bois, acier, pierre, terre crue, biosourcé, paille, chanvre, choix matériaux.
---

# `panorama-materiaux` : matériaux de construction en France

## Vue d'ensemble

Un projet se conçoit avec des matériaux. Connaître leurs propriétés est aussi important que les conventions de dessin.

## Familles de matériaux

### Béton

- **Béton armé** : béton + armatures acier. Polyvalent, monolithique, résiste à la compression et à la traction (grâce aux aciers).
- **Béton banché** : coulé en place dans des coffrages.
- **Béton préfabriqué** : éléments faits en usine, assemblés sur chantier.
- **Béton bas carbone / béton de site** : moins de ciment, plus de matières recyclées.
- **Qualités** : résistance, inertie thermique, durabilité, formes libres.
- **Limites** : empreinte carbone élevée (le ciment représente ~8% des émissions mondiales), pas isolant.

### Maçonnerie

- **Brique de terre cuite** : monomur, classique, isolation modeste à elle seule.
- **Bloc béton (parpaing)** : économique, à compléter par un isolant.
- **Brique de terre crue** : faible empreinte carbone, bonne inertie, à protéger de l'eau.
- **Pierre** : pierre de taille (massif), moellons (moins coûteux), pierre apparente ou enduite.
- **Qualités** : robustesse, inertie, esthétique ancienne.
- **Limites** : poids, mise en oeuvre lente.

### Bois

- **Ossature bois** : montants verticaux, isolant entre les montants. Léger, rapide.
- **CLT** (Cross-Laminated Timber, bois lamellé-croisé) : panneaux massifs, en plancher ou en mur.
- **Bois massif empilé** (rondin) : tradition montagnarde.
- **Charpente** : traditionnelle (fermes), industrielle (fermettes), lamellé-collé (grandes portées).
- **Qualités** : faible empreinte carbone, légèreté, préfabrication, ressource renouvelable si gérée.
- **Limites** : tenue au feu (gérée par dimensionnement), humidité à éviter.

### Acier

- **Profilés laminés** (IPE, HEB) : structure de bâtiments tertiaires, halles.
- **Charpente métallique** : grandes portées, halles, gares.
- **Bardage métallique** : enveloppe légère.
- **Qualités** : grande portée, légèreté structurelle, recyclabilité.
- **Limites** : conductivité thermique (ponts thermiques), corrosion à protéger, énergie grise élevée.

### Verre

- Mono, double, triple vitrage selon performance.
- Verre feuilleté (sécurité), trempé (résistance).
- **Qualités** : transparence, apport solaire.
- **Limites** : faible isolation à elle seule, fragilité, surchauffe possible.

### Isolants

Voir aussi `enveloppe-isolation`.

- **Minéraux** : laine de verre, laine de roche.
- **Pétrochimiques** : polystyrène expansé (PSE), polyuréthane (PUR), PIR.
- **Biosourcés** : laine de bois, ouate de cellulose, paille, chanvre, liège.
- **Compromis** : performance / coût / empreinte carbone / sensibilité à l'humidité.

### Terre crue

- **Pisé** : terre tassée dans des coffrages.
- **Adobe** : briques séchées au soleil.
- **Bauge** : terre + paille modelée.
- **Torchis** : terre + paille sur claie de bois.
- En revival : très bas carbone, inertie excellente, demande savoir-faire.

### Matériaux de réemploi

Tendance majeure : isolants, briques, charpentes récupérés sur d'autres chantiers. Voir Cycle Up, Bellastock.

## Procédure

1. **Identifier la demande** : panorama général, comparaison de 2 matériaux, choix pour un usage ?
2. **Donner les propriétés** clés : densité, conductivité thermique λ, résistance, durabilité, empreinte carbone.
3. **Donner les usages courants**.
4. **Donner les limites** sans complaisance.

## Sortie attendue

```
Mur porteur en bois CLT

Caractéristiques
  - densité : ~500 kg/m³
  - épaisseur courante : 100 à 200 mm pour un mur courant
  - λ (conductivité) : 0,12 W/m·K (pas isolant à lui seul)
  - performance feu : R60 selon dimensionnement
  - empreinte carbone : faible, stockage CO2 (bois)

Usages
  - mur porteur de logement R+4 et plus
  - plancher (épaisseur 140-180 mm)
  - voile de contreventement

Limites
  - sensible à l'humidité, demande étanchéité parfaite
  - coût plus élevé que ossature bois classique
  - approvisionnement encore limité en France

Bons exemples
  - immeuble Sensations à Strasbourg (KOZ Architectes)
  - immeuble Wood Up à Paris (LAN Architecture)
```

## Notes pédagogiques

- Un matériau n'est pas "bon" ou "mauvais" : il dépend du contexte (climat, usage, économie, culture locale).
- La **filière locale** compte : utiliser de la pierre des carrières voisines a plus de sens qu'importer.
- Le **carbone** est devenu un critère central depuis la RE2020.

## Limites

- Le panorama est volontairement simplifié.
- Les chiffres de λ et de densité sont indicatifs, varient selon les produits.
