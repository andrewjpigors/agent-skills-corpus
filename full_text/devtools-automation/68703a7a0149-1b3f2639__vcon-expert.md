---
name: vcon-expert
description: Comprehensive vCon (Virtualized Conversations) expert system for validation, analysis, Q&A, and multi-language code generation (Go, Typescript, Python). Based on latest IETF draft specifications with deep knowledge of vCon architecture, extensions, and use cases.
---

# vCon Expert - Complete Conversational Data Container Specialist

## ⚠️ CRITICAL: How to Access Documentation

**This skill includes IETF specification documents in its `vcon-documentation/` subdirectory.**

When performing any vCon operations, Claude MUST:
- ✅ Read docs from `./vcon-documentation/` (relative path within the skill)
- ✅ Use `Filesystem:read_file` tool with skill-relative paths
- ❌ NEVER read from `/mnt/project/` or user's local filesystem
- ❌ NEVER use absolute paths like `/home/`, `/Users/`, etc.

**Correct Example:**
```
Filesystem:read_file("./vcon-documentation/draft-ietf-vcon-vcon-core-02")
```

**Files bundled in this skill:**
- `./vcon-documentation/draft-ietf-vcon-vcon-core-02` - Core spec (v0.4.0)
- `./vcon-documentation/draft-ietf-vcon-cc-extension-01` - Contact Center extension
- `./vcon-documentation/draft-ietf-vcon-privacy-primer-00` - Privacy considerations
- `./vcon-documentation/draft-howe-vcon-wtf-extension-01` - World Transcription Format extension
- `./vcon-documentation/draft-miller-vcon-zip-bundle-00` - ZIP Bundle packaging format
- `./vcon-documentation/_draft-ietf-vcon-mimi-messages-00` - MIMI messaging extension
- `./vcon-documentation/_draft-ietf-vcon-overview-00` - Overview and use cases

## Overview

This skill provides **comprehensive expertise on vCon (Virtualized Conversations)**, the IETF standard for exchanging conversational data. It combines validation capabilities with deep knowledge to answer questions, provide guidance, and generate production-ready code in multiple languages.

**Primary Capabilities:**
1. **Validation & Compliance** - Validate vCon files against IETF standards
2. **Expert Q&A** - Answer detailed questions about vCon structure, use cases, and best practices
3. **Multi-Language Code Generation** - Generate Go, JavaScript, and Python implementations
4. **Architecture Guidance** - Provide system design advice for vCon integration
5. **Extension Support** - Explain and implement vCon extensions (CC, MIMI, WTF, etc.)

**When to Use This Skill:**
- Any question about vCons, their structure, or usage
- Validating vCon JSON files for compliance
- Generating code to work with vCons in Go, JavaScript, or Python
- Understanding vCon extensions and their applications
- Designing systems that integrate conversational data
- Privacy and security considerations for conversation handling
- Contact center, messaging, or emergency communication use cases

## Latest vCon Specification (v0.4.0)

### Current Version Status
- **Active Draft**: draft-ietf-vcon-vcon-core-02 (January 2026)
- **Version**: 0.4.0 (moving toward v1.0)
- **Working Group**: IETF Virtualized Conversations (vcon)
- **Status**: Internet-Draft (Standards Track)

### Key Updates from Latest IETF Documents

**Version Field Change:**
- The `vcon` field MUST have value `"0.4.0"`
- Working toward semantic versioning in future releases

**New Parameters:**
- `critical`: "String[]" - Lists incompatible extensions that MUST be supported (renamed from `must_support`)
- `did`: Decentralized Identifier support added to Party Object
- `product`: New Analysis Object parameter to identify vendor products
- `timezone`: New Party Object parameter for party location timezone

**Extension Framework Enhancements:**
- Compatible vs. Incompatible extension classification
- Extensions listed in `critical` MUST be supported to correctly interpret the vCon
- New IANA registries for vCon parameters and extensions
- Standardized extension naming conventions

**Media Type Registration:**
- `application/vcon+json` - Standard JSON vCon
- `application/vcon+gzip` - Compressed vCon format
- `application/vcon+zip` - vCon ZIP Bundle (.vconz) format

## Core vCon Architecture

### Three Forms of vCon

vCons exist in three distinct security forms:

1. **Unsigned Form** - Mutable, in-progress vCon for data collection
   - Contains: `parties`, `dialog`, `analysis`, `attachments` arrays
   - Use: During conversation capture and before export

2. **Signed Form (JWS)** - Immutable, integrity-protected vCon
   - Contains: `payload` (base64url encoded unsigned vCon) and `signatures`
   - Use: When crossing security domains or for audit trails

3. **Encrypted Form (JWE)** - Confidential, privacy-protected vCon
   - Contains: `ciphertext` (encrypted signed vCon) and `recipients`
   - Use: When containing PII or sensitive conversation data

### Required Top-Level Fields

```json
{
  "vcon": "0.4.0",
  "uuid": "018c8a7e-5f3d-8000-9a2b-3c4d5e6f7a8b",
  "created_at": "2025-10-20T14:30:00.000Z",
  "parties": [...]
}
```

### Optional Top-Level Fields

```json
{
  "extensions": ["CC", "MIMI"],
  "critical": ["CUSTOM-EXTENSION"],
  "updated_at": "2025-10-20T15:45:00.000Z",
  "subject": "Customer support call regarding order #12345",
  "dialog": [...],
  "analysis": [...],
  "attachments": [...],
  "redacted": {...},
  "amended": {...},
  "group": [...]
}
```

## vCon Object Model

### Party Object

Represents participants in the conversation:

```json
{
  "tel": "+1-555-0100",
  "sip": "user@example.com",
  "mailto": "user@example.com",
  "name": "Alice Smith",
  "did": "did:example:123456789abcdefghi",
  "uuid": "550e8400-e29b-41d4-a716-446655440000",
  "validation": "SSN-last-4",
  "gmlpos": "40.7128 -74.0060",
  "civicaddress": {
    "country": "US",
    "a1": "NY",
    "a3": "New York",
    "pc": "10001"
  },
  "timezone": "America/New_York"
}
```

### Dialog Object

Contains conversation media (text, audio, video):

```json
{
  "type": "recording",
  "start": "2025-10-20T14:30:00.000Z",
  "duration": 180.5,
  "parties": [0, 1],
  "originator": 0,
  "mediatype": "audio/x-wav",
  "filename": "call-recording.wav",
  "encoding": "base64url",
  "body": "UklGRn4...",
  "disposition": "resolved",
  "session_id": "a84b23a9cdef...",
  "application": "Zoom",
  "message_id": "msg_123456"
}
```

**Dialog Types:**
- `recording` - Audio/video recording
- `text` - Text message or chat
- `transfer` - Call transfer metadata (no media)
- `incomplete` - Failed connection attempt

### Analysis Object

Post-conversation analysis results:

```json
{
  "type": "transcript",
  "dialog": [0],
  "mediatype": "application/json",
  "vendor": "OpenAI",
  "product": "Whisper",
  "schema": "v3",
  "encoding": "json",
  "body": "{\"segments\": [...]}"
}
```

**Analysis Types:**
- `report` - General analysis report
- `summary` - Conversation summary
- `transcript` - Speech-to-text transcription
- `translation` - Language translation
- `sentiment` - Sentiment analysis
- `tts` - Text-to-speech generation

### Attachment Object

Related documents and files:

```json
{
  "purpose": "contract",
  "start": "2025-10-20T14:35:00.000Z",
  "party": 0,
  "dialog": 0,
  "mediatype": "application/pdf",
  "filename": "contract-v2.pdf",
  "url": "https://example.com/files/contract-v2.pdf",
  "content_hash": "SHA-512:z4PhNX7vuL..."
}
```

## vCon ZIP Bundle Format (.vconz)

### Overview

The vCon ZIP Bundle (.vconz) format provides a standardized way to package one or more vCons with their associated media files into a single, self-contained archive. This addresses the challenge of external file dependencies while enabling offline processing and simplified distribution.

**Key Features:**
- **Self-containment**: All referenced files included in the archive
- **Multi-vCon support**: Bundle multiple related vCons with automatic deduplication
- **Integrity preservation**: Original content hashes maintained for verification
- **Platform independence**: Standard ZIP format supported everywhere
- **Simplicity**: Flat structure with hash-based file naming
- **Offline processing**: No network dependencies after bundle creation

### Bundle Structure

```
bundle.vconz
├── manifest.json                    # Bundle format identifiers
├── files/                          # All media files (flat, deduplicated)
│   ├── sha512-GLy6IPa...UQ.wav    # Hash-named with extensions
│   ├── sha512-Def456...XYZ.pdf
│   └── sha512-Transcript...ABC.json
├── vcons/                          # All vCon JSON files
│   ├── 0195544a-b9b1-8ee4-b9a2-279e0d16bc46.json
│   └── 01955450-1234-5678-9abc-def012345678.json
└── extensions/                     # Future vCon extensions (optional)
    └── [extension-name]/
        ├── metadata.json
        └── files/
            └── sha256-ExtData...GHI.cbor
```

### Core Components

#### manifest.json

Minimal bundle metadata:
```json
{
  "format": "vcon-bundle",
  "version": "1.0"
}
```

#### vCon Files

- Stored as `vcons/[uuid].json`
- Complete, original vCon in any security form (unsigned, signed JWS, encrypted JWE)
- All external URL references and content_hash values preserved exactly as received

#### Media Files

- Stored in flat `files/` directory
- Named using pattern: `[hash-algorithm]-[base64url-hash].[extension]`
- Example: `sha512-GLy6IPaIUM1GqzZqfIPZlWjaDsNgNvZM...UQ.wav`
- Automatic deduplication: identical content (same hash) stored only once

### File Naming Conventions

**Hash-Based Filenames:**
- Format: `[algorithm]-[hash].[extension]`
- SHA-512 MUST be supported (primary algorithm)
- Additional algorithms MAY be supported
- Extensions determined by:
  1. MIME type from vCon mediatype field (preferred)
  2. Content analysis (magic bytes)
  3. Original URL extension
  4. Generic `.bin` if undetermined

**Multi-Hash Support:**
When a vCon has multiple content hashes:
- Use first hash for filename generation
- Prefer SHA-512 if present in array
- Verify ALL hashes during creation and extraction

### Bundle Creation Process

**For Unsigned vCons:**
1. Parse JSON to identify external references
2. Download files from HTTPS URLs
3. Verify content hashes (ALL algorithms)
4. Store in files/ directory with hash-based names
5. Preserve original vCon JSON

**For Signed vCons (JWS):**
1. Preserve complete JWS structure
2. Decode payload to identify external references
3. Resolve and bundle external files
4. Save original JWS structure (not payload)

**For Encrypted vCons (JWE):**
1. Preserve complete JWE structure
2. If decryption keys available: decrypt, resolve files, re-encrypt
3. If keys unavailable: include encrypted vCon without resolving files
4. Save original JWE structure

**Multi-vCon Bundling:**
1. Collect all vCons to include
2. Resolve files for each vCon
3. Automatic deduplication by content_hash
4. Store each vCon as vcons/[uuid].json
5. Include referenced vCons (via Group objects) when available

### Bundle Extraction and Usage

**Extraction Process:**
1. Extract ZIP to directory
2. Validate bundle structure (manifest.json, vcons/, files/)
3. Verify bundle format and version
4. Discover vCons by scanning vcons/ directory
5. For each vCon:
   - Parse according to security form
   - Identify file references via content_hash
   - Verify files exist in files/
   - Verify file integrity using content_hash

**File Resolution:**
```javascript
// To resolve a file from a vCon:
const contentHash = "sha512-GLy6IPa...UQ";
const mediatype = "audio/wav";
const extension = getExtension(mediatype); // .wav
const filePath = `files/${contentHash}.${extension}`;
```

### vCon References and Relationships

**Group Objects:**
vCons may reference other vCons through Group Objects. When bundling:
- Referenced vCons SHOULD be included as separate files
- Group Object's uuid field enables discovery
- Bundle readers check for content_hash in files/ before external resolution

**Reference Discovery:**
1. Scan vcons/ directory for all *.json files
2. For each vCon, check group[] array for uuid fields
3. Verify referenced vCons present in bundle
4. Build relationship graph

### Security Considerations

**Content Verification:**
- All files MUST be verified against ALL content_hash values
- Bundle creators MUST validate HTTPS certificates
- SHA-512 MUST be supported
- Hash verification failure MUST fail bundle creation

**Security Form Preservation:**
- Signed vCons: Preserve complete JWS, verify signatures
- Encrypted vCons: Preserve complete JWE, never downgrade
- Bundle creators MUST NOT modify vCon content or remove signatures

**Privacy Protection:**
- Preserve privacy controls from original vCons
- Maintain redaction integrity
- Handle party identification per privacy regulations
- ZIP-level encryption MAY be used but doesn't replace vCon-level security

**File Deduplication Security:**
- Same hash = identical content (cryptographic guarantee)
- No information leakage from file reuse
- Each vCon's content_hash independently verifiable

### Bundle Validation

Bundle creators MUST validate:
1. Hash verification (all content hashes match)
2. File completeness (all external references resolved)
3. Security form integrity (signatures/encryption intact)
4. UUID uniqueness (no duplicate vCon UUIDs)
5. File accessibility (all files referenced by at least one vCon)
6. Manifest validity (valid JSON with required fields)

### Extension Support

The `extensions/` directory supports future vCon extensions:

```
extensions/
└── [extension-name]/
    ├── metadata.json      # Extension metadata and schema
    └── files/            # Extension-specific files
        └── [hash-names]  # Following same naming conventions
```

**Extension Metadata:**
```json
{
  "extension_name": "mimi-messages",
  "extension_version": "1.0",
  "vcon_version_compatibility": ["0.4.0"],
  "bundle_format_version": "1.0",
  "description": "MIMI protocol message support for vCon"
}
```

### Bundle Examples

#### Single vCon Bundle
```
simple-call.vconz
├── manifest.json
├── files/
│   ├── sha512-GLy6IPa...UQ.wav
│   └── sha512-Transcript...XYZ.json
└── vcons/
    └── 0195544a-b9b1-8ee4-b9a2-279e0d16bc46.json
```

#### Multi-vCon Bundle with Deduplication
```
support-case.vconz
├── manifest.json
├── files/
│   ├── sha512-Call1Audio...ABC.wav
│   ├── sha512-Call2Audio...DEF.wav
│   ├── sha512-SharedDoc...GHI.pdf    # Referenced by both vCons!
│   ├── sha512-Transcript1...JKL.json
│   └── sha512-Transcript2...MNO.json
└── vcons/
    ├── 0195544a-b9b1-8ee4-b9a2-279e0d16bc46.json
    └── 0195544b-c2d3-4e5f-6a7b-8c9d0e1f2a3b.json
```

#### Redacted vCon Bundle
```
redacted-call.vconz
├── manifest.json
├── files/
│   ├── sha512-RedactedAudio...ABC.wav
│   ├── sha512-OriginalAudio...DEF.wav
│   └── sha512-RedactedTranscript...GHI.json
└── vcons/
    ├── 01955460-aaaa-bbbb-cccc-ddddeeeeeeee.json  # Original
    └── 01955461-ffff-gggg-hhhh-iiiijjjjkkkk.json  # Redacted
```

### Implementation Requirements

**MUST Support:**
- Multi-vCon bundling with automatic deduplication
- All vCon content arrays (parties, dialog, analysis, attachments)
- All three security forms (unsigned, signed JWS, encrypted JWE)
- SHA-512 content hash verification
- Hash-based file naming with extension determination
- Standard ZIP format with specified structure
- vCon discovery via vcons/ directory scanning
- File lookup via content_hash values
- Group object reference handling

**SHOULD Support:**
- JWS signature verification
- JWE decryption (with appropriate keys)
- Additional hash algorithms (SHA-256)
- Bundle validation and integrity checking
- Extension directory support
- Efficient large file handling (streaming)

**MAY Support:**
- Compression optimization
- Incremental bundle updates
- Bundle format migration tools
- Custom extension handling
- ZIP-level encryption
- Bundle analysis tools

### Error Handling

**Bundle Creation Errors:**
- Network failures: Retry with backoff, fail after max attempts
- Hash mismatches: MUST fail with expected vs actual
- Missing files: MUST fail unless configured to skip
- Access denied: MUST fail, do not retry
- Invalid JWS: SHOULD warn, MAY continue
- JWE decryption failure: MUST fail
- Missing keys: MUST fail with clear error

**Bundle Extraction Errors:**
- Corrupted ZIP: MUST fail
- Missing manifest.json: MUST fail
- Missing vcons/ directory: MUST fail
- Hash verification failure: MUST fail unless configured for warnings
- JWS signature failure: SHOULD warn, MAY continue
- Missing files: MUST fail if referenced in vCon
- Orphaned files: MAY warn if not referenced

### Best Practices

**Bundle Creation:**
1. Always validate content hashes before including files
2. Use HTTPS exclusively for external URLs
3. Preserve original vCon security forms
4. Include related vCons from Group references
5. Document bundle purpose in accompanying metadata

**Bundle Distribution:**
1. Consider ZIP-level encryption for sensitive bundles
2. Verify bundle integrity before distribution
3. Provide bundle validation tools to recipients
4. Document required decryption keys separately
5. Use secure channels for bundle transmission

**Bundle Storage:**
1. Store bundles with descriptive names (e.g., `case-12345-2025-01-15.vconz`)
2. Index bundles by vCon UUIDs for fast lookup
3. Maintain bundle metadata (creation date, source, purpose)
4. Implement retention policies
5. Regular integrity verification

## Multi-Language Code Generation

This skill generates production-ready code in three languages:

### Language Selection Guidance

**Go** - Best for:
- High-performance vCon processing
- Microservices and cloud-native applications
- System integrations with strong typing
- Validation and compliance tools

**JavaScript/TypeScript** - Best for:
- Web applications and APIs
- Real-time conversation capture
- Browser-based vCon tools
- Node.js backend services

**Python** - Best for:
- Data analysis and ML pipelines
- Rapid prototyping
- Scientific computing on conversation data
- Integration with AI/ML frameworks

### Code Generation Standards

All generated code MUST:
1. Include comprehensive type definitions/interfaces
2. Provide validation functions
3. Handle all three vCon forms (unsigned, signed, encrypted)
4. Include error handling and edge cases
5. Add inline documentation
6. Use language-specific best practices
7. Be production-ready without modifications

## vCon Extensions

### Contact Center (CC) Extension

Adds contact center-specific fields to Party and Dialog objects:

**Party Object Extensions:**
```json
{
  "contact_list": "premium_customers",
  "skill": "technical_support",
  "queue_time": 45,
  "ring_time": 8,
  "disposition": "resolved",
  "dnis": "+1-800-555-0100",
  "ani": "+1-555-0123",
  "customer_id": "CUST-98765"
}
```

### MIMI (More Instant Messaging Interoperability) Extension

Supports modern messaging platforms:

**Dialog Object Extensions:**
- Group conversation support
- Message threading
- Reactions and read receipts
- Rich media attachments
- Platform-specific metadata

### WTF (World Transcription Format) Extension

Standardized transcription analysis framework (draft-howe-vcon-wtf-extension-01):

**Extension Classification**: Compatible Extension - can be safely ignored by implementations that don't support transcription analysis

**Extension Token**: `wtf_transcription`

**Purpose**: Provides a unified analysis framework for speech-to-text transcription data from multiple providers with consistent structure, quality metrics, and confidence scoring.

**Supported Providers**:
- Whisper™ (OpenAI)
- Deepgram™
- AssemblyAI™
- Google Cloud Speech-to-Text™
- Amazon Transcribe™
- Azure Speech Services™
- Rev.ai™
- Speechmatics™
- Wav2Vec2™
- Parakeet™ (NVIDIA)

**Analysis Object Structure:**
```json
{
  "type": "wtf_transcription",
  "start": "2025-01-02T12:16:35Z",
  "dialog": 0,
  "encoding": "json",
  "body": {
    "transcript": {
      "text": "Complete transcription text",
      "language": "en-US",
      "duration": 65.2,
      "confidence": 0.92
    },
    "segments": [
      {
        "id": 0,
        "start": 0.5,
        "end": 4.8,
        "text": "Hello, this is Alice from customer service.",
        "confidence": 0.95,
        "speaker": 0,
        "words": [0, 1, 2, 3, 4, 5, 6]
      }
    ],
    "metadata": {
      "created_at": "2025-01-02T12:15:30Z",
      "processed_at": "2025-01-02T12:16:35Z",
      "provider": "deepgram",
      "model": "nova-2",
      "processing_time": 12.5,
      "audio": {
        "duration": 65.2,
        "sample_rate": 8000,
        "channels": 1,
        "format": "wav",
        "bitrate": 128
      },
      "options": {
        "punctuate": true,
        "diarize": true,
        "language": "en"
      }
    },
    "words": [
      {
        "id": 0,
        "start": 0.5,
        "end": 0.8,
        "text": "Hello",
        "confidence": 0.98,
        "speaker": 0,
        "is_punctuation": false
      }
    ],
    "speakers": {
      "0": {
        "id": 0,
        "label": "Alice (Customer Service)",
        "segments": [0],
        "total_time": 4.3,
        "confidence": 0.95
      }
    },
    "quality": {
      "audio_quality": "high",
      "background_noise": 0.1,
      "multiple_speakers": true,
      "overlapping_speech": false,
      "silence_ratio": 0.15,
      "average_confidence": 0.92,
      "low_confidence_words": 0,
      "processing_warnings": []
    },
    "extensions": {
      "provider_name": {
        // Provider-specific fields
      }
    }
  }
}
```

**WTF Schema Sections**:

*Required Fields*:
- `transcript`: Complete transcript with text, language (BCP-47), duration, and overall confidence
- `segments`: Time-aligned text chunks with start/end times, text, confidence, and optional speaker ID
- `metadata`: Processing information including timestamps, provider, model, audio details, and options

*Optional Fields*:
- `words`: Word-level details with timing and confidence
- `speakers`: Speaker diarization with labels, segments, and speaking time
- `quality`: Audio quality assessment and processing metrics
- `alternatives`: Alternative transcription hypotheses
- `enrichments`: Additional analysis features
- `extensions`: Provider-specific data preservation
- `streaming`: Real-time streaming information

**Key Features**:
- **Hierarchical Structure**: Words → Segments → Complete Transcript
- **Confidence Normalization**: All scores normalized to [0.0-1.0] range
- **Multi-Provider Support**: Consistent format across different transcription services
- **Quality Metrics**: Built-in audio quality and confidence assessments
- **Speaker Diarization**: "Who spoke when" analysis support
- **Extensibility**: Provider-specific features preserved in extensions field

## Changes in draft-ietf-vcon-vcon-core-02

### Key Updates from -01 to -02

**Field Renames:**
- `must_support` → `critical` (incompatible extension declaration)
- Attachment Object: `type` → `purpose` (semantic clarification)
- Party history events: `dtmfdown`/`dtmfup` → `keydown`/`keyup` (broader applicability)
- Party history parameter: `dtmf` → `button` (supports DTMF and application keys/buttons)

**Removed Fields:**
- `jCard` removed from Party Object

**New Fields and Types:**
- `report` added as a new Analysis type
- Group Object expanded with `body` and `encoding` parameters

**Semantic Changes:**
- **Session ID**: Null/unknown session IDs now use empty object `{}` instead of `null`
- **Anonymous Parties**: Party `name` may be "anonymous" for privacy; each anonymous participant requires a distinct Party Object
- **Dialog Transfer**: Missing dialog information uses empty Dialog Objects at corresponding indices instead of index `-1`

**New Sections:**
- **Long-Term Archiving (Section 5.2.3)**: Nested JWS signing approach for maintaining integrity over extended archival periods (JWS3→JWS2→JWS1→vCon nesting)

## Q&A Expertise

This skill can answer questions about:

### Technical Questions
- vCon structure and schema details
- Validation requirements and compliance
- Extension mechanisms and compatibility
- Security considerations (signing, encryption)
- Media type handling
- UUID generation strategies
- Redaction and appending workflows

### Use Case Questions
- Contact center integration
- Messaging platform data exchange
- Emergency services (ECRIT) applications
- Healthcare conversation management
- Legal and compliance requirements
- Multi-channel conversation aggregation

### Implementation Questions
- Best practices for vCon creation
- Performance optimization strategies
- Storage and retrieval patterns
- Real-time vs. batch processing
- API design considerations
- Testing and validation strategies

## Validation Capabilities

### Validation Process

1. **Structure Validation**
   - Valid JSON syntax
   - Required fields present
   - Correct vCon version

2. **Schema Validation**
   - Field types correct
   - Value constraints met
   - Array indices valid

3. **Content Validation**
   - UUID format (v8 or v4)
   - RFC 3339 timestamps
   - Tel/SIP/mailto URL formats
   - Content hash integrity

4. **Extension Validation**
   - Declared extensions used
   - `critical` extensions recognized
   - Extension-specific fields valid

5. **Security Validation**
   - HTTPS URLs only
   - SHA-512 content hashes present
   - Signature validation (if signed)
   - Encryption validation (if encrypted)

### Validation Report Format

```markdown
# vCon Validation Report

**File**: example-vcon.json
**Validation Date**: 2025-10-20T16:00:00Z
**vCon Version**: 0.4.0
**vCon Form**: unsigned

## Compliance Status

✅ **COMPLIANT**

## Summary

- **Total Issues**: 0
- **Critical Errors**: 0
- **Warnings**: 0
- **Suggestions**: 2

## Validation Results

### ✅ Structural Validity
- [x] Valid JSON structure
- [x] Required top-level fields present
- [x] Correct vCon version (0.4.0)
- [x] UUID format valid (UUID v8)

### ✅ Schema Compliance
- [x] All timestamps RFC 3339 compliant
- [x] Party indices within bounds
- [x] Dialog types valid
- [x] Media types properly formatted

### ✅ Extension Compliance
- [x] CC Extension properly declared
- [x] All CC-specific fields valid

### 💡 Suggestions

1. **Add updated_at timestamp**
   - Consider adding `updated_at` for audit trail

2. **Include content hashes for external URLs**
   - External dialog references should include SHA-512 hash
```

## Code Generation Examples

### Example 1: Go vCon Parser

**User Request**: "Generate Go code to parse and validate vCons"

**Response Structure:**
1. Type definitions for all vCon objects
2. Validation functions with detailed error handling
3. Parser with support for all three forms
4. Utility functions (UUID validation, date parsing, content hash verification)
5. Complete example usage

```go
package vcon

import (
    "crypto/sha512"
    "encoding/base64"
    "encoding/json"
    "fmt"
    "time"
)

// VCon represents the top-level vCon object
type VCon struct {
    VCon        string      `json:"vcon"`
    UUID        string      `json:"uuid"`
    Extensions  []string    `json:"extensions,omitempty"`
    Critical    []string    `json:"critical,omitempty"`
    CreatedAt   time.Time   `json:"created_at"`
    UpdatedAt   *time.Time  `json:"updated_at,omitempty"`
    Subject     string      `json:"subject,omitempty"`
    Parties     []Party     `json:"parties"`
    Dialog      []Dialog    `json:"dialog,omitempty"`
    Analysis    []Analysis  `json:"analysis,omitempty"`
    Attachments []Attachment `json:"attachments,omitempty"`
    Redacted    *Redacted   `json:"redacted,omitempty"`
    Amended     *Amended    `json:"amended,omitempty"`
    Group       []Group     `json:"group,omitempty"`
}

// Party represents a participant in the conversation
// Note: jCard has been removed in draft-ietf-vcon-vcon-core-02
// Names may be "anonymous" for privacy; distinct Party Objects required per anonymous participant
type Party struct {
    Tel          string       `json:"tel,omitempty"`
    SIP          string       `json:"sip,omitempty"`
    Mailto       string       `json:"mailto,omitempty"`
    Name         string       `json:"name,omitempty"`
    DID          string       `json:"did,omitempty"`
    UUID         string       `json:"uuid,omitempty"`
    Validation   string       `json:"validation,omitempty"`
    GMLPos       string       `json:"gmlpos,omitempty"`
    CivicAddress *CivicAddress `json:"civicaddress,omitempty"`
    Timezone     string       `json:"timezone,omitempty"`
}

// Validate checks if the vCon is compliant with the specification
func (v *VCon) Validate() error {
    if v.VCon != "0.4.0" {
        return fmt.Errorf("invalid vcon version: %s", v.VCon)
    }
    
    if err := validateUUID(v.UUID); err != nil {
        return fmt.Errorf("invalid uuid: %w", err)
    }
    
    if len(v.Parties) == 0 {
        return fmt.Errorf("at least one party is required")
    }
    
    // Validate all parties
    for i, party := range v.Parties {
        if err := party.Validate(); err != nil {
            return fmt.Errorf("invalid party at index %d: %w", i, err)
        }
    }
    
    // Validate dialog references
    for i, dialog := range v.Dialog {
        if err := dialog.ValidatePartyRefs(len(v.Parties)); err != nil {
            return fmt.Errorf("invalid dialog at index %d: %w", i, err)
        }
    }
    
    return nil
}

func validateUUID(uuid string) error {
    // UUID validation logic
    if len(uuid) != 36 {
        return fmt.Errorf("invalid uuid length")
    }
    return nil
}
```

### Example 2: JavaScript vCon Builder

**User Request**: "Create JavaScript code to build vCons programmatically"

**Response Structure:**
1. TypeScript interfaces for type safety
2. Builder class with fluent API
3. Validation methods
4. Serialization/deserialization
5. Example usage with real-world scenario

```javascript
/**
 * vCon Builder - TypeScript/JavaScript
 * Provides a fluent API for constructing vCon objects
 */

interface VCon {
  vcon: string;
  uuid: string;
  created_at: string;
  updated_at?: string;
  parties: Party[];
  dialog?: Dialog[];
  analysis?: Analysis[];
  extensions?: string[];
  critical?: string[];
}

interface Party {
  tel?: string;
  name?: string;
  mailto?: string;
  uuid?: string;
}

interface Dialog {
  type: 'recording' | 'text' | 'transfer' | 'incomplete';
  start: string;
  duration?: number;
  parties: number | number[];
  mediatype?: string;
  body?: string;
  encoding?: string;
  url?: string;
  content_hash?: string | string[];
}

class VConBuilder {
  private vcon: Partial<VCon>;
  
  constructor() {
    this.vcon = {
      vcon: '0.4.0',
      uuid: this.generateUUID(),
      created_at: new Date().toISOString(),
      parties: []
    };
  }
  
  addParty(party: Party): this {
    this.vcon.parties!.push(party);
    return this;
  }
  
  addDialog(dialog: Dialog): this {
    if (!this.vcon.dialog) {
      this.vcon.dialog = [];
    }
    this.vcon.dialog.push(dialog);
    return this;
  }
  
  setSubject(subject: string): this {
    this.vcon.subject = subject;
    return this;
  }
  
  addExtension(extension: string): this {
    if (!this.vcon.extensions) {
      this.vcon.extensions = [];
    }
    this.vcon.extensions.push(extension);
    return this;
  }
  
  build(): VCon {
    this.validate();
    return this.vcon as VCon;
  }
  
  private validate(): void {
    if (!this.vcon.parties || this.vcon.parties.length === 0) {
      throw new Error('At least one party is required');
    }
    
    // Validate party indices in dialogs
    if (this.vcon.dialog) {
      const maxPartyIndex = this.vcon.parties!.length - 1;
      for (const dialog of this.vcon.dialog) {
        const parties = Array.isArray(dialog.parties) 
          ? dialog.parties 
          : [dialog.parties];
        
        for (const partyIdx of parties) {
          if (partyIdx > maxPartyIndex) {
            throw new Error(
              `Dialog references invalid party index: ${partyIdx}`
            );
          }
        }
      }
    }
  }
  
  private generateUUID(): string {
    // UUID v8 generation (simplified)
    return 'xxxxxxxx-xxxx-8xxx-yxxx-xxxxxxxxxxxx'.replace(
      /[xy]/g,
      (c) => {
        const r = (Math.random() * 16) | 0;
        const v = c === 'x' ? r : (r & 0x3) | 0x8;
        return v.toString(16);
      }
    );
  }
  
  toJSON(): string {
    return JSON.stringify(this.build(), null, 2);
  }
}

// Example usage
const vcon = new VConBuilder()
  .setSubject('Customer support call')
  .addParty({
    tel: '+1-555-0100',
    name: 'Alice Smith'
  })
  .addParty({
    tel: '+1-555-0200',
    name: 'Support Agent'
  })
  .addDialog({
    type: 'recording',
    start: new Date().toISOString(),
    duration: 180.5,
    parties: [0, 1],
    mediatype: 'audio/x-wav',
    url: 'https://example.com/recordings/call123.wav',
    content_hash: 'SHA-512:abc123...'
  })
  .build();

console.log(JSON.stringify(vcon, null, 2));
```

### Example 3: Python vCon Analyzer

**User Request**: "Generate Python code for vCon analysis and data extraction"

**Response Structure:**
1. Pydantic models for validation
2. Parser and loader functions
3. Analysis extractors
4. Statistical aggregation
5. Export utilities

```python
"""
vCon Analyzer - Python
Provides tools for parsing, analyzing, and extracting data from vCons
"""

from datetime import datetime
from typing import List, Optional, Dict, Any, Union
from pydantic import BaseModel, Field, validator
import json
import hashlib
import base64

class Party(BaseModel):
    tel: Optional[str] = None
    sip: Optional[str] = None
    mailto: Optional[str] = None
    name: Optional[str] = None
    did: Optional[str] = None
    uuid: Optional[str] = None
    validation: Optional[str] = None
    
class Dialog(BaseModel):
    type: str
    start: datetime
    duration: Optional[float] = None
    parties: Union[int, List[int]]
    originator: Optional[int] = None
    mediatype: Optional[str] = None
    filename: Optional[str] = None
    body: Optional[str] = None
    encoding: Optional[str] = None
    url: Optional[str] = None
    content_hash: Optional[Union[str, List[str]]] = None
    
    @validator('type')
    def validate_type(cls, v):
        valid_types = ['recording', 'text', 'transfer', 'incomplete']
        if v not in valid_types:
            raise ValueError(f'Invalid dialog type: {v}')
        return v

class Analysis(BaseModel):
    type: str
    dialog: Optional[Union[int, List[int]]] = None
    mediatype: Optional[str] = None
    vendor: Optional[str] = None
    product: Optional[str] = None
    schema: Optional[str] = None
    body: Optional[str] = None
    encoding: Optional[str] = None
    url: Optional[str] = None
    
class VCon(BaseModel):
    vcon: str
    uuid: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    subject: Optional[str] = None
    parties: List[Party]
    dialog: Optional[List[Dialog]] = None
    analysis: Optional[List[Analysis]] = None
    extensions: Optional[List[str]] = None
    critical: Optional[List[str]] = None
    
    @validator('vcon')
    def validate_version(cls, v):
        if v != '0.4.0':
            raise ValueError(f'Unsupported vCon version: {v}')
        return v
    
    @validator('parties')
    def validate_parties(cls, v):
        if len(v) == 0:
            raise ValueError('At least one party is required')
        return v

class VConAnalyzer:
    """Analyzer for extracting insights from vCons"""
    
    def __init__(self, vcon: VCon):
        self.vcon = vcon
        
    def get_conversation_duration(self) -> float:
        """Calculate total conversation duration in seconds"""
        if not self.vcon.dialog:
            return 0.0
        
        total = sum(
            d.duration for d in self.vcon.dialog 
            if d.duration is not None and d.type == 'recording'
        )
        return total
    
    def get_participants(self) -> List[Dict[str, str]]:
        """Extract participant information"""
        participants = []
        for i, party in enumerate(self.vcon.parties):
            info = {
                'index': i,
                'name': party.name or 'Unknown',
                'tel': party.tel,
                'email': party.mailto
            }
            participants.append(info)
        return participants
    
    def get_transcripts(self) -> List[str]:
        """Extract all transcript analysis"""
        if not self.vcon.analysis:
            return []
        
        transcripts = []
        for analysis in self.vcon.analysis:
            if analysis.type == 'transcript' and analysis.body:
                # Decode if needed
                if analysis.encoding == 'base64url':
                    decoded = base64.urlsafe_b64decode(analysis.body)
                    transcripts.append(decoded.decode('utf-8'))
                elif analysis.encoding in ['json', 'none', None]:
                    transcripts.append(analysis.body)
        
        return transcripts
    
    def get_summary_stats(self) -> Dict[str, Any]:
        """Generate summary statistics"""
        return {
            'uuid': self.vcon.uuid,
            'created_at': self.vcon.created_at.isoformat(),
            'subject': self.vcon.subject,
            'num_parties': len(self.vcon.parties),
            'num_dialogs': len(self.vcon.dialog) if self.vcon.dialog else 0,
            'num_analysis': len(self.vcon.analysis) if self.vcon.analysis else 0,
            'total_duration': self.get_conversation_duration(),
            'extensions_used': self.vcon.extensions or [],
            'critical_extensions': self.vcon.critical or [],
            'has_recordings': any(
                d.type == 'recording' 
                for d in (self.vcon.dialog or [])
            ),
            'has_transcripts': any(
                a.type == 'transcript' 
                for a in (self.vcon.analysis or [])
            )
        }
    
    def export_to_dict(self) -> dict:
        """Export vCon to dictionary"""
        return self.vcon.dict(exclude_none=True)
    
    def export_to_json(self, indent: int = 2) -> str:
        """Export vCon to JSON string"""
        return json.dumps(self.export_to_dict(), indent=indent, default=str)

# Example usage
def load_vcon(filepath: str) -> VCon:
    """Load vCon from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    return VCon(**data)

def analyze_vcon(filepath: str):
    """Analyze a vCon file and print statistics"""
    vcon = load_vcon(filepath)
    analyzer = VConAnalyzer(vcon)
    
    stats = analyzer.get_summary_stats()
    print("vCon Analysis Report")
    print("=" * 50)
    print(f"UUID: {stats['uuid']}")
    print(f"Subject: {stats['subject']}")
    print(f"Participants: {stats['num_parties']}")
    print(f"Dialog segments: {stats['num_dialogs']}")
    print(f"Analysis objects: {stats['num_analysis']}")
    print(f"Total duration: {stats['total_duration']:.1f}s")
    print(f"Extensions: {', '.join(stats['extensions_used']) or 'None'}")
    print()
    
    participants = analyzer.get_participants()
    print("Participants:")
    for p in participants:
        print(f"  [{p['index']}] {p['name']}")
        if p['tel']:
            print(f"      Tel: {p['tel']}")
        if p['email']:
            print(f"      Email: {p['email']}")

# Run analysis
if __name__ == '__main__':
    analyze_vcon('example-vcon.json')
```

## Best Practices

### vCon Creation
1. **Always use version 0.4.0** in the `vcon` field
2. **Generate UUID v8** for global uniqueness
3. **Use RFC 3339 timestamps** with timezone information
4. **Declare extensions** before using extension-specific fields
5. **Index parties correctly** (0-based array indices)

### Security
1. **Sign vCons before encryption** (JWS → JWE)
2. **Use HTTPS for external URLs** (never HTTP)
3. **Generate SHA-512 hashes** for external files
4. **Include x5c certificate chain** in signed vCons
5. **Redact PII** before sharing across domains

### Performance
1. **Use external references** for large media files
2. **Compress with gzip** for transmission
3. **Batch process** analysis operations
4. **Cache parsed vCons** in memory
5. **Index by UUID** for fast lookups

### Privacy
1. **Create redacted versions** for limited access
2. **Reference encrypted originals** from redacted vCons
3. **Minimize data collection** from start
4. **Track consent** in attachments
5. **Use validated field** for identity verification

## Use Case Scenarios

### Contact Center Integration

**Scenario**: Integrate call recordings with customer support system

**Solution**:
1. Capture call metadata in vCon during conversation
2. Add recording as Dialog Object with external URL
3. Generate transcript using Analysis Object
4. Add customer details in CC extension fields
5. Sign vCon before exporting to CRM
6. Create redacted version for analytics team

### Multi-Channel Conversation

**Scenario**: Track customer journey across chat, email, and phone

**Solution**:
1. Create separate vCon for each channel/interaction
2. Use Group Object to link related vCons
3. Maintain consistent party UUIDs across vCons
4. Add application field to identify each platform
5. Aggregate analysis across all channels

### Emergency Services (ECRIT)

**Scenario**: Document 911 emergency call with location

**Solution**:
1. Capture caller location in gmlpos/civicaddress
2. Record audio with timestamp synchronization
3. Include dispatcher notes as analysis
4. Attach incident reports
5. Sign for legal admissibility
6. Encrypt for privacy protection

### Compliance and Audit

**Scenario**: Financial services call recording for compliance

**Solution**:
1. Create original vCon with full conversation
2. Add compliance tags in subject/analysis
3. Sign vCon with company certificate
4. Create redacted version (remove PII)
5. Store encrypted original for 7 years
6. Provide signed redacted version for audits

## Troubleshooting Guide

### Common Validation Errors

**"Invalid vCon version"**
- Fix: Ensure `"vcon": "0.4.0"`
- Check for typos or wrong version number

**"Party index out of bounds"**
- Fix: Count parties array (0-indexed)
- Verify dialog/attachment/analysis party references
- Add missing parties to parties array

**"Invalid RFC 3339 timestamp"**
- Fix: Use format `YYYY-MM-DDTHH:MM:SS.sssZ`
- Include timezone (Z or ±HH:MM)
- Ensure milliseconds have 3 digits

**"Unknown vCon form"**
- Issue: Missing identifying fields
- Unsigned: needs parties/dialog/analysis/attachments
- Signed: needs payload AND signatures
- Encrypted: needs ciphertext AND recipients

**"Extension not declared"**
- Fix: Add extension name to extensions array
- Check `critical` for incompatible extensions
- Verify extension-specific fields are valid

### Performance Issues

**"Slow parsing of large vCons"**
- Use streaming JSON parser
- Parse only needed sections
- Consider external references for media
- Cache parsed vCons in memory

**"High memory usage"**
- Don't load all dialog bodies in memory
- Use external references for recordings
- Process analysis in batches
- Implement pagination for large vCon collections

## Advanced Topics

### Custom Extension Development

**Steps to create a vCon extension:**

1. **Define the Use Case**
   - Identify what additional data is needed
   - Determine which objects need new parameters
   - Classify as Compatible or Incompatible

2. **Design the Schema**
   - Use snake_case naming
   - Define parameter types clearly
   - Document semantics thoroughly

3. **Register with IANA**
   - Choose unique extension name token
   - Submit registration template
   - Register new parameters

4. **Implement and Test**
   - Create reference implementation
   - Validate against core spec
   - Test interoperability

5. **Document**
   - Write extension specification
   - Provide code examples
   - Create migration guide if deprecating fields

### vCon Signing and Verification

**JWS Signing Process:**

```go
// Example: Sign a vCon in Go
func SignVCon(vcon *VCon, privateKey *rsa.PrivateKey, certChain []string) (string, error) {
    // 1. Serialize unsigned vCon to JSON
    payload, err := json.Marshal(vcon)
    if err != nil {
        return "", err
    }
    
    // 2. Optionally compress with gzip
    var compressedPayload bytes.Buffer
    gzipWriter := gzip.NewWriter(&compressedPayload)
    gzipWriter.Write(payload)
    gzipWriter.Close()
    
    // 3. Base64url encode
    encodedPayload := base64.RawURLEncoding.EncodeToString(compressedPayload.Bytes())
    
    // 4. Create JWS protected header
    header := map[string]interface{}{
        "alg": "RS256",
        "typ": "JWT",
        "x5c": certChain,  // Certificate chain
    }
    
    headerJSON, _ := json.Marshal(header)
    encodedHeader := base64.RawURLEncoding.EncodeToString(headerJSON)
    
    // 5. Create signing input
    signingInput := encodedHeader + "." + encodedPayload
    
    // 6. Sign with private key
    hash := sha256.Sum256([]byte(signingInput))
    signature, err := rsa.SignPKCS1v15(rand.Reader, privateKey, crypto.SHA256, hash[:])
    if err != nil {
        return "", err
    }
    
    // 7. Base64url encode signature
    encodedSignature := base64.RawURLEncoding.EncodeToString(signature)
    
    // 8. Create JWS compact serialization
    jws := encodedHeader + "." + encodedPayload + "." + encodedSignature
    
    // 9. Wrap in signed vCon JSON structure
    signedVCon := map[string]interface{}{
        "vcon": vcon.VCon,
        "uuid": vcon.UUID,
        "signatures": []map[string]string{{
            "protected": encodedHeader,
            "signature": encodedSignature,
        }},
        "payload": encodedPayload,
    }
    
    result, _ := json.Marshal(signedVCon)
    return string(result), nil
}
```

### vCon Encryption

**JWE Encryption Process:**

```javascript
// Example: Encrypt a signed vCon in JavaScript
async function encryptVCon(signedVCon, publicKey) {
  // 1. Serialize signed vCon to JSON
  const payload = JSON.stringify(signedVCon);
  
  // 2. Generate content encryption key (CEK)
  const cek = crypto.getRandomValues(new Uint8Array(32));
  
  // 3. Encrypt CEK with recipient's public key
  const encryptedKey = await crypto.subtle.encrypt(
    {
      name: 'RSA-OAEP',
      hash: 'SHA-256'
    },
    publicKey,
    cek
  );
  
  // 4. Generate IV
  const iv = crypto.getRandomValues(new Uint8Array(16));
  
  // 5. Encrypt payload with CEK
  const encodedPayload = new TextEncoder().encode(payload);
  const ciphertext = await crypto.subtle.encrypt(
    {
      name: 'AES-GCM',
      iv: iv,
      tagLength: 128
    },
    await crypto.subtle.importKey(
      'raw',
      cek,
      'AES-GCM',
      false,
      ['encrypt']
    ),
    encodedPayload
  );
  
  // 6. Base64url encode components
  const encodedEncryptedKey = base64urlEncode(encryptedKey);
  const encodedIV = base64urlEncode(iv);
  const encodedCiphertext = base64urlEncode(ciphertext);
  
  // 7. Create JWE structure
  const jwe = {
    vcon: signedVCon.vcon,
    uuid: signedVCon.uuid,
    recipients: [{
      encrypted_key: encodedEncryptedKey
    }],
    unprotected: {
      alg: 'RSA-OAEP',
      enc: 'A256GCM'
    },
    iv: encodedIV,
    ciphertext: encodedCiphertext
  };
  
  return jwe;
}
```

## Reference Documentation

### IETF Specifications

- **draft-ietf-vcon-vcon-core-02** (January 2026)
  - Core vCon specification
  - JSON schema definition
  - Security considerations
  - Long-term archiving with nested JWS signing

- **draft-ietf-vcon-cc-extension-01**
  - Contact Center extension
  - Call disposition fields
  - Queue metrics

- **draft-ietf-vcon-privacy-primer-00**
  - Privacy considerations
  - Redaction strategies
  - Consent management

- **draft-ietf-vcon-vcon-overview-00**
  - Use cases and scenarios
  - Architecture patterns
  - Integration guidance

- **draft-miller-vcon-zip-bundle-00** (November 2025)
  - vCon ZIP Bundle (.vconz) packaging format
  - Self-contained archives with media files
  - Multi-vCon support with automatic deduplication
  - Hash-based file naming and integrity verification
  - Supports all vCon security forms (unsigned, signed, encrypted)
  - Offline processing and simplified distribution
  - Media type: application/vcon+zip

- **draft-howe-vcon-wtf-extension-01**
  - World Transcription Format extension
  - Standardized analysis framework for speech-to-text transcription
  - Multi-provider support (Whisper™, Deepgram™, AssemblyAI™, Google, Amazon, Azure, etc.)
  - Compatible Extension - introduces new analysis type "wtf_transcription"
  - Hierarchical structure: words → segments → complete transcripts
  - Quality metrics and confidence scoring normalization [0.0-1.0]
  - Provider-specific features preserved through extensions field
  - Supports speaker diarization and audio quality assessment

### Related Standards

- **RFC 3339** - Date and Time on the Internet
- **RFC 4122** - UUID Standard
- **RFC 7515** - JSON Web Signature (JWS)
- **RFC 7516** - JSON Web Encryption (JWE)
- **RFC 8259** - JSON Specification
- **RFC 3986** - URI Syntax

### Online Resources

- IETF vCon Working Group: https://datatracker.ietf.org/wg/vcon/
- GitHub Repository: https://github.com/ietf-wg-vcon/
- Mailing List: vcon@ietf.org

---

## Skill Usage Patterns

### Pattern 1: Quick Validation

**User**: "Can you validate this vCon?"

**Process**:
1. Read the IETF core spec if needed
2. Parse the uploaded vCon JSON
3. Run comprehensive validation
4. Generate detailed report with fixes
5. Provide corrected example if non-compliant

### Pattern 2: Code Generation

**User**: "Generate Python code to parse vCons with validation"

**Process**:
1. Review language-specific requirements
2. Generate complete type definitions
3. Create parsing and validation functions
4. Add error handling
5. Include usage examples
6. Provide test cases

### Pattern 3: Q&A with Deep Dive

**User**: "How do vCon redactions work and when should I use them?"

**Process**:
1. Read redaction documentation from spec
2. Explain redaction concept clearly
3. Show object tree diagram
4. Provide use case examples
5. Generate code example in preferred language
6. Discuss privacy considerations

### Pattern 4: Extension Guidance

**User**: "I need to add custom fields for my healthcare application. How do I create a vCon extension?"

**Process**:
1. Review extension framework documentation
2. Discuss Compatible vs. Incompatible classification
3. Design the extension schema with user
4. Provide IANA registration template
5. Generate reference implementation in 3 languages
6. Create validation code for the extension

### Pattern 5: Architecture Consultation

**User**: "How should I design my system to handle vCons at scale?"

**Process**:
1. Understand user's specific requirements
2. Discuss vCon lifecycle (creation → signing → storage)
3. Recommend external references for large media
4. Suggest indexing strategies
5. Provide performance optimization tips
6. Show example architecture diagram
7. Generate starter code for their stack

---

**This comprehensive skill makes Claude the foremost expert on vCons, capable of answering any question, validating any vCon, and generating production-ready code in multiple languages. Always read the bundled IETF specifications when needed to provide accurate, up-to-date information.**