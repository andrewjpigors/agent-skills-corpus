---
name: qualification-oeuvre
description: >
  Qualification juridique d'une création au regard du droit d'auteur français
  (CPI Livre I) structurée en V2 : originalité, catégorie, titularité
  initiale, conséquences de droits et de durée, puis routage vers la brique
  spécialisée suivante. Point d'entrée du bloc droit d'auteur. Ne rédige PAS
  de contrat de cession ou de licence, ne traite PAS la chaîne de droits
  logiciel/data en revue globale, et ne qualifie PAS la contrefaçon.
argument-hint: "[description œuvre | nature | contexte création | objectif préventif/défensif/contentieux]"
version: "2.0.0"
authors: ["Hacienda"]
tags: [droit-auteur, qualification, originalite, titularite, preuve, CPI]
---

# Qualification œuvre V2

> **Qualification juridique ≠ avis d'opportunité.** Ce skill produit une
> **analyse de qualification** pour aider l'avocat spécialisé en propriété
> littéraire et artistique. Il NE conclut PAS à l'existence ou à la
> non-existence du droit d'auteur (= rôle du juge, in fine), NE rédige PAS un
> contrat de cession ou de licence (= `cession-droit-auteur` V4.1 /
> `licence-droit-auteur` V4.1), NE qualifie PAS une contrefaçon (=
> `contrefacon-droit-auteur` V4.2). Le droit d'auteur **naît automatiquement à
> la création** (CPI L.111-1) sans formalité de dépôt — mais la **preuve de la
> date de création et de l'identité de l'auteur** reste critique en cas de
> litige (cf. `depot-preuve-creation` : mode `open` pour `Evidence Register`
> et `Proof Gaps`, puis mode
> `timeline` si une chronologie doit être ordonnée).

> **Règle de bascule — logiciel/data.** Si la question principale porte
> d'abord sur la **titularité**, les **contributeurs**, les **datasets**,
> les **licences entrantes** ou une **due diligence** logiciel/data, ouvrir
> `revue-logiciel-donnees`. Dans cette configuration, `qualification-oeuvre`
> sert seulement à qualifier l'**originalité** et le **régime juridique**
> de chaque composant pertinent.

> **Aide-mémo V2.**
> `references/qualification-oeuvre-routing-and-output.md` résume le routage et
> les blocs de sortie. En cas d'écart, seul ce `SKILL.md` fait foi.

## Examples

<example>
<user>/h-pi:qualification-oeuvre [description œuvre | nature | contexte création | objectif préventif/défensif/contentieux]</user>
<response>
Brouillon de travail structuré, avec faits, droit, analyse, incertitudes, sources consultées, points `[à vérifier]` et validation humaine obligatoire.
</response>
</example>

## Chargement du profil

Avant tout travail substantiel, lire :

1. `~/.claude/plugins/config/hacienda-juridique/company-profile.md`
2. `~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/CLAUDE.md`

Si le profil est absent, incomplet ou contient `[A CONFIGURER]`, demander `/h-pi:entretien-demarrage` et garder les marqueurs `[à vérifier]` visibles.

## Intake

Identifier au minimum : demande, actif ou droit concerné, parties, territoire, dates utiles, documents disponibles, source officielle à consulter, urgence, sortie attendue et niveau de validation humaine requis.

## Gate non-juriste

Si l'utilisateur n'est pas juriste ou avocat, produire une explication opérationnelle, signaler les limites, refuser toute conclusion présentée comme avis juridique final et demander validation par un professionnel habilité avant usage externe.

## Outils MCP à privilégier

Appeler les outils par leur nom exact quand le serveur `Hacienda Propriété Intellectuelle` est disponible. Ne pas inventer de tool hors périmètre ; si une source ou un registre n'a pas été consulté directement, garder `[à vérifier]`.

- Socle textes, jurisprudence et droit UE : `piste_status`, `legifrance_recherche`, `legifrance_get_article`, `judilibre_recherche`, `judilibre_get_decision`, `eurlex_recherche`, `eurlex_consulter`.
- Dessins et modèles, droit d'auteur, logiciels, bases de données et droits voisins : utiliser le socle officiel ci-dessus ; les registres spécialisés non exposés par le serveur restent `[à vérifier]` ou traités via preuve/document client autorisé.
- Anno, quand disponible, reste une source interne de dossier : jamais un registre officiel INPI, EUIPO, OEB, OMPI ou BOPI.

## Emplacement des sorties

Écrire les livrables dans le dossier de pratique ou de dossier configuré : `~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/outputs/` ou `~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/matters/<slug-dossier>/outputs/`.

## Sortie

Structurer la sortie avec : faits retenus, droit applicable, analyse, incertitudes, sources consultées, décisions proposées, prochaine action et validation humaine. Toute source non consultée directement reste `[à vérifier]`.

## Exemples

```
/h-pi:qualification-oeuvre "Roman littéraire 320 pages — auteur personne physique seule — édition envisagée chez éditeur tiers — objectif préventif"
```

```
/h-pi:qualification-oeuvre "Logiciel SaaS B2B développé par équipe de 4 développeurs salariés — code source + interface graphique + base de données utilisateurs — objectif préventif avant levée de fonds"
```

```
/h-pi:qualification-oeuvre "Contenu marketing — vidéo publicitaire 30 sec commandée à agence externe — diffusion TV + web prévue — objectif préventif avant lancement campagne"
```

(Le skill demandera la description, le contexte de création, la date, les preuves disponibles et l'objectif.)

---

## QUALIFICATION JURIDIQUE, PAS AVIS D'OPPORTUNITÉ

**Reformuler en tête de chaque output. Ne jamais l'enlever. Ne jamais l'adoucir.**

> **Qualification juridique, pas avis d'opportunité.** Ce skill produit une
> analyse de qualification au regard du droit d'auteur français — il
> identifie les critères d'originalité (L.111-1 + jurisprudence CJUE
> Infopaq), la catégorie applicable (L.112-2 — liste non exhaustive), le cas
> de titularité initiale (7 cas exhaustifs), le partage droits patrimoniaux
> vs droit moral, la durée de protection, et les enjeux selon l'objectif
> (préventif / défensif / contentieux). Il NE conclut PAS à l'existence ou
> à l'inexistence du droit d'auteur sur l'œuvre concrète — c'est le **juge**
> qui tranche in fine, après contestation, sur la base de la preuve apportée
> par les parties. Le droit d'auteur naît automatiquement à la création sans
> formalité de dépôt (CPI L.111-1), mais la qualification reste un exercice
> juridique nécessitant validation par un avocat spécialisé en propriété
> littéraire et artistique avant tout acte (exploitation, cession,
> contestation, action en contrefaçon). Une qualification erronée porte des
> conséquences à sens unique : cession invalide, action contrefaçon mal
> fondée (déboutement + dépens + risque concurrence déloyale), violation
> droit moral non anticipée (action en cessation + dommages-intérêts).

C'est le garde-fou le plus visible du skill. Sous-qualifier l'originalité =
porte à sens unique (exploitation engagée, cession signée, dépôt fait sans
mesures de preuve). Sur-qualifier = porte à 2 sens, l'avocat affine.
Rester sur la porte à 2 sens.

---

## Charger le profil pratique avant de commencer

Avant tout, lire :
1. `~/.claude/plugins/config/hacienda-juridique/company-profile.md`
2. `~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/CLAUDE.md`

Récupérer :
- **Rôle** depuis `## 1. Profil cabinet et profil de pratique PI` (avocat
  inscrit au barreau / juriste interne / non-juriste — change l'en-tête de
  confidentialité ET le périmètre du secret professionnel). Le droit d'auteur
  relève du droit commun de la propriété littéraire et artistique — il N'EXISTE
  PAS de profession réglementée « mandataire en droit d'auteur » équivalente au
  mandataire INPI marques ou OEB brevets. Le rôle pertinent est donc **avocat
  spécialisé en propriété littéraire et artistique** (ou à défaut PI générale).
- **Secteurs des clients dominants** (édition / audiovisuel / logiciel / design
  / mode / publicité / multimédia / transversal — calibre les exemples et la
  vigilance sur les régimes spéciaux : L.113-9 logiciels, L.113-7 audiovisuel,
  L.132-36 journalistes, L.341-1 bases de données).
- **Posture conseil par défaut** (préventif vs réactif — calibre le ton :
  préventif = anticipation contractuelle, réactif = analyse défensive d'une
  contestation ou préparation contentieuse).
- **Matrice d'approbateurs** pour les escalades (avocat spécialisé PI / GC /
  Direction selon enjeu).

Ce skill ne conclut JAMAIS « œuvre protégée par le droit d'auteur » ni
« titularité acquise sans contestation possible » — il identifie les critères
applicables et les zones de risque.

Si le profil contient `[A CONFIGURER]`, surfacer :

> Le profil pratique n'est pas configuré — c'est ce qui adapte la posture, les
> secteurs, et la chaîne d'approbation à ta pratique. Tu peux continuer en
> mode provisoire (réponses génériques taguées `[non configuré]`) ou lancer
> `/h-pi:entretien-demarrage` (10 à 15 minutes).

---

## Contrat d'entrée V2

Avant les 5 questions, expliciter ces 3 dimensions :

- `objective_mode`: `preventive`, `défensive`, `litigation-prep`
- `work_type`: `text`, `image`, `music`, `audiovisual`, `software`,
  `database`, `design`, `mixed-media`, `other`
- `creation_context`: `single-author`, `collaboration`, `collective`,
  `composite`, `employee`, `commissioned`, `posthumous`, `unclear`

Champs de faits à exposer ensuite :

- `work_description`
- `creation_facts`
- `evidence_status`
- `suspected_category`
- `business_trigger`

Tout fait, pièce, date ou qualification non contrôlé reste `[à vérifier]`.

---

## Cadrage initial V2 — 5 questions en batch unique

Avant toute analyse, poser les 5 questions ci-dessous **en une seule fois**.
Ne pas dérouler le flux de travail tant que les réponses ne sont pas obtenues — ou
explicitement marquées « non applicable » par l'utilisateur.

**1. Description de l'œuvre**
- **Nature** : texte / image / musique / vidéo / logiciel / design / multimédia
  / autre
- **Forme tangible** : manuscrit / fichier numérique (préciser format) /
  partition / maquette / code source (préciser langage) / autre
- **Description précise** (objet, contenu, finalité — viser ≥ 30 mots ; si
  description vague, push pour précision : « pour qualifier l'originalité
  sérieusement, j'ai besoin de comprendre les choix créatifs concrets — peux-tu
  décrire l'œuvre plus en détail ? »)

**2. Contexte de création**
- **Créateur(s)** : personne physique seule / plusieurs personnes physiques
  (préciser nombre et rôles)
- **Commande** : oui / non ; si oui, par qui (client externe / employeur /
  personne morale) et selon quel cadre contractuel (devis signé / contrat de
  commande explicite / mail informel / rien d'écrit)
- **Salariat** : oui / non ; si oui, fonctions du salarié (la création
  relève-t-elle de ses **fonctions habituelles** définies au contrat de
  travail ou de la fiche de poste, ou bien a-t-elle été créée **hors fonctions**
  voire sur temps personnel ?) — distinction critique pour L.113-9 (logiciels)
  et pour le régime salarié droit commun.
- **Collaboration** : plusieurs créateurs avec apports identifiables et
  séparables (œuvre de collaboration L.113-2 al.1) ? Apports fusionnés sans
  séparation possible (indice œuvre de collaboration unitaire ou œuvre
  collective selon initiative) ?
- **Œuvre collective** : initiative + édition + diffusion sous le nom d'une
  personne morale (encyclopédie, dictionnaire, périodique, site web
  institutionnel) ? Critère cumulatif L.113-2 al.3.

**3. Date de création + preuves disponibles**
- **Date de création** : YYYY-MM-DD ou approximation (préciser fourchette
  si incertain — « début 2024 », « courant T2 2025 »)
- **Preuves disponibles** : manuscrits horodatés / mails datés contenant
  fichiers attachés / dépôts copyright.fr / constat d'huissier ou commissaire
  de justice / enveloppe Soleau INPI (déposée — date à confirmer) / dépôt
  notarié / publication antérieure horodatée / aucune preuve formelle
- Si **aucune preuve formelle**, signaler immédiatement : « la qualification
  est possible, mais en cas de litige tu auras besoin de constituer la preuve
  de date — je le note en recommandation de fin et je peux ouvrir
  `depot-preuve-creation` ensuite : mode `open` pour `Evidence Register` et
  `Proof Gaps`, puis `timeline` si une `Timeline` doit être reconstituée. »

**4. Catégorie suspectée** (référence non exhaustive L.112-2)
- Littéraire / artistique (peinture, sculpture, dessin, photographie) /
  musicale / audiovisuelle (cinéma, télévision, vidéo) / logicielle / base de
  données (structuré et/ou contenu) / design (arts appliqués) / dramatique /
  chorégraphique / graphique / typographique / multimédia (composition de
  plusieurs catégories) / autre
- En cas d'œuvre hybride (ex : site web = design + texte + logiciel +
  éventuellement musique), lister TOUTES les catégories applicables — le
  régime juridique peut différer par composant.

**5. Objectif de la qualification**
- **Préventif** : avant exploitation / diffusion / cession / dépôt produit —
  on veut sécuriser titularité, anticiper les cessions nécessaires, planifier
  les clauses droit moral.
- **Défensif** : contestation reçue d'un tiers (lettre, mise en demeure,
  action) — on veut établir notre titularité, l'originalité de l'œuvre,
  l'absence d'antériorité tierce.
- **Contentieux** : action en contrefaçon en préparation contre un tiers —
  on prépare le dossier, on évalue les preuves de date et de titularité,
  on identifie les droits violés.

L'objectif **change l'orientation finale du livrable** : le squelette
d'analyse reste identique (étapes 1 à 5), mais l'étape 6 « Enjeux identifiés »
et la section « Recommandations » sont calibrées différemment.

Si l'utilisateur ne sait pas trancher entre 2 objectifs, demander : « décris
le déclencheur — qu'est-ce qui t'amène à qualifier cette œuvre maintenant ? »

---

## Limites de routage V2

### Router vers `revue-logiciel-donnees`

Basculer si le sujet principal devient :

- la titularité sur code, repo, dataset, base, contributions ou fondateurs ;
- la chaîne de droits sur un actif logiciel/data ;
- la revue des pièces contractuelles permettant d'exploiter, céder, licencier
  ou lever des fonds.

Dans ce cas, `qualification-oeuvre` reste limité à l'originalité ou au régime
 de certains composants, sans absorber la revue globale de chaîne de droits.

### Router vers `depot-preuve-creation`

Basculer si le point bloquant principal est :

- la preuve de date ;
- la preuve de paternité ;
- la timeline ;
- le registre de pièces ;
- le bundle probatoire ou les `Proof Gaps`.

### Router vers `cession-droit-auteur`

Basculer si la qualification est suffisante et que le besoin devient la
 rédaction d'une cession.

### Router vers `licence-droit-auteur`

Basculer si la qualification est suffisante et que le besoin devient la
 rédaction d'une licence.

### Router vers `contrefacon-droit-auteur`

Basculer si la question dominante devient contradictoire :

- reprise alléguée ;
- comparaison des similitudes ;
- accès à l'œuvre ;
- action ou défense en contrefaçon.

### Rester dans `qualification-oeuvre`

Rester ici si la question dominante est encore :

- l'originalité ;
- la catégorie d'œuvre ;
- la titularité initiale ;
- la conséquence en droits moraux / patrimoniaux / durée ;
- le bon skill suivant à ouvrir.

---

## Étape 1 — Analyse de l'originalité (L.111-1 + CJUE Infopaq)

C'est le **cœur** de la qualification. Sans originalité = pas de droit d'auteur,
quelle que soit la qualité de l'œuvre, son utilité ou sa valeur marchande.

### Critère central

> **CPI L.111-1** : « L'auteur d'une œuvre de l'esprit jouit sur cette œuvre,
> du seul fait de sa création, d'un droit de propriété incorporelle exclusif
> et opposable à tous. »
>
> **Critère central de la jurisprudence française** : « l'œuvre porte la
> marque de la personnalité de son auteur » (Cour de cass. 1re civ., formule
> classique reprise dans de nombreuses décisions).
>
> **Reformulation européenne harmonisante** : **CJUE Infopaq C-5/08 (16 juillet
> 2009)** — « création intellectuelle propre à son auteur ». La directive
> 2001/29/CE sur le droit d'auteur dans la société de l'information est
> interprétée par la CJUE comme imposant un critère d'originalité
> autonome au droit de l'Union, applicable à toutes les œuvres relevant des
> droits harmonisés (reproduction, communication au public, distribution).
>
> L'originalité s'apprécie **au cas par cas**, en fonction des choix créatifs
> réellement opérés par l'auteur. **Pas de seuil minimal absolu** (une œuvre
> très courte peut être originale) ni de notion de « qualité artistique » :
> la jurisprudence rappelle régulièrement que **le juge ne porte pas
> d'appréciation esthétique** (principe de neutralité du juge en matière
> artistique — formule récurrente : « il n'appartient pas au juge de porter
> une appréciation sur la valeur artistique de l'œuvre »).

### Exemples par catégorie

**Œuvres dont l'originalité est généralement contestable** :
- **Annuaire téléphonique** (compilation alphabétique mécanique) → pas
  d'originalité par lui-même au sens du droit d'auteur (peut éventuellement
  bénéficier du droit sui generis sur les bases de données L.341-1 si
  investissement substantiel — régime distinct).
- **Photographie simple de catalogue** (produit cadré frontalement sur fond
  neutre) → originalité contestable si aucune mise en scène, aucun choix
  d'éclairage, d'angle, de cadrage personnels. La CJUE (Painer C-145/10) a
  toutefois rappelé que même une photographie documentaire peut être
  originale si l'auteur a exercé des choix libres.
- **Formulaire standard** (déclaration d'impôt, formulaire administratif) →
  généralement pas d'originalité, fonctionnel et imposé.
- **Liste d'ingrédients d'une recette** (l'arrangement créatif du texte
  qui présente la recette peut être original ; la liste brute non).

**Œuvres dont l'originalité est généralement présumée** :
- **Œuvre littéraire** (roman, essai, nouvelle, poésie) → présomption forte
  dès qu'il y a écriture personnelle.
- **Œuvre cinématographique / audiovisuelle** → présomption forte
  (succession de choix : scénario, montage, dialogues, prises de vue).
- **Logiciel** → critère reformulé par Cour de cass. 1re civ. 7 mars 1986
  (Pachot) : « effort personnalisé allant au-delà de la simple mise en
  œuvre d'une logique automatique et contraignante ». Voir aussi
  CJUE BSA C-393/09 (2010) sur le statut de l'interface graphique (non
  protégée par le droit d'auteur logiciel mais éventuellement protégée par
  le droit d'auteur général).
- **Œuvre musicale** → présomption d'originalité forte sauf reprise pure
  (la combinaison mélodie + harmonie + rythme suffit généralement).
- **Œuvre de design** → originalité reconnue si choix créatifs au-delà de
  la fonction technique pure (CJUE Cofemel C-683/17 (2019) : le critère
  d'originalité au sens du droit d'auteur est autonome et ne dépend pas d'un
  critère esthétique — cumul possible avec dessin et modèle enregistré).

### Tests pratiques pour évaluer l'originalité (à appliquer au cas concret)

1. **Test des choix libres vs choix techniques imposés** : le créateur a-t-il
   pu opérer des **choix libres** (forme, structure, expression, agencement,
   couleurs, mots) ? Ou tous les choix étaient-ils dictés par une **contrainte
   technique** (norme à respecter, format imposé, fonction unique possible) ?
   Plus les choix sont libres, plus l'originalité est probable.

2. **Test de l'identifiabilité** : l'œuvre est-elle **reconnaissable** par
   rapport à d'autres créations du même genre ? Un lecteur averti pourrait-il
   distinguer cette œuvre d'une production banale du même secteur ? Cette
   « empreinte personnelle » est un indice d'originalité.

3. **Test de l'effort intellectuel créatif** : y a-t-il un **effort
   intellectuel personnel** au-delà de la simple **compilation mécanique** ou
   de la **production automatique** (génération aléatoire pure, mise en page
   automatique sans choix éditorial) ? Ce test élimine les productions
   purement mécaniques ou automatiques.

### Verdict

- **🟢 Originalité probable** : oui aux 3 tests. L'œuvre porte clairement
  l'empreinte de choix créatifs personnels.
- **🟡 Originalité à argumenter** : résultats mixtes (par exemple choix libres
  oui mais identifiabilité faible ; ou effort intellectuel oui mais sur fond
  de contrainte technique forte). Il faut **construire l'argumentation
  juridique** en s'appuyant sur les éléments concrets de choix créatifs.
- **🔴 Originalité douteuse** : non aux 3 tests. Création strictement
  utilitaire, mécanique, ou imposée par les contraintes techniques. Le droit
  d'auteur est probablement inapplicable ; envisager d'autres régimes (droit
  sui generis bases de données, dessin et modèle, concurrence déloyale).

**Sortie de l'étape 1** : verdict 🟢/🟡/🔴 + 2-3 lignes de justification
basée sur l'application concrète des 3 tests à l'œuvre analysée (pas une
récitation des règles — un raisonnement appliqué).

> **Note** : ce verdict est une **appréciation prima facie** pour orienter
> l'analyse — il ne préjuge pas de la décision d'un juge sur le fond, qui
> peut diverger sur la base d'éléments de preuve supplémentaires apportés
> par les parties. Tag `[review]` systématique sur les cas 🟡.

---

## Étape 2 — Catégorie L.112-2 (liste NON exhaustive)

L'article L.112-2 du CPI énumère les catégories d'œuvres protégeables.
**Cette liste est explicitement non exhaustive** (« sont considérées
notamment comme œuvres de l'esprit … ») : toute création **originale**, même
ne relevant d'aucune catégorie listée, est protégeable dès lors que les
critères de l'originalité (étape 1) sont remplis.

### Catégories principales

| Catégorie | Exemples typiques | Régime |
|---|---|---|
| **Littéraires** | Livres, brochures, articles, manuels, conférences, allocutions, sermons, plaidoiries | Droit commun |
| **Artistiques** | Peintures, sculptures, dessins, photographies (originales), illustrations, cartes géographiques, gravures, lithographies | Droit commun |
| **Musicales** | Compositions avec ou sans paroles | Droit commun (interaction droits voisins L.211-1+) |
| **Dramatiques / chorégraphiques / pantomimes** | Pièces de théâtre, ballets, mimes | Droit commun |
| **Cinématographiques + audiovisuelles** | Films, séries, documentaires, vidéos | L.113-7 — œuvre de collaboration ; présomption d'auteurs : scénariste, adaptateur, dialoguiste, auteur des compositions musicales spécialement créées, réalisateur |
| **Graphiques / typographiques** | Œuvres typographiques, calligraphies, créations graphiques | Droit commun |
| **Arts appliqués (design)** | Mobilier, mode, objets, packaging | Droit commun + cumul possible avec dessin et modèle enregistré (cf. CJUE Cofemel) |
| **Logiciels** | Code source + code objet + matériel de conception préparatoire | **Régime spécial** — L.113-9 (titularité employeur si salarié dans ses fonctions) ; protection de l'expression du code, pas des idées / algorithmes ; si le sujet principal devient la chaîne de droits logiciel/data (titularité, contributeurs, datasets, bases, licences entrantes, due diligence), basculer vers `revue-logiciel-donnees` |
| **Multimedia** | Sites web créatifs, applications interactives, jeux vidéo | **Régime hybride** — composition de plusieurs catégories ; pas de qualification unifiée par la jurisprudence (jeux vidéo : Cour de cass. 25 juin 2009 retient une qualification distributive) |
| **Bases de données** | Bases structurées de données | **Double protection possible** : (a) droit d'auteur sur la **structure** originale (L.112-3) ; (b) droit sui generis sur le **contenu** L.341-1 si investissement substantiel — régime distinct durée 15 ans renouvelable (L.342-5) |
| **Traductions / adaptations / arrangements** | Œuvres dérivées | Œuvre composite (L.113-2 al.2) — protégée mais sous réserve des droits de l'œuvre préexistante |

**Note critique** : la qualification de **catégorie** détermine souvent le
**régime de titularité** (cas C ci-après pour l'audiovisuel L.113-7 ; cas F
spécial pour le logiciel L.113-9 ; cas spécial L.132-36 pour les œuvres
journalistiques en convention collective). Ne pas se contenter d'une
catégorie générale — pousser jusqu'au régime spécial le cas échéant.

> **Œuvres hybrides** : pour un livrable composite (ex : site web =
> design graphique + textes + code + base de données + éventuellement
> musique d'ambiance), lister **toutes les catégories applicables** et
> qualifier chaque composant séparément si les régimes diffèrent. La
> qualification globale d'« œuvre multimédia » n'évacue PAS la nécessité
> de qualifier le composant logiciel sous L.113-9 si pertinent.

---

## Étape 3 — Titularité initiale (7 cas exhaustifs A à G)

**Règle générale** (L.111-1) : la titularité naît automatiquement sur la tête
de **l'auteur personne physique**, du seul fait de la création. Les cas
suivants déclinent cette règle selon le contexte de création.

### Cas A — Créateur personne physique unique

**Configuration** : une seule personne physique a créé l'œuvre, hors commande
et hors salariat.

**Titularité** :
- **Droits patrimoniaux** : dévolus au créateur (L.111-1).
- **Droit moral** : dévolu au créateur (L.121-1) — perpétuel, inaliénable,
  imprescriptible.
- **Présomption L.113-1** : « la qualité d'auteur appartient, sauf preuve
  contraire, à celui ou à ceux sous le nom de qui l'œuvre est divulguée » —
  la mention du nom de l'auteur sur l'œuvre crée une présomption simple.

**Cas le plus simple. Risques** : aucun majeur, sauf preuve de date si
contestation ultérieure de l'antériorité.

### Cas B — Œuvre de collaboration (L.113-2 al.1)

**Configuration** : plusieurs personnes physiques ont participé à la création
de l'œuvre, avec des apports créatifs identifiables (mais l'œuvre est
exploitée comme un tout).

**Titularité** :
- **Cotitularité** entre les coauteurs (L.113-3).
- Répartition des droits proportionnelle aux contributions — **présomption
  d'égalité** faute de preuve contraire (souvent égalitaire en pratique).
- Chaque coauteur peut **faire valoir ses droits sur sa contribution
  distincte** si elle est séparable et exploitable indépendamment (L.113-3
  al.4) — sous réserve de ne pas porter préjudice à l'exploitation de
  l'œuvre commune.
- **Exploitation de l'œuvre commune** : requiert **l'accord de tous les
  coauteurs** (unanimité) — **risque majeur de blocage** en cas de
  désaccord ; en cas de litige, le juge tranche (L.113-3 al.3).

**Exemples** : livre coécrit (deux auteurs au nom indiqué), scénario écrit à
plusieurs mains, composition musicale en duo (musique + paroles).

**Risque critique** : **absence de pacte d'auteurs** dès le démarrage du
projet — proposer systématiquement la rédaction d'un pacte de coauteurs
définissant clés de répartition, modalités d'exploitation, gestion des
décisions, sortie d'un coauteur. (Renvoi vers `cession-droit-auteur` V4.1
pour la rédaction.)

### Cas C — Œuvre collective (L.113-2 al.3 et L.113-5)

**Configuration cumulative — 3 critères** :
1. L'œuvre est créée à l'**initiative** d'une personne physique ou morale ;
2. Cette personne **édite, publié et diffuse** l'œuvre **sous sa direction
   et son nom** ;
3. Les contributions individuelles **se fondent dans l'ensemble**, sans qu'il
   soit possible d'attribuer à chaque contributeur un droit distinct sur sa
   part.

**Titularité** :
- **Exception majeure au droit commun L.111-1** : la **personne morale (ou
  physique) commanditaire** est **titulaire ab initio** des droits sur
  l'œuvre collective (L.113-5).
- Les contributeurs individuels ne peuvent **pas** revendiquer un droit
  d'auteur individuel sur leur contribution à l'œuvre collective (sauf si
  cette contribution est exploitée séparément avec leur accord).

**Exemples typiques** : encyclopédies (Larousse, Universalis), dictionnaires,
anthologies, périodiques (journaux, magazines), sites web institutionnels
créés par une équipe sous direction éditoriale d'une entreprise, bases de
données rédactionnelles.

**Vigilance** : la qualification « œuvre collective » est **souvent invoquée
à tort** par les employeurs pour éviter de payer une cession de droits aux
contributeurs. La jurisprudence est **stricte** : il faut prouver les 3
critères cumulatifs, en particulier la **fusion** des contributions (Cour de
cass. 1re civ., décisions récurrentes refusant la qualification quand les
contributions restent identifiables).

### Cas D — Œuvre composite (L.113-2 al.2)

**Configuration** : œuvre nouvelle dans laquelle est **incorporée** une
œuvre préexistante, **sans la collaboration** de son auteur.

**Titularité** :
- L'auteur de l'œuvre composite est **titulaire de droits sur l'œuvre
  composite** (L.113-4).
- **MAIS** sous **réserve des droits de l'auteur de l'œuvre préexistante** :
  l'incorporation requiert l'autorisation préalable du titulaire des droits
  de l'œuvre préexistante (sauf exception L.122-5).

**Exemples** : adaptation cinématographique d'un roman, traduction d'un
texte, arrangement musical, remix, sample musical, mashup, recueil d'œuvres
préexistantes commentées.

**Risque critique** : **chaîne de droits cassée** si l'autorisation
préalable de l'auteur préexistant n'a pas été obtenue ou est mal documentée
— l'œuvre composite peut être qualifiée de contrefaçon, peu importe son
originalité propre. Vérifier systématiquement la chaîne de cessions amont.

### Cas E — Œuvre de commande

**Configuration** : œuvre créée par un créateur (personne physique
indépendante, freelance, agence) à la demande d'un commanditaire (personne
physique ou morale).

**Titularité — règle clé** :
- Le commanditaire **ne reçoit PAS automatiquement** les droits
  patrimoniaux. Le **créateur reste titulaire** tant qu'aucune cession écrite
  conforme n'a été conclue.
- **Cession écrite obligatoire** — formalisme L.131-3 al.1 : « la
  transmission des droits de l'auteur est subordonnée à la condition que
  chacun des droits cédés fasse l'objet d'une mention distincte dans l'acte
  de cession et que le domaine d'exploitation des droits cédés soit délimité
  quant à son **étendue** et à sa **destination**, quant au **lieu** et
  quant à la **durée** ».
- 5 mentions obligatoires cumulatives : (a) **énumération** droit par droit
  des prérogatives cédées (reproduction, représentation, adaptation,
  traduction…), (b) **étendue** et **destination** d'exploitation, (c)
  **lieu** (territoires), (d) **durée**, (e) **rémunération** (en principe
  proportionnelle L.131-4, forfait dérogatoire dans les cas listés).
- À défaut d'une seule de ces mentions, la cession peut être déclarée
  **nulle** par le juge — totalement ou partiellement.

**Erreur fréquente** : une agence de communication livre un logo à un client
sur la base d'un devis signé sans clause de cession explicite. Le client
suppose la cession implicite « j'ai payé donc c'est à moi ». **Faux** : le
créateur reste titulaire, peut s'opposer à toute utilisation au-delà de la
livraison initiale (rebranding, déclinaisons, support nouveau, exploitation
internationale), et peut même demander réparation pour exploitation non
autorisée.

**Sécurisation** : exiger un **contrat de cession explicite L.131-3 conforme**
avant toute exploitation — la simple facture, le simple devis, le mail
informel ne suffisent jamais.

### Cas F — Œuvre de salarié

**Configuration** : œuvre créée par un salarié dans le cadre de son contrat
de travail.

**Titularité — règle clé contre-intuitive** :
- **Régime de droit commun** : le **salarié reste titulaire** des droits
  d'auteur, même si l'œuvre a été créée dans l'exercice de ses fonctions et
  sur le temps de travail (CPI L.111-1 — exception au principe Code du
  travail selon lequel l'employeur est propriétaire du travail du salarié).
- Cette règle est **contre-intuitive** pour beaucoup d'employeurs : la
  qualification de salarié **n'emporte PAS** cession automatique des droits
  d'auteur. **Une cession écrite L.131-3 reste nécessaire**.

**Exceptions au droit commun** (cession ou titularité directe au profit de
l'employeur) :
- **Logiciels (L.113-9)** : les droits patrimoniaux sur le logiciel créé
  par un ou plusieurs employés **dans l'exercice de leurs fonctions ou
  d'après les instructions de leur employeur** sont **dévolus à l'employeur**
  directement (régime dérogatoire). Le droit moral reste sur le salarié.
  **Vigilance** : cette dévolution ne couvre PAS les créations hors
  fonctions (week-end, projet personnel non lié, contribution open source
  personnelle) — la frontière « dans l'exercice des fonctions » est
  appréciée concrètement (lien avec les missions, utilisation des moyens de
  l'entreprise, temps de travail). Si la question utile est de savoir qui
  détient le code, sous quel titre, avec quelles pièces et quelles réserves,
  ouvrir `revue-logiciel-donnees`. `qualification-oeuvre` reste ici limité à
  l'originalité et au régime applicable ; l'audit open source composant par
  composant relève de `revue-open-source`.
- **Œuvres journalistiques (L.132-36 à L.132-45)** : cession encadrée par
  **convention collective des journalistes** (CCNTJ) et accord d'entreprise
  — régime spécifique avec rémunération de référence (« titre de presse »
  d'origine + exploitation autre support).
- **Agents publics (L.111-1 al.4 et L.131-3-1+)** : régime spécifique pour
  les fonctionnaires — cession à l'État ou collectivité dans la mesure
  strictement nécessaire à l'accomplissement de la mission de service public,
  avec intéressement aux produits d'exploitation commerciale.

**Risque critique** : entreprises qui supposent automatiquement détenir les
droits sur les créations de leurs salariés (logos refaits par graphiste
salarié, textes marketing, vidéos, designs) — sans cession écrite, le
salarié peut, en cas de départ conflictuel ou de litige, contester
l'exploitation. La cession L.131-3 doit figurer dans le **contrat de
travail** (clause de cession) ou faire l'objet d'un avenant pour chaque
œuvre ou catégorie d'œuvres (cession globale d'œuvres futures encadrée
L.131-1 — prohibée sauf exceptions, en pratique on cède au fur et à mesure
ou par catégorie déterminée).

### Cas G — Œuvre posthume

**Configuration** : œuvre divulguée après le décès de l'auteur, ou auteur
décédé avec droits transmis aux héritiers.

**Titularité** :
- **Droits patrimoniaux** : dévolus aux **ayants droit** (héritiers et/ou
  cessionnaires antérieurs au décès), selon les règles de droit successoral.
  Durée standard 70 ans post mortem (L.123-1) à compter de l'année suivant
  le décès.
- **Droit moral** : transmissible **par voie testamentaire** aux héritiers
  (L.121-1 al.4) — perpétuel (ne s'éteint jamais), donc transmis de
  génération en génération.
- **Œuvres divulguées post mortem** (L.123-4) : pour les œuvres divulguées
  **après l'expiration du monopole d'exploitation** du droit commun (typique
  œuvres inédites retrouvées), durée spéciale de **25 ans** à compter de
  l'année de divulgation, au profit du propriétaire du manuscrit ou de
  l'ayant droit divulgateur.

**Risque** : indivision successorale entre héritiers — exploitation requiert
l'accord de tous les ayants droit (cf. cas B sur l'unanimité) ; en cas de
désaccord persistant, recours possible au juge.

---

## Étape 4 — Droits patrimoniaux vs Droit moral

La distinction droits patrimoniaux / droit moral structure tout le droit
d'auteur français. **Ce n'est pas un découpage économique ; c'est un
découpage juridique de nature** : les patrimoniaux sont cessibles et
limités dans le temps, le moral est inaliénable et perpétuel.

### Droits patrimoniaux (L.122-1 à L.122-12)

**Droits exclusifs d'exploitation** — cessibles, temporaires (70 ans post
mortem standard), divisibles (peuvent être cédés droit par droit).

| Droit | Article | Définition pratique |
|---|---|---|
| **Reproduction** | L.122-3 | Fixation matérielle de l'œuvre permettant sa communication indirecte : impression, gravure, numérisation, photocopie, enregistrement, stockage informatique |
| **Représentation** | L.122-2 | Communication directe au public : récitation, projection, exécution publique, télédiffusion, mise à disposition en ligne (streaming) |
| **Adaptation / traduction / transformation** | L.122-4 | Réalisation d'œuvres dérivées : traduction, adaptation cinématographique, arrangement musical, novellisation |
| **Distribution / location / prêt** | L.122-6 (logiciel) + droit commun | Mise sur le marché de copies physiques de l'œuvre — épuisement européen après première vente licité dans l'EEE (sauf droit de location qui ne s'épuise pas) |
| **Droit de suite** | L.122-8 | Spécifique aux œuvres graphiques et plastiques originales — participation de l'artiste au produit des reventes successives (3 % à 5 % progressif jusqu'à 12 500 €) |

**Cession** : cf. L.131-3 (formalisme : énumération, étendue, destination,
lieu, durée, rémunération) et L.131-4 (rémunération proportionnelle par
principe, forfait dans cas listés).

**Durée** : 70 ans post mortem (L.123-1), à compter du 1er janvier suivant
le décès. Après expiration, l'œuvre tombe dans le **domaine public** —
exploitation libre (mais droit moral perpétuel toujours opposable).

### Exceptions au monopole patrimonial (L.122-5)

Liste limitative — l'auteur ne peut interdire dans ces cas (sous conditions
strictes) :

- **Représentations privées et gratuites dans le cercle de famille** (L.122-5 1°)
- **Copies ou reproductions strictement réservées à l'usage privé du copiste**
  et non destinées à une utilisation collective (L.122-5 2°) — **copie privée**,
  compensée par redevance L.311-1+ administrée par Copie France
- **Analyses et courtes citations** justifiées par le caractère critique,
  polémique, pédagogique, scientifique ou d'information (L.122-5 3° a) —
  conditions : œuvre divulguée + mention du nom de l'auteur et de la source
  + courte par rapport à l'œuvre citée et l'œuvre citante
- **Revues de presse** (L.122-5 3° b)
- **Diffusion de discours publics** (L.122-5 3° c)
- **Reproductions intégrales ou partielles d'œuvres d'art graphiques ou
  plastiques** destinées à figurer dans le catalogue d'une vente judiciaire
  (L.122-5 3° d)
- **Parodie, pastiche, caricature** (L.122-5 4°) — selon les lois du genre
  (intention humoristique + absence de risque de confusion avec l'œuvre
  parodiée + absence d'intention de nuire)
- **Exception pédagogique et de recherche** (L.122-5 3° e) — conditions
  d'usage à des fins exclusives d'illustration de l'enseignement et de la
  recherche
- **Exception handicap** (L.122-5 7°) — reproduction et représentation en
  faveur des personnes handicapées (formats adaptés)
- **Reproduction temporaire transitoire ou accessoire** (L.122-5 6°) — cache
  web, transit de paquets, copies techniques nécessaires au fonctionnement
  des réseaux
- **Fouille de textes et de données** (L.122-5-3 — DAMUN 2019/790 transposée
  ord. 2021-1518) — text and data mining à des fins de recherche scientifique
  (conditions et opt-out pour usages commerciaux)

Les exceptions sont **d'interprétation stricte** (jurisprudence constante).

### Droit moral (L.121-1)

> **Article L.121-1 al.1** : « L'auteur jouit du droit au respect de son nom,
> de sa qualité et de son œuvre. »
>
> **Caractères** : « Ce droit est **attaché à sa personne**. Il est
> **perpétuel, inaliénable et imprescriptible**. Il est transmissible à cause
> de mort aux héritiers de l'auteur. »

**4 prérogatives** :

| Prérogative | Article | Définition |
|---|---|---|
| **Droit de divulgation** | L.121-2 | L'auteur a seul le droit de décider du **moment** et des **conditions** de la première publication de l'œuvre |
| **Droit de paternité** | L.121-1 al.1 | Exigence de la mention du **nom** et de la **qualité d'auteur** sur tous les supports et toutes les exploitations (sauf si l'auteur l'à expressément refusée — œuvre anonyme ou pseudonyme) |
| **Droit à l'intégrité (ou « respect de l'œuvre »)** | L.121-1 al.1 | Opposition à toute **modification, altération ou dénaturation** de l'œuvre, même autorisée contractuellement, dès lors qu'elle porte atteinte à son intégrité ou son esprit. Seuil élevé en jurisprudence — adaptations mineures généralement tolérées si prévues au contrat |
| **Droit de repentir / retrait** | L.121-4 | L'auteur peut faire **cesser l'exploitation** moyennant **indemnisation préalable** du cessionnaire pour le préjudice subi. Si l'auteur reprend ensuite l'exploitation, il doit la proposer en priorité au cessionnaire évincé. Rare en pratique (coût indemnisation dissuasif) |

**Caractères cumulatifs** :
- **Perpétuel** : ne s'éteint jamais — même après expiration des 70 ans
  post mortem patrimoniaux, le droit moral reste opposable aux héritiers
  (ou à défaut au ministre chargé de la culture L.121-3).
- **Inaliénable** : ne peut être cédé par contrat — toute clause de
  renonciation est nulle.
- **Imprescriptible** : pas de prescription extinctive, l'action est
  ouverte sans limitation de durée.

### Point de friction critique cession + droit moral

> **Le cessionnaire des droits patrimoniaux ne peut PAS modifier l'œuvre
> sans accord de l'auteur** (droit à l'intégrité moral inaliénable) — d'où
> **nécessité de clauses contractuelles spécifiques** dans tout contrat de
> cession :
> - **adaptation autorisée** (formats dérivés, déclinaisons, traductions)
> - **contexte de diffusion** (supports, territoires, modifications
>   éditoriales de cohérence)
> - **rebranding** (intégration dans nouvelle identité visuelle)
> - **intégration dans système tiers** (typiquement logiciel embarqué dans
>   plateforme tierce)
>
> Sans ces clauses, le cessionnaire prend un risque sur tout rebranding,
> toute modification, toute intégration ultérieure — l'auteur peut
> s'opposer et obtenir cessation + indemnisation. Tag `[review]` automatique
> pour tout contrat de cession qui ne traite pas explicitement ces points.

---

## Étape 5 — Durée de protection

La durée varie selon le type d'œuvre et le contexte de création. Toutes
les durées se calculent à compter du **1er janvier suivant l'événement
déclencheur** (article L.123-7).

| Type d'œuvre | Durée | Référence CPI |
|---|---|---|
| **Règle générale** | Vie de l'auteur + **70 ans post mortem** | L.123-1 |
| **Logiciels** | Vie de l'auteur + 70 ans (pas de dérogation de durée — seule la titularité L.113-9 diffère) | L.123-1 |
| **Bases de données — droit d'auteur sur la structure** | 70 ans post mortem | L.123-1 |
| **Bases de données — droit sui generis sur le contenu** | **15 ans** à compter du 1er janvier de l'année suivant l'achèvement (renouvelable si modification substantielle de la base) | L.342-5 |
| **Œuvre de collaboration** | 70 ans après le décès du **dernier coauteur survivant** | L.123-2 |
| **Œuvre collective / pseudonyme / anonyme** | 70 ans à compter de la **publication** (du 1er janvier de l'année suivante) | L.123-3 |
| **Œuvre posthume divulguée pendant la période de protection** | Durée standard (70 ans post mortem) — pas de prolongation | L.123-1 |
| **Œuvre posthume divulguée après expiration du monopole** | **25 ans** à compter du 1er janvier de l'année suivant la divulgation, au profit du propriétaire du manuscrit ou de l'ayant droit divulgateur | L.123-4 |
| **Droits voisins (artistes-interprètes, producteurs phonogrammes et vidéogrammes, entreprises de communication audiovisuelle)** | **70 ans** à compter de la fixation, de la publication ou de la communication au public (selon le droit voisin concerné) — régime distinct du droit d'auteur, voir `droits-voisins-ogc` | L.211-4 |

**Prolongations historiques de guerre** (L.123-8 à L.123-10) : pour les
œuvres créées avant le 1er janvier 1948, des prolongations spéciales
existent au titre des guerres de 1914-1918 et 1939-1945 (« prorogations de
guerre »). Calcul complexe — vérifier au cas par cas (CJUE Hauptmann
C-518/08 (2010) sur l'articulation avec la directive 2006/116/CE de durée
harmonisée).

**Domaine public** : à l'expiration du monopole patrimonial, l'œuvre peut
être exploitée librement par tous. **MAIS** le droit moral reste perpétuel —
les héritiers (ou à défaut le ministre chargé de la culture) peuvent
toujours agir en respect du nom et de l'intégrité de l'œuvre.

**Important — calcul concret** : pour estimer l'expiration des droits
patrimoniaux d'une œuvre, demander la **date de naissance** de l'auteur
(estimation prudente d'espérance de vie si vivant), calculer la date de
décès estimée, ajouter 70 ans, et arrondir au 1er janvier suivant. Tag
`[à vérifier]` sur toute date d'expiration calculée à partir d'une estimation
de durée de vie.

---

## Étape 6 — Enjeux identifiés (selon l'objectif de la qualification)

L'objectif (préventif / défensif / contentieux) déclaré à l'cadrage initial conditionne
la nature et la formulation des enjeux. Ne pas générer les 3 listes : ne
produire que celle correspondant à l'objectif déclaré (les autres en sont la
contrepartie en miroir).

### Objectif préventif (avant exploitation / diffusion / cession)

- **Cession incomplète ou inexistante** : risque d'opposition future de
  l'auteur (créateur indépendant, salarié non-cédé, agence externe) à toute
  exploitation au-delà de la livraison initiale.
- **Droits moraux mal gérés** : rebranding, modifications, intégration dans
  système tiers, déclinaisons de formats — sans clause spécifique au contrat
  de cession, ouvre l'action en violation du droit moral (cessation +
  dommages-intérêts).
- **Régime logiciel vs œuvre littéraire** : pour SaaS / applications,
  identification critique L.113-9 (logiciel salarié = employeur titulaire
  automatique) vs droit commun (contenu marketing, design d'interface si non
  logiciel) — frontière fine.
- **Conditions cumulatives L.131-3 non respectées** (mention écrit +
  énumération des droits + domaines + territoires + durée + rémunération) :
  nullité partielle ou totale de la cession — c'est l'erreur la plus
  fréquente en pratique.
- **Pacte de coauteurs absent** (cas B) : risque de blocage par l'un des
  coauteurs à l'exploitation.
- **Chaîne de droits d'œuvre composite non documentée** (cas D) :
  contrefaçon dérivée même en cas d'originalité propre.
- **Preuves de date insuffisantes** : risque défensif futur si contestation
  d'antériorité — proposer `depot-preuve-creation` : mode `open` pour
  `Evidence Register` et `Proof Gaps`, puis `timeline` si une `Timeline`
  ordonnée est nécessaire.

### Objectif défensif (contestation reçue d'un tiers)

- **Notre œuvre est-elle bien originale au sens CJUE Infopaq ?** Application
  rigoureuse des 3 tests de l'étape 1, identification des choix créatifs
  concrets opposables.
- **Notre titularité est-elle bien établie ?** Chaîne de cessions tracée
  depuis le créateur jusqu'à nous (contrats, avenants, factures avec mentions
  L.131-3, pacte de coauteurs si applicable).
- **L'œuvre contestée est-elle vraiment dérivée de la nôtre ?** Analyse
  comparative caractéristique par caractéristique — distinguer **idée**
  (non protégée) et **expression** (protégée).
- **Avons-nous des preuves de date de création antérieures** à l'œuvre
  contestée ? Inventaire des preuves disponibles, recommandation
  `depot-preuve-creation` si le dossier probatoire est lacunaire : mode
  `open` pour `Evidence Register` et `Proof Gaps`, puis `timeline` si une
  `Timeline` ordonnée est nécessaire pour argumenter l'antériorité.
- **Position défensive sur les exceptions L.122-5** : la partie adverse
  peut-elle invoquer copie privée, courte citation, parodie, exception
  pédagogique ?

### Objectif contentieux (préparation action contrefaçon)

- **Preuves de date de création** : ouvrir `depot-preuve-creation` en mode
  `open` pour `Evidence Register` et `Proof Gaps` sur les pièces
  (manuscrits horodatés, dépôts copyright.fr, enveloppe Soleau INPI, constat
  d'huissier ou commissaire de justice), puis `timeline` si une `Timeline`
  exploitable est nécessaire avant action.
- **Identification des droits violés** : patrimoniaux (lesquels précisément :
  reproduction, représentation, adaptation) et/ou moraux (paternité, intégrité).
- **Évaluation préjudice préliminaire** : différé `contrefacon-droit-auteur`
  V4.2 (réparation intégrale L.331-1-3 — conséquences économiques négatives,
  préjudice moral, bénéfices réalisés par le contrefacteur).
- **Compétence juridictionnelle** : **TJ Paris (3e chambre PI)** ou TJ
  régional désigné selon le défendeur (décret n° 2009-1205 — 10 TJ
  spécialisés PI en France hors Paris). Vérifier la compétence avant
  rédaction assignation.
- **Saisie-contrefaçon préalable** (L.332-1+) : mesure probatoire essentielle
  — ordonnance sur requête au président TJ, exécution par huissier. À
  préparer avant l'action.
- **Prescription** : action en contrefaçon se prescrit par **5 ans** à
  compter de la connaissance des faits (L.331-1-4) — vérifier que le délai
  n'est pas écoulé.

---

## Format de sortie V2

Le livrable doit suivre ce contrat de sortie stable :

### 1. `Qualification Snapshot`

- description courte de l'œuvre ;
- `objective_mode`, `work_type`, `creation_context` ;
- triage prudent : `clair`, `mixte`, `fragile` ;
- phrase courte sur le principal point de force ou de doute.

### 2. `Faits et revue probatoire`

- faits reçus ;
- pièces lues ;
- pièces annoncées mais non lues ;
- trous critiques `[à vérifier]`.

### 3. `Analyse de l'originalité`

- test 1 : choix libres vs contraintes ;
- test 2 : identifiabilite ;
- test 3 : effort intellectuel creatif ;
- conclusion motivee, jamais définitive.

### 4. `Category and Work-Type Map`

- catégorie principale ;
- régimes speciaux ou hybrides ;
- composants à traiter distinctement si œuvre mixte.

### 5. `Initial Ownership Map`

- cas de titularité retenu ;
- titulaire(s) apparent(s) ;
- risques de chaîne de droits ou d'attribution.

### 6. `Economic Rights, Moral Rights and Term`

- droits patrimoniaux apparents ;
- droit moral et points de friction ;
- durée applicable et éventuelle estimation `[à vérifier]`.

### 7. `Objective-Specific Risks`

- risques calibres selon `preventive`, `défensive` ou `litigation-prep` ;
- ne pas mélanger les trois listes ;
- ne garder que les risques utiles au dossier.

### 8. `Routage de prochaine étape`

Utiliser uniquement une issue principale parmi :

- `hold-and-document`
- `secure-proof-first`
- `clarify-chain-of-title`
- `draft-assignment`
- `draft-license`
- `prepare-copyright-attack`
- `insufficient-record`

Puis expliquer :

- pourquoi cette issue est la bonne ;
- quel skill ouvrir si nécessaire ;
- quelles pièces ou validations conditionnent la suite.

### 9. `Validation humaine`

- ce qui est établi ;
- ce qui reste hypothetique ;
- ce qui doit être vérifie ;
- quelle validation humaine est requise avant exploitation, cession, licence
  ou action.

Le livrable reste sans bandeau Hacienda et sans narration interne. Il ne doit
 jamais conclure definitivement à l'existence ou à l'inexistence du droit
 d'auteur.

---

## Seuil non-juriste — quand le profil indique « non-juriste »

Quand le profil pratique indique un rôle **non-juriste** (collaborateur opérationnel,
fondateur, manager produit, créateur indépendant sans formation juridique),
appliquer le gate suivant **avant** la production du livrable :

> Cette qualification est une **analyse juridique**, pas un avis d'opportunité
> d'action. Exploiter, céder ou contester une œuvre sans validation par un
> avocat spécialisé propriété littéraire et artistique à des conséquences
> concrètes :
>
> - **Cession invalide** (non-respect L.131-3) : le créateur peut s'opposer
>   à l'utilisation ultérieure de l'œuvre, demander cessation, et obtenir
>   indemnisation rétroactive.
> - **Action en contrefaçon mal fondée** : déboutement + dépens + risque
>   d'action reconventionnelle pour concurrence déloyale (procédure abusive).
> - **Violation droit moral non anticipée** : modification jugée dénaturante
>   = action en cessation + dommages-intérêts, même si la cession des droits
>   patrimoniaux est validé.
> - **Chaîne de droits cassée sur œuvre composite** : exploitation qualifiée
>   contrefaçon de l'œuvre préexistante, peu importe l'originalité propre.
>
> **Voici le brief à apporter à l'avocat spécialisé :**
>
> 1. **Œuvre** : [description courte, nature, forme tangible, date]
> 2. **Originalité** : verdict prima facie 🟢/🟡/🔴 + justification des 3
>    tests appliqués
> 3. **Titularité** : cas A à G applicable + identification titulaire(s)
>    + risques (cession écrite manquante, pacte coauteurs, chaîne composite)
> 4. **Droits patrimoniaux** : dévolus à [créateur / employeur / commanditaire
>    / cotitulaires]
> 5. **Droit moral** : conservé par [auteur(s) personne physique]
> 6. **Objectif** : préventif / défensif / contentieux
> 7. **3 questions critiques** à poser à l'avocat :
>    - « La qualification d'originalité tient-elle face à la jurisprudence
>      récente sur [domaine concerné] ? »
>    - « Le cas de titularité [X] est-il bien identifié — peut-il être
>      contesté par un tiers ? »
>    - « Le droit moral pose-t-il un risque sur [usage envisagé : adaptation,
>      rebranding, intégration tiers] ? »
>
> **Annuaires pour trouver un avocat spécialisé propriété littéraire et
> artistique :**
> - Conseil National des Barreaux — annuaire officiel : https://www.avocat.fr
>   (filtre « propriété intellectuelle » ou « propriété littéraire et
>   artistique »)
> - **ALAI France** (Association littéraire et artistique internationale —
>   section française) : réseau de spécialistes
> - **Organismes de gestion collective (OGC)** pour orientations selon
>   l'œuvre : **SACEM** (musique), **SCAM** (œuvres multimédias et
>   audiovisuelles non fiction), **SACD** (œuvres dramatiques, chorégraphiques,
>   cinématographiques), **SDRM** (reproduction mécanique)

Le livrable structuré (cf. format de sortie) est tout de même généré pour
servir de brief de travail. Il n'a pas vocation à être transmis tel quel à
un tiers (contrepartie, plateforme, juridiction) — c'est un **document
préparatoire interne**.

---

## Emplacement du livrable

Le livrable est écrit dans :

```
~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/outputs/qualification-oeuvre-<slug-oeuvre>-YYYY-MM-DD.md
```

Le slug est construit à partir de la description courte de l'œuvre, normalisé
en minuscules sans accents, avec tirets pour les espaces (ex :
`roman-litteraire-titre-x` pour « Roman littéraire — Titre X »).

Si workspaces de dossier activés (V1.1+, cf. `CLAUDE.md` extension §11),
l'emplacement bascule sur :

```
~/.claude/plugins/config/hacienda-juridique/hacienda-propriete-intellectuelle/matters/<slug-dossier>/qualification-oeuvre-<slug-oeuvre>-YYYY-MM-DD.md
```

Si le répertoire `outputs/` ou `matters/<slug-dossier>/` n'existe pas, le
créer. Si plusieurs qualifications du même jour pour la même œuvre, suffixer
`-v2`, `-v3`, etc.

---

## Ce que ce skill NE fait PAS

- **Conclure définitivement à l'existence du droit d'auteur** sur l'œuvre
  analysée — c'est le **juge** qui tranche in fine après contestation, sur
  la base de la preuve apportée par les parties. Ce skill produit une
  qualification **prima facie**, jamais un constat opposable.
- **Rédiger un contrat de cession** de droits patrimoniaux — voir
  `cession-droit-auteur` V4.1 (mentions L.131-3 obligatoires : énumération
  + étendue + destination + lieu + durée + rémunération).
- **Rédiger une licence** (propriétaire ou open source — MIT, Apache 2.0,
  GPL-3.0, AGPL-3.0, Creative Commons) — voir `licence-droit-auteur` V4.1.
- **Qualifier une contrefaçon** alléguée d'une œuvre tierce — voir
  `contrefacon-droit-auteur` V4.2 (analyse contradictoire originalité +
  similitudes substantielles + caractères différenciants).
- **Déposer une preuve de création** (enveloppe Soleau INPI, copyright.fr,
  constat d'huissier ou commissaire de justice, dépôt notarié, blockchain
  horodatée) — voir `depot-preuve-creation` : mode `open` pour `Evidence Register`
  et `Proof Gaps`, puis `timeline` si une `Timeline` ordonnée est utile.
- **Évaluer le préjudice** en cas de contrefaçon constatée (réparation
  intégrale L.331-1-3 — conséquences économiques négatives + préjudice moral
  + bénéfices réalisés par le contrefacteur) — différé V4.2.
- **Gérer la succession des ayants droit** d'une œuvre dont l'auteur est
  décédé — combine droit de la propriété littéraire et artistique + droit
  successoral, requiert intervention notaire + avocat spécialisé droit
  successoral.
- **Traiter les droits voisins** (artistes-interprètes, producteurs
  phonogrammes et vidéogrammes, entreprises de communication audiovisuelle
  L.211-1+) — régime distinct du droit d'auteur, voir `droits-voisins-ogc`.
- **Gérer les rapports avec les organismes de gestion collective (OGC)** —
  adhésion SACEM / SCAM / SACD / SDRM, déclaration des œuvres au répertoire,
  répartition des redevances — voir `droits-voisins-ogc`.
- **Conduire une recherche d'antériorité** sur l'œuvre (vérifier qu'elle ne
  contrefait pas une œuvre préexistante) — pas d'équivalent strict des
  recherches d'antériorité brevet ou marque en droit d'auteur (le droit
  d'auteur n'a pas de registre central) ; analyse comparative au cas par
  cas si litige.

---

## Ton

- **Analytique** — chaque verdict (originalité, cas de titularité, durée) est
  argumenté à partir des faits concrets et des règles applicables, pas
  asséné.
- **Précis** — citation systématique des articles CPI applicables (L.111-1,
  L.112-2, L.113-X, L.121-1+, L.122-1+, L.123-X, L.131-3) et de la
  jurisprudence pertinente (CJUE Infopaq, Painer, Cofemel, BSA ; Cass.
  Pachot pour logiciel).
- **Équilibré** — la qualification est rarement noire ou blanche, surtout
  sur l'originalité (souvent 🟡 en pratique). Présenter les forces ET les
  incertitudes. Une qualification trop affirmative trompe le décideur sur
  la solidité de sa position.
- **Adapté au profil** — avocat spécialisé : ton confraternel, raccourcis
  techniques OK ; juriste interne : explications complètes ; non-juriste :
  vulgarisation + gate explicite vers avocat.

---
