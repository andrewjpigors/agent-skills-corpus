---
name: pre-commit
description: Génère un brouillon de message de commit Conventional Commits en anglais à partir des fichiers modifiés sur la branche courante, et signale les console.log/debug/info oubliés. Jamais d'exécution git, uniquement un brouillon à copier.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Write, AskUserQuestion
---

# Pre-commit — Brouillon de message + check console.log

Commande simple : vérifier qu'il ne reste pas de `console.log` oubliés, puis générer un message de commit prêt à copier.

**JAMAIS d'exécution git**. Uniquement un brouillon affiché.

## Étape 0 — Configuration (au 1er run uniquement)

Le skill lit la **config partagée** `~/.claude/skills-config/ticket-prefix.json` (mutualisée avec d'autres skills comme `/jira` qui ont besoin du même préfixe).

**Si le fichier existe** → charger `prefix` et passer à l'étape 1.

**Si le fichier n'existe pas** → setup interactif via `AskUserQuestion` :

> "Quel est le pattern des tickets de ton projet ? (utilisé pour préfixer le commit message et résoudre les références ticket dans plusieurs skills)"
>
> Choix proposés :
> - `ALX-XXXX`
> - `JIRA-XXXX`
> - `PROJ-XXXX`
> - `Autre` (saisie libre — préfixe seul, ex: `ACME`)
> - `Pas de pattern fixe / auto-detect`

Sauvegarder dans `~/.claude/skills-config/ticket-prefix.json` :

```json
{
  "prefix": "ALX",
  "configuredAt": "YYYY-MM-DD"
}
```

Si le user choisit "Pas de pattern fixe" → sauvegarder `{ "prefix": null, "configuredAt": "YYYY-MM-DD" }`. Le skill bascule en auto-detect (regex `[A-Z]{2,10}-\d+`).

**Reconfiguration** : si le user lance `/pre-commit --setup`, re-poser la question (utile si changement de projet). La nouvelle valeur sera vue par tous les skills qui partagent cette config.

Créer le dossier `~/.claude/skills-config/` s'il n'existe pas avant l'écriture.

## Étape 1 — Récupérer les fichiers modifiés

```bash
git status --porcelain
```

Collecter :
- `SCOPE_STAGED` : fichiers avec `M`, `A`, `D`, `R` en première colonne (staged)
- `SCOPE_UNSTAGED` : fichiers avec `M`, `A`, `D` en deuxième colonne OU `??` (unstaged / untracked)
- `SCOPE_ALL` = staged + unstaged (on regarde tout ce que l'utilisateur pourrait commiter)

Si `SCOPE_ALL` est vide → afficher "Rien à committer." et s'arrêter.

Lire aussi :
- Le nom de la branche courante : `git branch --show-current` → pour détecter un éventuel ticket
- Les 5 derniers commits pour calquer le style : `git log -5 --pretty=format:'%s'`

## Étape 2 — Check `console.log` oubliés

Pour chaque fichier du scope (hors `.md`, `.json`, binaires) :

```bash
grep -nE "^\s*console\.(log|debug|info)\(" <fichier>
```

- Matche uniquement les lignes **non commentées** (pas de `//` ou `/*` en début de ligne après trim).
- `console.warn` et `console.error` sont **tolérés** (utilisés pour du vrai logging défensif).

Si des matches sont trouvés → les afficher en tête du rapport sous forme de **warning** (pas bloquant — juste visible). Format :

```
⚠️ console.log oubliés détectés :
  - src/auth/login.ts:42 → console.log('debug user', user)
  - src/services/api.ts:128  → console.debug(response)

À nettoyer avant de commiter (ou ignorer si c'est un log volontaire).
```

Si aucun match → ne rien afficher, passer directement à l'étape 3.

## Étape 3 — Analyser le diff pour le message de commit

Récupérer le diff complet sur `SCOPE_ALL` :

```bash
git diff HEAD -- <fichiers>
```

Lire les fichiers modifiés si nécessaire pour comprendre le **pourquoi** du changement (pas juste le quoi).

### Choix du type Conventional Commits

Selon la nature dominante du changement :

- `feat` — nouvelle fonctionnalité utilisateur
- `fix` — correction de bug
- `refactor` — restructuration sans changement de comportement observable
- `perf` — amélioration de performance
- `chore` — outillage, config, dépendances, docs internes
- `test` — ajout/modification de tests
- `docs` — documentation utilisateur / README
- `style` — formatage pur (rare, souvent fait par le linter)

**En cas d'ambiguïté** (commit mixte) : choisir le type qui reflète l'**intention principale**. Si vraiment multi-sujets → proposer de séparer en plusieurs commits (note dans le rapport, pas bloquant).

### Choix du scope

Déduire du chemin des fichiers modifiés. Exemples :

- Fichiers dans `auth/` → `auth`
- Fichiers dans `cart/` → `cart`
- Fichiers dans `dashboard/` → `dashboard`
- Services dans `services/user/` → `user`
- Multi-scope → omettre le scope OU prendre le plus représentatif

Si unclear → omettre le scope (`fix: ...` au lieu de `fix(xxx): ...`).

Calquer également le **style observé dans les 5 derniers commits** (lus à l'étape 1) — si le repo n'utilise jamais de scope, ne pas en imposer un. Si le repo a une convention (ex: scope toujours présent, kebab-case vs camelCase), s'y conformer.

### Référence ticket

1. Lire la config partagée dans `~/.claude/skills-config/ticket-prefix.json`.
2. **Si `prefix` est configuré** (ex: `ALX`) → chercher `<PREFIX>-\d+` dans le nom de la branche courante.
3. **Si `prefix` est `null`** (auto-detect) → chercher pattern générique `[A-Z]{2,10}-\d+` dans la branche.
4. **Si trouvé** → inclure à la fin du subject entre parenthèses, ex : `fix(auth): refresh token on 401 (PROJ-1234)`.
5. **Si la branche ne contient pas de ticket** → pas d'ajout.

### Subject

- **Anglais obligatoire**
- Verbe à l'impératif présent (`add`, `fix`, `refresh`, `update`, NOT `added` / `adds`)
- `< 70 caractères` idéalement
- Pas de point final
- Clair, factuel, pas marketing

### Body (optionnel)

Ajouter un body en dessous du subject (ligne vide entre les deux) **uniquement si** :

- Le pourquoi n'est pas évident depuis le code
- Le changement a une contrainte non triviale (race condition, compat back, dette)
- Plusieurs fichiers orthogonaux sont touchés et ça mérite un contexte

Sinon : subject seul suffit. Pas de body pour meubler.

## Étape 4 — Rapport final

Format de sortie :

```
[Warnings console.log si présents — voir Étape 2]

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Brouillon de message de commit
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

type(scope): subject line here (PROJ-1234)

Optional body explaining the why if non-obvious.
Multiple paragraphs allowed.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Fichiers inclus :
  - src/auth/login.ts
  - src/auth/login.test.ts

[Si multi-sujets détectés]
ℹ️ Ce commit couvre plusieurs sujets distincts. Tu peux splitter si tu veux :
   → Commit A : [fichiers X, Y] — subject A
   → Commit B : [fichiers Z]    — subject B
```

## Règles absolues

- **JAMAIS d'exécution git** au-delà de `git status`, `git diff`, `git log`, `git branch --show-current` (lecture seule uniquement).
- **Jamais de `git add` / `git commit` / `git push`** — l'utilisateur exécute lui-même son commit après avoir copié le brouillon.
- **Le message est un BROUILLON** présenté pour que l'utilisateur copie-colle. Aucune action automatique.
- **Langue du rapport** : français. **Langue du message de commit** : anglais.
- Si fichiers sensibles détectés dans le scope (`.env*`, configs perso, secrets) → mentionner en warning, mais ne pas bloquer (l'utilisateur décide).
- L'écriture dans `~/.claude/skills-config/` se limite au seul fichier `ticket-prefix.json` (config partagée). Aucun autre fichier n'est touché.
