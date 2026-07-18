---
name: harness-ops
description: "Deployment description: Deployment & Ops domain skill for the harness plugin. Provides ops methodology selection (GitOps, Platform Engineering, SRE, DevOps, Infrastructure-as-Code), development methodology (Pipeline-First, Infrastructure-First, Monitoring-First, Runbook-First, Security-First), verification strategy, deliverable verification, evaluation criteria (operational_readiness, automation_coverage, reliability_design, security_posture), and sprint contract checklist templates. Activated when domain_profile is "ops". Ops domain skill for the harness plugin. Provides ops methodology selection (GitOps, Platform Engineering, SRE, DevOps, Infrastructure-as-Code), development methodology (Pipeline-First, Infrastructure-First, Monitoring-First, Runbook-First, Security-First), verification strategy, deliverable verification, evaluation criteria (operational_readiness, automation_coverage, reliability_design, security_posture), and sprint contract checklist templates. Activated when domain_profile is "ops"."
---

# Deployment & Ops Domain Skill

> **Domain-specific.** This skill provides the HOW for deployment and operations projects. The harness provides the WHEN (orchestration, sprint contracts, feature ledger). This skill provides the HOW (methodology selection, development methodology, deliverable verification, evaluation criteria anchors, and ops-specific patterns).

Activated when `domain_profile: ops` is declared in `.harness/spec.md`.

## Scope of This Skill

This skill covers the full Deployment & Operations lifecycle:
- **Build**: CI/CD pipeline design, build automation, artifact management
- **Deploy**: Infrastructure provisioning, deployment strategies, configuration management
- **Operate**: Monitoring, alerting, incident response, runbooks
- **Secure**: Secret management, access control, compliance, vulnerability management
- **Optimize**: Capacity planning, cost optimization, performance tuning, reliability engineering

It is methodology-agnostic at its core — any of the supported approaches can be selected. GitOps is the default because it provides declarative infrastructure management with git as the single source of truth, mapping naturally to harness sprint boundaries.


## Activation Check

This skill activates when `domain_profile: ops` is set in `.harness/spec.md` or `.harness/state.json`.

Before using this skill's procedures:
1. Verify the project produces ops deliverables (runbooks, IaC configs, pipeline definitions, monitoring dashboards — not primarily application code)
2. Read spec.md -> identify the selected ops methodology (GitOps, SRE, Platform Engineering, etc.)
3. If no methodology specified -> default to GitOps
4. Check if `infrastructure/` or `ops/` directory exists -> if yes, verify against the Repository Structure (Section 9)
5. Identify the cloud provider/platform -> select appropriate reference patterns from Section 7

---

## Section 1: Ops Methodology

Select based on project characteristics during `/harness:start`:

| Methodology | When to Use | Phase Structure | Harness Mapping |
|-------------|-------------|-----------------|-----------------|
| GitOps | Kubernetes-native, declarative infrastructure | Define, Commit, Reconcile, Verify | 1 sprint = 1 environment or service stack |
| Platform Engineering | Internal developer platforms, self-service infrastructure | Foundation, Services, Portal, Adoption | 1 sprint = 1 platform capability |
| SRE (Site Reliability Engineering) | High-availability services, error budgets | Define SLOs, Measure SLIs, Error Budgets, Toil Reduction | 1 sprint = 1 SLO domain or toil reduction |
| DevOps | General CI/CD, culture-driven automation | Plan, Code, Build, Test, Release, Deploy, Operate, Monitor | 1 sprint = 1 pipeline stage or ops capability |
| Infrastructure-as-Code | Cloud provisioning, environment management | Design, Code, Test, Apply, Drift-Detect | 1 sprint = 1 infrastructure layer or environment |

**Default:** GitOps (if not specified by user).

The planner writes the selected methodology into `spec.md` during initialization. The coordinator uses the mapping to structure sprint boundaries accordingly.

---

## Section 2: Ops Development Methodology

Select based on project type and operational needs:

| Methodology | When to Use | How It Drives the Generator |
|-------------|-------------|----------------------------|
| Pipeline-First | CI/CD modernization, deployment automation | Generator defines pipeline stages FIRST (build, test, deploy, verify), then provisions infrastructure to support them |
| Infrastructure-First | Greenfield cloud setup, datacenter migration | Generator provisions infrastructure FIRST (networks, compute, storage, databases), then adds deployment pipelines on top |
| Monitoring-First | Observability gaps, incident reduction | Generator defines monitoring and alerting FIRST (metrics, logs, traces, dashboards, alerts), then builds runbooks around failure signals |
| Runbook-First | Operational maturity, incident response | Generator writes runbooks FIRST (procedures, escalation, recovery steps), then automates runbook steps where possible |
| Security-First | Compliance-driven, regulated environments | Generator defines security controls FIRST (IAM, encryption, network policies, audit logging), then builds infrastructure within security boundaries |

**Default:** Pipeline-First for all ops projects (if not specified).

### How Methodology Drives the Harness

The chosen methodology affects every phase:

1. **Generator behavior**: What to produce first (pipelines? infrastructure? monitoring?)
2. **Evaluator criteria**: What to prioritize (deployment reliability? infrastructure coverage? observability?)
3. **Sprint contract**: What acceptance criteria to define (pipeline stages? IaC coverage? alert coverage?)
4. **Artifact types**: What deliverables per sprint (pipeline configs? Terraform modules? Grafana dashboards?)

### Generator First-Action Table

| Methodology | Generator produces first | Then |
|-------------|------------------------|------|
| Pipeline-First | CI/CD pipeline definitions with stages, triggers, and gates | Infrastructure provisioning, deployment configs, environment promotion |
| Infrastructure-First | IaC modules for compute, networking, storage, and databases | CI/CD pipelines deploying to provisioned infrastructure |
| Monitoring-First | Monitoring stack with metrics collection, dashboards, and alert rules | Runbooks for each alert, SLO definitions, incident response procedures |
| Runbook-First | Operational runbooks with step-by-step procedures and escalation paths | Automation scripts replacing manual runbook steps, monitoring to trigger runbooks |
| Security-First | Security architecture with IAM policies, encryption config, network segmentation | Infrastructure and pipelines implementing security controls, audit logging |

---

## Section 3: Verification Strategy (Ops Equivalent of Testing)

| Verification Type | Ops Equivalent | Method |
|-------------------|---------------|--------|
| Unit test | Config validation | Each IaC module validates independently (terraform validate, helm lint, kustomize build) |
| Integration test | Environment smoke test | Provisioned environment responds to health checks, services discover each other |
| E2E test | Deployment dry-run | Full deployment pipeline executes in staging without errors, rollback tested |
| Smoke test | Deliverable completeness | Required configs, runbooks, and dashboards exist and are non-empty |
| Regression | Drift detection | Infrastructure state matches declared config (terraform plan shows no drift) |

### Operational Completeness Checks

- Does the CI/CD pipeline exist with build, test, and deploy stages?
- Are all environments provisioned with IaC (not manual)?
- Does each critical service have a health check endpoint?
- Are monitoring dashboards configured for key metrics (latency, error rate, throughput, saturation)?
- Do alert rules exist with defined severity levels and escalation paths?
- Does each alert have a corresponding runbook?
- Are secrets managed through a dedicated secret manager (not hardcoded)?
- Is there a rollback procedure documented and tested?

---

## Section 4: Deliverable Verification (Equivalent of Build/Runtime)

Since ops produces configurations and procedures, "build verification" means:

| Check | What to Verify | How |
|-------|---------------|-----|
| IaC syntax | Terraform/CloudFormation/Pulumi configs are valid | Run linting tools (terraform validate, cfn-lint, pulumi preview) |
| Pipeline syntax | CI/CD pipeline definitions are valid | Validate with platform tools (GitHub Actions, GitLab CI lint, Jenkins pipeline linter) |
| Secret scanning | No secrets in committed files | Run tools like gitleaks, truffleHog, or detect-secrets |
| Config drift | Deployed infrastructure matches IaC declarations | terraform plan, kubectl diff, or equivalent drift detection |
| Runbook completeness | Each runbook has required sections | Check for: trigger, impact, steps, escalation, rollback, verification |
| Dashboard validity | Monitoring dashboards query valid metrics | Validate Grafana/Datadog JSON, check metric names against actual emissions |
| Security compliance | Configs follow security baseline | Run checkov, tfsec, or cloud-specific security scanners |

### Pipeline Stage Gate Checks

| Stage | Required Checks |
|-------|----------------|
| Build | Source checkout, dependency install, compilation/bundling, artifact creation |
| Test | Unit tests, integration tests, security scan, linting |
| Deploy (staging) | Infrastructure provisioning, application deployment, health check verification |
| Verify (staging) | Smoke tests, integration tests against staging, monitoring confirmation |
| Deploy (production) | Blue/green or canary deployment, traffic shifting, health check verification |
| Post-deploy | Monitoring verification, alert testing, rollback readiness confirmation |

---

## Section 5: Evaluation Criteria (Ops Profile)

The 4 primary criteria for the `ops` domain profile. The evaluator MUST use these anchors for consistent scoring across sprints.

### operational_readiness (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no runbooks, no monitoring, no documented procedures |
| 1 | Severely incomplete — some monitoring exists but no runbooks, no incident response process |
| 2 | Below acceptable — runbooks exist but incomplete, monitoring gaps for critical services, no escalation paths |
| 3 | Acceptable — runbooks cover critical scenarios, monitoring dashboards for key metrics, alert rules with severity levels, escalation paths defined |
| 4 | Strong — comprehensive runbooks with automated steps, SLO-based monitoring, on-call rotation defined, post-incident review process in place |
| 5 | Excellent — fully automated incident detection and response, game days conducted, chaos engineering validated, mean-time-to-recovery measured and optimized |

### automation_coverage (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — all operations are manual |
| 1 | Severely incomplete — some scripts exist but no pipeline, manual deployments are the norm |
| 2 | Below acceptable — CI pipeline exists but CD is manual, infrastructure provisioned manually |
| 3 | Acceptable — CI/CD pipeline automates build-test-deploy, infrastructure provisioned via IaC, environments are repeatable |
| 4 | Strong — fully automated pipeline with staging and production, IaC covers all infrastructure, automated rollback, environment promotion automated |
| 5 | Excellent — zero-touch deployments, self-healing infrastructure, automated capacity scaling, GitOps reconciliation loop, canary analysis automated |

### reliability_design (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — no redundancy, no backup, no recovery plan |
| 1 | Severely incomplete — single points of failure, no backup strategy, no health checks |
| 2 | Below acceptable — some redundancy but untested, backups exist but restore untested, health checks incomplete |
| 3 | Acceptable — redundancy for critical components, backup and restore tested, health checks on all services, rollback procedure documented |
| 4 | Strong — multi-region or multi-zone redundancy, automated failover, disaster recovery tested, SLOs defined with error budgets, circuit breakers implemented |
| 5 | Excellent — chaos engineering validates resilience, RTO/RPO targets met and measured, graceful degradation designed, zero-downtime deployments proven |

### security_posture (0-5)

| Score | Anchor Description |
|-------|--------------------|
| 0 | Absent — secrets hardcoded, no access control, no encryption |
| 1 | Severely incomplete — some access control but secrets in config files, no encryption at rest |
| 2 | Below acceptable — secrets in vault but rotation not automated, basic IAM but overly permissive, partial encryption |
| 3 | Acceptable — secrets managed in dedicated vault with rotation, IAM follows least-privilege, encryption at rest and in transit, audit logging enabled |
| 4 | Strong — automated secret rotation, network segmentation with zero-trust principles, vulnerability scanning in pipeline, compliance baselines enforced (CIS, SOC2) |
| 5 | Excellent — continuous compliance monitoring, security as code fully integrated, threat modeling documented, penetration testing scheduled, incident response tested |

---

## Section 6: Sprint Contract Checklist Templates

Pre-built checklists for 5 ops phases. The generator includes the relevant checklist(s) in each sprint contract. The evaluator uses them as acceptance criteria.

### For CI/CD Pipeline

- [ ] Pipeline definition exists with build, test, and deploy stages
- [ ] Build stage produces versioned artifacts (container images, packages)
- [ ] Test stage runs unit tests, integration tests, and security scans
- [ ] Deploy stage supports at least staging and production environments
- [ ] Rollback mechanism defined and tested

### For Infrastructure Provisioning

- [ ] All infrastructure defined as code (Terraform, CloudFormation, Pulumi, or equivalent)
- [ ] Environments are reproducible from IaC definitions alone
- [ ] State management configured (remote state, locking)
- [ ] Module structure follows DRY principles (shared modules for common patterns)
- [ ] Cost estimation included (infracost or equivalent)

### For Monitoring & Alerting

- [ ] Metrics collection configured for all critical services (latency, error rate, throughput, saturation)
- [ ] Dashboards created for service health and business metrics
- [ ] Alert rules defined with severity levels (critical, warning, info)
- [ ] Alert routing configured with escalation paths and on-call schedule
- [ ] SLOs defined with measurable SLIs for key user journeys

### For Runbook Development

- [ ] Runbook exists for each critical alert
- [ ] Each runbook includes: trigger condition, impact assessment, diagnostic steps, resolution steps, escalation path, verification steps
- [ ] Runbooks reviewed by on-call engineers
- [ ] Automated remediation implemented for common scenarios
- [ ] Post-incident review template defined

### For Security Hardening

- [ ] Secrets stored in dedicated vault (HashiCorp Vault, AWS Secrets Manager, etc.)
- [ ] IAM policies follow least-privilege principle
- [ ] Network segmentation implemented (VPC, security groups, network policies)
- [ ] Encryption enabled at rest and in transit
- [ ] Vulnerability scanning integrated into CI/CD pipeline

---

## Section 7: Reference Materials

### Ops Frameworks

| Framework | Scope | Key Concepts |
|-----------|-------|-------------|
| DORA Metrics | DevOps performance measurement | Deployment frequency, lead time, change failure rate, MTTR |
| Google SRE Book | Site reliability engineering practices | SLOs, error budgets, toil reduction, incident management |
| AWS Well-Architected (Ops Pillar) | Cloud operational excellence | Organization, preparation, operation, evolution |
| NIST Cybersecurity Framework | Security and compliance | Identify, Protect, Detect, Respond, Recover |
| ITIL 4 | IT service management | Service value chain, practices, guiding principles |

### Common Tools by Category

| Category | Tools | Use Case |
|----------|-------|----------|
| IaC | Terraform, Pulumi, CloudFormation, Ansible | Infrastructure provisioning and configuration |
| CI/CD | GitHub Actions, GitLab CI, Jenkins, ArgoCD | Build, test, and deploy automation |
| Containers | Docker, Kubernetes, Helm, Kustomize | Application packaging and orchestration |
| Monitoring | Prometheus, Grafana, Datadog, New Relic | Metrics, dashboards, and alerting |
| Logging | ELK Stack, Loki, Splunk, CloudWatch Logs | Centralized log aggregation and search |
| Security | HashiCorp Vault, Checkov, Trivy, Falco | Secret management and security scanning |

---

## Section 8: Notation Guide

### Infrastructure Diagram Conventions

| Element | Symbol | Usage |
|---------|--------|-------|
| Cloud Region | Large dashed rectangle | Geographic boundary (us-east-1, eu-west-1) |
| Availability Zone | Dashed rectangle within region | Redundancy boundary |
| VPC/Network | Solid rectangle | Network isolation boundary |
| Subnet | Colored rectangle | Public (green), private (blue), data (orange) |
| Compute Instance | Server icon | VM, container, or serverless function |
| Database | Cylinder | Managed database service |
| Load Balancer | Horizontal bar with arrows | Traffic distribution |
| CDN/Edge | Cloud icon | Content delivery and edge computing |
| Security Group | Shield icon | Network access control |

### Pipeline Flow Notation

| Element | Representation | Usage |
|---------|---------------|-------|
| Stage | Rectangle with stage name | A phase of the pipeline (Build, Test, Deploy) |
| Step | Rounded rectangle within stage | A single action within a stage |
| Gate | Diamond | Approval or quality gate between stages |
| Parallel | Forked arrow | Steps running concurrently |
| Artifact | Document icon | Build output passed between stages |
| Trigger | Circle | Event that starts the pipeline (push, schedule, webhook) |

### Network Topology Standards

| Element | Representation | Usage |
|---------|---------------|-------|
| Internet | Cloud shape | Public internet boundary |
| Firewall/WAF | Brick wall icon | Network security boundary |
| DNS | Globe icon | Domain name resolution |
| Service Mesh | Dotted connections | Service-to-service communication layer |
| Message Queue | Queue icon | Asynchronous communication |

---

## Section 9: Ops Repository Structure

The generator should organize ops deliverables following this repository structure:

```
.harness/
  spec.md                              # Ops Statement of Work
  features.json                        # Ops deliverable tracker

project-root/
  infrastructure/
    1-foundation/
      networking.tf                    # VPC, subnets, security groups
      iam.tf                           # IAM roles, policies, service accounts
      dns.tf                           # DNS zones and records
      secrets.tf                       # Secret manager configuration
    2-compute/
      clusters.tf                      # Kubernetes clusters or compute instances
      autoscaling.tf                   # Auto-scaling configurations
      load-balancers.tf                # Load balancer definitions
    3-data/
      databases.tf                     # Database instances and configurations
      caches.tf                        # Cache layer (Redis, Memcached)
      storage.tf                       # Object storage, file systems
    4-monitoring/
      dashboards/                      # Grafana/Datadog dashboard definitions
      alerts/                          # Alert rule definitions
      slos.md                          # SLO definitions with SLIs
    modules/
      vpc/                             # Reusable VPC module
      eks/                             # Reusable Kubernetes module
      rds/                             # Reusable database module
    environments/
      dev/                             # Dev environment overrides
      staging/                         # Staging environment overrides
      production/                      # Production environment overrides
  pipelines/
    ci.yaml                            # CI pipeline definition
    cd-staging.yaml                    # CD pipeline for staging
    cd-production.yaml                 # CD pipeline for production
  runbooks/
    incident-response.md               # General incident response procedure
    service-a-outage.md                # Service-specific runbook
    database-failover.md               # Database failover procedure
    rollback-procedure.md              # Deployment rollback steps
  security/
    baseline.md                        # Security baseline requirements
    compliance-checklist.md            # Compliance verification checklist
    threat-model.md                    # Threat model documentation
```

### Repository Completeness Check (Evaluator)

The evaluator verifies repository structure completeness per phase:

| After Phase | Required Directories | Required Files (minimum) |
|-------------|---------------------|-------------------------|
| Foundation | `infrastructure/1-foundation/` | networking.tf, iam.tf |
| Compute | `infrastructure/2-compute/` | clusters.tf or equivalent compute definition |
| Pipeline | `pipelines/` | ci.yaml, at least 1 cd pipeline |
| Monitoring | `infrastructure/4-monitoring/` | at least 1 dashboard, at least 1 alert rule, slos.md |
| Runbooks | `runbooks/` | incident-response.md, at least 1 service runbook |
| Security | `security/` | baseline.md, compliance-checklist.md |

---

## Section 10: Ops Anti-Patterns (Evaluator Watch List)

The evaluator should flag these common ops anti-patterns when grading:

| Anti-Pattern | What It Looks Like | Impact | Score Penalty |
|-------------|-------------------|--------|---------------|
| **ClickOps** | Infrastructure provisioned through console clicks, not code | automation_coverage: -2 | Drop automation_coverage to max 2 |
| **Alert Fatigue** | Hundreds of alerts with no severity classification or runbook links | operational_readiness: -2 | Drop operational_readiness to max 2 |
| **Snowflake Servers** | Each environment configured differently, no IaC reproducibility | reliability_design: -2 | Drop reliability_design to max 2 |
| **Secrets in Code** | API keys, passwords, or tokens committed to version control | security_posture: -3 | Drop security_posture to max 1 |
| **Untested Backups** | Backups configured but restore never tested | reliability_design: -1 | Require restore test evidence |
| **Monitoring Gaps** | Only uptime monitored, no latency, error rate, or saturation metrics | operational_readiness: -1 | Require RED/USE metrics |
| **Manual Deployments** | Production deployments require SSH access and manual steps | automation_coverage: -1 | Flag as automation debt |
| **Overprovisioned Infrastructure** | Resources sized for peak with no auto-scaling or right-sizing | reliability_design: -1 | Flag as cost and efficiency risk |

---

## Section 11: GitOps Implementation

This section provides operational guidance for implementing GitOps practices. Use these templates when a sprint contract requires declarative infrastructure management with git as the source of truth.

### Reconciliation Loop

The GitOps reconciliation loop is a pull-based process where a controller continuously compares the desired state (declared in git) with the actual state (running in the cluster) and corrects any drift. This applies to both FluxCD and ArgoCD implementations.

**Reconciliation flow:**

1. **Observe**: Controller polls the git repository (or receives a webhook notification) for changes to manifests
2. **Compare**: Controller diffs the desired state from git against the actual state in the target cluster
3. **Act**: If drift is detected, controller applies the git-declared state to the cluster (create, update, or delete resources)
4. **Report**: Controller publishes sync status (Synced, OutOfSync, Degraded, Unknown) to its dashboard and alerting system
5. **Repeat**: Loop runs on a configurable interval (default: 3-5 minutes) or on git push events

| Phase | FluxCD Implementation | ArgoCD Implementation |
|-------|----------------------|----------------------|
| Observe | GitRepository custom resource with polling interval or webhook receiver | Application custom resource with repo URL and sync policy |
| Compare | Kustomize controller diffs rendered manifests against cluster | ArgoCD diff engine compares rendered manifests against live state |
| Act | Kustomize controller applies changes; Helm controller reconciles HelmReleases | ArgoCD sync operation applies changes (auto-sync or manual) |
| Report | Flux notification controller sends alerts to Slack, Teams, or webhook | ArgoCD notifications engine sends alerts to configured channels |
| Health check | Flux health checks on Kustomization and HelmRelease resources | ArgoCD resource health assessment (Healthy, Degraded, Progressing, Missing) |

### Directory Structure for GitOps Repos

Choose a repository strategy based on team size and environment count.

#### Mono-Repo vs Multi-Repo Comparison

| Factor | Mono-Repo | Multi-Repo |
|--------|-----------|------------|
| Structure | Single repo with directories per environment/service | Separate repo per environment or per team |
| Access control | Branch protection rules; path-based CODEOWNERS | Repo-level permissions; simpler access boundaries |
| Visibility | Full view of all environments in one place | Each team sees only their environments |
| Coordination | Easier cross-service changes (single PR) | Cross-service changes require multi-repo PRs |
| Scalability | Slows with many services (large repo, long CI) | Scales well; each repo stays small |
| Recommended for | Small-to-medium teams (under 10 services) | Large organizations, multi-team, strict isolation |

#### Recommended GitOps Repository Layout

```
gitops-repo/
  base/                              # Shared base manifests (DRY)
    service-a/
      deployment.yaml
      service.yaml
      configmap.yaml
      kustomization.yaml
    service-b/
      deployment.yaml
      service.yaml
      kustomization.yaml
  overlays/                          # Environment-specific patches
    dev/
      service-a/
        kustomization.yaml           # patches: [replica-count.yaml, dev-config.yaml]
        replica-count.yaml
        dev-config.yaml
      service-b/
        kustomization.yaml
    staging/
      service-a/
        kustomization.yaml
        staging-config.yaml
      service-b/
        kustomization.yaml
    production/
      service-a/
        kustomization.yaml
        production-config.yaml
        hpa.yaml                     # HorizontalPodAutoscaler for production only
      service-b/
        kustomization.yaml
  clusters/                          # Cluster-level bootstrap (Flux/Argo config)
    dev-cluster/
      flux-system/                   # Flux bootstrap or ArgoCD Application manifests
      sources.yaml
      kustomizations.yaml
    production-cluster/
      flux-system/
      sources.yaml
      kustomizations.yaml
```

### Drift Detection Workflow

Drift occurs when the actual cluster state diverges from the git-declared state (manual kubectl edits, operator side-effects, failed partial syncs). Use this procedure to detect and resolve drift.

**Drift detection procedure:**

1. **Scheduled scan**: Configure the GitOps controller to run a full reconciliation on a fixed interval (recommended: every 5 minutes for production, every 10 minutes for non-production)
2. **Alert on divergence**: When the controller reports OutOfSync status, emit an alert to the ops channel with:
   - Affected resource(s) and namespace
   - Summary of the diff (fields that changed)
   - Timestamp of last known sync
3. **Decision tree**:
   - Was the drift caused by a legitimate manual intervention (emergency hotfix)?
     - **Yes**: Commit the change to git to make git the source of truth again, then let the controller sync
     - **No**: Let the controller auto-remediate by reapplying the git-declared state
   - Is auto-remediation safe for this resource type?
     - **Stateless workloads (Deployments, Services)**: Auto-remediate (safe to reapply)
     - **Stateful resources (PVCs, databases, CRDs)**: Manual review required before remediation
4. **Post-drift action**: Log the drift event, root cause, and resolution in the ops incident log. If drift recurs on the same resource, investigate the root cause (operator conflict, missing RBAC, manual access patterns)

---

## Section 12: SRE Procedures

This section provides templates and formulas for Site Reliability Engineering practices. Use these when a sprint contract requires SLO definition, error budget tracking, or toil reduction deliverables.

### SLO/SLI Definition Template

Define one row per user journey. Each SLO must have a measurable SLI and a rolling measurement window.

| Service | User Journey | SLI Metric | SLI Measurement | SLO Target | Rolling Window | Error Budget |
|---------|-------------|-----------|-----------------|-----------|---------------|-------------|
| [Service name] | [User-facing action, e.g., "Load dashboard"] | Latency (p99) | 99th percentile response time measured at the load balancer | < 500ms | 30 days | [1 - SLO] |
| [Service name] | [User-facing action, e.g., "Submit order"] | Availability | Proportion of successful (non-5xx) responses out of total requests | 99.9% | 30 days | 0.1% |
| [Service name] | [User-facing action, e.g., "Search products"] | Throughput | Requests per second handled without queueing or shedding | >= 1000 rps | 30 days | N/A (threshold) |
| [Service name] | [User-facing action, e.g., "Upload file"] | Correctness | Proportion of responses returning expected data (validated by synthetic checks) | 99.99% | 30 days | 0.01% |

**SLI selection guidance:**
- **Latency**: Use for user-facing request/response flows. Measure at the closest point to the user (load balancer or edge).
- **Availability**: Use for any service where uptime matters. Measure as successful responses / total responses.
- **Throughput**: Use for batch or streaming systems where capacity matters more than individual response time.
- **Correctness**: Use for data pipelines or APIs where returning wrong data is worse than returning slowly.

### Error Budget Calculation

The error budget quantifies how much unreliability is permitted within the SLO window.

**Formula:**

```
Error Budget = 1 - SLO Target
```

**Examples:**
- 99.9% SLO = 0.1% error budget = 43.2 minutes of downtime per 30 days
- 99.95% SLO = 0.05% error budget = 21.6 minutes of downtime per 30 days
- 99.99% SLO = 0.01% error budget = 4.32 minutes of downtime per 30 days

**Burn rate** measures how fast the error budget is being consumed relative to the budget period.

```
Burn Rate = (Observed Error Rate) / (Error Budget Rate)
```

A burn rate of 1.0 means the budget will be fully consumed exactly at the end of the window. A burn rate above 1.0 means the budget will be exhausted before the window ends.

#### Burn-Rate Alerting Thresholds

| Alert Window | Burn Rate Threshold | Budget Consumed if Sustained | Recommended Action |
|-------------|--------------------|-----------------------------|-------------------|
| 1 hour | 14.4x | 2% of 30-day budget | Page on-call; immediate investigation |
| 6 hours | 6x | 5% of 30-day budget | Page on-call; investigate within 30 minutes |
| 24 hours | 3x | 10% of 30-day budget | Create ticket; investigate within 4 hours |
| 3 days | 1x | 10% of 30-day budget | Review in next planning; consider preventive action |

#### Error Budget Policy

Define escalation actions based on cumulative budget consumption.

| Budget Consumed | Status | Action |
|----------------|--------|--------|
| 0-50% | Healthy | Normal development velocity; ship features as planned |
| 50-75% | Caution | Slow feature releases; prioritize reliability improvements in next sprint |
| 75-100% | At Risk | Freeze non-critical deployments; dedicate engineering time to reliability |
| 100%+ | Exhausted | Full deployment freeze except reliability fixes; post-mortem required for any new incidents |

### Toil Reduction Tracking

Toil is manual, repetitive, automatable operational work that scales linearly with service size. Track toil to prioritize automation investments.

| Task | Frequency | Time per Occurrence | Monthly Total | Automatable | Automation Priority | Status |
|------|-----------|-------------------|---------------|-------------|-------------------|--------|
| [e.g., Certificate renewal] | [Monthly] | [30 min] | [30 min] | [Yes] | [High] | [Manual / Partially automated / Fully automated] |
| [e.g., Log rotation cleanup] | [Weekly] | [15 min] | [60 min] | [Yes] | [Medium] | [Manual / Partially automated / Fully automated] |

**Toil budget guidance (per Google SRE Book):** No team should spend more than 50% of its time on toil. If toil exceeds 50%, prioritize automation over feature work until toil drops below the threshold.

---

## Section 13: Runbook Template

Use this template for every operational runbook. Each runbook documents the response procedure for a specific alert or operational scenario. The goal is that any on-call engineer can follow the runbook without prior context.

### Runbook: [Alert Name / Scenario Name]

**Last updated:** [Date]
**Owner:** [Team or individual]
**Review cadence:** [Quarterly / after every incident that uses this runbook]

#### Trigger

| Field | Value |
|-------|-------|
| Alert name | [Name of the monitoring alert that triggers this runbook] |
| Alert condition | [Metric > threshold for duration, e.g., "HTTP 5xx rate > 1% for 5 minutes"] |
| Monitoring source | [Prometheus, Datadog, CloudWatch, PagerDuty, etc.] |
| Triggered by | [Automated alert / Manual escalation / Customer report] |

#### Impact

| Field | Value |
|-------|-------|
| Affected services | [List of services impacted] |
| User impact | [Description of what users experience, e.g., "Checkout flow returns 500 errors"] |
| Severity | [P0 / P1 / P2 / P3 / P4 -- reference Section 14 severity classification] |
| Business impact | [Revenue loss estimate, SLA breach risk, regulatory impact] |

#### Prerequisites

- [ ] Access to [monitoring dashboard URL]
- [ ] Access to [deployment tool / kubectl / cloud console]
- [ ] Credentials for [service account / database admin]
- [ ] Communication channel: [Slack channel / incident bridge]

#### Diagnostic Steps

1. Check the monitoring dashboard at [URL] to confirm the alert is active and identify the scope
2. Verify which instances or pods are affected: `[diagnostic command, e.g., kubectl get pods -n namespace]`
3. Check recent deployments: `[command to list recent deployments]`
4. Review application logs for errors: `[command to tail or search logs]`
5. Check dependent services for cascading failures: `[command or dashboard]`

#### Resolution Steps

1. If caused by a recent deployment:
   - Initiate rollback: `[rollback command]`
   - Verify service health after rollback: `[health check command]`
2. If caused by resource exhaustion:
   - Scale the affected service: `[scaling command]`
   - Monitor resource utilization until stable
3. If caused by a dependent service failure:
   - Activate circuit breaker or fallback: `[command or config change]`
   - Notify the dependent service team via [channel]
4. Verify resolution: confirm the alert clears and affected user journeys are functional

#### Escalation

| Condition | Escalate To | Contact Method | Response Expectation |
|-----------|------------|----------------|---------------------|
| No resolution within 15 minutes (P0/P1) | [Senior on-call / Team lead] | [PagerDuty / phone] | Immediate |
| Affecting multiple services | [Platform team] | [Slack channel] | Within 15 minutes |
| Customer-facing impact confirmed | [Engineering manager + Customer support] | [Incident bridge] | Within 30 minutes |
| Data loss suspected | [Database team + Security team] | [PagerDuty] | Immediate |

#### Rollback

| Field | Value |
|-------|-------|
| Rollback decision criteria | [When to rollback vs. forward-fix, e.g., "Rollback if not resolved within 15 min for P0"] |
| Rollback procedure | [Step-by-step rollback commands] |
| Rollback verification | [How to confirm rollback was successful] |
| Post-rollback actions | [Notify stakeholders, create follow-up ticket, schedule post-incident review] |

---

## Section 14: Incident Response

This section defines severity levels, response expectations, and the post-incident review process. Use these templates when a sprint contract requires incident management deliverables.

### Severity Classification

| Severity | Definition | Examples | Response Time | Update Cadence | Escalation Authority |
|----------|-----------|----------|---------------|---------------|---------------------|
| **P0 - Critical** | Complete service outage or data loss affecting all users; no workaround available | Production database down, authentication service unavailable, data corruption detected | 5 minutes | Every 15 minutes | VP of Engineering / CTO |
| **P1 - Major** | Significant degradation affecting a large percentage of users; limited workaround available | Payment processing failing for 50%+ of transactions, core API latency > 10x normal | 15 minutes | Every 30 minutes | Engineering Manager |
| **P2 - Moderate** | Partial service degradation affecting a subset of users; workaround available | Search returning stale results, file uploads failing for one region, non-critical feature unavailable | 1 hour | Every 2 hours | Team Lead |
| **P3 - Minor** | Minor issue with minimal user impact; workaround readily available | Cosmetic dashboard error, slow report generation, minor logging gap | 4 hours | Daily | On-call engineer |
| **P4 - Informational** | No current user impact; potential future issue or improvement opportunity | Elevated error rate on non-critical path, dependency deprecation warning, security advisory review | Next business day | Weekly | Team backlog |

### Incident Lifecycle

Each incident progresses through five phases. Define responsible roles, required actions, and exit criteria for each phase.

| Phase | Responsible Role | Required Actions | Exit Criteria |
|-------|-----------------|-----------------|---------------|
| **Detection** | Monitoring system / On-call engineer | Alert fires or customer report received; incident channel created; severity classified | Severity assigned, incident commander designated |
| **Triage** | Incident Commander | Assess scope and impact; assign investigation leads; establish communication cadence | Root cause hypothesis formed, affected components identified |
| **Mitigation** | Investigation Lead | Apply temporary fix to restore service (rollback, failover, traffic shift, feature flag disable) | User-facing impact eliminated or reduced to acceptable level |
| **Resolution** | Investigation Lead + Engineering Team | Implement permanent fix; deploy and verify; confirm monitoring shows normal levels | Service fully restored, monitoring confirms stability for 30+ minutes |
| **Post-Incident Review** | Incident Commander + All Responders | Conduct blameless review within 48 hours of resolution; document findings; assign action items | Post-incident review document published, action items tracked |

### Post-Incident Review Template

Conduct this review within 48 hours of incident resolution. The review is blameless -- it focuses on systems and processes, not individuals.

**Incident ID:** [INC-XXXX]
**Date:** [YYYY-MM-DD]
**Severity:** [P0-P4]
**Duration:** [Detection to Resolution]
**Incident Commander:** [Name]

#### Timeline

| Time (UTC) | Event | Actor |
|-----------|-------|-------|
| [HH:MM] | [Alert fired / Customer reported issue] | [Monitoring / Customer] |
| [HH:MM] | [Incident declared, commander assigned] | [On-call engineer] |
| [HH:MM] | [Root cause identified] | [Investigation lead] |
| [HH:MM] | [Mitigation applied] | [Engineer] |
| [HH:MM] | [Service fully restored] | [Engineer] |
| [HH:MM] | [Incident closed] | [Incident commander] |

#### Root Cause

[Clear, technical description of what caused the incident. Include the chain of events that led to user impact.]

#### Contributing Factors

- [Factor 1: e.g., "Missing alerting on connection pool exhaustion"]
- [Factor 2: e.g., "Deploy happened during peak traffic without canary phase"]
- [Factor 3: e.g., "Runbook for this scenario was outdated"]

#### Action Items

| ID | Action | Owner | Priority | Due Date | Status |
|----|--------|-------|----------|----------|--------|
| AI-01 | [Specific action to prevent recurrence] | [Team/Person] | [P0-P3] | [Date] | [Open/In Progress/Done] |
| AI-02 | [Specific action to improve detection] | [Team/Person] | [P0-P3] | [Date] | [Open/In Progress/Done] |
| AI-03 | [Specific action to improve response] | [Team/Person] | [P0-P3] | [Date] | [Open/In Progress/Done] |

#### Lessons Learned

- [What went well during the response]
- [What could be improved]
- [Process or tooling changes to adopt]

---

## Section 15: DORA Metrics

DORA (DevOps Research and Assessment) metrics measure software delivery performance. Use this section when a sprint contract requires delivery performance measurement or improvement tracking.

### Deployment Frequency

**Definition:** How often the organization deploys code to production.

**How to measure:** Count the number of successful deployments to the production environment per time period. Each deployment that delivers user-visible or operator-visible changes counts as one deployment. Rollbacks count separately.

**Data sources:** CI/CD pipeline logs, deployment tool API (ArgoCD sync events, Flux reconciliation events, GitHub Actions deployment workflow runs), release tag history.

| Classification | Threshold | Characteristics |
|---------------|-----------|-----------------|
| Elite | On-demand (multiple deploys per day) | Trunk-based development, automated testing, feature flags, zero-downtime deployments |
| High | Between once per day and once per week | Short-lived feature branches, automated CI/CD, staging validation |
| Medium | Between once per week and once per month | Sprint-based releases, manual QA gates, scheduled deployment windows |
| Low | Between once per month and once every six months | Long release cycles, heavy manual testing, change advisory board approval |

**Improvement guidance:** Reduce batch size of deployments, adopt trunk-based development, automate testing gates, implement feature flags to decouple deployment from release.

### Lead Time for Changes

**Definition:** The time from code commit to that code running successfully in production.

**How to measure:** For each production deployment, measure the elapsed time from the first commit included in the deployment to the moment the deployment is verified healthy in production. Report the median lead time over the measurement window.

**Data sources:** Git commit timestamps, CI/CD pipeline duration logs, deployment completion timestamps.

| Classification | Threshold | Characteristics |
|---------------|-----------|-----------------|
| Elite | Less than one hour | Automated pipeline from commit to production, minimal manual gates |
| High | Between one day and one week | Automated CI, manual approval for production deploy |
| Medium | Between one week and one month | Multi-stage approval, scheduled release trains |
| Low | Between one month and six months | Lengthy QA cycles, manual build and deploy processes |

**Improvement guidance:** Identify and eliminate manual steps in the delivery pipeline, parallelize test suites, implement automated security scanning in CI, reduce approval wait times.

### Change Failure Rate

**Definition:** The percentage of deployments to production that result in a degraded service (incident, rollback, hotfix, or patch) and require remediation.

**How to measure:** Divide the number of failed deployments (those causing incidents or requiring rollback/hotfix) by the total number of deployments in the measurement window. Express as a percentage.

```
Change Failure Rate = (Failed Deployments / Total Deployments) x 100%
```

**Data sources:** Incident tracking system (PagerDuty, Opsgenie, Jira incidents), deployment logs cross-referenced with incident timelines, rollback events.

| Classification | Threshold | Characteristics |
|---------------|-----------|-----------------|
| Elite | 0-5% | Comprehensive automated testing, canary deployments, feature flags, fast rollback |
| High | 5-10% | Good test coverage, staging validation, some manual verification |
| Medium | 10-15% | Moderate test coverage, limited pre-production validation |
| Low | 16-30% | Minimal automated testing, infrequent deployments with large batch sizes |

**Improvement guidance:** Increase automated test coverage (unit, integration, E2E), implement canary or blue-green deployments, reduce deployment batch size, add pre-production smoke tests.

### Mean Time to Restore (MTTR)

**Definition:** The time from when a production incident is detected to when service is fully restored for users.

**How to measure:** For each production incident, measure the elapsed time from detection (alert fired or customer report received) to resolution (service confirmed healthy and alert cleared). Report the median MTTR over the measurement window.

**Data sources:** Incident management system (PagerDuty, Opsgenie) timestamps for acknowledgment and resolution, monitoring system alert history.

| Classification | Threshold | Characteristics |
|---------------|-----------|-----------------|
| Elite | Less than one hour | Automated detection, well-practiced runbooks, one-click rollback, feature flag kill switches |
| High | Less than one day | Good monitoring, documented runbooks, tested rollback procedures |
| Medium | Between one day and one week | Partial monitoring, ad-hoc incident response, manual rollback |
| Low | Between one week and one month | Limited monitoring, no runbooks, manual investigation and recovery |

**Improvement guidance:** Improve monitoring coverage and alert quality, write and rehearse runbooks, implement automated rollback, conduct incident response drills, establish on-call rotations with escalation paths.

### DORA Metrics Summary Dashboard Template

Use this table to track all four metrics in a single view. Update monthly or per sprint.

| Metric | Current Value | Classification | Target | Trend (vs Prior Period) |
|--------|-------------|---------------|--------|------------------------|
| Deployment Frequency | [N per week] | [Elite/High/Medium/Low] | [target] | [Improving/Stable/Declining] |
| Lead Time for Changes | [N hours/days] | [Elite/High/Medium/Low] | [target] | [Improving/Stable/Declining] |
| Change Failure Rate | [N%] | [Elite/High/Medium/Low] | [target] | [Improving/Stable/Declining] |
| Mean Time to Restore | [N hours/days] | [Elite/High/Medium/Low] | [target] | [Improving/Stable/Declining] |
