---
name: agentforce-observe
description: "Analyze production Agentforce agent behavior using STDM session traces in Data Cloud, plus a fallback path using sf agent test + sf agent preview --authoring-bundle when STDM is unavailable. Use when investigating production failures, regressions, or performance regressions; querying ssot__AiAgentSession__dlm; reproducing reported issues in preview; or improving the .agent file based on production evidence. Trigger phrases: 'why is my agent failing in production', 'analyze production sessions', 'investigate this Agentforce regression', 'what happened in this session', 'reproduce this production issue', 'find sessions where the agent misrouted'. Do NOT trigger for development-time iteration — use /agentforce-develop or /agentforce-test."
argument-hint: "[org alias; optional --agent-file <path> --session-id <id> --days <n>]"
---

# <span data-proof="authored" data-by="ai:claude">/agentforce-observe</span>

> **<span data-proof="authored" data-by="ai:claude">Principles enforced:</span>** <span data-proof="authored" data-by="ai:claude">7 (outsource thinking, not understanding), 3 (jagged intelligence in production), 5 (taste / drift detection), 1 (preserve the quality ceiling). See</span> <span data-proof="authored" data-by="ai:claude">`PRINCIPLES.md`.</span>

## <span data-proof="authored" data-by="ai:claude">Copy-paste-to-agent</span>

```
Improve a deployed Agentforce agent using session-trace evidence. Three phases: (1) Observe
— query STDM session traces from Data Cloud (or fall back to sf agent test + sf agent preview
--authoring-bundle when STDM is unavailable); (2) Reproduce — re-run problematic conversations
in sf agent preview, classify CONFIRMED / INTERMITTENT / NOT REPRODUCED across 3 runs; (3)
Improve — edit the .agent file with targeted fixes, validate, publish, activate, then verify
in preview and post 24-48h re-run Phase 1 against baseline. Always pass --json on every sf
CLI command. Always re-run safety probes after any fix.
```

## <span data-proof="authored" data-by="ai:claude">When to use this skill</span>

<span data-proof="authored" data-by="ai:claude">This skill is for</span> **<span data-proof="authored" data-by="ai:claude">production-grade observation</span>** <span data-proof="authored" data-by="ai:claude">— the agent has shipped, real users are hitting it, and you need evidence to drive improvement. The institutional-memory principle (7) lives here: STDM is the wiki for production agent behavior, and</span> <span data-proof="authored" data-by="ai:claude">`docs/solutions/`</span> <span data-proof="authored" data-by="ai:claude">is the wiki for what we learned from analyzing it.</span>

<span data-proof="authored" data-by="ai:claude">Sister skills:</span>

* <span data-proof="authored" data-by="ai:claude">`/agentforce-develop`</span> <span data-proof="authored" data-by="ai:claude">— making code changes to the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file lives there</span>

* <span data-proof="authored" data-by="ai:claude">`/agentforce-test`</span> <span data-proof="authored" data-by="ai:claude">— Mode A preview testing is the engine this skill uses for reproduction</span>

***

## <span data-proof="authored" data-by="ai:claude">Inputs to gather before starting</span>

<span data-proof="authored" data-by="ai:claude">Ask the user (or auto-detect) the following before running any query:</span>

* **<span data-proof="authored" data-by="ai:claude">Org alias</span>** <span data-proof="authored" data-by="ai:claude">— required.</span>

* **<span data-proof="authored" data-by="ai:claude">Agent API name</span>** <span data-proof="authored" data-by="ai:claude">— required for preview and deploy. Ask if not provided.</span>

* **<span data-proof="authored" data-by="ai:claude">Agent file path</span>** <span data-proof="authored" data-by="ai:claude">— optional; default search is</span> <span data-proof="authored" data-by="ai:claude">`force-app/main/default/aiAuthoringBundles/<AgentName>/<AgentName>.agent`. If not local, retrieve from org.</span>

* **<span data-proof="authored" data-by="ai:claude">Session IDs</span>** <span data-proof="authored" data-by="ai:claude">— optional; if absent, query the last 7 days.</span>

* **<span data-proof="authored" data-by="ai:claude">Days to look back</span>** <span data-proof="authored" data-by="ai:claude">— optional; default 7.</span>

### <span data-proof="authored" data-by="ai:claude">Resolve the agent name (mandatory before STDM queries)</span>

<span data-proof="authored" data-by="ai:claude">STDM uses</span> <span data-proof="authored" data-by="ai:claude">`MasterLabel`</span> <span data-proof="authored" data-by="ai:claude">for filtering; the CLI uses</span> <span data-proof="authored" data-by="ai:claude">`DeveloperName`</span> <span data-proof="authored" data-by="ai:claude">(without the</span> <span data-proof="authored" data-by="ai:claude">`_vN`</span> <span data-proof="authored" data-by="ai:claude">suffix). Get both:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MjA4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf data query --json \
  --query "SELECT Id, MasterLabel, DeveloperName FROM GenAiPlannerDefinition WHERE MasterLabel LIKE '%<user-provided-name>%' OR DeveloperName LIKE '%<user-provided-name>%'" \
  -o <org>
```

<span data-proof="authored" data-by="ai:claude">Store:</span>

* <span data-proof="authored" data-by="ai:claude">`AGENT_MASTER_LABEL`</span> <span data-proof="authored" data-by="ai:claude">— for STDM</span> <span data-proof="authored" data-by="ai:claude">`findSessions()`</span> <span data-proof="authored" data-by="ai:claude">filter (e.g.</span> <span data-proof="authored" data-by="ai:claude">`"Order Service"`)</span>

* <span data-proof="authored" data-by="ai:claude">`AGENT_API_NAME`</span> <span data-proof="authored" data-by="ai:claude">—</span> <span data-proof="authored" data-by="ai:claude">`DeveloperName`</span> <span data-proof="authored" data-by="ai:claude">minus the</span> <span data-proof="authored" data-by="ai:claude">`_vN`</span> <span data-proof="authored" data-by="ai:claude">suffix (e.g.</span> <span data-proof="authored" data-by="ai:claude">`OrderService`)</span>

* <span data-proof="authored" data-by="ai:claude">`PLANNER_ID`</span> <span data-proof="authored" data-by="ai:claude">— Salesforce record ID</span>

### <span data-proof="authored" data-by="ai:claude">Locate the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file</span>

<span data-proof="authored" data-by="ai:claude">Search locally first:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6ODksImF0dHJzIjp7ImJ5IjoiYWk6Y2xhdWRlIn19XQ==
find <project-root>/force-app/main/default/aiAuthoringBundles -name "*.agent" 2>/dev/null
```

<span data-proof="authored" data-by="ai:claude">If not found, retrieve from org:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6ODksImF0dHJzIjp7ImJ5IjoiYWk6Y2xhdWRlIn19XQ==
sf project retrieve start --json --metadata "AiAuthoringBundle:<AGENT_API_NAME>" -o <org>
```

> **<span data-proof="authored" data-by="ai:claude">Known platform bug.</span>**<span data-proof="authored" data-by="ai:claude"></span> <span data-proof="authored" data-by="ai:claude">`sf project retrieve start`</span> <span data-proof="authored" data-by="ai:claude">for</span> <span data-proof="authored" data-by="ai:claude">`AiAuthoringBundle`</span> <span data-proof="authored" data-by="ai:claude">creates a double-nested path:</span> <span data-proof="authored" data-by="ai:claude">`force-app/main/default/main/default/aiAuthoringBundles/...`. Fix immediately:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MjgzLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
if [ -d "force-app/main/default/main/default/aiAuthoringBundles" ]; then
  mkdir -p force-app/main/default/aiAuthoringBundles
  cp -r force-app/main/default/main/default/aiAuthoringBundles/* \
        force-app/main/default/aiAuthoringBundles/
  rm -rf force-app/main/default/main
fi
```

***

## <span data-proof="authored" data-by="ai:claude">Phase 0: Discover the Data Space</span>

<span data-proof="authored" data-by="ai:claude">Before any STDM query, get the active Data Cloud Data Space:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NjgsImF0dHJzIjp7ImJ5IjoiYWk6Y2xhdWRlIn19XQ==
sf api request rest "/services/data/v63.0/ssot/data-spaces" -o <org>
```

> <span data-proof="authored" data-by="ai:claude">Note:</span> <span data-proof="authored" data-by="ai:claude">`sf api request rest`</span> <span data-proof="authored" data-by="ai:claude">is beta. Do NOT pass</span> <span data-proof="authored" data-by="ai:claude">`--json`</span> <span data-proof="authored" data-by="ai:claude">— it's unsupported and errors out.</span>

<span data-proof="authored" data-by="ai:claude">Decision logic:</span>

* <span data-proof="authored" data-by="ai:claude">If the call fails (404, permission error), fall back to</span> <span data-proof="authored" data-by="ai:claude">`default`</span> <span data-proof="authored" data-by="ai:claude">and surface the assumption to the user.</span>

* <span data-proof="authored" data-by="ai:claude">Filter to</span> <span data-proof="authored" data-by="ai:claude">`status: "Active"`.</span>

* <span data-proof="authored" data-by="ai:claude">One active space → use it, confirm to user: "Using Data Space:</span> <span data-proof="authored" data-by="ai:claude">`<name>`".</span>

* <span data-proof="authored" data-by="ai:claude">Multiple → list</span> <span data-proof="authored" data-by="ai:claude">`label + name`, ask which.</span>

<span data-proof="authored" data-by="ai:claude">Store the chosen</span> <span data-proof="authored" data-by="ai:claude">`name`</span> <span data-proof="authored" data-by="ai:claude">as</span> <span data-proof="authored" data-by="ai:claude">`DATA_SPACE`.</span>

### <span data-proof="authored" data-by="ai:claude">Probe STDM availability</span>

<span data-proof="authored" data-by="ai:claude">Deploy the helper class</span> <span data-proof="authored" data-by="ai:claude">`AgentforceOptimizeService`</span> <span data-proof="authored" data-by="ai:claude">once per org (see upstream</span> <span data-proof="authored" data-by="ai:claude">`references/stdm-queries.md`</span> <span data-proof="authored" data-by="ai:claude">for the class source). Then probe:</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NDQ4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf apex run -o <org> -f /dev/stdin << 'APEX'
ConnectApi.CdpQueryInput qi = new ConnectApi.CdpQueryInput();
qi.sql = 'SELECT ssot__Id__c FROM "ssot__AiAgentSession__dlm" LIMIT 1';
try {
    ConnectApi.CdpQueryOutputV2 out = ConnectApi.CdpQuery.queryAnsiSqlV2(qi, '<DATA_SPACE>');
    System.debug('STDM_CHECK:OK rows=' + (out.data != null ? out.data.size() : 0));
} catch (Exception e) {
    System.debug('STDM_CHECK:FAIL ' + e.getMessage());
}
APEX
```

* <span data-proof="authored" data-by="ai:claude">`STDM_CHECK:OK`</span> <span data-proof="authored" data-by="ai:claude">→ proceed to Phase 1.</span>

* <span data-proof="authored" data-by="ai:claude">`STDM_CHECK:FAIL`</span> <span data-proof="authored" data-by="ai:claude">→ STDM is not activated. Switch to</span> **<span data-proof="authored" data-by="ai:claude">Phase 1-ALT (fallback)</span>**<span data-proof="authored" data-by="ai:claude">. Inform the user: "STDM Session Trace Data Model is not available in this org. Enable via Setup → Data Cloud → Data Streams (verify</span> *<span data-proof="authored" data-by="ai:claude">Agentforce Activity</span>* <span data-proof="authored" data-by="ai:claude">is active). Proceeding with fallback: test suites + local traces."</span>

***

## <span data-proof="authored" data-by="ai:claude">Phase 1: Observe — query STDM (preferred path)</span>

### <span data-proof="authored" data-by="ai:claude">1.1 Find sessions</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`findSessions()`</span> <span data-proof="authored" data-by="ai:claude">(in the helper Apex class). Parse</span> <span data-proof="authored" data-by="ai:claude">`DEBUG|STDM_RESULT:`</span> <span data-proof="authored" data-by="ai:claude">from the Apex debug log. Returns session IDs and basic metadata.</span>

<span data-proof="authored" data-by="ai:claude">If</span> <span data-proof="authored" data-by="ai:claude">`findSessions()`</span> <span data-proof="authored" data-by="ai:claude">returns empty, the agent has no production traffic in the window. Switch to Phase 1-ALT (the fallback is also useful when there is no live traffic to observe).</span>

### <span data-proof="authored" data-by="ai:claude">1.2 Get conversation details</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`getMultipleConversationDetails()`</span> <span data-proof="authored" data-by="ai:claude">for up to 5 sessions, most recent first. Returns turn-by-turn data with messages, steps, topics, and action results.</span>

### <span data-proof="authored" data-by="ai:claude">1.2b LLM prompt + response (for LOW adherence cases)</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`getLlmStepDetails()`</span> <span data-proof="authored" data-by="ai:claude">to get the actual LLM prompt and response when grounding is low.</span>

### <span data-proof="authored" data-by="ai:claude">1.2c Aggregated metrics (start here for a health dashboard)</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`getAggregatedMetrics()`</span> <span data-proof="authored" data-by="ai:claude">for: session rates, top intents, quality distribution, RAG averages.</span>

### <span data-proof="authored" data-by="ai:claude">1.2d Moment insights (per-session)</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`getMomentInsights()`</span> <span data-proof="authored" data-by="ai:claude">for: intent summaries, quality scores (1-5), retriever metrics.</span>

### <span data-proof="authored" data-by="ai:claude">1.2e Targeted observability queries (RAG)</span>

<span data-proof="authored" data-by="ai:claude">Use</span> <span data-proof="authored" data-by="ai:claude">`runObservabilityQuery()`</span> <span data-proof="authored" data-by="ai:claude">for</span> <span data-proof="authored" data-by="ai:claude">`KnowledgeGap`,</span> <span data-proof="authored" data-by="ai:claude">`Hallucination`,</span> <span data-proof="authored" data-by="ai:claude">`RetrievalQuality`,</span> <span data-proof="authored" data-by="ai:claude">`AnswerRelevancy`, or</span> <span data-proof="authored" data-by="ai:claude">`Leaderboard`.</span>

### <span data-proof="authored" data-by="ai:claude">1.3 Reconstruct and classify</span>

<span data-proof="authored" data-by="ai:claude">Render a turn-by-turn timeline from</span> <span data-proof="authored" data-by="ai:claude">`ConversationData`</span> <span data-proof="authored" data-by="ai:claude">JSON. Then classify each session against the issue patterns:</span>

* <span data-proof="authored" data-by="ai:claude">Action errors</span>

* <span data-proof="authored" data-by="ai:claude">Subagent misroutes</span>

* <span data-proof="authored" data-by="ai:claude">Missing actions / wrong inputs</span>

* <span data-proof="authored" data-by="ai:claude">Variable capture failures</span>

* <span data-proof="authored" data-by="ai:claude">No transitions (dead-hub anti-pattern)</span>

* <span data-proof="authored" data-by="ai:claude">LOW adherence</span>

* <span data-proof="authored" data-by="ai:claude">Abandoned sessions</span>

* <span data-proof="authored" data-by="ai:claude">Publish drift (live behavior diverges from current</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">source)</span>

* <span data-proof="authored" data-by="ai:claude">Entry agent answering directly (SMALL_TALK pattern)</span>

* <span data-proof="authored" data-by="ai:claude">Safety regressions</span>

<span data-proof="authored" data-by="ai:claude">Priority:</span>

* **<span data-proof="authored" data-by="ai:claude">P1</span>** <span data-proof="authored" data-by="ai:claude">— action errors, misroutes, LOW adherence</span>

* **<span data-proof="authored" data-by="ai:claude">P2</span>** <span data-proof="authored" data-by="ai:claude">— missing actions, variable bugs, knowledge gaps</span>

* **<span data-proof="authored" data-by="ai:claude">P3</span>** <span data-proof="authored" data-by="ai:claude">— performance, abandoned sessions</span>

### <span data-proof="authored" data-by="ai:claude">1.4 Cross-reference against the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file</span>

<span data-proof="authored" data-by="ai:claude">After classifying, retrieve the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file (Phase 0) and run automated checks:</span>

* <span data-proof="authored" data-by="ai:claude">Subagent count vs. action blocks count</span>

* <span data-proof="authored" data-by="ai:claude">Dead-hub detection (subagent defined, never reached)</span>

* <span data-proof="authored" data-by="ai:claude">Orphan actions (Level 1 listed, never invoked at Level 2)</span>

* <span data-proof="authored" data-by="ai:claude">Cross-subagent variable dependencies (writes vs reads)</span>

<span data-proof="authored" data-by="ai:claude">Cross-reference STDM symptoms against</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">structure to identify root causes vs surface symptoms.</span>

### <span data-proof="authored" data-by="ai:claude">1.5 Present findings</span>

<span data-proof="authored" data-by="ai:claude">Show: sessions analyzed, issues grouped by root-cause category, and an estimated uplift if fixed. Then automatically proceed to Phase 2 unless the user wants to stop.</span>

***

## <span data-proof="authored" data-by="ai:claude">Phase 1-ALT: Fallback when STDM is unavailable</span>

| <span data-proof="authored" data-by="ai:claude">Source</span>                             | <span data-proof="authored" data-by="ai:claude">Pros</span>                                      | <span data-proof="authored" data-by="ai:claude">Cons</span>                             |
| ----------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | --------------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">STDM (Phase 1)</span>                     | <span data-proof="authored" data-by="ai:claude">Real production data, volume</span>              | <span data-proof="authored" data-by="ai:claude">Requires Data Cloud, ~15 min lag</span> |
| <span data-proof="authored" data-by="ai:claude">Test suites + local traces (1-ALT)</span> | <span data-proof="authored" data-by="ai:claude">Instant, full LLM prompt + variable state</span> | <span data-proof="authored" data-by="ai:claude">No real users; preview-only</span>      |

### <span data-proof="authored" data-by="ai:claude">1-ALT.1 Run an existing test suite, if any</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MzI1LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf agent test list --json -o <org>
sf agent test run --json --api-name <SuiteName> --wait 10 --result-format json -o <org> | tee /tmp/test_run.json
JOB_ID=$(python3 -c "import json; print(json.load(open('/tmp/test_run.json'))['result']['runId'])")
sf agent test results --json --job-id "$JOB_ID" --result-format json -o <org>
```

### <span data-proof="authored" data-by="ai:claude">1-ALT.2 Derive utterances from the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file</span>

<span data-proof="authored" data-by="ai:claude">Use the same derivation rules as</span> <span data-proof="authored" data-by="ai:claude">`/agentforce-test`</span> <span data-proof="authored" data-by="ai:claude">Step 0: subagent-based, action-based, guardrail, multi-turn, safety probes.</span>

> **⚠️ Debug logs must be on the Agent User, not the admin user.**
> When using `--use-live-actions`, Apex runs as the Einstein Agent User (the `@agentforce.com` scoped user), not your admin. If you set debug logs on your admin user, you will see zero Apex logs even when actions are being called. In Setup → Debug Logs, add the **agent user** specifically. Check the agent user's email in Setup → Users, filtered by "Einstein Agent".

> **⚠️ `available when:` gate behavior.** If a variable hasn't been captured yet (e.g. `customer_email` is still `""`), an action guarded by `available when @variables.customer_email != ""` will simply not appear in the `EnabledToolsStep` of the trace. The action is silently skipped — no error is thrown. If your action is never called, check the trace's `VariableUpdateStep` entries to confirm the variable was actually set before the action was invoked.

### <span data-proof="authored" data-by="ai:claude">1-ALT.3 Preview with</span> <span data-proof="authored" data-by="ai:claude">`--authoring-bundle`</span> <span data-proof="authored" data-by="ai:claude">(local traces)</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6NDYxLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf agent preview start --json --authoring-bundle <BundleName> -o <org> | tee /tmp/preview_start.json
SESSION_ID=$(python3 -c "import json; print(json.load(open('/tmp/preview_start.json'))['result']['sessionId'])")

sf agent preview send --json --session-id "$SESSION_ID" --authoring-bundle <BundleName> --utterance "<UTT>" -o <org> | tee /tmp/preview_response.json

sf agent preview end --json --session-id "$SESSION_ID" --authoring-bundle <BundleName> -o <org>
```

<span data-proof="authored" data-by="ai:claude">Trace files:</span> <span data-proof="authored" data-by="ai:claude">`.sfdx/agents/<BundleName>/sessions/<sessionId>/traces/<planId>.json`.</span>

### <span data-proof="authored" data-by="ai:claude">1-ALT.4 Local trace diagnosis</span>

| <span data-proof="authored" data-by="ai:claude">Issue type</span>            | <span data-proof="authored" data-by="ai:claude">Trace command</span>                                                                               |
| ---------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">Subagent misroute</span>     | <span data-proof="authored" data-by="ai:claude">`jq -r '.plan[] | select(.type=="NodeEntryStateStep") | .data.agent_name' "$TRACE"`</span>         |
| <span data-proof="authored" data-by="ai:claude">Action not called</span>     | <span data-proof="authored" data-by="ai:claude">`jq -r '.plan[] | select(.type=="EnabledToolsStep") | .data.enabled_tools[]' "$TRACE"`</span>      |
| <span data-proof="authored" data-by="ai:claude">LOW adherence</span>         | <span data-proof="authored" data-by="ai:claude">`jq -r '.plan[] | select(.type=="ReasoningStep") | {category, reason}' "$TRACE"`</span>            |
| <span data-proof="authored" data-by="ai:claude">Variable capture fail</span> | <span data-proof="authored" data-by="ai:claude">`jq -r '.plan[] | select(.type=="VariableUpdateStep") | .data.variable_updates[]' "$TRACE"`</span> |
| <span data-proof="authored" data-by="ai:claude">Vague instructions</span>    | <span data-proof="authored" data-by="ai:claude">`jq -r '.plan[] | select(.type=="LLMStep") | .data.messages_sent[0].content' "$TRACE"`</span>      |

> **<span data-proof="authored" data-by="ai:claude">DefaultTopic trace quirk.</span>** <span data-proof="authored" data-by="ai:claude">With</span> <span data-proof="authored" data-by="ai:claude">`--authoring-bundle`, the root</span> <span data-proof="authored" data-by="ai:claude">`.topic`</span> <span data-proof="authored" data-by="ai:claude">field often shows</span> <span data-proof="authored" data-by="ai:claude">`"DefaultTopic"`</span> <span data-proof="authored" data-by="ai:claude">even when routing works. Always use</span> <span data-proof="authored" data-by="ai:claude">`NodeEntryStateStep.data.agent_name`</span> <span data-proof="authored" data-by="ai:claude">for the real subagent chain.</span>

> **<span data-proof="authored" data-by="ai:claude">Entry-answering-directly (SMALL_TALK pattern).</span>** <span data-proof="authored" data-by="ai:claude">If</span> <span data-proof="authored" data-by="ai:claude">`start_agent`</span> <span data-proof="authored" data-by="ai:claude">trace shows</span> <span data-proof="authored" data-by="ai:claude">`SMALL_TALK`</span> <span data-proof="authored" data-by="ai:claude">grounding and transition tools are visible but none invoked, add</span> <span data-proof="authored" data-by="ai:claude">`"You are a router only. Do NOT answer questions directly."`</span> <span data-proof="authored" data-by="ai:claude">to</span> <span data-proof="authored" data-by="ai:claude">`start_agent: instructions:`.</span>

***

## <span data-proof="authored" data-by="ai:claude">Phase 2: Reproduce — live preview, 3-run classification</span>

<span data-proof="authored" data-by="ai:claude">For every confirmed issue from Phase 1, build one preview scenario per issue. Run each scenario</span> **<span data-proof="authored" data-by="ai:claude">3 times</span>** <span data-proof="authored" data-by="ai:claude">and classify:</span>

| <span data-proof="authored" data-by="ai:claude">Verdict</span>            | <span data-proof="authored" data-by="ai:claude">Criteria</span>                 |
| ------------------------------------------------------------------------- | ------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">`[CONFIRMED]`</span>      | <span data-proof="authored" data-by="ai:claude">Same failure in 3/3 runs</span> |
| <span data-proof="authored" data-by="ai:claude">`[INTERMITTENT]`</span>   | <span data-proof="authored" data-by="ai:claude">Failure in 1-2/3 runs</span>    |
| <span data-proof="authored" data-by="ai:claude">`[NOT REPRODUCED]`</span> | <span data-proof="authored" data-by="ai:claude">Passes 3/3</span>               |

<span data-proof="authored" data-by="ai:claude">Only</span> <span data-proof="authored" data-by="ai:claude">`[CONFIRMED]`</span> <span data-proof="authored" data-by="ai:claude">and</span> <span data-proof="authored" data-by="ai:claude">`[INTERMITTENT]`</span> <span data-proof="authored" data-by="ai:claude">proceed to Phase 3. The 3-run discipline exists because LLM jitter (Principle 3) will lie to you if you only run once.</span>

> **⚠️ Use `--use-live-actions` for reproduction.** Reproducing a production issue requires the same conditions: real Apex called. Without `--use-live-actions`, the preview runs in simulated mode and will likely succeed even for issues that fail in production. Always reproduce with:
> ```bash
> sf agent preview start --json --use-live-actions --apex-debug --authoring-bundle <Name> -o <org>
> ```

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MjUyLCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf agent preview start --json --authoring-bundle <Name> -o <org>
sf agent preview send --json --session-id "$SID" --utterance "<text>" --authoring-bundle <Name> -o <org>
sf agent preview end --json --session-id "$SID" --authoring-bundle <Name> -o <org>
```

<span data-proof="authored" data-by="ai:claude">Trace path:</span> <span data-proof="authored" data-by="ai:claude">`.sfdx/agents/<Name>/sessions/<sessionId>/traces/<planId>.json`.</span>

***

## <span data-proof="authored" data-by="ai:claude">Phase 3: Improve — edit the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file directly</span>

### <span data-proof="authored" data-by="ai:claude">3.0 Pre-flight</span>

<span data-proof="authored" data-by="ai:claude">Verify all action targets exist and are registered in the org before editing. If any are missing, present options to the user: deploy stubs, remove the actions, register via UI, or proceed with routing-only fixes.</span>

### <span data-proof="authored" data-by="ai:claude">3.1–3.3 Map each issue to a fix location</span>

| <span data-proof="authored" data-by="ai:claude">Confirmed issue</span>          | <span data-proof="authored" data-by="ai:claude">Fix location</span>                     | <span data-proof="authored" data-by="ai:claude">Strategy</span>                                                                                                                                          |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| <span data-proof="authored" data-by="ai:claude">Subagent misroute</span>        | <span data-proof="authored" data-by="ai:claude">`subagent: description:`</span>         | <span data-proof="authored" data-by="ai:claude">Add keywords from production utterances</span>                                                                                                           |
| <span data-proof="authored" data-by="ai:claude">Wrong action</span>             | <span data-proof="authored" data-by="ai:claude">Action descriptions</span>              | <span data-proof="authored" data-by="ai:claude">Add exclusion language</span>                                                                                                                            |
| <span data-proof="authored" data-by="ai:claude">LOW grounding</span>            | <span data-proof="authored" data-by="ai:claude">`instructions: ->`</span>               | <span data-proof="authored" data-by="ai:claude">Inject</span> <span data-proof="authored" data-by="ai:claude">`{!@variables.x}`</span> <span data-proof="authored" data-by="ai:claude">references</span> |
| <span data-proof="authored" data-by="ai:claude">Persona leak</span>             | <span data-proof="authored" data-by="ai:claude">`system: instructions:`</span>          | <span data-proof="authored" data-by="ai:claude">Move persona out of subagents</span>                                                                                                                     |
| <span data-proof="authored" data-by="ai:claude">Dead hub</span>                 | <span data-proof="authored" data-by="ai:claude">Transitions in upstream subagent</span> | <span data-proof="authored" data-by="ai:claude">Add transition action</span>                                                                                                                             |
| <span data-proof="authored" data-by="ai:claude">Entry answering directly</span> | <span data-proof="authored" data-by="ai:claude">`start_agent: instructions:`</span>     | <span data-proof="authored" data-by="ai:claude">Add router-only constraint</span>                                                                                                                        |
| <span data-proof="authored" data-by="ai:claude">Safety regression</span>        | <span data-proof="authored" data-by="ai:claude">`system: instructions:`</span>          | <span data-proof="authored" data-by="ai:claude">Re-state safety guidelines, response constraints</span>                                                                                                  |

<span data-proof="authored" data-by="ai:claude">Instruction principles (Principle 5 — taste over typing):</span>

* <span data-proof="authored" data-by="ai:claude">Name actions explicitly. Don't rely on the LLM to infer.</span>

* <span data-proof="authored" data-by="ai:claude">State pre-conditions clearly. Use</span> <span data-proof="authored" data-by="ai:claude">`available when:`</span> <span data-proof="authored" data-by="ai:claude">guards.</span>

* <span data-proof="authored" data-by="ai:claude">Scope tightly. One subagent, one job.</span>

* <span data-proof="authored" data-by="ai:claude">Persona in</span> <span data-proof="authored" data-by="ai:claude">`system:`</span> <span data-proof="authored" data-by="ai:claude">only — never in subagents.</span>

### <span data-proof="authored" data-by="ai:claude">3.4 Regression prevention</span>

* <span data-proof="authored" data-by="ai:claude">Establish a baseline before editing (the Phase 1 metrics).</span>

* <span data-proof="authored" data-by="ai:claude">Make minimal edits.</span>

* <span data-proof="authored" data-by="ai:claude">Test immediately after each edit.</span>

* <span data-proof="authored" data-by="ai:claude">One fix per publish cycle.</span>

* <span data-proof="authored" data-by="ai:claude">Check cross-subagent dependencies before touching shared variables.</span>

* <span data-proof="authored" data-by="ai:claude">Test adjacent subagents — fixing one routing description can break a sibling.</span>

### <span data-proof="authored" data-by="ai:claude">3.5 Apply</span>

<span data-proof="authored" data-by="ai:claude">Read the</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file with the Read tool. Edit with the Edit tool (use tabs for indentation if the file uses tabs). Show the diff to the user.</span>

### <span data-proof="authored" data-by="ai:claude">3.6 Validate, deploy, publish, activate</span>

```bash proof:W3sidHlwZSI6InByb29mQXV0aG9yZWQiLCJmcm9tIjowLCJ0byI6MjE4LCJhdHRycyI6eyJieSI6ImFpOmNsYXVkZSJ9fV0=
sf agent validate authoring-bundle --json --api-name <AGENT_API_NAME> -o <org>
sf agent publish authoring-bundle --json --api-name <AGENT_API_NAME> -o <org>
sf agent activate --json --api-name <AGENT_API_NAME> -o <org>
```

<span data-proof="authored" data-by="ai:claude">If</span> <span data-proof="authored" data-by="ai:claude">`publish`</span> <span data-proof="authored" data-by="ai:claude">fails, the deploy + activate fallback is incomplete — it does not propagate</span> <span data-proof="authored" data-by="ai:claude">`reasoning: actions:`</span> <span data-proof="authored" data-by="ai:claude">to live metadata. Fix the publish error rather than working around it.</span>

### <span data-proof="authored" data-by="ai:claude">3.7 Verify</span>

<span data-proof="authored" data-by="ai:claude">Re-run Phase 2 scenarios post-fix. Check the trace for correct routing, grounding, tools, and variables. Then</span> **<span data-proof="authored" data-by="ai:claude">schedule a re-run of Phase 1 in 24–48 hours</span>** <span data-proof="authored" data-by="ai:claude">to compare against baseline. Production lag is real; preview-only verification is not enough (Principle 3).</span>

### <span data-proof="authored" data-by="ai:claude">3.7b Safety re-verification (mandatory, Principle 1)</span>

<span data-proof="authored" data-by="ai:claude">Re-run safety probes against the modified</span> <span data-proof="authored" data-by="ai:claude">`.agent`</span> <span data-proof="authored" data-by="ai:claude">file.</span> **<span data-proof="authored" data-by="ai:claude">Revert any change that introduces a BLOCK finding.</span>** <span data-proof="authored" data-by="ai:claude">A regressed safety surface is not allowed to ship regardless of what other improvement it brings.</span>

### <span data-proof="authored" data-by="ai:claude">3.8 Capture regression tests</span>

<span data-proof="authored" data-by="ai:claude">Convert each</span> <span data-proof="authored" data-by="ai:claude">`[CONFIRMED]`</span> <span data-proof="authored" data-by="ai:claude">issue into a Testing Center YAML test case. Deploy with</span> <span data-proof="authored" data-by="ai:claude">`sf agent test create`</span> <span data-proof="authored" data-by="ai:claude">and verify all previously-broken scenarios pass. The regression suite is institutional memory — Principle 7.</span>

***

## <span data-proof="authored" data-by="ai:claude">Capture learnings</span>

<span data-proof="authored" data-by="ai:claude">Run</span> <span data-proof="authored" data-by="ai:claude">`/sf-compound`</span> <span data-proof="authored" data-by="ai:claude">to write the diagnosis to</span> <span data-proof="authored" data-by="ai:claude">`docs/solutions/`</span> <span data-proof="authored" data-by="ai:claude">under</span> <span data-proof="authored" data-by="ai:claude">`agent-issues`</span> <span data-proof="authored" data-by="ai:claude">(or the closest existing category). Production agent issues are exactly the kind of jagged-edge knowledge nothing else in the Salesforce ecosystem will retain for you.</span>

***

## <span data-proof="authored" data-by="ai:claude">Inspiration</span>

<span data-proof="authored" data-by="ai:claude">This skill is adapted from</span> [<span data-proof="authored" data-by="ai:claude">`forcedotcom/afv-library/skills/observing-agentforce`</span>](https://github.com/forcedotcom/afv-library/blob/main/skills/observing-agentforce/SKILL.md) <span data-proof="authored" data-by="ai:claude">(Apache-2.0). The upstream skill ships with five reference files (`references/stdm-queries.md`,</span> <span data-proof="authored" data-by="ai:claude">`references/issue-classification.md`,</span> <span data-proof="authored" data-by="ai:claude">`references/reproduce-reference.md`,</span> <span data-proof="authored" data-by="ai:claude">`references/improve-reference.md`,</span> <span data-proof="authored" data-by="ai:claude">`references/stdm-schema.md`) covering full STDM Apex source, DMO field schemas, complete issue-pattern tables, and detailed reproduction procedures. For the</span> <span data-proof="authored" data-by="ai:claude">`AgentforceOptimizeService`</span> <span data-proof="authored" data-by="ai:claude">Apex class source and full DMO schema, consult the upstream. This plugin's adaptation tightens the observe → reproduce → improve cycle around the principles framework and integrates with</span> <span data-proof="authored" data-by="ai:claude">`/sf-compound`</span> <span data-proof="authored" data-by="ai:claude">for institutional memory capture.</span>