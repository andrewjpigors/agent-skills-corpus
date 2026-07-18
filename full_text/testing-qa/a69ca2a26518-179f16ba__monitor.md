---
name: monitor
description: Set up recurring monitoring checks using /loop for test suites, builds, deployments, or custom health checks
disable-model-invocation: true
argument-hint: "<interval> <check-description>"
---

Set up a recurring monitoring check using the `/loop` skill. Parse the user's request to determine:

1. **What to monitor** (extract from arguments or ask)
2. **How often** (extract interval from arguments, default to 10m)
3. **What constitutes success/failure**

## Common Monitoring Patterns

### Test Suite Health
```
/loop 10m Run the test suite and report any failures: uv run pytest --tb=short
```

### Build Status
```
/loop 15m Check if the build passes: npm run build 2>&1 | tail -5
```

### Deployment Status
```
/loop 5m Check deployment status: curl -sf https://staging.example.com/health
```

### Dependency Freshness
```
/loop 2h Check for outdated dependencies: uv run pip list --outdated 2>/dev/null | head -20
```

### Git Branch Drift
```
/loop 30m Check how far this branch has drifted from main: git fetch origin && git log --oneline origin/main..HEAD | wc -l
```

## Workflow

1. Parse the user's `$ARGUMENTS` for an interval and check description
2. If the interval is provided (e.g., "5m", "1h"), use it directly
3. If no interval is provided, default to 10 minutes
4. Set up the `/loop` with the appropriate check command
5. Confirm what was set up and how to cancel it

## Output

Confirm the monitoring setup:
- What is being monitored
- How often (interval)
- How to cancel (`/loop` to list, then cancel by ID)
