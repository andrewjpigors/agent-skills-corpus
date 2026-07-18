---
name: diagnostics-rust
description: >
  Language-specific logging, error handling, and diagnostics patterns for Rust.
  Extends diagnostics-base with concrete Rust crate choices (tracing,
  tracing-subscriber, thiserror, anyhow, miette) and idiomatic code patterns
  for both libraries and applications (CLIs, HTTP services, async workers).
  Triggers whenever writing or reviewing error enums, `Result` returns, `?`
  propagation, `panic!`/`unwrap`/`expect`, or any `tracing!`/`log!` call in
  Rust. REQUIRES diagnostics-base to be installed — this skill does not repeat
  base rules, it extends them.
---

# Rust Diagnostics Skill

> **REQUIRED: Read `diagnostics-base` fully before applying any pattern here.**
> This skill extends diagnostics-base — it does not repeat base rules.
> All rules in diagnostics-base apply unchanged. This skill adds Rust-specific
> crate choices, syntax, and idiomatic patterns on top of them.

---

## Library Stack

The canonical modern Rust diagnostics stack. Every pattern below assumes these
crates — if the project uses different ones, update this table and regenerate.

| Role | Crate | Version | Notes |
|---|---|---|---|
| Logging / instrumentation | `tracing` | `0.1` | Async-first; spans + structured fields; de facto standard |
| Log subscriber / output | `tracing-subscriber` | `0.3` | JSON layer for prod, `fmt` layer for dev, `EnvFilter` for `RUST_LOG` |
| `log` ↔ `tracing` bridge | `tracing-log` | `0.2` | Re-emit `log::*` records as tracing events (for deps that use `log`) |
| Library error types | `thiserror` | `2.x` | Derive macro for `std::error::Error` on enums; zero runtime cost |
| Application errors | `anyhow` | `1.x` | Opaque `anyhow::Error` + `.context(...)` chains for app boundaries |
| Rich diagnostic display | `miette` | `7.x` | rustc-style spans/help/notes; integrates with thiserror via `#[derive(Diagnostic)]` |
| Decoding errors | `serde` | `1.x` | The error source for any deserialized input |
| Tracing/OTel export | `tracing-opentelemetry` + `opentelemetry-otlp` | latest | When OTel export is required |

**Crates intentionally NOT in this stack:**
- `eyre` / `color-eyre` — equivalent to `anyhow`+`miette`. Pick one stack; don't mix.
- `snafu` — more ceremony than `thiserror`; reach for it only if you need `snafu`'s context selectors.
- `failure` — deprecated; do not use.
- `log` + `env_logger` — fine for tiny libs; for anything else `tracing` is strictly superior. Use `tracing-log` to absorb deps that still emit `log` records.
- `slog` — legacy; do not start new projects with it.

---

## Decision Tree: thiserror vs anyhow vs miette

The single most common question in Rust diagnostics. Resolve it with these
three trees before writing any error type.

```
Are you writing a PUBLIC library / crate that others depend on?
  YES → thiserror enum + #[derive(Error)]
        reason: callers must match on specific variants; opaque types prevent
                exhaustive handling. NEVER return `anyhow::Error` from a lib.
  NO (you own the error boundary — binary, top-level service)
       → anyhow::Result<T> + .context("...") at meaningful layers
         reason: opaque is fine; cause chains + context are the priority
```

```
Are you rendering errors to END USERS (CLI / TUI / compiler-like tool)?
  YES → also derive miette::Diagnostic on your thiserror enum, or return
        miette::Result<()> from main(). Use #[diagnostic(code, help)] and
        #[source_code] / #[label] for source-span rendering.
  NO  → tracing structured fields are enough; the boundary logs them
```

```
Do you need to point at a SPECIFIC SPAN in user-supplied text (config,
query, source file)?
  YES → miette is the only sensible choice. Use NamedSource + #[label].
  NO  → plain thiserror Display is enough.
```

```
At the application boundary (HTTP handler, main(), worker loop):
  - Return anyhow::Result<T> internally,
  - then translate ONCE: tracing::error!/warn!/info!() based on taxonomy,
  - and convert to the boundary's user-facing form
    (axum IntoResponse / miette Report / process::exit).
```

`#[error(transparent)]` is the escape hatch when a thiserror variant only
wraps another error and adds nothing — use it instead of inventing a redundant
display.

---

## Log Setup

Canonical `tracing-subscriber` bootstrap. JSON in production, pretty in
development, level from `RUST_LOG`, and a global subscriber installed once at
process start.

```rust
// File: src/telemetry.rs
// Base rule: diagnostics-base §Log Setup, §Structured logging

use tracing_subscriber::{fmt, layer::SubscriberExt, util::SubscriberInitExt, EnvFilter};

pub fn init() {
    // RUST_LOG controls level per module/crate. Default to INFO; libraries
    // commonly set themselves to WARN below that. Example:
    //   RUST_LOG=info,sqlx=warn,hyper=warn,my_app=debug
    let filter = EnvFilter::try_from_default_env()
        .unwrap_or_else(|_| EnvFilter::new("info"));

    // tracing-log bridges any std `log::*` records from dependencies into
    // the tracing pipeline so they go through the same filter and subscriber.
    tracing_log::LogTracer::init().ok();

    let registry = tracing_subscriber::registry().with(filter);

    if is_prod() {
        // Production: JSON one event per line; aggregator parses fields.
        registry
            .with(
                fmt::layer()
                    .json()
                    .with_current_span(true)
                    .with_span_list(false) // span context is on the event itself
                    .with_target(true)
                    .with_file(false)
                    .with_line_number(false),
            )
            .init();
    } else {
        // Development: human-readable pretty output, no JSON noise.
        registry
            .with(fmt::layer().pretty().with_target(true))
            .init();
    }
}

fn is_prod() -> bool {
    std::env::var("APP_ENV").as_deref() == Ok("production")
}
```

Key configuration decisions:
- **Production format:** JSON, one event per line — log aggregators parse fields without regex.
- **Level source:** `RUST_LOG` env var — raisable without redeploy. Use per-target syntax (`my_app=debug,sqlx=warn`) to silence noisy deps.
- **Per-module level**: never one global level; suppress chatty deps individually.
- **Redaction:** `tracing` has no built-in redaction. Mark sensitive fields on the error type (`secret: SecretString`) using the `secrecy` crate or your own newtype with a `Debug`/`Display` impl that prints `"<redacted>"`. NEVER format a raw secret into a `tracing` field.
- **One install per process:** call `telemetry::init()` exactly once from `main`. `init()` panics if called twice — that's correct; double-init is a bug.

---

## Writing Log Calls

`tracing` macros take structured key-value pairs followed by a format string.
The format string is the stable event description; the keys are the data.

**✅ Correct — structured fields (base rule: §Structured logging)**
```rust
use tracing::info;

info!(
    user.id = %user_id,
    order.id = %order_id,
    amount_cents = amount,
    currency = %currency,
    "order completed"
);
```

The `%` sigil uses `Display`; `?` uses `Debug`. Bare names take any type
implementing `Value` (numbers, bools, strings).

**❌ Wrong — interpolated string**
```rust
info!("user {} completed order {} for ${}", user_id, order_id, amount);
// Filtering on user.id, summing amount, joining on order.id all become regex.
```

**Field naming — use OpenTelemetry semantic conventions:**
- `http.request.method`, `http.response.status_code`, `url.path`
- `error.type`, `error.message`, `exception.stacktrace`
- `user.id`, `service.name`
- `db.system`, `db.statement`

Dotted names work in `tracing` — the macros accept them directly:
`info!(http.response.status_code = 200, "request handled")`.

**Spans carry context across an operation.** Anything logged inside the span
inherits its fields automatically — the classic way to propagate `trace_id`,
`user.id`, `request.path` without threading them through every call.

```rust
use tracing::{info_span, Instrument};

async fn handle_request(req: Request) -> Result<Response, AppError> {
    let span = info_span!(
        "http.request",
        http.request.method = %req.method(),
        url.path = %req.uri().path(),
        trace_id = %req.trace_id(),
    );
    async move {
        info!("received");           // automatically carries the span fields
        process(req).await
    }
    .instrument(span)
    .await
}
```

The `#[tracing::instrument]` attribute is the macro version for sync/async
functions — prefer it on boundary handlers and any function with named
parameters worth correlating.

---

## Defining Error Types

### Library errors — thiserror enum (typed, matchable)

Use when callers need to discriminate on failure mode. Public, exhaustive,
stable.

```rust
// File: src/user_store/error.rs
// Base rule: diagnostics-base §Error taxonomy, §Retriability

use std::time::Duration;
use thiserror::Error;
use uuid::Uuid;

#[derive(Debug, Error)]
pub enum UserStoreError {
    #[error("user {id} not found")]
    NotFound { id: Uuid },

    #[error("user database is unavailable")]
    DatabaseUnavailable {
        // `#[source]` makes this the std::error::Error::source() return value,
        // preserving the cause chain for boundary logging.
        #[source]
        source: sqlx::Error,
    },

    #[error("rate limited; retry after {}s", retry_after.as_secs())]
    RateLimited { retry_after: Duration },

    #[error("malformed user record: field {field}: {reason}")]
    MalformedRecord {
        field: &'static str,
        reason: String,
        #[source]
        source: serde_json::Error,
    },
}

impl UserStoreError {
    /// Stable code for fingerprinting, dashboards, and docs lookup.
    /// Codes are stable across crate versions; Display text may evolve.
    pub fn code(&self) -> &'static str {
        match self {
            Self::NotFound { .. }            => "USER_STORE.NOT_FOUND",
            Self::DatabaseUnavailable { .. } => "USER_STORE.DB_UNAVAILABLE",
            Self::RateLimited { .. }         => "USER_STORE.RATE_LIMITED",
            Self::MalformedRecord { .. }     => "USER_STORE.MALFORMED_RECORD",
        }
    }

    /// Encoded in the type, not parsed from the message (base §Retriability).
    pub fn is_retriable(&self) -> bool {
        matches!(self, Self::DatabaseUnavailable { .. } | Self::RateLimited { .. })
    }

    pub fn retry_after(&self) -> Option<Duration> {
        if let Self::RateLimited { retry_after } = self { Some(*retry_after) } else { None }
    }

    /// Source-of-fault from the base taxonomy.
    pub fn source_kind(&self) -> Source {
        match self {
            Self::NotFound { .. } | Self::MalformedRecord { .. } => Source::User,
            Self::DatabaseUnavailable { .. } | Self::RateLimited { .. } => Source::Dependency,
        }
    }
}

#[derive(Debug, Clone, Copy)]
pub enum Source { User, Programmer, Dependency, Infra }
```

**Use `#[from]` only when the conversion is unambiguous and adds no
information.** Wrapping `io::Error` into three different variants? Use
`#[source]` and convert manually with `.map_err()`. Wrapping `io::Error` into
exactly one variant that means "filesystem failure"? `#[from]` is fine.

```rust
#[derive(Debug, Error)]
pub enum ConfigError {
    #[error("failed to read config file")]
    Read(#[from] std::io::Error),   // one io::Error variant — From is safe

    #[error("failed to parse TOML")]
    Parse(#[from] toml::de::Error),
}
```

### Library errors with miette — rich CLI display

When the error will be rendered to an end user (CLI / compiler-like tool),
derive `miette::Diagnostic` alongside `thiserror::Error`. Add `code`, `help`,
and `severity` for the rendered output; add `#[source_code]` + `#[label]` when
you can point at a span in user-supplied text.

```rust
use miette::{Diagnostic, NamedSource, SourceSpan};
use thiserror::Error;

#[derive(Debug, Error, Diagnostic)]
#[error("invalid value for `{field}` in {}", source_file.name())]
#[diagnostic(
    code(config::invalid_value),
    help("expected one of: {valid_values}"),
    url("https://docs.example.com/config#{field}"),
)]
pub struct InvalidConfigValue {
    pub field: String,
    pub valid_values: String,

    #[source_code]
    pub source_file: NamedSource<String>,

    #[label("this value")]
    pub span: SourceSpan,
}
```

Rendered with miette's fancy handler this produces a rustc-style diagnostic:
caret under the offending span, a `help:` line, a `code` for filtering, and a
`url` for docs.

### Application errors — anyhow::Result

In binary crates and at the application boundary, return `anyhow::Result<T>`
and chain context as you cross meaningful layers. Don't define a top-level
enum that wraps every possible error — that's `anyhow`'s job.

```rust
// File: src/checkout.rs
// Base rule: diagnostics-base §Context propagation

use anyhow::{Context, Result};

pub async fn checkout_cart(user_id: Uuid) -> Result<Receipt> {
    let user = user_store::load(user_id)
        .await
        .with_context(|| format!("loading user {user_id} for checkout"))?;

    let cart = cart_store::current(user_id)
        .await
        .with_context(|| format!("loading cart for user {user_id}"))?;

    let receipt = billing::charge(&user, &cart)
        .await
        .with_context(|| format!("charging user {user_id} for cart {}", cart.id))?;

    Ok(receipt)
}
```

**Use `.context("...")`, not `.unwrap()` or `.expect()`.** `.expect()` is for
assertions about invariants the type system can't express, not for "I hope
this works."

**Boundary handlers convert `anyhow::Error` to the user-facing form.** Library
code that needs to *match* on a specific variant downcasts: `if let Some(e) =
err.downcast_ref::<UserStoreError>()`. This is rare and lives only at
boundaries — inside the app you propagate.

---

## Cause Chaining — Never Lose the Original

Rust has first-class cause chains via `std::error::Error::source()`. Every
wrapping mechanism in this stack preserves it:

- `thiserror` with `#[source]` or `#[from]` → automatically implements `source()`.
- `anyhow::Error::context(...)` → wraps with a context message, original is `.source()`.
- `miette::Report` → walks the same chain plus its own `Diagnostic` traversal.

**✅ Correct — cause preserved with new context at each layer**
```rust
// Repository layer — wrap sqlx error into a typed library variant
async fn fetch_user(id: Uuid) -> Result<User, UserStoreError> {
    sqlx::query_as!(User, "select * from users where id = $1", id)
        .fetch_one(&pool)
        .await
        .map_err(|e| match e {
            sqlx::Error::RowNotFound => UserStoreError::NotFound { id },
            other => UserStoreError::DatabaseUnavailable { source: other },
        })
}

// Service layer — propagate with `?`, conversion is automatic if #[from] is set
async fn load_for_checkout(id: Uuid) -> anyhow::Result<User> {
    fetch_user(id)
        .await
        .with_context(|| format!("loading user {id} for checkout"))?
        .into_ok()
}
```

**❌ Wrong — cause swallowed**
```rust
// All three of these are bugs:
let user = fetch_user(id).await.unwrap();                       // panics, no chain
let user = fetch_user(id).await.map_err(|_| anyhow!("oops"))?;  // discards source
let user = fetch_user(id).await.map_err(|e| anyhow!("{e}"))?;   // stringifies cause; chain broken
```

Walking the chain at the boundary:

```rust
use std::error::Error as _;

fn log_chain(err: &dyn std::error::Error) -> Vec<String> {
    std::iter::successors(Some(err), |e| e.source())
        .map(|e| e.to_string())
        .collect()
}

// At the boundary:
match result {
    Err(err) => {
        let chain = log_chain(err.as_ref());
        tracing::error!(
            error.type = std::any::type_name_of_val(&*err),
            error.message = %err,
            error.chain = ?chain,
            "checkout failed"
        );
    }
    _ => {}
}
```

`anyhow::Error` has a built-in `.chain()` iterator that returns the same
sequence: `err.chain().map(ToString::to_string).collect()`.

---

## Error Messages — Rust-Specific Style

Rust conventions on top of base rules:

- **Lowercase first letter, no terminal period.** This matches `std::error`
  convention. `thiserror`'s `#[error("...")]` strings should follow it:
  `#[error("invalid port {port}")]`, not `#[error("Invalid port {port}.")]`.
- **Name the failed operation as a verb phrase** — `"failed to bind to {addr}"`,
  `"could not parse manifest"`. Compose well as the inner cause: when wrapped
  with `.context("starting server")`, the chain reads `"starting server: failed
  to bind to 0.0.0.0:8080"`.
- **`anyhow::Context` strings are NOUN PHRASES describing what we were doing**
  — `"loading user 12345 for checkout"`, not `"failed to load user"`. The
  underlying error already said it failed; context says *what we were doing
  when it failed*.
- **Never put a newline in a thiserror Display** — log lines and HTTP bodies
  break on it. Put detail in fields, not in the message.
- **`#[error("{0}")]` on a single transparent wrap** is a code smell — use
  `#[error(transparent)]` instead so `Display` and `source()` both delegate.
- **Never include a stack trace in the Display** — that's for the logger's
  `exception.stacktrace` field or the error tracker, not the human message.

---

## panic! / unwrap / expect — the discipline

`panic!`, `unwrap`, and `expect` are NOT error reporting. They are assertions
about invariants the type system can't express. Misuse is a defect.

| Use case | Right call |
|---|---|
| Recoverable failure | Return `Result`, never panic |
| Hard invariant the type can't express, in production code | `expect("INVARIANT: ...")` describing what must be true, not what failed |
| Test setup that cannot fail in a green build | `.unwrap()` is fine — tests are allowed to panic |
| Programmer bug detected at runtime (e.g., unreachable branch) | `unreachable!("CODE BUG: ...")` |
| Cannot continue startup | Log FATAL via tracing, then `std::process::exit(1)` (NOT panic) |

**`.expect()` message convention:** describe the invariant violated, not the
operation. The reader sees this message when something they thought was
impossible just happened.

```rust
// ❌ Wrong — says nothing about what was expected
let port = env::var("PORT").unwrap();
let port = env::var("PORT").expect("failed to read PORT");

// ✅ Right — describes the invariant
let port = env::var("PORT")
    .expect("PORT env var must be set by the orchestrator before launch");
```

**Never `unwrap()` an `Option` or `Result` from external input.** That input
will eventually be malformed and your service will crash on a Tuesday.

---

## The Application Boundary — Log Once Here

Log at the boundary that decides recovery; propagate everywhere else. Inner
functions return `Result<_, _>`; only the boundary calls `tracing::error!` /
`warn!` / `info!`.

### HTTP boundary (axum example, equivalent for actix-web / warp)

```rust
// File: src/http/error.rs
// Base rule: diagnostics-base §Boundary discipline

use axum::{http::StatusCode, response::{IntoResponse, Response}, Json};
use serde_json::json;

pub struct AppError(pub anyhow::Error);

impl<E> From<E> for AppError where E: Into<anyhow::Error> {
    fn from(err: E) -> Self { Self(err.into()) }
}

impl IntoResponse for AppError {
    fn into_response(self) -> Response {
        // Downcast to specific library errors to choose status + log level.
        // Anything we don't recognize is a 500 + ERROR.
        let (status, code, user_msg, level) = classify(&self.0);

        let chain: Vec<String> = self.0.chain().map(ToString::to_string).collect();

        // The SINGLE log call for this error. Inner layers did not log.
        match level {
            Level::Error => tracing::error!(
                error.code = code, error.chain = ?chain,
                http.response.status_code = status.as_u16(),
                "request failed"
            ),
            Level::Warn => tracing::warn!(
                error.code = code, error.chain = ?chain,
                http.response.status_code = status.as_u16(),
                "request failed"
            ),
            Level::Info => tracing::info!(
                error.code = code,
                http.response.status_code = status.as_u16(),
                "request rejected"
            ),
        }

        (status, Json(json!({
            "error": { "code": code, "message": user_msg }
        }))).into_response()
    }
}

enum Level { Error, Warn, Info }

fn classify(err: &anyhow::Error) -> (StatusCode, &'static str, String, Level) {
    if let Some(e) = err.downcast_ref::<UserStoreError>() {
        return match e {
            UserStoreError::NotFound { .. } =>
                (StatusCode::NOT_FOUND, e.code(), "user not found".into(), Level::Info),
            UserStoreError::RateLimited { .. } =>
                (StatusCode::TOO_MANY_REQUESTS, e.code(), "try again later".into(), Level::Warn),
            UserStoreError::DatabaseUnavailable { .. } =>
                (StatusCode::SERVICE_UNAVAILABLE, e.code(), "service unavailable".into(), Level::Warn),
            UserStoreError::MalformedRecord { .. } =>
                (StatusCode::INTERNAL_SERVER_ERROR, e.code(), "internal error".into(), Level::Error),
        };
    }
    // Unrecognized anyhow::Error: 500 + ERROR.
    (StatusCode::INTERNAL_SERVER_ERROR, "INTERNAL", "internal error".into(), Level::Error)
}
```

**What this handler decides** (base rule §Boundary discipline):
1. **Log level** — `NotFound` is a 404 = user error = INFO (per base taxonomy, not ERROR). `RateLimited` is a degraded transient = WARN. Unknown is ERROR.
2. **Structured fields** — `error.code` for fingerprinting, `error.chain` for the full cause, `http.response.status_code` for filtering.
3. **User-facing body** — translated message; never the raw `anyhow` chain.
4. **Single log call** — inner layers did NOT log this error. They returned `Err(...)?` upward.

### CLI boundary — `main()` returns `miette::Result`

```rust
// File: src/main.rs
use miette::{IntoDiagnostic, Result, WrapErr};

fn main() -> Result<()> {
    miette::set_hook(Box::new(|_| {
        Box::new(miette::MietteHandlerOpts::new()
            .terminal_links(true).build())
    })).ok();

    diagnostics_skill::telemetry::init();

    let args = Args::parse();
    run(args).wrap_err("command failed")
}

fn run(args: Args) -> Result<()> {
    let config = std::fs::read_to_string(&args.config)
        .into_diagnostic()
        .wrap_err_with(|| format!("reading config from {}", args.config.display()))?;
    // ...
    Ok(())
}
```

`miette::Result<T>` is `Result<T, miette::Report>`. Returning it from `main`
gets you a rustc-style printed diagnostic on exit, automatically.

Full boundary handlers for axum/actix-web/CLI/queue-consumer patterns are in
`references/boundary-examples.md`.

---

## Validation / Decoding Errors — Surfacing Schema Issues

Decoding errors from `serde` are **user errors** (base taxonomy: source=user):

- **Log level:** INFO (not ERROR — expected user outcome).
- **HTTP status:** 400.
- **Message:** surface the field path and what was wrong, not the serde
  internals.

```rust
#[derive(Debug, Error, Diagnostic)]
#[error("invalid request body: {message}")]
#[diagnostic(code(http::invalid_body), help("see schema at /docs/schemas"))]
pub struct ValidationError {
    pub message: String,
    pub field_path: String,
    #[source]
    pub source: serde_json::Error,
}

impl ValidationError {
    pub fn from_serde(err: serde_json::Error) -> Self {
        Self {
            message: err.to_string(),
            field_path: format!("line {}, column {}", err.line(), err.column()),
            source: err,
        }
    }
}
```

For richer business-rule validation, see `validator` (derive-based) or `garde`
(builder-style). Wrap their per-field errors in a `ValidationError` variant so
the boundary handler can produce a structured 400 response (one entry per
failing field, not one log line per field).

---

## Retriability — Encode in the Type

Base rule: §Retriability — callers must not parse messages to decide retry
behavior.

```rust
pub trait Retriable {
    fn is_retriable(&self) -> bool;
    fn retry_after(&self) -> Option<Duration> { None }
}

impl Retriable for UserStoreError {
    fn is_retriable(&self) -> bool {
        matches!(self, Self::DatabaseUnavailable { .. } | Self::RateLimited { .. })
    }
    fn retry_after(&self) -> Option<Duration> {
        if let Self::RateLimited { retry_after } = self { Some(*retry_after) } else { None }
    }
}

pub async fn with_retry<T, E, F, Fut>(mut op: F, attempts: u32) -> Result<T, E>
where
    E: Retriable + std::fmt::Display,
    F: FnMut() -> Fut,
    Fut: std::future::Future<Output = Result<T, E>>,
{
    let mut last_err = None;
    for attempt in 1..=attempts {
        match op().await {
            Ok(v) => return Ok(v),
            Err(e) if e.is_retriable() && attempt < attempts => {
                let wait = e.retry_after()
                    .unwrap_or_else(|| Duration::from_millis(100 * 2u64.pow(attempt)));
                tracing::warn!(attempt, wait_ms = wait.as_millis() as u64,
                    error.message = %e, "operation failed, retrying");
                tokio::time::sleep(wait).await;
                last_err = Some(e);
            }
            Err(e) => return Err(e),
        }
    }
    Err(last_err.unwrap())
}
```

---

## Async-Aware Patterns (tokio)

Three failure modes that the base skill does not cover:

- **Errors crossing thread/task boundaries must be `Send + Sync + 'static`.**
  `anyhow::Error` and `miette::Report` already are. `Box<dyn Error>` is NOT —
  use `Box<dyn Error + Send + Sync + 'static>` if you can't use anyhow.
- **`tokio::task::JoinError` from `JoinHandle::await` is a wrapper** — it can
  mean the task panicked OR was cancelled. Match on `.is_panic()` /
  `.is_cancelled()` and translate accordingly. A cancelled task is usually NOT
  an ERROR; a panicked one always is.
- **`#[tracing::instrument]` on `async fn` correctly propagates the span
  across `.await` points.** Use it; do not try to manually `enter()` a span
  across an await — that's a common bug.

Cancellation, span propagation, and `JoinSet` aggregation patterns are in
`references/async-patterns.md`.

---

## Checklist Addendum (Rust-Specific)

Apply AFTER the base skill checklist:

- [ ] Library code uses `thiserror` enum returning `Result<T, MyError>` — not `anyhow::Result` exposed publicly?
- [ ] Application code uses `anyhow::Result` + `.context(...)` at meaningful layers — not `.unwrap()` or stringified errors?
- [ ] Every `#[derive(Error)]` variant either has `#[source]` / `#[from]` on its cause field, or `#[error(transparent)]` if it adds nothing?
- [ ] `.context(...)` strings are noun phrases ("loading user {id}") — not "failed to ..." (the underlying error already says that)?
- [ ] Every error type that crosses a thread/task boundary is `Send + Sync + 'static`?
- [ ] No `.unwrap()` on external input (env, config, request bodies, file contents)?
- [ ] `tracing` calls use structured fields with OTel field names — not interpolated format strings?
- [ ] One global `tracing_subscriber` install in `main`, gated on `APP_ENV` for JSON-vs-pretty?
- [ ] `RUST_LOG` filter set to silence noisy dependencies (`sqlx=warn`, `hyper=warn`)?
- [ ] CLI `main()` returns `miette::Result<()>` for end-user-facing tools (not `Result<(), Box<dyn Error>>`)?
- [ ] Boundary handler logs ERROR/WARN/INFO based on downcast classification — not blanket ERROR on every `anyhow::Error`?
- [ ] `JoinError`-from-cancellation paths logged at DEBUG, not ERROR?
- [ ] Secrets wrapped in a redacting newtype (`secrecy::SecretString` or your own); never formatted raw into a tracing field?
- [ ] Inner layers propagate with `?` and do NOT log — only the boundary logs (single-log rule)?

---

## Quick Reference — Rust Anti-patterns

| Rust Anti-pattern | Fix |
|---|---|
| `println!("error: {e}")` / `eprintln!(...)` in production code paths | Use `tracing::error!` (or `warn!`/`info!` per taxonomy) with structured fields |
| `.unwrap()` / `.expect("failed")` on operations that can legitimately fail | Return `Result`; reserve `expect` for invariants with messages describing the invariant |
| `panic!` to signal recoverable failure | `Err(...)` — panic is for invariant violations and unrecoverable startup failures |
| Library returns `anyhow::Result<T>` publicly | Library exposes a `thiserror` enum so callers can `match` on variants |
| Wrapping with `anyhow!("failed: {}", e)` (stringifies the cause; chain broken) | `e.context("...")` or `Err(e).with_context(\|\| ...)` — `e` is preserved as `.source()` |
| `map_err(\|_\| MyError::Foo)` discarding the underlying error | Use `#[from]` / `#[source]` so the cause is preserved on the variant |
| `#[error("Failed to ...")]` capitalized + terminal period | Rust convention: lowercase, no period — `#[error("failed to ...")]` |
| `tracing::error!("failed for user {}", id)` interpolated | `tracing::error!(user.id = %id, "operation failed")` — structured fields |
| Inner function logs, then returns `Err(...)` (log-and-rethrow) | Inner returns `Err`; boundary logs ONCE with full chain |
| One enormous `AppError` enum covering every possible failure | One enum per domain; use `anyhow` to aggregate at the app boundary |
| Logging `error.localizedDescription`-equivalent (only top-level message) | Log `error.chain` = `err.chain().map(ToString::to_string).collect::<Vec<_>>()` |
| `#[derive(Error)]` enum variants that all wrap `io::Error` via `#[from]` (only one of them ever wins the conversion) | Use `#[source]` and convert explicitly with `.map_err()` — `#[from]` is for unambiguous single-variant conversion |
| `tokio::spawn`'d task that returns `Result` but nobody awaits the `JoinHandle` | Either `await` and handle errors, or use `JoinSet` to aggregate, or wrap in `tracing::error!` on drop |
| `Box<dyn Error>` (not `Send`/`Sync`) returned from an async function | Use `anyhow::Error` (already `Send + Sync + 'static`) or `Box<dyn Error + Send + Sync + 'static>` |
| Newtypes around secrets that derive `Debug` (leaks via `?` or `{:?}` in logs) | Implement `Debug` manually to print `"<redacted>"`, or use `secrecy::SecretString` |

---

## Additional Resources

### Reference Files

For detailed patterns referenced from the sections above:
- **`references/boundary-examples.md`** — Full axum, actix-web, CLI, and queue-consumer boundary handler implementations with classification tables
- **`references/cause-chains.md`** — Deep dive on `?`, `From`/`Into`, `#[from]` vs `#[source]`, `#[error(transparent)]`, `anyhow::Context`, walking the source chain
- **`references/async-patterns.md`** — `#[instrument]` on async fns, `JoinError` classification, `JoinSet` aggregation, span propagation across `.await`, `tokio-cancel` semantics

### Key Crate Docs

- `tracing`: https://docs.rs/tracing
- `tracing-subscriber`: https://docs.rs/tracing-subscriber
- `thiserror`: https://docs.rs/thiserror
- `anyhow`: https://docs.rs/anyhow
- `miette`: https://docs.rs/miette  (read the `Diagnostic` derive docs in particular)
- `secrecy` (for redaction): https://docs.rs/secrecy
- OpenTelemetry Rust: https://github.com/open-telemetry/opentelemetry-rust
- `diagnostics-base`: installed alongside this skill
