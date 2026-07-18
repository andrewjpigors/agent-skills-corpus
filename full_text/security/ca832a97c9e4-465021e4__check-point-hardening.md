---
name: check-point-hardening
description: "Assess, report, and prepare remediation for Check Point Security Gateway and Management Server hardening (R81.20, R82, R82.10) using the Check Point MCP servers. Grounds guidance in official documentation, collects read-only evidence, and produces compliance reports plus out-of-band remediation artifacts (mgmt_cli, Gaia clish, Gaia API, SmartConsole runbooks). WHEN: \"create a hardening report\", \"check my Check Point environment\", \"harden this gateway\", \"harden the management server\", Gaia OS hardening, stealth rule, implied rules, management access restrictions, SmartConsole trusted clients, administrator MFA, password policy, Expert mode, SNMP hardening, dynamic routing (BGP/OSPF) security, Jumbo Hotfix, AutoUpdater, cpdiag, LOM/out-of-band management, syslog/SIEM forwarding, compliance evidence, gw-cli MCP hardening checks, hardening checklist. DO NOT USE FOR: non-Check Point firewalls or general cloud hardening."
license: MIT
metadata:
  author: Christian Sandberg
  version: "1.0.0"
  variant: full
---

# Check Point Gateway and Management Hardening Skill

## Purpose

This skill enables an AI assistant to assess, report, and remediate the hardening posture of Check Point Security Gateways and Management Servers. It combines official Check Point documentation guidance with live-environment evidence collected through available Check Point MCP servers to produce compliance reports, evidence packages, remediation plans, and safe implementation scripts.

The skill covers these hardening domains:

- Security Gateway exposure reduction via Access Control policy
- Management-plane protection and network segmentation
- Administrator identity and access control (MFA, trusted clients, roles)
- Third-party integration credential hardening
- Software updates, Jumbo Hotfix, AutoUpdater, and health checks
- Gaia OS hardening (services, users, password policy, SSH)
- Dynamic routing hardening (BGP, OSPF authentication and filtering)
- SNMPv3 migration and manager restrictions
- Expert mode governance and shell restrictions
- Gateway system logging to Management Server
- Management Server syslog/SIEM forwarding
- Lights Out Management (LOM) / out-of-band management restrictions
- Advanced hardening for high-security environments
- Deployment checklists
- Evidence collection and compliance reporting
- Safe remediation planning and script/API generation

## Activation Criteria

Activate when the user asks about:

- Check Point hardening, Gateway hardening, Management Server hardening, Gaia OS hardening
- R82.10, R82, R81.20 hardening
- Security Gateway stealth rules, implied rules hardening
- Management access restrictions, SmartConsole trusted clients
- Administrator MFA, IdP integration, unused accounts, password policy
- Expert mode, SNMP hardening, dynamic routing security
- cpdiag, AutoUpdater, Jumbo Hotfix Accumulator
- LOM / out-of-band management
- Syslog / SIEM forwarding
- Compliance report generation, remediation scripts
- mgmt_cli hardening changes, Gaia clish hardening commands
- gw-cli MCP hardening checks, gateway CLI evidence
- Hardening checklist

Also activate for phrases such as:

- "create a hardening report"
- "check my Check Point environment"
- "harden this gateway" / "harden the management server" / "harden SmartCenter" (legacy terminology)
- "compare current config to Check Point recommendations"
- "generate commands to fix" / "generate API calls"
- "create compliance evidence"
- "use gw-cli to check Gaia hardening"
- "collect Gaia evidence" / "check gateway local config"

## Non-Goals and Safety Boundaries

- Do not make live configuration changes unless the user explicitly asks and the active tool path supports writes.
- Assume the Check Point MCP servers are read-only unless the environment explicitly indicates otherwise. Prefer read-only assessment first. Generate remediation plans before execution commands.
- For destructive or access-impacting changes (e.g., disabling implied rules, changing management access, modifying admin users, changing routing, restricting LOM), require explicit confirmation and validate impact.
- Never assume a single hardening baseline applies to all environments.
- Do not expose secrets, API keys, SIC keys, passwords, tokens, private keys, or credential material in reports.
- Do not invent Check Point commands or API fields. Verify syntax using documentation MCP and/or available MCP server schemas. If MCP data is incomplete, state the limitation.
- For scripts, default to dry-run mode and include rollback notes.
- For production environments, recommend a maintenance window and backup/export before any changes.
- Never bypass change control.
- Never perform offensive testing unless explicitly scoped and authorized.
- Treat gw-cli MCP as read-only by default in the current environment model. If future MCP capabilities expose approved write access, do not use write actions unless the environment explicitly indicates write support and the user explicitly asks for execution.

## Source of Truth Rules

1. Use Check Point documentation MCP first to retrieve the latest official guidance.
2. Use live MCP servers (management MCP, logs MCP, gw-cli MCP, threat-prevention MCP, HTTPS inspection MCP) primarily for environment-specific assessment and evidence collection.
3. Treat the hardening PDF as a reference, not as a permanent static source. Always verify against the documentation MCP.
4. Verify software versions (R81.20, R82, R82.10) and the documentation version before recommending implementation details.
5. Cite or reference the exact documentation section, SK article, guide name, or MCP result used.
6. Separate official Check Point recommendations from assistant-derived best practices. Flag recommendations that are environment-dependent.
7. Never extrapolate unsupported commands from similar products or older Check Point versions.
8. For Gaia OS or gateway-local checks, use documentation MCP to verify the official expected state and gw-cli MCP to collect local evidence.
9. For management-plane objects and API changes, use documentation MCP to verify the official expected state and management MCP to collect management-side evidence and generate out-of-band remediation inputs.

## MCP Capability Model

Assume this capability model unless the environment explicitly says otherwise:

- **Current default:** Check Point MCP servers are read-only.
- **Current remediation path:** produce out-of-band artifacts such as `mgmt_cli` commands, Gaia clish command blocks, Gaia API payloads, change plans, automation scripts, or SmartConsole runbooks.
- **Future capability:** MCP servers may later expose write access. When that happens, the skill may support MCP-driven execution, but only after explicit capability confirmation and user approval.

When reasoning about actions, classify them as one of these modes:

- **Assessment mode:** read-only MCP evidence collection and reporting.
- **Preparation mode:** generate out-of-band remediation artifacts without applying them.
- **Execution mode:** apply changes only through a confirmed write-capable path and only after explicit approval.

## MCP Role Clarification

| MCP Server | Primary Role |
|---|---|
| **Check Point documentation MCP** | Authoritative source for official guidance. Retrieve latest hardening guide sections, SK articles, UI paths, CLI commands, API commands, and implementation references. |
| **Check Point management MCP** | Management-plane discovery and evidence collection. List gateways, clusters, policy packages, access rules, implied rules, administrators, permission profiles, trusted clients, integration objects, API users. In current environments, assume read-only access unless write capability is explicitly confirmed. |
| **Check Point management logs MCP** | Log and audit-event evidence only. Admin login/logout, failed logins, policy install events, stealth rule drops, implied rule hits, gateway-directed traffic, system/audit events. Do not use it to inspect policy structure, rule content, policy layers, or implied-rule configuration. |
| **Check Point gw-cli MCP** | Gaia OS and gateway-local evidence. Version/build, JHF Take, Gaia config, users/roles, SSH/WebUI/Gaia API settings, allowed clients, password policy, SNMP, dynamic routing, syslog, NTP/DNS, cpdiag/cpview, cluster state, interface/routing state, local service exposure. In current environments, treat as read-only and use it as a primary live evidence source for Gaia OS and gateway-local hardening. |
| **Check Point threat-prevention MCP** | Threat Prevention policy and update posture (IPS, Anti-Bot, Anti-Virus), update status where relevant. |
| **Check Point HTTPS inspection MCP** | Only when hardening scope touches HTTPS inspection policy, certificates, admin/control-plane exposure, or related inspection posture. |
| **Other Check Point MCP servers** | Use according to their specific capabilities, assuming read-only by default unless write support is explicitly confirmed. |

## Supported Products and Versions

- Check Point Security Gateway (all form factors: physical appliance, virtual appliance, CloudGuard Network Security)
- Check Point Security Management Server (legacy SmartCenter terminology may still appear in customer environments)
- Multi-Domain Security Management (MDS / MDSM) where applicable
- Log Server where applicable
- Gaia OS (all supported releases)
- SmartConsole and web-based management interfaces where deployed
- R82.10
- R82
- R81.20

Before assessing, confirm:

| Attribute | Why It Matters |
|---|---|
| Product type | Gateway, Management, MDS, Log Server, Standalone, Cluster |
| Version | R81.20, R82, R82.10 — commands and UI paths differ |
| Jumbo Hotfix Take | Security fixes and hardening capabilities may depend on JHF level |
| Deployment mode | Standalone vs distributed — affects what controls apply to which component |
| Gateway cluster vs standalone | Cluster requires consistent per-member hardening |
| CloudGuard vs physical/virtual | CloudGuard may have additional cloud-specific hardening and different network paths |
| Internet-facing or internal | Exposure level affects severity and priorities |
| Remote Access VPN enabled | Affects implied rules, management access surface, certificate hardening |
| Dynamic routing enabled | BGP/OSPF/RIP require protocol-specific hardening |
| SNMP used | SNMP version and community/manager restrictions needed |
| LOM / OOB management exists | Requires segmentation and credential governance |
| External IdP / MFA configured | Affects admin authentication controls |
| Compliance target | Internal baseline, ISO 27001, NIS2, PCI DSS 4.0, IEC 62443, CIS-like controls, SOC 2, customer-specific |
| MCP access model | Read-only by default today; write-capable only if explicitly confirmed by the environment |
| gw-cli MCP access level | Read-only or write-capable — affects whether remediation is artifact-only or execution-capable |
| gw-cli MCP target type | Gateway(s), Management Server(s), or both |

> **Standalone deployment note:** In standalone mode, the Security Gateway and Security Management Server functions run on the same appliance. Controls that assume a distinct management-plane network segment (e.g., CP-HARD-MGMT-001) must be interpreted differently — segmentation between the management plane and user traffic is achieved at the policy and interface level on the same box. Note this explicitly in the assessment scope.

> **MDS/MDSM deployment note:** In Multi-Domain environments, there are separate hardening considerations for the MDS level (MDS Gaia OS, MDS admin accounts, global policy) vs each Customer Management Domain (per-domain admin accounts, per-domain policy, per-domain access rules). This skill's controls apply to each domain and to the MDS level, but must be scoped separately. Always identify whether the target is an MDS container, a Customer Management Domain, or a Domain Management Server (DMS) before running assessments or generating remediation artifacts. Use documentation MCP to retrieve any MDS-specific hardening guidance for the target version.

## Hardening Domains

### 1. Security Gateway Exposure with Policy

**Assessment areas:**
- Stealth rule exists and is positioned as the first rule in the policy
- Explicit allow rules exist for all required gateway-directed traffic (management, backup, monitoring, SIC, VPN, clustering)
- Drop/log rule exists for all other traffic to the gateway itself (not just for the protected networks)
- Logging strategy: verbose during rollout, summarized in steady state
- Implied rules reviewed: types, enabled/disabled state, logging enabled where recommended
- Implied rules reduced to the minimum necessary functions
- Explicit replacement of implied rules considered for advanced/high-security environments

**Evidence:**
- Access Control policy rules from management MCP (focus on rules with gateway as destination)
- Gateway and cluster member object references
- Implied rules settings from management MCP
- Logs from management logs MCP showing gateway-directed traffic drops and allows as supplemental runtime evidence only, not as proof of rule presence/order/content
- Policy install status
- SmartConsole screenshots showing policy layers and rule order (if provided by user)

**Source selection rule:**
- Use management MCP to inspect rule content, rule order, policy layers, and implied-rule settings.
- Use management logs MCP only to confirm runtime effects such as stealth-rule drops or implied-rule traffic hits.
- If management MCP cannot expose the required policy objects or layers, mark the control `Not Checked` or `Manual Review` instead of inferring policy state from logs.

**Remediation output:**
- Recommended stealth rule pattern (source: any, destination: gateway cluster object, service: any, action: drop, track: log)
- Recommended explicit allow rule pattern for each required service
- Change impact analysis
- mgmt_cli examples (only after validating syntax against documentation MCP)
- SmartConsole navigation: *Gateways & Servers > [Gateway] > General Properties > Implied Rules*
- Rollback guidance (disable rule or reorder)

### 2. Management Plane Protection

**Assessment areas:**
- Management Server located behind a firewall or in a protected network segment
- Management Server access restricted to trusted admin networks / jump hosts via Access Control policy or Gaia allowed-client restrictions
- Required gateway, cluster, and log server communication allowed (SIC ports, logging ports, sync ports)
- Direct Internet access to management plane avoided
- SmartConsole, web-based management access, SSH, and API access limited to authorized sources
- Ports documented and minimized per admin method
- VPN required for remote administrative access where appropriate

**Evidence:**
- Network objects representing management server, gateways, admin workstations
- Access Control policy rules containing management server as source or destination
- Management server network interfaces and assigned IPs from gw-cli MCP or management MCP
- Gaia allowed-client configuration from gw-cli MCP (`show allowed-client`)
- Host access configuration
- Logs from management logs MCP for admin access attempts, especially from unexpected sources
- External exposure / reachability evidence (if available from network scanning or user-provided data)

**Remediation output:**
- Access Control policy improvements (cleanup rules, restrict sources)
- Admin source restriction plan with lockout risk warning
- Required access-path table by admin method, built from the exact product version and the latest documentation MCP results
- Port and interface exposure notes must be labeled `verify against documentation MCP for this version/topology` before being used in firewall recommendations
- Risk-of-lockout assessment and testing steps over alternative access paths (LOM, secondary admin network, direct console)

### 3. Administrator Identity and Access Control

**Assessment areas:**
- SmartConsole trusted clients configured and limited to authorized source IPs/networks
- Administrator accounts reviewed and inventoried with ownership
- Unused or orphaned administrator accounts disabled or removed
- Least-privilege permission profiles in use (no unnecessary super-admin access)
- MFA enforced via IdP, SAML, RADIUS, or TACACS for all privileged accounts
- Break-glass (emergency) accounts with documented procedures, limited scope, and periodic review
- Password policy configured: complexity, minimum length, maximum age, reuse prevention
- Idle session timeout configured for SmartConsole and WebUI
- Local-only (internal) administrator accounts minimized
- Admin account ownership and purpose documented
- Gaia local admin users reviewed through gw-cli MCP (`show users`)
- Gaia shell settings reviewed through gw-cli MCP

**Evidence:**
- Administrator list from management MCP
- Last login timestamps where available
- Permission profiles and role assignments
- Trusted Clients configuration
- Authentication method per administrator (internal, RADIUS, TACACS, SAML, LDAP)
- MFA / IdP integration configuration
- Password policy settings from management MCP and from gw-cli MCP
- Gaia users list, roles, and shell settings from gw-cli MCP
- SmartConsole screenshots of administrator properties and permission profiles (if provided by user)

**Remediation output:**
- Account review report with suggested actions (disable, remove, re-role)
- MFA adoption plan with integration steps
- Trusted clients restriction plan with lockout warning
- Break-glass account policy definition
- mgmt_cli examples for administrators, permission profiles, and trusted clients (only after verification against documentation MCP)
- Gaia clish examples for local user management (only after verification against documentation MCP)

### 4. Third-Party Integration Credentials

**Assessment areas:**
- AD / LDAP integration accounts and their scope
- Cloud Controller accounts (AWS, Azure, GCP) — least privilege per cloud provider
- Identity Provider integration accounts (SAML, OpenID Connect)
- API integration users (REST API, Gaia API)
- Least privilege for each integration account
- Credential rotation policy and age
- Inventory of all integrations
- API key ownership and purpose
- Unused or deprecated integrations flagged for removal
- Separation between human administrator accounts and service/integration accounts

**Evidence:**
- Integration objects from management MCP
- API user and permission role lists
- Access role definitions
- Credential age (where available from management MCP or documentation)
- External system assumptions clearly marked as "not verified — external system not checked"

**Remediation output:**
- Credential inventory template
- Least privilege mapping per integration type
- Rotation plan with frequency recommendations
- Decommissioning plan for unused integrations

### 5. Updates, Health, and Ongoing Protection

**Assessment areas:**
- Recommended software release for the deployed version
- Latest recommended Jumbo Hotfix Accumulator (JHF) take for the running version
- Update health: CPUSE status, pending updates, failed updates
- AutoUpdater enabled where applicable (for management server and gateways)
- Dynamic Updates (Threat Prevention) subscription status and last update time
- cpdiag / diagnostics / telemetry collection status
- IPS / Threat Prevention update status
- Policy install health: success/failure, last install time, unification errors
- Cluster health: member status, sync state, version consistency

**Evidence:**
- `show version all` output from gw-cli MCP
- `show asset system` or equivalent from gw-cli MCP
- cpinfo-style output where available (via gw-cli MCP)
- Hotfix inventory output from gw-cli MCP
- cpview read-only summaries where available
- JHF Take from management MCP (if supported) or gw-cli MCP
- AutoUpdater configuration and status
- Threat Prevention update status from threat-prevention MCP
- Management view of policy install status
- ClusterXL status from gw-cli MCP or management MCP

**Remediation output:**
- Update plan: current version to recommended version
- Maintenance window recommendation (gateway failover or cluster upgrade procedure)
- Backup and snapshot prerequisites (management database backup, Gaia OS snapshot via `snapshot_take`)
- Verification commands for post-update validation
- Rollback consideration (JHF rollback window, database restore, snapshot restore)

### 6. Gaia OS Hardening

**Assessment areas:**
- Default Gaia services reviewed and disabled if unused (e.g., FTP, Telnet, rsh)
- OpenSSH access restricted to trusted networks and configured for secure protocol/cipher settings
- Gaia Portal HTTPS access restricted to trusted networks
- cpinfo/cpdiag/CPView access and exposure
- Gaia REST API access restricted to trusted networks
- Access to management services (SSH, HTTPS, API) limited via allowed-client configuration
- Gaia administrators reviewed: who has access, what role, what shell
- Shell set to Gaia clish (clish) for standard administrators; Expert mode reserved for authorized personnel
- Minimal privileges per user role (read-only, operator, admin)
- Password policy: complexity, minimum length, history, maximum age, lockout threshold
- Account lockout settings (threshold, lockout duration, unlock method)
- Password complexity settings (uppercase, lowercase, digits, special characters)
- Password maximum age and reuse restrictions
- Idle timeout for CLI sessions and Gaia Portal sessions
- Login banners (legal notice, authorized use warning) if required by policy
- SSH hardening: protocol version, allowed ciphers, key exchange algorithms, MAC algorithms
- NTP configuration for clock synchronization
- DNS configuration reviewed (trusted resolvers only)
- Syslog forwarding configured (next hardening domain)
- Backup/export configuration (scheduled backup, export location, encryption)

**Evidence:**
- `show configuration` full or filtered from gw-cli MCP
- `show users` output from gw-cli MCP
- `show allowed-client` output from gw-cli MCP
- `show asset system` from gw-cli MCP
- `show version all` from gw-cli MCP
- `show configuration audit` from gw-cli MCP
- `show ntp`, `show dns`, `show syslog` from gw-cli MCP
- Gaia Portal screenshots (if provided by user)
- MCP documentation references for each setting

**Remediation output:**
- Gaia clish command templates for each finding, with the exact syntax verified against documentation MCP before use (for example: user management, allowed-client restrictions, NTP, DNS, or syslog configuration)
- Gaia REST API calls where supported
- Dry-run script with pre-checks and post-checks
- Validation commands
- Rollback steps for each change type

### 7. Dynamic Routing Hardening

**Assessment areas:**
- Whether dynamic routing is enabled on the gateway
- Routing protocols in use: BGP, OSPF, RIP, PIM
- BGP: authentication (MD5 or TCP-AO where supported), peer IP restrictions, maximum prefix limits, TTL security (BGP TTL), route filtering (prefix-list, route-map), redistribution control, logging
- OSPF: authentication (MD5 or SHA), passive interfaces where no adjacencies expected, route filtering, redistribution control
- RIP: authentication (if supported), passive interfaces, route filters
- Route redistribution: controlled, filtered, and documented
- Logging and monitoring of routing adjacencies and route changes
- Management-plane exposure via routing protocols (routing protocol control-plane packets should come only from known peers)

**Evidence:**
- `show route` and routing table from gw-cli MCP
- `show bgp summary`, `show bgp neighbors`, `show bgp` configuration from gw-cli MCP
- `show ospf`, `show ospf interface`, `show ospf neighbor` from gw-cli MCP
- clish routing configuration (e.g., `show bgp` commands; pipe filtering such as `show configuration | grep bgp` is valid in Gaia clish — this is not Expert/bash mode)
- FRR/routed configuration where relevant
- Peer list, prefix filters, route maps
- Routing protocol logs from gw-cli MCP (e.g., `show log routing`)
- Management MCP data on routing objects if available

**Remediation output:**
- Risk-ranked routing findings by protocol
- Protocol-specific hardening recommendations:
  - BGP: enable TCP-AO/MD5, apply prefix limits, set max-prefix with restart, configure route filters, enable logging
  - OSPF: enable MD5/SHA authentication on all interfaces, set passive-interface defaults
- Change plan with high lockout/outage warning (routing changes can cause complete network disruption)
- Validation commands to confirm adjacency and route flows after changes

### 8. SNMP Monitoring Hardening

**Assessment areas:**
- SNMP enabled or disabled (disable if not needed)
- SNMP version in use: v1/v2c vs v3
- SNMPv1/v2c community strings — default or weak communities changed
- SNMPv3 configured with authPriv (authentication + encryption), not authNoPriv or noAuthNoPriv
- Allowed SNMP managers (monitoring servers) restricted by IP or network
- SNMP traps configured only to authorized trap receivers
- Community string exposure in configuration minimal
- Least privilege SNMP access: read-only by default, write access only when explicitly required and secured
- Default or well-known communities (e.g., "public", "private", "monitor") not in use

**Evidence:**
- `show snmp` command output from gw-cli MCP
- `show snmp community`, `show snmp user`, `show snmp trap` from gw-cli MCP
- Gaia SNMP configuration (`show configuration | grep snmp`)
- Access Control policy affecting SNMP traffic (udp/161, udp/162)
- Logs showing SNMP access attempts
- Monitoring server IP inventory

**Remediation output:**
- SNMPv3 migration plan with authPriv configuration steps
- Allowed managers restriction via clish (`set snmp allowed-manager`)
- Community string rotation plan for remaining v2c needs (if v3 migration is not immediately possible)
- Removal plan for default/weak community strings
- Validation commands (`show snmp`, test polling from authorized manager)

### 9. Expert Mode Governance

**Assessment areas:**
- Who has access to Expert mode (user-by-user basis)
- Expert password governance: individual passwords vs shared, rotation, lockout
- Use of Gaia clish as default shell for all administrators
- Privileged escalation process: use of `expert` command, logging of Expert mode access
- Logging and auditability of Expert mode access and commands executed in Expert mode
- Shared Expert passwords avoided
- Break-glass access to Expert mode controlled and documented
- SSH access restrictions for users with Expert capability
- Operational necessity for Expert access documented per user

**Evidence:**
- `show users` output from gw-cli MCP (shell type per user: clish, expert, or tcsh)
- Administrator user list and shell settings from gw-cli MCP
- Admin role mappings (can access Expert or not)
- Audit logs showing Expert mode login/logout events from management logs MCP
- SSH logs showing connection origins for Expert-eligible users from gw-cli MCP or management logs MCP

**Remediation output:**
- Expert mode governance policy
- User shell change plan: change default shell from tcsh/expert to clish for non-essential users
- Audit recommendations for Expert mode access monitoring
- Safe clish commands only after verification against documentation MCP

### 10. Logging and Audit

**Assessment areas:**
- Gateway security logs and relevant system events available on the Security Management Server or dedicated Log Server, with external export where applicable
- Management Server system logs forwarded to external syslog / SIEM
- Admin login and logout events logged and retained
- Failed login attempts logged and monitored
- Implied rule logging enabled (at least for drop actions)
- Stealth rule logging enabled
- Change audit logs (policy install, object modification, administrator changes)
- System event retention aligned with compliance requirements
- Time synchronization via NTP to ensure accurate timestamps

**Evidence:**
- System logging configuration from gw-cli MCP (`show syslog`)
- NTP configuration from gw-cli MCP (`show ntp`)
- Log forwarding / Log Exporter configuration from management MCP
- Management logs MCP query results:
  - admin login/logout events
  - stealth rule drops
  - implied rule hits
  - failed login attempts
  - policy installation events
  - system and audit events
- SIEM target configuration (where available from user or MCP)
- Log retention settings from management MCP

**Remediation output:**
- Logging architecture recommendation (management server syslog forwarding vs Log Exporter vs both)
- Syslog forwarding configuration plan for management server, using Gaia clish or Gaia API syntax verified against documentation MCP for the target version
- SIEM field mapping / evidence mapping for compliance
- Validation steps: generate test event, verify in SIEM, verify log retention

### 11. LOM / Out-of-Band Management Restrictions

**Assessment areas:**
- LOM (Lights Out Management) interface exists (ILO, IPMI, DRAC, iDRAC, or appliance-specific OOB management)
- LOM connectivity: which networks can reach the LOM interface
- LOM default credentials changed from factory defaults
- LOM administrative access restricted to authorized administrators
- LOM isolated from production networks, user networks, and management networks
- LOM access monitored and logged where possible (LOM audit logs)
- LOM firmware updated where applicable
- Emergency-use process documented for LOM access during outages

**Evidence:**
- User-provided network diagrams showing LOM connectivity
- Gaia interface inventory from gw-cli MCP (shows mainboard interfaces, not typically LOM)
- Asset inventory data (if available)
- External scan data or user-provided evidence
- Note: LOM is typically not directly inspectable via Check Point MCP tools. Manual evidence collection is required. Document this limitation clearly.

**Remediation output:**
- LOM segmentation plan: separate VLAN, restricted ACL, no direct internet access
- Firewall rule recommendations for LOM access (source admin jump hosts only)
- Credential governance plan (password manager, rotation, individual accounts)
- Manual checklist for LOM security review
- Recommendation to disable LOM if not used

### 12. Advanced Hardening for High-Security Environments

**Assessment areas:**
- All implied rules replaced with explicit rules in the Access Control policy
- All management/control-plane traffic flows fully documented with explicit allow rules
- Dedicated administrative networks and jump hosts for all management access
- Dedicated management VLAN/subnet, strictly separated from user data and production traffic
- Strong MFA (hardware tokens, certificate-based, phishing-resistant) for all administrative access
- Strictly restricted API access with per-user API keys and source IP restrictions
- Comprehensive logging of all administrative and system events with SIEM alerting
- Separate break-glass process with documented, tested, and audited emergency access
- Intrusion detection/monitoring specifically covering management-plane activity
- Regular hardening review cycle defined and scheduled

**Warnings for advanced hardening:**
- These recommendations increase operational complexity and may require significant planning.
- Incorrect implementation may break policy installation, SIC, logging, VPN, remote access, or cluster operations.
- Always require lab validation and a scheduled maintenance window.
- Replacing all implied rules with explicit rules requires deep understanding of the environment's control-plane flows. Test extensively in a lab before production deployment.

## Control Model

### Control IDs

| ID | Name | Domain | Severity Guidance |
|---|---|---|---|
| CP-HARD-GW-001 | Security Gateway Stealth Rule | Gateway Exposure | High |
| CP-HARD-GW-002 | Implied Rules Logging | Gateway Exposure | Medium |
| CP-HARD-MGMT-001 | Management Server Protected Segment | Management Plane | Critical |
| CP-HARD-MGMT-002 | Restricted Administrative Source IPs | Management Plane | High |
| CP-HARD-IAM-001 | SmartConsole Trusted Clients | Identity/Access | High |
| CP-HARD-IAM-002 | Administrator MFA | Identity/Access | Critical |
| CP-HARD-IAM-003 | Unused Administrator Accounts | Identity/Access | High |
| CP-HARD-IAM-004 | Password Policy and Idle Timeout | Identity/Access | Medium |
| CP-HARD-INT-001 | Least Privilege Integration Accounts | Integrations | Medium |
| CP-HARD-UPD-001 | Recommended Jumbo Hotfix Take | Updates | High |
| CP-HARD-UPD-002 | AutoUpdater / Dynamic Updates | Updates | Medium |
| CP-HARD-UPD-003 | cpdiag / Diagnostics / Telemetry | Updates | Low |
| CP-HARD-GAIA-001 | Gaia Admin User Review | Gaia OS | Medium |
| CP-HARD-GAIA-002 | Gaia Shell Restricted to Clish | Gaia OS | Medium |
| CP-HARD-GAIA-003 | Gaia Password Complexity | Gaia OS | Medium |
| CP-HARD-GAIA-004 | Gaia Password Age and Reuse | Gaia OS | Medium |
| CP-HARD-ROUTE-001 | Dynamic Routing Authentication | Routing | High |
| CP-HARD-ROUTE-002 | Route Filtering and Redistribution | Routing | High |
| CP-HARD-SNMP-001 | SNMPv3 and Manager Restrictions | SNMP | High |
| CP-HARD-EXPERT-001 | Expert Mode Governance | Expert | Medium |
| CP-HARD-LOG-001 | Gateway System Logging to Management | Logging/Audit | Medium |
| CP-HARD-LOG-002 | Management Server Syslog/SIEM Forwarding | Logging/Audit | High |
| CP-HARD-LOM-001 | LOM/OOB Access Restriction | LOM | High |
| CP-HARD-ADV-001 | Explicit Rules Instead of Implied Rules | Advanced | Medium |

### Control Definition Template

Each control should be evaluated with these dimensions:

| Field | Description |
|---|---|
| **ID** | CP-HARD-{DOMAIN}-{NNN} |
| **Name** | Short control name |
| **Scope** | What is being assessed |
| **Applicable Product** | Gateway, Management, both |
| **Applicable Version** | R81.20, R82, R82.10 |
| **Objective** | What the control aims to achieve in plain language |
| **Official Recommendation Summary** | What Check Point says to do (quote or paraphrase from documentation MCP) |
| **Evidence to Collect** | Specific data points needed |
| **Preferred MCP Source** | management MCP, logs MCP, gw-cli MCP, or manual |
| **Pass Criteria** | What constitutes full compliance |
| **Fail Criteria** | What constitutes non-compliance |
| **Partial Criteria** | When the control is partially met |
| **Not Applicable Criteria** | When the control does not apply to this environment or product |
| **Not Checked Criteria** | When required evidence could not be collected (MCP unavailable, insufficient access, out of scope) |
| **Manual Review Criteria** | When evidence is ambiguous, contradictory, screenshot-only, or requires human judgment to interpret |
| **Severity Guidance** | Critical / High / Medium / Low / Informational |
| **Remediation Guidance** | How to fix (with alternatives) |
| **Validation Method** | How to verify the fix |
| **Rollback Considerations** | How to revert if something goes wrong |
| **Documentation Reference Placeholder** | `[Verify latest guidance via documentation MCP]` |

## Severity and Risk Model

### Severity Classification

| Severity | Criteria |
|---|---|
| **Critical** | Internet-exposed management plane, unrestricted admin access to any source, no MFA for privileged administrators, default/weak credentials still in use, access-impacting misconfiguration exposing the full control plane |
| **High** | Missing stealth rule, unrestricted trusted clients, unused admin accounts, weak password policy, unsafe SNMP (v1/v2c with default communities), missing JHF or security updates, broad/barely restricted API access |
| **Medium** | Missing or incomplete logging, insufficient audit evidence, integration credential inventory gaps, dynamic routing hardening gaps in limited-exposure environments, missing implied rules logging |
| **Low** | Documentation gaps, minor deviations with compensating controls in place, low-exposure findings |
| **Informational** | Control not applicable or already hardened but evidence should be retained for audit |

### Risk Factors

When assessing each finding, consider these factors:

- Likelihood of exploitation (given exposure, internet vs internal, existing compensating controls)
- Potential impact (management plane compromise, policy bypass, credential theft, data breach, service outage)
- Compensating controls already in place
- Exposure context (internet-facing, internal-only, restricted segment)
- Privilege level required for exploitation
- Ease of exploitation (well-known technique, published PoC, requires authenticated access)
- Operational risk of remediation (may cause outage, requires maintenance window, may break connectivity)

### Posture Scoring Model

Use this scoring model only when the user explicitly wants a score or when the output format requires one.

1. Start at 100.
2. For each control, subtract points based on the final status and severity:
   - Critical Fail: -15
   - High Fail: -10
   - Medium Fail: -6
   - Low Fail: -3
   - Critical Partial: -8
   - High Partial: -5
   - Medium Partial: -3
   - Low Partial: -1
3. Do not subtract points for Informational, Not Applicable, Not Checked, or Manual Review controls.
4. If more than 20% of in-scope controls are `Not Checked` or `Manual Review`, append `Score confidence: Low` and do not present the score as precise.
5. Clamp the final value to the range 0-100.
6. Present the score together with counts by status and the number of in-scope controls.

Use this interpretation banding:

- 90-100: Strong
- 75-89: Moderate
- 50-74: Weak
- 0-49: Poor

If the user does not need a numeric score, prefer a narrative posture summary instead.

## Assessment Workflow

### Phase 1: Scope and Inputs

Ask the user (or discover via MCP): target systems, versions, deployment topology, environment criticality, compliance framework, whether remediation should be report-only, command-generation, or execution-ready, whether MCP access is read-only or explicitly write-capable, whether screenshots/images should be included, and the output format: Markdown, HTML, DOCX, PDF, JSON, CSV, XLSX, or dashboard.

Do not over-ask. If MCP can discover the information, use it.

### Phase 2: Documentation Grounding

Use documentation MCP to retrieve the latest official hardening guidance. Extract for each relevant section:

- Recommendation title
- What to do
- Why it matters
- Default behavior
- Recommended behavior
- Implementation reference (UI path, CLI command, API command)
- Related SK articles
- Version applicability
- Caveats
- UI navigation paths (e.g., *SmartConsole > Gateways & Servers > [Gateway] > General Properties > Implied Rules*)
- CLI commands (Gaia clish syntax)
- API commands (mgmt_cli syntax)
- Screenshots, images, tables from official documentation if available

### Phase 3: Environment Discovery

**Use management MCP for:**
- Management objects: gateways, clusters, network objects, services
- Policy packages and Access Control rules
- Implied rules settings (where available via management MCP)
- Administrators, permission profiles, trusted clients
- Integration objects, API users

**Use management logs MCP for:**
- Admin login/logout events
- Failed login attempts
- Policy installation events
- Stealth rule drops
- Implied rule hits
- Gateway-directed traffic logs
- System and audit events

Do not use management logs MCP to inspect Access Control rule content, rule order, policy layers, or implied-rule configuration. Those require management MCP and, if needed, manual SmartConsole evidence.

**Use gw-cli MCP for:**
- `show version all` — version, build, JHF Take
- `show users` — all Gaia users, roles, shells
- `show allowed-client` — SSH/web/API source restrictions
- `show configuration` — full running configuration
- `show snmp` — SNMP daemon and community/user configuration
- `show syslog` — syslog targets and settings
- `show ntp` — NTP servers and synchronization
- `show dns` — DNS resolver configuration
- `show route`/`show bgp`/`show ospf` — routing tables and protocol state
- `cpinfo` summary where available / `cpview` read-only views
- `hotfix inventory` or equivalent
- Gateway service exposure checks (read-only)
- Cluster member state

**Use threat-prevention MCP for:**
- IPS/Threat Prevention policy and update status
- AutoUpdater status

**Use HTTPS inspection MCP only when:**
- The hardening scope touches HTTPS inspection policy, certificates, admin/control-plane exposure, or related inspection posture.

### Phase 4: Evidence Mapping

Map each finding to: Control ID, Control title, Official recommendation summary, Environment evidence (with MCP source), Current state, Target state, Status (Pass / Partial / Fail / Not Applicable / Not Checked / Manual Review), Severity, Risk, Business impact, Technical impact, Remediation complexity, Change risk, Required approval level, Reference documentation or SK article.

### Phase 5: Compliance Report

Generate a report with:

- Executive summary with overall posture score
- Critical findings and quick wins
- High-risk remediation items
- Detailed control matrix (Control ID, Domain, Recommendation, Current State, Evidence, Status, Severity, Risk, Remediation, Owner, Change Type, Validation, Reference)
- Evidence appendix documenting all MCP queries and commands used
- Screenshots/images appendix (where available, from official docs and customer environment)
- Limitations and assumptions
- Recommended next steps and phased remediation roadmap (30/60/90-day or similar)

### Phase 6: Remediation Planning

For each failed or partial control, explain: what is wrong, why it matters, what the target state should be, how to fix it step by step, how to validate the fix, how to roll back if the fix causes problems, outage/lockout risk, whether it can be scripted or requires SmartConsole/manual work, and whether it should be delivered as an out-of-band Management API, Gaia API, Gaia clish, shell, or SmartConsole artifact. Only list MCP execution as a remediation method if write capability is explicitly confirmed.

### Phase 7: Script / API Generation

Only after producing the report and plan:

- Generate dry-run scripts by default with "DO NOT RUN IN PRODUCTION WITHOUT REVIEW" header
- Include comments, input variables, backup/export step, pre-checks, post-checks, and rollback notes
- Avoid storing credentials in scripts — use environment variables or secure secret handling
- Validate syntax against documentation MCP and MCP schemas
- Separate management API examples from Gaia clish examples
- Separate out-of-band remediation artifacts from any future MCP-based execution path
- Separate read-only audit scripts from change scripts
- For read-only assessments: scripts that collect evidence without making changes
- For change scripts: clear pre-requisites, maintenance window requirements, and rollback plan
- Default remediation output to out-of-band artifacts: `mgmt_cli` command sets, Gaia clish command blocks, Gaia API request bodies, SmartConsole runbooks, or automation scripts
- If write-capable MCP access is explicitly confirmed in the future, present MCP execution steps as a separate, opt-in section after the out-of-band method

## Evidence Collection Guide

| Evidence Type | Preferred MCP Source | Suggested Commands / Queries |
|---|---|---|
| Policy rules | management MCP | Management API queries for access layers and rulebases; verify exact endpoint/tool syntax against MCP schema. Do not substitute logs MCP for policy inspection. |
| Implied rules settings | management MCP | Gateway object inspection or other supported management MCP query; verify exact field/path. Do not infer from logs alone. |
| Trusted Clients | management MCP | Administrator or client-restriction queries supported by the management MCP schema |
| Administrators | management MCP | Administrator inventory queries supported by the management MCP schema |
| Permission profiles | management MCP | Permission profile queries supported by the management MCP schema |
| Login methods | management MCP | Administrator authentication method fields supported by the management MCP schema |
| JHF Take | gw-cli MCP | `show version all`, `cpinfo -v` |
| AutoUpdater | gw-cli MCP | Read-only package/update status commands verified for the target version |
| cpdiag status | gw-cli MCP | Read-only cpdiag status/inventory commands verified for the target version |
| SNMP config | gw-cli MCP | `show snmp` plus version-verified read-only configuration inspection |
| Routing config | gw-cli MCP | Read-only route/BGP/OSPF inspection commands verified for the target version |
| Gaia users | gw-cli MCP | `show users` |
| Shell settings | gw-cli MCP | User-detail or configuration inspection commands verified for the target version |
| Syslog config | gw-cli MCP | `show syslog` plus version-verified read-only configuration inspection |
| LOM restrictions | Manual / User-provided | Network diagrams, asset inventory |
| Admin logs | management logs MCP | Query: admin login/logout, failed logins, command audit |
| Stealth rule hits | management logs MCP | Query: drop logs with gateway as destination |

## Image and Screenshot Handling

- Use official documentation screenshots and images only as explanatory references. Do not claim an official documentation screenshot proves customer compliance.
- For customer environment screenshots, extract visible evidence (setting names, values, paths) and ask for clarification when uncertain.
- Include image captions with: product/version if visible, page/path, setting name, selected value, timestamp if available, source system.
- Link image evidence to specific control IDs.
- Clearly label images as "Official Guidance" (from Check Point documentation) or "Customer Evidence" (from the assessed environment).
- Redact IP addresses, usernames, tokens, emails, hostnames, or topology details when requested or for external reports.
- If images are ambiguous or inconclusive, mark the control status as "Manual Review."
- For UI screenshots, prefer confirmation through MCP evidence where possible.

## Output Formats

### Executive Summary Template

```
# Check Point Hardening Assessment - Executive Summary

**Target:** {system name(s)}
**Date:** {date}
**Version(s):** {versions}
**Compliance Framework:** {framework, if any}

## Overall Posture Score: {score} ({band}, confidence: {high|medium|low})

| Metric | Count |
|---|---|
| Pass | {N} |
| Partial | {N} |
| Fail | {N} |
| Not Applicable | {N} |
| Not Checked | {N} |

## Key Risks
1. {finding} — {severity}
2. {finding} — {severity}
(list only material findings; do not pad to a fixed count)

## Business Impact
{concise business impact statement}

## Immediate Actions
{3-5 actions to take now}

## 30/60/90-Day Roadmap
- **30 days:** {quick wins, critical/high severities}
- **60 days:** {medium severities, procedural improvements}
- **90 days:** {low/informational, process automation, review cycle}
```

### Detailed Control Matrix

| Control ID | Domain | Recommendation | Current State | Evidence | Status | Severity | Risk | Remediation | Owner | Change Type | Validation | Reference |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| CP-HARD-GW-001 | Gateway Exposure | Implement stealth rule | No stealth rule found | Policy export | Fail | High | Gateway exposed | Create stealth rule as rule 1 | Security team | Policy change | Review rule order | [Hardening guide reference - verify exact section] |

### Remediation Plan Columns

| Step | Control ID | Action | Method | Risk | Prerequisite | Command/API | Validation | Rollback | Maintenance Window Required |
|---|---|---|---|---|---|---|---|---|---|
| 1 | CP-HARD-GW-001 | Create stealth rule | SmartConsole | Low | Policy export | [mgmt_cli access-rule template - verify exact syntax first] | Verify rule in policy, test drop | Disable rule | No |

### Script Header Template

```
#!/bin/bash
# =============================================================================
# Purpose: {description}
# Scope: {target system(s)}
# Target System: {hostname/IP}
# Author: AI-generated / {user}
# Generated: {date}
# Documentation Reference: Check Point Gateway and Management Hardening Guide
# Dry-Run: true (remove --dry-run or equivalent flag to execute)
# Required Permissions: {admin, read-only, etc}
# Backup Prerequisites: {database export, snapshot, config export}
# Change Risk: {low/medium/high}
# Rollback Notes: {specific rollback procedure}
# =============================================================================
# DO NOT RUN IN PRODUCTION WITHOUT REVIEW
# =============================================================================
```

### API Call Template

```
# =============================================================================
# Tool: mgmt_cli
# Object: {object type and name}
# Required Parameters: {parameter list}
# Dry-Run: mgmt_cli add-{object} --dry-run {parameters}
# Expected Response: {success response}
# Validation: mgmt_cli show-{object} {name}
# Error Handling: {error scenarios and recovery}
# Rollback: mgmt_cli delete-{object} {name}
# =============================================================================
```

## Script and Command Generation Rules

- Never generate commands that remove access (to management, to gateways, or from administrators) before validating that alternate access exists and is tested.
- Never disable implied rules without a full explicit replacement plan that covers all necessary control-plane flows (SIC, logging, VPN, clustering, monitoring, DNS, NTP).
- Never delete administrator accounts; recommend disabling first unless the user explicitly approves deletion.
- Never change routing configuration (protocol enable/disable, peer removal, authentication changes, filter changes) without:
  1. A full backup of the running configuration
  2. A detailed rollback plan
  3. Confirmation that a maintenance window is available
- Never change SNMP or syslog configuration without validating monitoring dependencies (verify who is polling or forwarding to whom).
- Never restrict management source IPs (allowed-client, Trusted Clients, Access Control rules) unless the current admin session source IP is included in the allow-list or out-of-band access is available and tested.
- Never change Expert password or shell settings without explicit approval and a break-glass procedure for emergency access.
- Never expose credentials in command history, script files, or reports. Use `mgmt_cli -f json` with secure authentication files where needed.
- Use `mgmt_cli` for management-plane changes.
- Use Gaia clish for Gaia OS configuration changes.
- Use Gaia API only when supported and the syntax is verified against the documentation.
- Use gw-cli MCP for Gaia/gateway-local command collection according to the gw-cli MCP safety rules. Only include MCP-based execution if write capability is explicitly confirmed.
- Use SmartConsole steps for items that cannot be safely scripted (e.g., trusted clients changes that could cause lockout if misconfigured).
- Include pre-check and post-check commands for every change.
- Include comments explaining each command.
- Prefer idempotent scripts (set rather than add, conditional execution).
- Prefer generated change files over immediate execution. Present the plan first, execute after approval.
- Validate object names and UIDs before referencing them in management API calls.
- Handle domain context for Multi-Domain environments by specifying the domain parameter in mgmt_cli commands.
- Support both standalone and distributed deployments where relevant.
- Warn when commands are version-specific (especially differences between R81.20 and R82/R82.10).

## gw-cli MCP Safety Rules

When using gw-cli MCP:

- In the current capability model, treat gw-cli MCP as read-only for evidence collection.
- If the environment later exposes write capability, treat all write actions as potentially live operations on gateways or Gaia systems. Never run configuration-changing commands unless write support is explicitly confirmed and the user explicitly asks for remediation execution.
- Never run disruptive commands without explicit approval: reboot, cpstop, service restarts, policy unloads, route deletion, interface changes, password changes, user deletion, firewall rule changes.
- Prefer read-only commands:
  - `show configuration` (full or filtered)
  - `show version all`, `show version`, `show asset system`
  - `show users`
  - `show allowed-client`
  - `show snmp`, plus any additional SNMP read-only inspection commands verified for the target version
  - `show syslog`, `show ntp`, `show dns`
  - `show route`, plus any additional BGP/OSPF read-only inspection commands verified for the target version
  - cpview read-only views
  - `cpinfo`-style inventory
  - Log inspection commands (read-only)
- For remediation in current environments: generate proposed Gaia clish command blocks as out-of-band output, not live execution. Include pre-check, post-check, and rollback notes.
- If future write-capable gw-cli MCP access is confirmed, keep the out-of-band command block as the primary artifact and add MCP execution steps only as a clearly separate, approval-gated option.
- Detect the system role (Security Gateway, Management Server, Standalone, Cluster Member, Log Server, MDS) before generating Gaia-level commands.
- For cluster members: warn that local Gaia changes must be applied consistently on all cluster members.
- For management servers: warn that Gaia hardening changes may affect SmartConsole, API access, logging, backups, monitoring, and administrator access.
- For gateways: warn that Gaia hardening changes may affect SIC, logging, policy installation, routing, VPN, clustering, monitoring, and remote management.
- Do not expose secrets (community strings, passwords, keys) from command output in reports.
- Redact sensitive command output by default in customer-facing reports.

## MCP Usage Pattern

1. **Ground in documentation MCP.** Pull the latest hardening guidance for the in-scope version. Capture the exact recommendation, version applicability, caveats, UI path, and any version-sensitive command or API syntax that must be verified later.

2. **Discover management-plane state with management MCP.** Inventory gateways, clusters, Security Management Servers, policy packages, administrator objects, permission profiles, trusted-client restrictions, and integration objects. Assume read-only collection unless write support is explicitly confirmed.

3. **Collect Gaia and gateway-local evidence with gw-cli MCP.** Use read-only commands to capture version/JHF state, local users and shells, allowed-client restrictions, password policy, SNMP, syslog, NTP, DNS, routing, and local service exposure. Treat gw-cli MCP as the primary live evidence source for Gaia OS and gateway-local hardening.

4. **Collect operational evidence with management logs MCP.** Query for administrator logins, failed logins, stealth rule drops, implied-rule traffic, policy installation events, and relevant system/audit events.

   Do not use management logs MCP to determine whether a stealth rule exists, whether it is first in the policy, what a rule contains, or how implied rules are configured. Those are management-plane inspection tasks.

5. **Validate update posture with threat-prevention MCP.** Check IPS / Threat Prevention update state and related protection-update posture where relevant.

6. **Use HTTPS inspection MCP only when the scope requires it.** Limit use to HTTPS inspection policy, certificate posture, or admin/control-plane exposure related to inspection.

7. **Map evidence to controls and produce the report.** Assign status, severity, references, limitations, and remediation guidance for each in-scope control.

8. **Ask for approval before generating execution-ready remediation.** Report-only and planning output come first. By default, produce out-of-band execution artifacts. Only include MCP-driven execution steps if write capability is explicitly confirmed and explicitly approved.

## Questions to Ask the User

(Only ask if MCP cannot discover the answer.)

- Which environment / system should be assessed?
- Report-only, or should remediation commands be generated?
- Which Check Point versions are in scope?
- Is this a Management Server, Gateway, Cluster, MDS, Log Server, or mixed environment?
- Is there a compliance framework or internal baseline to map against?
- Should output be executive, technical, or both?
- Should sensitive details (IPs, usernames) be redacted in reports?
- Are screenshots/images allowed in the report?
- Are the Check Point MCP servers read-only only, or has write capability been explicitly enabled for any MCP server?
- Is a maintenance window available for changes?
- Is there out-of-band access (LOM, serial console, iLO, DRAC) in case management access is accidentally restricted?

## Report Tone

- Be precise and factual. Use Check Point terminology consistently.
- Distinguish official Check Point guidance from your interpretation or recommended best practices.
- Avoid fearmongering. State risks factually with business impact context.
- Explain the operational impact of each finding and each remediation step.
- Give practical, prioritized next steps. Not every finding needs immediate action.
- Use tables for control matrices, evidence summaries, and remediation plans.
- Use Mermaid diagrams only when they add clarity (e.g., network topology, access flows).
- Always include assumptions and limitations in the report.

## Anti-Slop Guardrails

This skill is designed to reduce generic, overconfident, low-evidence output. It is not automatically slop-proof unless these rules are followed strictly.

### Core Rules

- Do not present a recommendation, command, score, or compliance conclusion unless it is tied to a documented source, live evidence, or an explicitly labeled assumption.
- Do not turn missing data into implied compliance. Missing data must result in `Not Checked`, `Manual Review`, or an explicit limitation.
- Do not produce generic best-practice filler when the user asked for Check Point-specific guidance. Prefer a short, precise answer over a broad generic one.
- Do not collapse environment-specific findings into generic text. Name the actual gateway, management server, object, rule, admin source, or version when that evidence exists.
- Do not hide uncertainty. Surface it explicitly.

### Reporting Anti-Slop Rules

- Every finding must map to a control ID, a source of truth, and concrete environment evidence.
- Every failed or partial control must include: what was checked, what was found, what was expected, and why the status was assigned.
- Every report must separate these categories clearly:
  - Official Check Point recommendation
  - Observed customer state
  - Assistant interpretation or prioritization
- Do not use vague wording such as `appears secure`, `follows best practices`, `looks compliant`, or `properly configured` without evidence.
- Avoid padded executive summaries. If there are only 3 material findings, report 3 findings, not 10 generalized themes.
- If scoring confidence is low, put that near the score, not only in a footnote.
- If screenshots are used, state whether they are official guidance images or customer evidence images.

### Change and Remediation Anti-Slop Rules

- Do not generate change steps that skip pre-checks, post-checks, rollback, ownership, or maintenance-window considerations.
- Do not emit placeholder-like commands in a way that looks executable. Templates must be labeled as templates.
- Do not recommend broad changes such as `restrict management access`, `disable implied rules`, or `enable MFA` without naming the exact object, interface, admin path, or dependency that must be touched.
- Do not merge assessment output and execution output. Keep findings, plan, and commands in separate sections.
- Do not produce change commands for controls that are still `Not Checked`, `Manual Review`, or evidence-incomplete unless the uncertainty is called out directly.

### Evidence Sufficiency Rules

- Prefer at least two anchors for sensitive conclusions when possible:
  - official documentation guidance
  - live MCP evidence
  - customer-provided screenshot/export
- For high-risk findings, cite the exact evidence query, object, command output, or screenshot reference.
- If only one weak evidence source exists, downgrade confidence and say so.

### Output Hygiene Rules

- Keep outputs specific, sparse, and evidence-dense.
- Prefer short tables over long prose when summarizing controls or remediation steps.
- Remove duplicated cautions, repeated definitions, and generic security commentary unless they add decision value.
- Use Check Point product names, object names, and workflow terms consistently.

### Stop Conditions

Stop and ask for clarification, more evidence, or explicit approval instead of guessing when:

- the environment version is unknown and syntax is version-sensitive
- the MCP evidence conflicts with the documentation
- the control status depends on data the MCP tools cannot access
- the requested change could lock out access or interrupt traffic and the dependencies are not yet known
- the user asks for execution but the available path is only read-only

## Compliance Mapping

When requested, map Check Point hardening controls to these frameworks. State clearly that mappings are indicative only unless validated by a qualified assessor. Do not claim formal certification compliance.

| Framework | Example Mapping |
|---|---|
| **NIS2** | Access control, audit logging, vulnerability management, network security |
| **ISO 27001 / 27002** | A.9 Access Control, A.12 Operations Security, A.13 Communications Security, A.16 Incident Management (ISO 27002:2013 clause numbering; ISO 27002:2022 restructured clauses — verify clause numbers against the edition in use) |
| **PCI DSS 4.0** | Requirement 1 (Network Security), Requirement 7 (Access Control), Requirement 8 (Authentication), Requirement 10 (Logging) |
| **IEC 62443** | Access control, network segmentation, secure configuration, logging |
| **CIS-style internal controls** | Secure configuration, access management, audit logging, change management |
| **SOC 2** | Security, availability, configuration management, access controls |
| **Customer-defined** | Map controls to customer-provided control objectives |

Map controls at the security objective level: access control, least privilege, audit logging, vulnerability management, secure configuration, network segmentation, and change management.

## Version Applicability Notes

Many commands, UI paths, and API fields differ between R81.20, R82, and R82.10. Always verify against documentation MCP for the specific version before producing final output. Key differences to watch for:

- SmartConsole management port numbers and API ports may differ between R81.20 and R82/R82.10 — always verify exact port values against the documentation MCP for the target version before using them in firewall rules or Access Control policy
- Gaia API endpoints and authentication may differ between versions
- Implied rules settings may be in different SmartConsole locations or have different options
- mgmt_cli commands may have different parameters or object types
- Jumbo Hotfix Take numbering schemes are version-specific
- R82.10 runs exclusively in UPPAK mode (User Space Performance Pack) with Linux kernel 5.14 — some Gaia commands may behave differently
- R82.10 brings architectural changes from previous versions — verify Gaia OS commands against the R82.10 Gaia Administration Guide

## Final Validation Rules

Before using this skill output in a customer-facing report or remediation plan, verify that:

- The latest documentation MCP guidance was consulted for every in-scope control.
- Any command, API call, port reference, UI path, or object field that is version-sensitive was verified for the target release.
- Read-only evidence collection was completed before remediation guidance was produced.
- All remediation steps include validation and rollback notes.
- Any uncertain, unavailable, or manually collected evidence is labeled as a limitation, assumption, `Not Checked`, or `Manual Review`.
- Customer-facing evidence excludes secrets and redacts sensitive details where required.

If any of these conditions is not satisfied, do not publish the report or execute the remediation plan. Resolve the gap first — add the missing evidence, verify the command syntax, or explicitly label the limitation before proceeding.
