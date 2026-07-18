---
name: stphelper
description: Recommended order and workflow for fixing stphelper lint rules when converting a markdown thesis/report to DOCX. Trigger when the user runs stphelper, asks how to fix a specific rule code, or wants guidance on resolving layout/style/correctness diagnostics in the generated PDF.
---

# stphelper skill — fixing lint rules in order

This document describes how to work through the diagnostics `stphelper` reports
on a converted markdown file. Print it any time with:

```bash
stphelper --skill
```

The goal is a deterministic workflow: apply all mechanical fixes first, then
address the pagination-dependent layout rules, then do the manual work. Each
stage feeds the next, so do not skip ahead.

## Agent rules (read first)

If you're an agent (Claude Code, Cursor, etc.), these rules apply to every
action below, not just one stage. Violating rule 1 is the single most common
cause of permission-prompt spam in stphelper sessions.

### 1. Never shell out for something a native tool can do

Every `Bash` call typically prompts the user for permission. `Read`, `Grep`,
and `Edit` do not. Use them.

| task                     | ❌ Bash (prompts)               | ✅ Native (auto-approves)                         |
| ------------------------ | ------------------------------- | ------------------------------------------------- |
| read lines N–M of a file | `sed -n 'N,Mp' file`            | `Read(file, offset=N-1, limit=M-N+1)`             |
| search for a pattern     | `grep 'rx' file`                | `Grep(pattern='rx', path='file')`                 |
| first/last N lines       | `head -N file` / `tail -N file` | `Read(file, limit=N)` for head                    |
| count matches            | `grep -c 'rx' file`             | `Grep(pattern='rx', output_mode='count')`         |
| pattern + context lines  | `grep -A3 'rx' file`            | `Grep(pattern='rx', -A=3, output_mode='content')` |
| slice then filter        | `sed … \| grep …`               | one `Grep` with `-A`/`-B` flags                   |
| in-place file edit       | `sed -i 's/a/b/' file`          | `Edit(file, old_string='a', new_string='b')`      |

Only reach for `Bash` when there's no native equivalent: running
`stphelper`, `git`, or writing a file via shell redirection
(`cmd > out.log`).

### 2. Don't make edits that will be reversed on the next run

Editing the same paragraph or code block 3+ times means the local fix
isn't the right fix. Stop, widen your view. See _When local edits aren't
converging_ below.

### 3. Ask the user before any structural move

Deleting a heading, removing a subsection, moving an algorithm,
redistributing content — these change what the document _says_, not just
how it paginates. Propose and wait. See the gate note in _When local
edits aren't converging_.

## Project mode (stphelper.toml present)

Check the working directory or any parent for `stphelper.toml`. If one
exists, you're in **project mode**. Each part is rendered to its own
ephemeral PDF for lint (`_lint_via_pdf` in `pipeline/parts.py`), so
single-file iteration is valid — page boundaries inside a chapter only
depend on that chapter, not on its neighbors. Pick the command by what
you actually need:

| task                                | command                                   |
| ----------------------------------- | ----------------------------------------- |
| full build (DOCX + PDF, merged)     | `stphelper build`                         |
| lint every part in one Word launch  | `stphelper lint`                          |
| lint or iterate on one chapter      | `stphelper lint path/to/chapter.md`       |
| apply safe fixes across the project | `stphelper build --fix` (or `lint --fix`) |
| also apply unsafe fixes             | add `--unsafe-fixes`                      |
| skip lint during build              | `stphelper build --no-lint`               |

Notes:

- Project-wide `--fix` walks every part and rewrites all of them in one
  pass. Single-file `--fix` only touches that file. Both are safe
  because each part lints independently.
- `stphelper lint` (no arg) keeps Word alive across files — much faster
  than running `lint <path>` in a loop.
- `render <md>` and `lint <md>` auto-pick up the project's template +
  Jinja context from the nearest `stphelper.toml`, so chapter-level
  commands work the same in or out of project mode.
- Abstracts (`type = "abstract"`) are linted and rendered by
  `stphelper build` (phase 2, with real `counts.*` injected). Don't try
  to `render` or `lint` them standalone — they reference `{{ counts.* }}`
  which only the project pipeline computes. **BD001 is suppressed for
  abstracts** by design (digit artifact-counts are required there).
- Output lands in `output/<name>.docx` + `output/<name>.pdf`, with
  frontmatter splits in `output/<name>-parts/`. Add `output/` and
  `.stphelper/` to `.gitignore` if they aren't already.

## Recommended order

Run `stphelper render input.md` (or `stphelper lint input.md` in project
mode) between each stage — later stages depend on the PDF pagination
produced by the previous stage.

### Stage 1 — markdown-only safe fixes (text correctness and style)

These rules operate on the markdown source alone. They do not depend on
pagination, so they are safe to apply in bulk first.

- **YR001** `yo-to-ye` — `ё` → `е`. SAFE fix.
- **ED001** `em-dash` — `—` → `–`. SAFE fix.
- **LP001** `list-punctuation` — bullet items end with `;`, last with `.`;
  numbered (`1. `) items all end with `.`. SAFE fix. Depends on `SL001`:
  single-item lists are skipped.
- **LP002** `numbered-list-capitalization` — numbered (`1. `) items must
  start with a capital letter. SAFE fix. Depends on `SL001`: single-item
  lists are skipped.

Apply:

```bash
stphelper render input.md --fix
```

### Stage 2 — markdown-only unsafe fixes (digits → words)

- **BD001** `bare-digits` — standalone digits `0`–`9` rewritten as words
  (`три`, `пять`, …). UNSAFE because the chosen word form may not agree with the
  surrounding grammatical case. Skipped on `type = "abstract"` parts, where digit
  artifact-counts are required by convention.

Apply, then review the diff:

```bash
stphelper render input.md --fix --unsafe-fixes
git diff input.md
```

Fix any wrong case endings manually (`три` → `трёх`, etc.). Re-run until
`--fix --unsafe-fixes` reports nothing new.

### Stage 3 — manual: markdown-level structure (SL001, IM001)

These are markdown-only, no autofix. Resolve before PDF-dependent stages
because each edit shifts pagination.

- **SL001** `single-item-list` — a markdown list with only one `- ` item.
  Either merge the single item into the surrounding paragraph, add genuine
  sibling items, or rewrite as prose.
- **IM001** `image-bad-aspect` — image rendered aspect ratio is too elongated
  (h:w > 2.5 = too tall/narrow, or w:h > 4 = banner). Auto-shrink can't fix
  aspect, and a `<!-- image: width=N -->` override doesn't help either — the
  rule reads the **rendered** dims (including any override), so shrinking
  just produces the same aspect at a smaller size.

  **As an agent, do not silently work around this.** You can't rotate, crop,
  or redesign the source image yourself, and editing the source markdown
  won't change the aspect. Surface the warning to the user with the figure's
  `file:line` reference, name the specific failure mode (too tall vs. too
  wide), and ask whether they can provide a re-shot or re-cropped version of
  the image. If the user has no better source available and explicitly
  accepts the warning, leave it; otherwise pause until they supply a
  replacement.

### Stage 4 — pagination-dependent safe fixes

These need the PDF, so do them after all markdown-only edits are stable.

- **CR002** `blank-code-at-page-edge` — a blank line inside a fenced code block
  landed at the top or bottom of a page. SAFE fix: delete the blank line from
  the source.
- **DW001** `dash-wrapping` — an en-dash `–` wrapped to the start of a visual
  line. SAFE fix: replace `" – "` with `"&nbsp;– "` so the dash sticks to the
  preceding word.

Apply:

```bash
stphelper render input.md --fix
```

Re-run afterwards — fixing one wrap can nudge pagination and expose or resolve
the next one.

### Stage 5 — pagination-dependent unsafe fix (TS001)

- **TS001** `table-spans-page` — a markdown table is rendered across a page
  break without an explicit `<!-- table-break -->`. Word silently splits the
  table mid-flow, no continuation header, looks broken. UNSAFE autofix: inserts
  `<!-- table-break -->` at the row that overflowed, plus
  `<!-- prettier-ignore-start/end -->` wrappers around the whole table when
  absent (without wrappers, prettier reformats the new break and corrupts it).

  UNSAFE because the _position_ is mechanically derived from PyMuPDF's row
  count on the spanning page, but the _choice_ of split row is sometimes
  layout-aesthetic — you may prefer to split earlier to keep a logical group
  intact (paired rows, summary rows, etc.).

  Apply:

  ```bash
  stphelper render input.md --fix --unsafe-fixes
  git diff input.md
  ```

  Review the diff. If the autofix split at the wrong row, move the
  `<!-- table-break -->` line manually — keep it inside the prettier-ignore
  wrappers. Don't delete the wrappers when relocating the break.

  When the diagnostic fires without an autofix (no `[*]` marker), the row
  counting was ambiguous — usually merged cells via empty-cell colspan
  confused PyMuPDF's table detector. Insert the break manually.

  Multi-pass: very tall tables converge over multiple `--fix` passes. After
  fixing the first span, re-run; if a continuation segment is itself too
  long, TS001 fires again with a fresh diagnostic. This is expected.

### Stage 6 — manual: code ratio (CR001)

- **CR001** `code-ratio` — a page is more than 40% code. The diagnostic prints
  a `blocks:` summary listing every code block on the page as
  `L<start_md>:<pdf_lines>` (`*` marks the **overflow block** — the first one
  in source order that pushes cumulative code over 40%, not necessarily the
  largest), then a green/red keep/cut hint for the overflow block.
- The cited line and the green/red rows are the overflow block. Read the
  `blocks:` summary before deciding what to cut: the largest block is often a
  better target than the cited one, and shrinking it may resolve the page
  without touching the cited block at all.

No autofix. This is the rule agents handle worst — be careful.

Preferred tactics, in order:

1. **Delete.** Drop imports, boilerplate, trivial getters/setters, blank
   lines, and repeated patterns (keep one example, elide the rest with
   `// ...`). A shorter listing is almost always the right answer.
2. **Collapse.** Replace long repeated branches with `// ...` or `// и т.д.`
   inside the same code block.
3. **Split only as a last resort.** If you must split a listing across two
   code blocks, **do not invent connecting prose**. Write one short sentence
   at most (e.g. `Продолжение листинга ниже.`) — ideally nothing. See the
   _Anti-filler_ section below for the full list of walkthrough-prose
   patterns to avoid — they apply here too.

Do not paraphrase deleted code into prose. That makes the page longer, not
shorter, and it's almost always the exact filler a human reviewer will call
out.

Re-run after each round; the percentage and target block will shift. If
you find yourself editing the same block for the third time, stop — see
_When local edits aren't converging_ below.

### Stage 7 — manual: figure redistribution (IM002)

- **IM002** `too-many-figures-per-page` — more than two figures landed on a
  single rendered page. The convention is "an image can take more than half a
  page _if_ there aren't several of them" — three or more figures crowded
  together usually means the surrounding prose between them is too short.

Options, in order of preference:

1. **Add explanatory prose between figures** so each one has its own context
   paragraph, naturally pushing later figures onto the next page.
2. **Merge two related figures** into a single composite (e.g. two screenshots
   showing before/after into one labelled image).
3. **Move a figure** to a more relevant nearby section. Sometimes a figure is
   placed at the end of a section when it fits better mid-section.
4. **Drop a figure** that's redundant with surrounding prose or another figure.

Resolve before PF001 — moving figures shifts pagination, which invalidates
PF001 measurements.

### Stage 8 — manual: page fill (PF001)

- **PF001** `page-fill` — the page ends well above the typical baseline (the
  75th percentile of last-line y across all pages). Usually means a forced
  page break (heading, table) left the previous page underfilled.

Expand the body text preceding the break. The diagnostic prints a `ДОПИШИ…`
placeholder sized to the gap — use it as a rough target length for how much
prose to add.

Do this **last**: every earlier fix changes pagination, so fill decisions made
too early tend to get invalidated.

If the page adjacent to the PF001 page is code-heavy (near or above the CR001
threshold), **do not add prose** — see the PF001 ↔ CR001 conflict section below.
Local expansion in that situation just rotates the problem across pages.

### Stage 9 — project-wide: sources appendix size (SA001)

- **SA001** `sources-page-ratio` — combined `[[parts]] type = "sources"` page
  count exceeds 30% of the visible diploma total. Fires only on
  `stphelper build` (the per-file `render` / `lint` commands have no merged
  PDF, so they can't see the ratio). No autofix.

  The diagnostic prints the actual page count, ratio, and how many pages to
  cut. Resolve by editing the sources part(s) in `stphelper.toml`, in order
  of preference:
  1. **Add `exclude` patterns** for generated, vendored, or boilerplate code
     (`exclude = ["**/migrations/*", "*.pb.py", "vendor/**"]`). Cuts noise
     first.
  2. **Hand-pick with `select`** — when noise patterns aren't enough and only
     specific files actually warrant inclusion. Discover candidates with
     `stphelper sources --list --format json` (post-`exclude`, post-gitignore;
     each entry has `path`, `lines`, `bytes`). Then:
     - Rank files by `lines` and propose a shortlist of the ones whose names
       suggest core implementation (e.g. `models.py`, `views.py`, `main.py`)
       over plumbing (`__init__.py`, `urls.py`, fixtures, generated code).
     - **Ask the user** which files belong in the appendix, showing your
       guesses with line counts (e.g. "`src/models.py` — 320 lines (keep?),
       `src/views.py` — 280 lines (keep?), `src/migrations/0001_*.py` —
       45 lines (drop, autogenerated)?"). Do not pick silently — the
       appendix is the user's curated artifact.
     - Write the agreed list back as `select = [...]` (project-root-relative
       gitignore-style globs). Every entry must match ≥1 file or the build
       errors; rerun `--list` to verify.
  3. **Set or lower `max_pages`** on the sources part. Soft cap at file
     boundaries — drops whole files until the line budget fits. The
     diagnostic suggests a concrete value. Useful as a backstop when
     `select` is hard to author.
  4. **Trim `roots` or `extensions`** to scan less code overall.

  Re-run `stphelper build` after each round. Do this **after** all per-file
  stages converge — the merged PDF page count moves with every body edit, so
  the threshold can flip in either direction late in the iteration.

## When local edits aren't converging

Stages 6-8 tell you to fix diagnostics one at a time and re-run. That
works until two neighboring rules start fighting. Watch for these signs:

- **You're editing the same paragraph or code block for the 3rd time.** The
  local fix isn't wrong — the frame is wrong. Stop editing that block and
  widen your view to the full section.
- **Error count oscillates** across re-runs (3 → 1 → 3 → 2) instead of
  monotonically decreasing.
- **The same Edit keeps getting partially reverted** on the next round.

When this happens, stop running stphelper for a moment and do a structural
move instead of another local edit.

> **Ask the user first before any structural move.** Deleting a heading,
> removing a subsection, moving an algorithm, or redistributing content
> between sections changes what the document _says_, not just how it
> paginates. Section structure in a thesis is often dictated by external
> requirements the agent cannot see (institution template, supervisor's
> outline, ГОСТ). Propose the move, name the specific subsection or
> heading, and wait for approval. Do **not** delete content unilaterally
> to satisfy a layout rule.

### PF001 ↔ CR001 conflict

PF001 on page N combined with CR001 on page N±1 is the classic trap.
Expanding prose on page N to fix PF001 pushes that prose across the page
break, which either doesn't help CR001 or makes it worse. Options, in order
of preference:

1. **Shorten the code on the CR001 page.** Its trailing prose slides up into
   the underfilled page, fixing both rules in one edit.
2. **Move a section break.** Drop a subsection heading earlier, or delete a
   `###` heading near the bottom of the underfilled page — `###` headings
   pull the next paragraph across the page break with them, so when one
   lands near the bottom the page above gets left short.
3. **Remove an algorithm / subsection entirely.** A shorter, tighter
   document almost always scores better than a longer one padded with
   narration. 10 pages of dense algorithms > 12 pages half-filled.

### Structural-move menu

When local edits thrash and the conflict above doesn't apply, zoom out:

- **Cut a whole subsection** that exists mainly to fill space. Deletion
  almost always helps both PF001 (ripple removes short pages) and CR001
  (less total content, denser packing).
- **Redistribute code between subsections** so no single subsection is
  > 40% code. Don't split one listing into two — move a different one.
- **Demote or delete a heading.** Forced page breaks from `##` / heavy
  `###` are the root cause of most PF001 hits. One fewer heading =
  one fewer forced break = one fewer underfilled page.

## Anti-filler: prose patterns to avoid everywhere

Stage 6 bans narration-style prose _between_ split code blocks. The same
patterns are filler _anywhere_ they appear — especially after a code block
or in a PF001 "expand this page" edit:

- `Первое действие – …`
- `Далее выполняется …`
- `После этого …`
- `Последнее действие – …`
- `Данный метод принимает на вход …` (restating the signature)

Step-by-step walkthroughs of code that was just printed right above add zero
information — the reader has the code. They are the primary form of "вода"
and they multiply every time you try to fix PF001 by expanding a code-
adjacent page. `stphelper` cannot detect them, but a human reviewer will.

If you need text after a code block, it should **add context the code
doesn't show**: a design tradeoff, a reference to another subsection, a
constraint that motivated the approach, an invariant that isn't obvious
from the listing. Not a prose restatement of control flow.

## Formula rendering (authoring reference)

Formulas render as real Office Math (OMML) with fraction bars, subscripts, sums,
etc. No lint rules cover this yet — the guidance here is authoring-only.

### Numbered formula (default)

LaTeX between `$$ … $$` on its own lines. Auto-numbered `(X.Y)` on the right.

```markdown
$$
P_р = \frac{З_о \cdot Н_р}{100},
$$

где $Н_р$ – норматив расходов на реализацию, %.
```

- The `(X.Y)` label is produced by Word's list numbering — do **not** type the
  number in the markdown.
- A trailing `,` or `.` inside `$$ … $$` is peeled out automatically and rendered
  in Times New Roman (upright), not Cambria Math. Write the natural sentence
  punctuation inside the block; don't try to hoist it out.

### Calculation (unnumbered)

An HTML comment `<!-- calc -->` on its own line immediately before `$$ … $$`
flags the block as a calculation — centered, no number:

```markdown
<!-- calc -->

$$
P_р = \frac{24357{,}14 \cdot 3}{100} = 730{,}71~р.
$$
```

### "где …" variable definitions

The paragraph immediately after a numbered formula, if it starts with `где`,
is auto-styled `Где (формула)` and gets a tab between `где` and the rest:

```markdown
где $К_{пр}$ – коэффициент премий;

$n$ – категория исполнителей, которые заняты разработкой;

$З_{чi}$ – часовой оклад исполнителя i-ой категории, р.;
```

- Use inline math `$…$` for the variable names so they render in math italic.
- Each subsequent definition is its own body paragraph (blank line between).
- The en-dash between variable and description is automatically tightened to
  non-breaking spaces on both sides (`$X$ – …` → `$X$&nbsp;–&nbsp;…`) so the
  dash stays glued to the variable. Don't add `&nbsp;` manually.

### What not to do

- **No bullet list under `где:`**. A `- $a$ – first` list with bullets is not
  the convention. Write plain paragraphs, one per definition.
- **No manual `(1.5)` labels** on numbered formulas. Auto-numbering handles it.
- **No manual blank paragraphs** around formulas for spacing. The renderer sets
  `space_before`/`space_after` on the right paragraphs already.
- **No inline math inside `$$ … $$`**. It's one mode at a time — either a whole
  block is display math, or `$…$` is inline inside regular prose.

## Table rendering (authoring reference)

Standard GFM tables. Two extensions of the standard syntax matter for thesis-
style tables; both are pure GFM (no project-specific magic) and mistune parses
them natively.

### Per-column alignment via separator markers

Body cells default to **centered**. Override per column with the GFM colon
markers in the separator row:

| marker  | alignment | typical use                     |
| ------- | --------- | ------------------------------- |
| `:---`  | LEFT      | label / category column         |
| `:---:` | CENTER    | explicit center (same as `---`) |
| `---:`  | RIGHT     | numeric / monetary column       |
| `---`   | CENTER    | default, no override            |

```markdown
| Категория исполнителя | Месячный оклад | Часовой оклад | Трудоёмкость | Итого, р. |
| :-------------------- | :------------: | :-----------: | :----------: | --------: |
| Backend/AI-инженер    |      4200      |     25,00     |     340      |   8500,00 |
```

Header rows always render centered (the `Центр` style) regardless of markers
— the colons govern body cells only.

### Colspan via empty cells

A body cell with no content merges leftward into the preceding non-empty cell.
Useful for summary / total rows where a single label spans the data columns:

```markdown
| Категория            | Мес. оклад | Час. оклад | Труд. | Итого, р. |
| :------------------- | :--------: | :--------: | :---: | --------: |
| ...                  |
| Итого                |            |            |       |  15714,29 |
| Премия (55%)         |            |            |       |   8642,86 |
| Всего затраты на ... |            |            |       |  24357,14 |
```

Mistune requires every row to have the same cell count as the header, so the
empties are mandatory padding — not optional. A merged anchor inherits its
starting column's alignment, so combining `:---` on column 0 with `---:` on
the last column gives the conventional left-label / right-value summary look
for free.

Runs of consecutive empty cells all merge into the same anchor. An empty cell
at the **start** of a row has no left anchor and stays empty (no merge).

### Forcing a visually empty but unmerged cell

If you genuinely need an empty cell that does **not** merge — rare in technical tables, where N/A is usually spelled out — write `&nbsp;` as the
content. The entity survives `strip()`, so it counts as content for the merge
detector but renders as a non-breaking space (visually empty).

### Per-table column widths

By default content tables inherit equal-width columns from the template, so a
column whose content is wider than its `1/n` share wraps to multiple visual
lines. To pin column widths, place a `<!-- table-widths -->` pragma on its own
line immediately before the table (or its caption):

```markdown
<!-- table-widths: 3.5 10.5 2.5 -->

| Название продукта | Модель подписки                 | Цена, $ за год |
| :---------------- | ------------------------------- | -------------- |
| Crunchbase Pro    | Подписка за пользователя на год | 588            |
```

- Bare space-separated **cm** values, one per column. No unit suffix.
- Sum should equal the text-area width (16.5 cm). A different sum produces a
  stderr warning but does not abort — useful for deliberately narrow tables.
- Column-count mismatch (`<!-- table-widths: 4 10 -->` on a 3-column table)
  raises `ValueError` and aborts the run.
- One pragma per logical table — it persists across `<!-- table-break -->`
  automatically, so the continuation segment uses the same widths. Don't
  repeat it before the second segment.

When to use it: the row-wraps-to-two-lines symptom in the rendered PDF, or
when a table you didn't want to split is forced across pages because rows
are too tall.

### What not to do

- **Don't type the `Таблица X.Y` number** in a heading or paragraph; the
  caption paragraph (`Таблица 1.1 – Description`) auto-numbers via Word's
  list. The `Таблица X.Y – ` prefix in the source is stripped before render.
- **Don't use `<!-- table-break -->` to express colspan.** That marker
  splits a table into a "Продолжение таблицы X.Y" continuation with its
  own number row — it's for tables that genuinely break across pages, not
  for summary rows. Use empty-cell colspan instead, in the same table.
- **Don't add manual `\***1***`/`***2**\*` number rows.** The renderer adds
  the `1 2 3 …` row automatically when (and only when) a table is split
  via `<!-- table-break -->`.
- **Don't add manual blank paragraphs around tables** for spacing. The
  renderer inserts the trailing spacer paragraph and skips it for split
  continuations.
- **Don't ignore TS001 by leaving the table unsplit.** When the linter says a
  table spans a page break, fix it — either accept the autofix
  (`--fix --unsafe-fixes`) or place `<!-- table-break -->` manually at your
  preferred row. A silently-spanning table renders without a "Продолжение
  таблицы X.Y" continuation header, which violates the convention.

## Image rendering (authoring reference)

Standard Markdown image syntax emits a centered, numbered figure with its
caption below. Two lint rules cover image layout: **IM001** (bad aspect
ratio) and **IM002** (too many figures per page) — see the workflow stages.

```markdown
![Рисунок 1.1 – Схема тестовой системы](img/schema.png)
```

- The `Рисунок X.Y` number is produced by Word's list — do **not** rely on the
  number in the alt text for layout. The `Рисунок X.Y – ` prefix in the source
  is stripped before rendering; it's only there so the markdown reads naturally.
- The image must be the **sole content of its paragraph** (one blank line before
  and after in the source). Mixed text + inline image raises an error — there's
  no matching Word style for that layout.
- Caption text is the alt text. Bold/italic/inline-math in the caption work
  (e.g. `![Рисунок 1.1 – Зависимость $y(x)$](plot.png)`).
- The image path is resolved relative to the markdown file. Missing files raise
  `FileNotFoundError` with the resolved path — no silent fallback.

### Default sizing (no directive)

Both axes are capped, aspect ratio preserved, whichever cap binds first wins:

- **Width** is hard-capped at 16.5 cm (page text width). Always enforced.
- **Height** is soft-capped at 12.85 cm (~50% of the text-area height). Applied
  by default to prevent any single image dominating its page; overridable per
  image via the directive below.

Images that fit both caps render at native size.

### Per-figure directive: `<!-- image: ... -->`

Place on its own line **immediately before** the image. Carries any combination
of: `width=N` (cm), `height=N` (cm), `native` (use intrinsic size, width-cap
only), `border` (thin black 1 pt outline). `width`, `height`, and `native` are
mutually exclusive — they all decide sizing. `border` is orthogonal to size.

```markdown
<!-- image: width=10 -->

![Рисунок 2.1 – Схема](schema.png)

<!-- image: height=8 border -->

![Рисунок 2.2 – Окно приложения](window.png)

<!-- image: native border -->

![Рисунок 2.3 – Полноразмерный плакат](poster.png)
```

- Use `native` to opt out of the 12.85 cm height cap when an image legitimately
  needs to be tall. The 16.5 cm width cap still applies.
- Use `border` for screenshots whose own background blends into the page — UI
  windows on white, light diagrams without their own frame, etc.
- Out-of-range values (`width=20`, `width=10 height=5`, unknown attributes)
  raise `ValueError` at build time with the source line number.

### What not to do

- **No manual `Рисунок 1.1` labels** in plain paragraphs. The caption paragraph
  auto-numbers.
- **No manual blank paragraphs** around figures for spacing. The renderer
  handles gaps before the image and after the caption, and collapses the
  figure-to-figure gap to one blank line when two figures are adjacent.
- **No inline images** (`text ![x](y) text`). Must be alone in its paragraph.
- **No title-less figures** (`![](img.png)`). Word's list always appends `–`,
  so the caption would render as `Рисунок 1.3 – ` with a trailing separator.
  Always provide a caption.
- **No `width=` and `height=` together.** They're mutually exclusive — pick one
  axis, the other follows from the source aspect ratio. Forcing both would
  distort the image.
- **Don't reach for `native` to silence IM001.** IM001 reads the rendered dims
  _including_ the directive, so opting out of the height cap with `native` just
  produces a larger image with the same elongated aspect — still flagged. Fix
  the source image instead.

## Full rule catalog

| Code  | Name                         | Category    | Needs PDF | Fix    | Stage |
| ----- | ---------------------------- | ----------- | --------- | ------ | ----- |
| YR001 | yo-to-ye                     | CORRECTNESS | no        | SAFE   | 1     |
| ED001 | em-dash                      | STYLE       | no        | SAFE   | 1     |
| LP001 | list-punctuation             | STYLE       | no        | SAFE   | 1     |
| LP002 | numbered-list-capitalization | STYLE       | no        | SAFE   | 1     |
| BD001 | bare-digits                  | CORRECTNESS | no        | UNSAFE | 2     |
| SL001 | single-item-list             | STYLE       | no        | —      | 3     |
| IM001 | image-bad-aspect             | STYLE       | no        | —      | 3     |
| CR002 | blank-code-at-page-edge      | LAYOUT      | yes       | SAFE   | 4     |
| DW001 | dash-wrapping                | LAYOUT      | yes       | SAFE   | 4     |
| TS001 | table-spans-page             | LAYOUT      | yes       | UNSAFE | 5     |
| CR001 | code-ratio                   | LAYOUT      | yes       | —      | 6     |
| IM002 | too-many-figures-per-page    | LAYOUT      | yes       | —      | 7     |
| PF001 | page-fill                    | LAYOUT      | yes       | —      | 8     |
| SA001 | sources-page-ratio           | LAYOUT      | yes       | —      | 9     |

## Flags quick reference

- `--fix` — apply SAFE fixes to the markdown source.
- `--fix --unsafe-fixes` — also apply UNSAFE fixes (review the diff after).
- `--skill` — print this document and exit.
- `-t TEMPLATE` — override the bundled `template.docx`.
- `-o OUTPUT` — override the default `<input>.docx` output path.

## Tips

- Commit between stages. Each stage's fixes are easy to review in isolation
  and trivial to revert if something went wrong.
- Re-run after every round of manual edits — layout rules can cascade.

## Reading output without blowing up context

The full diagnostic stream is long — especially `CR001` hint blocks and
`PF001` `ДОПИШИ…` placeholders. Don't pipe the whole thing back into your
context window, and don't re-run stphelper just to re-read it (each run
spawns Word and is slow).

Apply Agent rule 1 (see top of document): use `Read`/`Grep` on `.lint.out`,
not shell `sed`/`grep`/`head`/`tail`.

Workflow:

1. **Apply fixes first.** `--fix` and `--fix --unsafe-fixes` remove those
   diagnostics from the output entirely. Fewer warnings in = less to read.
2. **Save the run to a project-local file** (not `/tmp/`, which lives
   outside the working directory and often triggers extra permission
   prompts). Add it to `.gitignore`:

   ```bash
   stphelper render input.md > .lint.out 2>&1
   ```

3. **Query the file with `Grep`, not by reading it whole.**
   - Summary only — one line per rule group plus the footer:
     `Grep` pattern `^(⚠|Found|\[\*\])` on `.lint.out`.
   - Locations for a single rule:
     `Grep` pattern `CR001|input\.md:[0-9]+` with `-A 2` for context.
   - Block-style diagnostics (CR001 hint block, PF001 placeholder):
     use `Grep` with `-A 40` on the rule header line (`⚠ .* \[CR001\]`)
     rather than slurping the whole file.

4. **Read markdown source directly**, not the pasted context lines. The
   diagnostic truncates each context line to ~120 chars anyway; use
   `Read` with `offset=LINE-2` `limit=5` on the real source file when you
   need to see the surrounding lines.

Rule of thumb: if you're about to load more than ~50 lines of stphelper
output into context, you're doing it wrong. Fix, filter, or slice first.
