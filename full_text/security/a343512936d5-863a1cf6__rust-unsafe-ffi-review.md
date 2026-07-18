---
name: rust-unsafe-ffi-review
description: >-
  Reviews Rust unsafe code and FFI bindings for memory safety and soundness issues.
  Use when auditing unsafe blocks, FFI interfaces, or preparing Rust code for security-critical use.
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Grep Glob Bash(cargo clippy *)
---

# Rust Unsafe and FFI Review

Audit Rust code that uses unsafe or interfaces with C/C++ code. You can't let soundness bugs slip through -- they'll become security issues.

## When to Use This Skill

- You've written new `unsafe` blocks or FFI bindings and want soundness verification
- You're reviewing a PR that adds unsafe Rust or C interop code
- You're auditing a crate before adding it as a dependency in a security-sensitive context
- A fuzzer or sanitizer flagged a potential memory safety issue and you're investigating the root cause
- You're wrapping a C library and need to verify the safe API layer is actually sound

## Quick Start

**Critical unsafe patterns to check:**
1. **Uninitialized memory** — Use MaybeUninit, not mem::uninitialized
2. **Dangling references and mutable aliasing** — Lifetime violations, multiple &mut to same memory
3. **Data races** — Send/Sync violations in unsafe code
4. **FFI invariants** — repr(C), null checks, panic unwinding

Run Miri on all unsafe code. If Miri fails, the code isn't sound.

## MANDATORY: Dependency Security Baseline

**MUST complete BEFORE reviewing unsafe code:**

```bash
# Install dependency management tools
cargo install cargo-edit cargo-audit

# Check for outdated dependencies
cargo outdated

# Update ALL dependencies to latest versions
cargo upgrade

# Update Cargo.lock
cargo update

# Scan for known vulnerabilities
cargo audit

# Verify all tests still pass
cargo test
```

**Quality gates:**
- [ ] cargo-edit and cargo-audit installed
- [ ] All dependencies updated to latest versions (verified with crates.io)
- [ ] `cargo outdated` shows "All dependencies are up to date"
- [ ] `cargo audit` shows zero vulnerabilities
- [ ] All tests passing after updates

**Why this matters for unsafe code:**

Outdated dependencies in FFI or unsafe contexts are especially dangerous:
- C library bindings (openssl-sys, libsqlite3-sys) may have known exploits
- Unsafe code often depends on exact library behavior — version changes matter
- Security patches in sys crates require immediate updates

**Do NOT skip this step.** Vulnerable dependencies make unsafe code risks worse.

## ANSSI Secure Rust Guidelines

The French cybersecurity agency's core rules for unsafe Rust. You won't regret following them.

### Rule 1: Document Every unsafe Block

**Bad:**
```rust
unsafe {
    *ptr = value;
}
```

**Good:**
```rust
unsafe {
    // SAFETY: ptr is valid, aligned, and points to initialized T.
    // ptr is not aliased mutably anywhere else.
    *ptr = value;
}
```

**Check:**
- [ ] Every unsafe block has SAFETY comment
- [ ] Comment explains why operation is safe
- [ ] Invariants documented

### Rule 2: Minimize unsafe Scope

**Bad:**
```rust
unsafe {
    do_safe_thing();
    do_another_safe_thing();
    *ptr = value;  // Only this line needs unsafe
}
```

**Good:**
```rust
do_safe_thing();
do_another_safe_thing();
unsafe {
    // SAFETY: ptr is valid and aligned
    *ptr = value;
}
```

**Check:**
- [ ] unsafe blocks contain only operations that need it
- [ ] Safe code not wrapped in unsafe

### Rule 3: No mem::uninitialized

**Bad:**
```rust
let mut x: T = unsafe { mem::uninitialized() };  // Undefined behavior
```

**Good:**
```rust
use std::mem::MaybeUninit;

let mut x = MaybeUninit::<T>::uninit();
// Initialize x...
let x = unsafe {
    // SAFETY: x has been fully initialized above
    x.assume_init()
};
```

**Check:**
- [ ] No use of mem::uninitialized() or mem::zeroed() for non-ZST types
- [ ] Use MaybeUninit for uninitialized memory

### Rule 4: Verify Send/Sync Implementations

**Bad:**
```rust
unsafe impl<T> Send for MyType<T> {}  // Wrong if T: !Send
```

**Good:**
```rust
unsafe impl<T: Send> Send for MyType<T> {}

// Or use PhantomData
struct MyType<T> {
    ptr: *mut T,
    _marker: PhantomData<T>,  // Inherit Send/Sync from T
}
```

**Check:**
- [ ] Manual Send/Sync only when necessary
- [ ] Bounds match actual safety requirements
- [ ] PhantomData used for owned data via raw pointers

## FFI Safety Patterns

### Pattern 1: repr(C) for FFI Types

**Bad:**
```rust
// Rust struct layout is unspecified
struct Point {
    x: i32,
    y: i32,
}

#[no_mangle]
pub extern "C" fn process_point(p: *const Point) { ... }
```

**Good:**
```rust
#[repr(C)]
struct Point {
    x: i32,
    y: i32,
}

#[no_mangle]
pub extern "C" fn process_point(p: *const Point) {
    if p.is_null() {
        return;
    }
    unsafe {
        // SAFETY: Checked non-null above, C caller ensures valid Point
        let point = &*p;
        // Use point...
    }
}
```

**Check:**
- [ ] All FFI structs use #[repr(C)]
- [ ] Null pointer checks before dereferencing
- [ ] No Rust-specific types in extern "C" signatures

### Pattern 2: Catch Panics at FFI Boundary

**Bad:**
```rust
#[no_mangle]
pub extern "C" fn process(data: *const u8, len: usize) -> i32 {
    let slice = unsafe { slice::from_raw_parts(data, len) };
    do_something(slice).unwrap()  // Panics cross FFI boundary!
}
```

**Good:**
```rust
use std::panic::catch_unwind;

#[no_mangle]
pub extern "C" fn process(data: *const u8, len: usize) -> i32 {
    let result = catch_unwind(|| {
        if data.is_null() {
            return -1;
        }
        let slice = unsafe {
            // SAFETY: C caller guarantees data is valid for len bytes
            slice::from_raw_parts(data, len)
        };
        match do_something(slice) {
            Ok(val) => val,
            Err(_) => -1,
        }
    });

    result.unwrap_or(-1)
}
```

**Check:**
- [ ] FFI functions use catch_unwind
- [ ] Panics can't unwind into C code
- [ ] Error codes returned instead of panicking

### Pattern 3: Ownership Transfer via Box

**Bad:**
```rust
#[no_mangle]
pub extern "C" fn create_object() -> *mut MyObject {
    let obj = MyObject::new();
    &obj as *const _ as *mut _  // Dangling pointer!
}
```

**Good:**
```rust
#[no_mangle]
pub extern "C" fn create_object() -> *mut MyObject {
    Box::into_raw(Box::new(MyObject::new()))
}

#[no_mangle]
pub extern "C" fn destroy_object(ptr: *mut MyObject) {
    if !ptr.is_null() {
        unsafe {
            // SAFETY: Pointer created by create_object, called once
            drop(Box::from_raw(ptr));
        }
    }
}
```

**Check:**
- [ ] Objects returned via Box::into_raw
- [ ] Destruction via Box::from_raw
- [ ] Documentation requires paired create/destroy calls

### Pattern 4: CString for C Strings

**Bad:**
```rust
#[no_mangle]
pub extern "C" fn get_name() -> *const c_char {
    "hello".as_ptr() as *const c_char  // No null terminator!
}
```

**Good:**
```rust
use std::ffi::CString;

#[no_mangle]
pub extern "C" fn get_name() -> *mut c_char {
    CString::new("hello").unwrap().into_raw()
}

#[no_mangle]
pub extern "C" fn free_string(s: *mut c_char) {
    if !s.is_null() {
        unsafe {
            // SAFETY: String created by get_name, called once
            drop(CString::from_raw(s));
        }
    }
}
```

**Check:**
- [ ] CString/CStr used for C strings
- [ ] Null termination guaranteed
- [ ] Strings freed via CString::from_raw

## Common Unsafe Bugs

Here's where things go wrong most often.

### Bug 1: Mutable Aliasing

**Unsound:**
```rust
let mut data = vec![1, 2, 3];
let ptr1 = data.as_mut_ptr();
let ptr2 = data.as_mut_ptr();

unsafe {
    *ptr1 = 10;  // Violation: two mutable aliases
    *ptr2 = 20;
}
```

**Sound:**
```rust
let mut data = vec![1, 2, 3];
let ptr = data.as_mut_ptr();

unsafe {
    // SAFETY: No other references to data[0] exist
    *ptr.offset(0) = 10;
    // SAFETY: No other references to data[1] exist
    *ptr.offset(1) = 20;
}
```

### Bug 2: Lifetime Extension

**Unsound:**
```rust
fn extend_lifetime<'a>(s: &str) -> &'a str {
    unsafe { std::mem::transmute(s) }  // Dangling reference!
}

let s = extend_lifetime(&String::from("temp"));
// s is now dangling after String dropped
```

**Sound:**
```rust
// Don't try to extend lifetimes with unsafe
// If you need owned data, use String or Cow<str>
fn use_string(s: String) -> String {
    s  // Transfer ownership properly
}
```

### Bug 3: Unaligned Access

**Unsound:**
```rust
#[repr(C, packed)]
struct Packed {
    a: u8,
    b: u64,  // Misaligned if after u8
}

let packed = Packed { a: 1, b: 2 };
let ptr: *const u64 = &packed.b;
unsafe {
    let val = *ptr;  // Undefined behavior: unaligned load
}
```

**Sound:**
```rust
use std::ptr;

#[repr(C, packed)]
struct Packed {
    a: u8,
    b: u64,
}

let packed = Packed { a: 1, b: 2 };
let val = unsafe {
    // SAFETY: ptr::read_unaligned handles misalignment
    ptr::read_unaligned(&packed.b)
};
```

## Validation Tools

### Miri: Undefined Behavior Detector

Run on all unsafe code:

```bash
rustup +nightly component add miri
cargo +nightly miri test
```

Miri catches:
- Use-after-free
- Out-of-bounds accesses
- Uninitialized memory use
- Invalid pointer arithmetic
- Data races
- Violations of unsafe code guidelines

**If Miri reports an error, the code isn't sound.**

### Clippy Restriction Lints

Enable strict lints:

```toml
# clippy.toml
doc-valid-idents = ["FFI"]
```

```bash
cargo clippy -- \
  -D clippy::undocumented_unsafe_blocks \
  -D clippy::missing_safety_doc \
  -D clippy::mem_forget \
  -W clippy::cast_ptr_alignment \
  -W clippy::multiple_unsafe_ops_per_block
```

**Check:**
- [ ] No undocumented unsafe blocks
- [ ] Functions with unsafe have # Safety section
- [ ] Alignment checked for casts

### cargo-geiger: Unsafe Code Metrics

```bash
cargo install cargo-geiger
cargo geiger
```

Shows unsafe usage across dependencies. You'll want to minimize the unsafe surface.

### cargo-audit: Vulnerability Scanner

```bash
cargo install cargo-audit
cargo audit
```

Checks dependencies against RustSec database.

### Test effectiveness: cargo-mutants + cargo-crap (mandatory for unsafe code)

Unsafe Rust with passing tests but weak assertions is the worst of both worlds — the type system isn't protecting you, and neither is the suite. Two mechanical checks close that gap:

- **`cargo mutants --in-diff <(git diff origin/main)`** — surfaces lines the test suite can't constrain. Any surviving mutant on an unsafe block means your `// SAFETY:` claim isn't backed by a test.
- **`cargo llvm-cov --lcov --output-path lcov.info && cargo crap --lcov lcov.info`** — produces a CRAP score (Savoia & Evans 2007: `comp² × (1 − cov)³ + comp`). Threshold 30. Any unsafe-containing function above the threshold is a P0 finding.

Full runbook (reading mutation output, scoping, SARIF for CI, cross-language equivalents for FFI's C side, version pinning caveats): [references/test-effectiveness.md](references/test-effectiveness.md).

### cargo-deny: Policy Enforcement

```bash
cargo install cargo-deny
cargo deny check
```

Enforces license compliance, ban

s unsafe in dependencies, security policy.

## Unsafe Checklist

Don't merge unsafe code until you've verified all of these:

**Documentation:**
- [ ] SAFETY comment explains why operation is safe
- [ ] All invariants documented
- [ ] # Safety section in public unsafe fn docs

**Soundness:**
- [ ] Miri passes with no errors
- [ ] No mutable aliasing
- [ ] No lifetime extension
- [ ] No uninitialized memory (use MaybeUninit)

**FFI:**
- [ ] All FFI types use #[repr(C)]
- [ ] Null pointers checked
- [ ] Panics caught at boundary
- [ ] Ownership transfer documented

**Testing:**
- [ ] Unit tests for unsafe code paths
- [ ] Miri runs in CI
- [ ] AddressSanitizer/MemorySanitizer clean (if applicable)
- [ ] **cargo-mutants:** zero surviving mutants on changed unsafe / FFI lines (`cargo mutants --in-diff <(git diff origin/main)`)
- [ ] **cargo-crap:** no unsafe-containing function scores above 30 (`cargo crap --lcov lcov.info`)

**Linting:**
- [ ] cargo clippy passes with restriction lints
- [ ] cargo geiger shows minimal unsafe usage
- [ ] cargo audit reports no vulnerabilities

## Writing Style

Apply `natural-writing-style` to all review output and findings.

Review findings should be direct and specific — state what you found and where, not vague summaries. Don't claim issues are "fixed" or "resolved" unless you've verified the fix. Cite specific line numbers or file paths where relevant.

## Resources

- `references/anssi-guidelines.md` — Complete ANSSI Secure Rust rules
- `references/ffi-cookbook.md` — FFI patterns with examples
- `references/miri-usage.md` — Running Miri, interpreting errors
- `references/test-effectiveness.md` — cargo-mutants and cargo-crap runbook for unsafe / FFI code
- `assets/unsafe-checklist.md` — Pre-commit unsafe code review
