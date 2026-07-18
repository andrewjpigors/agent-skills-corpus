#!/usr/bin/env python3
"""
09_classify.py — reproducible two-axis classification of every skill.

Axis 1 (agent_platform): derived from the SKILL.md path namespace (deterministic).
Axis 2 (category): a transparent keyword-scoring taxonomy over
  frontmatter name (weight 3) + description (weight 2) + path (weight 2) + body head (weight 1).
Each category is the arg-max of keyword hits; ties broken by TAXONOMY order; 0 hits -> "other".

Outputs:
  data/classification.jsonl   {id, repo, path, category, category_score, agent_platform, top3}
  data/taxonomy.json          the exact rules (categories + keywords + platform markers)
Prints the category + platform distribution.

Rules live in TAXONOMY below so they are auditable and reproducible. Edit + re-run to refine.
"""
import os, sys, re, json
from collections import Counter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C

# ---- agent platform markers (path-namespace, ordered; first match wins) ----
PLATFORM_MARKERS = [
    ("claude",     [r"\.claude/", r"(^|/)claude[-_]?skills?/"]),
    ("codex",      [r"\.codex/", r"(^|/)codex[-_]?skills?/"]),
    ("gemini",     [r"\.gemini/?"]),
    ("cursor",     [r"\.cursor/?"]),
    ("amazon-q",   [r"\.aws/amazonq", r"amazonq"]),
    ("opencode",   [r"\.opencode/?"]),
    ("windsurf",   [r"\.windsurf/?"]),
    ("aider",      [r"\.aider/?"]),
    ("continue",   [r"\.continue/?"]),
    ("cyberstrike",[r"\.cyberstrike/?"]),
]

# ---- functional taxonomy v3 (ordered = tie-break priority; specific -> general) ----
# Refined via a mine-the-"other" + per-category precision-audit workflow: ai-ml-llm was
# tightened to real ML/LLM engineering (broad 'agent'/'claude'/'mcp' removed — they matched
# generic Agent Skills and gave 16.7% precision), agent-workflow-meta / crypto-defi-finance /
# legal-regulatory / expert-persona-advisor were added to absorb the largest "other" clusters,
# and moderate-breadth keywords were kept on the well-performing categories to hold recall.
# 'agent' alone is deliberately NOT a keyword anywhere (every file here is an "Agent Skill").
TAXONOMY = {
    "security": ["security","vulnerab","cve","cwe","cis benchmark","pentest","penetration test",
        "exploit","owasp","threat model","threat hunting","red team","blue team","malware","encrypt",
        "cryptograph","authentication","authorization","secrets vault","credential management","firewall",
        "hardening","xss","sql injection","ssrf","csrf","reverse engineer","forensic","incident response",
        "security audit","cyberstrike","zero-day","infosec","sigma rule","detection rule","mitre att&ck",
        "lateral movement","siem","sysmon","smart contract audit"],
    "agent-workflow-meta": ["multi-agent","multi agent","sub-agent","subagent","orchestrat","agent team",
        "delegate to","intelligent routing","task routing","hierarchical coordinator","coordinator agent",
        "execute the plan","implement the plan","implement plan","execute phase","plan review","plan-ceo-review",
        "review loop","iterate on pr","worktree","scope lock","phase gate","one ticket at a time","skill creator",
        "create skill","create a new skill","skillify","publish skill","find skills","meta-skill","codify workflow",
        "session handoff","handoff baton","pickup","closing session","goal drift","checkpoint validation",
        "codebase onboarding","project init","agent succession","dispatch","babysit","wrapup"],
    "ai-ml-llm": ["large language model"," llm ","llm-","prompt engineer","prompt template","system prompt",
        "model context protocol","rag pipeline","retrieval-augmented","retrieval augmented","embedding","fine-tun",
        "rlhf","training loop","learning rate","overfitting","vllm","sglang","megatron","pytorch","tensorflow",
        "fsdp","model checkpoint","gpu training","tokenizer","eval harness","evaluating llms","mmlu","gsm8k",
        "transformer model","inference optimization","llm judge","langchain","llamaindex","vector database",
        "vector similarity","faiss","hugging face","music generation","audiocraft","neural network","diffusion model",
        "prompt","machine learning","language model","ml model"],
    "testing-qa": ["unit test","integration test","end-to-end test","e2e test","playwright","smoke test",
        "regression test","test coverage","test suite","test plan","test-first","test-driven","tdd","bdd",
        "differential testing","metamorphic test","oracle test","api testing","pytest","jest","cypress","vitest",
        "quality assurance","fuzz test","test automation","debugpy","test","testing","qa"],
    "crypto-defi-finance": ["cryptocurrency","crypto ","defi","trading bot","backtest","exchange adapter",
        "dapp","polymarket","aave","uniswap","hyperliquid","pancakeswap","on-chain","blockchain","smart contract",
        "web3","nft","stock analysis","technical analysis","fundamental analysis","piotroski","financial data api",
        "tushare","portfolio optim","hedge","options trading","candlestick","market maker"],
    "legal-regulatory": ["criminal law","advogado","trademark","markenrecherche","dpma","euipo","case law",
        "类案","contract drafting","contract review","gdpr","eu ai act","regulatory compliance","litigation",
        "kyc","aml","beneficial ownership","underwriting","insolven","legal research","patent filing","jurisdiction",
        "anonymization","k-anonymity","retention policy","compliance framework"],
    "database": ["database schema","schema design","query optimization","sql migration","postgres","postgresql",
        "mysql","mongodb","sqlite","redis","point-in-time recovery","partitioning","normalization","er diagram",
        "table schema"," orm ","nosql","data warehouse","supabase","prisma","clickhouse","dynamodb","oltp","olap",
        "replication","database","sql query"," sql ","schema","db migration"],
    "devops-cloud-infra": ["devops","ci/cd","cicd","continuous integration","continuous deployment","docker",
        "kubernetes","k8s","terraform","ansible","helm chart","ci/cd pipeline","infrastructure-as-code",
        "infrastructure as code","provision","serverless","observability","prometheus","grafana","opentelemetry",
        "nginx","cloudformation"," sre ","autoscaling","load balancer","incident on-call","amazon web services",
        "azure ","gcp ","google cloud","ec2","s3 bucket","gpu cloud","deploy","docker","kubernetes","pipeline",
        "infrastructure","monitoring","cloud"],
    "mobile": ["ios app","android app","mobile app","swiftui","jetpack compose","react native","expo ","flutter",
        "kotlin","xcode","android studio","app store","material design","push notification","mobile development"],
    "web-frontend": ["frontend","front-end","react component","vue","angular","svelte","tailwind","next.js","nextjs",
        "ui component","web app","landing page","responsive layout","responsive design","dom rendering","wcag",
        "framer motion","storybook","shopify app","image to code","screenshot to code"," css ","html/css",
        "react","frontend","front-end","web app","web ui","browser"],
    "backend-api": ["backend","back-end","rest api","restful","graphql","api endpoint","microservice","webhook",
        "grpc","fastapi","express.js","django","flask","rails","spring boot","http server","openapi","swagger",
        "oauth","control-plane api","third-party api","api","backend","rest","endpoint","server-side"],
    "data-analytics": ["data analysis","data analytics","dataset","etl pipeline","data pipeline","pandas",
        "bi dashboard","business intelligence","statistical","data visualization","tableau","power bi","spark",
        "data cleaning","exploratory data","csv analysis","lakehouse","semantic layer","pivot table","metrics reporting",
        "analytics","dashboard","dataset","data science","reporting"],
    "code-review-quality": ["code review","reviewing code","pull request review","pr review","lint","refactor",
        "code smell","clean code","static analysis","code quality","maintainab","technical debt","coding standard",
        "style guide","code audit","ast-grep","structural refactor","root cause investigation","systematic debugging",
        "code review","lint","refactor","best practices","debugging"],
    "design-ux-creative": ["ux design","ui design","user experience","figma","wireframe","design system",
        "graphic design","illustration","branding","typography","image generation","video generation","video editing",
        "3d model","3d asset","game design","logo design","icon design","color palette","visual design","storyboard",
        "motion graphics","generative art","app store screenshot"," aso "],
    "writing-docs-content": ["technical writing","documentation","readme","blog post","copywriting","content writing",
        "markdown doc","translation","translate ","localization","summariz","proofread","seo content","changelog",
        "release notes","tutorial","user guide","newsletter","humanize","humanizer","ai slop","de-slop",
        "remove ai-generated","paper writing","academic paper","camera-ready","novel","fiction writing","resume","cv writing",
        "documentation","docs","writing","content","readme","markdown","translate"],
    "architecture-planning": ["software architecture","system design","domain-driven design","bounded context",
        "event storming","technical design doc","architecture.md","product requirements"," prd ","feature specification",
        "requirements gathering","discovery interview","design decision record","roadmap","proposal","adr ","scalability",
        "high-level design","architecture","specification","planning","design doc","requirements"],
    "devtools-automation": ["workflow automation","cli tool","command-line tool","github action","gitlab ci",
        "build system","makefile","task runner","code generation","codegen","scaffold","boilerplate","git hook",
        "pre-commit","monorepo","linter","formatter","log analysis","post-mortem","jujutsu","language server"," lsp ",
        "obsidian","shell script","dev tooling","automation","cli","git ","tooling","code generation","developer tool"],
    "productivity-business": ["product management","product-market fit","go-to-market","lead generation","marketing",
        "email marketing","campaign","sales pipeline","crm","accounting","project management","meeting notes",
        "email draft","inbox organization","email triage","invoic","customer discovery","market research","e-commerce",
        "seo strategy","social media","customer support","business","product ","sales","seo","e-commerce"],
    "expert-persona-advisor": ["perspective","视角","thinking framework","mental model","persona of","in the style of",
        "channel the","embody","advisor persona","founder mode","day 1 mindset","coaching persona","mentor persona",
        "specialist persona","methodology of"],
    "domain-science-other": ["bioinformatic","genomic","chip-seq","gene expression","medicinal chemistry","wet-lab",
        "flow cytometry","single-cell","gwas","sequence alignment","phylogenetic","copy number variation",
        "variant interpretation","fluid-structure interaction","geospatial","chemistry","physics simulation",
        "astronomy","medical imaging","clinical","robotics","iot "],
}
NAME_W, DESC_W, PATH_W, BODY_W = 3, 2, 2, 1

def platform_of(path):
    p = path.lower()
    for name, pats in PLATFORM_MARKERS:
        for pat in pats:
            if re.search(pat, p):
                return name
    return "generic"

def _count(keywords, text):
    s = 0
    for kw in keywords:
        if " " in kw or not kw.strip().isalnum():
            s += text.count(kw)                      # phrase / has punctuation -> substring
        else:
            s += len(re.findall(r"\b" + re.escape(kw) + r"\b", text))
    return s

def classify(name, desc, path, body):
    name_l = " " + (name or "").lower().replace("-", " ") + " "
    desc_l = " " + (desc or "").lower() + " "
    path_l = " " + (path or "").lower().replace("/", " ").replace("-", " ") + " "
    body_l = " " + (body or "")[:600].lower() + " "
    best, best_score, scores = "other", 0, {}
    for cat, kws in TAXONOMY.items():
        sc = (NAME_W * _count(kws, name_l) + DESC_W * _count(kws, desc_l)
              + PATH_W * _count(kws, path_l) + BODY_W * _count(kws, body_l))
        scores[cat] = sc
        if sc > best_score:
            best, best_score = cat, sc
    top3 = sorted(scores.items(), key=lambda x: -x[1])[:3]
    return best, best_score, [f"{c}:{s}" for c, s in top3 if s > 0]

def main():
    src = os.path.join(C.DATA, "metadata.jsonl")
    out = os.path.join(C.DATA, "classification.jsonl")
    catc, platc = Counter(), Counter()
    n = 0
    if os.path.exists(out): os.remove(out)
    buf = []
    for ln in open(src, encoding="utf-8", errors="replace"):
        o = json.loads(ln); n += 1
        cat, score, top3 = classify(o.get("frontmatter_name"), o.get("frontmatter_description"),
                                    o.get("path"), o.get("skill_md_text"))
        plat = platform_of(o.get("path", ""))
        catc[cat] += 1; platc[plat] += 1
        buf.append({"id": o.get("id"), "repo": o.get("repo"), "path": o.get("path"),
                    "category": cat, "category_score": score, "agent_platform": plat, "top3": top3})
        if len(buf) >= 5000:
            with open(out, "a", encoding="utf-8", errors="replace") as f:
                for b in buf: f.write(json.dumps(b, ensure_ascii=False) + "\n")
            buf = []
    if buf:
        with open(out, "a", encoding="utf-8", errors="replace") as f:
            for b in buf: f.write(json.dumps(b, ensure_ascii=False) + "\n")
    json.dump({"functional_taxonomy": TAXONOMY, "platform_markers": PLATFORM_MARKERS,
               "weights": {"name": NAME_W, "description": DESC_W, "path": PATH_W, "body_head": BODY_W}},
              open(os.path.join(C.DATA, "taxonomy.json"), "w"), indent=1, ensure_ascii=False)
    print(f"classified {n}")
    print("\n== category distribution ==")
    for c, v in catc.most_common():
        print(f"  {v:7} {100*v/n:5.1f}%  {c}")
    print("\n== agent_platform distribution ==")
    for p, v in platc.most_common():
        print(f"  {v:7} {100*v/n:5.1f}%  {p}")

if __name__ == "__main__":
    main()
