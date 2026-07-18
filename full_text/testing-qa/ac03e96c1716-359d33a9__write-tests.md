---
name: write-tests
description: Génère des tests unitaires Vitest pour les fichiers modifiés sur la branche courante (et leurs impacts proches). Focus qualité métier — edge cases, cas tordus, règles complexes — pas les getters triviaux. Écrit les .spec.ts à côté du fichier source, puis exécute vitest et rapporte le résultat. Détecte d'autres frameworks (Jest / Karma) et propose une mise à jour du skill si nécessaire.
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash, Edit, Write, AskUserQuestion
---

# Write-tests — Génération de tests unitaires Vitest

Génère des tests pour le périmètre en cours d'édition. Focus **qualité** : règles métier, edge cases, cas tordus. Pas les getters triviaux.

**Framework cible : Vitest.** Si un autre framework est détecté, le skill propose de se mettre à jour.

## Étape 0 — Détection du framework de test

Lire `package.json` à la racine du projet. Détecter dans cet ordre :

1. **Vitest** (`vitest` dans `devDependencies`) → continuer normalement.
2. **Jest** (`jest` dans `devDependencies`) → afficher :

   > "Ce skill est écrit pour Vitest, mais ton projet utilise Jest. Tu peux :
   > - **A.** Demander à Claude d'étendre ce skill à Jest. Les templates sont dans `~/.claude/skills/write-tests/SKILL.md`. Prompt suggéré : *« Mets à jour write-tests pour supporter aussi Jest : adapter imports, mocks (jest.fn vs vi.fn), commande d'exécution. »*
   > - **B.** Continuer quand même : les patterns AAA, TestBed Angular et la philosophie restent valides, mais tu adapteras manuellement les imports/mocks."

   Demander via `AskUserQuestion` lequel choisir. Si A → stop (l'utilisateur ira étendre le skill). Si B → continuer en mode "best-effort Jest" (pas de templates fournis, on s'inspire des templates Vitest et l'utilisateur ajuste).

3. **Karma + Jasmine** (`karma` + `jasmine-core`) → même flow que Jest, message adapté.
4. **Aucun** → afficher : "Aucun framework de test détecté dans `package.json`. Skill conçu pour Vitest. Installe Vitest (`npm i -D vitest`) et relance, ou étends ce skill pour ton framework." et stop.

Si plusieurs frameworks détectés (cas rare, ex: migration en cours) → demander via `AskUserQuestion` lequel utiliser.

## Étape 1 — Détection du périmètre

Objectif : identifier les fichiers du **changement en cours** (working tree + branche courante) ET leurs dépendances de proximité.

1. **Working tree + staged** : `git status --porcelain` → fichiers modifiés/ajoutés.
2. **Diff branche** : `git diff --name-only <main>...HEAD` où `<main>` = `dev` / `main` / `master` (détecter via `git remote show origin` ou convention).
3. **Union** → `SCOPE_DIRECT`.
4. **Dépendances de proximité** : pour chaque fichier de `SCOPE_DIRECT` :
   - Fichiers qui **importent** ce fichier (impact amont) : `grep -rE "from.*['\"].*<basename sans .ts>" src/`
   - Fichiers qu'il **importe** localement (`./` ou `../`) (impact aval)
   - Profondeur limitée à 1 niveau pour garder le scope raisonnable.
5. **Filtrer** :
   - Garder : `.ts` sauf `.spec.ts`, `.test.ts`, `.d.ts`, `index.ts` (barrel)
   - Exclure : `*.interface.ts`, `*.type.ts`, `*.enum.ts` (pas de logique testable)
   - Exclure : `node_modules`, `dist`, build dirs, manifests, assets
6. **Classer par priorité** selon la densité de logique :
   - **P0** : `*.util.ts`, `*.policy.ts`, `*.helper.ts` (pure functions, facile + haute valeur)
   - **P1** : Services (entity et feature) avec signals, computed, effects, transformations
   - **P2** : Composants complexes (multi-states, effects, forms avec logique)
   - **P3** : Autres (guards, interceptors, directives, pipes)
   - **Skip** : composants purement présentationnels (template + 1-2 inputs), DTOs mappers triviaux

Si `SCOPE_DIRECT` est vide → "Rien à tester (pas de fichier modifié)." et stop.

## Étape 2 — Analyse du scope

Pour chaque fichier du scope (ordre P0 → P3) :

1. **Lire le fichier** intégralement.
2. **Vérifier si un spec existe déjà** : `<path>/<basename>.spec.ts` ou `<basename>.test.ts`.
   - **Existe** → mode "compléter". Lire le spec existant, identifier les cas non couverts, ne **JAMAIS** écraser : demander confirmation avant de merger/modifier.
   - **N'existe pas** → mode "créer". Générer de zéro.
3. **Identifier les cas de test à écrire** (cf. Étape 3).
4. **Trouver un spec de référence** dans le projet courant pour calquer le style (cf. Étape 4).

## Étape 3 — Cas de test à couvrir (priorités)

**Philosophie** : couverture qualitative > quantitative. **Pas** les getters/setters triviaux, **pas** les constructeurs vides, **pas** les pass-through sans logique.

### Obligatoires (si applicable au fichier)

- **Règles métier** : chaque branche logique (`if/else`, `switch`, ternaires avec logique) → 1 test.
- **Edge cases** :
  - `null` / `undefined` en entrée sur des params non-typés strict
  - Collection vide (`[]`, `new Map()`)
  - Collection à 1 élément (test de bornes)
  - Valeurs aux bornes (`0`, `-1`, `Infinity`, strings vides, dates passées/futures)
  - Discriminated unions : 1 test par variant du type
- **Cas tordus** — les penser volontairement :
  - Ordre d'arrivée des signaux/données inverse (ex: data avant id)
  - Deux effects qui se déclenchent en cascade
  - User qui change en cours d'appel API (token refresh)
  - Double-submit / race condition (si applicable)
  - Rechargement du même id consécutivement (cache hit)
  - Retour back malformé (champ manquant, type inattendu)
- **Regression anchors** : si le code modifié corrige un bug, écrire un test qui **échouerait sans le fix**. Le nom du test décrit le comportement attendu, pas l'origine. Exemple : `il ne doit plus perdre la sélection après reload`. **Aucune référence ticket** dans le nom du test — la traçabilité vit dans le commit message et le PR.

### Pour les services

- Mocks typés des dépendances (pas de `as any`)
- Test de l'état exposé : lecture avant + après mutation
- Test de l'invalidation / refresh (si pattern de versioning par signal)
- Test de `toSignal` → utiliser `fixture.detectChanges()` ou lecture explicite pour forcer la subscription (piège connu d'Angular)
- Gestion d'erreur : assert sur l'état du signal après un `throwError()`
- Pour un cache : test hit / miss / TTL / invalidation / dedup fetches concurrents

### Pour les composants Angular

- Création sans crash avec les inputs minimaux (smoke test)
- Pour chaque input signal : changement → assertion sur le computed/UI résultant
- Pour chaque event listener : dispatch → assertion sur l'output / side-effect
- Forms : dirty / valid / soumission
- `viewChild` résolu après `detectChanges`

### À NE PAS tester

- Getter trivial qui se contente d'exposer un champ en lecture
- DI trivial (`inject(Foo)` — Angular garantit ça)
- Templates sans logique (juste `{{ value() }}`)
- Constructeurs vides (sauf si l'`effect` dedans est la cible)

### Proposition avant écriture

Avant d'écrire le spec, **lister les cas prévus** en bullet-points dans la sortie console :

```
📝 Plan de test pour src/services/foo.service.ts :

Règles métier (5) :
  - Retourne X quand state=draft et hasAccountingDate=false
  - Retourne Y quand state=draft et hasAccountingDate=true
  - ...

Edge cases (3) :
  - Liste vide → signal initialValue = []
  - Tenant null → pas de fetch
  - ...

Cas tordus (2) :
  - Changement d'id pendant que le fetch précédent est in-flight (switchMap)
  - Double subscribe sur le cache → dedup via shareReplay

Total : 10 tests estimés.
```

Si le fichier source est simple (< 50 lignes de logique) → pas de proposition préalable, écrire directement.
Si ≥ 50 lignes ou logique dense → proposer le plan, écrire directement **sans attendre** (l'utilisateur a déjà validé en lançant le skill). L'utilisateur peut élaguer après.

## Étape 4 — Style & conventions Vitest

### Infrastructure attendue

- Framework : **Vitest** (avec ou sans `@analogjs/vite-plugin-angular` + `@analogjs/vitest-angular` pour les projets Angular)
- Config : `vite.config.ts` ou `vitest.config.ts`, setup `src/test-setup.ts`
- Pour Angular moderne (v17+) : import platform `@angular/platform-browser/testing` (pas `platform-browser-dynamic/testing` qui n'existe plus à partir d'Angular 21)
- Assertions : matchers vitest natifs (`expect.stringContaining`, `expect.objectContaining`, etc.)

### Template — Util / pure function

```typescript
import { describe, expect, it } from 'vitest';
import { maFonction } from './ma-fonction.util';

describe('maFonction', () => {
  describe('règles métier', () => {
    it('retourne X quand la condition A est vraie', () => {
      expect(maFonction({ a: true })).toBe('X');
    });

    it('retourne Y quand la condition A est fausse et B est vraie', () => {
      expect(maFonction({ a: false, b: true })).toBe('Y');
    });
  });

  describe('edge cases', () => {
    it('gère un objet vide sans crasher', () => {
      expect(() => maFonction({})).not.toThrow();
    });

    it("retourne la valeur par défaut quand l'entrée est null", () => {
      expect(maFonction(null as unknown as Input)).toBe('default');
    });
  });

  describe('cas tordus', () => {
    it("applique la priorité correcte quand plusieurs conditions se chevauchent", () => {
      expect(maFonction({ a: true, b: true, c: true })).toBe('X');
    });
  });
});
```

### Template — Service Angular

```typescript
import { TestBed } from '@angular/core/testing';
import { describe, expect, it, vi, beforeEach } from 'vitest';
import { of, throwError } from 'rxjs';

import { MonService } from './mon.service';
import { ApiService } from '../commons/api.service';

describe('MonService', () => {
  let service: MonService;
  let apiMock: { get: ReturnType<typeof vi.fn>; post: ReturnType<typeof vi.fn> };

  beforeEach(() => {
    apiMock = {
      get: vi.fn(),
      post: vi.fn(),
    };

    TestBed.configureTestingModule({
      providers: [
        MonService,
        { provide: ApiService, useValue: apiMock },
      ],
    });

    service = TestBed.inject(MonService);
  });

  describe('loadFoo', () => {
    it("appelle l'api avec le bon endpoint et met à jour le signal", () => {
      const data = { id: 1, name: 'Test' };
      apiMock.get.mockReturnValue(of(data));

      service.loadFoo(1);

      expect(apiMock.get).toHaveBeenCalledWith('foos/1');
      expect(service.foo()).toEqual(data);
    });

    it("garde le signal à undefined si l'API émet une erreur", () => {
      apiMock.get.mockReturnValue(throwError(() => new Error('500')));

      service.loadFoo(1);

      expect(service.foo()).toBeUndefined();
    });
  });

  describe('cas tordus', () => {
    it("annule le fetch précédent quand un nouvel id arrive (switchMap)", () => {
      // cf. tests de switchMap via rxjs TestScheduler ou fake timer
    });
  });
});
```

### Template — Composant avec `toSignal` lazy (piège documenté)

```typescript
it('lit correctement le signal dérivé de toSignal après detectChanges', () => {
  const fixture = TestBed.createComponent(MonComponent);
  fixture.componentRef.setInput('id', 1);

  fixture.detectChanges(); // force la subscription toSignal

  expect(fixture.componentInstance.derivedSignal()).toEqual(expectedValue);
});
```

### Règles transverses

- `describe` et `it` en **français**. Texte descriptif, pas une paraphrase du code.
- **Pas de `as any`** — typer correctement les mocks. Si narrowing impossible → `unknown` + cast ciblé avec commentaire.
- **Pas de `jest.fn()`** — `vi.fn()` (Vitest).
- **Pas d'assertion sur l'implémentation** (private fields, méthodes privées). Tester le comportement public.
- **AAA** (Arrange / Act / Assert) implicite, séparer par lignes vides plutôt que commentaires.
- Un `it` = un assert logique. Plusieurs `expect` OK s'ils décrivent le même comportement.
- Pas de `beforeEach` qui setup trop de choses — si complexe, extraire un helper nommé.

## Étape 5 — Écriture

Pour chaque fichier à tester :

1. **Si le spec n'existe pas** → utiliser `Write` pour créer `<path>/<basename>.spec.ts`.
2. **Si le spec existe déjà** → afficher une comparaison des cas couverts vs cas proposés. Proposer un patch. **Ne pas écraser sans accord explicite**.
3. **Détection du spec de référence** :
   - Chercher un spec "sibling" dans le même dossier
   - Sinon chercher un spec du même type (util/service/component) dans le projet via `Glob`
   - En dernier recours, utiliser le template ci-dessus

## Étape 6 — Exécution Vitest

Après chaque écriture de spec, lancer le test :

```bash
./node_modules/.bin/vitest run <path/to/new.spec.ts>
```

**Rapport à l'utilisateur** :

- ✅ Tous les tests passent → "X tests verts sur Y écrits pour <fichier>"
- ❌ Tests en échec :
  - Afficher le(s) test(s) qui échouent avec extrait de l'erreur
  - Identifier si c'est :
    - **Un bug dans le test** → proposer une correction (demander accord avant d'Edit)
    - **Un bug dans le code source** → flag pour revue (ne pas modifier le code source, laisser décider l'utilisateur)
    - **Un cas non implémenté** (test révèle un trou dans la logique) → rapporter

**Ne jamais commit / push** le spec après écriture — c'est à l'utilisateur de décider.

## Étape 7 — Rapport final

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Rapport write-tests
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Framework : Vitest
Scope analysé : N fichiers modifiés, M dépendances proches
Priorisés    : X P0, Y P1, Z P2, skipped (triviaux) : K

Specs créés :
  ✅ src/utils/foo.util.spec.ts — 8 tests, tous verts
  ✅ src/services/bar.service.spec.ts — 12 tests, tous verts
  ⚠️ src/services/baz.service.spec.ts — 10 tests, 2 échecs :
       - "ne doit pas perdre la sélection après reload" → bug dans le code source suspect, voir finding
  ⏸️ src/services/qux.service.spec.ts — spec existant, 4 cas proposés à merger, en attente d'accord

Specs ignorés (triviaux) :
  - src/components/simple.component.ts (getter only)

Findings révélés par les tests :
  1. baz.service.ts:42 — le code ne gère pas le cas où `id` change pendant un fetch in-flight

Total : X tests ajoutés, Y ✅ / Z ❌.
```

## Règles absolues

- **Jamais d'écrasement de spec existant** sans accord explicite.
- **Jamais de modification du code source** sans accord explicite (test échoue → rapporter, pas fixer unilatéralement).
- **Jamais de commande git** écrivante.
- **Langue** : rapport en français, `describe`/`it` en français, commentaires en français si besoin.
- Si scope > 10 fichiers → prévenir l'utilisateur avant d'écrire (volume élevé, proposer P0+P1 uniquement).
- **Aucune référence ticket** dans les noms de tests — ça vit dans le commit message et le PR.
