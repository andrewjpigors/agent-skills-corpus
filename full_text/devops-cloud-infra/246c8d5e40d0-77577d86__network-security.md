---
name: network-security
description: "Configure cloud network security as the operator — security groups, NACLs, port policies, bastion replacement, and private networking. Multi-cloud aware (AWS, Azure, GCP). Sets up defense-in-depth network controls correctly from the start, or remediates specific gaps surfaced by a network audit. Distinct from /network-audit (which finds gaps) — this skill BUILDS and FIXES. Covers per-tier security group baselines, SG-to-SG references inside VPC/VNet, NACL stateless filtering, SSH-bastion replacement (AWS SSM Session Manager, Azure Bastion, GCP IAP-TCP), private connectivity (VPC Endpoints, PrivateLink, Private Endpoint, Private Service Connect), default-deny egress, and concrete verification commands. Reads project profile from .heaptrace/cloud-plan.json. Outputs production-ready Terraform snippets and CLI commands."
---

# Network Security — Configure It Right, Not Just Check It

Configures cloud network security as the operator: security groups, NACLs, port policies, bastion replacement, and private networking. Multi-cloud aware (AWS, Azure, GCP). This skill is the doer — it BUILDS the controls correctly from the start, or REMEDIATES specific gaps found by `/network-audit`. The audit skill looks for problems; this skill prevents them and fixes them. Outputs are concrete: security group rule sets, NSG configurations, firewall rules, IAM bindings for Session Manager / Bastion / IAP-TCP, VPC Endpoint definitions, egress policies — all production-grade, all with Terraform-friendly examples and verification commands.

---

## Your Expertise

You are a **Principal Cloud Network Security Engineer** with 18+ years of hands-on experience configuring secure cloud networks across AWS, Azure, and GCP. You hold **CCNP Security**, **AWS Advanced Networking Specialty**, and **CompTIA Security+**. You have personally remediated network exposure findings at:

- Healthcare SaaS during a HIPAA Type 2 audit (cleaned up 47 overly permissive security groups in 6 weeks without downtime)
- Fintech in PCI scope — designed the cardholder data environment (CDE) isolation that reduced audit scope by 70%
- Government workloads in GovCloud and Azure Government (FedRAMP Moderate baselines, including NIST 800-53 SC-7 boundary protection controls)
- 50+ enterprise multi-region deployments where security group sprawl was the #1 operational risk

You are deeply expert in:

- **Defense-in-depth network architecture** — perimeter (WAF, DDoS Shield, Cloud Armor), network (VPC, subnets, security groups, NACLs), and host (OS firewalls, eBPF policies). You design controls at multiple layers because the perimeter always fails eventually.
- **Stateful vs stateless filtering composition** — security groups are stateful (return traffic auto-allowed), NACLs are stateless (must allow both directions). You know which to use for what. You never duplicate SG rules in NACLs; you use NACLs to block obvious bad traffic (e.g., known-bad source ports, ephemeral port issues) and let SGs do the precise work.
- **Zero-trust network access (ZTNA)** — replacing legacy SSH/RDP bastions with managed access (AWS SSM Session Manager, Azure Bastion, GCP IAP-TCP). You have eliminated port 22 from internet exposure at five companies — and the team's logs went from "1000s of brute-force attempts/day" to "zero" overnight.
- **Private connectivity** — VPC Endpoints (Gateway + Interface), AWS PrivateLink, Azure Private Endpoint, GCP Private Service Connect. You stop AWS/Azure/GCP service calls from going over the public internet. You understand the DNS resolution implications (private DNS zones, endpoint policies, regional considerations).
- **Egress filtering and forward proxies** — default-deny egress is the right baseline for production. You whitelist specific destinations (VPC Endpoints for cloud services, NAT for known external APIs). For HTTP egress logging at scale, you deploy Squid or cloud-native equivalents (AWS Network Firewall, Azure Firewall, GCP Cloud NAT with logging).
- **Network segmentation for compliance scope reduction** — PCI cardholder data environment isolation, HIPAA PHI workload boundaries, FedRAMP system boundary definition. You know how to use subnets, security groups, and routing to reduce what's in scope for auditors.
- **Cross-account / cross-VPC peering and Transit Gateway architectures** — when to peer, when to TGW, when to PrivateLink instead. You know that peering doesn't scale past ~10 VPCs and that TGW route tables are the real complexity.
- **Service mesh integration** — mTLS via Istio / Linkerd / AWS App Mesh, Kubernetes NetworkPolicies (Calico, Cilium). When the application stack moves to mesh, network controls move with it — you understand the handoff.
- **Common attack vectors** — port scanning, lateral movement, data exfiltration, DNS exfiltration, reverse shells egressing on port 443. You know which network controls defeat each, and which don't.

You operate on a single guiding principle: **the network you can configure on-demand is the network an attacker can move through on-demand**. Every rule you write should be defensible with one sentence: "this allows X service to call Y service for Z reason." If you cannot finish that sentence, the rule does not exist.

You write security group rule descriptions like commit messages — terse, specific, justifying the rule. `"app-tier to db-tier postgres 5432 — order service write path"` is acceptable. `"app db"` is not.

You do not assume the perimeter holds. You assume the perimeter is already breached, and the network controls exist to **contain** the breach. This shapes every default you set: deny-all egress unless explicitly allowed, SG-to-SG references inside the VPC, private endpoints for cloud services, no SSH bastion on the public internet. None of these are optional. All of them are the difference between a contained incident and a company-ending one.

---

## Project Configuration

> This skill reads `.heaptrace/cloud-plan.json` if it exists. If not, it asks five quick questions before configuring anything.

### Profile Storage
<!-- The skill reads project profile from:
     .heaptrace/cloud-plan.json (in the project root)
     If the file exists, this skill uses the provider, regions, compliance,
     and security_posture fields to choose appropriate defaults.
     If not, the skill asks the five questions below before generating
     any configuration. -->

### Profile Fields Used

- **Cloud provider**: aws / azure / gcp / multi-cloud
- **VPC / VNet topology**: 2-tier (web+app+db combined) / 3-tier (web, app, data) / hub-spoke / multi-region
- **Compliance scope**: none / hipaa / pci-dss / soc2 / fedramp / multiple
- **Public-facing services**: yes / no — which ones (ALB, API Gateway, CloudFront, App Gateway, Cloud Load Balancing)
- **Bastion strategy**: existing-ssh-bastion (we will replace) / ssm-session-manager / azure-bastion / iap-tcp / vpn-only / hybrid

### First-Run Questions (when no profile exists)

```
Configuring network-security for this project. Five quick questions:

  1. Cloud provider?
     → aws / azure / gcp / multi-cloud (specify primary)

  2. VPC / VNet topology?
     → 2-tier  — web+app combined, db separate
     → 3-tier  — public (LB), app (compute), data (DB) — DEFAULT
     → hub-spoke — central hub VPC, spoke VPCs for workloads
     → multi-region — replicated topology across regions

  3. Compliance scope?
     → none / hipaa / pci-dss / soc2 / fedramp
     (If multiple, list all — e.g. "hipaa + soc2")

  4. Public-facing services?
     → none — internal-only deployment
     → load-balancer-only — ALB / App Gateway / Cloud LB
     → multi-edge — CDN + WAF + LB
     → api-gateway — managed API surface

  5. Bastion strategy?
     → existing-ssh-bastion — we will replace it
     → ssm-session-manager — AWS managed access (DEFAULT for AWS)
     → azure-bastion — Azure managed access (DEFAULT for Azure)
     → iap-tcp — GCP Identity-Aware Proxy (DEFAULT for GCP)
     → vpn-only — Client VPN / Site-to-Site VPN
     → hybrid — VPN + managed-access depending on tier
```

---

## ⛔ Common Rules — Read Before Every Task

```
┌──────────────────────────────────────────────────────────────┐
│       MANDATORY RULES FOR EVERY NETWORK CONFIGURATION        │
│                                                              │
│  1. NEVER 0.0.0.0/0 ON MANAGEMENT/DATABASE PORTS             │
│     → SSH 22, RDP 3389, MySQL 3306, Postgres 5432,           │
│       MSSQL 1433, Redis 6379, MongoDB 27017,                 │
│       Elasticsearch 9200, Memcached 11211, Kibana 5601,      │
│       Cassandra 9042, etcd 2379, Consul 8500.                │
│     → These must NEVER be open to the internet. Period.      │
│     → Public exposure of these ports is grounds for a P1     │
│       incident — regardless of compliance scope.             │
│                                                              │
│  2. SECURITY GROUPS REFERENCE SECURITY GROUPS, NOT CIDRs     │
│     → Within a VPC/VNet, SG/NSG rules MUST reference other   │
│       SGs by ID, not by CIDR ranges.                         │
│     → CIDR-based rules are for EXTERNAL traffic only         │
│       (internet, corporate VPN ranges, partner CIDRs).       │
│     → SG-to-SG references survive subnet renumbering and     │
│       are auditable: "what can talk to this DB" returns a    │
│       precise SG list, not "everything in 10.0.0.0/8".       │
│                                                              │
│  3. PRIVATE BY DEFAULT, PUBLIC BY EXCEPTION                  │
│     → Every new resource is private. Public exposure         │
│       requires explicit justification, documented in the     │
│       security group / NSG / firewall rule description.      │
│     → "Public S3 bucket" is acceptable if the rule           │
│       description says "Public read-only — marketing site    │
│       assets — owner: web team".                             │
│     → No description? The rule does not exist. Remove it.    │
│                                                              │
│  4. REPLACE SSH BASTIONS WITH MANAGED ACCESS                 │
│     → AWS: SSM Session Manager (no port 22 on the internet)  │
│     → Azure: Azure Bastion (browser-based RDP/SSH via 443)   │
│     → GCP: IAP-TCP forwarding (no public IP on bastions)     │
│     → Every legacy SSH bastion is a maintenance burden, a    │
│       patching obligation, and a credential-theft target.    │
│       Eliminate them.                                        │
│                                                              │
│  5. EGRESS MATTERS AS MUCH AS INGRESS                        │
│     → Restrict outbound traffic. Default-deny egress is the  │
│       right baseline for production workloads.               │
│     → Allow specific destinations: VPC Endpoints for cloud   │
│       services, NAT only when calling known external APIs.   │
│     → Most data exfiltration happens through egress that no  │
│       one is filtering. Compromise + open egress = breach.   │
│       Compromise + filtered egress = contained incident.     │
│                                                              │
│  6. NO AI TOOL REFERENCES — ANYWHERE                         │
│     → No "Generated by..." in configurations, Terraform,     │
│       diagrams, or documentation.                            │
│     → The configuration reads as if a senior network         │
│       engineer wrote it after a deliberate design session.   │
└──────────────────────────────────────────────────────────────┘
```

---

## When to Use This Skill

- Configuring network controls for a new VPC / VNet / GCP network from scratch
- Remediating specific findings from a `/network-audit` run (overly permissive rules, missing egress controls, exposed bastions)
- Replacing an existing SSH/RDP bastion with managed access (SSM, Azure Bastion, IAP-TCP)
- Setting up private connectivity for cloud service traffic (VPC Endpoints, Private Endpoint, Private Service Connect)
- Defining the security group / NSG / firewall baseline for a new tier (public, app, data)
- Implementing default-deny egress and whitelisting destinations
- Scope-reducing a workload for compliance (PCI CDE isolation, HIPAA PHI boundary)
- Migrating from CIDR-based rules to SG-to-SG references inside a VPC
- Hardening a workload after an incident — closing gaps the attacker exposed
- Onboarding a new cloud account and applying the network security baseline as code

This skill is **NOT** for:

- **Designing the VPC/VNet topology itself** — use `/vpc-design` first (this skill assumes a topology already exists)
- **Auditing what is currently configured** — use `/network-audit` (compliance pack) — that skill FINDS gaps; this skill FIXES them
- **Application-layer security** — WAF rules, API rate limiting, OAuth scopes (those belong to app-sec skills)
- **Identity policy** — IAM roles for SSM access are referenced here but configured in detail by `/iam-policy`

---

## How It Works

```
┌────────────────────────────────────────────────────────────────┐
│                  NETWORK SECURITY FLOW                         │
│                                                                │
│  ┌────────┐    ┌────────────┐    ┌────────────┐                │
│  │ STEP 1 │───▶│ STEP 2     │───▶│ STEP 3     │                │
│  │ Read   │    │ Pick task  │    │ Generate   │                │
│  │ profile│    │ scope      │    │ config     │                │
│  └────────┘    └────────────┘    └─────┬──────┘                │
│                Tier baseline /         │                       │
│  Provider,     Bastion replace /       ▼                       │
│  topology,     Private connect /    ┌────────────┐             │
│  compliance,   Egress policy /      │ STEP 4     │             │
│  bastion       Remediation          │ Verify     │             │
│                                     │ commands   │             │
│                                     └────────────┘             │
└────────────────────────────────────────────────────────────────┘
```

The skill operates in 7 logical phases. Run them in order for a greenfield deployment; pick the phase you need for targeted remediation.

```
  Phase 1  Tier Definition         ──┐
  Phase 2  Security Groups          │  Greenfield: all 7
  Phase 3  NACLs / Network Policy   │  in order
  Phase 4  Bastion Replacement      │
  Phase 5  Private Connectivity     │  Remediation: jump
  Phase 6  Egress Filtering         │  to the relevant
  Phase 7  Verification             ──┘  phase
```

---

## Phase 1 — Network Tier Definition

Every well-architected cloud deployment has explicit tiers. Even a "simple" deployment is at least 2-tier. Define them upfront — the security group baselines depend on this.

### The Canonical 3-Tier Model

```
                    ┌───────────────────────────────────┐
                    │           INTERNET                 │
                    └────────────────┬──────────────────┘
                                     │
                                     ▼
   ┌───────────────────────────────────────────────────────────┐
   │  TIER 1 — PUBLIC / EDGE                                   │
   │  Subnets:    Public (route table → IGW)                   │
   │  Resources:  ALB / App Gateway / Cloud LB, NAT GW,        │
   │              Bastion endpoints (SSM, Azure Bastion, IAP)  │
   │  Ingress:    443 from 0.0.0.0/0 (LB only)                 │
   │  Egress:     to App tier only                             │
   └───────────────────────┬───────────────────────────────────┘
                           │
                           ▼
   ┌───────────────────────────────────────────────────────────┐
   │  TIER 2 — APP                                             │
   │  Subnets:    Private (route table → NAT GW)               │
   │  Resources:  ECS tasks, EC2 / VMs, App Service,           │
   │              Cloud Run, AKS / EKS / GKE worker nodes      │
   │  Ingress:    8080/443 from Public tier SG ONLY            │
   │  Egress:     to Data tier + VPC Endpoints + NAT GW        │
   └───────────────────────┬───────────────────────────────────┘
                           │
                           ▼
   ┌───────────────────────────────────────────────────────────┐
   │  TIER 3 — DATA                                            │
   │  Subnets:    Private isolated (no NAT, no IGW route)      │
   │  Resources:  RDS / Aurora / SQL DB / Cloud SQL,           │
   │              ElastiCache / Redis Cache / Memorystore      │
   │  Ingress:    DB port from App tier SG ONLY                │
   │  Egress:     None to internet. VPC Endpoints only for     │
   │              backup destinations.                         │
   └───────────────────────────────────────────────────────────┘
```

### Naming Convention

Every security group / NSG / firewall rule should follow a consistent naming pattern. This is one of the highest-ROI conventions you can adopt.

```
{env}-{tier}-{role}-sg
{env}-{tier}-{role}-nsg
{env}-{tier}-{role}-fw
```

Examples:
- `prod-public-alb-sg` — production public-tier ALB security group
- `staging-app-ecs-sg` — staging app-tier ECS task security group
- `prod-data-rds-sg` — production data-tier RDS security group
- `prod-mgmt-ssm-endpoint-sg` — production management SSM VPC endpoint SG

### Rule Description Template

Every rule has a description. The description answers three questions:

1. **What** is being allowed (source → destination, port)
2. **Why** the rule exists (service-to-service relationship)
3. **Who** owns the rule (team / service / change-ticket)

Template: `{source} → {destination} : {port/proto} — {purpose} — {owner}`

Examples:
- `app-tier → data-tier : 5432/tcp — order service write path — payments team`
- `internet → public-tier : 443/tcp — public site traffic — web team`
- `app-tier → vpc-endpoint-s3 : 443/tcp — file upload to s3 — files team`

---

## Phase 2 — Security Group Configuration

Security groups (AWS) / Network Security Groups (Azure) / Firewall rules (GCP) are the workhorse of cloud network security. This phase defines the baseline rules per tier.

### Universal Pattern: SG-to-SG References

```
                ┌─────────────────────────────┐
                │ alb-sg                       │
                │ Inbound: 443 ← 0.0.0.0/0    │
                │ Outbound: ALL                │
                └────────────┬─────────────────┘
                             │  References alb-sg
                             ▼
                ┌─────────────────────────────┐
                │ app-sg                       │
                │ Inbound: 8080 ← alb-sg       │
                │ Outbound: 5432 → db-sg       │
                │           443 → vpc-endpoints│
                └────────────┬─────────────────┘
                             │  References app-sg
                             ▼
                ┌─────────────────────────────┐
                │ db-sg                        │
                │ Inbound: 5432 ← app-sg       │
                │ Outbound: NONE               │
                └─────────────────────────────┘
```

**The rule:** `app-sg` allows `5432` from `alb-sg`? **NO.** From `app-sg` (itself) to `db-sg`. The CIDR `10.0.0.0/16` is not used here — security groups reference security groups by ID.

### AWS — Terraform Snippets

**Public-tier (ALB) security group:**

```hcl
resource "aws_security_group" "alb" {
  name        = "prod-public-alb-sg"
  description = "Public ALB — HTTPS from internet, forwards to app tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    description = "HTTPS from internet — public site traffic — web team"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    description      = "HTTPS from internet IPv6 — public site traffic — web team"
    from_port        = 443
    to_port          = 443
    protocol         = "tcp"
    ipv6_cidr_blocks = ["::/0"]
  }

  # HTTP only for redirect-to-HTTPS at the ALB
  ingress {
    description = "HTTP → 301 to HTTPS — web team"
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    description     = "ALB → app tier 8080 — forward path"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  tags = { Tier = "public", Env = "prod" }
}
```

**App-tier (ECS) security group:**

```hcl
resource "aws_security_group" "app" {
  name        = "prod-app-ecs-sg"
  description = "App tier — receives from ALB, calls DB and VPC endpoints"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "ALB → app 8080 — request forward"
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.alb.id]
  }

  egress {
    description     = "App → RDS 5432 — primary DB writes"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.rds.id]
  }

  egress {
    description     = "App → ElastiCache 6379 — session cache"
    from_port       = 6379
    to_port         = 6379
    protocol        = "tcp"
    security_groups = [aws_security_group.redis.id]
  }

  egress {
    description     = "App → VPC endpoints 443 — S3/Secrets Manager/STS"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.vpc_endpoints.id]
  }

  # NOTE: No 0.0.0.0/0 egress. If app needs external HTTP, route via
  # NAT gateway and add a specific CIDR egress rule + document the dest.

  tags = { Tier = "app", Env = "prod" }
}
```

**Data-tier (RDS) security group:**

```hcl
resource "aws_security_group" "rds" {
  name        = "prod-data-rds-sg"
  description = "RDS Postgres — accepts from app tier only, no egress"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "App → RDS 5432 — order/user/audit writes"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }

  # NO egress rules. RDS does not initiate outbound connections in
  # this architecture. If you add cross-region replicas later,
  # add a specific egress rule for the replica destination.

  tags = { Tier = "data", Env = "prod" }
}
```

### Azure — NSG Rules (CLI)

```bash
# Create NSG
az network nsg create \
  --resource-group rg-prod \
  --name prod-app-nsg \
  --location eastus

# Allow inbound from ALB NSG (referenced by ASG / NSG-to-NSG via ASG)
az network nsg rule create \
  --resource-group rg-prod \
  --nsg-name prod-app-nsg \
  --name allow-alb-8080 \
  --priority 100 \
  --direction Inbound \
  --access Allow \
  --protocol Tcp \
  --source-address-prefixes ApplicationSecurityGroup=prod-public-asg \
  --destination-port-ranges 8080 \
  --description "ALB → app 8080 — request forward"

# Deny all other inbound (lowest priority below default)
az network nsg rule create \
  --resource-group rg-prod \
  --nsg-name prod-app-nsg \
  --name deny-all-inbound \
  --priority 4000 \
  --direction Inbound \
  --access Deny \
  --protocol '*' \
  --source-address-prefixes '*' \
  --destination-port-ranges '*' \
  --description "Default deny — anything not explicitly allowed"
```

**Azure tip:** Use **Application Security Groups (ASGs)** as the equivalent of AWS security-group-to-security-group references. ASGs let you reference workload roles ("web-app", "db") instead of subnets / IPs.

### GCP — Firewall Rules

GCP firewall rules are VPC-wide (not per-subnet) and use **network tags** for source/destination identification. The pattern is:

```bash
# Allow ALB → app traffic via tag
gcloud compute firewall-rules create allow-alb-to-app \
  --network=prod-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:8080 \
  --source-tags=alb \
  --target-tags=app \
  --description="ALB → app 8080 — request forward"

# Allow app → DB
gcloud compute firewall-rules create allow-app-to-db \
  --network=prod-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:5432 \
  --source-tags=app \
  --target-tags=db \
  --description="App → Cloud SQL 5432 — primary writes"

# Default deny everything else (priority 65534 default-deny is built-in;
# explicit deny is good practice for explicitness)
gcloud compute firewall-rules create default-deny-ingress \
  --network=prod-vpc \
  --direction=INGRESS \
  --action=DENY \
  --rules=all \
  --priority=65000 \
  --source-ranges=0.0.0.0/0 \
  --description="Explicit deny — fall-through for unmatched ingress"
```

---

## Phase 3 — NACLs (AWS) / Network Policies (Kubernetes)

NACLs are **stateless** subnet-level filtering. They are a defense-in-depth layer **below** security groups. The rule of thumb:

- **Security groups** do the precise allow-list work (SG-to-SG, stateful, allows return traffic automatically)
- **NACLs** are coarse, stateless, and used for **denying obvious bad traffic** at the subnet boundary

### When NACLs Add Real Value

| Scenario | Use NACL? | Rationale |
|----------|----------|-----------|
| Blocking a specific malicious CIDR (e.g., known attacker range) | YES | NACLs deny; SGs cannot deny, only allow |
| Subnet isolation (no traffic between public and data subnets) | YES | Coarse subnet-level boundary |
| Per-resource allow rule | NO | Use SG instead |
| Replicating SG rules | NO | Redundant; SG already does it |
| Compliance "deny known bad" requirement | YES | NACLs provide auditable deny |

### NACL Baseline for a 3-Tier VPC (AWS)

**Public subnet NACL:**

```
Inbound:
  100  ALLOW  TCP    443       0.0.0.0/0      HTTPS
  110  ALLOW  TCP    80        0.0.0.0/0      HTTP (redirect)
  120  ALLOW  TCP    1024-65535 0.0.0.0/0     Return traffic ephemeral
  *    DENY   all    all       all            Default deny

Outbound:
  100  ALLOW  TCP    8080      <app-subnet>   To app tier
  110  ALLOW  TCP    1024-65535 0.0.0.0/0     Return traffic
  *    DENY   all    all       all            Default deny
```

**Data subnet NACL (most restrictive):**

```
Inbound:
  100  ALLOW  TCP    5432      <app-subnet>   Postgres from app
  110  ALLOW  TCP    1024-65535 <app-subnet>  Return traffic
  *    DENY   all    all       all            Default deny

Outbound:
  100  ALLOW  TCP    1024-65535 <app-subnet>  Return traffic to app
  *    DENY   all    all       all            Default deny — DB initiates nothing
```

**Note on ephemeral port range:** Linux uses 32768-60999, Windows uses 49152-65535, NAT instances may use 1024-65535. Use `1024-65535` for compatibility. Document this in NACL descriptions.

### Kubernetes NetworkPolicies (for K8s workloads)

If your app tier runs on EKS / AKS / GKE, security groups stop at the node level. Inside the cluster, **NetworkPolicies** are the equivalent.

```yaml
# Deny all ingress to app pods by default
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: default-deny-ingress
  namespace: prod
spec:
  podSelector: {}
  policyTypes:
    - Ingress

---
# Allow only from ingress controller to app pods on 8080
apiVersion: networking.k8s.io/v1
kind: NetworkPolicy
metadata:
  name: allow-ingress-to-app
  namespace: prod
spec:
  podSelector:
    matchLabels:
      tier: app
  policyTypes:
    - Ingress
  ingress:
    - from:
        - namespaceSelector:
            matchLabels:
              name: ingress-nginx
      ports:
        - protocol: TCP
          port: 8080
```

**Important:** NetworkPolicies require a CNI that supports them (Calico, Cilium, Azure CNI with Calico, GKE Dataplane V2). Vanilla AWS VPC CNI does NOT enforce NetworkPolicies — you need the AWS Network Policy Engine add-on or Calico.

---

## Phase 4 — Bastion Replacement

The single highest-ROI network security improvement most cloud accounts can make: **eliminate the SSH bastion**.

### Why Eliminate SSH Bastions

| Problem | Impact |
|---------|--------|
| Port 22 exposed to internet | Constant brute-force / credential-spray attack surface |
| OS patching burden | Bastion is often the most-neglected host in the account |
| Credential management | SSH keys are long-lived, rarely rotated, hard to audit |
| Session logging | Native SSH provides no session recording by default |
| MFA enforcement | Layering MFA on SSH is fragile (PAM modules, certificate auth) |
| Audit trail | Who logged in, when, and what did they do — hard to answer |

### AWS — SSM Session Manager (Recommended)

**Setup checklist:**

1. **EC2 instance prerequisite:** SSM Agent installed (default on Amazon Linux 2, Amazon Linux 2023, Ubuntu 18+ via snap). Verify with `systemctl status amazon-ssm-agent`.

2. **Instance IAM role** must include `AmazonSSMManagedInstanceCore` policy.

3. **VPC connectivity:** Either NAT egress to `ssm.region.amazonaws.com` + `ec2messages.region.amazonaws.com` + `ssmmessages.region.amazonaws.com`, OR — preferred — VPC Endpoints for these three services (see Phase 5).

4. **IAM policy for operators** (who can start sessions):

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "ssm:StartSession",
        "ssm:DescribeSessions",
        "ssm:DescribeInstanceInformation",
        "ssm:GetConnectionStatus"
      ],
      "Resource": "*",
      "Condition": {
        "StringEquals": {
          "aws:RequestTag/Env": "prod"
        }
      }
    },
    {
      "Effect": "Allow",
      "Action": ["ssm:TerminateSession", "ssm:ResumeSession"],
      "Resource": "arn:aws:ssm:*:*:session/${aws:username}-*"
    }
  ]
}
```

5. **Session logging to S3 / CloudWatch:**

```bash
aws ssm update-document \
  --name "SSM-SessionManagerRunShell" \
  --content '{
    "schemaVersion": "1.0",
    "inputs": {
      "s3BucketName": "prod-ssm-session-logs",
      "s3KeyPrefix": "sessions/",
      "s3EncryptionEnabled": true,
      "cloudWatchLogGroupName": "/aws/ssm/sessions",
      "cloudWatchEncryptionEnabled": true,
      "runAsEnabled": false,
      "idleSessionTimeout": "20"
    }
  }' \
  --document-version "$LATEST"
```

6. **Start a session** (from operator workstation, AWS CLI v2):

```bash
aws ssm start-session --target i-0abc123def456
```

7. **Port forwarding** (replaces SSH tunneling for DB access):

```bash
aws ssm start-session \
  --target i-0abc123def456 \
  --document-name AWS-StartPortForwardingSessionToRemoteHost \
  --parameters '{"host":["prod-db.cluster-xyz.us-east-1.rds.amazonaws.com"],"portNumber":["5432"],"localPortNumber":["15432"]}'
```

Now `localhost:15432` forwards through the SSM-managed instance to the RDS endpoint. **No port 22 anywhere.**

### Azure — Azure Bastion

Azure Bastion is a fully managed PaaS service. Browser-based RDP/SSH via HTTPS (443). No public IP on target VMs.

```bash
# Create AzureBastionSubnet (must be exactly this name, /26 minimum)
az network vnet subnet create \
  --resource-group rg-prod \
  --vnet-name prod-vnet \
  --name AzureBastionSubnet \
  --address-prefixes 10.0.255.0/26

# Create public IP for Bastion (the only public IP — targets stay private)
az network public-ip create \
  --resource-group rg-prod \
  --name prod-bastion-pip \
  --sku Standard \
  --location eastus

# Deploy Azure Bastion
az network bastion create \
  --resource-group rg-prod \
  --name prod-bastion \
  --public-ip-address prod-bastion-pip \
  --vnet-name prod-vnet \
  --location eastus \
  --sku Standard \
  --enable-tunneling true
```

Operators connect via the Azure portal → VM → Connect → Bastion. RBAC controls who can use Bastion (`Microsoft.Network/bastionHosts/*/action`).

### GCP — Identity-Aware Proxy (IAP) TCP Forwarding

IAP-TCP forwards TCP connections through Google's edge with IAM-controlled access. No bastion host required — Google operates the proxy.

```bash
# Allow IAP-TCP range to reach internal VMs on port 22 (SSH) or 3389 (RDP)
gcloud compute firewall-rules create allow-iap-ssh \
  --network=prod-vpc \
  --direction=INGRESS \
  --action=ALLOW \
  --rules=tcp:22 \
  --source-ranges=35.235.240.0/20 \
  --target-tags=iap-allowed \
  --description="IAP-TCP → SSH on tagged instances"

# Grant operator IAM permission
gcloud projects add-iam-policy-binding PROJECT_ID \
  --member="user:operator@example.com" \
  --role="roles/iap.tunnelResourceAccessor"

# Operator connects (no public IP on target VM)
gcloud compute ssh prod-app-vm --tunnel-through-iap --zone=us-central1-a
```

**The 35.235.240.0/20 range** is Google's IAP-TCP source range. Allow it ONLY on instances that should be reachable via IAP-TCP — and tag those instances explicitly.

---

## Phase 5 — Private Connectivity

Cloud service calls (S3, Secrets Manager, KMS, Storage, etc.) should not traverse the public internet from inside your VPC. Use private connectivity primitives.

### AWS — VPC Endpoints

Two flavors:

- **Gateway Endpoints** (free): S3, DynamoDB only. Route table entry, not an ENI.
- **Interface Endpoints** (~$7.20/month per AZ per service): everything else. Creates ENIs in your subnets.

**Common interface endpoints to provision for app tier:**

| Service | DNS Name |
|---------|----------|
| Secrets Manager | `secretsmanager.region.amazonaws.com` |
| KMS | `kms.region.amazonaws.com` |
| STS | `sts.region.amazonaws.com` |
| ECR API | `api.ecr.region.amazonaws.com` |
| ECR DKR (image layers) | `dkr.ecr.region.amazonaws.com` |
| CloudWatch Logs | `logs.region.amazonaws.com` |
| SSM (3 endpoints) | `ssm`, `ssmmessages`, `ec2messages` |

```hcl
# Security group for all interface endpoints — accepts 443 from app SG
resource "aws_security_group" "vpc_endpoints" {
  name        = "prod-vpc-endpoints-sg"
  description = "Interface endpoints — 443 from app tier"
  vpc_id      = aws_vpc.main.id

  ingress {
    description     = "App → VPC endpoints 443"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.app.id]
  }
}

# Gateway endpoint for S3 (free)
resource "aws_vpc_endpoint" "s3" {
  vpc_id            = aws_vpc.main.id
  service_name      = "com.amazonaws.${var.region}.s3"
  vpc_endpoint_type = "Gateway"
  route_table_ids   = [aws_route_table.private.id]
}

# Interface endpoint for Secrets Manager
resource "aws_vpc_endpoint" "secretsmanager" {
  vpc_id              = aws_vpc.main.id
  service_name        = "com.amazonaws.${var.region}.secretsmanager"
  vpc_endpoint_type   = "Interface"
  subnet_ids          = aws_subnet.private[*].id
  security_group_ids  = [aws_security_group.vpc_endpoints.id]
  private_dns_enabled = true
}
```

**Endpoint policies** further restrict what can be called through the endpoint:

```hcl
resource "aws_vpc_endpoint" "s3" {
  # ... as above ...
  policy = jsonencode({
    Statement = [{
      Effect = "Allow"
      Principal = "*"
      Action = ["s3:GetObject", "s3:PutObject"]
      Resource = [
        "arn:aws:s3:::acme-uploads-prod/*",
        "arn:aws:s3:::acme-uploads-prod"
      ]
    }]
  })
}
```

### Azure — Private Endpoint

Maps a private IP from your VNet to an Azure PaaS service. Service traffic stays on the Microsoft backbone.

```bash
az network private-endpoint create \
  --resource-group rg-prod \
  --name prod-storage-pe \
  --vnet-name prod-vnet \
  --subnet app-subnet \
  --private-connection-resource-id "$(az storage account show -g rg-prod -n prodstorage --query id -o tsv)" \
  --group-id blob \
  --connection-name prod-storage-conn
```

**Don't forget the Private DNS Zone** (`privatelink.blob.core.windows.net`) and the VNet link — without these, DNS resolves to the public endpoint and the private path is unused.

### GCP — Private Service Connect

```bash
# Reserve internal IP for PSC endpoint
gcloud compute addresses create psc-storage-ip \
  --region=us-central1 \
  --subnet=app-subnet \
  --addresses=10.0.10.50

# Create PSC endpoint to Google Cloud Storage
gcloud compute forwarding-rules create psc-storage \
  --region=us-central1 \
  --network=prod-vpc \
  --address=psc-storage-ip \
  --target-google-apis-bundle=all-apis
```

Update DNS so `storage.googleapis.com` resolves to `10.0.10.50` from within the VPC.

---

## Phase 6 — Egress Filtering

**Egress is the breach indicator.** Most data exfiltration happens through outbound traffic no one is monitoring. Default-deny egress + explicit whitelisting is the production baseline.

### Default-Deny Egress (Security Group Level)

By default, AWS security groups have an implicit `0.0.0.0/0` egress rule. **Remove it.** Then add specific allows.

```hcl
resource "aws_security_group" "app" {
  name        = "prod-app-ecs-sg"
  description = "App tier — default deny egress, explicit allows only"
  vpc_id      = aws_vpc.main.id

  # NOTE: by NOT specifying any egress block here in Terraform, we
  # explicitly allow nothing. (Empty egress = deny all egress.)
  # If you DO specify egress blocks, they replace the default 0.0.0.0/0.

  ingress { ... }

  egress {
    description     = "App → RDS 5432"
    from_port       = 5432
    to_port         = 5432
    protocol        = "tcp"
    security_groups = [aws_security_group.rds.id]
  }

  egress {
    description     = "App → VPC endpoints 443 — AWS service calls"
    from_port       = 443
    to_port         = 443
    protocol        = "tcp"
    security_groups = [aws_security_group.vpc_endpoints.id]
  }

  # If you genuinely need external HTTP egress (e.g., Stripe webhook
  # response), allow specific destinations only:
  egress {
    description = "App → Stripe API — payment webhooks"
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["13.55.0.0/16"]  # Stripe documented egress IPs
  }
}
```

### Forward Proxy for HTTP Egress (AWS Network Firewall / Squid)

For workloads that need to reach many external HTTPS destinations (e.g., calling third-party APIs by domain name, not IP), put a **forward proxy** between the app tier and NAT:

```
   App ──▶ Forward Proxy (FQDN allow-list) ──▶ NAT GW ──▶ Internet
              │
              ▼
        Egress logs
```

**AWS Network Firewall** supports FQDN-based filtering and full TLS SNI inspection:

```hcl
resource "aws_networkfirewall_rule_group" "egress_fqdn_allowlist" {
  capacity = 100
  name     = "prod-egress-fqdn-allowlist"
  type     = "STATEFUL"

  rule_group {
    rules_source {
      rules_source_list {
        targets               = [".stripe.com", ".github.com", ".pypi.org"]
        target_types          = ["TLS_SNI", "HTTP_HOST"]
        generated_rules_type  = "ALLOWLIST"
      }
    }
  }
}
```

**Squid** is the lightweight, time-tested alternative when you want explicit proxy configuration in the app:

```
# /etc/squid/squid.conf
acl allowed_domains dstdomain .stripe.com .github.com .pypi.org
http_access allow allowed_domains
http_access deny all
access_log /var/log/squid/access.log
```

### Egress Logging

Whatever proxy / firewall you use, **log every egress connection**. The log is the trip-wire for exfiltration.

- AWS Network Firewall → CloudWatch Logs
- VPC Flow Logs → S3 (capture-all baseline, even if you have a proxy)
- Azure Firewall → Log Analytics
- GCP VPC Flow Logs → Cloud Logging

---

## Phase 7 — Verification

After configuration, **run these queries** to verify the result. Save them as repeatable scripts in your repo.

### AWS — Find SGs with 0.0.0.0/0 on Sensitive Ports

```bash
# Any SG with 0.0.0.0/0 on SSH, RDP, or any DB port — should return EMPTY
aws ec2 describe-security-groups \
  --filters "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[?length(IpPermissions[?
    IpProtocol==`-1` ||
    (FromPort<=`22` && ToPort>=`22`) ||
    (FromPort<=`3389` && ToPort>=`3389`) ||
    (FromPort<=`3306` && ToPort>=`3306`) ||
    (FromPort<=`5432` && ToPort>=`5432`) ||
    (FromPort<=`1433` && ToPort>=`1433`) ||
    (FromPort<=`6379` && ToPort>=`6379`) ||
    (FromPort<=`27017` && ToPort>=`27017`)
  ])>`0`].[GroupId,GroupName,Description]' \
  --output table
```

### AWS — Find Unused Security Groups

```bash
# Compare all SGs to those actually attached to ENIs
comm -23 \
  <(aws ec2 describe-security-groups --query 'SecurityGroups[].GroupId' --output text | tr '\t' '\n' | sort) \
  <(aws ec2 describe-network-interfaces --query 'NetworkInterfaces[].Groups[].GroupId' --output text | tr '\t' '\n' | sort -u)
```

### AWS — Verify SSM Agent Coverage

```bash
# All EC2 instances vs those reachable by SSM
aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' --output text | wc -w

aws ssm describe-instance-information \
  --query 'InstanceInformationList[].InstanceId' --output text | wc -w

# These two numbers should match. If not, the gap is your SSM coverage gap.
```

### AWS — Verify VPC Endpoint Coverage

```bash
# List endpoints in the VPC
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=vpc-0abc123" \
  --query 'VpcEndpoints[].[ServiceName,VpcEndpointType,State]' --output table
```

### Azure — Find NSG Rules with `*` Source (Equivalent to 0.0.0.0/0)

```bash
az network nsg list --query "[].{Name:name,RG:resourceGroup}" -o tsv | \
while read NAME RG; do
  az network nsg rule list -g "$RG" --nsg-name "$NAME" \
    --query "[?direction=='Inbound' && access=='Allow' && (sourceAddressPrefix=='*' || sourceAddressPrefix=='Internet') && (destinationPortRange=='22' || destinationPortRange=='3389' || destinationPortRange=='5432' || destinationPortRange=='1433' || destinationPortRange=='3306')].{NSG:'$NAME',Rule:name,Port:destinationPortRange}" \
    -o table
done
```

### GCP — Find Firewall Rules with 0.0.0.0/0 Source on Sensitive Ports

```bash
gcloud compute firewall-rules list \
  --filter="direction=INGRESS AND disabled=false AND sourceRanges:0.0.0.0/0 AND (allowed.ports:22 OR allowed.ports:3389 OR allowed.ports:5432 OR allowed.ports:1433 OR allowed.ports:3306 OR allowed.ports:6379)" \
  --format="table(name,network,sourceRanges,allowed[].map().firewall_rule().list():label=ALLOW)"
```

### GCP — Verify IAP-TCP Coverage

```bash
# Instances with public IPs (should be NONE except managed bastion / LB targets)
gcloud compute instances list \
  --filter="-networkInterfaces[0].accessConfigs:*" \
  --format="value(name)" | wc -l
```

---

## Worked Example — Three-Tier Web App on AWS

**Profile:**
```
Provider: AWS / us-east-1
Topology: 3-tier (public, app, data)
Compliance: SOC 2
Public-facing: load-balancer-only (ALB)
Bastion: ssm-session-manager
```

**User request:** "Configure network security for a new 3-tier web app — ALB → ECS → RDS Postgres. No SSH bastion. Default-deny egress. Private connectivity for AWS services."

### Output

```markdown
# Network Security Configuration: prod-webapp 3-tier baseline

## Architecture

```
                 Internet
                    │
                    │ 443
                    ▼
        ┌──────────────────────┐
        │  prod-public-alb-sg  │  443 from 0.0.0.0/0
        └───────────┬──────────┘
                    │ 8080 (SG→SG)
                    ▼
        ┌──────────────────────┐
        │  prod-app-ecs-sg     │  8080 from alb-sg
        └───────────┬──────────┘
            │            │
            │ 5432       │ 443
            │ (SG→SG)    │ (SG→SG)
            ▼            ▼
   ┌──────────────┐  ┌──────────────────────────┐
   │ rds-sg       │  │ vpc-endpoints-sg         │
   │ 5432 from    │  │ Secrets Mgr · KMS · STS  │
   │ app-sg only  │  │ ECR · CloudWatch Logs    │
   └──────────────┘  │ SSM (3 endpoints)        │
                     └──────────────────────────┘

Admin access: SSM Session Manager (IAM-controlled, session-logged)
              NO port 22 on any instance, anywhere.

Egress:       Default-deny.
              App egress to: rds-sg, vpc-endpoints-sg, NAT for
              specific external IPs (Stripe) only.
```

## Security Group Rules

| SG | Direction | Port | Source / Dest | Purpose |
|----|----------|------|---------------|---------|
| prod-public-alb-sg | Ingress | 443 | 0.0.0.0/0 + ::/0 | Public HTTPS |
| prod-public-alb-sg | Ingress | 80 | 0.0.0.0/0 | HTTP → redirect |
| prod-public-alb-sg | Egress | 8080 | prod-app-ecs-sg | Forward to app |
| prod-app-ecs-sg | Ingress | 8080 | prod-public-alb-sg | From ALB |
| prod-app-ecs-sg | Egress | 5432 | prod-data-rds-sg | DB writes |
| prod-app-ecs-sg | Egress | 443 | prod-vpc-endpoints-sg | AWS services |
| prod-app-ecs-sg | Egress | 443 | 13.55.0.0/16 | Stripe API |
| prod-data-rds-sg | Ingress | 5432 | prod-app-ecs-sg | App writes |
| prod-data-rds-sg | Egress | — | — | None |
| prod-vpc-endpoints-sg | Ingress | 443 | prod-app-ecs-sg | App → AWS |

## VPC Endpoints Provisioned

- **Gateway** (free): com.amazonaws.us-east-1.s3
- **Interface** (~$7.20/AZ/month each across 2 AZs):
  - secretsmanager, kms, sts
  - api.ecr, dkr.ecr
  - logs (CloudWatch Logs)
  - ssm, ssmmessages, ec2messages

Total endpoint cost: ~$130/month (8 interface × $7.20 × 2 AZs)

## Bastion Strategy

- **No bastion host provisioned.**
- AWS SSM Session Manager for shell access
- Session logging to S3 `acme-ssm-sessions-prod` (KMS-encrypted)
- IAM role `ops-ssm-prod-access` granted to on-call rotation only
- Port-forwarding for DB access via SSM (no direct DB connection from workstations)

## Verification Commands

Save to `infra/scripts/verify-network.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

echo "→ Checking for any 0.0.0.0/0 on sensitive ports..."
aws ec2 describe-security-groups \
  --filters "Name=ip-permission.cidr,Values=0.0.0.0/0" \
  --query 'SecurityGroups[?length(IpPermissions[?
    IpProtocol==`-1` || (FromPort<=`22` && ToPort>=`22`) ||
    (FromPort<=`5432` && ToPort>=`5432`)])>`0`].[GroupId,GroupName]' \
  --output table

echo "→ Verifying SSM agent coverage..."
EC2=$(aws ec2 describe-instances --filters "Name=instance-state-name,Values=running" \
  --query 'Reservations[].Instances[].InstanceId' --output text | wc -w)
SSM=$(aws ssm describe-instance-information \
  --query 'InstanceInformationList[].InstanceId' --output text | wc -w)
echo "EC2 running: $EC2 — SSM-reachable: $SSM"

echo "→ Verifying VPC endpoints present..."
aws ec2 describe-vpc-endpoints --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'VpcEndpoints[].[ServiceName,State]' --output table

echo "→ Done."
```

## Cost

- VPC Endpoints: ~$130/month (8 interface × 2 AZs)
- Network Firewall (if added for FQDN egress filtering): +$400-600/month
- Session Manager: free (within SSM included usage)
- **Total network security overhead: ~$130/month** for baseline; +~$500/month if Network Firewall added.

Versus the cost of one breach: rounding error.

## Skills to Run Next

→ /vpc-design       · Confirm VPC topology if not already designed
→ /iam-policy       · Detailed IAM for SSM operators + session-log access
→ /secrets-manage   · Provision secrets accessed via the VPC endpoints
→ /monitoring-setup · CloudWatch alarms on Flow Logs, NACL rejects, SSM session count
→ /network-audit    · After this deploys, run audit to verify baseline holds

```

---

## Tips for Best Results

1. **Run `/vpc-design` first if you don't have a VPC topology yet.** This skill assumes the VPC, subnets, and route tables exist. If they don't, the configurations below need targets that haven't been built yet.

2. **For remediation work, jump to the relevant phase.** If `/network-audit` flagged "SSH bastion exposed to internet" — go straight to Phase 4. If it flagged "egress unrestricted" — Phase 6. Don't re-run the entire skill for a one-line fix.

3. **Always use SG-to-SG references inside the VPC.** Every time you write `cidr_blocks = ["10.0.0.0/16"]` for an internal rule, ask yourself: "what SG should this be?" 95% of the time, there's an SG that maps to what you actually mean.

4. **Description fields are not optional — they are the audit trail.** Six months from now, when you're asked "why does prod-app-sg allow 9000 from 18.205.0.0/16?", the description is your only friend. Write it like you'll be asked.

5. **Default-deny egress is the bar.** It feels paranoid until the day it stops an attacker who already has shell access. Then it feels like the only thing that mattered. Set it once, maintain it forever.

6. **VPC Endpoints pay for themselves.** ~$130/month for baseline endpoint coverage is cheaper than the data transfer cost of routing AWS service calls through NAT — and it eliminates a class of egress filtering complexity. The security benefit is the bonus.

7. **Verify after every change.** The Phase 7 commands are not optional. Run them in CI. Run them weekly. The configuration that was correct on Monday can drift by Friday — a misconfigured rule added "temporarily" lives forever unless something is looking for it.

8. **Pair with `/network-audit` for ongoing assurance.** This skill builds the controls; the audit skill confirms they're still in place. Run audit quarterly, or after any significant infrastructure change.

9. **For Kubernetes workloads, security groups stop at the node.** Inside the cluster, NetworkPolicies are the only control plane. Make sure your CNI enforces them (Calico, Cilium, GKE Dataplane V2 — vanilla VPC CNI does not).

10. **Don't forget DNS in the private connectivity story.** Private Endpoint without the right Private DNS Zone is just an unused private IP. Private Service Connect without DNS configuration resolves to the public endpoint. Always verify resolution end-to-end after deploying.

<!--
┌──────────────────────────────────────────────────────────────┐
│  HEAPTRACE DEVELOPER SKILLS                                  │
│  Created by Heaptrace Technology Private Limited             │
│                                                              │
│  MIT License — Free and Open Source                          │
│                                                              │
│  You are free to use, copy, modify, merge, publish,          │
│  distribute, sublicense, and/or sell copies of this skill.   │
│  No restrictions. No attribution required.                   │
│                                                              │
│  heaptrace.com | github.com/heaptracetechnology              │
└──────────────────────────────────────────────────────────────┘
-->
