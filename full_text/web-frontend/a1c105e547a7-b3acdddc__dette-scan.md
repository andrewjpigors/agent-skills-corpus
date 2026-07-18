---
name: dette-scan
description: Détecte la dette technique d'un projet Angular (anti-patterns bannis, signaux non-migrés, RxJS migrable, conventions projet violées). Par défaut analyse les fichiers modifiés sur la branche courante. Findings taggés par catégorie + gravité + fix proposé. S'adapte aux conventions projet via CLAUDE.md. Aucune modification de code, rapport console seulement.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# Dette-scan — Détection de dette technique Angular

Analyse statique pour repérer les anti-patterns Angular et les opportunités de migration vers les conventions modernes (signal-first, OnPush, control flow Angular 17+, etc.) ainsi que les conventions spécifiques du projet documentées dans `CLAUDE.md`.

**Aucune modification de code source** — rapport console uniquement.

## Étape 1 — Détection du scope

### Mode par défaut (sans argument) — branche courante

```bash
git status --porcelain
git diff --name-only dev...HEAD 2>/dev/null || git diff --name-only main...HEAD 2>/dev/null || git diff --name-only master...HEAD
```

Filtrer pour ne garder que :
- `*.ts` (sauf `.spec.ts`, `.test.ts`, `.d.ts`, `.module.ts`, `.routes.ts`)
- `*.component.ts`, `*.service.ts`, `*.directive.ts`, `*.guard.ts`, `*.interceptor.ts`, `*.pipe.ts`, `*.util.ts`
- `*.component.html`, `*.component.scss` (pour les checks UI/template)

Exclure :
- `core/interfaces/`, `core/types/` (pas de logique testable)
- `node_modules/`, `dist/`, `.angular/`
- Add-ins / manifestes XML

### Mode argument explicite

```
/dette-scan src/app/ui/pages/foo/foo.component.ts
/dette-scan src/app/ui/pages/bar/
```

- Chemin fichier → audit ce fichier
- Chemin dossier → audit récursif

### Mode `--all` (snapshot global, opt-in)

```
/dette-scan --all
```

Scan complet du repo. **Output différent** : agrégé par pattern, pas finding par finding (sinon illisible).

- Top 10 fichiers les plus dégradés (par nombre de findings pondérés)
- Compteur par catégorie (ex: "47 fichiers utilisent encore `BehaviorSubject`")

Si `--all` → demander confirmation avant lancement (peut prendre 1-3 min sur 100+ services).

**Note** : ce mode est console-only. Pas de persistance des résultats. Si tu veux comparer entre deux runs, copie l'output dans un fichier perso.

### Mode filtres

```
/dette-scan --signals          # uniquement [SIGNALS]
/dette-scan --rxjs             # uniquement [RXJS]
/dette-scan --blocking         # uniquement les findings 🔴
```

Si scope vide → "Aucun fichier modifié à scanner." et s'arrêter.

## Étape 2 — Lecture du contexte projet

Lire en début de scan (cache pour la session) :

1. **`CLAUDE.md` du projet** — conventions documentées (anti-patterns spécifiques au projet, form controls custom, pièges connus, migrations en cours). **Les règles documentées priment sur les règles génériques** ci-dessous.
2. **`tsconfig.json`** pour détecter le mode strict et adapter les checks `any`.

## Étape 3 — Catégories d'audit

Chaque finding est **taggé** + **gravité** + **fix proposé**.

### 🚦 [SIGNALS] — Migration signal-first

#### Inputs / Outputs / ViewChild legacy

- 🟠 `@Input()` → préférer `input()` ou `input.required<T>()`
- 🟠 `@Output()` → préférer `output<T>()`
- 🟠 `@ViewChild()` → préférer `viewChild<T>()` ou `viewChild.required<T>()`
- 🟠 `@ContentChild()` / `@ContentChildren()` → équivalents signal

#### Cycle de vie

- 🟠 `ngOnInit()` qui pourrait être remplacé par `constructor()` + `effect()` (sauf si interaction avec parent post-mount qui justifie ngOnInit — rare)
- 🔴 `ngOnInit()` ET `constructor()` qui font tous les deux du setup → confusion, à consolider

#### State

- 🟠 `BehaviorSubject` privé utilisé uniquement en interne → migrable en `signal()`
- 🟠 `Subject<void>` utilisé pour trigger refresh → préférer pattern `_version = signal(0)` + `update(v => v+1)`
- 🟠 `@Input() set foo()` setter → `input()` + `effect()` pour réagir au changement
- 🔴 `.value` ou `.next()` appelé sur ce qui devrait être un signal (anti-pattern de migration partielle)
- 🔴 `.pipe()` appelé sur un signal (impossible — confusion avec Observable)

#### Templates

- 🟠 Fonction appelée dans le template (`{{ computeStuff() }}`, `[disabled]="isDisabled()"` quand `isDisabled` est une méthode) → préférer `computed()`
- 🟠 `*ngIf` / `*ngFor` / `*ngSwitch` → préférer `@if` / `@for` / `@switch` (Angular 17+ control flow)

### 🌊 [RXJS] — RxJS à éliminer ou simplifier

#### Anti-patterns

- 🔴 `toObservable(signal).subscribe()` → utiliser `effect()` à la place
- 🔴 `toSignal(toObservable(signal))` → passer le signal directement
- 🟠 Subscription RxJS sans `takeUntilDestroyed()` ni `DestroyRef` (potentielle fuite mémoire)
- 🟠 `UntilDestroy` décorateur sur un POST/PUT/PATCH/DELETE one-shot → inutile (le subscribe se termine de lui-même)

#### Patterns migrables

- 🟠 `Observable<T>` retourné par un service GET → migrer en `Signal<T>` via `toSignal(...switchMap..., { initialValue })`
- 🟡 `combineLatest` de 2 BehaviorSubject → `computed()` de 2 signaux

### 🔧 [QUALITY] — Qualité code générale

#### TypeScript

- 🔴 `as any` dans le code (sauf justifié par commentaire pour API legacy/lib non-typée)
- 🟠 `: any` en annotation explicite (préférer `unknown` + narrowing)
- 🟠 Type retour omis sur méthode publique d'un service (lecture difficile)
- 🟡 `let` quand `const` suffit

#### Anti-patterns Angular bannis

- 🔴 `setTimeout(..., N)` comme workaround de synchro (sauf cas justifié type debounce/throttle)
- 🔴 Effect "fourre-tout" qui fait > 3 responsabilités distinctes (un effect = une responsabilité nommée)
- 🟠 Nom de variable cryptique (1-2 lettres, abréviations non standard)
- 🟠 Méthode > 50 lignes ou avec > 4 niveaux d'imbrication

#### Commentaires

- 🟠 Commentaire avec **prénom d'utilisateur** ou **numéro de ticket** dans le code (TODO, JSDoc, inline) — ces infos appartiennent au commit message ou au PR, pas au code (rot rapidement, pas portables, deviennent obsolètes).
- 🟡 Commentaire qui paraphrase le code (le quoi) au lieu d'expliquer le pourquoi
- 🟡 Code mort, code commenté, `console.log`/`debug`/`info` oubliés

### 💧 [LEAKS] — Fuites mémoire potentielles

- 🔴 `subscription.subscribe()` sans gestion du nettoyage (`takeUntilDestroyed`, `DestroyRef`, manuel)
- 🔴 `setInterval` / `setTimeout` long sans `clearInterval` / `clearTimeout`
- 🔴 `addEventListener` sur `window`, `document` ou DOM sans `removeEventListener`
- 🔴 `ResizeObserver` / `IntersectionObserver` / `MutationObserver` instancié sans `.disconnect()`
- 🟠 `socket.on(...)` sans `socket.off(...)`

### 🔁 [LOOPS] — Boucles infinies / cascades

- 🔴 `effect()` qui **set** un signal qu'il **read** dans la même fonction (sauf garde anti-boucle documentée par un commentaire)
- 🟠 `computed()` A qui dépend de `computed()` B qui dépend de A (circularité)
- 🟠 `effect()` qui dépend de `> 5 signaux` distincts → effect fourre-tout, à splitter

### 🏷️ [PROJECT] — Conventions projet (depuis `CLAUDE.md`)

**Étape obligatoire** : si `CLAUDE.md` projet existe et documente des anti-patterns ou conventions spécifiques, les appliquer comme checks supplémentaires. Exemples typiques :

- **Form controls custom** : si le projet a des composants comme `<app-select>`, `<app-multi-select>`, `<app-textarea>`, `<app-button>` documentés → flagger l'usage des contrôles bruts (PrimeNG, HTML natif) à la place quand le custom existe.
- **Pièges API documentés** : si `CLAUDE.md` documente un piège (ex: "ButtonComponent utilise content projection, pas d'input `label`") → flagger les violations.
- **Renommages tiers** : si `CLAUDE.md` documente une migration de lib (ex: "PrimeNG 19 : `<p-inputSwitch>` → `<p-toggleswitch>`") → flagger l'ancien nom.
- **Patterns de service** : si `CLAUDE.md` documente une structure (ex: "services entity dans `core/services/entities/`") → flagger les fichiers mal placés.
- **Migrations en cours** : si `CLAUDE.md` documente une migration legacy → moderne (ex: PopupService → SidePanelService) → flagger l'usage du legacy.

**Règle générale** : tout ce qui est dans `CLAUDE.md` projet est **prioritaire** et doit être checké. Le skill ne hardcode aucune convention spécifique — il s'adapte au projet via `CLAUDE.md`.

## Étape 4 — Format du rapport

### Mode par défaut (branche / chemin)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dette-scan — N fichier(s) analysé(s)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scope : <branche courante | chemin explicite>
Filtres actifs : <aucun | --signals | etc.>

────────────────────────────────
Résumé
────────────────────────────────

🔴 X bloquant(s)   — anti-pattern projet ou risque (leaks/loops)
🟠 Y important(s)  — migration recommandée
🟡 Z suggestion(s) — amélioration opportuniste

Par catégorie :
  🚦 [SIGNALS]  : a (🔴 b / 🟠 c / 🟡 d)
  🌊 [RXJS]     : ...
  🔧 [QUALITY]  : ...
  💧 [LEAKS]    : ...
  🔁 [LOOPS]    : ...
  🏷️ [PROJECT]  : ...

────────────────────────────────
Findings — src/app/ui/.../foo.component.ts
────────────────────────────────

🔴 [LEAKS] Subscription non nettoyée
   Ligne 42 : this.userService.user$.subscribe(...)
   Problème : pas de takeUntilDestroyed() ni DestroyRef → fuite à chaque destruction du composant.
   Fix proposé :
     this.userService.user$
       .pipe(takeUntilDestroyed())
       .subscribe(...)

🟠 [SIGNALS] @Input legacy
   Ligne 28 : @Input() id!: number;
   Problème : `@Input` décorateur déprécié dans le projet (signal-first).
   Fix proposé : `readonly id = input.required<number>();`

🟠 [PROJECT] Form-control brut au lieu du composant projet
   Ligne 105 (template) : <p-dropdown [options]="states" ...>
   Problème : le projet documente `<app-select>` qui gère required/erreurs/labels (cf. CLAUDE.md).
   Fix proposé : <app-select [options]="states" formControlName="state" label="État" />

🟡 [QUALITY] `let` au lieu de `const`
   Ligne 67 : let amount = this.computeAmount();
   Problème : la variable n'est jamais réassignée.
   Fix proposé : `const amount = this.computeAmount();`

────────────────────────────────
Findings — src/app/ui/.../bar.service.ts
────────────────────────────────

[...]
```

### Mode `--all` (snapshot global, console-only)

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dette-scan global — repo complet
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Scanné : 1 247 fichiers TS/HTML
Durée  : 2m 14s

────────────────────────────────
Vue d'ensemble
────────────────────────────────

[SIGNALS]  47 fichiers avec @Input / @Output / @ViewChild legacy
           23 fichiers avec ngOnInit migrable
           18 fichiers avec BehaviorSubject migrable

[RXJS]      9 fichiers avec subscribe() sans takeUntilDestroyed
            4 fichiers avec UntilDestroy sur POST/PUT/PATCH

[QUALITY]  12 occurrences de `as any`
            3 setTimeout magique non documenté
            8 méthodes > 50 lignes

[LEAKS]     2 ResizeObserver sans disconnect
            1 setInterval non cleared

[LOOPS]     0 effect read+set détecté

[PROJECT]   6 fichiers avec contrôles bruts au lieu des form-controls custom (cf. CLAUDE.md)
            2 fichiers avec ancien composant déprécié documenté

────────────────────────────────
Top 10 fichiers les plus dégradés
────────────────────────────────

  1. src/app/ui/pages/foo/foo.component.ts (12 findings, 3 🔴)
  2. src/app/core/services/entities/bar.service.ts (9 findings)
  3. ...

────────────────────────────────
Note
────────────────────────────────

Mode console-only : aucune persistance. Pour comparer entre deux runs,
copie l'output dans un fichier perso.
```

## Règles absolues

- **Aucune modification de code source** — rapport console seulement. Le développeur applique les fixes lui-même.
- **Aucune écriture de fichier** — le skill n'écrit nulle part, il affiche.
- **Aucune commande git** au-delà de `git status`, `git diff --name-only`, `git branch --show-current` (lecture seule).
- **Détection vs faux positifs** : préférer ne **pas** remonter un finding incertain plutôt que polluer le rapport. Mieux vaut 10 findings sûrs que 50 dilués.
- **Convention projet > règle générique** : si `CLAUDE.md` projet définit une exception (ex: pattern `_version + switchMap` autorisé, garde anti-boucle documentée pour un cas spécifique), respecter l'exception et ne pas flagger.
- **Volume `--all`** : avertir avant lancement. Stop si l'utilisateur n'a pas confirmé.
- **Langue** : rapport en **français**, descriptions en français, fix proposés en code (anglais des identifiers conservé).
- **Pas de double-scan** : si le même finding apparaît dans plusieurs fichiers (ex: même ligne dupliquée), le mentionner une fois avec un compteur.
- **Confidentialité** : ne jamais lire ni mentionner `.env*`, secrets, configs perso.
