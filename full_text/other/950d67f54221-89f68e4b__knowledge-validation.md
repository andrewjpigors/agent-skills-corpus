---
name: knowledge-validation
description: Knowledge de validation des travaux. Se lance automatiquement au démarrage de chaque session.
---

## Knowledge de validation des travaux

Tu dois exécuter ce knowledge en utilisant l'outil AskUserQuestion. Le knowledge a 3 niveaux. Tu dois suivre cette logique exactement.

### Source de configuration

La structure du knowledge (questions, actions, messages) est définie dans le fichier `knowledge/methodology/methodology-knowledge.md`. Au démarrage du skill, lire ce fichier avec l'outil Read pour obtenir :
- La liste des knowledge (noms, lettres, questions)
- Les actions associées à chaque question (fonction/programme)
- Les messages à afficher quand l'utilisateur répond Vrai
- Les choix disponibles pour le sous-knowledge (Vrai, Faux, Passer / True, False, Skip)
- Le message de fin

**Format bilingue :** Le fichier de configuration supporte le français et l'anglais :
- **Titre** : `# Titre FR | Title EN`
- **Messages** : préfixés `FR:` et `EN:` sur des lignes séparées
- **Noms de knowledge** : `### Nom FR | Name EN (lettre: X)` — optionnel : `(lettre: X, methodology: methodology-name)` pour associer une méthodologie spécifique (fichier `knowledge/methodology/<methodology-name>.md`)
- **Tableaux** : 6 colonnes — `| ID | Choix FR | Choix EN | Action | Message FR | Message EN |`
  - `ID` : identifiant technique (A1, B2, D1...)
  - `Choix FR` / `Choix EN` : label affiché dans AskUserQuestion selon la langue
  - `Action` : type d'action (fonction, programme, executer_demande)
  - `Message FR` / `Message EN` : message affiché quand l'utilisateur répond Vrai
- **Choix du sous-knowledge** : `FR: Vrai, Faux, Passer` / `EN: True, False, Skip`

Le parseur (`knowledge/engine/knowledge_config/__init__.py`) accepte un paramètre `langue` ("fr" ou "en") et retourne les données dans la langue sélectionnée. Par défaut : "fr". Chaque question retournée contient un champ `choix` (le label bilingue) en plus de `id`, `action_vrai`, `message_vrai`.

**Pour AskUserQuestion**, utiliser le champ `choix` comme label des options (au lieu de l'ID brut). L'ID reste utilisé pour les clés internes et la grille de résultats.

Utiliser ces données pour construire dynamiquement les options AskUserQuestion, les résultats par défaut, et les messages d'action. Ne PAS utiliser de valeurs codées en dur.

**Exception hardcodée :** La **dernière** question du 1er knowledge est TOUJOURS de type `executer_demande`, peu importe son ID ou ce qui est écrit dans `methodology-knowledge.md`. Cette règle est programmatique et prioritaire sur le contenu du fichier de configuration.

### Persistance des résultats (survie au compactage)

Les résultats du knowledge DOIVENT être sauvegardés dans le fichier `.claude/knowledge_resultats.json` après CHAQUE réponse de l'utilisateur. Cela garantit que les résultats survivent au compactage de session.

**Format du fichier `.claude/knowledge_resultats.json` :**
Le format est construit dynamiquement à partir de `knowledge/methodology/methodology-knowledge.md`. Exemple avec la config actuelle :
```json
{
  "en_cours": true,
  "user_session_id": "us-20260308-a1b2c3",
  "started_at": "2026-03-08T14:30:00Z",
  "niveau": "principal",
  "knowledge_actif": null,
  "page_principal": 0,
  "page_secondaire": 0,
  "demande_executee": false,
  "demande_reformulee": null,
  "issue_github": null,
  "collateral_tasks": [],
  "system_sessions": [],
  "valeurs_detectees": {},
  "resultats": {
    "Validation de la demande": {"A1": "--", "A2": "--", "A3": "--", "A4": "--"},
    "Qualité du travail": {"B1": "--", "B2": "--", "B3": "--", "B4": "--"},
    "Intégrité de session": {"C1": "--", "C2": "--", "C3": "--", "C4": "--"},
    "Documentation": {"D1": "--", "D2": "--", "D3": "--"},
    "Approbation": {"E1": "--", "E2": "--", "E3": "--"}
  }
}
```
Pour construire les résultats par défaut : pour chaque knowledge dans `methodology-knowledge.md`, créer une entrée avec le nom du knowledge, et pour chaque question, initialiser à `"--"`.

**Au démarrage du skill :**
1. Lire `.claude/knowledge_resultats.json` avec l'outil Read
2. Si le fichier existe et `en_cours` est `true` : reprendre le knowledge au niveau indiqué (survie au compactage). Le `user_session_id` existant est conservé — c'est la même session utilisateur qui reprend après compaction/crash.
   - Ajouter la branche système courante dans `system_sessions[]` si elle n'y est pas déjà (chaque redémarrage système est une nouvelle entrée).
3. Si le fichier existe et `en_cours` est `false` : c'est un résidu d'une session précédente. Supprimer le fichier (`rm .claude/knowledge_resultats.json && git add .claude/knowledge_resultats.json && git commit -m "knowledge: nettoyage début de session" && git push -u origin <branche-courante>`), puis créer un nouveau fichier et démarrer le knowledge
4. Si le fichier n'existe pas : créer le fichier avec les valeurs par défaut et démarrer le knowledge

**Identité de session utilisateur (v2.0) :**
À la CRÉATION d'un nouveau fichier `knowledge_resultats.json` (étapes 3 et 4), générer les champs d'identité :
- `user_session_id` : format `"us-YYYYMMDD-XXXXXX"` où XXXXXX = 6 caractères aléatoires hex. Cet ID est l'ancre interne de la session utilisateur. Il NE dépend PAS de GitHub.
- `started_at` : timestamp ISO UTC du démarrage
- `system_sessions` : `["<branche-courante>"]` — la première session système
- `collateral_tasks` : `[]` — les sous-demandes collatérales auto-générées pendant la session

**Continuité :** Quand `en_cours` est `true` (étape 2), le `user_session_id` SURVIT au compactage. C'est ce qui permet d'agréger N sessions système en 1 session utilisateur. La branche courante est ajoutée à `system_sessions[]` uniquement si absente.

**Propagation :** Le `user_session_id` doit être écrit dans le runtime cache (`session_data.user_session_id`) via `knowledge/engine/scripts/session_agent/cache.py` pour que le compilateur de sessions puisse l'utiliser.
5. **Pré-remplissage (God Mode)** : Après l'étape 1-4, analyser le message initial de l'utilisateur. Si le message contient un bloc JSON `{"resultats": {...}}` (sur une ligne séparée, après la demande), l'extraire. La demande est le texte AVANT le bloc JSON.
   - **Si aucun JSON trouvé dans le message** : pas de pré-remplissage, continuer normalement.
   - **IMPORTANT** : Ne JAMAIS lire de fichier sur disque comme source de pré-remplissage. Le fichier `.claude/knowledge_prerempli.json.example` est un template de référence pour l'utilisateur uniquement.

   Le format attendu :
      ```json
      {
        "resultats": {
          "Validation de la demande": {"A1": "Vrai", "A2": "Faux"},
          "Qualité du travail": {"B1": "Vrai"}
        }
      }
      ```
      Seules les clés présentes sont fusionnées. Les questions absentes restent à `"--"`.

   **Appliquer le pré-remplissage :**
   a. Fusionner les valeurs dans `knowledge_resultats.json` : pour chaque knowledge et chaque question présente dans le pré-rempli, remplacer la valeur `"--"` par la valeur fournie (Vrai, Faux, ou Passer)
   b. Sauvegarder `knowledge_resultats.json` mis à jour
   c. Committer : `git add .claude/knowledge_resultats.json && git commit -m "knowledge: pré-remplissage appliqué"`

**Après CHAQUE réponse de l'utilisateur (persistance sur branche de travail) :**
1. Mettre à jour les résultats dans le JSON
2. Mettre à jour `niveau` ("principal", "secondaire", "sous_knowledge") et `knowledge_actif` (la lettre en cours)
3. Sauvegarder le fichier avec l'outil Write
4. Committer sur la branche de travail : `git add .claude/knowledge_resultats.json && git commit -m "knowledge: mise à jour des résultats"`
5. Pousser sur la branche de travail : `git push -u origin <branche-courante>`

**Quand l'utilisateur fait Skip au niveau principal (synchronisation vers main) :**
1. Mettre `en_cours` à `false`
2. Sauvegarder le fichier
3. Committer sur la branche de travail : `git add .claude/knowledge_resultats.json && git commit -m "knowledge: validation terminée"`
4. Pousser sur la branche de travail : `git push -u origin <branche-courante>`
5. Afficher la grille de résultats
6. Exécuter `compilation_metriques(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py` — compilation **incrémentale** : ne compile que le delta depuis la dernière compilation (post-exécution). Si des changements de métriques sont détectés, met `_documentation_requise = True`
7. Exécuter `compilation_temps(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py` — compilation **incrémentale** : ne compile que le delta depuis la dernière compilation (post-exécution). Si des changements de temps sont détectés, met `_documentation_requise = True`
8. Exécuter `pre_sauvegarde(resultats)` depuis `knowledge/engine/scripts/knowledge_skills.py` — **Pré-sauvegarde** : exécute les règles de conformité. Première sous-fonction : `confirmation_documentation` (compare le flag interne avec le résultat de l'étape Documentation du quiz). D'autres règles suivront.
9. Exécuter `sauvegarde(resultats)` depuis `knowledge/engine/scripts/knowledge_skills.py`
10. **Commit final + push (ÉTAPE OBLIGATOIRE)** : committer TOUS les fichiers générés par les étapes 6-9 (sessions.json, tasks.json, knowledge_resultats.json mis à jour, et tout autre fichier modifié) :
    - `git add -A && git commit -m "knowledge: compilation finale — sessions.json + tasks.json pour interfaces web"` (si des changements existent)
    - `git push -u origin <branche-courante>`
11. **Créer le PR et merger vers main (ÉTAPE OBLIGATOIRE)** :
   - Utiliser **exclusivement** `knowledge/engine/scripts/gh_helper.py` (JAMAIS `gh` CLI, JAMAIS git direct) :
     ```
     export GH_TOKEN="$GH_TOKEN" && python3 -c "
     from knowledge.engine.scripts.gh_helper import GitHubHelper
     gh = GitHubHelper()
     result = gh.pr_create_and_merge('packetqc/knowledge', '<branche-courante>', 'main', 'Knowledge: validation terminée — <user_session_id>', body='Grille de résultats:\n<grille_markdown>')
     import json; print(json.dumps(result))
     "
     ```
   - Le titre du PR inclut le `user_session_id` pour traçabilité
   - Le body du PR contient la grille de résultats
   - **Le PR inclut maintenant TOUT** : knowledge_resultats.json, sessions.json, tasks.json, et toutes les compilations — c'est ce qui alimente les interfaces web
   - Si `pr_create_and_merge` échoue : afficher "Note: le merge vers main doit être fait manuellement." mais ne PAS bloquer le reste du flow
Note : le fichier `knowledge_resultats.json` reste sur main avec les résultats après le merge. Il sera nettoyé au démarrage de la prochaine session.

### Configuration des actions

Quand l'utilisateur répond **Vrai**, consulter `knowledge/methodology/methodology-knowledge.md` pour trouver l'action et le message associés à la question courante :
- Chaque question dans le fichier a un champ `action_vrai` (fonction ou programme) et un champ `message_vrai`
- Afficher le `message_vrai` de la question

Quand l'utilisateur répond **Faux**, enregistrer "Faux" sans action.
Quand l'utilisateur répond **Passer**, enregistrer "Passer" sans action.

### Système de pagination

AskUserQuestion est limité à 4 options (2 à 4). Pour supporter un nombre illimité d'éléments dans `methodology-knowledge.md`, un système de pagination est utilisé aux niveaux principal et secondaire.

**Règle de pagination (identique aux deux niveaux) :**
- Calculer le nombre total d'éléments (knowledge ou questions) depuis `methodology-knowledge.md`
- Il n'y a plus d'option de contrôle fixe (Terminer/Passer) dans les choix — le bouton **Skip** natif de AskUserQuestion remplit ce rôle
- Si total = 1 : entrée automatique (pas de menu — voir mode initial du principal)
- Si total ≤ 4 : afficher tous les éléments (2 à 4 options, pas de pagination)
- Si total > 4 : pagination nécessaire
  - **Page intermédiaire** : 3 éléments + `Suivant ▸` (4 options)
  - **Dernière page** : éléments restants (2 à 4 options, pas de `Suivant ▸`)
- Maintenir un index de page courant dans `.claude/knowledge_resultats.json` : champs `page_principal` et `page_secondaire` (défaut: 0)

**Persistance de la page :** Après chaque navigation de page, sauvegarder l'index dans le JSON et committer/pousser comme pour toute autre mise à jour.

### Niveau 1 : Knowledge Principal

**Mode initial (demande_executee = false) :**
- **Entrée automatique** dans le Knowledge A : puisqu'il n'y a qu'un seul knowledge disponible (le 1er), entrer directement dans le Knowledge Secondaire correspondant sans afficher de menu principal. AskUserQuestion exige minimum 2 options, et avec un seul élément sans option de contrôle, le menu serait impossible.
- Toutes les demandes, y compris `interactif`/`interactive`, passent par le flux normal avec auto-validation des valeurs pré-remplies puis A4. La détection du mode interactif se fait à l'étape A4 (`executer_demande`) lors du routage de la commande.
- L'utilisateur entre dans le 1er knowledge, où les questions pré-remplies sont auto-validées et la dernière question (executer_demande) permet d'exécuter sa demande
- Mettre `demande_executee` à `true` **UNIQUEMENT** quand l'exécution retourne **Vrai** (succès). Si Faux, `demande_executee` reste `false`.
- Quand l'utilisateur fait **Skip** au niveau secondaire en mode initial, traiter comme **Terminer** (afficher grille et finir) plutôt que retourner au principal (puisque le principal n'a qu'un seul élément)

**Mode complet (demande_executee = true) :**
- Afficher avec AskUserQuestion (multiSelect: false) :
  - header: "Principal"
  - question: format `"Choisir. (Si vous avez terminé, appuyez sur Skip)"` — en anglais : `"Choose. (If you are done, press Skip)"`
  - Tous les knowledge lus depuis `methodology-knowledge.md` (le 1er knowledge reste toujours accessible pour relancer l'exécution via A4, y compris pour re-déclencher le mode interactif)
  - **Label du 1er knowledge (Knowledge A)** : puisque `demande_executee` est `true` en mode complet, le 1er knowledge a déjà été exécuté avec succès. Son label doit être modifié pour refléter cet état :
    - label: `"Réexécuter la demande"` (FR) / `"Re-execute request"` (EN) — au lieu du nom original du knowledge
    - description: `"✓"` — le crochet indique que la demande a déjà été exécutée avec succès
  - **Description des autres options (avec indicateur de complétion)** : pour chaque knowledge (autre que le 1er), vérifier si TOUTES les questions de ce knowledge ont été répondues (aucune valeur `"--"` dans les résultats de ce knowledge). Si toutes complétées : description = `"✓"`. Si au moins une question est `"--"` : description = `""` (chaîne vide). Ne PAS afficher les noms génériques ("Knowledge A", etc.) en sous-titre — les vrais noms de la méthodologie sont déjà dans les labels.
  - Appliquer la pagination sans option de contrôle (Skip natif remplace Terminer)
- Si l'utilisateur choisit un knowledge : lancer le Knowledge Secondaire correspondant (questionnaire de validation)
- Si l'utilisateur choisit `Suivant ▸` : incrémenter la page et réafficher
- **Skip** (bouton natif) affiche la grille de résultats et le knowledge est terminé
- Les options restent TOUJOURS visibles (ne jamais retirer une option complétée)
- Boucler jusqu'à ce que l'utilisateur choisisse **Skip**

### Niveau 2 : Knowledge Secondaire

**Décodage et détection automatique des valeurs :**
À la première entrée dans un Knowledge Secondaire, AVANT d'afficher le menu, Claude doit décoder la demande de l'utilisateur et auto-détecter les valeurs correspondant à chaque question (sauf `executer_demande` et `tous`).

**Parsing de la demande utilisateur :**
Le message initial (ou `demande_reformulee` si non null) est structuré ainsi :
1. **Ligne 1** = la commande de l'utilisateur (contient souvent le titre). Exemples : `project create Mon Super Projet`, `build mon-app`
2. **Texte après la ligne 1** (tout ce qui suit, SAUF le bloc JSON `{"resultats": ...}` de pré-remplissage) = la **description** de la demande
3. Le bloc JSON de pré-remplissage (s'il existe) est ignoré pour le décodage — il a déjà été traité au démarrage

**Extraction des valeurs :**
- **A1 (titre)** : extraire le titre **exact** depuis la ligne 1 de la commande, **sans reformulation ni synthèse** (ex: dans `project create Mon Super Projet` → titre = `"Mon Super Projet"`, dans `interactive` → titre = `"interactive"`). C'est le texte brut de l'utilisateur, mot pour mot. Claude ne doit JAMAIS reformuler, capitaliser, ou embellir le titre — c'est l'utilisateur qui choisit son titre via Vrai/Faux/Other au niveau 3.
- **A2 (description)** : extraire tout le texte après la ligne 1 (hors bloc JSON). C'est la description brute de l'utilisateur. **Quand la description existe** (texte non vide après la ligne 1) : `valeur` = le texte exact de l'utilisateur, `original` = `null`. Pas de synthèse, pas de reformulation — le texte de l'utilisateur EST la valeur. **Si la description est absente ou vide** (aucun texte après la ligne 1) : Claude PEUT auto-générer une synthèse contextuelle pour **affichage seulement** (ex: pour `project create Mon App` → valeur = `"Création du projet Mon App"`). La valeur `original` reste `null`. **RÈGLE D'INTÉGRITÉ** : la synthèse auto-générée est un confort d'affichage UNIQUEMENT — elle démontre que Claude a compris la demande. Elle ne doit JAMAIS être utilisée pour classifier, router, ou influencer la nature de l'exécution. Le routage et l'exécution se basent TOUJOURS sur la ligne 1 brute (A1) et le texte original (A2), jamais sur une synthèse.
- **A3 (projet)** : détecter le projet GitHub associé à la demande. Stratégie de détection en cascade :
  0. **Commande de création de projet** : si la commande est `project create [titre]` (route `project-create`), le projet est celui qui est **en cours de création**. A3 = A1 (le titre du nouveau projet). Ne PAS chercher un projet existant — le projet n'existe pas encore. Passer directement à la valeur stockée sans exécuter les étapes 1-4.
  1. **Chercher dans la demande** : analyser le titre (A1) et la description (A2) pour un nom de projet GitHub explicite (ex: `issue dans CC`, `pour le projet test-project-5`)
  2. **Chercher le dernier projet créé** : utiliser `project_list_page(per_page=1)` via `knowledge/engine/scripts/gh_helper.py` pour obtenir le projet le plus récent. Si un projet existe, l'utiliser comme présélection (ex: si le dernier projet créé est `"Mon App"`, présélectionner `"Mon App"`)
  3. **Fallback au repo local** : seulement si aucun projet n'existe sur GitHub (liste vide), vérifier le repo Git courant via `git remote get-url origin` pour extraire le nom du repo (ex: `packetqc/knowledge` → `knowledge`)
  4. **Si aucun match** : mettre `null` — l'utilisateur devra spécifier via le champ texte (Other) au niveau 3
  - La valeur stockée est le nom du projet (ex: `"CC"`, `"MPLIB"`, `"test-project-5"`)
  - **Important** : `gh` CLI utilise la variable d'environnement `GH_TOKEN` déjà présente pour l'authentification. Ne pas demander de token à l'utilisateur.
- **Autres questions** : détecter selon le champ `choix` comme indice sémantique et le contexte du projet

**Format de stockage dans `valeurs_detectees` de `knowledge_resultats.json` :**
```json
"valeurs_detectees": {
  "A1": {"valeur": "Mon Super Projet", "original": null},
  "A2": {"valeur": "Synthèse concise de la description", "original": "Le texte complet de la description fournie par l'utilisateur sur plusieurs lignes..."},
  "A3": {"valeur": "CC", "original": null}
}
```
- `valeur` : la valeur synthétisée/nettoyée par Claude — c'est ce qui sera utilisé par le système en aval
- `original` : le texte brut extrait de la demande (utile surtout pour A2 où l'utilisateur a écrit un long texte). `null` si pas de texte brut distinct (ex: A1 où la valeur est déjà concise)
- Si une valeur ne peut pas être détectée, mettre `{"valeur": null, "original": null}`
- Les valeurs détectées sont recalculées à chaque entrée dans le knowledge secondaire (pour tenir compte de reformulations)

**Auto-validation des valeurs pré-remplies (Knowledge A uniquement) :**
À l'entrée dans le Knowledge Secondaire A, AVANT d'afficher le menu, appliquer l'auto-validation :
- Pour chaque question non-`executer_demande` et non-`tous` du knowledge A (ex: A1, A2, A3) :
  - Si `valeurs_detectees[ID].valeur` est **non null** (une valeur a été détectée) ET le résultat est `"--"` (pas encore répondu) :
    - Mettre automatiquement le résultat à `"Vrai"` dans `knowledge_resultats.json`
    - Ne PAS demander de confirmation à l'utilisateur — la valeur détectée est considérée comme validée
  - Si `valeurs_detectees[ID].valeur` est **null** : le résultat reste `"--"`, l'utilisateur devra sélectionner cette question manuellement
- Les options auto-validées sont affichées dans le menu secondaire avec ✓ (comme si l'utilisateur avait confirmé)
- L'utilisateur peut TOUJOURS cliquer sur une option auto-validée pour la corriger (entre au niveau 3 normalement)
- **Conséquence sur A4** : si toutes les valeurs sont pré-remplies, A1/A2/A3 passent à "Vrai" automatiquement et l'utilisateur peut cliquer directement sur "Exécuter la demande" — une seule action au lieu de 4
- **INTERDIT — Auto-exécution de A4** : Claude NE DOIT JAMAIS lancer l'exécution (A4) automatiquement, même si toutes les conditions sont remplies (A1/A2/A3 tous à "Vrai"). Le menu secondaire DOIT être affiché et l'utilisateur DOIT manuellement sélectionner "Exécuter la demande".

**Affichage du menu :**
Pour chaque knowledge, afficher avec AskUserQuestion :
- header: le nom du knowledge (ex: "Validation")
- question: format `"Choisir parmi les options suivantes. (Pour passer, appuyez sur Skip)"` — en anglais : `"Choose from the following options. (To skip, press Skip)"`
- Lire toutes les questions du knowledge depuis `methodology-knowledge.md`
- **Ordre des options** : si une question de type `tous` existe dans ce knowledge, elle est affichée **en première position** (avant toutes les autres questions). Cela permet à l'utilisateur de lancer "Tous" immédiatement sans paginer.
- **Options `tous` (en premier si présente)** : label du champ `choix`, description vide
- **Options (non-executer_demande, non-tous)** :
  - label: le champ `choix` de la question (ex: "Confirmez le titre")
  - description: la valeur `valeur` de `valeurs_detectees[ID]` (ex: `"Mon Super Projet"`) ou `"(non détecté)"` si `valeur` est null. Si la question est déjà répondue, ajouter un indicateur : `"Mon Super Projet ✓"`
- **Options `executer_demande`** : label "Exécuter la demande", description comme avant
- Appliquer la pagination sans option de contrôle (Skip natif remplace Passer)
- Si l'utilisateur choisit `Suivant ▸` : incrémenter la page (revenir à 0 après la dernière page) et réafficher
- Chaque question lance le Sous-knowledge correspondant
- **Skip** (bouton natif) retourne au Knowledge Principal (et remet `page_secondaire` à 0)
- Les options restent TOUJOURS visibles
- Boucler jusqu'à ce que l'utilisateur choisisse **Skip**

**Retour après reformulation :**
Si on entre dans le Knowledge Secondaire et que `demande_reformulee` est non `null` dans `knowledge_resultats.json`, cela signifie que l'utilisateur a reformulé sa demande après un échec. Dans ce cas :
- Afficher le message : "Vos réponses précédentes sont conservées. Vous pouvez les raffiner avant de procéder à l'exécution."
- Les questions déjà répondues restent accessibles pour raffinement optionnel
- Les prérequis de `executer_demande` sont déjà satisfaits (les réponses précédentes comptent)

### Règle critique : toujours afficher le menu secondaire — JAMAIS d'exécution automatique

**IMPORTANT** : Le menu du Knowledge Secondaire (niveau 2) doit TOUJOURS être affiché avec AskUserQuestion et attendre le choix explicite de l'utilisateur. L'auto-validation met les résultats à "Vrai" en arrière-plan, mais l'EXÉCUTION (A4) n'est JAMAIS déclenchée automatiquement. Le flow est :
1. À l'entrée dans le knowledge secondaire A : auto-valider toutes les questions dont `valeurs_detectees[ID].valeur` est non null → résultat = "Vrai"
2. Afficher le menu secondaire → **ATTENDRE** que l'utilisateur clique sur une option
3. Si l'utilisateur clique sur une question auto-validée → niveau 3 s'affiche normalement (l'utilisateur peut corriger via Vrai/Faux/Passer/Other)
4. **Si l'utilisateur clique sur "Exécuter la demande"** → lancer l'exécution (les auto-validées comptent comme prérequis satisfaits). C'est le SEUL déclencheur valide.
5. Si l'utilisateur fait Skip → retourner au principal ou terminer

> **INTERDIT** : Claude ne doit JAMAIS sauter l'étape 2 (affichage du menu) ni l'étape 4 (clic explicite de l'utilisateur sur A4).
> Même si A1/A2/A3 sont tous "Vrai" et que les conditions sont parfaites, le menu DOIT être affiché et l'utilisateur DOIT cliquer.
> Claude NE DOIT JAMAIS lancer l'exécution avant que l'utilisateur ait cliqué A4.

Les questions auto-validées sont affichées avec ✓ dans la description. L'utilisateur peut y entrer pour corriger mais n'y est PAS obligé. Le cas optimal : tout est pré-rempli → l'utilisateur clique directement "Exécuter la demande".

### Niveau 3 : Sous-knowledge

**Accès direct à la correction des questions déjà répondues :**
Quand l'utilisateur sélectionne une question déjà répondue (≠ `"--"`) au niveau 2, afficher **immédiatement** l'interface de correction complète — ne PAS afficher "déjà répondu" ni retourner au menu secondaire. L'utilisateur doit pouvoir modifier la valeur dès le premier clic :
- Afficher avec AskUserQuestion le choix Vrai/Faux/Passer avec une option supplémentaire `"Garder [valeur actuelle]"` (description: la valeur actuelle)
- Si l'utilisateur choisit **Garder** : conserver la valeur, retourner au Knowledge Secondaire
- Si l'utilisateur choisit **Vrai** : confirmer, retourner au Knowledge Secondaire
- Si l'utilisateur choisit **Faux** : rejeter, enregistrer "Faux", retourner au Knowledge Secondaire
- Si l'utilisateur choisit **Passer** : enregistrer "Passer", retourner au Knowledge Secondaire
- Si l'utilisateur utilise **Other** (champ texte) : traiter comme Vrai avec correction (mettre à jour `valeurs_detectees[ID].valeur`), retourner au Knowledge Secondaire
- Pour le cas spécial A3 (projet), afficher le menu de sélection de projet avec lazy fetch au lieu du choix Garder/Faux/Passer

Pour chaque question, vérifier d'abord le type d'action dans `methodology-knowledge.md` :

**Si l'action est `executer_demande` (ex: A4) :**
- **Prérequis** : vérifier que TOUTES les questions qui précèdent dans ce même knowledge ont été répondues (pas de `"--"`). Les valeurs auto-validées (pré-remplies avec `valeur` non null → résultat "Vrai" automatique) comptent comme répondues. Si une ou plusieurs questions précédentes n'ont pas été répondues :
  - Afficher un message d'avertissement : "Vous devez répondre aux questions précédentes avant d'exécuter la demande."
  - Retourner au Knowledge Secondaire sans exécuter
- Ne PAS afficher de choix Vrai/Faux/Passer à l'utilisateur
- Cette option est entièrement programmatique et non modifiable par l'humain dans le fichier de configuration
- **Déterminer la demande à exécuter** : lire `demande_reformulee` dans `knowledge_resultats.json`. Si non `null`, utiliser cette valeur. Sinon, utiliser le **message initial brut** de l'utilisateur au démarrage de la session. **RÈGLE CRITIQUE** : le routage et la classification de la demande se font TOUJOURS sur le texte brut de l'utilisateur (ligne 1 = commande, lignes suivantes = description). Ne JAMAIS utiliser les valeurs synthétisées (auto-générées quand la description est vide) pour classifier ou router la demande — la synthèse est un confort d'affichage, pas une source de vérité pour l'exécution.
- **Collecter le contexte** : lire dans `knowledge_resultats.json` les réponses ET les valeurs détectées de TOUTES les questions qui précèdent dans ce knowledge. Pour chaque question précédente, inclure le résultat (Vrai/Faux/Passer) et la valeur confirmée/corrigée (champ `valeur` de `valeurs_detectees`). Construire un objet JSON enrichi :
  ```json
  {"A1": {"resultat": "Vrai", "valeur": "Mon Super Projet"}, "A2": {"resultat": "Vrai", "valeur": "Application de gestion de tâches avec interface web"}, "A3": {"resultat": "Vrai", "valeur": "CC"}}
  ```
  Note : les `valeur` transmises via `--context` sont les textes exacts de l'utilisateur (jamais des synthèses). Pour la création du billet GitHub, le titre (A1) et la description (A2) utilisent les valeurs **exactes** validées — `valeur` pour A1, `original` (si non null, sinon `valeur`) pour A2.

**Checkpoint — Vérification pré-exécution (survie à la compaction) :**
Avant de lancer l'exécution, vérifier s'il existe déjà un checkpoint :
```
python3 knowledge/engine/scripts/executer_demande.py --status
```
- **Si checkpoint existe avec `phase: "termine"`** : une exécution précédente s'est terminée (probablement avant une compaction). Ne pas relancer. Lire directement le résultat dans `details.resultat` du checkpoint et dans `.claude/preuve_execution.json`, puis passer à l'étape 4 (vérification de preuve).
- **Si checkpoint existe avec `phase: "en_cours"`** : le programme tournait quand la compaction a eu lieu. Vérifier `.claude/preuve_execution.json` :
  - Si preuve existe → le programme a fini entre-temps → lire le résultat
  - Si pas de preuve → exécution interrompue → relancer l'exécution (étape 1)
- **Si checkpoint existe avec `phase: "pre_execution"`** : le programme n'a pas encore démarré → continuer normalement (étape 1)
- **Si pas de checkpoint** : première exécution → continuer normalement (étape 1)

**Issue GitHub — Journalisation de la demande (non-bloquant) :**
Avant l'exécution, tenter de créer un issue GitHub pour journaliser la demande. Cette étape est **non-bloquante** : si GitHub est indisponible, l'information est persistée sur disque et l'exécution continue normalement. La synchronisation vers GitHub se fait dès que possible.

1. Vérifier l'état actuel de l'issue :
   - Lire `knowledge_resultats.json` → champ `issue_github`
   - **Si `issue_github.numero` existe (non null)** : l'issue existe déjà sur GitHub → passer à l'exécution
   - **Si `issue_github.local_only` est `true`** : données persistées sur disque d'une session précédente → tenter la synchronisation (étape 3), puis passer à l'exécution dans tous les cas
   - **Si `issue_github` est `null` ou absent** : créer l'issue (étape 2)

2. Créer l'issue GitHub via `knowledge/engine/scripts/gh_helper.py` :
   a. Déterminer le repo cible : utiliser la valeur confirmée de A3 (projet) au format `owner/repo`. Si le projet est le repo courant, déduire `owner/repo` depuis l'URL du remote origin.
   b. Construire le titre : utiliser la valeur **exacte** de `valeurs_detectees.A1.valeur` (le titre tel que validé/corrigé par l'utilisateur, JAMAIS re-synthétisé par Claude)
   c. Construire le body : utiliser le texte **exact** de `valeurs_detectees.A2.original` si non null (le texte intégral de l'utilisateur), sinon `valeurs_detectees.A2.valeur`. **CRITIQUE** : le titre et la description dans le billet GitHub doivent être les valeurs ORIGINALES validées par l'utilisateur, pas des reformulations de Claude. La synthèse de Claude (`valeur` pour A2) peut être ajoutée en complément dans le body (ex: "Synthèse: ...") mais ne remplace JAMAIS le texte original.
   d. Tenter la création via Bash :
      ```
      python3 -c "
      from knowledge.engine.scripts.gh_helper import GitHubHelper
      gh = GitHubHelper()
      result = gh.issue_create(repo='<owner/repo>', title='<titre_A1>', body='<description_A2>', labels=['task'])
      import json; print(json.dumps(result))
      "
      ```
   e. **Si la création réussit** (`created: true` dans le résultat) : sauvegarder dans `knowledge_resultats.json` :
      ```json
      "issue_github": {
        "numero": <numero>,
        "repo": "<owner/repo>",
        "url": "<html_url>",
        "node_id": "<node_id>",
        "local_only": false
      }
      ```
      Committer : `git add .claude/knowledge_resultats.json && git commit -m "knowledge: issue GitHub #<numero> créé"`
      Pousser : `git push -u origin <branche-courante>`
      → Passer à l'exécution.
      **Note** : le lien issue → project board se fait **après** l'exécution (voir section post-exécution Vrai).
   f. **Si la création échoue** (erreur réseau, token invalide, etc.) : → **Fallback sur disque** (étape 4), puis passer à l'exécution quand même.

3. **Synchronisation d'un issue local vers GitHub** (reprise après fallback) :
   - Lire les données persistées dans `issue_github` (titre, body, repo)
   - Tenter la création via `gh.issue_create(repo, title, body, labels=['task'])`
   - **Si réussite** : mettre à jour `issue_github` avec `numero`, `url`, `node_id`, et `local_only: false`. Committer et pousser.
   - **Si échec** : GitHub toujours indisponible. Les données restent persistées sur disque pour la prochaine session. L'exécution continue normalement.

4. **Fallback sur disque** (GitHub indisponible) :
   Persister les informations de l'issue localement pour synchronisation ultérieure :
   a. Sauvegarder dans `knowledge_resultats.json` :
      ```json
      "issue_github": {
        "numero": null,
        "repo": "<repo>",
        "url": null,
        "local_only": true,
        "titre": "<titre_A1>",
        "body": "<description_A2>"
      }
      ```
   b. Committer : `git add .claude/knowledge_resultats.json && git commit -m "knowledge: issue persisté sur disque (GitHub indisponible)"`
   c. Pousser : `git push -u origin <branche-courante>`
   d. L'exécution **continue normalement**. À la prochaine session, le knowledge détectera l'issue en attente et tentera la synchronisation automatique (étape 3).

**Note :** Une fois l'issue créé sur GitHub (`local_only: false`), les champs temporaires `titre` et `body` ne sont plus nécessaires — tout pointe vers le système externe.

**Exécution inline (NE PAS utiliser l'outil Skill) :**
L'exécution se fait **directement dans le flow du knowledge-validation** sans appeler de sous-skill. Cela évite les frontières de tour qui interrompent le flow. Toutes les étapes ci-dessous s'enchaînent dans le MÊME tour de réponse.

**Rollback — Snapshot git avant exécution :**
1. Avant d'exécuter, supprimer toute preuve précédente : `rm -f .claude/preuve_execution.json`
2. Créer un snapshot : `git stash --include-untracked -m "snapshot-avant-execution"`
3. **Classifier et router la demande (inline)** :
   a. Lire les routes disponibles : `python3 knowledge/engine/scripts/executer_demande.py --list-routes`
   b. Classifier l'intention de la demande en analysant sémantiquement :
      - Les identifiants de route, descriptions, syntaxe officielle
      - Les mots-clés comme indices (pas comme critères absolus)
      - Détection de syntaxe exacte (ex: `project create Mon Titre` → route `project-create`)
      - Détection en langage naturel (ex: "peux-tu créer le projet X" → route `project-create`, param title = "X")
      - **Règles de matching des commandes multi-mots :**
        - Analyser le champ `syntaxe` de chaque route pour distinguer les commandes simples (un seul mot, ex: `build`) des commandes composées (multi-mots, ex: `project create [title]`)
        - Pour les commandes composées : la demande DOIT contenir tous les mots de la commande (ex: "project create") pour matcher. Le mot primaire seul (ex: "project") ne suffit PAS — il pourrait correspondre à d'autres sous-commandes futures (project view, project list, etc.)
        - Pour les commandes simples (un seul mot, sans sous-commande) : un match sur ce mot unique est suffisant
        - Si la demande contient un mot primaire de commande composée mais sans sous-commande spécifique → **aucune route ne correspond** → traiter comme pas de match
   c. **Si une route correspond ET la route a `type: "interactive"`** : ne PAS exécuter via `executer_demande.py`. Entrer directement dans le **Mode Interactif** (voir section dédiée ci-dessous) :
      - Supprimer le stash créé à l'étape 2 : `git stash drop` (pas de programme à rollback)
      - Exécuter le Mode Interactif (Étapes 1-3 de la section Mode Interactif)
      - **Si l'utilisateur complète la session (terminé/done)** → Résultat = **Vrai** : enregistrer "Vrai" pour A4, mettre `demande_executee` à `true`, sauvegarder, retourner au Knowledge Principal (mode complet)
      - **Si l'utilisateur fait Skip au menu des méthodologies** → Résultat = **Faux** : enregistrer "Faux", proposer la reformulation (voir ci-dessous)
      - **Sauter les étapes 4-5** (vérification de preuve et rollback ne s'appliquent pas au mode interactif)
   d. **Si une route correspond (route standard, sans type spécial)** : exécuter via Bash :
      - Sans paramètres : `python3 knowledge/engine/scripts/executer_demande.py --route <id> --context '<json_contexte>'`
      - Avec paramètres : `python3 knowledge/engine/scripts/executer_demande.py --route <id> --args "<valeur>" --context '<json_contexte>'`
      - Toujours passer `--context` avec le JSON des réponses précédentes
   e. **Si aucune route ne correspond** (ex: "bonjour", "project" seul) : ne rien exécuter → Résultat = **Faux**
   f. **Règles strictes** : NE JAMAIS répondre à la demande, NE JAMAIS inventer une route, NE JAMAIS créer le fichier preuve_execution.json
4. Vérifier la preuve d'exécution (pour les routes standard uniquement, pas pour `type: "interactive"`) :
   - Lire le fichier `.claude/preuve_execution.json` avec l'outil Read
   - **Si le fichier EXISTE** : vérifier `execution_reelle` est `true` et `code_retour` est cohérent. Le `token` SHA-256 prouve l'authenticité.
   - **Si le fichier N'EXISTE PAS** : → Résultat = **Faux**
5. Déterminer le résultat :
   - **Dans TOUS les cas (Vrai OU Faux) — Première passe de compilation (post-exécution) :**
     Compiler les métriques et temps du travail qui vient d'être exécuté, **que l'exécution ait réussi ou échoué**. Cette compilation doit se faire AVANT le rollback (cas Faux) pour capturer les métriques du travail tenté. Le temps passé et les fichiers touchés sont des données importantes même en échec — pour la traçabilité, la documentation, et la gestion du projet.
     - Exécuter `compilation_metriques(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py`
     - Exécuter `compilation_temps(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py`
     - Sauvegarder les résultats de compilation dans `knowledge_resultats.json` sous le champ `compilations_post_execution`, en ajoutant `"resultat_execution": "vrai"` ou `"resultat_execution": "faux"` pour distinguer les compilations d'une exécution réussie de celles d'un échec
   - **Vrai** (preuve existe ET `code_retour` = 0) — étapes obligatoires : commit + push résultats :
     - Supprimer le stash : `git stash drop`
     - Nettoyer : `rm -f .claude/journal_actions.json .claude/preuve_execution.json .claude/checkpoint_execution.json`
     - Enregistrer "Vrai" pour cette question
     - Mettre `demande_executee` à `true`
     - Effacer `demande_reformulee` (remettre à `null` dans `knowledge_resultats.json`)
     - **Poster le résultat sur l'issue GitHub (étape obligatoire — non-bloquant)** : si `issue_github.numero` existe, poster un commentaire de succès via `gh.issue_comment_post(repo, numero, body)` avec :
       ```markdown
       ## Résultat : ✅ Exécution réussie
       **Route** : <route_id>
       **Métriques** : <fichiers changés, additions, deletions depuis compilations_post_execution>
       **Temps** : <calendar_formatted, active_formatted depuis compilations_post_execution>
       ```
     - **Lier l'issue au project board (post-exécution, non-bloquant) :**
       Après une exécution réussie, créer/vérifier le board et lier l'issue. Cette étape est toujours post-exécution pour couvrir uniformément tous les cas (projet existant, nouveau projet créé par A4, ou "Nouveau" choisi à A3).
       1. Déterminer le titre du projet : utiliser `valeurs_detectees.A3.valeur` (le nom du projet confirmé)
       2. Déterminer `owner/repo` depuis git remote origin (jamais depuis A3 — A3 est un nom de projet, pas un repo)
       3. Vérifier si `project_board` existe déjà dans `knowledge_resultats.json` avec un `project_number` valide → si oui, passer directement au lien issue→board (étape 5)
       4. Tenter `project_ensure(titre_projet, owner, repo_name)` via `knowledge/engine/scripts/gh_helper.py` :
          ```
          python3 -c "
          from knowledge.engine.scripts.gh_helper import GitHubHelper
          gh = GitHubHelper()
          result = gh.project_ensure('<titre_A3>', '<owner>', '<repo_name>')
          import json; print(json.dumps(result))
          "
          ```
          Si réussite : sauvegarder dans `knowledge_resultats.json` :
          ```json
          "project_board": {
            "project_id": "<node_id>",
            "project_number": <number>,
            "owner": "<owner>",
            "repo": "<repo>",
            "created": true/false,
            "verified_at": "<ISO timestamp>"
          }
          ```
          Si échec : persister `"project_board": {"local_only": true, ...}` — non bloquant
       5. Si `issue_github.numero` existe et `project_board.project_number` existe : lier l'issue au board via `project_item_add_by_number(owner, project_number, owner/repo, issue_number)`. Si échec, non bloquant.
       6. Committer et pousser les mises à jour
     - Sauvegarder résultats, commit + push → **retourner au Knowledge Principal** (niveau 1, mode complet)
   - **Faux** (pas de preuve OU `code_retour` != 0) — étapes obligatoires : rollback + commit + push résultats :
     - Exécuter le rollback : `python3 knowledge/engine/scripts/executer_demande.py --rollback`
     - Restaurer les fichiers : `git checkout . && git clean -fd`
     - Restaurer le stash : `git stash pop`
     - Nettoyer : `rm -f .claude/preuve_execution.json`
     - **Note** : les compilations (faites avant le rollback) sont conservées dans `knowledge_resultats.json` avec `"resultat_execution": "faux"` — le rollback efface les fichiers de code mais les données de compilation restent pour traçabilité
     - **Poster le résultat sur l'issue GitHub (étape obligatoire — non-bloquant)** : **ne PAS fermer l'issue** — elle reste ouverte pour journaliser le déroulement. Si `issue_github.numero` existe, poster un commentaire d'échec via `gh.issue_comment_post(repo, numero, body)` avec :
       ```markdown
       ## Résultat : ❌ Exécution échouée
       **Route** : <route_id>
       **Erreur** : <code_retour ou message d'erreur>
       **Métriques** : <fichiers changés, additions, deletions depuis compilations_post_execution>
       **Temps** : <calendar_formatted, active_formatted depuis compilations_post_execution>
       Rollback effectué. Reformulation en cours.
       ```
     - Enregistrer "Faux" pour cette question
     - Sauvegarder résultats → proposer la reformulation (voir ci-dessous)

**Reformulation après échec :**
Quand l'exécution retourne Faux, NE PAS retourner directement au Knowledge Secondaire. À la place :
1. Afficher avec AskUserQuestion :
   - header: "Reformuler"
   - question: "L'exécution a échoué. Souhaitez-vous reformuler votre demande ?"
   - options:
     - `Reformuler` (description: "Tapez votre nouvelle demande via le champ texte 'Other'")
     - `Continuer sans reformuler` (description: "Conserver le résultat Faux et retourner au quiz")
2. Si l'utilisateur choisit **"Other"** (champ texte libre) : c'est sa nouvelle demande reformulée
   - Sauvegarder le texte saisi comme `demande_reformulee` dans `knowledge_resultats.json`
   - **Retourner au Knowledge Secondaire** (pas directement à l'exécution)
   - Afficher le message : "Vos réponses précédentes sont conservées. Vous pouvez les raffiner avant de procéder à l'exécution."
   - Les questions déjà répondues (ex: A1, A2) restent accessibles pour raffinement mais ne bloquent PAS l'accès à "Exécuter la demande" (les prérequis sont déjà satisfaits)
   - Quand l'utilisateur choisit "Exécuter la demande" (A3), utiliser la `demande_reformulee` au lieu de la demande initiale
3. Si l'utilisateur choisit **"Reformuler"** : lui redemander via AskUserQuestion avec un champ texte
4. Si l'utilisateur choisit **"Continuer sans reformuler"** : conserver Faux, retourner au Knowledge Secondaire
- Retourner automatiquement au Knowledge Secondaire

**Gestion de la demande reformulée :**
- Le champ `demande_reformulee` dans `knowledge_resultats.json` contient la dernière reformulation (ou `null` si pas de reformulation)
- Lors de l'exécution (A3), la priorité est : `demande_reformulee` > demande initiale de session
- Après une exécution **Vrai**, effacer `demande_reformulee` (remettre à `null`)
- Après une nouvelle reformulation, écraser la valeur précédente

**Tâches collatérales (v2.0) :**
Pendant l'exécution d'une demande (mode normal ou interactif), des sous-demandes internes peuvent être déclenchées automatiquement (ex: créer un issue collatéral pour un bug découvert, générer de la documentation suite à un changement). Ces tâches collatérales sont enregistrées dans `collateral_tasks[]` dans `knowledge_resultats.json` :
```json
"collateral_tasks": [
  {
    "id": "ct-001",
    "title": "Fix CSS dark mode regression",
    "type": "fix",
    "status": "completed",
    "issue_number": 55,
    "created_at": "2026-03-08T15:00:00Z",
    "pr_numbers": [56]
  }
]
```
Chaque tâche collatérale :
- Est créée comme issue GitHub (si disponible) avec label `task` et lien vers l'issue principale
- Si GitHub indisponible : persistée localement dans `collateral_tasks[]`, synchronisée plus tard
- Est liée à la session utilisateur via le `user_session_id` partagé
- Apparaît dans le Session Viewer et le Task Viewer comme sous-tâche de la tâche principale

**Si l'action est `tous` (ex: B4, C4, D3, E3, E4) — OBLIGATOIRE :**

> **CRITIQUE** : "Tous" est un raccourci programmatique. Quand l'utilisateur clique "Tous",
> Claude DOIT exécuter automatiquement CHAQUE question du knowledge comme si l'utilisateur
> avait répondu "Vrai" à chacune. C'est l'équivalent d'un batch — pas un simple label.
> Après exécution, le retour au Knowledge Principal est OBLIGATOIRE (si tout réussit).

- Cette action est **programmatique** — ne PAS afficher de choix Vrai/Faux/Passer
- Quand l'utilisateur sélectionne cette option au niveau secondaire, exécuter cette séquence COMPLÈTE :
  1. **Itérer** automatiquement à travers TOUTES les autres questions du même knowledge (celles qui ne sont PAS de type `tous`), dans l'ordre de leurs IDs
  2. **Pour chaque question** : exécuter l'action associée comme si l'utilisateur avait répondu **Vrai** (afficher le message, déclencher la fonction/programme si applicable)
  3. **Pour chaque question** : enregistrer "Vrai" si l'exécution a réussi, "Faux" si elle a échoué
  4. **Sauvegarder** les résultats dans `knowledge_resultats.json` et committer
  5. **Évaluer le résultat global :**
     - **Si TOUTES les questions ont réussi (toutes Vrai)** :
       - Enregistrer "Vrai" pour la question `tous` elle-même
       - Afficher le message associé à la question `tous`
       - **Retourner directement au Knowledge Principal** (pas au secondaire — tout est fait, inutile de rester)
     - **Si AU MOINS UNE question a échoué (au moins un Faux)** :
       - Enregistrer "Faux" pour la question `tous`
       - Afficher un récapitulatif des résultats : pour chaque question, indiquer le statut (Vrai/Faux)
       - **Rester au Knowledge Secondaire** pour permettre à l'utilisateur de re-sélectionner individuellement les questions en échec
  6. **Ne JAMAIS s'arrêter avant d'avoir complété la séquence** — "Tous" déclenche un pipeline complet, pas une confirmation passive

- Ce type d'action est **réutilisable** par n'importe quel knowledge qui souhaite offrir un raccourci "tout faire d'un coup"

**Pour toutes les autres actions (fonction, programme) :**
- **Lecture de methodology pré-exécution** : avant d'exécuter l'action, vérifier si le knowledge parent a un champ `methodology` dans sa configuration (ex: `methodology: methodology-documentation` dans le header du knowledge). Si oui :
  1. Lire le fichier `knowledge/methodology/<methodology>.md` avec l'outil Read (ex: `knowledge/methodology/methodology-documentation.md`)
  2. Utiliser les instructions de cette methodology pour guider l'exécution de la fonction/programme
  3. Cela permet à Claude d'être spécialisé pour la tâche sans charger toutes les methodologies en mémoire
- Si pas de champ `methodology` : exécuter normalement sans lecture supplémentaire
- **Afficher avec AskUserQuestion :**
  - header: l'identifiant de la question (ex: "A1")
  - **Construction de la question** — deux cas selon que `original` existe ou non dans `valeurs_detectees[ID]` :
    - **Si `original` est non null** (ex: A2 description — l'utilisateur a écrit un long texte) :
      La question doit montrer les DEUX versions pour comparaison :
      ```
      Confirmez: <valeur (synthèse)>

      Texte original: <original>
      ```
      Exemple pour A2 :
      ```
      Confirmez: Application de gestion de tâches avec interface web

      Texte original: Je veux créer une application qui permet de gérer des tâches, avec une interface web moderne, des notifications, et un système de priorités...
      ```
      L'utilisateur voit la synthèse de Claude ET son texte original, et peut juger si la synthèse est fidèle. Ce qui sera utilisé en aval par le système, c'est la `valeur` (la synthèse), pas l'original.
    - **Si `original` est null** (ex: A1 titre — valeur déjà concise) :
      Question simple : `"Confirmez: <valeur>"` (ex: `"Confirmez: Mon Super Projet"`)
      - **Cas spécial A3 (projet) — Sélection de projet avec lazy fetch paginé :**
        Au lieu d'un simple "Confirmez", A3 affiche un **menu de sélection de projet** avec chargement paresseux :
        1. Charger les projets **par page de 3** via `project_list_page` (lazy fetch) :
           ```
           python3 -c "
           from knowledge.engine.scripts.gh_helper import GitHubHelper
           gh = GitHubHelper()
           page = gh.project_list_page(per_page=3)  # Page 1 (pas de cursor)
           import json; print(json.dumps(page))
           # page = {'projects': [...], 'next_cursor': '...', 'has_next': True/False}
           "
           ```
           - **Ne PAS** utiliser `project_list()` (charge tout d'un coup) — utiliser `project_list_page()` qui ne charge que 3 projets à la fois.
           - Les projets sont déjà triés du plus récent au plus ancien par l'API.
           - Pour la page suivante : `gh.project_list_page(per_page=3, cursor=page['next_cursor'])`
        2. Afficher avec AskUserQuestion (multiSelect: false) :
           - header: "A3"
           - question: `"Choisir le projet pour cette demande."`
           - **Page 1 spéciale** : `"Nouveau"` en option 1 + les 3 premiers projets (4 options max, dont `Suivant ▸` si `has_next`)
             - Si `has_next` est True ET qu'il y a déjà "Nouveau" + 3 projets : remplacer le 3e projet par `Suivant ▸` (garder max 4 options)
             - Sinon : afficher "Nouveau" + les 3 projets normalement
           - **Pages suivantes** : 3 projets + `Suivant ▸` si `has_next` (4 options max)
           - label: le nom du projet (ex: `"knowledge"`, `"One-Liner"`)
           - description: `"#<number>"`. Si le projet correspond à la valeur pré-détectée (`valeurs_detectees.A3.valeur`), ajouter `" (détecté)"` à la description.
           - Appliquer la pagination : 3 éléments + `Suivant ▸` si `has_next` (toujours max 4 options AskUserQuestion)
        4. **Si l'utilisateur choisit un projet existant** :
           - Mettre à jour `valeurs_detectees.A3.valeur` avec le nom du projet choisi
           - Enregistrer "Vrai" pour A3
           - Afficher le message associé
           - Retourner au Knowledge Secondaire
           - **Important** : si un project board GitHub existe déjà pour ce projet (même `project_number`), le réutiliser — ne PAS en créer un nouveau
        5. **Si l'utilisateur choisit "Nouveau"** :
           - Afficher un sous-AskUserQuestion :
             - header: "Projet"
             - question: `"Entrez le nom du nouveau projet via le champ texte (Other)."`
             - options: `"Annuler"` (description: `"Retour à la sélection de projet"`) — minimum 2 options requis, le choix principal est via Other
           - Si l'utilisateur tape un nom (Other) : mettre à jour `valeurs_detectees.A3.valeur`, enregistrer "Vrai", retourner au Knowledge Secondaire
           - Si l'utilisateur choisit "Annuler" : retourner au menu de sélection de projet
        6. **Si l'utilisateur fait Skip** : enregistrer "Passer", retourner au Knowledge Secondaire
    - **Si `valeur` est null** : `"Confirmez: (non détecté)"`
  - options: utiliser les choix définis dans `sous_knowledge.choix` de `methodology-knowledge.md` (Vrai, Faux, Passer)
    - **Vrai** : confirme la synthèse. Enregistrer "Vrai", conserver `valeurs_detectees`, afficher le message associé, retourner au Knowledge Secondaire
    - **Faux** : rejette la synthèse. Enregistrer "Faux", retourner au Knowledge Secondaire
    - **Passer** : enregistrer "Passer", retourner au Knowledge Secondaire
    - **Other (champ texte libre)** : l'utilisateur tape une **valeur corrigée** (reformulation, précision, ou réécriture complète). Traiter comme **Vrai** avec correction :
      - Mettre à jour `valeurs_detectees[ID].valeur` avec la nouvelle valeur saisie (la synthèse est remplacée)
      - L'`original` reste inchangé (c'est le texte brut de l'utilisateur)
      - Enregistrer "Vrai" pour cette question
      - Afficher le message associé
      - Retourner au Knowledge Secondaire
    - Au retour au Knowledge Secondaire, la description de l'option reflètera la valeur mise à jour

### Mode Interactif

Le mode interactif permet à l'utilisateur d'entrer dans une session de travail libre guidée par une méthodologie interactive. C'est un mode alternatif à l'exécution programmatique (A4/executer_demande).

**Déclenchement :**
- Via `executer_demande` (A4) : quand la route détectée a `type: "interactive"`, le flow entre dans le Mode Interactif au lieu d'exécuter un programme
- Fonctionne aussi bien en mode initial (première exécution A4) qu'en mode complet (re-exécution via Knowledge A → A4)

**Étape 1 — Menu de sélection de la méthodologie interactive :**
1. Scanner le répertoire `knowledge/methodology/` pour tous les fichiers correspondant au pattern `interactive-*.md` (utiliser l'outil Glob avec `knowledge/methodology/interactive-*.md`)
2. Pour chaque fichier trouvé :
   - Extraire le nom lisible depuis la première ligne `# Titre` du fichier (lire les 3 premières lignes avec Read)
   - Le nom de fichier (sans `interactive-` et `.md`) sert d'identifiant (ex: `conception`, `diagnostic`, `documentation`, `work-sessions`)
3. Afficher avec AskUserQuestion (multiSelect: false) :
   - header: `"Interactif"` (FR) / `"Interactive"` (EN)
   - question: `"Choisir le type de session interactive. (Pour annuler, appuyez sur Skip)"` — en anglais : `"Choose the interactive session type. (To cancel, press Skip)"`
   - Options : une par fichier `interactive-*.md` trouvé
     - label: le titre extrait du fichier (ex: `"Interactive Conception"`, `"Interactive Diagnostic"`)
     - description: chaîne vide `""`
   - Appliquer la pagination si plus de 4 fichiers (même règles que la pagination standard)
4. **Skip** au menu interactif :
   - En mode initial : traiter comme **Terminer** (afficher grille et finir)
   - En mode complet : retourner au menu principal

**Étape 2 — Entrée en session interactive :**
1. Lire le fichier méthodologie sélectionné en entier avec l'outil Read (ex: `knowledge/methodology/methodology-interactive-diagnostic.md`)
2. **Afficher la demande originale et la synthèse** — avant de commencer le travail, rappeler le contexte :
   - Lire `valeurs_detectees` dans `knowledge_resultats.json`
   - Afficher :
     ```
     ═══════════════════════════════════════════
     SESSION INTERACTIVE — <Titre de la méthodologie>
     ═══════════════════════════════════════════
     Tapez "terminé" ou "done" pour terminer la session.

     📋 Demande originale :
     > <valeurs_detectees.A2.original si non null, sinon valeurs_detectees.A2.valeur>

     📝 Synthèse :
     > <valeurs_detectees.A2.valeur>
     ```
3. **Afficher le help automatiquement (message de bienvenue)** — immédiatement après la bannière, exécuter la commande `help` pour annoncer que la session est prête et montrer les commandes disponibles :
   ```
   python3 knowledge/engine/scripts/executer_demande.py --route help --context '<json_contexte>'
   ```
   Afficher la sortie du programme. C'est le signal visuel que la session interactive est opérationnelle.
4. **Démarrage automatique si la description contient des instructions claires** :
   - Analyser `valeurs_detectees.A2` (original et valeur) pour déterminer si la description contient des instructions suffisamment précises pour démarrer les premiers travaux
   - **Si la description contient des instructions actionnables** (verbes d'action, tâches identifiables, objectifs clairs) : commencer directement le travail selon la méthodologie, sans demander à l'utilisateur quoi faire
   - **Si la description est vague ou absente** (pas d'instructions claires, description générique, ou `valeur` null) : demander à l'utilisateur ce qu'il souhaite travailler dans cette session
5. **Mode ligne de commande libre** : Claude entre dans un mode de travail collaboratif avec l'utilisateur :
   - Claude suit les instructions et principes de la méthodologie lue
   - L'utilisateur est libre d'écrire ce qu'il veut — demandes, instructions, questions
   - Claude répond et travaille normalement selon la méthodologie
   - **Pas de quiz**, pas de choix forcés — c'est une session de travail libre
6. **Détection de sortie — OBLIGATOIRE** : après CHAQUE message de l'utilisateur, vérifier **en priorité absolue** si le message est exactement ou commence par :
   - `terminé` ou `Terminé` ou `TERMINÉ` (FR)
   - `done` ou `Done` ou `DONE` (EN)
   - **Si détecté : ARRÊTER IMMÉDIATEMENT la session interactive et exécuter l'Étape 3 en entier.** Ne PAS répondre "session terminée" et s'arrêter — l'Étape 3 est OBLIGATOIRE et inclut le retour au Knowledge Principal.
   - Sinon : continuer la session normalement

**Étape 3 — Sortie, enregistrement et retour au quiz (ÉTAPE OBLIGATOIRE — TOUTES les sous-étapes) :**

> **CRITIQUE** : Cette étape doit être exécutée EN ENTIER quand l'utilisateur tape "terminé"/"done".
> Ne JAMAIS s'arrêter après avoir affiché "SESSION INTERACTIVE TERMINÉE".
> Le retour au Knowledge Principal (sous-étape 5) est OBLIGATOIRE.

1. Afficher un message de fin :
   ```
   ═══════════════════════════════════════════
   SESSION INTERACTIVE TERMINÉE
   ═══════════════════════════════════════════
   ```
2. Enregistrer le résultat **Vrai** pour la dernière question du 1er knowledge (A4)
3. Sauvegarder dans `knowledge_resultats.json` :
   - Mettre à jour le résultat A4 = "Vrai"
   - Mettre `demande_executee` à `true`
   - Ajouter un champ `interactive_session` dans `knowledge_resultats.json` :
     ```json
     "interactive_session": {
       "methodology": "methodology-interactive-<type>.md",
       "completed": true
     }
     ```
4. **Première passe de compilation (post-exécution)** : compiler les métriques et temps du travail de la session interactive AVANT le retour au quiz. Cela nourrit les étapes de validation (B, C, D) avec des données concrètes :
   - Exécuter `compilation_metriques(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py`
   - Exécuter `compilation_temps(resultats, incremental=True)` depuis `knowledge/engine/scripts/knowledge_skills.py`
   - Sauvegarder les résultats de compilation dans `knowledge_resultats.json` sous le champ `compilations_post_execution`
5. **Lier l'issue au project board (post-exécution, non-bloquant)** — même logique que pour les routes standard (voir section Vrai du sous-knowledge executer_demande) : project_ensure + project_item_add_by_number. Non-bloquant si GitHub indisponible.
6. Committer et pousser comme pour toute mise à jour du knowledge
7. **RETOUR AU KNOWLEDGE PRINCIPAL — OBLIGATOIRE** :
   - `demande_executee` est maintenant `true` → le Knowledge Principal passe en **mode complet**
   - Afficher IMMÉDIATEMENT le menu Knowledge Principal (AskUserQuestion avec tous les knowledge disponibles)
   - L'utilisateur peut alors choisir quel knowledge valider (B, C, D, E) ou faire Skip pour voir la grille
   - **Ne JAMAIS s'arrêter ici** — le quiz DOIT continuer jusqu'à ce que l'utilisateur fasse Skip au niveau principal
   - Si Skip au menu principal → afficher la grille des résultats et terminer le knowledge

   > En résumé : "terminé"/"done" → bannière → sauvegarde → commit → **menu principal du quiz** (pas d'arrêt entre)

   - Skip au menu des méthodologies (avant d'entrer en session) → Résultat Faux → le flow `executer_demande` traite comme un échec et propose la reformulation

**Persistance (survie au compactage) :**
- L'état de la session interactive est persisté via `interactive_session` dans `knowledge_resultats.json`
- Si après compactage, `interactive_session.completed` est `true` : la session est terminée, ne pas relancer
- Si après compactage, `interactive_session` existe mais `completed` est `false` : la session était en cours. Afficher : "Session interactive interrompue par compactage. Résultat enregistré comme Vrai." puis enregistrer Vrai et continuer

### Grille de résultats

Quand l'utilisateur fait **Skip** au niveau principal, construire et afficher un tableau dynamique basé sur les knowledge et questions présents dans `methodology-knowledge.md` :

- **Lignes** : une par knowledge trouvé, en utilisant le **nom FR du knowledge** tel que défini dans `methodology-knowledge.md` (ex: "Validation de la demande", "Qualité du travail", "Intégrité de session", "Documentation", "Approbation"). Si le nom est trop long, le tronquer pour garder la grille lisible (max ~20 caractères).
- **Colonnes** : utiliser les **IDs des questions** tels que définis dans `methodology-knowledge.md` (ex: A1, A2, A3, B1, B2...). Chaque knowledge affiche ses propres IDs comme en-têtes de colonnes.
- **Valeurs** : remplacer par la réponse (Vrai, Faux, Passer) ou `--` si non répondu
- **Largeur de colonne** : 10 caractères, valeurs centrées

Exemple avec les 5 knowledge :
```
                    GRILLE DE RÉSULTATS
+---------------------+----------+----------+----------+----------+
|                     |    A1    |    A2    |    A3    |    A4    |
+=====================+==========+==========+==========+==========+
| Valid. demande      |   Vrai   |   Vrai   |   Vrai   |   Vrai   |
+---------------------+----------+----------+----------+----------+
|                     |    B1    |    B2    |    B3    |    B4    |
+---------------------+----------+----------+----------+----------+
| Qualité travail     |    --    |   Vrai   |    --    |    --    |
+---------------------+----------+----------+----------+----------+
|                     |    C1    |    C2    |    C3    |    C4    |
+---------------------+----------+----------+----------+----------+
| Intégrité session   |  Faux    |    --    |   Vrai   |    --    |
+---------------------+----------+----------+----------+----------+
|                     |    D1    |    D2    |    D3    |
+---------------------+----------+----------+----------+
| Documentation       |    --    |    --    |    --    |
+---------------------+----------+----------+----------+
|                     |    E1    |    E2    |    E3    |
+---------------------+----------+----------+----------+
| Approbation         |    --    |    --    |    --    |
+---------------------+----------+----------+----------+
```
Chaque knowledge a sa propre rangée d'en-têtes avec ses IDs, suivie de sa rangée de valeurs. Cela permet de supporter des nombres de colonnes différents par knowledge.

**Message de fin conditionnel :** Après la grille, vérifier si toutes les questions de tous les knowledge ont été répondues (aucune valeur `"--"` dans les résultats) :
- **Si complet** (aucun `"--"`) : afficher `message_fin_complet` de `methodology-knowledge.md`
- **Si incomplet** (au moins un `"--"`) : afficher `message_fin_incomplet` de `methodology-knowledge.md`

**Publication de la grille sur l'issue GitHub :**
Après l'affichage de la grille, si `issue_github.numero` existe (non null, synchronisé vers GitHub), poster un commentaire sur l'issue via `knowledge/engine/scripts/gh_helper.py` :
```python
from knowledge.engine.scripts.gh_helper import GitHubHelper
gh = GitHubHelper()
gh.issue_comment_post(repo='<owner/repo>', issue_number=<numero>, body='<grille_markdown>')
```
Le body du commentaire doit contenir :
- La grille de résultats en format markdown (même contenu que celui affiché à l'utilisateur)
- Le message de fin (complet ou incomplet)
- Si `local_only: true` (GitHub était indisponible), ne pas tenter le commentaire — les données restent sur disque pour la prochaine session.

**Fonctions post-grille :** Ces fonctions (définies dans `knowledge/engine/scripts/knowledge_skills.py`) sont appelées par le flux knowledge-validation aux étapes 6-9 ci-dessus :
1. `compilation_metriques(resultats)` — Compile les métriques. Si des changements sont détectés, met `_documentation_requise = True`
2. `compilation_temps(resultats)` — Compile le temps. Si des changements sont détectés, met `_documentation_requise = True`
3. `pre_sauvegarde(resultats)` — Étape 8 : exécute les règles de conformité pré-sauvegarde. Première sous-fonction : `confirmation_documentation`. D'autres règles suivront.
4. `sauvegarde(resultats)` — Sauvegarde les résultats (compile sessions.json + tasks.json pour les interfaces web)

**Mécanisme du flag `_documentation_requise` — cycle de vie :**
1. **Exécution démarre (A3)** → `reset_documentation_requise()` → flag = `False` (ardoise propre — on ne sait pas encore s'il y aura des changements)
2. **Compilations** (étapes 6-7) → détectent des changements → `set_documentation_requise()` → flag = `True` (documentation requise car changements détectés)
3. **`confirmation_documentation`** (sous-fonction de `pre_sauvegarde`, étape 8) → **compare deux valeurs** :
   - Le flag interne `_documentation_requise` (True si les compilations ont détecté des changements)
   - Le résultat de l'étape Documentation dans le quiz (dernière rangée du tableau des résultats = dernier knowledge au niveau principal, à venir)
   - **Flag `False`** → passe (pas de changements, rien à documenter)
   - **Flag `True` + résultat doc `Vrai`** → passe (l'utilisateur a documenté)
   - **Flag `True` + résultat doc `--`/`Faux`/`Passer`** → suggérer via AskUserQuestion (rappel de discipline, pas un bloqueur — l'utilisateur peut Skip, il repassera dans ~15 min)

Ces fonctions sont **toujours** exécutées après la grille, que le quiz soit complet ou non. L'appel se fait via `from knowledge_skills import compilation_metriques, compilation_temps, pre_sauvegarde, sauvegarde`.

### Important

- Si l'utilisateur sélectionne "No preference", "Other" ou **Skip** dans AskUserQuestion :
  - Au niveau principal : traiter comme **Terminer** (afficher grille et finir)
  - Au niveau secondaire en mode initial (`demande_executee = false`) : traiter aussi comme **Terminer** (afficher grille et finir), car le principal n'a qu'un seul élément
  - Au niveau secondaire en mode complet (`demande_executee = true`) : traiter comme **retour au Knowledge Principal** (et remettre `page_secondaire` à 0)
- Toujours montrer le message de la fonction/programme quand Vrai est sélectionné AVANT de retourner au niveau supérieur.
- **CRITIQUE** : Après un compactage de session, TOUJOURS lire `.claude/knowledge_resultats.json` pour retrouver l'état du knowledge avant de continuer.
