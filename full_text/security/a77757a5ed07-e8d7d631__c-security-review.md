---
name: c-security-review
description: >-
  Security-focused code review for C programs targeting CWE Top 25 and CERT C violations.
  Use when auditing C code for memory safety, input validation, and cryptographic issues.
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Grep Glob Bash(cppcheck *) Bash(clang *) AskUserQuestion
---

# C Security Review

Catch security vulnerabilities in C code before they ship. You can't afford to miss these in production.

## Quick Start

Scan the entry points first — find all functions that accept external input — then **use `AskUserQuestion`** to confirm: "I found [X files / Y functions] that handle external input. Do you want a full audit or should I focus on specific modules? I spotted [top findings] as likely areas of concern."

**Critical checks:**
1. **Buffer overflows** — Use bounded functions (strlcpy, snprintf)
2. **Integer overflows** — Check arithmetic before use
3. **Use-after-free** — Clear pointers after free, validate lifetimes
4. **Injection flaws** — No user input as format strings, no untrusted data in system()

Run these checks on every function that handles external input. Don't assume the caller did it already.

## MANDATORY: Library Dependency Audit

**Before reviewing code, MUST check all third-party libraries:**

```bash
# Check for known vulnerabilities in C libraries
# Use your package manager to list installed libraries
pkg-config --list-all | grep -E 'ssl|crypto|curl|xml|json'

# For each library, check latest version
pkg-config --modversion openssl
pkg-config --modversion libcurl

# Update libraries to latest versions (requires system package manager)
# Debian/Ubuntu:
sudo apt update && sudo apt upgrade libssl-dev libcurl4-openssl-dev
# Fedora/RHEL:
sudo dnf update openssl-devel libcurl-devel
# Arch:
sudo pacman -Syu openssl curl
# OpenBSD:
sudo pkg_add -u
```

**Quality gate:**
- [ ] All third-party libraries updated to latest stable versions
- [ ] No known CVEs in dependencies (check https://www.cvedetails.com/)
- [ ] Vendored code (if any) updated to latest upstream

**C-specific dependency concerns:**
- OpenSSL/LibreSSL versions (crypto vulnerabilities)
- zlib versions (compression vulnerabilities)
- libcurl versions (network security)
- libxml2/expat versions (XXE vulnerabilities)

**CRITICAL:** For embedded or vendored libraries, MUST manually check upstream for security patches.

## CWE Top 25 Patterns in C

### CWE-787: Out-of-bounds Write (Buffer Overflow)

**Vulnerable:**
```c
void copy_data(char *dest, const char *src) {
    strcpy(dest, src);  // No bounds checking
}

char buffer[32];
strcpy(buffer, user_input);  // Overflow if input > 32 bytes
```

**Secure:**
```c
#include <string.h>  // For strlcpy (OpenBSD)
// OR
#include <bsd/string.h>  // For libbsd on Linux

void copy_data(char *dest, size_t dest_size, const char *src) {
    strlcpy(dest, src, dest_size);  // Guaranteed null-termination
}

char buffer[32];
strlcpy(buffer, user_input, sizeof(buffer));
```

**Check:**
- [ ] No use of strcpy, strcat, sprintf, gets
- [ ] All string operations use bounded versions
- [ ] Buffer sizes passed explicitly to functions

### CWE-79: Improper Input Validation

**Vulnerable:**
```c
void process_filename(const char *filename) {
    char cmd[256];
    sprintf(cmd, "cat %s", filename);  // Injection if filename = "; rm -rf /"
    system(cmd);
}
```

**Secure:**
```c
#include <ctype.h>
#include <stdbool.h>

bool is_safe_filename(const char *name) {
    for (size_t i = 0; name[i]; i++) {
        if (!isalnum(name[i]) && name[i] != '.' && name[i] != '_') {
            return false;  // Reject special chars
        }
    }
    return true;
}

void process_filename(const char *filename) {
    if (!is_safe_filename(filename)) {
        return;  // Reject unsafe input
    }
    // Use safe API instead of system()
    FILE *f = fopen(filename, "r");
    if (f) {
        // Process file safely
        fclose(f);
    }
}
```

**Check:**
- [ ] All external input validated before use
- [ ] Allowlist validation (not blocklist)
- [ ] No use of system(), popen() with untrusted data

### CWE-125: Out-of-bounds Read

**Vulnerable:**
```c
int get_value(int *array, int index) {
    return array[index];  // No bounds check
}

int data[10];
int val = get_value(data, user_index);  // Read beyond bounds
```

**Secure:**
```c
#include <errno.h>

int get_value(int *array, size_t array_len, size_t index, int *out) {
    if (index >= array_len) {
        errno = EINVAL;
        return -1;
    }
    *out = array[index];
    return 0;
}

int data[10];
int val;
if (get_value(data, 10, user_index, &val) == 0) {
    // Use val safely
}
```

**Check:**
- [ ] Array access includes bounds checking
- [ ] Index validation before use
- [ ] Errors handled properly

### CWE-416: Use After Free

**Vulnerable:**
```c
void process() {
    char *buffer = malloc(1024);
    free(buffer);
    strcpy(buffer, "data");  // Use after free - undefined behavior
}
```

**Secure:**
```c
void process() {
    char *buffer = malloc(1024);
    if (!buffer) return;

    // Use buffer...

    free(buffer);
    buffer = NULL;  // Clear pointer
}

// Better: Use explicit_bzero before free for sensitive data
void process_sensitive() {
    char *password = malloc(128);
    if (!password) return;

    // Use password...

    explicit_bzero(password, 128);  // Clear memory
    free(password);
    password = NULL;
}
```

**Check:**
- [ ] Pointers set to NULL after free
- [ ] No use of freed pointers
- [ ] Sensitive data cleared before free

### CWE-190: Integer Overflow

**Vulnerable:**
```c
void allocate_buffer(size_t count, size_t size) {
    size_t total = count * size;  // Overflow if count * size > SIZE_MAX
    char *buf = malloc(total);
    // ...
}
```

**Secure:**
```c
#include <stdint.h>
#include <limits.h>

void *safe_multiply_alloc(size_t count, size_t size) {
    // Check for overflow before multiplication
    if (count > 0 && size > SIZE_MAX / count) {
        errno = EOVERFLOW;
        return NULL;
    }
    return malloc(count * size);
}

// Or use reallocarray (OpenBSD)
void *allocate_buffer(size_t count, size_t size) {
    return reallocarray(NULL, count, size);  // Checks overflow internally
}
```

**Check:**
- [ ] Arithmetic checked for overflow before use
- [ ] Use reallocarray where available
- [ ] Size calculations validated

## CERT C Critical Rules

Here's what the CERT C standard says about the most dangerous patterns.

### STR31-C: No null-termination assumptions

**Vulnerable:**
```c
char dest[10];
strncpy(dest, src, sizeof(dest));
printf("%s\n", dest);  // May not be null-terminated
```

**Secure:**
```c
char dest[10];
strncpy(dest, src, sizeof(dest) - 1);
dest[sizeof(dest) - 1] = '\0';  // Ensure termination

// Or use strlcpy (better)
strlcpy(dest, src, sizeof(dest));
```

### FIO30-C: No format string from user input

**Vulnerable:**
```c
void log_message(const char *user_msg) {
    syslog(LOG_INFO, user_msg);  // Format string attack
}
```

**Secure:**
```c
void log_message(const char *user_msg) {
    syslog(LOG_INFO, "%s", user_msg);  // Use fixed format
}
```

### MEM30-C: Don't access freed memory

Already covered in CWE-416 above.

### INT32-C: Ensure no signed integer overflow

**Vulnerable:**
```c
int total = a + b;  // Overflow causes undefined behavior
```

**Secure:**
```c
#include <limits.h>

bool safe_add(int a, int b, int *result) {
    if (a > 0 && b > INT_MAX - a) {
        return false;  // Would overflow
    }
    if (a < 0 && b < INT_MIN - a) {
        return false;  // Would underflow
    }
    *result = a + b;
    return true;
}
```

## Dangerous Functions → Safe Replacements

| Dangerous | Why | Use Instead |
|-----------|-----|-------------|
| `strcpy()` | No bounds check | `strlcpy()` or `strncpy()` + null term |
| `strcat()` | No bounds check | `strlcat()` or careful `strncat()` |
| `sprintf()` | No bounds check | `snprintf()` |
| `gets()` | No bounds check | `fgets()` |
| `scanf("%s")` | No bounds check | `scanf("%99s")` with limit |
| `strlen()` on untrusted | No length limit | `strnlen()` |
| `system()` | Command injection | `execve()` with args array |
| `popen()` | Command injection | `fork()` + `execve()` |
| `rand()` | Not cryptographic | `arc4random()` (BSD) or `getrandom()` |
| `atoi()` | No error checking | `strtol()` with validation |

## Memory Safety Checklist

You'll want to run through this for each function:

**Allocation:**
- [ ] Check malloc/calloc return value (can be NULL)
- [ ] Size calculations checked for integer overflow
- [ ] Use reallocarray instead of manual size multiplication

**Access:**
- [ ] All array indices validated
- [ ] String operations use bounded functions
- [ ] No pointer arithmetic beyond allocated bounds

**Deallocation:**
- [ ] Every malloc has matching free
- [ ] Pointers set to NULL after free
- [ ] No double-free possible
- [ ] Sensitive data cleared before free

**Pointers:**
- [ ] Initialized to NULL or valid address
- [ ] NULL checks before dereference
- [ ] No dangling pointers after free

## Compiler Hardening Flags

**GCC/Clang minimum:**
```makefile
CFLAGS += -Wall -Wextra -Werror
CFLAGS += -D_FORTIFY_SOURCE=2
CFLAGS += -fstack-protector-strong
CFLAGS += -fPIE
LDFLAGS += -pie -Wl,-z,relro,-z,now
```

**Explanation:**
- `-Wall -Wextra -Werror` — Treat warnings as errors
- `-D_FORTIFY_SOURCE=2` — Buffer overflow detection
- `-fstack-protector-strong` — Stack canaries
- `-fPIE` + `-pie` — Position independent executable (ASLR)
- `-Wl,-z,relro,-z,now` — Full RELRO (GOT protection)

**Additional hardening:**
```makefile
CFLAGS += -Wformat=2 -Wformat-security
CFLAGS += -Wnull-dereference
CFLAGS += -Wstack-protector
CFLAGS += -Wtrampolines
CFLAGS += -fno-common
```

## Static Analysis Tools

**These won't catch everything, but run them on every commit:**

```bash
# cppcheck - basic static analysis
cppcheck --enable=all --error-exitcode=1 src/

# clang static analyzer
scan-build make

# Semgrep with C rules
semgrep --config=p/cwe-top-25 src/
```

**For OpenBSD projects:**
```bash
# Lint with OpenBSD compiler
cc -Wall -Wextra -pedantic -Wformat=2 *.c
```

## Runtime Analysis

Static analysis isn't enough on its own. Use these runtime tools too.

**AddressSanitizer (ASan) -- It's the fastest way to detect memory errors:**
```bash
cc -fsanitize=address -g program.c
./a.out
```

**UndefinedBehaviorSanitizer (UBSan) — Detects UB:**
```bash
cc -fsanitize=undefined -g program.c
./a.out
```

**Valgrind — Memory leak detection:**
```bash
valgrind --leak-check=full ./program
```

## Test Effectiveness: Mutation Testing and CRAP

Memory-safety bugs are routinely shipped with passing test suites — the tests run the happy path, the bug lives on a branch the tests never explore. Two checks reveal that class of gap mechanically.

**Mutation testing for C with mull:**

```bash
# Install: https://mull.readthedocs.io/
brew install mull-project/mull/mull        # or build from source

# Run with your CMake / build setup
mull-runner-19 --ide-reporter ./build/tests
```

Mull mutates C/C++ operators, branches, and constants. A surviving mutant on memory-handling code (null checks, length checks, bounds, free / use-after-free pairs) is a memory-safety bug waiting to manifest — the test suite literally cannot tell whether the line is correct.

**CRAP score for C:**

There's no packaged `cargo-crap` equivalent for C. Compute it from the formula by hand:

```bash
# 1. Cyclomatic complexity per function
pmccabe src/*.c | sort -rn | head -20

# 2. Coverage per function
cc -fprofile-arcs -ftest-coverage -g src/*.c -o test_runner
./test_runner
gcov src/*.c
# (or use lcov for line / branch coverage data)

# 3. CRAP = comp² × (1 − cov/100)³ + comp  (Savoia & Evans, 2007)
```

Any function with cyclomatic complexity > 8 AND coverage < 70% will land above the conventional threshold of 30 — that's a P1 candidate for tests-then-refactor. For C codebases that ship a Java or .NET binding alongside, `crap4java` and NDepend produce the same score on those sides. See `.claude/rules/static-analysis.md` for cross-language guidance.

**Why this matters for C specifically:** the language gives you no help. Every conditional branch, every pointer dereference, every length parameter is a place a bug can hide. Mutation testing and CRAP turn "did we write tests?" into a measurable signal — which, in C, is the only signal that maps to safety.

## When to Use This Skill

- Auditing C code for memory safety violations before committing or shipping
- Reviewing code that handles external input: network data, file content, user strings
- Checking a codebase after adding new string manipulation or buffer operations
- Validating that dangerous functions (strcpy, sprintf, system) have been replaced
- Pre-release security review of any C library or daemon

## Writing Style

Apply `natural-writing-style` to all review output and findings.

Review findings should be direct and specific — state what you found and where (function name, line number if available), not vague summaries. Don't claim issues are "fixed" unless you've verified the fix compiles and passes tests. Cite file paths and function names when reporting vulnerabilities.

## Resources

- `references/cwe-top-25.md` — Detailed coverage of all CWE Top 25
- `references/cert-c-rules.md` — Complete CERT C Secure Coding rules
- `references/dangerous-functions.md` — Full banned function list with replacements
- `assets/security-checklist.md` — Pre-commit security review checklist
