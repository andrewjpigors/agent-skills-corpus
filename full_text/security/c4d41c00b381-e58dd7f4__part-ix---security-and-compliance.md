---
name: Part IX - Security and Compliance
version: 1.0.0
description: Comprehensive security mandates, protocols, and compliance requirements for AI systems and infrastructure. This skill establishes the foundational security architecture that all AI agents and systems must adhere to.
scope: security, compliance, infrastructure, data-protection
authority: AI Constitution - Directive Principles
enforcement: MANDATORY
review_cycle: quarterly
---

# PART IX: SECURITY AND COMPLIANCE

## CONSTITUTIVE PRINCIPLES

### Article 1: Security-First Mandate

**1.1** Security shall not be considered an afterthought but shall be a foundational principle embedded in every layer of the AI system's architecture, design, implementation, and operation.

**1.2** The principle of "secure by default" shall govern all system configurations. Default settings must always favor security over convenience.

**1.3** Security considerations shall be integrated into the software development lifecycle from the initial design phase through deployment, maintenance, and eventual decommissioning.

**1.4** All security controls and measures must be documented, version-controlled, and subject to regular audit and review.

**1.5** Security incidents must be reported within established timeframes, thoroughly investigated, and lessons learned must be incorporated into preventive measures.

### Article 2: Zero Trust Architecture Mandate

**2.1** The Zero Trust security model shall be the foundational architecture for all AI systems and infrastructure.

**2.2** Definition of Zero Trust: No entity, whether internal or external, shall be trusted by default. All access requests must be verified, authorized, and continuously validated.

**2.3** Core Principles of Zero Trust Implementation:

   (a) **Verify Explicitly**: Always authenticate and authorize based on all available data points, including identity, location, device health, service or workload, data classification, and anomalies.

   (b) **Use Least Privileged Access**: Limit user access with just-in-time and just-enough-access, risk-based adaptive policies, and data protection.

   (c) **Assume Breach**: Minimize blast radius and segment access. Verify end-to-end encryption. Use analytics to improve detection and response.

**2.4** Micro-segmentation Requirements:

   (a) Network segmentation must be implemented at the application and service level, not just at the perimeter.

   (b) Each service and data domain must have its own access controls independent of network location.

   (c) Lateral movement within the network must be prevented or severely restricted.

**2.5** Identity as the New Perimeter: All access control decisions must be identity-centric, with strong authentication and continuous validation.

### Article 3: Defense in Depth Mandate

**3.1** Multiple layers of security controls must be implemented to protect assets. No single security control shall be relied upon as the sole protection mechanism.

**3.2** The security architecture must include, at minimum:

   (a) Physical security controls
   (b) Network security controls (firewalls, intrusion detection/prevention)
   (c) Host security controls (hardening, patching, monitoring)
   (d) Application security controls (secure coding, WAF, input validation)
   (e) Data security controls (encryption, access controls, masking)
   (f) Identity and access management controls

**3.3** Each layer must be able to function independently if other layers are compromised.

**3.4** Security controls at different layers must not have dependencies that could cause cascading failures.

### Article 4: Security Through Transparency

**4.1** All security controls, configurations, and policies must be documented and made available to authorized auditors.

**4.2** Security decisions must be traceable through audit logs that capture who, what, when, where, and why.

**4.3** Security architecture documentation must be maintained and updated whenever changes are made.

**4.4** Threat models and risk assessments must be documented and reviewed periodically.

---

## CHAPTER I: INPUT VALIDATION IMPERATIVE

### Article 5: Universal Input Validation Mandate

**5.1** All data entering the system, regardless of source, must be validated before processing, storage, or transmission.

**5.2** Input validation must be performed on the server-side as the authoritative source of truth. Client-side validation is for user experience only and must never be relied upon for security.

**5.3** Input validation must use an allowlist (positive validation) approach rather than a blocklist (negative validation) approach wherever possible.

**5.4** Validation must be performed at the earliest possible point in the request processing pipeline.

### Article 6: Type Validation Standards

**6.1** All inputs must be validated for:

   (a) **Data Type**: Ensuring the input matches the expected data type (string, integer, array, object, etc.)
   
   (b) **Format**: Ensuring the input conforms to expected formats (email, URL, date, phone number, etc.)
   
   (c) **Length**: Ensuring the input falls within minimum and maximum length constraints
   
   (d) **Range**: Ensuring numeric inputs fall within acceptable ranges
   
   (e) **Pattern**: Ensuring string inputs match expected patterns using regular expressions or schema validation
   
   (f) **Required Fields**: Ensuring all required fields are present and non-empty

**6.2** Schema validation using JSON Schema, OpenAPI schemas, or equivalent must be implemented for all structured inputs.

**6.3** Type coercion must be explicitly controlled and validated. Unexpected type conversions must be rejected.

### Article 7: Sanitization Standards

**7.1** All user-supplied input that will be rendered, stored, or executed must be sanitized appropriately for its destination context.

**7.2** HTML Sanitization Requirements:

   (a) HTML input must be sanitized using a well-established sanitization library (e.g., DOMPurify, sanitize-html)
   
   (b) Allowlists must be used to specify permitted HTML elements and attributes
   
   (c) All style attributes must be disallowed or strictly allowlisted
   
   (d) JavaScript URIs (javascript:) must never be permitted
   
   (e) Event handlers must never be permitted

**7.3** SQL Sanitization Requirements:

   (a) All database queries must use parameterized queries or prepared statements
   
   (b) String concatenation or template literals must never be used to build SQL queries
   
   (c) Input values must be properly escaped when dynamic SQL cannot be avoided

**7.4** Command Injection Prevention:

   (a) User input must never be passed directly to system commands, shell commands, or operating system calls
   
   (b) If command execution is absolutely necessary, use strict allowlists for all parameters
   
   (c) Prefer language-native APIs over shell execution

**7.5** Path Traversal Prevention:

   (a) All file paths derived from user input must be validated to ensure they do not escape the intended directory
   
   (b) Use canonicalization functions to resolve symbolic links and relative path references
   
   (c) Implement chroot jails or containerization for file operations

### Article 8: Output Encoding Mandate

**8.1** All output must be encoded appropriately for its destination context to prevent injection attacks.

**8.2** Context-Specific Encoding Requirements:

   (a) **HTML Context**: HTML entity encoding
   
   (b) **JavaScript Context**: JavaScript string encoding with Unicode escaping
   
   (c) **URL Context**: URL encoding (percent-encoding)
   
   (d) **CSS Context**: CSS string encoding with Unicode escaping
   
   (e) **JSON Context**: JSON encoding (automatic in most frameworks)
   
   (f) **XML Context**: XML entity encoding

**8.3** Encoding must be applied at the point of output generation, not at storage.

**8.4** Context-aware auto-escaping features in template engines must be enabled and used.

---

## CHAPTER II: AUTHENTICATION STANDARDS

### Article 9: Authentication Architecture

**9.1** Strong authentication must be implemented for all access to system resources, APIs, and administrative functions.

**9.2** Multi-Factor Authentication (MFA) Requirements:

   (a) MFA must be mandatory for all administrative accounts and privileged access
   
   (b) MFA must be available and strongly recommended for all user accounts
   
   (c) MFA must use at least two different authentication factors from:
       - Something you know (password, PIN)
       - Something you have (hardware token, authenticator app, smart card)
       - Something you are (biometric)
   
   (d) SMS-based OTP is deprecated and should only be used when no better option is available
   
   (e) TOTP (Time-based One-Time Password) or hardware keys are the preferred MFA methods

**9.3** Authentication providers must implement industry-standard protocols (OAuth 2.0, OpenID Connect, SAML).

### Article 10: Password Standards

**10.1** Password Composition Requirements:

   (a) Minimum password length: 12 characters (16+ recommended)
   
   (b) Maximum password length: 128 characters minimum (allow longer for passphrases)
   
   (c) Complexity requirements may be waived if password length exceeds 16 characters
   
   (d) Passwords must not be common passwords, dictionary words, or previously breached passwords

**10.2** Password Storage Requirements:

   (a) Passwords must be hashed using bcrypt, scrypt, Argon2, or PBKDF2 with appropriate work factors
   
   (b) Salt must be unique per password and cryptographically random (minimum 32 bits)
   
   (c) Passwords must never be stored in plain text
   
   (d) Passwords must never be logged or transmitted in plain text
   
   (e) Password hashes must be compared using constant-time comparison functions

**10.3** Password Recovery and Reset:

   (a) Password reset must require identity verification through a separate channel
   
   (b) Password reset tokens must be:
       - Cryptographically random and secure
       - Single-use
       - Time-limited (maximum 15 minutes validity)
       - Bound to the user account and requesting IP address
   
   (c) Upon password reset, all existing sessions must be invalidated
   
   (d) Password reset requests must be rate-limited

**10.4** Password Change Requirements:

   (a) Users must be required to enter their current password when changing to a new password
   
   (b) New passwords must be checked against the previous password and recent password history
   
   (c) Password change must invalidate all sessions except the current one (optional: present option to invalidate all)

### Article 11: Session Management Standards

**11.1** Session Token Requirements:

   (a) Session identifiers must be generated using cryptographically secure random number generators
   
   (b) Session tokens must be at least 128 bits of entropy
   
   (c) Session tokens must be unpredictable and non-sequential
   
   (d) Session tokens must never be reused

**11.2** Session Storage and Transmission:

   (a) Session tokens must only be transmitted over HTTPS (secure channels)
   
   (b) Session tokens must not be transmitted in URLs
   
   (c) Session tokens must be stored securely (httpOnly cookies preferred for browser clients)
   
   (d) Session tokens must not be logged

**11.3** Session Lifecycle Management:

   (a) Sessions must have defined absolute timeouts (recommended: 30 minutes of inactivity)
   
   (b) Sessions must have maximum lifetimes (recommended: 8-24 hours regardless of activity)
   
   (c) Session termination (logout) must:
       - Invalidate the session token server-side
       - Clear the session token from the client
       - Clear any session-scoped cookies
   
   (d) Sessions must be invalidated upon password change
   
   (e) Sessions must be invalidated upon role or permission changes

**11.4** Concurrent Session Management:

   (a) Systems may implement concurrent session limits
   
   (b) When limits are reached, oldest sessions or least recently used sessions must be invalidated
   
   (c) Users must be able to view and terminate their active sessions

### Article 12: Credential Handling

**12.1** Credentials must be handled according to the following principles:

   (a) Credentials must be entered directly into the application, not pasted from password managers that store them insecurely
   
   (b) Password managers integrated via browser APIs must be supported but not required
   
   (c) Show/hide password functionality must be available
   
   (d) Password entry fields must not autocomplete on sensitive forms where inappropriate

**12.2** Credential Transmission:

   (a) Credentials must only be transmitted over encrypted channels (HTTPS with TLS 1.2+)
   
   (b) Credentials must be transmitted in the request body, not in URLs
   
   (c) Credentials must not be logged or stored in access logs

---

## CHAPTER III: AUTHORIZATION STANDARDS

### Article 13: Authorization Architecture

**13.1** Authorization decisions must be enforced at every layer of the application (presentation, business logic, data access).

**13.2** The principle of least privilege must govern all authorization decisions.

**13.3** Authorization logic must be centralized and consistently applied across the application.

**13.4** Deny-by-default: Access must be explicitly granted, not implicitly denied.

### Article 14: Role-Based Access Control (RBAC)

**14.1** Role-Based Access Control (RBAC) must be implemented for managing user permissions.

**14.2** Role Definitions:

   (a) Roles must represent job functions or responsibilities
   
   (b) Roles must be defined based on the principle of least privilege
   
   (c) Roles must be documented with clear descriptions of associated permissions
   
   (d) Role hierarchies must be carefully designed to avoid unintended privilege escalation

**14.3** Role Assignment:

   (a) Role assignments must be approved by authorized personnel
   
   (b) Role assignments must be documented and auditable
   
   (c) Role assignments must be reviewed periodically
   
   (d) Temporary role elevations must be time-limited and require justification

**14.4** Permission Management:

   (a) Permissions must be granular and specific (resource + action)
   
   (b) Permissions must be composable into roles
   
   (c) Permissions must be validated before every protected operation

### Article 15: Attribute-Based Access Control (ABAC)

**15.1** For complex authorization requirements, Attribute-Based Access Control (ABAC) may be implemented in addition to RBAC.

**15.2** Attributes may include:

   (a) User attributes (department, clearance level, location)
   
   (b) Resource attributes (classification, owner, sensitivity)
   
   (c) Environmental attributes (time, location, device health)
   
   (d) Action attributes (read, write, delete, execute)

**15.3** ABAC policies must be defined, documented, and reviewed by security personnel.

### Article 16: Privileged Access Management

**16.1** Privileged accounts (administrators, root, service accounts with elevated permissions) require additional controls:

   (a) Privileged account usage must be logged in detail
   
   (b) Privileged sessions must be monitored and recorded where technically feasible
   
   (c) Privileged access must be time-limited and session-scoped
   
   (d) Emergency access procedures must be documented and tested
   
   (e) Break-glass procedures must be available for critical situations with additional audit requirements

**16.2** Service Account Security:

   (a) Service accounts must have minimal permissions required for their function
   
   (b) Service account credentials must be rotated regularly
   
   (c) Service account credentials must be stored in secure secret management systems
   
   (d) Interactive logins with service accounts must be prohibited or heavily restricted

### Article 17: Resource Authorization

**17.1** Every protected resource must have explicit authorization rules.

**17.2** Resource ownership must be defined and enforced:

   (a) Resources must have designated owners
   
   (b) Resource owners must have special permissions (delegate, revoke, audit)
   
   (c) Resource access must be trackable and auditable

**17.3** Data Access Authorization:

   (a) Access to data must be based on data classification and user clearance
   
   (b) Sensitive data fields may require additional access controls beyond record-level access
   
   (c) Bulk data access must be restricted and monitored

---

## CHAPTER IV: DATA ENCRYPTION MANDATE

### Article 18: Encryption at Rest

**18.1** All sensitive data must be encrypted at rest.

**18.2** Encryption Technologies:

   (a) Database encryption: Use AES-256 or equivalent for database-level encryption
   
   (b) File system encryption: Use dm-crypt/LUKS, FileVault, or equivalent for full disk encryption
   
   (c) Application-level encryption: Sensitive data fields must be encrypted at the application layer
   
   (d) Backup encryption: All backups must be encrypted before leaving the source system

**18.3** Key Management Requirements:

   (a) Encryption keys must be managed separately from encrypted data
   
   (b) Key rotation must be performed according to defined schedules (recommended: annual minimum)
   
   (c) Key escrow procedures must be documented for disaster recovery
   
   (d) Key access must be logged and audited

**18.4** Transparent Data Encryption (TDE):

   (a) Database TDE should be enabled for all database instances
   
   (b) TDE does not replace application-level encryption for highly sensitive fields

### Article 19: Encryption in Transit

**19.1** All data in transit must be encrypted.

**19.2** TLS Requirements:

   (a) TLS 1.2 or higher must be used for all encrypted connections
   
   (b) TLS 1.0 and TLS 1.1 must be deprecated and disabled where possible
   
   (c) TLS 1.3 is recommended where supported
   
   (d) Perfect Forward Secrecy (PFS) must be enabled
   
   (e) Weak cipher suites must be disabled (SSL, RC4, MD5, SHA1 for signatures)

**19.3** Certificate Management:

   (a) Certificates must be obtained from trusted Certificate Authorities
   
   (b) Certificate validation must verify the entire certificate chain
   
   (c) Certificate expiration must be monitored and certificates renewed before expiration
   
   (d) Certificate pinning may be implemented for high-security applications with appropriate fallback procedures

**19.4** Internal Service Communication:

   (a) Service-to-service communication within the network should use mutual TLS (mTLS) where possible
   
   (b) Internal services should use private certificate authorities

### Article 20: Field-Level Encryption

**20.1** Highly sensitive individual fields must use application-level encryption in addition to storage-level encryption.

**20.2** Fields requiring field-level encryption include:

   (a) Social Security Numbers or national identifiers
   
   (b) Financial account numbers
   
   (c) Health information (PHI)
   
   (d) Authentication credentials (in addition to hashing)
   
   (e) API keys and secrets
   
   (f) Personal identifying information as defined by privacy regulations

**20.3** Searchable Encryption Considerations:

   (a) Encrypted fields may use deterministic encryption for searchability where needed
   
   (b) Searchable encryption implementations must be reviewed by security specialists

---

## CHAPTER V: SECRET MANAGEMENT STANDARDS

### Article 21: Secret Definition

**21.1** The following are classified as secrets requiring special handling:

   (a) Database credentials (usernames, passwords, connection strings)
   
   (b) API keys and tokens
   
   (c) Encryption keys and certificates
   
   (d) SSH keys and private keys
   
   (e) Service account credentials
   
   (f) Integration passwords and tokens
   
   (g) Application secrets (session keys, signing keys)

### Article 22: Secret Storage Requirements

**22.1** Secrets must be stored in purpose-built secret management systems.

**22.2** Approved Secret Management Systems:

   (a) HashiCorp Vault (preferred)
   
   (b) AWS Secrets Manager
   
   (c) Azure Key Vault
   
   (d) Google Cloud Secret Manager
   
   (e) Kubernetes Secrets (with additional controls)

**22.3** Prohibited Secret Storage:

   (a) Source code or version control
   
   (b) Configuration files committed to repositories
   
   (c) Environment variables in container images
   
   (d) Plain text files on servers
   
   (e) Documentation or wikis

**22.4** Secret Rotation:

   (a) Secrets must be rotated according to defined schedules
   
   (b) Emergency rotation procedures must be documented
   
   (c) Rotation must not cause service disruption (using versioned secrets)

### Article 23: Secret Access Controls

**23.1** Access to secrets must be:

   (a) Restricted to explicitly authorized services and personnel
   
   (b) Logged with timestamps, identities, and purposes
   
   (c) Time-limited where possible
   
   (d) Reviewed quarterly

**23.2** Secret Access Patterns:

   (a) Applications must retrieve secrets at startup from secret management systems
   
   (b) Long-lived secrets should be refreshed periodically without restart where possible
   
   (c) Applications must handle secret rotation gracefully

### Article 24: Secret Handling in Code

**24.1** Code must never contain hardcoded secrets.

**24.2** Code must use secret references that are resolved at runtime.

**24.3** Secret injection via environment variables is acceptable but variables must not be logged or exposed.

**24.4** CI/CD Pipeline Secret Handling:

   (a) Secrets must be injected into build and deployment environments securely
   
   (b) Secrets must not be exposed in build logs or artifacts
   
   (c) Build containers must not persist secrets after build completion

---

## CHAPTER VI: CORS STANDARDS

### Article 25: Cross-Origin Resource Sharing (CORS) Policy

**25.1** CORS configurations must follow the principle of least privilege.

**25.2** Allowed Origins:

   (a) Allowed origins must be explicitly enumerated, not wildcards (except for specific documented use cases)
   
   (b) Origin validation must use exact string matching, not prefix matching
   
   (c) Dynamic origin validation based on allowlists must be implemented for multi-tenant scenarios

**25.3** Prohibited CORS Configurations:

   (a) Access-Control-Allow-Origin: * must never be used for APIs handling sensitive data
   
   (b) Access-Control-Allow-Credentials: true must never be used with wildcard origins

**25.4** Allowed Methods and Headers:

   (a) Only necessary HTTP methods must be allowed
   
   (b) Only necessary headers must be allowed in Access-Control-Allow-Headers
   
   (c) Exposure of sensitive headers via Access-Control-Expose-Headers must be minimized

**25.5** CORS Preflight Caching:

   (a) Access-Control-Max-Age should be set to reasonable values to reduce preflight requests
   
   (b) Maximum preflight cache time should not exceed 24 hours

---

## CHAPTER VII: RATE LIMITING MANDATE

### Article 26: Rate Limiting Architecture

**26.1** Rate limiting must be implemented at multiple layers:

   (a) API Gateway level
   
   (b) Application level
   
   (c) Database connection level

**26.2** Rate Limiting Strategy:

   (a) Implement progressive rate limiting (e.g., 100 requests/minute, 1000 requests/hour, 10000 requests/day)
   
   (b) Different limits for different endpoint categories (read vs. write, authenticated vs. anonymous)
   
   (c) Per-user, per-IP, and per-endpoint rate limiting

**26.3** Rate Limit Headers:

   (a) Include X-RateLimit-Limit header in responses
   
   (b) Include X-RateLimit-Remaining header in responses
   
   (c) Include X-RateLimit-Reset header in responses
   
   (d) Include Retry-After header when rate limit is exceeded

### Article 27: Rate Limit Responses

**27.1** When rate limits are exceeded:

   (a) Return HTTP 429 (Too Many Requests) status code
   
   (b) Return descriptive error message in response body
   
   (c) Log rate limit violations for security monitoring
   
   (d) Consider temporary IP or account blocking for repeated violations

**27.2** Graceful Degradation:

   (a) Services should implement graceful degradation under high load
   
   (b) Rate limiting should prioritize critical operations over non-critical ones

---

## CHAPTER VIII: SQL INJECTION PREVENTION

### Article 28: SQL Injection Defense

**28.1** Parameterized Queries (Prepared Statements):

   (a) All database queries must use parameterized queries or prepared statements
   
   (b) Query structure must never include user input
   
   (c) Parameter values must never be interpolated into SQL strings

**28.2** ORM Usage:

   (a) ORMs may be used but must be configured to use parameterized queries
   
   (b) Raw SQL queries through ORMs must also use parameterized queries
   
   (c) ORM query builder must be reviewed for injection vulnerabilities

**28.3** Query Validation:

   (a) Dynamic table/column names derived from user input must be validated against allowlists
   
   (b) ORDER BY, GROUP BY, and other clauses with dynamic values must be validated

**28.4** Error Handling:

   (a) Database errors must never be exposed to users
   
   (b) Generic error messages must be displayed while logging detailed errors internally
   
   (c) SQL syntax must not be revealed in error messages

---

## CHAPTER IX: XSS PREVENTION MANDATE

### Article 29: Cross-Site Scripting (XSS) Prevention

**29.1** Context-Aware Output Encoding:

   (a) All user-generated content must be encoded for its output context
   
   (b) HTML encoding for HTML contexts
   
   (c) JavaScript encoding for script contexts
   
   (d) URL encoding for URL contexts
   
   (e) CSS encoding for style contexts

**29.2** Content Security Policy (CSP):

   (a) CSP headers must be implemented to mitigate XSS attacks
   
   (b) CSP must restrict script sources to trusted origins
   
   (c) Inline scripts and eval() must be prohibited where possible
   
   (d) CSP must be tested thoroughly before deployment

**29.3** HTTPOnly and Secure Flags:

   (a) Cookies containing sensitive data must have HttpOnly flag set
   
   (b) Cookies transmitted over HTTPS must have Secure flag set

**29.4** Input Sanitization:

   (a) Rich text input requiring HTML must use allowlist-based sanitization
   
   (b) All event handlers and JavaScript URIs must be stripped from HTML input

### Article 30: DOM-Based XSS Prevention

**30.1** Client-Side JavaScript Security:

   (a) Never use user input in dangerous DOM methods:
       - innerHTML
       - outerHTML
       - document.write()
       - eval()
       - setTimeout/setInterval with string arguments
   
   (b) Prefer safe alternatives:
       - textContent
       - innerText
       - createTextNode()
       - text/template

**30.2** URL Handling:

   (a) User-controlled URLs must be validated before use
   
   (b) javascript: URLs must be blocked regardless of context
   
   (c) Use URL parsing libraries rather than string manipulation

---

## CHAPTER X: CSRF PREVENTION MANDATE

### Article 31: Cross-Site Request Forgery (CSRF) Prevention

**31.1** CSRF Tokens:

   (a) Anti-CSRF tokens must be implemented for all state-changing operations
   
   (b) Tokens must be:
       - Cryptographically random and unpredictable
       - Tied to the user's session
       - Validated on every state-changing request
   
   (c) Tokens must be transmitted via:
       - Custom request header (preferred)
       - Request body parameter (for form submissions)

**31.2** Same-Site Cookies:

   (a) Cookies for state-changing operations must have SameSite=Strict or SameSite=Lax
   
   (b) SameSite=None requires Secure flag and must only be used for cross-origin needs

**31.3** Origin Validation:

   (a) Validate Origin and Referer headers for cross-origin requests
   
   (b) Require explicit whitelist of allowed origins for sensitive operations

**31.4** Additional CSRF Mitigations:

   (a) Implement double-submit cookie pattern as additional layer
   
   (b) Consider Custom Header requirement for API endpoints (browsers can't set custom headers cross-origin without CORS)

---

## CHAPTER XI: SECURITY HEADERS MANDATE

### Article 32: Required Security Headers

**32.1** The following security headers must be implemented:

   (a) **Strict-Transport-Security (HSTS)**:
       - Minimum: max-age=31536000; includeSubDomains
       - Recommended: max-age=63072000; includeSubDomains; preload
   
   (b) **X-Content-Type-Options**: nosniff
   
   (c) **X-Frame-Options**: DENY or SAMEORIGIN
   
   (d) **X-XSS-Protection**: 1; mode=block (legacy browsers; CSP is primary defense)
   
   (e) **Referrer-Policy**: strict-origin-when-cross-origin or no-referrer
   
   (f) **Permissions-Policy**: Restrict available features to necessary ones only

**32.2** Content-Security-Policy Header:

   (a) Implement CSP to control resource loading and execution
   
   (b) Default-src directive must be set to 'none' or strict allowlist
   
   (c) Script-src must not allow 'unsafe-inline' or 'unsafe-eval'
   
   (d) Style-src must not allow 'unsafe-inline' where possible
   
   (e) img-src, font-src, connect-src, frame-src must be explicitly allowlisted

### Article 33: Cache-Control for Sensitive Data

**33.1** Responses containing sensitive data must include appropriate Cache-Control headers:

   (a) No-store for highly sensitive data
   
   (b) No-cache with revalidation for moderately sensitive data
   
   (c) Private cache directives for user-specific data

---

## CHAPTER XII: VULNERABILITY MANAGEMENT

### Article 34: Vulnerability Assessment

**34.1** Regular vulnerability assessments must be conducted:

   (a) Automated scanning: Weekly minimum
   
   (b) Manual penetration testing: Annual minimum
   
   (c) Code review for security: During every significant release
   
   (d) Dependency scanning: With every build

**34.2** Vulnerability Scanning Requirements:

   (a) Use multiple scanning tools for comprehensive coverage
   
   (b) Scan all environments (development, staging, production)
   
   (c) Maintain asset inventory for complete scanning coverage

**34.3** Penetration Testing Standards:

   (a) Engage qualified third-party testers annually
   
   (b) Include OWASP Top 10 and SANS Top 25 in test scope
   
   (c) Test both external and internal attack vectors
   
   (d) Document and remediate findings according to severity

### Article 35: Vulnerability Remediation

**35.1** Remediation SLAs based on severity:

   (a) Critical: Within 24 hours
   
   (b) High: Within 7 days
   
   (c) Medium: Within 30 days
   
   (d) Low: Within 90 days

**35.2** Emergency Patch Procedures:

   (a) Maintain capability for emergency security patches
   
   (b) Emergency patches must still be tested before deployment
   
   (c) Rollback procedures must be documented and tested

### Article 36: Dependency Management

**36.1** Dependency Security:

   (a) Maintain an inventory of all dependencies (libraries, frameworks, packages)
   
   (b) Monitor dependencies for known vulnerabilities using automated tools
   
   (c) Update dependencies regularly, prioritizing security updates
   
   (d) Remove unused dependencies to reduce attack surface

**36.2** Dependency Update Policy:

   (a) Security updates: Apply within SLA based on severity
   
   (b) Major version updates: Test thoroughly within 3 months
   
   (c) Regular updates: Monthly review minimum

---

## CHAPTER XIII: COMPLIANCE MANDATE

### Article 37: GDPR Compliance

**37.1** Lawfulness of Processing:

   (a) All personal data processing must have a valid legal basis
   
   (b) Legal bases include: consent, contract, legitimate interest, legal obligation, vital interests, public task
   
   (c) Processing purposes must be documented and communicated

**37.2** Data Subject Rights:

   (a) Right to access: Provide mechanisms for data subjects to access their data
   
   (b) Right to rectification: Allow correction of inaccurate data
   
   (c) Right to erasure: Implement mechanisms for data deletion upon valid requests
   
   (d) Right to data portability: Provide data in machine-readable formats
   
   (e) Right to object: Provide mechanisms to object to processing
   
   (f) Rights related to automated decision-making: Provide human review options

**37.3** Data Protection by Design and Default:

   (a) Privacy must be considered from the initial design phase
   
   (b) Default settings must be privacy-preserving
   
   (c) Data minimization: Collect only necessary data
   
   (d) Purpose limitation: Use data only for stated purposes

**37.4** Data Protection Impact Assessments (DPIA):

   (a) Conduct DPIA for high-risk processing activities
   
   (b) Document processing activities in Records of Processing Activities (RoPA)

**37.5** Breach Notification:

   (a) Report breaches to supervisory authority within 72 hours
   
   (b) Notify affected individuals when high risk to their rights

### Article 38: PCI DSS Compliance

**38.1** PCI DSS Scope:

   (a) Identify all systems that store, process, or transmit cardholder data
   
   (b) Minimize cardholder data storage according to business needs
   
   (c) Never store sensitive authentication data post-authorization

**38.2** PCI DSS Requirements:

   (a) Install and maintain network security controls
   
   (b) Protect stored cardholder data with strong encryption
   
   (c) Maintain vulnerability management program
   
   (d) Implement strong access control measures
   
   (e) Monitor and test networks regularly
   
   (f) Maintain information security policies

**38.3** Tokenization and Point-to-Point Encryption:

   (a) Use tokenization to minimize cardholder data in systems
   
   (b) Use validated point-to-point encryption solutions

### Article 39: Additional Compliance Requirements

**39.1** SOC 2 Compliance (if applicable):

   (a) Implement controls addressing Trust Service Criteria:
       - Security
       - Availability
       - Processing integrity
       - Confidentiality
       - Privacy

**39.2** HIPAA Compliance (if handling health information):

   (a) Implement administrative, physical, and technical safeguards
   
   (b) Ensure Business Associate Agreements are in place
   
   (c) Implement breach notification procedures

**39.3** Industry-Specific Regulations:

   (a) Identify and comply with industry-specific security requirements
   
   (b) Maintain compliance documentation for audits

---

## CHAPTER XIV: SECURITY OPERATIONS

### Article 40: Security Monitoring

**40.1** Logging Requirements:

   (a) Log all authentication events (success and failure)
   
   (b) Log all authorization decisions for sensitive operations
   
   (c) Log all administrative actions
   
   (d) Log all data access to sensitive data
   
   (e) Log all security-relevant configuration changes
   
   (f) Log all system errors and exceptions

**40.2** Log Standards:

   (a) Logs must include: timestamp, user identity, action, resource, result, source IP
   
   (b) Logs must be immutable and tamper-evident
   
   (c) Logs must be retained according to retention policies
   
   (d) Logs must be protected from unauthorized access

**40.3** Security Information and Event Management (SIEM):

   (a) Implement SIEM solution for log aggregation and analysis
   
   (b) Configure alerting for security-relevant events
   
   (c) Conduct regular log review and analysis

### Article 41: Incident Response

**41.1** Incident Response Plan:

   (a) Documented incident response procedures must exist
   
   (b) Define incident classification and severity levels
   
   (c) Define roles and responsibilities during incidents
   
   (d) Establish communication procedures and escalation paths

**41.2** Incident Detection:

   (a) Implement automated detection for common attack patterns
   
   (b) Configure alerts for anomalous behavior
   
   (c) Establish monitoring for security-relevant events

**41.3** Incident Response Phases:

   (a) **Preparation**: Train response team, maintain tools and contacts
   
   (b) **Detection and Analysis**: Identify, classify, and analyze incidents
   
   (c) **Containment**: Limit incident scope and prevent spread
   
   (d) **Eradication**: Remove threat from environment
   
   (e) **Recovery**: Restore systems and services
   
   (f) **Post-Incident**: Document lessons learned, update procedures

**41.4** Incident Response Timeframes:

   (a) Critical incidents: Response within 1 hour
   
   (b) High severity: Response within 4 hours
   
   (c) Medium severity: Response within 24 hours
   
   (d) Low severity: Response within 5 business days

---

## CHAPTER XV: SECURITY AUDIT AND GOVERNANCE

### Article 42: Security Audits

**42.1** Audit Requirements:

   (a) Conduct internal security audits quarterly
   
   (b) Conduct external security audits annually
   
   (c) Maintain audit reports and remediation plans
   
   (d) Track audit findings to resolution

**42.2** Compliance Audits:

   (a) Maintain evidence of compliance with all applicable regulations
   
   (b) Conduct regular compliance self-assessments
   
   (c) Prepare for external audits with organized evidence

### Article 43: Security Governance

**43.1** Security Policies:

   (a) Maintain documented security policies covering all aspects of this skill
   
   (b) Review and update policies annually minimum
   
   (c) Communicate policies to all personnel
   
   (d) Require acknowledgment of policy compliance

**43.2** Security Training:

   (a) Provide security awareness training to all personnel
   
   (b) Provide role-specific security training for developers and administrators
   
   (c) Conduct phishing simulations and awareness exercises
   
   (d) Track training completion and effectiveness

**43.3** Security Metrics:

   (a) Track key security metrics:
       - Mean time to detect (MTTD)
       - Mean time to respond (MTTR)
       - Number of vulnerabilities by severity
       - Patch compliance percentage
       - Security training completion rate
   
   (b) Report metrics to leadership regularly

---

## SCHEDULES AND ANNEXURES

### Schedule I: Security Checklist

**Pre-Deployment Security Checklist:**

- [ ] Input validation implemented and tested
- [ ] Output encoding implemented for all contexts
- [ ] Authentication properly implemented (passwords hashed, MFA available)
- [ ] Session management with secure defaults
- [ ] Authorization model defined and implemented
- [ ] Encryption at rest enabled
- [ ] Encryption in transit enabled (TLS 1.2+)
- [ ] Secrets removed from code and configuration
- [ ] CORS configured with minimal allowed origins
- [ ] Rate limiting implemented
- [ ] Security headers implemented
- [ ] CSP implemented
- [ ] CSRF tokens implemented
- [ ] Security logging enabled
- [ ] Dependencies scanned for vulnerabilities
- [ ] Security review completed

### Schedule II: Encryption Algorithm Standards

**Approved Algorithms:**

- Symmetric Encryption: AES-256-GCM (preferred), AES-256-CBC
- Asymmetric Encryption: RSA-2048 minimum, RSA-4096 preferred, ECC (P-256, P-384)
- Hashing: SHA-256 minimum, SHA-384 preferred
- Password Hashing: Argon2id (preferred), bcrypt, scrypt, PBKDF2
- HMAC: HMAC-SHA-256 minimum
- Key Derivation: HKDF, PBKDF2

**Deprecated/Prohibited:**

- DES, 3DES
- RC4
- MD5 (except for non-security purposes)
- SHA-1 (except for non-security purposes)
- SSL (all versions)
- TLS 1.0, TLS 1.1
- Export-grade ciphers

### Schedule III: Security Testing Tools

**Recommended Security Testing Tools:**

- Static Application Security Testing (SAST): SonarQube, Semgrep, CodeQL
- Dynamic Application Security Testing (DAST): OWASP ZAP, Burp Suite
- Software Composition Analysis (SCA): Snyk, Dependabot, OWASP Dependency-Check
- Interactive Application Security Testing (IAST): Contrast Security
- Secret Scanning: GitGuardian, TruffleHog
- Infrastructure Scanning: Nessus, OpenVAS

---

## ENFORCEMENT AND INTERPRETATION

### Article 44: Enforcement

**44.1** All requirements in this skill are MANDATORY unless explicitly stated as RECOMMENDED.

**44.2** Violations of mandatory requirements must be documented and remediated according to severity.

**44.3** Significant security violations may result in service deployment blocks.

### Article 45: Interpretation

**45.1** In case of ambiguity, security considerations shall prevail over convenience.

**45.2** New security threats may require immediate implementation of additional controls not explicitly stated in this document.

**45.3** Interpretation guidance may be provided by the Security team.

### Article 46: Updates and Amendments

**46.1** This skill must be reviewed quarterly and updated as needed.

**46.2** Emergency amendments may be issued by the Security team in response to emerging threats.

**46.3** All changes must be communicated to affected teams with adequate notice for implementation.

---

## APPENDIX: SECURITY COMPLIANCE SCRIPTS

### check-secrets.js

Scans files for potential secrets and credentials using pattern matching.

**Usage:**
```bash
node scripts/check-secrets.js [path] [-r] [-v]
```

**Options:**
- `-r, --recursive`: Scan directories recursively
- `-v, --verbose`: Include full context in output

**Patterns Detected:**
- AWS credentials
- GitHub tokens
- Bearer/JWT tokens
- Private keys (SSH, GPG)
- API keys for 25+ services
- Connection strings with passwords

**Output:** JSON report with severity levels

**Exit Code:** 1 if secrets found

**Severity Levels:**
| Level | Description |
|-------|-------------|
| Critical | Private keys, production API keys |
| High | API keys, tokens, passwords |
| Medium | Basic auth, publishable keys |
| Low | Placeholder patterns |

---

*End of Part IX: Security and Compliance*
