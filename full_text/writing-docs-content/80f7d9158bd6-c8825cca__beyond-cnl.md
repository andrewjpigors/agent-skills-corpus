---
name: beyond-cnl
description: Write, generate, convert, or validate documents in Beyond CNL, a method-only controlled subset of American English that achieves information-flow safety through grammar (E-Prime copula ban, mandatory evidential E-tags, a fixed verb and lexicon allow-list, and typed Markdown blocks). Use this skill whenever the user wants to author a Beyond CNL document, translate or convert standard English into Beyond CNL, check or audit a document for Beyond CNL compliance, work with evidential tags (E-tags), build the v0.4 document YAML frontmatter (instruments, references, conditions, technical_names, models, parameter_sets, simulation_runs, datasets, methods, hypothesis_space), or asks anything about the Beyond CNL language, its lexicon, verbs, or grammar — even when referred to informally (e.g. "method-only English", "the CNL", "the boundary language").
---

# SKILL: Beyond CNL — Method-Only Controlled Natural Language

## Version 0.4.1

*Sync with Evidential System v0.4 / Envelope Grammar §6. The
formal grammar in §6.7 of the Evidential System document is the
authoritative source of truth for E-tag shape; this skill file
is the operational companion.*

*v0.4.1 changelog: (1) `for COND` rationale slot on E-PRO; (2) `so`/`because` removed from the lexicon, purposive/causal linkage banned in prose; (3) FRONT-1 identifier-declaration enforcement clarified; (4) `product`/`quotient` admitted as arithmetic-result nouns.*

---

## What Beyond CNL Does

Beyond CNL is a controlled, method-only subset of American
English designed for communication in scenarios where the
recipient may have arbitrarily higher intelligence and
capability, and where any leaked information about the
sender's identity, values, intentions, capabilities, or
location could produce unbounded harm.

The language achieves safety through grammar, not policy.
Every restriction exists because the vocabulary or syntax
needed to express unsafe content has been removed. A
compliant document reads like a laboratory protocol:
procedures, measurements, definitions, observations,
simulations, aggregates, and bounded hypothesis spaces.

---

## The One Rule That Governs Everything

**Goguen-Meseguer non-interference:** two authors with
identical procedures but different identities, values, and
intentions produce byte-identical Beyond CNL documents for
the same observational data. If a document would differ
depending on who wrote it, it contains a leak.

---

## What You Must Never Generate

### Copula (E-Prime ban)

Remove every form of "to be":

`am`, `is`, `are`, `was`, `were`, `be`, `been`, `being`,
`'m`, `'re`, `'s` (copula), `isn't`, `aren't`, `wasn't`,
`weren't`, `ain't`

| Forbidden | Replacement |
|---|---|
| The signal is strong | The signal registers 42 dBm (measured, `RX-4`) |
| BEYOND is a planner | BEYOND exhibits planning-consistent responses (observed, `ARR-3`) |
| The channel is reliable | The channel passed 60 of 60 checks (measured, `CTR-1`) |
| This result is important | [DELETE — evaluative] |

### Banned word classes

| Class | Examples | Why |
|---|---|---|
| First-person singular | I, me, my, mine, myself | Identity |
| Identity-constructing plurals | "we humans", "we the people" | Identity |
| Proper nouns of groups | Earth, humanity, Americans, UN | Identity / location |
| Propositional-attitude verbs | believe, want, intend, prefer, hope, fear, wish, desire, expect, suspect, feel (mental), think (opinion), mean (intend) | Intent / values |
| Evaluative adjectives | good, bad, beautiful, important, right, wrong, noble, sacred, elegant | Values |
| Suasive verbs | ask, beg, demand, insist, propose, recommend, suggest, urge | Coercion |
| Deontic modals | should, ought, must (obligation) | Values |
| Epistemic hedging modals | might, may (possibility), could (speculation) | Cognitive architecture |
| Intensifiers | very, really, truly, totally, absolutely | Expressive |
| Stance adverbs | frankly, honestly, surprisingly, obviously, clearly | Attitude |
| Interjections | oh, wow, alas, hello, goodbye | Affect |
| Affect nouns | joy, sorrow, anger, fear, love, hate, pride, shame | Affect |
| Metaphor markers | like (comparison), as if, as though | Cognitive architecture |
| Exclamation marks | ! | Expressive |
| Purposive/causal subordinators | so that, in order to, because, purposive "so" | Intent / teleology |

### Common non-lexicon words and their replacements

| Temptation | Replacement |
|---|---|
| maintain | continue, remain |
| establish | set, create |
| determine | calculate, measure, identify |
| permit | allow |
| automatic | automated |
| previous | last |
| can | restructure to declarative |
| do / did / does (auxiliary) | restructure with `never` or simple tense |
| than | above, below, exceeding, within |
| must | restructure as constraint |
| become | restructure (activate, change to, shift to) |
| trigger (verb) | activate |
| send | transmit |
| keep | continue |
| denote | designate |
| characterize | describe, measure, map |
| override | cancel |
| because / so (purpose or result) | restructure: step rationale via `for COND` (E-PRO) or a declarative E-DER `(follows, from …)` |
| divided-by (coined operator) | the ratio of X to Y; or the `product`/`quotient` nouns |

---

## What You Must Always Generate

### Evidential tags on every declarative clause

Nine types in three tiers. Tag goes in parentheses at end
of clause, before the period. The formal shape of every
E-tag is fixed by the EBNF in §6.7 of the Evidential System
spec — examples below are operational; the grammar governs.

**Tier 1 — Direct**

```
(observed, instrument `ID`)
(observed, operator)
(detected, instrument `ID`)
(registered, thermocouple `ID`)
(measured, instrument `ID`, 1-sigma)
(measured, counter `ID`)
(measured, receiver `ID`, ± 0.4 dB)
(sampled, logger `ID`, n=500)
```

The optional instrument-class prefix (`instrument`, `array`,
`thermocouple`, `receiver`, `counter`, `logger`, `sensor`,
`detector`, `balance`, ...) names the device's class before
the inline-code identifier. The bare keyword `operator`
covers unaided human observation; no backtick identifier is
needed for it.

**Tier 2 — Mediated**

```
(derived, from `MSR-4.2`, `DEF-1.1`)
(calculated, from `MSR-3.1`, `MSR-3.2`)
(follows, from `OBS-2.7`, `DEF-2.3`)
(reported, in `REF-NIST-2023`)
(cited, from `REF-NIST-2023`)
(replicated, from `REF-LAB-A`, by instrument `ARR-3`)
(simulated, from model `MOD-1`, parameters `PAR-1`, run `RUN-1`)
(aggregated, from dataset `DAT-1`, method `MET-1`, n=500)
(hypothesis, candidate `H-1`, from `MSR-1.1`, distinguishable-from `H-2`)
```

**Tier 3 — Stipulative**

```
(defined)
(stipulated, for `Characterization`)
(procedure)
(procedure, step 3)
(procedure, step 5, if `COND-2.1`)
(procedure, step 5, for `COND-2.1`)
```

The `(defined)` tag takes no arguments — `(specified, …)` is
**not** an admitted E-DEF form under §6.7. Use `(defined)`
inside a fenced `definition` code block, or after a bolded
term at its first occurrence.

The `for `COND`` argument names the declared condition a step contributes to (the rationale slot). Its argument resolves to a `conditions:` entry only; it carries no free text. It mirrors `if `COND``, which gates a step on a condition.

### Compound sentences: each clause gets its own E-tag

```
The flux increased by 12% (measured, `RX-4`), and the noise
floor remained constant (measured, `RX-4`).
```

---

## Approved Verb List (325)

This is the **complete** set. If a verb does not appear here,
it cannot appear in a Beyond CNL document. Transitivity:
(tr) transitive, (intr) intransitive, (both) either.

### Physical action (81)

| Verb | Tr | Sense |
|---|---|---|
| `activate` | tr | cause to begin operating |
| `adjust` | tr | change setting of |
| `align` | tr | bring into line with reference |
| `apply` | tr | put onto surface or put into effect |
| `assemble` | tr | put parts together |
| `attach` | tr | join one thing to another |
| `bend` | tr | change angle of |
| `block` | tr | prevent passage through |
| `break` | tr | separate into parts by force |
| `build` | tr | construct from parts |
| `calibrate` | tr | adjust to match a known standard |
| `carry` | tr | transport from one location to another |
| `clean` | tr | remove contaminants from |
| `close` | tr | move to stop flow or access |
| `compress` | tr | reduce volume of by force |
| `connect` | tr | join so that signal or material passes |
| `construct` | tr | build by assembling components per plan |
| `cool` | tr | reduce temperature of |
| `cover` | tr | place over the surface of |
| `cut` | tr | separate by edged tool |
| `deactivate` | tr | cause to stop operating |
| `decrease` | tr | make smaller in quantity |
| `destroy` | tr | reduce to non-functional state |
| `detach` | tr | separate one thing from another |
| `disconnect` | tr | break connection of |
| `drain` | tr | remove liquid from |
| `dry` | tr | remove moisture from |
| `empty` | tr | remove all contents from |
| `expand` | tr | increase volume of |
| `extend` | tr | make longer |
| `fasten` | tr | secure in position |
| `fill` | tr | put contents into until capacity |
| `filter` | tr | pass through selective barrier |
| `flatten` | tr | make flat |
| `fold` | tr | bend over onto itself |
| `form` | tr | give shape to |
| `heat` | tr | increase temperature of |
| `hold` | tr | keep in fixed position |
| `increase` | tr | make larger in quantity |
| `insert` | tr | put into |
| `install` | tr | put into position for use |
| `join` | tr | connect two or more parts |
| `lift` | tr | move upward |
| `load` | tr | put contents into carrier |
| `lock` | tr | secure against movement or access |
| `loosen` | tr | make less tight |
| `lower` | tr | move downward |
| `mix` | tr | combine into uniform composition |
| `mount` | tr | fix onto support structure |
| `move` | tr | change position of |
| `open` | tr | move to allow flow or access |
| `pack` | tr | place compactly into container |
| `place` | tr | put at a location |
| `position` | tr | set at specific coordinates |
| `pour` | tr | cause liquid to flow from container |
| `press` | tr | apply force to surface of |
| `pull` | tr | apply force toward self on |
| `push` | tr | apply force away from self on |
| `raise` | tr | move upward |
| `release` | tr | stop holding |
| `remove` | tr | take away from location |
| `repair` | tr | restore to working condition |
| `replace` | tr | put new in place of old |
| `reshape` | tr | change form of |
| `rotate` | tr | turn around axis |
| `seal` | tr | close to prevent passage |
| `separate` | tr | divide into parts |
| `set` | tr | adjust to specified value |
| `shorten` | tr | make shorter |
| `shrink` | intr | decrease in spatial extent |
| `split` | tr | divide into two or more parts |
| `stabilize` | tr | bring to steady state |
| `straighten` | tr | make straight |
| `stretch` | tr | extend by pulling |
| `tighten` | tr | make more tight |
| `transfer` | tr | move from one system to another |
| `turn` | tr | rotate partially |
| `unfasten` | tr | release from fastened position |
| `unload` | tr | remove contents from carrier |
| `unlock` | tr | release from locked state |
| `wrap` | tr | enclose by winding cover around |

### Information and control (65)

| Verb | Tr | Sense |
|---|---|---|
| `add` | tr | include in set or sum |
| `allocate` | tr | assign portion of resource |
| `archive` | tr | store for long-term retention |
| `assign` | tr | designate for role or value |
| `calculate` | tr | determine by mathematical operation |
| `cancel` | tr | revoke previously issued instruction |
| `categorize` | tr | place into defined class |
| `change` | tr | make different from current state |
| `check` | tr | examine for compliance with specification |
| `classify` | tr | assign to category |
| `clear` | tr | remove all data from |
| `combine` | tr | put together into one |
| `compare` | tr | examine for differences and similarities |
| `compute` | tr | perform calculation on |
| `configure` | tr | set parameters of system |
| `confirm` | tr | verify that condition holds |
| `convert` | tr | change from one form to another |
| `copy` | tr | make duplicate of |
| `count` | tr | determine number of |
| `create` | tr | bring into existence by procedure |
| `define` | tr | state the meaning of term |
| `delete` | tr | remove from record |
| `derive` | tr | obtain by logical or mathematical operation |
| `designate` | tr | assign identifier to |
| `disable` | tr | prevent from operating |
| `distribute` | tr | allocate across recipients |
| `divide` | tr | separate into equal or specified parts |
| `enable` | tr | allow to operate |
| `enter` | tr | input data into system |
| `erase` | tr | remove recorded data from |
| `estimate` | tr | determine approximate value of |
| `evaluate` | tr | determine numerical value of expression |
| `execute` | tr | carry out instruction |
| `format` | tr | arrange data per specification |
| `generate` | tr | produce by automated process |
| `group` | tr | organize into sets |
| `identify` | tr | determine which item matches specification |
| `index` | tr | create ordered reference to |
| `initialize` | tr | set to starting state |
| `label` | tr | attach identifier to |
| `list` | tr | enumerate items of |
| `log` | tr | record in append-only store |
| `map` | tr | establish correspondence between sets |
| `mark` | tr | place indicator on |
| `merge` | tr | combine two ordered sets into one |
| `modify` | tr | change specified property of |
| `multiply` | tr | perform multiplication on |
| `normalize` | tr | scale to standard range |
| `number` | tr | assign sequential identifier to |
| `organize` | tr | arrange according to system |
| `process` | tr | apply defined sequence of operations to |
| `program` | tr | enter instructions into |
| `read` | tr | obtain data from source |
| `record` | tr | store observation in persistent form |
| `reset` | tr | return to initial state |
| `retrieve` | tr | obtain from storage |
| `run` | tr | execute procedure or test |
| `save` | tr | write to persistent storage |
| `select` | tr | choose item matching criterion |
| `sort` | tr | arrange in specified order |
| `store` | tr | place for later retrieval |
| `subtract` | tr | remove quantity from |
| `update` | tr | change to reflect current state |
| `verify` | tr | confirm by independent check |
| `write` | tr | output data to destination |

### Observation and measurement (47)

| Verb | Tr | Sense |
|---|---|---|
| `appear` | intr | present to observation as |
| `approach` | both | move closer to; come nearer to value |
| `cease` | intr | stop occurring |
| `converge` | intr | approach common value |
| `correlate` | intr | vary together with |
| `cross` | tr | pass through threshold |
| `decay` | intr | decrease progressively; undergo spontaneous transformation |
| `decline` | intr | decrease in measured value |
| `detect` | tr | register presence of |
| `differ` | intr | have different measured value from |
| `diminish` | intr | become smaller |
| `disappear` | intr | cease to register on instrument |
| `diverge` | intr | move apart in value |
| `emerge` | intr | become detectable |
| `exceed` | tr | surpass threshold value |
| `fall` | intr | decrease in value |
| `fluctuate` | intr | vary irregularly |
| `follow` | tr | come after in sequence |
| `grow` | intr | increase in measured quantity |
| `happen` | intr | take place at time |
| `indicate` | tr | show on display or instrument |
| `last` | intr | persist for duration |
| `match` | tr | correspond to within tolerance |
| `measure` | tr | determine quantity by instrument |
| `observe` | tr | register through sensor or instrument |
| `occur` | intr | take place |
| `oscillate` | intr | vary periodically |
| `pass` | tr | move through or beyond |
| `peak` | intr | reach maximum value |
| `persist` | intr | continue without change |
| `precede` | tr | come before in sequence |
| `produce` | tr | yield as output |
| `reach` | tr | arrive at value or location |
| `register` | tr | show reading on instrument |
| `remain` | intr | continue in current state |
| `repeat` | intr | occur again |
| `reproduce` | tr | generate same result independently |
| `respond` | intr | change after stimulus |
| `result` | intr | follow as consequence |
| `return` | intr | go back to last value |
| `rise` | intr | increase in value |
| `saturate` | intr | reach maximum capacity |
| `shift` | intr | change position or value |
| `show` | tr | display on readout |
| `spread` | intr | extend over larger area or range |
| `stabilize` | intr | reach steady state |
| `vary` | intr | change in value over parameter |

### Communication and documentation (22)

| Verb | Tr | Sense |
|---|---|---|
| `acknowledge` | tr | confirm receipt of |
| `amend` | tr | make specified change to document |
| `announce` | tr | make available to all parties |
| `cite` | tr | reference prior record |
| `confirm` | tr | state that check passed |
| `correct` | tr | change to accurate value |
| `declare` | tr | state formally in record |
| `deny` | tr | state that statement fails verification |
| `describe` | tr | state observable properties of |
| `disclose` | tr | make information available |
| `document` | tr | create record of |
| `notify` | tr | transmit information to specified party |
| `post` | tr | make available in public record |
| `publish` | tr | release for general access |
| `reference` | tr | point to location of prior record |
| `report` | tr | present findings in structured form |
| `retract` | tr | withdraw statement |
| `revise` | tr | produce updated version of |
| `specify` | tr | state precise requirements for |
| `state` | tr | express in declarative sentence |
| `submit` | tr | deliver for review |
| `transmit` | tr | send via channel |

### State and control (31)

| Verb | Tr | Sense |
|---|---|---|
| `allow` | tr | permit by rule |
| `begin` | intr | start |
| `complete` | tr | finish all steps of |
| `conceal` | tr | prevent from being detected |
| `contain` | tr | hold within boundary |
| `continue` | intr | persist in current operation |
| `control` | tr | regulate state of |
| `depend` | intr | require as precondition |
| `end` | intr | stop |
| `exist` | intr | have presence in specified domain |
| `fail` | intr | not meet specification |
| `finish` | tr | complete |
| `fit` | intr | conform to dimensional specification |
| `function` | intr | operate as specified |
| `halt` | intr | stop all operation |
| `include` | tr | have as component |
| `lack` | tr | not have |
| `limit` | tr | constrain range of |
| `need` | tr | require as input |
| `operate` | intr | function within specification |
| `pause` | intr | temporarily stop |
| `prevent` | tr | stop from occurring |
| `prohibit` | tr | forbid by rule |
| `require` | tr | have as necessary condition |
| `restrict` | tr | limit to subset |
| `resume` | intr | continue after pause |
| `reveal` | tr | make detectable |
| `start` | intr | begin operating |
| `stop` | intr | cease operating |
| `supply` | tr | provide as input |
| `support` | tr | bear load of or provide resource to |

### Movement and spatial (16)

| Verb | Tr | Sense |
|---|---|---|
| `accelerate` | both | increase velocity (of) |
| `advance` | intr | move forward |
| `arrive` | intr | reach destination |
| `circulate` | intr | move in closed path |
| `decelerate` | both | decrease velocity (of) |
| `descend` | intr | move downward |
| `drift` | intr | move slowly without directed force |
| `enter` | tr | move into |
| `exit` | intr | move out of |
| `flow` | intr | move continuously as fluid |
| `orbit` | intr | move in closed path around |
| `propagate` | intr | travel through a medium |
| `recede` | intr | move away from observer |
| `retract` | intr | move back |
| `rotate` | tr | turn around axis |
| `travel` | intr | move from one location to another |

### Logical and mathematical (17)

| Verb | Tr | Sense |
|---|---|---|
| `approximate` | tr | come close to in value |
| `assume` | tr | take as given for derivation (NOT suppose/believe) |
| `bound` | tr | set upper or lower limit on |
| `constrain` | tr | limit by rule |
| `contradict` | tr | produce incompatible result with |
| `correspond` | intr | map one-to-one with |
| `demonstrate` | tr | show by derivation or experiment |
| `disprove` | tr | show to fail by test |
| `eliminate` | tr | remove from consideration by test |
| `entail` | tr | follow necessarily from |
| `equal` | tr | have same value as |
| `exclude` | tr | remove from set |
| `falsify` | tr | show to fail against data |
| `imply` | tr | follow from under given rules |
| `negate` | tr | form logical complement of |
| `satisfy` | tr | meet all conditions of |
| `solve` | tr | find value that satisfies formula |

### Sensory and detection (13)

| Verb | Tr | Sense |
|---|---|---|
| `absorb` | tr | take in energy or material |
| `amplify` | tr | increase signal strength of |
| `attenuate` | tr | reduce signal strength of |
| `capture` | tr | record incoming signal |
| `collect` | tr | gather samples or data |
| `emit` | tr | release energy or particles |
| `expose` | tr | subject to stimulus |
| `illuminate` | tr | direct light onto |
| `radiate` | intr | emit energy outward |
| `receive` | tr | accept incoming signal |
| `reflect` | tr | return incoming energy from surface |
| `scan` | tr | examine systematically across range |
| `sense` | tr | detect by instrument |

### Astronomy (7)

| Verb | Tr | Sense |
|---|---|---|
| `accrete` | intr | accumulate matter by gravitational attraction |
| `brighten` | intr | increase in luminous intensity |
| `dim` | intr | decrease in luminous intensity |
| `erupt` | intr | expel material suddenly from interior |
| `occult` | tr | pass in front of, blocking from line of sight |
| `precess` | intr | rotate orientation of orbital or spin axis |
| `transit` | tr | pass across disc of larger body |

### Physics (8)

| Verb | Tr | Sense |
|---|---|---|
| `annihilate` | tr | convert matter and antimatter into energy |
| `collide` | intr | strike against another body |
| `conduct` | tr | transmit heat, electric current, or sound through a medium |
| `diffract` | intr | spread after passing through aperture |
| `excite` | tr | raise to higher energy state |
| `insulate` | tr | prevent the passage of heat, electric current, or sound |
| `ionize` | tr | remove or add electrons to atom or molecule |
| `polarize` | tr | restrict oscillation to single plane |

### Chemistry (10)

| Verb | Tr | Sense |
|---|---|---|
| `catalyze` | tr | increase the rate of a reaction using a catalyst |
| `condense` | both | change from vapor to liquid |
| `corrode` | both | degrade a metal by chemical reaction |
| `crystallize` | both | form crystals from a solution or melt |
| `dilute` | tr | reduce the concentration of a solution by adding solvent |
| `dissolve` | tr | cause a solute to pass into solution |
| `evaporate` | both | change from liquid to vapor |
| `neutralize` | tr | react an acid with a base to remove reactive properties |
| `oxidize` | tr | cause to combine with oxygen or lose electrons |
| `synthesize` | tr | form a compound from simpler substances |

### Information theory (9)

| Verb | Tr | Sense |
|---|---|---|
| `decode` | tr | convert from encoded form to source form |
| `demodulate` | tr | extract information from modulated carrier |
| `encode` | tr | convert from source form to channel form |
| `encrypt` | tr | transform data to prevent unauthorized reading |
| `modulate` | tr | vary carrier property to encode information |
| `multiplex` | tr | combine multiple signals onto single channel |
| `quantize` | tr | map continuous values to discrete levels |
| `sample` | tr | obtain value of signal at specific time |
| `synchronize` | tr | bring systems to common time reference |

### Arts and fabrication (4)

| Verb | Tr | Sense |
|---|---|---|
| `etch` | tr | remove material from surface to produce pattern |
| `inscribe` | tr | mark characters permanently onto surface |
| `project` | tr | cast light or image onto surface |
| `render` | tr | produce visual representation from data |

---

## Sentence Structure

### Declarative (max 25 words)

```
[Subject] [verb] [object/complement] [modifiers]
(E-tag, source/refs).
```

Simple present or simple past. No progressive. No perfect.
No gerunds. No modal stacking.

### Imperative (max 20 words)

```
[Verb] [object] [modifiers] (procedure[, step N][, if COND][, for COND]).
```

### Past-participle-as-adjective: ALLOWED
"the specified value", "the measured amplitude", "the
defined term"

### Present-participle-as-adjective: NOT ALLOWED
"the following steps" → "these steps" or "the steps below"
"the preceding window" → "the last window"
"the remaining cycles" → "the cycles after the pause"

---

## Markdown Structure

| Element | Role | E-tag constraint |
|---|---|---|
| H1 `#` | Protocol identifier (one per doc) | none (H-1) |
| H2 `##` | Phase or section header | none (H-1) |
| Ordered list `1.` | Procedure steps | E-PRO only (O-1); must follow a heading beginning `Procedure` or `Steps` (O-2) |
| Blockquote `>` | Observation report | E-OBS or E-MSR (B-1) |
| Fenced code `definition` | Term definition | E-DEF (C-1) |
| Fenced code `constraint` | Formal constraint | E-DEF or E-DER (C-2) |
| Fenced code `measurement` | Recorded measurement | E-MSR (C-3) |
| Fenced code `simulation` | Simulation output | E-SIM (C-5) |
| Fenced code `aggregation` | Statistical aggregate | E-AGG (C-6) |
| Fenced code `relation` | Formula / arithmetic relation | E-DER (C-7); operator notation admitted only here |
| Paragraph under `Hypothesis` heading | Bounded hypothesis | E-HYP only there (HYP-PLACE) |
| Fenced code (other info string) | Domain-specific | unrestricted, flagged for review (C-4) |
| Inline code `` ` `` | Defined identifier | — |
| Bold `**` | First occurrence of Technical Name | — |

**Forbidden:** italics, HTML, exclamation marks, indented
code blocks (use fenced with info string).

**Not in the §6.5 envelope:** tables, unordered lists, and
images do not appear in the formal envelope grammar. Treat
parameter sets as frontmatter `parameter_sets:` entries.

---

## YAML Frontmatter (every document)

```yaml
---
schema: beyond-cnl-v0.4
purpose: [narrow procedural purpose in Beyond CNL]
phase: [Discovery | Validation | Characterization |
        Open-Contact | Negotiation]
instruments:
  - id: [ID]
    type: [type]
    calibration: [window]
references:
  - id: [ID]
    title: [title]
    access: [public | restricted]
conditions:
  - id: [ID]
    statement: [condition in Beyond CNL]
technical_names:
  - term: [compound term]
    pos: noun
    definition: [using only core lexicon words]
models:
  - id: [MODEL-ID]
    specification_ref: [REF-ID]
    parameter_schema_ref: [REF-ID]
parameter_sets:
  - id: [PARAMETERS-ID]
    model: [MODEL-ID]
simulation_runs:
  - id: [RUN-ID]
    model: [MODEL-ID]
    parameters: [PARAMETERS-ID]
datasets:
  - id: [DATASET-ID]
    schema_ref: [REF-ID]
methods:
  - id: [METHOD-ID]
    catalogue_ref: [REF-ID]
hypothesis_space:
  - id: [H-ID]
    statement: [candidate statement in Beyond CNL]
    discriminates_via: [MEASUREMENT-OR-DERIVATION-ID]
---
```

---

## Technical Names

Nouns not in the core lexicon enter via escape mechanism:
first occurrence **bold** + `definition` code block;
subsequent uses in `inline code`; noun-only; registered
in frontmatter. Definition uses only lexicon words.

---

## Common Pitfalls

### 1. Smuggling copula
Wrong: "The signal proves strong."
Right: "The signal registers 42 dBm (measured, `RX-4`)."

### 2. Using -tion nouns not in lexicon
| Use | Not in lexicon → use instead |
|---|---|
| computation | ✅ in lexicon |
| verification | ✅ in lexicon |
| calculation | ✗ → computation |
| confirmation | ✗ → verification, check |
| cancellation | ✗ → restructure with cancel |
| publication | ✗ → release |
| interruption | ✗ → pause, stop |
| declaration | ✗ → record, report |

### 3. Attributing agency to BEYOND
Wrong: "BEYOND responded to our signal."
Right: "The anomaly rate decreased by 40% during the
low-cadence window (measured, `CTR-1`)."

### 4. Missing E-tags
Count clauses. Count E-tags. They match.

### 5. Using "must" for constraints
Wrong: "Each amendment must contain a proof chain."
Right (as procedure, imperative form): "Add a proof chain
to each amendment (procedure)."
Right (as constraint, declarative form in a `constraint`
block): "Each amendment contains a proof chain (defined)."

Note: `(procedure)` E-tags require an imperative leading
verb (E-PRO-1). A declarative sentence cannot carry a
`(procedure)` tag.

### 6. Precision as capability leak
Wrong: "Our instruments resolve to 0.5 Hz precision."
Right: State the measurement. Precision speaks for itself.

### 7. "Than" in comparisons
Use `above`, `below`, `exceeding`, `within`.

### 8. Present-participle adjectives
Wrong: "the following steps" → "these steps"
Wrong: "the preceding window" → "the last window"

### 9. Auxiliary do/did/does
Wrong: "The condition did not activate."
Right: "The condition never activated (observed, `CTR-1`)."

### 10. Rationale without a home
Wrong: "Limit heat time so the fronts remain separated."
(purposive `so` — banned). Right, step-local: "Limit heat
time (procedure, step 7, for `COND-FRONT-SEPARATION`)." Right,
as mechanism: "Limited heat time prevents front contact
(follows, from `COND-FRONT-SEPARATION`)."

### 11. `(defined)` on a mechanism claim
Wrong: "Higher collector voltage pulls electrons through the
base (defined)." A causal/functional claim is not a
stipulation. Right: tag it E-DER with the premise referencing
a definition or condition: "(follows, from `REVERSE-BIAS`)".

### 12. Undeclared identifiers (FRONT-1)
Every `inline-code` identifier in the body must resolve to a
declared `technical_names`, `conditions`, `references`, or
`instruments` entry. Backticking a word does not exempt it:
a backtick that wraps a plain lexicon word (e.g. `` `hydrogen` ``)
or a whole phrase (e.g. `` `A | B | C` ``) is evasion, not an
identifier. Reconcile body identifiers against frontmatter.

---

## Conversion: Standard English → Beyond CNL

1. Extract procedures → imperative + `(procedure)` E-tag
2. Extract measurements → declarative + `(measured)` E-tag
3. Extract definitions → `definition` block + `(defined)`
4. Extract derivations → declarative + `(derived)` E-tag
5. Extract citations of prior records → declarative +
   ``(reported, in `REF-...`)`` or ``(cited, from `REF-...`)``;
   add `REF-…` to `references:` frontmatter
6. Extract simulation outputs → declarative + ``(simulated, from model `MOD`, parameters `PAR`, run `RUN`)``; declare all three frontmatter records
7. Extract aggregates → declarative + ``(aggregated, from dataset `DAT`, method `MET`, n=N)``; declare dataset and method records
8. Extract bounded hypotheses only under a `Hypothesis` heading → ``(hypothesis, candidate `H`, from `PREM`, distinguishable-from `OTHER`)``; declare candidates in `hypothesis_space:`
9. Attach step rationale via `for COND` (E-PRO) or a
   declarative E-DER — never via purposive "so"/"because"
10. Discard identity, values, opinions, intentions, requests
11. Check every word against lexicon; replace or restructure
12. Build YAML frontmatter: declare every `` `ID` `` you used
   in the matching v0.4 frontmatter namespace
13. Reconcile (FRONT-1): every `inline-code` identifier in the
   body resolves to a frontmatter declaration; flag lexicon
   words and phrases wrapped in backticks as evasion
14. Verify non-interference: would a different author produce
   the same document from the same data?

---

## v0.4 Extended E-tags

E-SIM, E-AGG, and E-HYP are admitted in `schema: beyond-cnl-v0.4`.

| Tag | Form | Required frontmatter |
|---|---|---|
| E-SIM | ``(simulated, from model `M`, parameters `P`, run `R`)`` | `models:`, `parameter_sets:`, `simulation_runs:` |
| E-AGG | ``(aggregated, from dataset `D`, method `M`, n=N)`` | `datasets:`, `methods:` |
| E-HYP | ``(hypothesis, candidate `H`, from `PREM`, distinguishable-from `OTHER`)`` | `hypothesis_space:` and a `Hypothesis` heading |

---

## Non-Compliant Example (27+ violations)

> "We, the people of Earth, are reaching out to you in peace
> and friendship. We believe that communication between our
> civilizations could lead to mutual understanding."

`we` (identity) · `the people of Earth` (proper noun, location)
· `are` (copula) · `reaching out` (-ing progressive) ·
`in peace and friendship` (values) · `believe` (attitude) ·
`our` (identity) · `could` (epistemic hedge) ·
`mutual understanding` (value claim) · zero E-tags ·
no YAML · no Markdown structure

In Beyond CNL this reduces to empty output. That emptiness
correctly represents the information-hazard cost.

---

## Quick Reference Card

```
NEVER:  am is are was were be been being
NEVER:  I me my mine myself
NEVER:  believe want intend hope fear wish desire expect
NEVER:  good bad important beautiful right wrong
NEVER:  should ought must (obligation)
NEVER:  might may could (speculation)
NEVER:  ask suggest recommend demand propose
NEVER:  very really truly obviously clearly
NEVER:  ! (exclamation mark)
NEVER:  so because (purposive/causal subordination)

ALWAYS: (E-tag) at end of every declarative clause
ALWAYS: instrument `ID` in every observation E-tag
ALWAYS: premise references in every derivation E-tag
ALWAYS: YAML frontmatter with schema: beyond-cnl-v0.4
ALWAYS: model/dataset/hypothesis IDs in their v0.4 namespaces
ALWAYS: `inline code` for identifiers
ALWAYS: **bold** for first Technical Name occurrence
ALWAYS: every `inline-code` identifier declared in frontmatter (FRONT-1)
ALWAYS: `for COND` (or E-DER) for step rationale

DEFAULT: ambiguity = rejection
DEFAULT: missing E-tag = rejection
DEFAULT: non-lexicon word = rejection
DEFAULT: undeclared identifier = rejection
DEFAULT: expressiveness gap = correct behavior
```

---

## Design Lineage

| Tradition | Contribution |
|---|---|
| E-Prime | Copula ban |
| ASD-STE100 | Procedural register, sentence limits, one-word-one-meaning |
| Attempto CE | Deterministic interpretation, mandatory determiners |
| Lojban | Mandatory evidentials, typed predicates |
| Markdown | Typed block grammar |
| Saltzer-Schroeder | Default-deny, complete mediation, open design, least privilege |

---

## Companion Lexicon — when and how to load it

**File:** `beyond_cnl_COMPANION_LEXICON.md`, located alongside
this skill file (same directory).

**Contents:** the complete noun (939), adjective (230),
adverb (52), numeral/unit (68), and function-word (137) lists
with sense pins, plus dual-sense and dropped-noun tables. The
verb list (313) lives in *this* skill file, not the lexicon;
the lexicon's sections are numbered to continue from it (it
starts at "3. Function Words"), so do not look for a Section 4
inside it.

**Load rule:**

- **Conversion or compliance/validation task** — read
  `beyond_cnl_COMPANION_LEXICON.md` before checking words
  against the lexicon (workflow step 10 above). It carries the
  allow-list this skill file does not.
- **Generation task** — do **not** load it. This skill file
  with the verb list above suffices; noun and adjective gaps
  surface at validation and resolve via the Technical Name
  mechanism or the pitfalls-section replacements.

**Reading it efficiently:** at ~1,760 lines it should not be
read whole. Jump to the relevant section — `## 5. Nouns`,
`## 6. Adjectives`, `## 7. Adverbs`, `## 8. Numerals and
Units`, `## 3. Function Words`, `## Dual-Sense Nouns`, or
`## Dropped Nouns` — using a targeted view of just that
heading's range.

---

*End of Beyond CNL Skill Document v0.4.1.*
