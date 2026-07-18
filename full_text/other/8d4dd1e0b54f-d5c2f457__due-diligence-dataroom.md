---
name: due-diligence-dataroom
description: >
  Analyse de data-room M&A sur 7 thèmes (corporate, contrats, social, PI,
  fiscal, contentieux, RGPD). S'appuie sur revue-tabulaire pour l'extraction
  multi-documents. Produit un rapport structuré par thème, une grille de
  matérialité, une Q&A list et des recommandations pour la GAP. Brouillon
  soumis à validation humaine (avocat). Mode `--pe` (alias `--mode=pe-red-flags`) :
  lentille red flags Private Equity — chaque finding matériel converti en
  traitement deal (CP / GAP / W&I / specific indemnity / price chip / Q&A).
version: "2.1.0"
argument-hint: "[dataroom, side, thèmes, seuil de matérialité]"
authors: ["Hacienda"]
tags: [due-diligence, dataroom, ma, materialite, gap, pe, red-flags]
---

# Skill — Due diligence data-room

> **BROUILLON SOUMIS À validation humaine (avocat) M&A.**
>
> Audit juridique d'une data-room d'opération M&A sur 7 thèmes : corporate /
> gouvernance, contrats matériels, social / RH, propriété intellectuelle,
> fiscal / financier, contentieux / passifs, RGPD / conformité. La sortie est
> un rapport de DD préliminaire — il oriente la négociation et la GAP mais ne
> les remplace pas, et doit être validé par un avocat M&A.
>
> **Une data-room contient un volume massif de données sensibles** — contrats
> nominatifs, données salariés, IBAN, montants, données de santé éventuelles,
> SIREN, mentions « secret des affaires ». Le pré-flight `check-pii` sur
> l'ensemble du dossier est **critique** : le franchissement du seuil B est ici
> la règle, pas l'exception. Ne jamais traiter une data-room sans pré-flight.
>
> **L'analyse oriente la GAP, ne s'y substitue pas.** Les findings matériels
> alimentent les recommandations GAP (étape 6), mais la revue de la Garantie
> d'Actif et de Passif elle-même relève du skill `gap-review`.

---

## Examples

<example>
<user>/h-da:due-diligence-dataroom ./data-room-cible-X/ --side=acquereur</user>
<response>
1. Pré-flight `check-pii` sur l'ensemble du dossier data-room (volume élevé : contrats salariés, IBAN, SIREN, montants > 10k€ → seuil B franchi → prompt utilisateur, décision respectée)
2. Lecture profil cabinet (bloc M&A / Corporate : side acquéreur, posture DD — thèmes prioritaires et seuil de matérialité)
3. Inventaire de la data-room : N documents recensés, classés par thème
4. Extraction multi-documents — invocation du skill V1 `revue-tabulaire` (colonnes adaptées au thème : parties, dates, durée, changement-de-contrôle, exclusivité…) ; récupération du tableau d'extraction
5. Analyse des 7 thèmes via `references/grille-due-diligence-fr.md` : points de contrôle, red flags, documents manquants — renvois en pointeurs vers PI / fiscal / RGPD
6. Grille de matérialité : chaque finding classé thème × gravité (🟢/🟡/🟠/🔴) × statut
7. Q&A list générée — questions complémentaires à adresser au cédant
8. Recommandations GAP pour les findings matériels (lien `gap-review`)
9. Post-flight `verifier-citations`
10. Sortie : en-tête confidentialité + note du relecteur (5 champs) + résumé exécutif + rapport par thème + grille de matérialité + Q&A list + recommandations GAP + question hors checklist + arbre 5 options
</response>
</example>

<example>
<user>/h-da:due-diligence-dataroom ./data-room/ --side=acquereur --themes=corporate,contrats,contentieux</user>
<response>
DD ciblée sur 3 thèmes (corporate / gouvernance, contrats matériels, contentieux / passifs). Les 4 autres thèmes (social, PI, fiscal, RGPD) ne sont pas couverts.

Le rapport ne traite que les 3 thèmes demandés. La note du relecteur, champ « Lecture », mentionne explicitement les 4 thèmes non couverts : « DD ciblée — social, PI, fiscal, RGPD non audités ; rapport partiel, ne pas le présenter comme une DD complète. » Le champ « Signalé pour ton jugement » liste les documents manquants sur les thèmes effectivement couverts.
</response>
</example>

<example>
<user>/h-da:due-diligence-dataroom ./data-room-volumineuse/ --side=acquereur</user>
<response>
Data-room volumineuse (plusieurs centaines de documents : contrats de travail, liasses fiscales, contrats clients nominatifs). Le pré-flight `check-pii` agrège les identifiants sur tout le dossier : le seuil B (50 identifiants OU 1+ catégorie sensible) est très largement franchi dès les premiers documents (IBAN, NIR sur contrats de travail, montants).

`check-pii` rend un verdict seuil B atteint → prompt utilisateur : [continuer une fois] [ne plus demander pour ce dossier] [installer hacienda-ghost]. Le skill respecte la décision et ne poursuit l'analyse qu'après celle-ci. Si l'utilisateur installe `hacienda-ghost`, l'anonymisation est appliquée avant analyse ; sinon, footer A rappelé en fin de sortie.
</response>
</example>

<example>
<user>/h-da:due-diligence-dataroom ./data-room/ --side=acquereur --themes=corporate,contrats</user>
<response>
DD ciblée corporate + contrats. Findings matériels remontés : (a) un contrat client clé comporte une clause de changement de contrôle permettant la résiliation en cas de cession → 🔴 ; (b) une clause d'agrément statutaire non purgée → 🟠.

Étape 6 — recommandations GAP : pour chaque finding matériel, esquisse de la protection GAP à demander :
- Clause de changement de contrôle sur contrat clé → déclaration spécifique du cédant sur les contrats à *change of control*, condition suspensive d'obtention du consentement du cocontractant avant closing, ou garantie spécifique chiffrée si le consentement ne peut être obtenu.
- Clause d'agrément non purgée → condition suspensive de purge de l'agrément avant closing.
La sortie renvoie au skill `gap-review` pour la revue de la GAP elle-même, une fois le projet de garantie disponible.
</response>
</example>

<example>
<user>/h-da:due-diligence-dataroom ./data-room-cible-Y/ --side=acquereur --pe</user>
<response>
DD buyside pour un sponsor (acquisition via BidCo FR). Le mode `--pe` charge `references/pe-dd-red-flags-overlay-fr.md` : après les étapes standard (inventaire, extraction, 7 thèmes, grille de matérialité, Q&A, recommandations GAP), l'étape 6bis convertit chaque finding matériel en traitement deal.

Exemples de conversion : (a) clause de changement de contrôle sur le contrat client structurant (28 % du CA — cumul concentration × clause) → CP de consentement du cocontractant, repli specific indemnity + price chip [à compléter] ; (b) redressement URSSAF en cours → known issue exclu de la police W&I → specific indemnity, fond social renvoyé au spécialiste ; (c) clause de change of control default dans le contrat de crédit existant → CP de waiver bancaire, chemin de mainlevée transmis à `/h-da:closing-checklist-fr --pe`.

Livrable : red flag report partner-ready (findings 🔴/🟠 matériels + table de conversion), grille complète en annexe. Aucun montant chiffré, jalons en semaines relatives.
</response>
</example>

---

## Chargement du profil

> Lire `~/.claude/plugins/config/hacienda-juridique/hacienda-droit-affaires/CLAUDE.md`, bloc « M&A / Corporate » :
> - **Side habituel M&A** — cédant / acquéreur / conseil des deux
> - **Posture DD** — thèmes prioritaires et **seuil de matérialité** (montant ou
>   pourcentage en deçà duquel un finding n'est pas qualifié de matériel)
> - **Taille de deals typique et secteurs cibles** — pour calibrer la lecture
> - **Matrice d'approbateurs** — la signature d'un SPA y figure ; le rapport de DD
>   s'escalade de préférence au même approbateur
> - **Politique PII** — `passive` / `active` (défaut) / `strict` + seuil B + catégories sensibles
> - **Rôle de l'utilisateur courant** — pour l'en-tête de confidentialité

Si le profil n'est pas encore peuplé (`[A CONFIGURER]` présent) : stopper et
demander `/h-da:entretien-demarrage`. Le bloc M&A est requis —
sans side habituel ni seuil de matérialité, la qualification des findings et la
grille de matérialité ne peuvent pas être calibrées. Voir aussi
`~/.claude/plugins/config/hacienda-juridique/company-profile.md` pour les éléments cabinet partagés.

---

## Intake

1. **Dossier data-room** — chemin du dossier contenant la data-room
   (ex : `./data-room-cible-X/`). Le skill inventorie récursivement les documents.
2. **Thèmes à couvrir** — `--themes=corporate,contrats,social,pi,fiscal,contentieux,rgpd`.
   **Défaut : les 7 thèmes.** Si l'option est fournie, seuls les thèmes listés sont
   audités et le caractère partiel du rapport est consigné dans la note du relecteur.
3. **Side** — `--side=acquereur` | `--side=cedant`. Détermine la posture : côté
   acquéreur, la DD cherche les expositions et alimente les protections GAP à exiger ;
   côté cédant (*vendor due diligence*), la DD anticipe les findings que l'acquéreur
   relèvera et prépare la *disclosure*.
4. **Seuil de matérialité** (optionnel) — `--seuil-materialite=50000` (en €).
   Override du seuil configuré au profil ; en deçà, un finding n'est pas qualifié
   de matériel (reste signalé mais ne déclenche pas de recommandation GAP).
5. **Mode `--pe`** (optionnel, alias accepté : `--mode=pe-red-flags`) — overlay
   Private Equity, side sponsor (buyside DD) : charge
   `references/pe-dd-red-flags-overlay-fr.md` et ajoute la conversion de chaque
   finding matériel en **traitement deal** (CP / GAP / W&I / specific indemnity /
   price chip / Q&A) plus un red flag report partner-ready. Avec `--side=cedant`,
   lecture *vendor DD* (anticipation / disclosure). Hors `--pe`, si des **signaux
   PE** sont détectés (sponsor/BidCo, W&I, reliance letter, dette LBO / certain
   funds, management package, red flag report demandé), **proposer** l'overlay
   sans l'imposer.

---

## Gate non-juriste

- [ ] Pré-flight `check-pii` exécuté sur l'ensemble de la data-room, décision utilisateur respectée (seuil B très probablement franchi)
- [ ] `--side` fourni et confirmé (acquéreur ou cédant)
- [ ] Profil cabinet bloc M&A lu : side, posture DD, seuil de matérialité
- [ ] Data-room inventoriée : N documents comptés et classés par thème, fichiers illisibles signalés
- [ ] `revue-tabulaire` invoqué pour l'extraction multi-documents, consommé sans modification
- [ ] Les 7 thèmes couverts (ou ceux de `--themes`, le caractère partiel consigné en note du relecteur)
- [ ] Renvois en pointeurs effectués pour PI / fiscal / RGPD — analyse de premier niveau réalisée ici, expertise approfondie renvoyée
- [ ] Articles hors index ou en `[a compléter]` tagués `[à vérifier]` ; RGPD tagué `[Eurlex]` ou `[à vérifier]`
- [ ] Citations vérifiées via `verifier-citations` ou taguées `[à vérifier]`
- [ ] Si mode `--pe` : module `pe-dd-red-flags-overlay-fr.md` chargé, chaque finding matériel routé vers un traitement deal, price chips non chiffrés, gate France/Lux appliqué
- [ ] Sortie comprend : en-tête confidentialité + note du relecteur (5 champs) + résumé exécutif + rapport par thème + grille de matérialité + Q&A list + recommandations GAP (+ table de conversion PE si `--pe`) + question hors checklist + arbre de décision 5 options + footer A si applicable

---

## Mode Anno Desktop Optionnel

Pour une data-room autorisée, appeler `anno_health`, puis `detect`. N'utiliser `legal_ingest` que sur demande explicite d'indexation. Ensuite, `legal_search`, `legal_graph_query`, `legal_extract_contract`, `review_create`, `review_add_rows`, `review_extract` peuvent aider à relier pièces, contrats, risques et findings. Anno est une source interne de dossier, jamais une source primaire.

## Outils MCP à privilégier

Appeler les outils par leur nom exact quand le serveur `Hacienda Droit des Affaires` est disponible. Ne pas inventer de tool hors périmètre ; si une source n'a pas été consultée directement, garder `[à vérifier]`.

- Socle sources officielles : `piste_status`, `legifrance_recherche`, `legifrance_get_article`, `judilibre_recherche`, `judilibre_get_decision`, `eurlex_recherche`, `eurlex_consulter`.
- Entreprises, BODACC et procédures collectives : `company_full_profile`, `bodacc_by_siren`, `bodacc_procedures`.
- Points fiscaux et sociaux de due diligence : `bofip_rechercher`, `bofip_consulter`, `boss_recherche`, `boss_get_document`.
- Tout résultat issu d'un corpus client ou d'un outil interne reste distingué des sources primaires officielles.

## Emplacement des sorties

```
outputs/due-diligence-dataroom-<cible-slug>-YYYY-MM-DD.md
```

Si la grille de matérialité dépasse 10 lignes, générer en parallèle un dashboard
HTML autonome via `renderDashboard()` de `@hacienda/core` (sortable, filtrable,
ouvrable hors-ligne, zéro CDN, XSS-safe — voir `references/dashboard-template.md`).

---

## Sortie

### Format livrable

```
[En-tête de confidentialité selon le rôle utilisateur — voir CLAUDE.md §2]

> **⚠️ Note du relecteur**
> - **Sources :** Légifrance ✓ / Judilibre ✓ / Pappers ✓ / BODACC ✓ (cocher ✗ si non connectée)
> - **Lecture :** {N} documents de la data-room sur {N} ; thèmes couverts : {liste} {si --themes : « DD ciblée — {thèmes} non audités ; rapport partiel »} ; {fichiers illisibles le cas échéant}
> - **Signalé pour ton jugement :** {N} findings [review] | {N} documents manquants identifiés | aucun
> - **Fraîcheur :** recherche des évolutions depuis {date} — {N} mises à jour intégrées | rien trouvé
> - **Avant de t'appuyer dessus :** {1-2 actions concrètes — typiquement « obtenir les pièces de la Q&A list avant de figer la grille » OU « prêt pour relecture »}

# Résumé exécutif

{Trois phrases pour comité d'investissement / DG / sponsor business. Pas de
jargon. Une ligne bottom-line : poursuivre / poursuivre sous conditions /
suspendre. Une ligne de risque dominant (red flag le plus grave). Une ligne de
prochaine action — typiquement l'envoi de la Q&A list.}

# Rapport structuré par thème

## Étape 1 — Pré-flight

1. **`check-pii` sur l'ensemble de la data-room** — invocation obligatoire et
   **critique**. Une data-room agrège un volume massif de données sensibles ;
   le seuil B (50 identifiants OU 1+ catégorie sensible) est franchi dès les
   premiers documents (IBAN, NIR sur les contrats de travail, montants > 10k€,
   SIREN, mentions « confidentiel / secret des affaires »). Le verdict seuil B
   atteint est ici **la règle**. Présenter le prompt utilisateur
   `[continuer une fois] [ne plus demander pour ce dossier] [installer hacienda-ghost]`
   et **respecter strictement la décision** (continue / prompt / abort) avant
   toute lecture analytique. Ne jamais analyser une data-room sans ce pré-flight.
2. Lire le profil cabinet (CLAUDE.md droit-affaires, bloc M&A) et
   `~/.claude/plugins/config/hacienda-juridique/company-profile.md` : side habituel, posture DD, seuil de
   matérialité, rôle utilisateur pour l'en-tête de confidentialité.
3. Si un fichier de la data-room est illisible ou tronqué : le signaler
   explicitement dans la note du relecteur — ne pas l'omettre silencieusement.

---

## Étape 2 — Inventaire et extraction

### 2.1 Inventaire

Parcourir le dossier data-room, recenser les documents et les **classer par
thème** (1 à 7). Compter N documents au total et n par thème. Repérer d'emblée
les **catégories de documents attendues mais absentes** au regard de la grille
`references/grille-due-diligence-fr.md` (ex : pas de registre des mouvements de
titres, pas de registre des traitements RGPD) — ces absences sont des findings à
part entière (documents manquants).

### 2.2 Extraction multi-documents via `revue-tabulaire`

Pour l'extraction structurée des valeurs contractuelles sur un lot de documents
d'un même thème, **invoquer le skill V1 `revue-tabulaire`** — il est la brique
atomique d'extraction et est consommé **tel quel, sans aucune modification**.

**Comment passer la main à `revue-tabulaire` :**

- Appeler `revue-tabulaire` en lui fournissant son **intake** : le *pattern* de
  documents (le sous-ensemble de la data-room correspondant au thème, ex :
  `./data-room/02-contrats/*`) et la liste des **colonnes** à extraire, en alias
  séparés par des virgules (flag `--colonnes="parties,date-signature,changement-de-controle,..."`).

- Choisir les colonnes selon le thème audité, en s'appuyant sur les alias
  documentés dans `revue-tabulaire` (`parties`, `date-signature`,
  `date-expiration`, `durée`, `loi-applicable`, `juridiction`, `non-concurrence`,
  `exclusivite`, `resiliation`, `clause-penale`, `confidentialite`…). Exemples :
  - Thème 2 (contrats) : `parties,date-signature,date-expiration,exclusivite,resiliation,changement-de-controle`
    (`changement-de-controle` est une colonne libre — `revue-tabulaire` l'interprète
    en langage naturel ; signaler dans la note si l'interprétation est incertaine).
  - Thème 3 (social) : `parties,date-signature,non-concurrence,resiliation`.
  - Thème 1 (corporate) : `parties,date-signature` sur les PV et statuts.

**Ce que `revue-tabulaire` rend, et comment le consommer :**

- `revue-tabulaire` retourne un **tableau Markdown** (une ligne par document,
  une colonne par alias), sans attribution de criticité — il **extrait**, il
  n'analyse pas. Les cellules valent : valeur textuelle, `—` (absent),
  `⚠️ à vérifier` (présent mais illisible / contradictoire).
- `due-diligence-dataroom` **récupère ce tableau** comme matière première de
  l'étape 3 : c'est lui — et non `revue-tabulaire` — qui attribue la criticité
  🟢/🟡/🟠/🔴 à chaque valeur extraite, en appliquant la grille DD. Une cellule
  `⚠️ à vérifier` de `revue-tabulaire` devient une question de la Q&A list
  (étape 5). Une valeur extraite signalant un red flag (ex : présence d'une
  clause de changement de contrôle) devient un finding qualifié de l'étape 3.
- `revue-tabulaire` n'est **ni modifié, ni étendu** : il est consommé via son
  interface publique (intake *pattern* + colonnes → tableau). Si un thème ne se
  prête pas à une extraction tabulaire (ex : analyse d'un litige isolé), lire le
  document directement sans passer par `revue-tabulaire`.

---

## Étape 3 — Analyse par thème

Pour **chacun des 7 thèmes** (ou ceux demandés via `--themes`), appliquer la
grille `references/grille-due-diligence-fr.md` :

1. **Points de contrôle** — passer en revue les points de contrôle du thème
   contre les documents inventoriés et le tableau d'extraction de l'étape 2.
2. **Red flags** — confronter aux signaux d'alerte de la grille ; chaque red flag
   constaté devient un finding, qualifié 🟢/🟡/🟠/🔴.
3. **Documents manquants** — tout document attendu par la grille et absent de la
   data-room est un finding « document manquant » (au minimum 🟡 ; 🟠 ou 🔴 si le
   document est structurant — ex : registre des mouvements de titres).

Chaque finding subjectif (matérialité, opposabilité, suffisance d'une couverture)
porte le tag inline `[review]`. Respecter le **plancher de sévérité cross-skill** :
ne pas dégrader une criticité sans justification explicite.

### Renvois en pointeurs (thèmes 4, 5, 7)

L'analyse de **premier niveau** — recensement, red flags, documents manquants —
reste réalisée ici pour les 7 thèmes. Pour les thèmes 4, 5 et 7, l'audit
**approfondi** relève d'une expertise dédiée ; poser le pointeur **sans s'y
substituer** :

- **Thème 4 — Propriété intellectuelle** → pointeur `hacienda-propriete-intellectuelle`
  (skill `contrats-pi`) pour la validité des titres, la liberté d'exploitation,
  la chaîne de cession des droits, l'audit open source approfondi.
- **Thème 5 — Fiscal / Financier** → pointeur `hacienda-fiscal` **et
  expert-comptable** pour le chiffrage d'un risque de redressement, le régime
  des plus-values, les droits d'enregistrement. **Pas de conseil fiscal détaillé
  ici** — signalement et renvoi.
- **Thème 7 — RGPD / Conformité** → pointeur `hacienda-ghost` pour l'audit RGPD
  approfondi (analyse traitement par traitement, bases légales, transferts hors
  UE, contrôle des sous-traitants).

### Tags de provenance

- Articles cités : vérifier dans `references/articles-c-civ-c-com-index.md`.
  Citables `[Légifrance]` (LEGIARTI réel) : **1104**, **1112-1**, **1602**,
  **1626**, **1641**, **1170**, **1231-5** C.civ, **L.442-1** C.com.
- En `[a compléter]` dans l'index → tag `[à vérifier]` obligatoire : **1112**,
  **1123**, **1124** C.civ, **L.420-1**, **L.420-2** C.com.
- Articles du Code du travail (L.1224-1 transfert des contrats, L.2312-8
  information-consultation CSE) — hors index → `[à vérifier]`.
- **RGPD (règlement UE 2016/679)** : les art. 28 (sous-traitance) et 30
  (registre) sont des références UE → tag `[Eurlex]` si consulté en session,
  sinon `[à vérifier]`.
- Tag de provenance placé **après** la citation, **sans backticks dans les
  cellules de tableau** (backticks admis dans le corps narratif).

---

## Étape 4 — Grille de matérialité

Consolider tous les findings des 7 thèmes (ou des thèmes demandés) dans une
**grille de matérialité** : chaque finding classé **thème × gravité × statut**.

| # | Thème | Finding | Gravité | Statut | Matériel ? |
|---|---|---|---|---|---|
| 1 | Contrats | Clause de changement de contrôle sur contrat client clé | 🔴 | Confirmé | Oui |
| 2 | Corporate | Clause d'agrément statutaire non purgée | 🟠 | Confirmé | Oui |
| 3 | RGPD | Registre des traitements incomplet | 🟠 | Confirmé | Oui [review] |
| 4 | Contentieux | Litige prud'homal en cours, provision à vérifier | 🟠 | À documenter | Oui [review] |
| ... | ... | ... | 🟢/🟡/🟠/🔴 | ... | ... |

- **Gravité** — échelle canonique 🟢/🟡/🟠/🔴 du `CLAUDE.md §3`.
- **Statut** — `Confirmé` (établi sur pièces) / `À documenter` (suspecté, pièce
  manquante → alimente la Q&A list) / `Document manquant` (catégorie absente).
- **Matériel ?** — `Oui` / `Non` par rapport au seuil de matérialité (profil ou
  `--seuil-materialite`). Un finding non matériel reste signalé mais ne déclenche
  pas de recommandation GAP. La qualification de matérialité porte `[review]`
  dès qu'elle relève d'une appréciation.

Tri par gravité décroissante 🔴 → 🟠 → 🟡 → 🟢 ; à gravité égale, tri par thème
(1 → 7). Si la grille dépasse 10 lignes, générer en parallèle un dashboard HTML
autonome via `renderDashboard()` de `@hacienda/core` (voir
`references/dashboard-template.md`).

---

## Étape 5 — Q&A list

Générer la **liste des questions complémentaires à adresser au cédant** (*Q&A
list* / *information request list*) — l'artefact opérationnel transmis à la
partie adverse pour compléter la data-room.

Une question par ligne, alimentée par : les findings `À documenter` et
`Document manquant` de la grille, les cellules `⚠️ à vérifier` remontées par
`revue-tabulaire`, les points de contrôle non vérifiables faute de pièce.

| # | Thème | Question au cédant | Finding lié | Priorité |
|---|---|---|---|---|
| 1 | Corporate | Communiquer le registre des mouvements de titres à jour. | #2 | Haute |
| 2 | Contrats | Confirmer si le contrat client [X] a fait l'objet d'une demande de consentement au changement de contrôle. | #1 | Haute |
| 3 | RGPD | Communiquer le registre des traitements complet et les contrats de sous-traitance art. 28 RGPD. | #3 | Moyenne |
| ... | ... | ... | ... | ... |

Priorité `Haute` pour les questions liées à un finding 🔴/🟠 matériel,
`Moyenne` / `Basse` sinon. Côté cédant (*vendor DD*), la Q&A list est lue comme
les questions à anticiper et à pré-documenter dans la *disclosure*.

---

## Étape 6 — Recommandations GAP

Pour **chaque finding matériel** de la grille (étape 4), esquisser la protection
à demander dans la Garantie d'Actif et de Passif. Ce sont des **esquisses** : la
revue de la GAP elle-même relève du skill `gap-review`.

| # | Finding matériel | Gravité | Protection GAP esquissée |
|---|---|---|---|
| 1 | Clause de changement de contrôle sur contrat client clé | 🔴 | Déclaration spécifique du cédant sur les contrats à *change of control* ; condition suspensive d'obtention du consentement du cocontractant avant closing ; à défaut, garantie spécifique chiffrée. |
| 2 | Clause d'agrément statutaire non purgée | 🟠 | Condition suspensive de purge de l'agrément avant closing. |
| 3 | Litige prud'homal en cours | 🟠 | Garantie de passif social couvrant le litige, durée alignée sur la prescription ; déclaration sur l'exhaustivité des litiges. |
| 4 | Registre des traitements RGPD incomplet | 🟠 | Déclaration de conformité RGPD ; garantie spécifique données personnelles ; ou ajustement de prix si la mise en conformité est chiffrable. |

Types de protections à mobiliser : **déclarations** (le cédant affirme un fait),
**garanties** (le cédant indemnise si le fait se révèle faux ou si un passif
apparaît), **indemnisations spécifiques** (couverture chiffrée d'un risque
identifié), **conditions suspensives** (régularisation exigée avant closing),
**ajustement de prix**.

> **Lien `gap-review`.** Ces recommandations préparent la GAP ; elles ne la
> remplacent pas. Une fois le projet de GAP disponible, le passer à
> `gap-review` — son axe 5 (confrontation findings DD) consomme précisément le
> rapport de DD produit ici (`--dd-findings=./rapport-dd.md`).

---

## Étape 6bis — Overlay PE red flags (si `--pe` ou overlay accepté)

**N'exécuter que si le mode PE est actif.** Charger
`references/pe-dd-red-flags-overlay-fr.md` et dérouler les axes D1–D5 :

1. **D1 — red flag report orienté deal** : livrable court partner-ready limité aux
   findings 🔴/🟠 matériels + **table de conversion** — chaque finding routé vers un
   traitement deal (CP / déclaration-garantie GAP / specific indemnity / couverture
   W&I / price chip / Q&A), avec repli. Un finding matériel sans traitement désigné =
   DD inachevée. Grille complète (🟡/🟢 inclus) en annexe.
2. **D2 — change of control, contrats clés & concentration client** : consentements
   en CP, cumul concentration × clause, termination for convenience, exclusivités.
3. **D3 — dette existante, sûretés & cash pooling** : change of control defaults →
   waiver en CP ; chemin de mainlevée / pay-off letters ; débranchement du cash
   pooling ; substitution des garanties groupe ; assistance financière **nommée et
   renvoyée** → `/h-da:closing-checklist-fr --pe`.
4. **D4 — management, incentives & social/fiscal** : package existant →
   `/h-da:management-package-pe` ; known issues fiscal/social → specific indemnity,
   fond **nommé et renvoyé** (fiscaliste / socialiste), jamais traité.
5. **D5 — articulation W&I / disclosure / VDD** : findings identifiés = known issues
   exclus de la police (→ specific indemnity, pas couverture W&I) ; reliance letter
   vérifiée ; matrice fine police ↔ GAP → `/h-da:gap-review --pe`.

**Gate France/Lux** (cf. module partagé `references/pe-overlay-fr.md`) : entité/docs
fonds Lux → hors périmètre, renvoi conseil luxembourgeois ; l'overlay couvre la jambe
FR. **Ne jamais chiffrer** les price chips ni les passifs (`[à compléter]`) ; jalons en
semaines relatives, aucune date calendaire. Si la cible est aussi en difficulté,
l'overlay PE et la doctrine distressed **s'empilent** sans se dupliquer
(`references/distressed-overlay-fr.md`).

---

## Étape 7 — Post-flight

Appel automatique de `verifier-citations` sur la sortie complète. Les articles
C.civ / C.com. cités doivent exister dans
`references/articles-c-civ-c-com-index.md` ; à défaut, tag `[à vérifier]` et
ligne dédiée dans la note du relecteur. Les références RGPD (art. 28, 30) sont
vérifiées comme références UE, taguées `[Eurlex]` si confirmées, `[à vérifier]`
sinon. Si PISTE n'est pas configuré : mode dégradé documenté dans la note du
relecteur (« `verifier-citations` non exécuté — N citations à valider
manuellement »).

---

## Thème 1 — Corporate / Gouvernance
{Points de contrôle vérifiés, red flags constatés, documents manquants, findings + statuts}

## Thème 2 — Contrats matériels
{idem}

## Thème 3 — Social / RH
{idem}

## Thème 4 — Propriété intellectuelle
{Analyse de premier niveau + pointeur hacienda-propriete-intellectuelle}

## Thème 5 — Fiscal / Financier
{Analyse de premier niveau + pointeur hacienda-fiscal / expert-comptable}

## Thème 6 — Contentieux / Passifs
{idem}

## Thème 7 — RGPD / Conformité réglementaire
{Analyse de premier niveau + pointeur hacienda-ghost}

{Un thème non demandé via --themes : mention « Non audité — hors périmètre DD demandé. »}

# Grille de matérialité

| # | Thème | Finding | Gravité | Statut | Matériel ? |
|---|---|---|---|---|---|
| ... | ... | ... | 🔴/🟠/🟡/🟢 | ... | ... |

# Q&A list

| # | Thème | Question au cédant | Finding lié | Priorité |
|---|---|---|---|---|
| ... | ... | ... | ... | ... |

# Recommandations GAP

| # | Finding matériel | Gravité | Protection GAP esquissée |
|---|---|---|---|
| ... | ... | ... | ... |

## Overlay PE (si `--pe`) — red flags convertis en traitements deal

| # | Finding (🔴/🟠 matériel) | Thème | Traitement deal recommandé | Repli | Renvoi |
|---|---|---|---|---|---|
| ... | ... | ... | CP / GAP / W&I / specific indemnity / price chip `[à compléter]` / Q&A | ... | ... |

- Renvois PE : {spa-review --pe / gap-review --pe / management-package-pe / closing-checklist-fr --pe}

# Une question hors de ma checklist habituelle

{Observation transversale qu'un relecteur attentif ferait. Omettre la ligne si
rien d'honnête à dire — ne pas fabriquer.}

# Que veux-tu faire ? Choisis une option et je la déroule :

1. **Rédiger** — je produis le rapport de DD consolidé pour comité d'investissement, ou la Q&A list mise en forme prête à être adressée au cédant.
2. **Escalader** — note d'escalade vers {approbateur SPA configuré} avec les findings 🔴 / 🟠 matériels, le risque dominant et la décision attendue avant de poursuivre le deal.
3. **Compléter les faits** — j'envoie la Q&A list au cédant et je consolide la grille de matérialité dès réception des pièces complémentaires.
4. **Surveiller et attendre** — j'ajoute le dossier de DD au tracker du deal avec note motivée et date de revisite (réception des pièces, signing, expiration d'exclusivité).
5. **Autre** — précise ce que tu veux en faire.

{Footer A — si check-pii est passé en mode passif sous le seuil B (rare sur une data-room) :
[Ce skill a traité {N} mentions identifiantes. Pour anonymiser automatiquement avant envoi à Claude, installer hacienda-ghost.](https://hacienda.diy/ghost)
Sinon, rien.}
```

### Mode silencieux (livrable externe)

Si la sortie est destinée à un comité d'investissement, un sponsor business
non-juriste, la contrepartie ou un conseil tiers :

- Conserver l'en-tête de confidentialité (si le destinataire est dans le
  périmètre du secret) et la note du relecteur.
- Retirer la narration de skill et les renvois inter-commandes (les placer dans
  un message séparé).
- La Q&A list adressée au cédant est un livrable externe : en retirer la colonne
  « Finding lié » (interne) et l'en-tête de confidentialité (destinataire hors
  périmètre du secret).
- Le livrable doit se lire comme s'il avait été rédigé par un associé M&A.

---

## Ce skill ne fait pas

- Revue de la GAP elle-même → `gap-review` (les findings de DD alimentent son axe 5).
- Revue ou rédaction de la LOI / du term sheet → `loi-term-sheet`.
- Revue ou rédaction du SPA / acte de cession → `reviser-contrat` (tronc commercial) ou skill SPA dédié.
- Analyse de fond d'un pacte d'associés → `pacte-associes-review`.
- Audit PI approfondi → `hacienda-propriete-intellectuelle` (le thème 4 reste un recensement de premier niveau).
- Audit fiscal approfondi et conseil fiscal → `hacienda-fiscal` + expert-comptable (le thème 5 reste un recensement de premier niveau).
- Audit RGPD approfondi → `hacienda-ghost` (le thème 7 reste un recensement de premier niveau).
- Extraction tabulaire brute multi-documents → `revue-tabulaire` (consommé comme brique, non remplacé).
- Anonymiser réellement les données de la data-room — `check-pii` détecte et alerte, `hacienda-ghost` anonymise.
- Valider, signer ou exécuter l'opération (acte des parties + approbateur configuré).
- **Chiffrer** les price chips, passifs ou redressements en mode `--pe` (`[à compléter]`, équipe financière / fiscaliste).
- Traiter au fond le fiscal/social d'un management package ou d'un contrôle en cours en mode `--pe` (nommé et renvoyé).
- Souscrire ou placer la police W&I en mode `--pe` (articulation signalée, matrice fine → `gap-review --pe`).

---

## Ton

Technique, structuré, factuel. **Side-dépendant** : côté acquéreur, la DD
cherche les expositions et prépare les protections GAP à exiger ; côté cédant
(*vendor DD*), elle anticipe les findings de l'acquéreur et prépare la
*disclosure*. Distinguer nettement ce qui est **établi sur pièces** de ce qui
est **suspecté faute de pièce** (statut `À documenter` → Q&A list). Les
documents manquants sont des findings à part entière, jamais une omission
silencieuse. Les renvois PI / fiscal / RGPD sont des **pointeurs** : l'analyse
de premier niveau est rendue ici, l'expertise approfondie est renvoyée — ne pas
prétendre faire l'audit complet de ces trois thèmes. La sortie est un brouillon
de DD préliminaire soumis à validation humaine (avocat) M&A : elle oriente la négociation
et la GAP, elle ne les remplace pas.
