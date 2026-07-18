---
name: kyc-customer-onboarding
description: >
  Performs customer KYC (Know Your Customer) verification and onboarding
  for commercial banking, including identity verification, document
  collection, risk assessment, sanctions screening, and account activation.
industry: financial-services
sub-sector: commercial-banking
function: compliance
version: 1.0.0
authors:
  - name: Tyms
    url: https://tyms.com
supported_locales:
  - UG
tags:
  - kyc
  - onboarding
  - compliance
  - aml
  - customer-verification
complexity: intermediate
reference_framework:
  primary:
    name: "BIAN (Banking Industry Architecture Network)"
    version: "13.0"
    mapping: "Party Reference Data Management, Customer Offer, Party Authentication"
  secondary:
    name: "APQC Banking PCF"
    mapping: "8.1.1 Establish KYC/CDD, 8.1.2 Perform due diligence"
---

# KYC Customer Onboarding

## Purpose

This skill enables an AI agent to guide and execute the customer KYC (Know Your Customer) verification and onboarding process for commercial banking operations. It covers the end-to-end workflow from initial customer identification through document collection, risk assessment, sanctions screening, approval routing, and account activation. The skill encodes regulatory compliance requirements, reporting obligations, and audit standards that govern KYC operations across jurisdictions.

## When to Use

- New customer account opening (individual or business)
- Periodic KYC review or re-verification when a scheduled review date is reached
- Customer upgrade requiring enhanced verification (e.g., from basic to full account)
- Trigger-based enhanced due diligence following a suspicious activity indicator
- Onboarding a customer acquired through a merger, acquisition, or portfolio transfer
- Re-onboarding a previously offboarded customer who wishes to resume the relationship

## Process Overview

### Step 1: Customer Identification

- Collect customer identity information including full legal name, date of birth, nationality, and contact details
- Determine customer type: individual, sole proprietor, corporate, NGO, trust, or other legal entity
- Determine the required verification level based on customer type and initial risk indicators: simplified, standard, or enhanced
- Capture the declared purpose of the account and expected transaction profile
- Record the channel through which the application was received (branch walk-in, online, agent-assisted, referral)
- Assign a unique application identifier and timestamp the start of the process

### Step 2: Document Collection & Verification

- Request required identity documents based on customer type and locale requirements
- For individuals: national identity card, passport, or other government-issued photo ID
- For businesses: certificate of incorporation, memorandum and articles of association, tax identification certificate, trading license, board resolution, and beneficial ownership declaration
- Verify document authenticity using automated verification where available (e.g., national ID database API)
- Cross-reference document details against the information provided in Step 1
- Assess document quality and legibility; request resubmission with quality guidelines if documents are unreadable
- For business accounts: trace beneficial ownership to ultimate beneficial owners holding 25% or more
- Store verified documents in the document management system with classification tags and retention metadata

### Step 3: Risk Assessment

- Score customer risk based on the following factors: customer type, geographic location, product type, expected transaction volume, source of funds, industry or occupation, and any adverse information
- Apply risk scoring rules to produce a numeric risk score (0-100) and a risk classification (low, medium, or high)
- Flag high-risk indicators that require enhanced due diligence: cash-intensive businesses, cross-border activity with high-risk jurisdictions, complex ownership structures, or unusual transaction profiles
- Determine the approval authority level required based on the risk classification: auto-approve for low risk, compliance officer for medium risk, senior compliance or committee for high risk
- Document the risk factors and scoring rationale for the audit trail

### Step 4: Screening

- Screen the customer (and all beneficial owners for business accounts) against international sanctions lists: United Nations, OFAC, EU, and locally mandated lists
- Check against Politically Exposed Persons (PEP) databases, including domestic and foreign PEP lists
- Screen for adverse media coverage related to financial crime, fraud, corruption, or terrorism
- Record each screening result individually with the list name, match confidence, and timestamp
- For positive matches: classify as confirmed match, possible match, or false positive
- For possible matches: queue for manual review by a compliance officer with match details

### Step 5: Approval / Escalation

- Auto-approve low-risk customers who meet all criteria: valid identity verified, documents collected, risk score below threshold, all screenings clear
- Route medium-risk applications to a compliance officer for review with the full case file
- Escalate high-risk applications to senior compliance officer or compliance committee with detailed risk assessment and screening results
- For any PEP match (confirmed or possible): require human review at approver level regardless of overall risk score
- For any confirmed sanctions match: block the application immediately and trigger a suspicious activity report
- Record the decision (approved, rejected, escalated), the decision maker (auto-system, operator, reviewer, approver, committee), and a written rationale
- For rejections: record the specific rejection reason and notify the customer with permitted information only

### Step 6: Account Activation

- Confirm that all KYC requirements have been satisfied: identity verified, documents collected and verified, risk assessed, screenings completed, and approval obtained
- Activate the account in the core banking system with the appropriate account type and product configuration
- Set transaction limits based on the assigned KYC level (simplified, standard, or enhanced)
- Schedule the next KYC review date based on the risk classification: 12 months for high-risk, 36 months for medium-risk, 60 months for low-risk
- Generate the compliance package containing all verification records, screening results, risk assessment, and approval documentation
- Send account activation confirmation to the customer through their preferred communication channel

## Required Inputs

| Input | Type | Required | Notes |
|-------|------|----------|-------|
| `customer_name` | string | Yes | Full legal name as it appears on identity documents |
| `date_of_birth` | date | Yes | For individual customers; ISO 8601 format |
| `nationality` | string | Yes | ISO 3166-1 alpha-2 country code |
| `address` | object | Yes | Physical and/or postal address with country, city, and street |
| `contact_phone` | string | Yes | At least one contact channel required; E.164 format preferred |
| `contact_email` | string | Yes | At least one contact channel required |
| `customer_type` | enum | Yes | One of: `individual`, `sole_proprietor`, `corporate`, `ngo`, `trust` |
| `identity_documents` | file[] | Yes | Scans or photos of identity documents; types vary by locale overlay |
| `source_of_funds` | string | Yes | Free-text declaration or selection from categorized list |
| `purpose_of_account` | string | Yes | Free-text declaration or selection from categorized list |
| `expected_monthly_turnover` | number | No | Estimated monthly transaction volume in local currency |
| `occupation_or_industry` | string | No | For individuals: occupation; for businesses: industry sector |
| `business_registration_docs` | file[] | Conditional | Required for business customer types; certificate, articles, etc. |
| `beneficial_ownership` | object[] | Conditional | Required for business customers; details of all 25%+ shareholders |
| `tax_identification_number` | string | Conditional | Required for business customers; may be required for individuals by locale |
| `application_channel` | enum | No | One of: `branch`, `online`, `agent`, `referral`, `mobile` |

## Outputs

| Output | Type | Description |
|--------|------|-------------|
| `application_id` | string | Unique identifier assigned to this KYC application |
| `kyc_status` | enum | Final status: `approved`, `pending`, `rejected`, `escalated` |
| `risk_score` | number (0-100) | Calculated composite risk score |
| `risk_classification` | enum | Classification derived from risk score: `low`, `medium`, `high` |
| `screening_result` | enum | Aggregate screening outcome: `clear`, `match`, `possible_match` |
| `screening_details` | object[] | Individual results per screening list with match confidence |
| `decision_rationale` | string | Written explanation for the approval, rejection, or escalation decision |
| `decision_maker` | object | Identity and role of the person or system that made the final decision |
| `kyc_level` | enum | Assigned verification tier: `simplified`, `standard`, `enhanced` |
| `next_review_date` | date | Scheduled date for the next periodic KYC review |
| `transaction_limits` | object | Daily, monthly, and per-transaction limits based on KYC level |
| `compliance_package` | object | Full documentation bundle for audit: documents, screenings, risk assessment, decision record |

## Integration Points

| System | Purpose | Direction |
|--------|---------|-----------|
| Core banking system | Account creation, product assignment, limit configuration | Outbound |
| National identity verification API | Real-time identity document verification against government databases | Outbound |
| Sanctions and PEP screening service | Watchlist and PEP database screening | Outbound |
| Adverse media screening service | Automated media screening for negative news | Outbound |
| Document management system | Secure storage and retrieval of identity documents and verification records | Bidirectional |
| Compliance case management system | Escalation routing, case tracking, and workflow management | Outbound |
| Customer communication channel | Status updates, document requests, approval notifications | Outbound |
| Regulatory reporting system | Filing of suspicious activity reports and large transaction reports | Outbound |

---

## Dependencies & Handoffs

### Requires (inputs from other skills)

| Skill | Data Required | Mandatory |
|-------|--------------|-----------|
| None (entry point skill) | -- | -- |

### Triggers (outputs to other skills)

| Condition | Triggers Skill | Data Passed |
|-----------|---------------|-------------|
| Customer approved | `account-opening` | `customer_id`, `kyc_level`, `risk_score`, `transaction_limits` |
| Sanctions match confirmed | `suspicious-activity-reporting` | `customer_id`, `match_details`, `screening_timestamp` |
| KYC review date reached (periodic) | `kyc-customer-onboarding` (self) | `customer_id`, `previous_kyc_date`, `previous_risk_score` |
| Enhanced due diligence required | `enhanced-due-diligence` | `customer_id`, `risk_factors`, `triggering_event` |
| Business account approved | `beneficial-ownership-registry` | `business_id`, `ownership_structure` |

### Workflow Position

```
[Customer Request / Periodic Trigger]
              |
              v
   [KYC Customer Onboarding]  <-- THIS SKILL
              |
              +-- Approved -----------> [Account Opening] --> [Product Onboarding]
              |
              +-- Sanctions Match ----> [Suspicious Activity Reporting]
              |
              +-- Rejected -----------> [Rejection Notification]
              |
              +-- EDD Required -------> [Enhanced Due Diligence]
              |
              +-- Business Approved --> [Beneficial Ownership Registry]
              |
              +-- Periodic Trigger ---> [KYC Review] (self)
```

---

## Roles & Permissions

| Role | Permissions | Typical Title |
|------|------------|---------------|
| `operator` | Execute standard KYC process, collect documents, initiate automated checks, request resubmissions | KYC Analyst, Customer Service Officer |
| `reviewer` | Approve medium-risk applications, override auto-decisions with documented rationale, request additional information, resolve possible screening matches | Compliance Officer |
| `approver` | Approve high-risk applications, escalated cases, PEP and sanctions-related decisions, approve exceptions to standard process | Senior Compliance Officer, Money Laundering Reporting Officer (MLRO) |
| `auditor` | View-only access to all decisions, case files, reports, and the full audit trail; cannot modify any records | Internal Auditor, External Auditor |
| `admin` | Configure risk scoring thresholds, manage screening list subscriptions, update document acceptance rules, define approval routing logic | Head of Compliance, Chief Compliance Officer |

### Segregation of Duties

| Action | Cannot Be Performed By |
|--------|----------------------|
| Approve an application | The same operator who initiated or processed the case |
| Override a sanctions match result | Anyone below Approver level |
| Modify risk scoring thresholds or rules | Anyone below Admin level |
| Delete or modify audit records | No one -- audit trail is immutable |
| Access sanctions/PEP match details | Anyone without Reviewer level or above |
| Change document acceptance rules | Anyone below Admin level |

---

## Reporting

### Key Performance Indicators

| KPI | Description | Data Source | Target | Frequency |
|-----|------------|-------------|--------|-----------|
| First-pass approval rate | Percentage of applications approved without escalation or additional information requests | Step 5: Approval | >= 85% | Daily |
| Average processing time | Elapsed time from application receipt to final decision | `start_timestamp` to `decision_timestamp` | < 24 hours | Daily |
| Rejection rate | Percentage of applications rejected | Step 5: Approval | Monitor (no fixed target) | Weekly |
| Compliance exception rate | Percentage of applications flagged for compliance review due to screening hits or risk triggers | Step 4: Screening | < 2% | Daily |
| Document resubmission rate | Percentage of applications requiring at least one document resubmission | Step 2: Document Collection | < 15% | Weekly |
| PEP and sanctions hit rate | Percentage of applications with positive screening matches (confirmed or possible) | Step 4: Screening | Monitor (no fixed target) | Daily |
| Auto-approval rate | Percentage of low-risk applications approved without human intervention | Step 5: Approval | >= 60% for low-risk applications | Weekly |
| Escalation rate | Percentage of applications escalated to senior compliance or committee | Step 5: Approval | < 5% | Weekly |
| KYC review overdue rate | Percentage of existing customers whose periodic KYC review is past the scheduled date | Periodic trigger | < 3% of portfolio | Monthly |

### Data Points to Capture

Each execution of this skill should produce the following data points for reporting and analytics:

| Data Point | Type | Captured At | Used In |
|-----------|------|-------------|---------|
| `application_id` | string | Process start | All reports, primary key for tracking |
| `customer_type` | enum | Step 1: Identification | Segmentation, risk distribution reports |
| `application_channel` | enum | Step 1: Identification | Channel efficiency reports |
| `verification_method` | enum (`automated`, `manual`) | Step 2: Document Collection | Automation efficiency reports |
| `documents_collected_count` | integer | Step 2: Document Collection | Completeness tracking |
| `resubmission_required` | boolean | Step 2: Document Collection | Document quality metrics |
| `risk_score` | number (0-100) | Step 3: Risk Assessment | Risk distribution analysis |
| `risk_classification` | enum (`low`, `medium`, `high`) | Step 3: Risk Assessment | Risk segmentation reports |
| `screening_lists_checked` | string[] | Step 4: Screening | Compliance coverage reports |
| `screening_result` | enum (`clear`, `match`, `possible_match`) | Step 4: Screening | Hit rate tracking |
| `decision` | enum (`approved`, `rejected`, `escalated`) | Step 5: Approval | Decision distribution reports |
| `decision_maker_type` | enum (`auto`, `operator`, `reviewer`, `approver`, `committee`) | Step 5: Approval | Automation tracking |
| `rejection_reason` | string | Step 5: Approval | Rejection analysis |
| `processing_duration_hours` | number | Process end | SLA tracking, bottleneck analysis |
| `kyc_level_assigned` | enum (`simplified`, `standard`, `enhanced`) | Step 6: Account Activation | KYC level distribution |

### Suggested Reports

| Report | Frequency | Audience | Description |
|--------|-----------|----------|-------------|
| KYC Operations Dashboard | Real-time | Operations Manager | Live pipeline view showing applications by status: pending, in-progress, approved, rejected, escalated. Includes volume trends and aging analysis. |
| Compliance Summary | Daily | Compliance Officer | Exceptions, escalations, screening matches, overdue reviews, and pending compliance decisions requiring action. |
| Processing Efficiency Report | Weekly | Head of Operations | Processing times by step, bottleneck identification, approval rates segmented by customer type and risk level. |
| Risk Distribution Report | Weekly | Risk Committee | Distribution of risk scores across the portfolio, trend analysis over time, concentration of high-risk customers by geography and industry. |
| Regulatory Compliance Report | Monthly / Quarterly | Regulator (e.g., Bank of Uganda, Central Bank of Kenya) | Suspicious transaction report counts, large transaction report counts, compliance metrics, KYC completion rates, and portfolio review status. |
| Automation Effectiveness Report | Monthly | Digital Transformation Lead | Auto-approval rates, manual intervention frequency, time saved through automation, false positive rates in screening. |

### Alert Triggers

| Alert | Condition | Severity | Action |
|-------|-----------|----------|--------|
| Processing backlog | Pending applications exceed 50 AND average wait time exceeds 48 hours | High | Notify operations manager; consider temporary resource allocation or overtime |
| Compliance exception spike | Exception rate exceeds 5% in a rolling 24-hour window | High | Notify compliance officer; investigate root cause (screening list update, new customer segment, data quality) |
| Sanctions match detected | Any positive sanctions match (confirmed or possible) | Critical | Immediate compliance officer notification; block application approval; begin investigation |
| First-pass approval rate drop | First-pass approval rate falls below 70% over a rolling 7-day period | Medium | Investigate potential causes: rule changes, data quality degradation, shift in customer segment |
| KYC reviews overdue | Overdue reviews exceed 10% of the active customer portfolio | High | Notify compliance; prioritize the review queue; assess regulatory exposure |
| Auto-approval anomaly | Auto-approval rate changes by more than 20 percentage points in a 24-hour period | Medium | Investigate rule engine behavior; check for data pipeline issues or screening service changes |

---

## Error Handling

### Failure Scenarios

| Scenario | Handling | Fallback | Severity |
|----------|---------|----------|----------|
| National ID verification API unavailable | Queue the application for retry (maximum 3 attempts over 24 hours) | Route to manual verification using document scan and visual inspection | Medium |
| Document quality too low for automated verification | Request resubmission from the customer with specific quality guidelines (resolution, lighting, framing) | Route to manual review by operator after second failed resubmission | Low |
| Sanctions screening service timeout | Block approval until screening completes; retry every 15 minutes | Never approve without completed screening; notify customer of delay if wait exceeds 4 hours | Critical |
| Customer provides conflicting information | Flag the application for human review with conflict details highlighted | Do not auto-resolve conflicts; require operator to contact customer for clarification | Medium |
| Duplicate application detected | Alert operator and link to the existing application | Merge records if confirmed duplicate by reviewer; reject the newer application if intentional re-submission | Low |
| Risk scoring model unavailable | Use rule-based fallback scoring with conservative thresholds | Route all applications to human review until model service recovers | High |
| Core banking system down during account activation | Complete all KYC steps; queue account activation for when system recovers | Activate accounts in FIFO order upon recovery; notify customer of activation delay | Medium |
| Document storage system full or unavailable | Alert admin immediately; continue process using temporary local storage | Do not skip document collection; migrate to permanent storage when available | Medium |
| Customer abandons the application midway | Save all progress; send a reminder after 24 hours and again after 7 days | Close the incomplete application after 30 days of inactivity with a final notification | Low |

### Critical Rules

These rules must never be violated regardless of system state, operational pressure, or override requests:

1. **Never approve without completed sanctions screening** -- even if the screening service is down, the application must wait. No exception, no workaround.
2. **Never auto-approve a PEP match** -- all PEP matches (confirmed or possible) require human review at approver level regardless of the overall risk score.
3. **Never delete or modify audit records** -- the audit trail is immutable. No role, including admin, has permission to alter historical records.
4. **Never bypass document verification** -- identity documents must be collected and verified even if the customer is known from other banking relationships.
5. **Never share screening results with the customer** -- sanctions match, PEP match, and adverse media details are confidential and must not be disclosed to the applicant or any unauthorized party.
6. **Never approve an application you initiated** -- the operator who processes the case cannot also be the approver; segregation of duties must be enforced at all times.

---

## Framework Alignment

### Primary Framework: BIAN (Banking Industry Architecture Network) v13.0

This skill maps to three BIAN service domains that together cover the end-to-end KYC and customer onboarding process:

| BIAN Service Domain | BIAN Business Area | Relationship to This Skill |
|--------------------|-------------------|---------------------------|
| Party Reference Data Management | Operations | Primary -- governs customer identification and data collection (Steps 1-2). BIAN defines this domain as responsible for maintaining reference information about parties including individuals and organizations. |
| Customer Offer | Sales & Service | Supporting -- governs the account opening and product assignment that follows successful KYC (Step 6). BIAN defines this domain as responsible for orchestrating the evaluation and fulfillment of a customer product offer. |
| Party Authentication | Operations | Supporting -- governs the identity verification and document authentication processes (Step 2). BIAN defines this domain as responsible for authenticating the identity of a party through document and data verification. |
| Party Screening | Risk & Compliance | Supporting -- governs the sanctions and PEP screening workflow (Step 4). |
| Regulatory Compliance | Risk & Compliance | Supporting -- provides the compliance context for audit, reporting, and regulatory obligations. |

**What BIAN defines:** BIAN provides a service-oriented architecture framework that identifies approximately 300 service domains representing discrete business capabilities. For KYC, BIAN defines the high-level service boundaries, data entities, and inter-domain relationships. BIAN tells an enterprise architect which capabilities exist and how they relate to each other at the architecture level.

**What BIAN does not define:** BIAN does not prescribe locale-specific regulatory requirements, accepted identity documents, risk scoring methodologies, operational KPIs, error handling procedures, audit retention periods, SLA targets, or role-based approval workflows. These are left to the implementing institution.

**What OpenIOM adds:** This skill fills the gap between BIAN's architectural blueprint and production operations. It provides the step-by-step operational logic, locale-specific compliance requirements (via locale overlays), risk assessment criteria, screening procedures, reporting KPIs, data classification, error handling and fallback procedures, audit event definitions, SLA expectations, role definitions with segregation of duties, and validation scenarios that a platform needs to actually execute the KYC process. Where BIAN says "Party Reference Data Management exists as a service domain," OpenIOM says "here is exactly how to collect, verify, and manage customer identity data, what can go wrong, what to measure, and what to log."

### Secondary Framework: APQC Banking PCF

This skill aligns with the following APQC Banking Process Classification Framework process areas:

| APQC Process ID | Process Name | Relationship to This Skill |
|----------------|-------------|---------------------------|
| 8.1.1 | Establish KYC / Customer Due Diligence | Steps 1-3 of this skill: customer identification, document collection, and risk assessment |
| 8.1.2 | Perform due diligence | Steps 3-4 of this skill: risk assessment and screening |
| 8.1.3 | Monitor ongoing customer activity | Periodic review trigger that re-invokes this skill |

APQC provides a hierarchical process taxonomy that complements BIAN's service-oriented view. Where BIAN organizes by capability, APQC organizes by process flow. Together they provide a complete picture: BIAN tells you which services are involved, APQC tells you where the process sits in the enterprise process hierarchy.

### Notes

- BIAN service domain mappings are based on the publicly available BIAN Service Landscape v13.0. Detailed behavioral qualifiers and service operation mappings may require BIAN membership access for full validation.
- APQC Banking PCF process ID mappings are based on the publicly available process classification hierarchy. Detailed sub-process mappings may vary by APQC version.
- This mapping is considered stable for the v1.0.0 release. Community feedback and formal BIAN/APQC validation are welcome to refine the alignment.

---

## Audit Requirements

### Mandatory Audit Events

Every execution of this skill must log the following events for compliance and audit purposes:

| Event | Data to Log | Triggered At | Immutable |
|-------|------------|--------------|-----------|
| Application received | `application_id`, `customer_id`, `customer_type`, `application_channel`, `receiving_operator_id`, `timestamp` | Process start | Yes |
| Document collected | `application_id`, `document_type`, `document_id`, `collection_method` (`upload`, `scan`, `physical`), `timestamp` | Step 2: Document Collection | Yes |
| Document verified | `application_id`, `document_type`, `verification_method` (`automated`, `manual`), `verification_result` (`pass`, `fail`, `inconclusive`), `verifier_id`, `timestamp` | Step 2: Document Verification | Yes |
| Resubmission requested | `application_id`, `document_type`, `reason`, `requesting_operator_id`, `timestamp` | Step 2: Document Collection | Yes |
| Risk score assigned | `application_id`, `risk_score`, `risk_classification`, `scoring_factors`, `model_version`, `timestamp` | Step 3: Risk Assessment | Yes |
| Screening performed | `application_id`, `lists_checked`, `individual_results_per_list`, `aggregate_result`, `service_provider`, `timestamp` | Step 4: Screening | Yes |
| PEP match found | `application_id`, `match_details`, `match_confidence`, `source_list`, `timestamp` | Step 4: Screening | Yes |
| Decision made | `application_id`, `decision` (`approved`, `rejected`, `escalated`), `decision_maker_id`, `decision_maker_role`, `authority_level`, `rationale`, `timestamp` | Step 5: Approval | Yes |
| Escalation triggered | `application_id`, `escalation_reason`, `escalated_from_role`, `escalated_to_role`, `timestamp` | Step 5: Approval | Yes |
| Override applied | `application_id`, `original_decision`, `override_decision`, `override_reason`, `overrider_id`, `overrider_role`, `timestamp` | Step 5: Approval | Yes |
| Account activated | `application_id`, `account_id`, `kyc_level`, `transaction_limits`, `activation_timestamp` | Step 6: Account Activation | Yes |
| KYC review scheduled | `application_id`, `customer_id`, `next_review_date`, `review_trigger` (`risk_based`, `regulatory`, `event_based`), `timestamp` | Step 6: Account Activation | Yes |

### Regulatory Retention Requirements

Retention periods vary by jurisdiction. The base requirement follows FATF recommendations. Locale overlays specify binding local requirements.

| Jurisdiction | Minimum Retention | Post-Relationship | Reference |
|-------------|-------------------|-------------------|-----------|
| Global (FATF baseline) | 5 years | From end of business relationship | FATF Recommendation 11 |
| Uganda | 10 years | From end of business relationship | Anti-Money Laundering Act 2013, Section 19 |
| Kenya | 7 years | From end of business relationship | Proceeds of Crime and Anti-Money Laundering Act (POCAMLA) 2009, Section 45 |
| Tanzania | 10 years | From end of business relationship | Anti-Money Laundering Act 2006, Section 16 |

*Note: Locale overlays provide the definitive local requirements for each jurisdiction. The table above is indicative and must be supplemented by the applicable locale overlay.*

### Audit Trail Access

| Role | Access Level |
|------|-------------|
| Operator | Own actions only for applications they processed |
| Reviewer | All actions within their review scope and assigned cases |
| Approver | All actions for applications within their approval authority |
| Auditor | Full read access to all audit records across all applications |
| Admin | Full read access to all audit records; cannot modify or delete |
| Regulator | Full read access upon formal written request or regulatory examination |

---

## Data Classification

### Data Sensitivity Levels

All data points handled by this skill are classified for appropriate handling by implementing platforms:

| Data Point | Classification | Handling Requirements |
|-----------|---------------|---------------------|
| `customer_name` | PII | Encrypt at rest; mask in logs and non-essential displays |
| `date_of_birth` | PII | Encrypt at rest; do not display in summary views |
| `nationality` | PII | Encrypt at rest |
| `address` | PII | Encrypt at rest; mask in displays showing only city/country |
| `contact_phone` | PII | Encrypt at rest; mask in displays (show last 4 digits only) |
| `contact_email` | PII | Encrypt at rest; mask in displays (show domain only) |
| `national_id_number` | Sensitive PII | Encrypt at rest and in transit; strict access control; never log in plaintext |
| `identity_document_scans` | Sensitive PII | Encrypt at rest; secure storage with access logging; retention policy applies |
| `tax_identification_number` | Sensitive PII | Encrypt at rest and in transit; strict access control |
| `beneficial_ownership_details` | Confidential | Encrypt at rest; compliance and management role access only |
| `source_of_funds` | Confidential | Encrypt at rest; compliance role access only |
| `risk_score` | Internal | Access restricted to compliance and management roles |
| `risk_classification` | Internal | Access restricted to compliance and management roles |
| `risk_factors` | Confidential | Access restricted to compliance roles; do not expose to operators |
| `screening_result` (aggregate) | Confidential | Audit trail required for all access; never share with the customer |
| `pep_match_details` | Restricted | Compliance roles only; all access logged; regulator access on formal request |
| `sanctions_match_details` | Restricted | Compliance roles only; all access logged; regulator access on formal request |
| `adverse_media_results` | Confidential | Compliance roles only; access logged |
| `decision_rationale` | Internal | Retain per audit requirements; accessible to reviewers and above |
| `application_id` | Internal | No special handling required beyond standard access controls |
| `kyc_level` | Internal | No special handling required beyond standard access controls |
| `transaction_limits` | Internal | Accessible to operations and compliance roles |

### Classification Definitions

| Level | Description | Access |
|-------|------------|--------|
| Public | Non-sensitive information that can be shared freely | All roles |
| Internal | Business-internal information not intended for external sharing | Authenticated users with an assigned role |
| Confidential | Sensitive business information requiring access restrictions | Specific roles only, as defined in the Roles & Permissions section |
| PII | Personally Identifiable Information subject to data protection law | Need-to-know basis; subject to data protection and privacy legislation |
| Sensitive PII | High-risk personal data including national identifiers, biometrics, and document scans | Strict access control; encryption mandatory at rest and in transit |
| Restricted | Highest sensitivity level for sanctions, PEP, and law enforcement-related data | Named individuals only; all access logged and auditable |

---

## Validation Scenarios

Platforms implementing this skill should verify correct behavior against the following scenarios:

| # | Scenario | Input Profile | Expected Outcome |
|---|----------|--------------|-----------------|
| 1 | Standard individual, low risk | Valid national ID, employed (salaried), low-value savings account, no screening hits | Auto-approved; assigned standard KYC level; standard transaction limits; next review in 60 months |
| 2 | Standard individual, medium risk | Valid national ID, self-employed, medium-value business account, no screening hits | Routed to compliance officer for review; standard or enhanced KYC level based on reviewer decision |
| 3 | High-risk individual | Valid national ID, cash-intensive business owner, high-value account, high expected turnover | Enhanced due diligence triggered; requires committee-level approval; enhanced KYC level; next review in 12 months |
| 4 | PEP detected | Customer matches PEP database (domestic, high confidence) | Enhanced due diligence mandatory; routed to approver level; cannot be auto-approved regardless of risk score |
| 5 | Confirmed sanctions match | Positive confirmed match on OFAC or UN sanctions list | Application blocked immediately; suspicious activity report filed; escalated to MLRO; customer not informed of match reason |
| 6 | Possible sanctions match (fuzzy) | Partial or fuzzy name match with low confidence score | Flagged for manual review by compliance officer; not auto-rejected; reviewer must confirm or clear the match |
| 7 | Expired identity document | National ID card past its expiry date | Resubmission requested with guidance to renew; application held but not rejected outright |
| 8 | Poor document quality | Blurry scan, unreadable text, partial document | Resubmission requested with specific quality guidelines; maximum 2 resubmission attempts before routing to manual review |
| 9 | Minor applicant | Date of birth indicates age under 18 | Redirected to minor or guardian account process; cannot proceed through standard KYC flow |
| 10 | Refugee customer | Government-issued Refugee Identity Card, no national ID number | Accepted under simplified KYC tier per refugee provisions in the applicable locale; reduced transaction limits applied |
| 11 | Business account, simple structure | Sole proprietor, single owner, valid business registration and tax ID | Standard business KYC; single beneficial owner recorded; standard processing timeline |
| 12 | Business account, complex ownership | Corporate entity with 5 shareholders across 2 layers of holding companies | Beneficial ownership traced to all ultimate beneficial owners; enhanced review triggered by ownership complexity |
| 13 | NGO account | Valid NGO registration, multiple foreign funding sources | Additional scrutiny applied per NGO regulatory provisions; enhanced due diligence on funding sources and donor relationships |
| 14 | Duplicate application | Same national ID number as an existing pending application | Duplicate detected; operator alerted with link to existing application; applications linked for review |
| 15 | Conflicting information | Address on identity document does not match the declared address | Flagged for human review; operator must contact customer to resolve the conflict before the application can proceed |
| 16 | Screening service unavailable | Valid application, all documents collected, but sanctions screening API returns timeout | Application queued; approval blocked until screening completes; customer notified of processing delay |
| 17 | Periodic KYC review | Existing approved customer, scheduled KYC review date has been reached | Re-verification process triggered; previous data pre-populated; only changes since last review require re-verification |
| 18 | Customer from high-risk geographic region | Valid national ID, residential address in a border region adjacent to a conflict zone | Geographic risk factor applied to risk scoring; may trigger enhanced due diligence depending on overall risk profile |

Locale overlays may add additional validation scenarios specific to their jurisdiction. For example, the Uganda locale overlay includes scenarios for LC1 letters, mobile money KYC tier upgrades, and URA TIN verification failures.

---

## SLA Expectations

### Processing Time Targets

| Step | Target Duration | Maximum Duration | Notes |
|------|----------------|-----------------|-------|
| Step 1: Customer Identification | < 5 minutes | 15 minutes | Primarily depends on customer input speed and channel |
| Step 2: Document Collection | Immediate (digital upload) / 3 days (physical submission) | 7 days before sending a follow-up reminder | Depends on customer responsiveness and document availability |
| Step 2: Document Verification | < 5 minutes (automated) / < 4 hours (manual) | 24 hours | Automated verification strongly preferred |
| Step 3: Risk Assessment | < 1 minute (automated) | 2 hours (if manual fallback is required) | Should be fully automated under normal operating conditions |
| Step 4: Screening | < 2 minutes | 30 minutes | Dependent on screening service availability and response time |
| Step 5: Approval (low-risk, auto) | Immediate | 4 hours | Should be instant when all automated checks pass |
| Step 5: Approval (medium-risk) | < 4 hours | 24 hours | Requires compliance officer review |
| Step 5: Approval (high-risk) | < 24 hours | 72 hours | May require compliance committee convening |
| Step 6: Account Activation | < 15 minutes | 4 hours | Post-approval; mostly automated core banking system interaction |

### End-to-End Targets

| Scenario | Target | Maximum |
|----------|--------|---------|
| Low-risk individual with digital documents | < 30 minutes | 24 hours |
| Medium-risk individual | < 4 hours | 48 hours |
| High-risk individual | < 48 hours | 5 business days |
| Business account (standard structure) | < 24 hours | 5 business days |
| Business account (complex ownership) | < 72 hours | 10 business days |

### SLA Breach Handling

| Breach | Action |
|--------|--------|
| Any step exceeds its maximum duration | Auto-escalate to the next authority level with aging details |
| End-to-end processing exceeds the maximum target | Alert operations manager and compliance officer; application flagged for priority processing |
| Customer waiting more than 48 hours without a status update | Send automated status update to the customer through their preferred channel |
| Screening step pending for more than 30 minutes | Attempt failover to backup screening service if available; alert operations if no backup |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 1.0.0 | 2026-02-17 | Initial release. Core KYC process with 6 steps. Full reporting section with 9 KPIs, 15 data points, 6 reports, and 6 alerts. Error handling with 9 failure scenarios and 6 critical rules. Audit requirements, data classification, 18 validation scenarios, SLA expectations. Framework alignment to BIAN v13.0 and APQC Banking PCF. Uganda locale overlay supported at launch. |
