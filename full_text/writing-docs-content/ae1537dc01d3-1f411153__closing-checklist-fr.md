---
name: closing-checklist-fr
description: >
  Génère une checklist de closing M&A adaptée au droit français : conditions
  suspensives à lever, séquençage signing/closing, documentation à réunir,
  formalités post-closing (dépôt au greffe, registre de mouvements de titres,
  droits d'enregistrement). Brouillon soumis à validation humaine (avocat).
  Mode `--pe` : lentille closing LBO (funds flow / sources & uses, mécanique day-1, assistance financière).
version: "2.1.0"
argument-hint: "[deal, side, conditions suspensives, calendrier] [--pe --side=sponsor|cedant]"
authors: ["Hacienda"]
tags: [closing, checklist, ma, conditions-suspensives, formalites, pe, lbo, funds-flow]
---

# Skill — Checklist de closing

> **BROUILLON SOUMIS À validation humaine (avocat) M&A.**
>
> Ce skill produit une checklist de travail destinée à organiser et à
> séquencer la réalisation d'une opération M&A. Elle ne vaut ni acte, ni
> conseil juridique, ni conseil fiscal : elle s'appuie sur les documents
> fournis et sur les usages de la pratique, et doit être validée par un avocat
> avant d'être utilisée pour piloter un closing.
>
> **Une formalité post-closing omise — inscription au registre de mouvements
> de titres, droits d'enregistrement — peut affecter l'opposabilité de la
> cession ou entraîner une pénalité fiscale.** L'inscription au registre de
> mouvements de titres et la mise à jour des comptes d'associés conditionnent
> l'opposabilité de la cession d'actions ; la formalité d'enregistrement de la
> cession a un délai propre dont le dépassement expose à une pénalité. Ces
> deux volets ne sont pas accessoires : ils figurent au cœur du post-closing.
>
> **Les taux de droits d'enregistrement relèvent de la fiscalité.** Ce skill
> rappelle l'existence de la formalité et de son délai, mais ne chiffre jamais
> un taux : tout taux ou seuil fiscal est tagué `[à vérifier]` et renvoyé à
> l'expert-comptable ou au plugin `hacienda-fiscal`.

---

## Examples

<example>
<user>/h-da:closing-checklist-fr --type=cession-titres --forme=SAS</user>
<response>
1. Pré-flight `check-pii` (parties, dirigeants, prix de cession → probable seuil B → prompt utilisateur, décision respectée)
2. Lecture profil cabinet (bloc M&A / Corporate : side habituel, matrice d'approbateurs — ligne « Signature SPA »)
3. Intake : opération = cession de titres ; forme = SAS ; conditions suspensives connues ; date de closing visée
4. Étape 1 — recensement des conditions suspensives : agrément, financement, autorisations — statut / responsable / échéance par CP
5. Étape 2 — séquençage signing / closing : ordre des étapes, actes à signer le jour du closing
6. Étape 3 — documentation de closing : ordres de mouvement de titres, déclarations, attestations, mainlevées de sûretés
7. Étape 4 — formalités post-closing : inscription au registre de mouvements de titres + mise à jour des comptes d'associés (opposabilité de la cession d'actions), enregistrement de la cession (formalité + délai ; taux `[à vérifier]` → renvoi expert-comptable / `hacienda-fiscal`), information des tiers
8. Étape 5 — post-flight `verifier-citations`
9. Sortie : en-tête confidentialité + note du relecteur (5 champs) + checklist en 4 volets (CP / séquençage / documentation / post-closing) sous forme de tableaux + question hors checklist + arbre de décision 5 options
</response>
</example>

<example>
<user>/h-da:closing-checklist-fr --type=cession-titres --forme=SAS --cp="agrément du conseil, autorisation administrative sectorielle"</user>
<response>
Conditions suspensives multiples. L'étape 1 tabule chaque CP séparément :
- CP « agrément du conseil » → organe compétent à identifier dans les statuts (clause d'agrément SAS — art. L.227-14 C.com. `[Légifrance]`), responsable = cédant, échéance = avant le closing.
- CP « autorisation administrative sectorielle » → relève du droit réglementaire ; ne pas en chiffrer le délai ni en préjuger l'issue `[review]` ; responsable = acquéreur le plus souvent ; renvoyer le volet sectoriel à `hacienda-reglementaire`.
Chaque CP porte un statut (levée / en cours / à lever), un responsable et une échéance. Une CP non levée à la date de closing visée fait remonter un point 🟠/🔴 : le closing ne peut pas intervenir tant qu'une CP est pendante, sauf renonciation expresse par la partie bénéficiaire. Le séquençage de l'étape 2 ordonne la levée des CP avant la réunion de closing.
</response>
</example>

<example>
<user>/h-da:closing-checklist-fr --type=cession-titres --forme=SAS --volet=post-closing</user>
<response>
Focus sur le volet 4 — formalités post-closing d'une cession d'actions de SAS :
- **Inscription au registre de mouvements de titres** et mise à jour des comptes d'associés individuels : l'ordre de mouvement de titres signé au closing est inscrit au registre ; cette inscription, et non le seul acte de cession, emporte le transfert opposable des actions. Responsable : la société (ou son mandataire). Échéance : sans délai après le closing. Omission → la cession peut être inopposable à la société et aux tiers `[review]`.
- **Enregistrement de la cession (CERFA / formalité fiscale)** : la cession de droits sociaux est soumise à une formalité d'enregistrement assortie d'un délai propre. Les droits d'enregistrement sont dus ; **leur taux et leur assiette relèvent de la fiscalité — `[à vérifier]`, renvoi expert-comptable / `hacienda-fiscal`**. Ce skill rappelle la formalité et le délai, il ne chiffre pas le taux.
- **Information des tiers** : cocontractants liés par une clause de changement de contrôle, organes sociaux, le cas échéant salariés selon le cas.
La checklist post-closing est rendue en tableau avec statut et responsable par formalité.
</response>
</example>

<example>
<user>/h-da:closing-checklist-fr --type=cession-titres --forme=SAS --pe --side=sponsor</user>
<response>
Mode PE (side sponsor). Outre les 4 volets standard, l'Étape PE applique L1–L5 : Volet 5 funds flow /
sources & uses (structure, montants `[à compléter]`), séquençage CP financement (DCL/ECL/certain funds),
chorégraphie day-1 (capitalisation BidCo → tirage dette → paiement vendeurs → rollover →
refinancement/mainlevées → security package), et 🔴 contrôle assistance financière (L.225-216 C.com.
`[à vérifier]` : la cible ne peut pas garantir la dette d'acquisition — `[review]`, renvoi montage).
Registre de mouvements de titres aux deux niveaux (BidCo + cible) + accession deed rollover au closing.
Gate France/Lux : docs fonds Lux hors périmètre.
</response>
</example>

---

## Chargement du profil

> Lire `~/.claude/plugins/config/hacienda-juridique/hacienda-droit-affaires/CLAUDE.md`, bloc « M&A / Corporate » du §1 :
> - **Side habituel M&A** — cédant / acquéreur / conseil des deux — oriente la lecture des CP (qui les lève) et de la documentation à réunir
> - **Taille de deals typique et secteurs cibles** — pour calibrer l'ampleur du séquençage et la documentation attendue
> - **Matrice d'approbateurs** — la ligne « Signature SPA » désigne l'approbateur ; un closing s'escalade de préférence au même approbateur
> - **Politique PII** — `passive` / `active` (défaut) / `strict` + seuil B + catégories sensibles
> - **Rôle de l'utilisateur courant** — pour l'en-tête de confidentialité

Si le profil n'est pas encore peuplé (`[A CONFIGURER]` présent) : stopper et
demander `/h-da:entretien-demarrage`. Le bloc M&A est requis
— sans side habituel ni matrice d'approbateurs, le séquençage et l'escalade ne
peuvent pas être calibrés. Voir aussi `~/.claude/plugins/config/hacienda-juridique/company-profile.md`
pour les éléments cabinet partagés cross-plugins.

---

## Intake

1. **Type d'opération** — `--type=cession-titres` | `--type=cession-fonds` | `--type=fusion`. Détermine les formalités applicables : la cession de titres, la cession de fonds de commerce et la fusion **n'obéissent pas aux mêmes formalités**. À défaut, demander explicitement — le skill ne devine pas le type d'opération.
2. **Forme(s) sociale(s) concernée(s)** — `--forme=SAS` | `--forme=SARL` | `--forme=SA` | autre. Pour une cession de titres, la forme conditionne le mode de transfert (registre de mouvements de titres pour les actions de SAS / SA ; signification ou acceptation de la cession de parts pour la SARL) et l'organe d'agrément.
3. **Conditions suspensives connues** — `--cp="agrément du conseil, financement"`. Liste libre des CP déjà identifiées. Si l'option est absente, le skill demande les CP à l'intake ou les déduit des documents fournis et le signale.
4. **Date de closing visée** — `--closing=2026-09-30`. Sert à calculer les échéances de levée des CP et à ordonner le séquençage. Si absente, le séquençage est rendu en jalons relatifs (closing − N jours).

**Mode `--pe` (overlay Private Equity, side sponsor).** Charge `references/pe-closing-overlay-fr.md`.
En mode `--pe`, `--side` bascule sur `--side=sponsor` (défaut, ≡ acquéreur) | `--side=cedant`
(≡ cédant sponsor). Hors `--pe`, si des **signaux PE** sont détectés (sponsor / BidCo / funds flow /
sources & uses / ECL / DCL / certain funds / rollover / accession deed / debt push-down), **proposer**
l'overlay sans l'imposer (un seul signal sérieux suffit). L'overlay couvre la **jambe française** ;
docs / entité fonds luxembourgeois → STOP overlay, renvoi conseil luxembourgeois (gate France/Lux,
cf. module partagé).

Le skill peut aussi prendre en intake les documents disponibles (SPA, projet de
GAP, statuts, projet de CP) ; il les lit pour alimenter le recensement, sans
les analyser au fond — la revue de fond relève des skills dédiés (voir
« Ce skill ne fait pas »).

---

## Gate non-juriste

- [ ] Type d'opération fourni et confirmé (cession de titres / cession de fonds de commerce / fusion — formalités distinctes)
- [ ] Forme(s) sociale(s) identifiée(s) — mode de transfert et organe d'agrément calibrés sur la forme
- [ ] Pré-flight `check-pii` exécuté et décision utilisateur respectée
- [ ] Profil cabinet bloc M&A lu : side habituel, matrice d'approbateurs (ligne « Signature SPA »)
- [ ] Volet 1 — conditions suspensives recensées avec statut / responsable / échéance par CP
- [ ] Volet 2 — séquençage signing / closing : distinction signing / closing explicite, actes à signer le jour du closing identifiés
- [ ] Volet 3 — documentation de closing listée, pièces manquantes signalées
- [ ] Volet 4 — formalités post-closing : inscription au registre de mouvements de titres + mise à jour des comptes d'associés présentes ; enregistrement / droits d'enregistrement présents avec taux tagués `[à vérifier]` et renvoi expert ; information des tiers présente
- [ ] Aucun taux ou seuil fiscal chiffré comme une certitude — tout taux renvoyé à l'expert-comptable / `hacienda-fiscal`
- [ ] Articles hors index ou en `[a compléter]` tagués `[à vérifier]`
- [ ] Citations vérifiées via `verifier-citations` ou taguées `[à vérifier]`
- [ ] Sortie comprend : en-tête confidentialité + note du relecteur (5 champs) + checklist en 4 volets sous forme de tableaux + question hors checklist + arbre de décision 5 options + footer A si applicable
- [ ] Si `--pe` : module `references/pe-closing-overlay-fr.md` chargé, side `sponsor`/`cedant` posé, gate France/Lux respecté
- [ ] Si `--pe` : Volet 5 funds flow / sources & uses produit (structure ; montants `[à compléter]`, aucun chiffre fabriqué)
- [ ] Si `--pe` : assistance financière (L.225-216 C.com.) vérifiée — aucune sûreté/garantie remontante de la cible validée ; risque qualifié `[review]` et renvoyé
- [ ] Si `--pe` : registre de mouvements de titres aux deux niveaux (BidCo + cible) ; accession deed rollover présent

---

## Outils MCP à privilégier

Appeler les outils par leur nom exact quand le serveur `Hacienda Droit des Affaires` est disponible. Ne pas inventer de tool hors périmètre ; si une source n'a pas été consultée directement, garder `[à vérifier]`.

- Socle sources officielles : `piste_status`, `legifrance_recherche`, `legifrance_get_article`, `judilibre_recherche`, `judilibre_get_decision`, `eurlex_recherche`, `eurlex_consulter`.
- Entreprises, BODACC et procédures collectives : `company_full_profile`, `bodacc_by_siren`, `bodacc_procedures`.
- Points fiscaux et sociaux de due diligence : `bofip_rechercher`, `bofip_consulter`, `boss_recherche`, `boss_get_document`.
- Tout résultat issu d'un corpus client ou d'un outil interne reste distingué des sources primaires officielles.

## Emplacement des sorties

```
outputs/closing-checklist-<parties-slug>-YYYY-MM-DD.md
```

La checklist agrège quatre tableaux ; dès que l'ensemble dépasse 10 lignes ou
contient des dates / échéances sérialisables, générer en parallèle un dashboard
HTML autonome via `renderDashboard()` de `@hacienda/core` (sortable, filtrable,
ouvrable hors-ligne, zéro CDN, XSS-safe — voir `references/dashboard-template.md`).

---

## Sortie

### Format livrable

```
[En-tête de confidentialité selon le rôle utilisateur — voir CLAUDE.md §2]

> **⚠️ Note du relecteur**
> - **Sources :** Légifrance ✓ / Judilibre ✓ / Pappers ✓ / BODACC ✓ (cocher ✗ si non connectée)
> - **Lecture :** {documents fournis lus : SPA / GAP / statuts / projet de CP — ou « aucun document fourni, checklist générée sur la base de l'intake »}
> - **Signalé pour ton jugement :** {N} éléments marqués [review] | aucun
> - **Fraîcheur :** recherche des évolutions depuis {date} sur les formalités de cession et d'enregistrement — {N} mises à jour intégrées | rien trouvé
> - **Avant de t'appuyer dessus :** {1-2 actions concrètes — typiquement « faire confirmer par l'expert-comptable la formalité et le délai d'enregistrement, et les taux applicables » OU « prêt pour relecture »}

# Checklist de closing — {type d'opération}, {forme sociale}

## Étape 1 — Conditions suspensives

Recenser **toutes les conditions suspensives** de l'opération — celles fournies
via `--cp`, celles extraites des documents, celles que la nature de l'opération
rend usuelles (agrément, autorisations, financement, accord des organes
sociaux). Pour **chaque CP**, renseigner :

- **Objet** — la condition elle-même (ex : « obtention par l'acquéreur de son financement »).
- **Statut** — `levée` / `en cours` / `à lever`. Une CP `levée` est documentée par une pièce justificative ; une CP `en cours` est engagée mais non aboutie ; une CP `à lever` n'a pas encore été engagée.
- **Responsable** — la partie ou le tiers chargé de lever la CP (cédant, acquéreur, société, organe social, autorité administrative). Côté `--side` configuré, distinguer les CP que l'utilisateur maîtrise de celles qui dépendent de la contrepartie ou d'un tiers.
- **Échéance** — la date butoir de levée, rapportée à la date de closing visée. Toute CP non levée à la date de closing est un point de vigilance : le closing ne peut pas intervenir tant qu'une CP demeure pendante, sauf renonciation expresse par la partie qui en bénéficie `[review]`.

Points de qualification :

- **CP potestative** — une CP dont la réalisation dépend de la seule volonté de la partie obligée est fragile `[review]` ; la signaler.
- **CP d'agrément statutaire** — lorsque les statuts soumettent la cession à un agrément (clause d'agrément SAS — liberté statutaire art. L.227-14 C.com. `[Légifrance]` ; identifier l'organe compétent dans les statuts), l'agrément doit être **obtenu avant le closing** et **ne peut pas être régularisé après ni écarté par le seul acquéreur**. Signaler expressément la **sanction** : une cession réalisée **en violation** d'une clause statutaire d'agrément est **nulle** (art. L.227-15 C.com. `[Légifrance]`). C'est donc une CP 🔴 tant qu'elle n'est pas levée — pas une simple formalité interne.
- **CP réglementaire / sectorielle** — une autorisation administrative (autorisation sectorielle, contrôle des investissements étrangers, contrôle des concentrations) ne se chiffre pas et son issue ne se préjuge pas `[review]` ; renvoyer le volet réglementaire à `hacienda-reglementaire` et le volet concurrence à un conseil concurrence. Ce skill recense la CP, il ne l'instruit pas.
- **Renonciation à une CP** — préciser quelle partie peut renoncer à quelle CP (une CP est en principe stipulée dans l'intérêt d'une partie déterminée).

Findings 🟢/🟡/🟠/🔴 par CP selon le statut et la proximité de l'échéance. Tag
`[review]` sur les appréciations (caractère potestatif, probabilité de levée
dans les délais).

---

## Étape 2 — Séquençage signing / closing

**Distinguer signing et closing.** Le *signing* est la signature du contrat de
cession (SPA / acte de cession) ; le *closing* (réalisation) est le moment où
la propriété des titres ou du fonds est effectivement transférée et le prix
payé. Entre les deux s'écoule la **période intercalaire** (*interim period*),
pendant laquelle les conditions suspensives sont levées. Lorsque signing et
closing sont concomitants (closing « en une seule étape »), le séquençage se
réduit, mais la distinction des actes reste utile.

Ordonner les étapes :

1. **Avant le signing** — finalisation du SPA et de la GAP, dernières
   vérifications de due diligence, accords préalables internes.
2. **Au signing** — signature du SPA / de l'acte de cession ; le cas échéant,
   versement d'un acompte ou constitution d'un séquestre.
3. **Période intercalaire** — levée des conditions suspensives (étape 1),
   respect des engagements d'interim (gestion en bon père de famille, absence
   d'opérations hors cours normal), purge des droits de préemption ou
   d'agrément.
4. **Au closing — actes à signer le jour du closing.** Identifier précisément
   les actes signés le jour de la réalisation, typiquement :
   - **Cession de titres** : ordres de mouvement de titres signés par le
     cédant ; le cas échéant, réitération de l'acte de cession ; constatation
     de la levée des CP ; quittance de prix ; démission et nomination des
     dirigeants et organes sociaux ; mainlevées de sûretés grevant les titres.
   - **Cession de fonds de commerce** : acte de cession du fonds ; séquestre du
     prix entre les mains du rédacteur ou d'un séquestre conventionnel
     (protection des créanciers du vendeur) ; états et inventaires.
   - **Fusion** : approbation du traité de fusion par les assemblées des
     sociétés concernées ; constatation de la réalisation.
5. **Après le closing** — formalités post-closing (étape 4).

Le séquençage est rendu en tableau (étape / acte / moment / responsable). Tag
`[review]` sur l'ordonnancement lorsqu'une étape conditionne une autre et que
l'ordre dépend d'un arbitrage (ex : purge de l'agrément avant ou
concomitamment au signing).

---

## Étape 3 — Documentation de closing

Lister les **documents à réunir** pour le closing. Le contenu varie selon le
type d'opération et la forme sociale ; recenser au minimum :

- **Actes de transfert** — ordres de mouvement de titres (actions de SAS / SA) ;
  acte de cession de parts et formalités de signification ou d'acceptation
  (parts de SARL) ; acte de cession du fonds (cession de fonds de commerce) ;
  traité de fusion (fusion).
- **Preuves de levée des CP** — pour chaque CP `levée`, la pièce justificative
  (décision d'agrément, lettre de financement, autorisation administrative,
  PV d'organe social).
- **Déclarations et attestations** — déclarations des parties au titre de la
  GAP, attestations de non-procédure collective, attestations sociales et
  fiscales, certificats de l'expert-comptable le cas échéant.
- **Mainlevées de sûretés** — mainlevée des nantissements de titres, gages,
  cautionnements ou sûretés grevant les actifs cédés ; accords des créanciers
  bénéficiaires.
- **Documents sociaux** — registre de mouvements de titres et comptes
  d'associés (à jour pour constater l'inscription post-closing), statuts à
  jour, PV des organes sociaux, démissions et nominations des mandataires.
- **Quittances et flux financiers** — quittance de prix, instructions de
  virement, convention de séquestre / d'escrow le cas échéant.
- **Pièces fiscales** — formulaire d'enregistrement de la cession (CERFA) à
  préparer pour le post-closing (voir étape 4).

La documentation est rendue en tableau (document / volet / statut / responsable
de la production). Une pièce manquante est un point de vigilance, jamais une
omission silencieuse.

---

## Étape 4 — Formalités post-closing

Les formalités qui suivent la réalisation conditionnent l'opposabilité de
l'opération et la régularité fiscale. **Distinguer selon le type d'opération.**

### 4.1 Cession de titres

- **Inscription au registre de mouvements de titres et mise à jour des comptes
  d'associés.** Pour les actions (SAS, SA), le transfert de propriété **s'opère
  par virement du compte du cédant au compte de l'acquéreur** (art. L.228-1 al. 9
  C.com. `[Légifrance]` et art. L.211-17 CMF `[Légifrance]`) : l'ordre de
  mouvement de titres signé au closing est inscrit sur le **registre de
  mouvements de titres** de la société et le compte d'associé individuel de
  l'acquéreur est mis à jour. **C'est cette inscription en compte — et non le
  seul acte de cession ni la seule signature — qui emporte le transfert et son
  opposabilité** à la société et aux tiers. Corriger expressément toute idée que
  « la signature suffit » ou que « les formalités se régularisent plus tard » :
  tant que le virement de compte à compte n'est pas porté, l'acquéreur n'est pas
  propriétaire opposable. L'omission est un risque sérieux `[review]`.
  Responsable : la société (ou son mandataire / l'avocat).
  Échéance : sans délai après le closing.
  - Pour les **parts de SARL**, la cession est rendue opposable à la société
    soit par signification (formes de l'art. 1690 C.civ `[à vérifier]`), soit —
    voie usuelle — par le dépôt d'un original de l'acte de cession au siège
    social contre attestation de dépôt délivrée par le gérant (art. L.221-14
    C.com. `[à vérifier]`) ; elle n'est opposable aux tiers qu'après ces
    formalités et la publicité au RCS. Adapter à la forme sociale.
- **Enregistrement de la cession — droits d'enregistrement.** La cession de
  droits sociaux est soumise à une **formalité d'enregistrement** auprès du
  service des impôts, assortie d'un **délai propre** dont le dépassement
  expose à une **pénalité fiscale**. Un formulaire CERFA est déposé. **Les
  taux et l'assiette des droits d'enregistrement relèvent de la fiscalité :
  `[à vérifier]` — renvoi à l'expert-comptable ou au plugin `hacienda-fiscal`.**
  Ce skill rappelle l'existence de la formalité et de son délai ; il ne chiffre
  jamais un taux et ne donne pas de conseil fiscal détaillé.
- **Mise à jour des registres légaux et publicité** — registre des décisions,
  le cas échéant mise à jour des informations au RCS (changement de
  dirigeant), dépôt au greffe si la cession s'accompagne d'une modification
  statutaire (voir 4.4).

### 4.2 Cession de fonds de commerce

- **Enregistrement de l'acte de cession** auprès du service des impôts —
  formalité et délai propres ; droits d'enregistrement dus, **taux fiscal
  `[à vérifier]` → renvoi expert-comptable / `hacienda-fiscal`**.
- **Publicité de la cession** — publication dans un support d'annonces légales
  et au BODACC, qui fait courir le délai d'opposition des créanciers du
  vendeur.
- **Séquestre du prix** — le prix reste séquestré le temps des délais
  d'opposition et de purge des privilèges et inscriptions.
- Pas de registre de mouvements de titres ici : la cession de fonds n'est pas
  une cession de droits sociaux — ne pas confondre les deux régimes.

### 4.3 Fusion

- **Dépôt et publicité** — dépôt des actes de fusion au greffe, publicité au
  BODACC, le cas échéant radiation de la société absorbée.
- **Formalités d'enregistrement** propres à l'opération — **taux et régime
  fiscal `[à vérifier]` → renvoi expert-comptable / `hacienda-fiscal`** (le
  régime de faveur des fusions est un sujet fiscal, hors périmètre de ce skill).
- **Transfert universel de patrimoine** — la fusion emporte transmission du
  patrimoine de l'absorbée ; vérifier les formalités d'opposabilité propres
  aux actifs transmis (immeubles, titres, contrats).

### 4.4 Dépôt au greffe (le cas échéant, tous types)

Lorsque l'opération s'accompagne d'une modification statutaire (changement de
dénomination, de dirigeant, de siège, augmentation de capital concomitante),
les actes modificatifs sont déposés au greffe du tribunal de commerce et la
modification est inscrite au RCS. Le dépôt des comptes annuels au greffe
(art. L.232-23 C.com. `[Légifrance]`) suit son propre calendrier, distinct du
closing.

### 4.5 Information des tiers

- **Cocontractants** — information ou demande de consentement des
  cocontractants liés par une clause de **changement de contrôle** (voir
  `references/clauses-sensibles-fr.md`, bloc 15) ; l'idéal est d'avoir purgé
  ces consentements en condition suspensive avant le closing.
- **Organes sociaux** — information des organes de gouvernance, mise à jour
  des mandats.
- **Salariés** — information selon le cas : l'opération peut déclencher des
  obligations d'information ou de consultation. Le détail relève du droit
  social et de `hacienda-social` ; ce skill signale le point sans l'instruire
  `[review]`.
- **Administrations et partenaires** — banques, assureurs, bailleurs,
  administrations sectorielles selon la nature de l'activité.

Chaque volet est rendu en tableau (formalité / délai / statut / responsable).
Tout taux ou seuil fiscal porte `[à vérifier]` et un renvoi explicite à
l'expert ; aucun taux n'est chiffré comme une certitude.

---

## Étape PE — Overlay closing LBO (si `--pe` ou overlay accepté)

Ne s'exécute qu'avec `--pe` (flag) ou après acceptation d'une auto-proposition. Charger
`references/pe-closing-overlay-fr.md` et appliquer les 5 axes, side `sponsor` (défaut) ou `cedant` :

1. **L1 — Funds flow / sources & uses** : produire le **tableau sources & uses** (Volet 5) ;
   réconciliation Σsources = Σuses, cohérence avec le prix SPA et les montants ECL/DCL ; waterfall
   des virements day-1. **Ne pas chiffrer** — structure et lignes, montants en `[à compléter]`.
2. **L2 — CP financement & certain funds** : séquencer les conditions DCL/ECL et le certain funds
   pour le jour J ; signaler tout désalignement CP du SPA ↔ conditions de financement (→ Volet 1).
3. **L3 — Mécanique de closing LBO** : chorégraphie day-1 (capitalisation BidCo → tirage dette →
   paiement vendeurs → rollover → refinancement/mainlevées → security package) (→ Volet 2).
4. **L4 — Security package & assistance financière** : 🔴 vérifier qu'aucune sûreté/garantie
   remontante de la cible ne sécurise la dette d'acquisition (**assistance financière L.225-216
   C.com. `[à vérifier]`**) ; qualifier le risque `[review]`, **ne jamais valider un montage**,
   renvoyer au montage fiscal/financier (→ Volets 2/3 + findings).
5. **L5 — Adhésion rollover & post-closing PE** : accession deed au closing ; **registre de
   mouvements de titres aux deux niveaux (BidCo + cible)** ; inscription des nantissements ; closing
   bible PE ; régime fiscal d'apport rollover → `[à vérifier]`, renvoi expert (→ Volet 4).

**Gate France/Lux** (module partagé) : entité/docs fonds Lux → STOP overlay, renvoi conseil
luxembourgeois ; l'overlay couvre la jambe FR. Sortir les findings PE dans les volets existants
(sévérité 🟢🟡🟠🔴) + le **Volet 5 funds flow**. **Ne pas chiffrer** le funds flow (`[à compléter]`) ;
**ne pas valider** l'assistance financière (`[review]`, renvoi) ; **ne pas dater** le closing
(semaines relatives). Si la cible est aussi en difficulté, **les overlays `--pe` et `--distressed`
s'empilent** sans se dupliquer.

---

## Étape 5 — Post-flight

Appel automatique de `verifier-citations` sur la sortie complète. Les articles
C.civ / C.com. cités doivent exister dans
`references/articles-c-civ-c-com-index.md` ; à défaut, ou s'ils sont en
`[a compléter]`, tag `[à vérifier]` et ligne dédiée dans la note du relecteur.
Si PISTE n'est pas configuré : mode dégradé documenté dans la note du relecteur
(« `verifier-citations` non exécuté — N citations à valider manuellement »).

---

## Volet 1 — Conditions suspensives

| # | Condition suspensive | Statut | Responsable | Échéance | Sévérité |
|---|---|---|---|---|---|
| ... | ... | levée / en cours / à lever | ... | ... | 🔴/🟠/🟡/🟢 |

## Volet 2 — Séquençage signing / closing

| # | Étape | Acte / livrable | Moment | Responsable |
|---|---|---|---|---|
| ... | ... | ... | avant signing / au signing / interim / au closing / post-closing | ... |

## Volet 3 — Documentation de closing

| # | Document | Volet | Statut | Responsable de la production |
|---|---|---|---|---|
| ... | ... | ... | à produire / en cours / réuni | ... |

## Volet 4 — Formalités post-closing

| # | Formalité | Délai | Statut | Responsable |
|---|---|---|---|---|
| ... | Inscription au registre de mouvements de titres + mise à jour des comptes d'associés | sans délai après closing | ... | société / mandataire |
| ... | Enregistrement de la cession — droits d'enregistrement (taux a verifier — renvoi expert-comptable / hacienda-fiscal) | délai propre — a verifier | ... | acquéreur / rédacteur |
| ... | Information des tiers (changement de contrôle, organes, salariés selon le cas) | ... | ... | ... |

## Volet 5 — Funds flow / sources & uses (si `--pe`)

Réconciliation **sources & uses** au closing (structure ; **montants en `[à compléter]`, jamais chiffrés**).

| Sources | Montant | Uses | Montant |
|---|---|---|---|
| Equity sponsor (ECL) | [à compléter] | Prix d'acquisition (SPA) | [à compléter] |
| Rollover managers (reinvest) | [à compléter] | Refinancement dette existante cible | [à compléter] |
| Dette senior (DCL) | [à compléter] | Frais de transaction + prime W&I | [à compléter] |
| Mezzanine / unitranche / vendor loan | [à compléter] | Frais de mise en place de la dette | [à compléter] |
| Cash on balance sheet | [à compléter] | Escrow / holdback + BFR day-1 | [à compléter] |
| **Σ sources** | [à compléter] | **Σ uses** | [à compléter] |

Réconciliation : Σsources = Σuses ; le prix SPA figure en use ; cohérence ECL/DCL/reinvest.
Toute incohérence est un point 🟠/🔴. Waterfall des virements day-1 rendu en tableau (étape / flux /
compte émetteur → récepteur / moment), avec la ligne 🔴 **assistance financière** si une sûreté/garantie
remontante de la cible sécurise la dette d'acquisition (L.225-216 C.com. `[à vérifier]`, `[review]`).

# Une question hors de ma checklist habituelle

{Observation transversale qu'un relecteur attentif ferait. Omettre la ligne si
rien d'honnête à dire — ne pas fabriquer.}

# Que veux-tu faire ? Choisis une option et je la déroule :

1. **Rédiger** — je produis le calendrier de closing détaillé (timeline jalonnée) ou la liste de pièces (closing bible) mise en forme prête à être adressée aux parties.
2. **Escalader** — je rédige une note d'escalade vers {approbateur SPA configuré} avec les CP non levées, les pièces manquantes et la décision attendue avant de fixer la date de closing.
3. **Compléter les faits** — questions ouvertes à poser au {cédant / acquéreur / société cible / conseil / expert-comptable} pour compléter le recensement des CP et de la documentation.
4. **Surveiller et attendre** — j'ajoute la checklist au tracker du deal avec note motivée et date de revisite (levée des CP, date de closing, échéance de la formalité d'enregistrement).
5. **Autre** — précise ce que tu veux en faire.

{Footer A — si check-pii est passé en mode passif sous le seuil B :
[Ce skill a traité {N} mentions identifiantes. Pour anonymiser automatiquement avant envoi à Claude, installer hacienda-ghost.](https://hacienda.diy/ghost)
Sinon, rien.}
```

### Mode silencieux (livrable externe)

Si la sortie est destinée à un comité d'investissement, un sponsor business
non-juriste, la contrepartie ou un conseil tiers :

- Conserver l'en-tête de confidentialité (si le destinataire est dans le
  périmètre du secret) et la note du relecteur.
- Retirer la narration de skill et les renvois inter-commandes (les placer
  dans un message séparé).
- Le livrable — calendrier de closing ou liste de pièces — doit se lire comme
  s'il avait été préparé par un associé M&A.

---

## Ce skill ne fait pas

- Réviser ou rédiger le SPA / l'acte de cession → `reviser-contrat` (tronc commercial) ou skill SPA dédié.
- Réviser la GAP → `gap-review` (les CP de la GAP alimentent le volet 1).
- Réviser ou rédiger la LOI / le term sheet → `loi-term-sheet`.
- Conduire la due diligence → `due-diligence-dataroom`.
- Donner un avis fiscal détaillé : régime des plus-values, **taux et assiette des droits d'enregistrement**, régime de faveur des fusions, intégration fiscale — signalement uniquement, renvoi à l'expert-comptable et à `hacienda-fiscal`. Ce skill rappelle la formalité et le délai, jamais le taux.
- Instruire une autorisation administrative ou sectorielle (contrôle des investissements étrangers, autorisations sectorielles) → `hacienda-reglementaire` ; le contrôle des concentrations relève d'un conseil concurrence.
- Instruire les obligations d'information-consultation des salariés → `hacienda-social`.
- Réaliser, signer ou exécuter le closing — acte des parties et de l'approbateur configuré ; ce skill organise et séquence, il n'exécute pas.
- En mode `--pe` : ne **chiffre pas** le funds flow (structure du tableau sources & uses ; montants `[à compléter]`).
- En mode `--pe` : ne **valide pas** un montage d'**assistance financière / debt push-down / upstream guarantee** (L.225-216 C.com.) — risque nommé, qualifié `[review]`, renvoyé.
- En mode `--pe` : pas d'avis fiscal (régime d'apport du rollover, intégration fiscale LBO, droits d'enregistrement) → `[à vérifier]`, renvoi expert / `hacienda-fiscal`.
- En mode `--pe` : ne structure pas les instruments du management package (BSA/BSPCE/ADP/AGA/OC) → `financement-startup`.
- En mode `--pe` : ne couvre pas les documents luxembourgeois (gate France/Lux).

---

## Ton

Technique, structuré, opérationnel. La checklist est un outil de pilotage : la
distinction **signing / closing** doit être explicite, le **séquençage** des
actes clair, les **responsables** et **échéances** nommés. Les formalités
post-closing ne sont pas un appendice : l'inscription au registre de mouvements
de titres et la mise à jour des comptes d'associés conditionnent l'opposabilité
de la cession d'actions, et la formalité d'enregistrement a un délai propre
dont le dépassement coûte une pénalité. Distinguer nettement cession de titres,
cession de fonds de commerce et fusion — les formalités diffèrent. Ne jamais
chiffrer un taux de droits d'enregistrement : c'est un sujet fiscal, tagué
`[à vérifier]` et renvoyé à l'expert. La sortie est un brouillon soumis à
validation humaine (avocat) M&A avant d'être utilisée pour piloter une opération réelle.
En mode `--pe`, le funds flow / sources & uses est l'artefact central (structure, jamais les montants), et l'assistance financière (L.225-216 C.com.) est le piège closing LBO à signaler sans jamais valider de montage.
