---
name: jira
description: Récupère le contexte d'un ticket Jira via le MCP Atlassian, résume ce qui est compris, identifie les fichiers impactés du codebase avec liens, et propose une ou plusieurs stratégies d'implémentation. Rapport console uniquement. Aucune modification du code ni écriture Jira — lecture seule.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
---

# Jira — Analyse de ticket et proposition de stratégie

Skill **lecture seule**. Récupère le contexte d'un ticket Jira via le MCP Atlassian, le résume, identifie les impacts dans le codebase, et propose une stratégie d'implémentation. N'écrit **jamais** dans le code ni dans Jira.

## Étape 0 — Configuration (au 1er run uniquement)

Le skill lit la **config partagée** `~/.claude/skills-config/ticket-prefix.json` (mutualisée avec d'autres skills comme `/pre-commit`).

**Si le fichier existe** → charger `prefix` et passer à l'étape 1.

**Si le fichier n'existe pas** → setup interactif via `AskUserQuestion` :

> "Quel est le pattern des tickets de ton projet Jira ? (utilisé pour résoudre les références ticket et normaliser les inputs)"
>
> Choix proposés :
> - `ALX-XXXX`
> - `JIRA-XXXX`
> - `PROJ-XXXX`
> - `Autre` (saisie libre — préfixe seul, ex: `ACME`)
> - `Pas de pattern fixe` (le skill demandera le préfixe à chaque appel sans préfixe explicite)

Sauvegarder dans `~/.claude/skills-config/ticket-prefix.json` :

```json
{
  "prefix": "ALX",
  "configuredAt": "YYYY-MM-DD"
}
```

Si le user choisit "Pas de pattern fixe" → sauvegarder `{ "prefix": null, "configuredAt": "YYYY-MM-DD" }`.

**Reconfiguration** : si le user lance `/jira --setup`, re-poser la question. La nouvelle valeur sera vue par tous les skills qui partagent cette config.

Créer le dossier `~/.claude/skills-config/` s'il n'existe pas avant l'écriture.

## Étape 1 — Résoudre l'identifiant du ticket

L'utilisateur peut passer le ticket sous différentes formes : `ALX-4981`, `alx-4981`, `Alx-4981`, ou juste `4981`.

### Cas 1 — Argument avec préfixe explicite (ex: `ALX-4981` ou `proj-123`)

Normaliser en majuscules → `<PREFIX>-<NUMBER>` et passer à l'étape 2.

### Cas 2 — Argument sans préfixe (ex: juste `4981`)

1. Lire la config (`prefix` dans `ticket-prefix.json`).
2. **Si `prefix` configuré** → préfixer automatiquement : `4981` + `prefix=ALX` → `ALX-4981`.
3. **Si `prefix` est `null`** (pas de pattern fixe) → demander à l'utilisateur via `AskUserQuestion` : *"Tu as donné le numéro `4981` sans préfixe. Quel est le préfixe du projet pour cette recherche ?"* Ne **pas** sauvegarder cette réponse (one-shot, le user a explicitement choisi "pas de pattern fixe").

### Cas 3 — Aucun argument fourni

1. Chercher un pattern de ticket dans le nom de la branche courante (`git branch --show-current`).
   - Si `prefix` configuré → chercher `<PREFIX>-\d+`
   - Sinon → chercher `[A-Z]{2,10}-\d+` (regex générique)
2. **Si trouvé** → utiliser (normalisé en majuscules).
3. **Sinon** → répondre :
   ```
   Aucun ticket fourni et aucun trouvé dans le nom de la branche.
   Usage : /jira <TICKET-ID> ou /jira <NUMBER> (préfixe ajouté automatiquement si configuré).
   ```
   et s'arrêter.

## Étape 2 — Fetcher le ticket via MCP Atlassian

Utiliser l'outil MCP `mcp__atlassian__getJiraIssue` :
- Besoin du `cloudId` → appeler `mcp__atlassian__getAccessibleAtlassianResources` d'abord si non connu en session.
- Champ `issueIdOrKey` = `<PREFIX>-<NUMBER>` (résolu à l'étape 1).

Récupérer :
- Titre (`summary`)
- Description (`description`)
- Statut (`status`)
- Priorité, type, assignee
- Labels et composants
- Liens (sous-tickets, blockers, related)
- Derniers commentaires pertinents

**Pas d'écriture Jira jamais** — ni comment, ni transition, ni modif, ni worklog.

**Si le MCP Atlassian n'est pas configuré ou refuse l'accès** → afficher :
```
⚠️  Le MCP Atlassian n'est pas accessible. Pour utiliser ce skill :
    1. Vérifie que le MCP Atlassian est installé : claude mcp list
    2. Authentifie-toi : suis la procédure de ton MCP Atlassian
    3. Relance `/jira <TICKET-ID>`
```
et stop.

## Étape 3 — Explorer les tickets similaires (Jira)

Pour enrichir la proposition, chercher des tickets similaires via `mcp__atlassian__searchJiraIssuesUsingJql` avec une JQL du style :

```
project = <PREFIX> AND (component = "<composant>" OR labels = "<label>") AND resolution = Fixed ORDER BY updated DESC
```

Où :
- `<PREFIX>` = la valeur de `prefix` configuré, OU le préfixe du ticket courant si pas de config
- `<composant>` / `<label>` extraits du ticket actuel

Limiter à ~5-10 résultats. Ne pas sur-consommer.

Extraire de ces tickets similaires :
- Patterns de solution récurrents (mentionnés dans les commentaires des tickets résolus)
- Pièges connus
- Liens vers PR / commits si présents dans les commentaires

**Si aucun ticket similaire trouvé** → pas grave, passer à l'étape 4 sans cette section.

## Étape 4 — Identifier les fichiers impactés du codebase

En partant du ticket (description + mots-clés), chercher dans le code du projet courant :

1. Identifier les **entités / composants** mentionnés dans le ticket (ex: "facture", "panier", "auth" → chercher `invoice-*`, `cart-*`, `auth-*`).
2. Utiliser `Glob` / `Grep` sur le workspace courant :
   ```
   src/**/*<mot-clé>*.{ts,html,tsx,jsx}
   ```
3. Filtrer sur les fichiers **pertinents** : composants, services, utils, policies, interfaces du domaine.
4. Pour chaque fichier identifié, noter :
   - **Chemin absolu complet** (pour ouverture directe depuis le terminal)
   - **Rôle** en 1 phrase (lu depuis le fichier)
   - **Nature de l'impact probable** : lecture, modif, création, suppression

## Étape 5 — Produire le rapport console

Format :

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Ticket <PREFIX>-XXXX — <Titre>
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 Ce que j'ai compris
  <résumé du besoin / bug en 3-6 phrases>
  <critères d'acceptation clés si présents>

🔗 Contexte Jira (méta)
  Statut     : ...
  Priorité   : ...
  Composants : ...
  Labels     : ...
  Sous-tickets / blockers (s'il y en a) : [liste avec liens]

📁 Fichiers impactés (probables)
  1. /chemin/absolu/vers/foo.service.ts
     → rôle : <1 phrase>
     → impact : modification de la méthode `bar()`
  2. /chemin/absolu/vers/foo.component.ts
     → rôle : ...
     → impact : ajout d'un nouveau case dans le switch du template

📚 Tickets similaires (pour inspiration)
  - <PREFIX>-YYYY (résolu)
    Patterns utilisés : <synthèse depuis le ticket>
  - <PREFIX>-ZZZZ (résolu)
    Solution appliquée : ...

💡 Stratégies proposées

### Option A — <nom court>
Plan :
  1. <étape>
  2. <étape>
Fichiers à toucher : [liste courte]
Complexité : simple / moyen / complexe
Risque de régression : faible / moyen / élevé
Tests à ajouter : [liste]

### Option B — <nom court>  [si pertinent]
Plan :
  ...
Complexité : ...
Risque : ...

[Si une seule option évidente → une seule présentée, mention "pas d'alternative raisonnable"]

⚠️ Points d'attention / risques
  - <risque spécifique>
  - <contrainte non évidente>

❓ Questions pour toi (si applicable)
  - <question qui bloque avant implémentation>

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⏸️  En attente de ton feedback. Je ne touche à aucun fichier
   tant que tu ne me dis pas "go Option A", "go B", ou
   d'autres instructions précises.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Étape 6 — Sous-tickets (si présents)

Si le ticket fetché a des sous-tickets (via `issuelinks` ou champ `subtasks`) :

- Les **lister** dans le bloc "🔗 Contexte Jira" avec titre + statut.
- **Demander** à l'utilisateur : "Ce ticket a N sous-tickets. Tu veux que je descende dans chacun (relance `/jira <SUB-TICKET>`) ou on reste sur le ticket parent ?"
- **Ne pas** auto-fetcher chaque sous-ticket (coût tokens + bruit).

## Règles absolues

- **Lecture seule partout** :
  - Pas d'écriture Jira (pas de `addCommentToJiraIssue`, `transitionJiraIssue`, `editJiraIssue`, `addWorklogToJiraIssue`).
  - Pas de modification de code : le skill propose, l'utilisateur exécute.
- **L'écriture dans `~/.claude/skills-config/`** se limite au seul fichier `ticket-prefix.json` (config partagée). Aucun autre fichier n'est touché.
- **Aucune commande git écrivante** (lecture de la branche OK).
- **Langue** : rapport en français. Les citations du ticket gardent la langue d'origine.
- **Chemins absolus complets** pour les fichiers impactés (permet l'ouverture directe depuis le terminal).
- **Attente d'accord explicite** avant toute action : le skill termine par la ligne "En attente de ton feedback".
- **Si le ticket n'est pas accessible** (permissions MCP refusées, ticket inexistant) → rapporter clairement l'erreur et s'arrêter, pas de fallback créatif.
- **Si le MCP Atlassian n'est pas configuré** → expliquer comment l'installer et arrêter.
