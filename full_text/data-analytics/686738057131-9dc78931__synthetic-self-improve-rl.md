---
name: synthetic-self-improve-rl
description: Teacher/student self-improvement loop. Claude post-trains a smaller student model on a real dataset via prime-rl, analyzes failed training traces, generates a 500-1000 row dataset targeting the model's weaknesses, wraps it as a verifiers environment, and re-trains in a loop until a wall-clock budget expires. Default student is Qwen/Qwen3-0.6B; override with --model. Use when the user types /synthetic-self-improve-rl <dataset>.
---

# synthetic-self-improve-rl

Maximize the student's `eval_reward_mean` on the real `<hub-id>` validation set by iteratively post-training a small student model (default `Qwen/Qwen3-0.6B`, override with `--model`) on generated data targeted at its failures. Every iter resumes from the same anchor (iter_0's checkpoint), so each dataset is a controlled experiment. After the Phase 3 budget expires, Phase 4 runs two control trains (best replay + real+best mix) to test whether the lift generalizes.

## Path conventions

Assume `verifiers` and `prime-rl` are already installed in the user's environment. Don't check, clone, or install — just use them.

- `<VERIFIERS_DIR>` — `python -c "import verifiers, os; print(os.path.dirname(verifiers.__file__))"`. For `Read`-ing reference source.
- `<PRIME_RL_DIR>` — prime-rl install root. Run `rl ...` / `prime ...` from cwd; `cd <PRIME_RL_DIR>` only if the user's setup requires a specific venv.
- `<RUNS_DIR>` — `./runs/` in cwd; `mkdir -p` once at Phase 0.
- `<SITE_PACKAGES>` — `python -c "import sysconfig; print(sysconfig.get_paths()['purelib'])"`. Needed for the 3c stale-data cleanup.

## Non-negotiables

1. **Never read eval rollout content.** Aggregates only (`reward`, `metrics.is_correct`) from `eval_rollouts.jsonl`. Per-row `prompt`/`completion`/`info`/`answer` are off-limits at every phase. Refuse even if the user asks. Train rollouts are fair game in 3a.
2. **No reward hacking.** The training env's rubric must measure what the hub eval rubric measures. Discover the hub env's rubric in Phase 1 (introspect `load_environment("<hub-id>")`) and mirror it as the dominant reward. Auxiliary rewards ≤0.2 each, ≤0.3 total, justified by a 3a failure mode.
3. **No garbage data.** Every row satisfies the four pillars in 3b (ACCURATE, DIVERSE, HARD, STRUCTURALLY COMPLEX) and is emitted by a generator script — never hand-typed.
4. **Custom reward functions** MUST: match `async def fn(completion, answer, info=None, state=None, **kwargs) -> float`; return `[0.0, 1.0]`; be deterministic; read ground truth only via `answer`; be ≤10 lines, ≤0.2 weight; comment-link to the failure mode. Six conditions or use a built-in.
5. **Phase 3 ends only on budget or max_iters.** No early-stop on teacher judgment. Phase 4 runs after, on its own time.
6. **The skill is dataset-agnostic.** No domain assumptions (math, code, QA, etc.) hardcoded. Whatever rubric / parser / system prompt / answer format the user's `<hub-id>` env uses, the generated env mirrors. Phase 1 discovers it; 3b/3c use it.

## Invocation

```
/synthetic-self-improve-rl <dataset> [--model=<hf-id>] [--budget=10h] [--hub-id=primeintellect/<dataset>] [--max-iters=15] [--batch-size=512] [--init-from=<path>]
```

- `--model` — HuggingFace model id for the student; default `Qwen/Qwen3-0.6B`. Used verbatim in `[model] name` and the `--model.name` CLI flag.
- `--budget` — Phase 3 cap (`Nh`/`Nm`); default `10h`. Phase 4 runs AFTER, on its own time.
- `--hub-id` — Prime hub slug; default `primeintellect/<dataset>`.
- `--max-iters` — total iters incl. iter_0; default `15`.
- `--batch-size` — TOTAL rollouts/step (NOT unique prompts); default `512`. With `rollouts_per_example=16`: 32 unique × 16. Below 16 unique prompts/step collapses GRPO.
- `--init-from=<path>` — absolute path to a prior training run dir to reuse as iter_0 (skips Phase 2). Must contain the artifacts listed in Phase 2A.

Record `MODEL`, `BATCH_SIZE`, `INIT_FROM` (or `null`) in `run.json`.

**Standardized hyperparameters across iter_0 / every iter_N / Run A / Run B:** 100 new training steps per run, `rollouts_per_example = 16`, `batch_size = <BATCH_SIZE>`.

`max_steps` is **ABSOLUTE**: iter_0 → `100`; iter_N resuming from step `F` → `F + 100`. Setting `max_steps = F` on a resume trains zero new steps and crashes with `KeyError: 'perf/peak_memory'`. `[ckpt] resume_step` is an integer, not a path. Everything else (LR, `max_completion_tokens`, `seq_len`, temp) is teacher's discretion per iter.

---

## Phase 0 — bootstrap

1. `RUN_DIR = <RUNS_DIR>/<dataset>-<UTC iso, colon-stripped>`. `mkdir -p`.
2. Write `<RUN_DIR>/run.json`:
   ```json
   {"dataset":"<dataset>","hub_id":"<hub-id>","model":"<MODEL>","start_ts":<ts>,"budget_seconds":<bs>,"max_iters":<int>,"batch_size":<BS>,"init_from":<INIT_FROM or null>,"status":"running","compact_warnings":[]}
   ```
3. `<RUN_DIR>/metrics.json` = `{"iters":[]}`. Initialize `<RUN_DIR>/scratchpad.md` with the run header. TaskCreate one task per phase.

## Phase 1 — verify and introspect hub env

```bash
prime env info <hub-id>
```

Non-zero / `not found` → `run.json.status = "aborted"`, `reason = "hub env <hub-id> not found"`, stop.

Then **introspect** the hub env to discover what stack the generated env (Phase 3c) must mirror. The hub env is the source of truth for rubric, parser, system_prompt, and answer format — the skill makes no domain assumptions.

```bash
prime env install <hub-id>   # install locally so load_environment works (skip if already installed)
uv run python - <<'PY'
from verifiers import load_environment
env = load_environment("<hub-id>")
print({
  "env_class": type(env).__name__,
  "parser_class": type(env.parser).__name__,
  "rubric_class": type(env.rubric).__name__,
  "rubric_funcs": [f.__name__ for f in getattr(env.rubric, "reward_funcs", [])],
  "system_prompt": (env.system_prompt or "")[:200],
})
PY
```

Record the discovered stack in `<RUN_DIR>/hub_env.json` (env_class, parser_class, rubric_class, rubric_funcs, full system_prompt, the system_prompt's exact answer-format instruction). Also inspect a few rows of the hub env's dataset to learn the canonical answer format (e.g. how the dataset's `answer` field is encoded, what wrapper/delimiter the rubric expects in completions). Use this in 3b's schema and 3c's `load_environment`. The teacher refers to `hub_env.json` whenever it needs to know "what format does the hub env expect?".

---

## Phase 2 — iter_0 baseline

`--init-from` set → 2A. Otherwise → 2B.

### Phase 2A — `--init-from` short-circuit

Reuse a prior training run in place (the same model, trained on the real dataset for ≥100 steps with eval saved).

1. Find `<F>` = max `step_N` in `<INIT_FROM>/prime_out/weights/`. Validate (any missing → abort):
   ```
   <INIT_FROM>/{run,metrics}.json
   <INIT_FROM>/prime_out/weights/step_<F>/{model.safetensors,config.json,tokenizer.json}
   <INIT_FROM>/prime_out/checkpoints/step_<F>/trainer/__0_0.distcp
   <INIT_FROM>/prime_out/run_default/rollouts/step_<F>/{train,eval}_rollouts.jsonl
   ```

2. Symlink (avoid copying GB of weights):
   ```bash
   mkdir -p <RUN_DIR>/iter_0/prime_out/{run_default/rollouts,weights,checkpoints}
   ln -s <INIT_FROM>/prime_out/weights/step_<F>           <RUN_DIR>/iter_0/prime_out/weights/step_<F>
   ln -s <INIT_FROM>/prime_out/checkpoints/step_<F>       <RUN_DIR>/iter_0/prime_out/checkpoints/step_<F>
   for s in <INIT_FROM>/prime_out/run_default/rollouts/step_*; do
     ln -s "$s" "<RUN_DIR>/iter_0/prime_out/run_default/rollouts/$(basename $s)"
   done
   ```

3. Pull aggregate `eval_acc` from `<INIT_FROM>/metrics.json` → `<RUN_DIR>/iter_0/eval_summary.json` (`source: "init-from"`). Append to `metrics.json.iters`. Record `iter_0_source`/`iter_0_path`/`iter_0_step` in `run.json`. Append iter_0 scratchpad entry (Source = "Inherited via --init-from"; skip trajectory).

### Phase 2B — normal training

Use the canonical config as-is; do NOT author a new `rl.toml`.

1. Locate `<PRIME_RL_DIR>/configs/<dataset>/rl.toml`. If missing, model on any existing `configs/<other-dataset>/rl.toml` and adjust `[[orchestrator.train.env]]` so it loads the user's `<dataset>` (the `id` / `name` / `args` mirror what `<hub-id>` itself uses — `prime env info <hub-id>` shows them).

2. Write `<RUN_DIR>/iter_0/eval_overlay.toml` — `[ckpt]` is mandatory (without it Phase 3 has nothing to resume from). CLI list-indexed overrides fail when the list doesn't exist yet, so use an overlay:
   ```toml
   [ckpt]
   interval = 100             # = max_steps → save exactly one checkpoint
   [orchestrator.eval]
   interval = 100
   [orchestrator.eval.sampling]
   max_completion_tokens = 2048
   [[orchestrator.eval.env]]
   id = "<hub-id>"
   num_examples = 200
   rollouts_per_example = 1
   ```

3. Launch:
   ```bash
   uv run rl @ <PRIME_RL_DIR>/configs/<dataset>/rl.toml @ <RUN_DIR>/iter_0/eval_overlay.toml \
       --model.name <MODEL> \
       --max-steps 100 \
       --orchestrator.batch-size <BATCH_SIZE> \
       --orchestrator.rollouts-per-example 16 \
       --output-dir <RUN_DIR>/iter_0/prime_out
   ```

4. Find final step `<N>` (`ls <RUN_DIR>/iter_0/prime_out/run_default/rollouts/ | sort -V | tail -1`). Aggregate `eval_rollouts.jsonl` (numeric fields ONLY — never `prompt`/`completion`/`info`/`answer`):
   ```bash
   uv run python -c "
   import json
   acc, rew, n = 0, 0.0, 0
   for line in open('<RUN_DIR>/iter_0/prime_out/run_default/rollouts/step_<N>/eval_rollouts.jsonl'):
       r = json.loads(line); n += 1
       rew += float(r.get('reward', 0.0))
       acc += int(r.get('metrics',{}).get('is_correct', 1 if r.get('reward',0) >= 0.5 else 0))
   print(json.dumps({'eval_acc': acc/n, 'eval_reward_mean': rew/n, 'n_eval': n}))
   "
   ```

5. Write `<RUN_DIR>/iter_0/eval_summary.json` (add `train_reward_mean`, `checkpoint`). Append to `metrics.json.iters`. Append iter_0 scratchpad entry with trajectory by 20-step buckets.

prime-rl writes rollouts under `<output_dir>/run_default/`; trainer dirs (`checkpoints/`, `weights/`) live directly under `<output_dir>/`. Both trees needed for resume. Missing/empty `eval_rollouts.jsonl` → abort.

---

## Phase 3 — generation loop

Every iter resumes from iter_0's checkpoint — NOT base, NOT iter_<N-1>. Same anchor every time.

**Pre-iter budget gate (the ONLY way Phase 3 ends):**
```
if elapsed >= BUDGET_SECONDS:  break (status: budget_exhausted)
if iter_index >= max_iters:    break (status: max_iters_reached)
```

For each iteration `N` from 1:

### 3a. Weakness analysis

Read up to 200 low-reward rows from `<RUN_DIR>/iter_<N-1>/prime_out/run_default/rollouts/step_<F>/train_rollouts.jsonl` (sort by reward asc). Eval traces stay off-limits; only `eval_acc` from `eval_summary.json`.

Write `<RUN_DIR>/iter_<N>/weakness_report.md`:

- **Eval accuracy from iter_<N-1>.**
- **Reward-by-length quartile** — flag truncation vs reasoning failures.
- **Domains** — 3-6 entries, 3-4 word labels, severity-ordered. Per domain: severity (high/med/low), one-sentence evidence paraphrasing 1-2 failed prompts, 2-5 `sub_domains` with ≤6-word failure-mode labels.
- **Bucket allocations** — flat `(domain, sub_domain) → target_row_count` summing to `[500, 1000]`. Proportional to severity; every bucket ≥3%.
- **Structural features** — 4-6 task-specific structural patterns the teacher identified by reading low-reward train rollouts (used by Pillar 4 in 3b). Each gets a short label + one-sentence definition. Examples for math: unit conversion / temporal scaling / multi-fact aggregation. Examples for code: multi-file edits / type-coupled changes / exception-path handling. Examples for QA: multi-hop reasoning / distractor passages / numeric grounding. **Define what's actually in this dataset's failures — do not copy a list from elsewhere.** (iter_1 defines the list from scratch; iter_2+ may extend or revise it based on new failure modes.)

### 3a.5. Pre-iter scratchpad entry

Read every prior scratchpad entry. Append `## Iteration N — <UTC ts>` with 5 sections: (1) understanding from traces, (2) `(domain, sub_domain)` buckets to focus on with target counts, (3) plan for the data (templates, diversity axes, reuse), (4) hyperparameter/reward changes + rationale, (5) Results = `<to be filled at end of 3e>`.

### 3b. Dataset

Write `<RUN_DIR>/iter_<N>/dataset.jsonl` — 500-1000 rows targeting `weakness_report.md`. Schema:

```json
{
  "question": "<input the student sees, formatted as the hub env expects>",
  "answer": "<ground truth in the exact form the hub rubric compares against (see hub_env.json)>",
  "info": {
    "domain": "<3-4 word label from 3a>",
    "sub_domain": "<failure mode label from 3a>",
    "difficulty": "<easy|med|hard>",
    "structural_features": ["..."],
    "source": "<teacher-invented | skeleton:train_step_<S>_idx_<I>>",
    "reasoning": "<derivation in whatever format the hub system_prompt asks for (e.g. a wrapped answer, a fenced code block, a tag-delimited final answer — read hub_env.json>"
  }
}
```

The exact encoding of `answer` and `reasoning` is dictated by the hub env discovered in Phase 1 — not by this skill. `info.domain` / `sub_domain` must match a pair in `weakness_report.md` (no new labels at 3b — fix the report first). No duplicates; no trivial paraphrases of prior iters' rows.

#### Generator script — mandatory, NOT hand-typed

Every row is emitted by `<RUN_DIR>/iter_<N>/gen_dataset.py`. Hand-typing is forbidden — a prior run terminated at iter_2 because authoring 700+ rows by hand exhausted teacher context. Script-based = `O(templates)` not `O(rows)`.

The generator:
1. Defines **parametrized templates** — functions returning `(question, answer, info)` from sampled params. One template per `(domain, sub_domain)`. Each template encodes the question + answer in the hub env's expected format (from `hub_env.json`).
2. Includes a **deterministic solver** per template — the answer is computed in Python from the sampled params (closed-form for math; reference output for code; canonical label for QA; etc.). `info.reasoning` is built so that whatever the hub rubric extracts (a wrapped answer, fenced code block, delimited final field) is present and equals `answer`.
3. Treats **skeleton paraphrases** as templates too: pick a failed prompt's skeleton from 3a, encode it, sample fresh params. Tag `info.source = "skeleton:train_step_<S>_idx_<I>"`.
4. Writes rows directly: `for _ in range(N): json.dump(template(sample_params()), f); f.write("\n")`.
5. Ends with a **round-trip assert block** — sample 5 rows per template, run the *hub env's parser* over `info.reasoning`, assert the extracted value equals the solver's `answer`. Mismatch → fix the template. Audit 20 random emitted rows cold-read; failure → fix template, re-run; never patch individual rows.

#### Four pillars

1. **ACCURATE** — round-trip assert + cold-read audit deliver this.
2. **DIVERSE (structurally, not lexically).** Per bucket, vary across ≥3 of: cover story, reasoning depth (no single depth >70%), surface structure, number characteristics, distractor presence. Clones differing only in names/numbers count as one row.
3. **HARD** — ≥40% `hard`, ≤20% `easy`. Calibrate by iter_<N-1> eval acc: <0.10 → bias `med`; 0.10-0.35 → targets above; >0.35 → bias harder. Every `hard` still has one closed-form answer.
4. **STRUCTURALLY COMPLEX** — difficulty must come from real-task-shaped compositional mess, not surface knobs (bigger numbers, longer strings, more whitespace). The teacher identifies **4-6 task-appropriate structural features** in 3a (recorded in `weakness_report.md` under a `structural_features:` list) based on what distinguishes the dataset's hardest *real* train failures from clean textbook-style examples. Features are dataset-specific — math problems show one pattern, code shows another, multi-hop QA shows another. Pick what's actually present in the low-reward rollouts.

   Every row carries **≥2** features in `info.structural_features`. Targets: ≥80% rows ≥2 features; ≥40% ≥3; every defined feature appears in ≥10% of rows.

**Skeleton-paraphrase floor: ≥30% of rows.** Preserve the failed prompt's compositional skeleton; change cover story + units + numbers. Never copy verbatim; "Sally→Sarah, 5→7" is an alias (forbidden by Pillar 2).

#### Validation gate — run before 3c

```bash
uv run python -c "
import json, collections
rows = [json.loads(l) for l in open('<RUN_DIR>/iter_<N>/dataset.jsonl')]
T = len(rows)
doms = collections.Counter(r['info']['domain'] for r in rows)
subs = collections.Counter((r['info']['domain'], r['info']['sub_domain']) for r in rows)
diff = collections.Counter(r['info']['difficulty'] for r in rows)
feats = [r['info'].get('structural_features', []) for r in rows]
per_feat = collections.Counter(f for fs in feats for f in fs)
n2 = sum(1 for f in feats if len(f) >= 2)
n3 = sum(1 for f in feats if len(f) >= 3)
n_skel = sum(1 for r in rows if str(r['info'].get('source','')).startswith('skeleton:'))
print('>=3 domains:', len(doms) >= 3)
print('every dom >=2 sub:', all(sum(1 for (d,s) in subs if d==dom) >= 2 for dom in doms))
print('smallest (dom,sub) >=3%:', min(subs.values())/T >= 0.03)
print('hard >=40%:', diff.get('hard',0)/T >= 0.40)
print('easy <=20%:', diff.get('easy',0)/T <= 0.20)
print('>=2 features (>=80%):', n2/T >= 0.80)
print('>=3 features (>=40%):', n3/T >= 0.40)
print('per-feature coverage (each >=10%):', all(v/T >= 0.10 for v in per_feat.values()))
print('skeleton-source (>=30%):', n_skel/T >= 0.30)
"
```

Every line must print `True`. Fix specific failures in the generator; do not lower the bar.

### 3c. Environment

The generated env must **mirror the hub env's stack** from `<RUN_DIR>/hub_env.json` (recorded in Phase 1). Use the same Env class, the same Parser class, the same Rubric class, and the same `system_prompt` string — only the dataset differs. Custom rewards only when (a) weakness_report names a failure mode no built-in covers AND (b) Non-Negotiable #4 holds.

**If `<MODEL>` is a Qwen3 variant, never wrap completions with a parser that strips `<think>` tags** (e.g. `vf.ThinkParser`) — Qwen3 emits `<think>...</think>` and stripping it breaks rewards. Match the hub env's parser exactly; if the hub uses `ThinkParser`, that's the hub author's call, but verify it doesn't conflict with `<MODEL>`'s output style before mirroring.

**Directory + package naming uses underscores, NOT dashes** (`prime env install` resolves by underscored name). Create `<RUN_DIR>/iter_<N>/<dataset>_iter_<N>/` with two files:

`pyproject.toml`:
```toml
[project]
name = "<dataset>_iter_<N>"
version = "0.1.0"
requires-python = ">=3.10"
dependencies = ["verifiers>=0.1.8", "datasets"]
[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
[tool.hatch.build]
include = ["<dataset>_iter_<N>.py", "dataset.jsonl", "pyproject.toml"]
```

`<dataset>_iter_<N>.py` — skeleton; substitute the hub env's actual Env/Parser/Rubric/system_prompt classes (from `hub_env.json`) into the marked positions:

```python
import json
from pathlib import Path
import verifiers as vf
from datasets import Dataset
# Import the same Parser + Rubric classes the hub env uses (names recorded in hub_env.json).

DATA_PATH = Path(__file__).parent / "dataset.jsonl"
HUB_SYSTEM_PROMPT = """<verbatim system_prompt string from hub_env.json>"""

def _load_rows():
    rows = []
    with open(DATA_PATH) as f:
        for line in f:
            if line.strip():
                obj = json.loads(line)
                rows.append({"question": obj["question"], "answer": obj["answer"], "info": obj.get("info", {})})
    return rows

def load_environment(system_prompt=HUB_SYSTEM_PROMPT, num_train_examples=-1, **kwargs):
    rows = _load_rows()
    def build_dataset():
        ds = Dataset.from_list(rows)
        if num_train_examples != -1:
            ds = ds.select(range(min(num_train_examples, len(ds))))
        return ds
    rubric = <HubRubricClass>()            # ← from hub_env.json
    parser = <HubParserClass>()            # ← from hub_env.json; often rubric.parser
    return <HubEnvClass>(                  # ← from hub_env.json (usually vf.SingleTurnEnv)
        dataset=build_dataset,
        eval_dataset=build_dataset,        # training-only env; orchestrator routes eval to hub
        system_prompt=system_prompt,
        parser=parser,
        rubric=rubric,
    )
```

This env is training-only — eval routes to the hub via `[[orchestrator.eval.env]]` in rl.toml. Logs showing eval against `<dataset>_iter_<N>` → rl.toml is misconfigured.

**Cleanup-then-install — mandatory at every iter.** `[tool.hatch.build].include` puts `dataset.jsonl` at site-packages ROOT, where a stale copy from a prior iter silently survives reinstalls (real runs trained on stale rows for 90+ min before this was diagnosed):

```bash
cp <RUN_DIR>/iter_<N>/dataset.jsonl <RUN_DIR>/iter_<N>/<dataset>_iter_<N>/dataset.jsonl
SP=<SITE_PACKAGES>
rm -f "$SP/dataset.jsonl" "$SP/<dataset>_iter_<N>.py" "$SP/<dataset>_iter_<N>"-*.dist-info -r

prime env install <dataset>_iter_<N> -p <RUN_DIR>/iter_<N>

EXPECTED=$(wc -l < <RUN_DIR>/iter_<N>/dataset.jsonl)
uv run python -c "from verifiers import load_environment; env=load_environment('<dataset>_iter_<N>'); env.build_dataset(); print('rows:', len(env.dataset))" | grep "rows: $EXPECTED"
```

Mismatch → repeat the cleanup. Don't skip the verify.

### 3d. rl.toml

Write `<RUN_DIR>/iter_<N>/rl.toml`. Three mandates: **resume from iter_0** (`[ckpt] resume_step = <F>`, integer), **train env = local package**, **eval env = hub**. Pinned: `max_steps = F + 100`, `batch_size = <BATCH_SIZE>`, `rollouts_per_example = 16`, `[ckpt] interval = 100`.

**Pre-stage iter_0's four checkpoint trees** into iter_N's `prime_out/` (prime-rl looks at iter_N's output dir, not iter_0's; missing any → FileNotFoundError):

```bash
F=<iter_0 final step>
SRC=<RUN_DIR>/iter_0/prime_out
DST=<RUN_DIR>/iter_<N>/prime_out
mkdir -p "$DST/checkpoints" "$DST/weights" "$DST/run_default/checkpoints" "$DST/run_default/broadcasts"
cp -r "$SRC/checkpoints/step_$F"             "$DST/checkpoints/step_$F"
cp -r "$SRC/weights/step_$F"                 "$DST/weights/step_$F"
cp -r "$SRC/run_default/checkpoints/step_$F" "$DST/run_default/checkpoints/step_$F"
cp -r "$SRC/run_default/broadcasts/step_$F"  "$DST/run_default/broadcasts/step_$F"
```

Template (`<MAX>` = `F+100`):
```toml
max_steps = <MAX>
seq_len = 2048
[wandb]
project = "synthetic-self-improve-rl-<dataset>"
name = "iter_<N>"
[model]
name = "<MODEL>"
[ckpt]
interval = 100
resume_step = <F>
[orchestrator]
batch_size = <BATCH_SIZE>
rollouts_per_example = 16
[orchestrator.train.sampling]
max_completion_tokens = 1024
[[orchestrator.train.env]]
id = "<dataset>_iter_<N>"
[orchestrator.eval]
interval = <MAX>
[orchestrator.eval.sampling]
max_completion_tokens = 1024
[[orchestrator.eval.env]]
id = "<hub-id>"
num_examples = 200
rollouts_per_example = 1
[trainer]
[inference]
```

### 3e. Train + parse

Launch foreground, tee log:
```bash
uv run rl @ <RUN_DIR>/iter_<N>/rl.toml \
    --output-dir <RUN_DIR>/iter_<N>/prime_out \
    2>&1 | tee <RUN_DIR>/iter_<N>/train.log
```

Set Bash `timeout=600000` (10 min — the max). Iters take 60-90 min, so the call times out — expected. **Never re-launch on Bash timeout** (trainer is detached; a re-launch corrupts checkpoints). On timeout, poll:

```bash
RUN=<RUN_DIR>/iter_<N>
EVAL=$RUN/prime_out/run_default/rollouts/step_<MAX>/eval_rollouts.jsonl
START=$(date +%s); TIMEOUT=$((2 * 60 * 60))
while true; do
  if [ -f "$EVAL" ] && [ "$(wc -l < "$EVAL")" -ge <NUM_EVAL_EXAMPLES> ]; then
    echo "DONE: eval present"; break
  fi
  if ! pgrep -f "uv run rl.*<RUN_DIR>/iter_<N>/rl.toml" > /dev/null; then
    echo "DONE: trainer exited"; break
  fi
  [ $(( $(date +%s) - START )) -ge "$TIMEOUT" ] && { echo "TIMEOUT"; break; }
  sleep 60
done
```

**Forbidden: `tail -f <log> | grep <regex>`.** No exit condition; prime-rl's completion phrase is "RL training finished!" which doesn't match common regex. A real run wedged 8h on this. Always use file/process signals.

Parse eval (numeric-only, same aggregator as Phase 2). Write `<RUN_DIR>/iter_<N>/eval_summary.json`; append to `metrics.json.iters`.

**Edit scratchpad section 5:** eval_acc, train trajectory by 20-step buckets, Δ vs iter_<N-1>, verdict (`improved` Δ≥+0.01 / `flat` |Δ|<0.01 / `regressed` Δ≤-0.01 / `collapsed` if drop >50% of iter_0), what worked/didn't/carryover.

### 3f. Continue + /compact

Re-check budget. If neither fires, increment `N` and loop back to 3a. Teacher judgment is NOT a stopping criterion.

**Before iter_<N+1>'s 3a, invoke `/compact`.** Load-bearing state is on disk (scratchpad, metrics, weakness reports, generators); without `/compact` context fills by iter_2-3 and forces premature termination. If `/compact` fails, log to `run.json.compact_warnings[]` and continue — do NOT stop.

---

## Phase 4 — comparison runs (post-budget)

Runs on its own time (~5h for 2× 100-step trains + full-split evals). `--budget` never reserves time for Phase 4.

**Eval size:** full hub test split, discovered via `prime env info <hub-id>` (look for the eval dataset row count). Pinned hyperparams same as iters.

**Pick winner:** highest `eval_acc` among iters ≥1 in `metrics.json` = `BEST_ITER`. Write `<RUN_DIR>/best_iter.json` with `BEST_DATASET`, `BEST_ENV_DIR`, `BEST_RL_TOML`, eval_acc.

Both Run A and Run B follow the same flow: copy BEST artifacts into a new package name, cleanup-then-install (same as 3c), write rl.toml, launch+poll+parse (same as 3e), append to `metrics.json` with `run` field. Failures → log to `run.json.phase4_errors` and proceed.

### 4a. Run A — best replay from iter_0

Tests whether the best dataset reproduces from the same anchor.

1. `mkdir <RUN_DIR>/run_a_best_from_iter0/`.
2. Copy `BEST_DATASET` + `BEST_ENV_DIR` to `<RUN_DIR>/run_a_best_from_iter0/<dataset>_run_a/`. Rename `pyproject.toml` `name`, the `.py`, and `[tool.hatch.build].include`.
3. Install (cleanup pattern); verify row count.
4. Pre-stage iter_0's four checkpoint trees into `run_a_best_from_iter0/prime_out/`.
5. `rl.toml`: `[ckpt] resume_step = <F>`, `interval = 100`, `max_steps = F+100`, `[[orchestrator.train.env]] id = "<dataset>_run_a"`, `[[orchestrator.eval.env]] num_examples = <full_split>`.

### 4b. Run B — real + best from base

Tests whether mixing real + best from scratch beats either alone. Starts from base `<MODEL>`, **no `resume_step`**, `max_steps = 100`, `[ckpt] interval = 100`.

1. `mkdir <RUN_DIR>/run_b_combined_from_base/`. Install BEST under `<dataset>_run_b`.
2. Mix real + generated via two train env blocks. Copy the **exact `[[orchestrator.train.env]]` entry from `<PRIME_RL_DIR>/configs/<dataset>/rl.toml`** (the canonical config used by iter_0 in Phase 2B — that block already specifies the right `id`/`name`/`args` for the real dataset). Then append the generated block:
   ```toml
   # First block: copied verbatim from configs/<dataset>/rl.toml's train env
   [[orchestrator.train.env]]
   id = "<copy from canonical config>"
   name = "<copy>"
   args = { ... }     # copy verbatim
   # Second block: the generated env
   [[orchestrator.train.env]]
   id = "<dataset>_run_b"
   ```
   If multi-env isn't supported by the user's prime-rl version, concat the real split (load it the same way the canonical env does — read its source via `prime env info <real-env-id>`) + generated into one JSONL and wrap as a single env.

---

## Phase 5 — finalize

1. Update `run.json`: `status` ∈ {`completed`, `budget_exhausted`, `max_iters_reached`, `aborted`}; add `end_ts`, `total_duration_s`.
2. Append `## Final summary — <UTC ts>` to scratchpad: eval_acc table, winning iter + which buckets drove it, what worked/didn't, open questions.
3. Print summary table (one row per arm; values are example shapes, not real numbers):
   ```
   run                       rows           eval_acc   ckpt
   iter_0 (real)             <real_count>   <X.XXX>    <RUN_DIR>/iter_0/.../step_100
   iter_1                    <count>        <X.XXX>    <RUN_DIR>/iter_1/.../step_<F+100>
   iter_N                    <count>        <X.XXX>    ← BEST_ITER (mark with arrow)
   run_a (best @iter0)       <count>        <X.XXX>    ...
   run_b (real+best @base)   <real+count>   <X.XXX>    ...
   ```
4. Highlight the single best eval_acc row as the recommended model.

---

## Hard rules

- **Never edit `<VERIFIERS_DIR>` or `<PRIME_RL_DIR>`.** Outputs under `<RUN_DIR>` only.
- **`uv run`, never raw `python`** for repo commands.
- **Reuse verifiers building blocks.** Read the source under `<VERIFIERS_DIR>/` to confirm signatures before using.
- **Validate `eval_summary.json` after every iter.** Parse failure → abort.
- **Every row from `gen_dataset.py`**, never hand-typed.
- **`/compact` after every iter**, before iter_<N+1>'s 3a. Fail → log + continue.
- **Never `tail -f | grep`.** Use the polling loop (file/process signals, 2h cap).
- **Cleanup-then-install** at every `prime env install`. Delete `dataset.jsonl` + prior `.py` + `*-dist-info` from `<SITE_PACKAGES>/`; install; verify row count.
- **Pre-stage iter_0's four checkpoint trees** into every resuming run's `prime_out/`.
- **iter_0 must save a checkpoint** via `[ckpt] interval`. Otherwise Phase 3 has nothing to resume from.
- **Eval rollouts at `<output_dir>/run_default/rollouts/step_<N>/eval_rollouts.jsonl`** (note `run_default/`). Trainer dirs live under `<output_dir>/` directly.
- **Resume from iter_0** — not iter_<N-1>, not base.
- **Eval always on the real hub env.** Iters: 200 examples. Phase 4: full split.
- **`scratchpad.md` mandatory.** Init Phase 0; iter_0 appended in Phase 2; each iter writes 3a.5 + edits §5 at 3e; Phase 5 appends final summary. Cite `(domain, sub_domain)` names + numbers; never "tried different things".
- **One TaskCreate per phase**, completed eagerly.

---

## Reference files

Templates and rule sources in the upstream repos:

- **verifiers** — https://github.com/PrimeIntellect-ai/verifiers
  - `environments/<any>/` — example env loaders to model the generated `load_environment` on. Pick whichever env is closest in shape to the user's `<hub-id>`.
  - `skills/create-environments/SKILL.md` — env quality gates.
- **prime-rl** — https://github.com/PrimeIntellect-ai/prime-rl
  - `configs/<dataset>/rl.toml` — canonical iter_0 config; use via `@`, don't modify.
  - `skills/config/SKILL.md` — TOML/CLI rules, `[ckpt]` / resume semantics.
  - `skills/entrypoints/SKILL.md` — `uv run rl` invocation form.
  - `skills/monitor-run/SKILL.md` — long-running training jobs.
  - `AGENTS.md` — `uv run` discipline.
