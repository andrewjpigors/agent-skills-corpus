---
name: review
description: Code review complète des dernières modifications (diff vs branche principale). Vérifie signal-first Angular, performance templates, RxJS, clean code, sécurité, régressions. S'adapte aux conventions du projet via CLAUDE.md. Rapport structuré avec sévérités et corrections proposées.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Agent
---

# Code Review — Modifications récentes

## Étape 1 : Récupérer le contexte

1. Identifie la branche principale (`dev`, `main`, ou `master`) via `git remote show origin` ou les conventions du repo.
2. Récupère le diff complet de la branche courante vs la branche principale : `git diff <main-branch>...HEAD`
3. Liste les fichiers modifiés : `git diff --name-only <main-branch>...HEAD`
4. Lis intégralement chaque fichier modifié pour avoir le contexte complet (pas juste le diff).
5. Lis le fichier `CLAUDE.md` à la racine du projet s'il existe — il contient les conventions du projet. Respecte-les dans ton analyse, elles **priment** sur les règles génériques ci-dessous.

## Étape 2 : Analyser selon ces critères

### 2.1 Angular & Signals (Signal-First)

- Les nouveaux composants utilisent-ils `input()`, `output()`, `viewChild()`, `model()` (jamais `@Input`/`@Output`/`@ViewChild`) ?
- L'état local utilise-t-il `signal()` et `computed()` (pas de `BehaviorSubject` sauf flux RxJS complexes) ?
- Les `effect()` sont-ils ciblés (un effect = une responsabilité) ? Pas d'effect fourre-tout ?
- Aucun `toObservable(signal).subscribe()` (anti-pattern → utiliser `effect()`) ?
- Les formulaires utilisent-ils `computed()` au lieu de fonctions `FormGroupInit` ?
- `ChangeDetectionStrategy.OnPush` est-il défini sur tous les nouveaux composants ?
- `inject()` est-il utilisé systématiquement (jamais d'injection via constructor) ?
- La syntaxe template Angular 19+ est-elle utilisée (`@if`, `@for`, `@switch`) ?

### 2.2 Performance & Templates

- **RÈGLE CRITIQUE : Aucune expression complexe ni condition dans les templates.** Toute logique (conditions, transformations, concaténations, ternaires) doit être extraite dans un `computed()` et appelée dans le template via `monComputed()`. Raison : les expressions dans les templates sont réévaluées à chaque cycle de change detection, même avec OnPush. Un `computed()` ne recalcule que lorsque ses dépendances changent.
- Y a-t-il des appels de fonctions dans les templates qui devraient être des `computed()` ?
- **Risque de boucles infinies** (🔴 CRITIQUE) : effect qui modifie un signal qu'il lit, cascade infinie effect→signal→computed→effect, circular dependency entre computed, valueChanges → patchValue sans `emitEvent: false`.
- Les subscriptions RxJS longues sont-elles correctement nettoyées (`takeUntilDestroyed`, `DestroyRef`) ?
- Y a-t-il des fuites mémoire potentielles (event listeners non retirés, observers orphelins, timers non cleared, sockets non disconnect) ?
- Les listes utilisent-elles `track` dans les `@for` ?
- Les appels API sont-ils correctement dédupliqués (pas de double-fetch) ?

### 2.2.bis RxJS subscribe — error handler & finalize

**Si le projet a un `ErrorInterceptor` global** (vérifier dans `app.config.ts` / `provideHttpClient` / `HTTP_INTERCEPTORS`) :

- Un `subscribe({ error })` dont le handler fait **uniquement** du logging / toast générique est **redondant** → supprimer, laisser l'interceptor. Garder l'error local seulement si la gestion est contextuelle (404 → fallback, 409 → side panel, retry custom).
- **Cleanup dupliqué** entre `next` et `error` (loader off, reset state) → déplacer dans `finalize()`. Le `next` ne garde que la logique de succès.

**Sinon** (pas d'interceptor global) : ne pas flagger les error handlers locaux, ils sont nécessaires.

### 2.2.ter Avoid-first — setTimeout & magic numbers

- **`setTimeout` / `setInterval`** : flag tout setTimeout du diff. Outil toléré mais **pas en 1ère intention**. Avant de l'accepter, chercher :
  - `effect()` / `afterNextRender()` / `afterRender()` pour attendre la CD
  - `queueMicrotask()` / `Promise.resolve().then()` pour différer d'un tick (plus lisible que `setTimeout(..., 0)`)
  - `debounceTime(N)` RxJS pour un debounce input user
  - `timer(0, N).pipe(takeUntilDestroyed())` pour un polling (cleanup inclus)
  - Dette back si c'est une race condition serveur

  Si l'alternative est pertinente (résout mieux, ou plus propre) → la proposer. Sinon, tolérer le `setTimeout` **mais exiger un commentaire justificatif** à côté. Cas **🔴 Critique** : `setTimeout(() => signal.set(...), 0)` (anti-pattern), `setInterval` sans cleanup.

- **Magic numbers** : valeurs numériques métier (seuils, durées, tailles) en dur → extraire en `const NOM_PARLANT = ...;`. Tolérer : indices triviaux (0, 1, -1), arithmétique évidente (/100), code 1-2 lignes avec sens auto-explicite.

### 2.3 Clean Code (DRY, KISS, SOLID)

- Y a-t-il du code dupliqué qui devrait être factorisé ?
- Les composants ont-ils une responsabilité unique ? Faut-il extraire de la logique dans un service ?
- Le code est-il inutilement complexe ? Peut-on simplifier ?
- Les noms de variables/méthodes sont-ils clairs et descriptifs ?
- Y a-t-il du code mort, commenté, ou des `console.log` oubliés ?
- Les types sont-ils stricts (pas de `any` évitable) ?

### 2.4 Maintenabilité & Architecture

- Les types/interfaces sont-ils au bon endroit (dossier `core/interfaces/`, `types/`, ou équivalent documenté dans `CLAUDE.md`) ?
- Les services suivent-ils les patterns du projet (séparation entity vs feature, ou structure documentée dans `CLAUDE.md`) ?
- Le code suit-il les conventions décrites dans `CLAUDE.md` ?

### 2.4.bis Conventions projet (depuis `CLAUDE.md`)

**Étape obligatoire** : si `CLAUDE.md` projet existe et documente des conventions spécifiques, les appliquer comme checks. Exemples typiques de conventions à chercher dans `CLAUDE.md` :

- **Form controls custom** : si le projet a des composants comme `<app-select>`, `<app-multi-select>`, `<app-textarea>`, etc. documentés → flagger l'usage des contrôles bruts (PrimeNG, HTML natif) à la place.
- **Pièges connus** : si `CLAUDE.md` documente un piège (ex: "ButtonComponent utilise content projection, pas d'input `label`") → flagger les violations.
- **Renommages tiers** : si `CLAUDE.md` documente une migration de lib (ex: "PrimeNG 19 : `<p-inputSwitch>` → `<p-toggleswitch>`") → flagger l'ancien nom.
- **Patterns de service** : si `CLAUDE.md` documente une structure (ex: "services entity dans `core/services/entities/`") → flagger les fichiers mal placés.
- **Side panels vs popups** : si `CLAUDE.md` documente une migration → flagger l'usage du legacy.

**Règle générale** : tout ce qui est dans `CLAUDE.md` projet est **prioritaire** et doit être checké. Le skill ne hardcode aucune convention spécifique — il s'adapte au projet via `CLAUDE.md`.

### 2.5 Régressions & Sécurité

- Le code modifié peut-il casser des fonctionnalités existantes ?
- Les droits/permissions sont-ils vérifiés là où nécessaire (RBAC service, guards, etc.) ?
- Y a-t-il des risques XSS (`innerHTML` non sanitizé, `bypassSecurityTrust*` injustifié) ?
- Les inputs utilisateur sont-ils validés ?

## Étape 3 : Produire le rapport

### Tableau des problèmes

Pour chaque problème trouvé, indique :

| # | Sévérité | Fichier:Ligne | Catégorie | Problème | Correction proposée |
|---|----------|---------------|-----------|----------|---------------------|

Sévérités :
- 🔴 **Critique** — Bug, fuite mémoire, boucle infinie, faille sécurité, régression
- 🟡 **Important** — Anti-pattern, violation convention, dette technique significative
- 🔵 **Mineur** — Amélioration de lisibilité, nommage, simplification possible

### Résumé

- **Points positifs** du code produit
- **Nombre de problèmes** par sévérité
- **Top 3 des corrections prioritaires** avec explication du pourquoi

### Proposition de corrections

Pour chaque problème 🔴 et 🟡, propose le code corrigé (avant/après).

## Règles absolues

- **Aucune modification de code** — rapport seulement. Le développeur applique les fixes.
- **Aucune commande git écrivante** au-delà de `git status`, `git diff`, `git log`, `git branch --show-current` (lecture seule).
- **Conventions projet > règles génériques** : si `CLAUDE.md` projet définit une exception ou un pattern différent, suivre la règle projet et ne pas flagger.
- **Langue** : rapport en français.
