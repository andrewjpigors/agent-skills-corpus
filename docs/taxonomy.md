# Classification taxonomy

Every skill in the corpus is labelled on two independent axes. Both are **deterministic and
reproducible** from `scripts/09_classify.py` + `data/taxonomy.json`; re-running the classifier on
`data/metadata.jsonl` reproduces `data/classification.jsonl` exactly.

## Axis 1 — functional category

**Method.** A keyword-scoring classifier. For each category we count keyword/phrase hits across the
frontmatter `name` (weight ×3), `description` (×2), `path` (×2) and the first 600 chars of the body
(×1). The category with the highest score wins; ties break by the (specific → general) order in
`taxonomy.json`; a skill with zero hits is labelled `other`. Single ambiguous words that appear in
almost every Agent Skill (notably `agent`, and — after audit — `claude`/`mcp`/bare `review`) are
deliberately **not** keywords.

**The 20 categories** (share of 55,698):

| category | share | what it covers |
|---|---:|---|
| writing-docs-content | 11.3% | documentation, technical writing, translation, blogging, de-AI-slop, papers |
| devops-cloud-infra | 8.4% | CI/CD, Docker, Kubernetes, Terraform, AWS/Azure/GCP, monitoring |
| devtools-automation | 7.8% | CLI tooling, git workflows, codegen, scaffolding, linters/formatters |
| backend-api | 7.3% | REST/GraphQL APIs, microservices, servers, webhooks, OAuth |
| testing-qa | 6.3% | unit/integration/e2e tests, TDD/BDD, coverage, Playwright/pytest |
| security | 5.7% | pentest, vuln/CVE, threat modelling, crypto, detection rules, hardening |
| architecture-planning | 5.4% | system design, DDD, specs/PRDs, requirements, roadmaps |
| web-frontend | 5.3% | React/Vue/Svelte, CSS/Tailwind, UI components, responsive/WCAG |
| agent-workflow-meta | 4.9% | multi-agent orchestration, plan/implement/review loops, skill authoring |
| code-review-quality | 4.8% | code review, refactoring, static analysis, technical debt, debugging |
| ai-ml-llm | 4.4% | LLM/ML engineering: prompts, RAG, embeddings, fine-tuning, PyTorch, eval |
| productivity-business | 3.9% | marketing, sales/CRM, PM, finance, e-commerce, email |
| database | 3.1% | schema design, SQL, migrations, Postgres/Mongo/Redis, ORM |
| data-analytics | 2.2% | data analysis, ETL, dashboards, BI, visualization |
| design-ux-creative | 2.2% | UX/UI design, Figma, branding, image/video generation, game design |
| crypto-defi-finance | 1.0% | crypto/DeFi trading bots, on-chain, stock/fundamental analysis |
| mobile | 0.9% | iOS/Android, SwiftUI, Kotlin, Flutter, React Native |
| legal-regulatory | 0.9% | legal research, contracts, trademark, GDPR/compliance, KYC/AML |
| domain-science-other | 0.8% | bioinformatics, chemistry, physics, medical, geospatial, robotics |
| expert-persona-advisor | 0.4% | persona/perspective skills that adopt a thinker's mental models |
| **other** | **12.9%** | genuinely idiosyncratic or too-generic to place |

## Axis 2 — agent platform

Derived from the `SKILL.md` path namespace (first match wins):

| platform | marker | share |
|---|---|---:|
| generic | `skills/`, `.agents/skills`, other | 85.0% |
| claude | `.claude/skills`, `claude-skills/` | 10.9% |
| cyberstrike | `.cyberstrike` (a security toolkit) | 2.2% |
| codex | `.codex/skills` | 0.6% |
| cursor | `.cursor` | 0.6% |
| opencode | `.opencode` | 0.6% |
| gemini | `.gemini` | 0.2% |
| windsurf / aider / amazon-q / continue | resp. dot-dirs | <0.1% |

## How the taxonomy was refined

The first taxonomy had a serious precision leak: `ai-ml-llm` was a false-positive magnet (16.7%
precision) because broad terms like `agent`/`claude`/`mcp` match almost every Agent Skill. We ran an
automated review — parallel agents (1) *mined the `other` bucket* to surface recurring missed
clusters and (2) *audited per-category precision* on stratified samples — then synthesised the
result into: tightening `ai-ml-llm` to real ML/LLM engineering, adding `agent-workflow-meta`,
`crypto-defi-finance`, `legal-regulatory` and `expert-persona-advisor`, and applying high-precision
keyword additions while keeping moderate-breadth terms for recall.

## Limitations

Keyword classification is **approximate**: spot audits put per-category precision around 65–80%, and
~13% of skills remain `other`. Treat `category` as a coarse filter. Because every record ships with
`content_sha256` and (for clear-license skills) full text, you can re-classify with an embedding or
LLM method of your own and join back on `id` / `content_sha256`.
