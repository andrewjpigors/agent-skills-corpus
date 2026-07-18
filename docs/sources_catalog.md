# Agent Skills — Marketplaces, Aggregators & Awesome-Lists Catalog

Snapshot date: **2026-07-18**

This catalog records the skills marketplaces / registries / aggregators and `awesome-*`
lists used to discover GitHub repositories that host Agent Skills (`SKILL.md` files with
YAML frontmatter). The extracted GitHub candidates are written to
`marketplace_github_candidates.jsonl` in this directory.

> **IMPORTANT — counters are page-specific signals, not a global unique total.**
> Each "indexed skills" number below is what that site/list advertised *on its own page*
> on the snapshot date. These counts overlap heavily (most aggregators re-index the same
> underlying GitHub repos, especially `anthropics/skills`, `obra/superpowers`, and vendor
> monorepos) and use different definitions of "skill" (a `SKILL.md` file vs. a repo vs. a
> plugin). They must **not** be summed into a global unique total. The deduplicated,
> owner/name-correct repo set we actually extracted is **~2,032 distinct GitHub repos**
> (2,050 records incl. per-path rows), which is the meaningful number for the enrichment
> pipeline.

Total distinct GitHub repos extracted: **2,032** (records: **2,050**).

---

## First-party (Anthropic / OpenAI / vendor) sources

### anthropics/skills — official Anthropic reference repo
- URL: https://github.com/anthropics/skills
- What: Anthropic's official public repository for Agent Skills; defines the `SKILL.md`
  format, the Agent Skills spec (`/spec`), and a template (`/template`).
- Indexed skills: **17 first-party skills** under `skills/*` + 1 template `SKILL.md`
  (verified 2026-07-18 via git tree). Exact `SKILL.md` paths were extracted and emitted
  as individual candidate rows (18 path rows + 1 repo-level row = 19 records).
- Exposes repos: it *is* the repo. Paths recorded directly (e.g. `skills/pdf/SKILL.md`).
- Provenance tag: `official:anthropic`
- Note: `agentskills.io` and `skills.sh/anthropics/skills` are referenced from its README
  as the "Agent Skills standard" and a distribution mirror.

### anthropics/claude-plugins-official — official plugin marketplace
- URL: https://github.com/anthropics/claude-plugins-official
- What: The official Claude Code plugin marketplace repo (added via
  `/plugin marketplace add anthropics/claude-plugins-official`).
- Indexed skills: **30 `SKILL.md` files** (verified 2026-07-18 via git tree).
- Provenance: first-party Anthropic. Tag: `awesome:GetBindu/...` (first surfaced there)
  and cross-referenced by claudeskills.info.

### Verified vendor first-party skill monorepos
Confirmed 2026-07-18 to contain `SKILL.md` files via GitHub git-tree API. Tag
`official:vendor-monorepo` / surfaced via VoltAgent list. Counts = `SKILL.md` files:
- `microsoft/skills` — **190** SKILL.md
- `dotnet/skills` — **106** SKILL.md
- `huggingface/skills` — **26** SKILL.md
- `expo/skills` — **22** SKILL.md
- `vercel-labs/skills` — **1** SKILL.md (monorepo root skill)
- `cloudflare/agents` — exists (skills/agent assets)
- Other vendor orgs (OpenAI/Codex `openai/*`, `stripe/*`, `getsentry/*`, `hashicorp/*`,
  `googleworkspace/*`, `WordPress/*`, `figma/*`, `neondatabase/*`, `clickhouse/*`,
  `sanity-io/*`, `firecrawl/*`, `netlify/*`, `google-gemini/*`, `fal-ai-community/*`,
  `tinybirdco/*`, `greensock/*`, `binance/*`) were listed **per-skill** by VoltAgent's
  list. Their exact monorepo owner/name was **not** independently verified here, so
  fabricated repo names were deliberately **excluded** to keep owner/name correct. The
  pipeline should resolve these vendor orgs directly if desired.

---

## Community aggregators / marketplaces (with GitHub source attribution)

### Chat2AnyLLM/awesome-claude-skills  ← MOST PRODUCTIVE
- URL: https://github.com/Chat2AnyLLM/awesome-claude-skills
- Backing data: `config.yaml` sources a master registry
  `https://raw.githubusercontent.com/Chat2AnyLLM/awesome-repo-configs/main/skill_repos.json`.
- What: An auto-generated awesome-list. A scraper walks a machine-readable registry of
  source repos and counts discoverable `SKILL.md` files per repo via the GitHub API.
- Indexed skills: README advertises **95,278 discoverable skills across 1,719 enabled
  source repositories** (2026-07-18).
- Exposes repos: `skill_repos.json` is a JSON dict keyed by **`owner/name`** with
  `{owner,name,branch,skillsPath,enabled}` per entry — an exact, machine-readable list of
  1,719 host repos. **All 1,719 extracted** into the candidate JSONL (path left empty;
  pipeline discovers `SKILL.md` paths via each repo's `skillsPath`).
- Provenance: community. Tag: `awesome:Chat2AnyLLM/awesome-claude-skills (via awesome-repo-configs/skill_repos.json)`

### claudeskills.info — curated directory with JSON API
- URL: https://claudeskills.info/skills/  · API: https://claudeskills.info/api/v1/search
- What: Editor-curated open-source skills directory. Each entry carries source provenance
  (`source.repo`, `source.url`).
- Indexed skills: homepage advertises **381 editor-selected** skills (34 official / 347
  community); the search API reports **total: 3,830** entries (2026-07-18).
- Exposes repos: REST API returns `source.repo` (owner/name) per skill. Paginated first
  ~1,600 rows → **72 distinct source repos** extracted (e.g. `obra/superpowers`,
  `antfu/skills`, `dotnet/skills`, `garrytan/gstack`).
- Provenance: community. Tag: `marketplace:claudeskills.info`

### netresearch/claude-code-marketplace (agentskills.io)
- URL: https://github.com/netresearch/claude-code-marketplace
- What: Vendor-curated Agent Skills marketplace (Netresearch), open-standard
  (agentskills.io), portable across Claude Code / Cursor / Copilot / Codex / Gemini CLI.
- Indexed skills: **40 curated Agent Skills** (README, 2026-07-18); catalog in
  `marketplace.json`.
- Exposes repos: README lists **43** `netresearch/*` skill repos (owner/name). All extracted.
- Provenance: community/vendor. Tag: `marketplace:netresearch/claude-code-marketplace (agentskills.io)`

### skills.sh — "npm for skills" CLI marketplace
- URL: https://skills.sh/
- What: Vercel-backed package-manager-style skills marketplace (`npx skills add`),
  cross-tool (Claude Code / Codex / Cursor / OpenClaw). Community-submitted, no formal review.
- Indexed skills: leaderboard shows **928,842** all-time skills (2026-07-18); the main
  project repo is `vercel-labs/skills`. Sample source repos surfaced: `anthropics/skills`,
  `mattpocock/skills`, `vercel-labs/agent-skills`, `supabase/*`.
- Exposes repos: per-skill pages carry an owner/repo path; `/docs/api` for programmatic
  access. Not bulk-extracted here (large, overlaps master list); `vercel-labs/skills`
  captured and verified.
- Provenance: community. Referenced from anthropics/skills README as a distribution mirror.

### SkillsMP (skillsmp.com)
- URL: https://skillsmp.com/
- What: Agent-skills marketplace/directory for Claude Code / Codex CLI / ChatGPT with
  keyword search and GitHub-source inspection.
- Indexed skills: advertises **2,000,000+** skills (2026-07-18). Free REST API + developer
  portal. No repo URLs on the landing page; API not bulk-harvested (count is a broad,
  non-unique signal that overlaps GitHub at large).
- Provenance: community.

### agentskill.sh
- URL: https://agentskill.sh/
- What: AI Agent Skills directory/marketplace (Claude, Cursor, Copilot, +more).
- Indexed skills: advertises **274,000+** skills (2026-07-18). Exposes creators via GitHub
  avatars/profiles; no direct repo URLs on the landing page.
- Provenance: community.

### Other marketplaces observed (not bulk-harvested; overlap the master list)
- LobeHub — https://lobehub.com/skills — advertises **169K+** skills (2026-07-18).
- MCP Market — https://mcpmarket.com/tools/skills — agent-skills directory (Claude/ChatGPT/Codex).
- claudemarketplaces.com — community directory of Claude Code skills/plugins/MCP servers.
- Agensi — https://www.agensi.io/ — curated skills + the "7 marketplaces" comparison used
  as a discovery lead.
These advertise large per-site counters that are **not** unique and were not summed.

---

## Community awesome-lists (README-extracted GitHub repos)

| List (repo) | URL | What / count signal (2026-07-18) | Provenance |
|---|---|---|---|
| BehiSecc/awesome-claude-skills | https://github.com/BehiSecc/awesome-claude-skills | Curated list; **~127 GitHub repo links** in README, 97 distinct extracted after dedup | community |
| GetBindu/awesome-claude-code-and-skills | https://github.com/GetBindu/awesome-claude-code-and-skills | Broad Claude Code + skills collection; ~99 repo links, 66 distinct extracted | community |
| ComposioHQ/awesome-claude-skills | https://github.com/ComposioHQ/awesome-claude-skills | Advertises **1000+** production skills/plugins; ~48 distinct repo links extracted | community (Composio) |
| VoltAgent/awesome-agent-skills | https://github.com/VoltAgent/awesome-agent-skills | Vendor-organized official + community skills (Anthropic/OpenAI/Google/HF/Cloudflare/etc.); ~288 per-skill rows, 31 distinct community/vendor repos extracted | community (VoltAgent) |
| travisvn/awesome-claude-skills | https://github.com/travisvn/awesome-claude-skills | Curated Claude Code skills list; 5 repo links (mostly meta-lists + superpowers/anthropics) | community |
| karanb192/awesome-claude-skills | https://github.com/karanb192/awesome-claude-skills | "50+ verified" skills; points mainly to `obra/superpowers`, `anthropics/skills`, and other awesome-lists | community |
| mingrath/awesome-claude-skills | https://github.com/mingrath/awesome-claude-skills | Claude Code skills list; skills documented as `anthropics/skills` subpaths; 2 distinct 3rd-party repos | community |
| heilcheng/awesome-agent-skills | https://github.com/heilcheng/awesome-agent-skills | Overlaps VoltAgent vendor set (Anthropic/OpenAI/Gemini/HF/vendor orgs) | community |

### Notable meta / related lists seen (linked from the above, not separately harvested)
`hesreallyhim/awesome-claude-code`, `alvinunreal/awesome-claude`,
`libukai/awesome-agent-skills`, `VoltAgent/awesome-openclaw-skills`,
`VoltAgent/awesome-claude-code-subagents`, `vijaythecoder/awesome-claude-agents`,
`punkpeye/awesome-mcp-servers`, `langgptai/awesome-claude-prompts`,
`rohitg00/awesome-claude-code-toolkit`. Their notable member repos are captured where they
appeared in the harvested READMEs.

---

## Extraction method notes
- The bulk of coverage comes from **one machine-readable registry** (`skill_repos.json`,
  1,719 repos) plus the **claudeskills.info JSON API** (owner/name provenance) — the two
  sources that expose clean owner/name attribution.
- Awesome-list READMEs contributed the vendor-org and long-tail community repos.
- GitHub API use was limited to READ-ONLY `repos/{owner}/{repo}` and git-tree calls to
  (a) confirm vendor monorepos actually contain `SKILL.md`, and (b) enumerate the exact
  `anthropics/skills` paths. **No** `gh search code` / `/search/code` was used.
- Deliberately excluded fabricated vendor monorepo names where owner/name could not be
  verified, to keep the candidate set owner/name-correct.
- Records are deduplicated on `(repo, path)`; one line per pair. Where the exact `SKILL.md`
  path is unknown, `path` is empty and the pipeline discovers it from the repo tree.
