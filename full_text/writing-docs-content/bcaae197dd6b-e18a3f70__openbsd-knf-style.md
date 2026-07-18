---
name: openbsd-knf-style
description: >-
  Enforcing OpenBSD Kernel Normal Form (KNF) style in C code. Use when
  writing or reviewing C code targeting OpenBSD, when the user mentions
  style(9) or KNF, or when working with OpenBSD kernel or userland code.
license: MIT
metadata:
  version: 1.0.0
  author: r0
  last-modified: 2026-02-12
  source-material: https://man.openbsd.org/style
allowed-tools: Bash(knfmt *) Bash(gcc *) Bash(clang *) Read Edit Write
---

## Quick Start

Writing OpenBSD-style C? Here's what matters most:

1. 8-char tabs (never spaces), 80-column limit
2. Return type on its own line above function name
3. Include `<sys/types.h>` or `<sys/param.h>` first (never both)
4. Use `err(3)`/`warn(3)` for errors, `strlcpy(3)` for strings, `queue(3)` for lists

Run `knfmt -d yourfile.c` to check — zero diff means you're good.

## When to Use This Skill

- Writing new C code for OpenBSD (kernel or userland)
- Porting code to OpenBSD
- Code review of OpenBSD contributions
- User mentions "style(9)", "KNF", or "OpenBSD style"
- Working in `/usr/src` tree

## Core Rules

### 1. Indentation & Line Length

**8-character tabs** for indentation. 4 spaces for continuation lines. Hard 80-column limit.

```c
// GOOD
int
main(int argc, char *argv[])
{
	int very_long_variable_name = some_function(argument1,
	    argument2, argument3);  /* 4-space continuation */

	if (condition)
		single_statement();

	return 0;
}

// BAD - spaces instead of tabs, exceeds 80 columns
int main(int argc, char *argv[]) {
    int very_long_variable_name = some_function(argument1, argument2, argument3, argument4);
    return 0;
}
```

### 2. Function Declarations

Return type on **separate line** above function name. Prototypes don't include variable names.

```c
// GOOD
static int
function_name(int arg1, const char *arg2)
{
	/* Function body */
}

// Prototype in header
int function_name(int, const char *);

// BAD - return type on same line
static int function_name(int arg1, const char *arg2) {
	/* ... */
}

// BAD - variable names in prototype
int function_name(int arg1, const char *arg2);
```

### 3. Include Ordering

Strict hierarchy. Blank lines between groups.

```c
// GOOD
#include <sys/types.h>  /* OR <sys/param.h>, never both */

#include <sys/queue.h>
#include <sys/socket.h>

#include <netinet/in.h>

#include <ctype.h>
#include <err.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include "pathnames.h"
#include "externs.h"

// BAD - wrong order, no blank lines
#include <stdio.h>
#include <sys/types.h>
#include "externs.h"
#include <sys/queue.h>
```

Order: `<sys/types.h>` → other `<sys/*.h>` → network headers → blank line → `/usr/include` alphabetical → blank line → local `"headers.h"`

### 4. Variable Declarations

Sorted by size (largest first), then alphabetical. One declaration per line.

```c
// GOOD
int
function(void)
{
	struct complicated_struct *csp;
	long long bignum;
	int counter, index;
	char ch, *str;

	/* ... */
}

// BAD - unsorted, multiple per line randomly
int
function(void)
{
	char ch;
	int counter, *str, index;
	long long bignum;
	struct complicated_struct *csp;
}
```

Don't initialize variables with function calls at declaration.

```c
// GOOD
int fd;

fd = open("/dev/null", O_RDONLY);
if (fd == -1)
	err(1, "open");

// BAD - function call in declaration
int fd = open("/dev/null", O_RDONLY);
if (fd == -1)
	err(1, "open");
```

### 5. Control Flow

One statement per line. Braces for multi-statement blocks. No braces for single statements unless it clarifies.

```c
// GOOD
if (condition)
	single_statement();

if (complex_condition) {
	statement1();
	statement2();
}

// switch/case: indent switch, don't indent case
switch (value) {
case 0:
	handle_zero();
	break;
case 1:
	/* FALLTHROUGH */
case 2:
	handle_one_or_two();
	break;
default:
	handle_default();
}

// GOOD - goto cleanup pattern
	if ((fd = open(path, O_RDONLY)) == -1)
		goto fail;

	if (read(fd, buf, sizeof(buf)) == -1)
		goto cleanup;

	process(buf);

cleanup:
	close(fd);
fail:
	return -1;

// BAD - unnecessary braces
if (simple)
{
	statement();
}

// BAD - case indented
switch (value) {
	case 0:
		break;
}

// BAD - missing FALLTHROUGH
switch (value) {
case 0:
	setup();
case 1:  /* implicit fallthrough - add comment! */
	process();
	break;
}
```

### 6. OpenBSD-Specific APIs

**YOU MUST use these** instead of standard C or POSIX equivalents:

```c
// String handling - use strlcpy/strlcat
char dst[64];
if (strlcpy(dst, src, sizeof(dst)) >= sizeof(dst))
	errx(1, "string truncation");

// NOT strcpy, strncpy, or strcat

// Error reporting - use err(3) family
if (fd == -1)
	err(1, "open %s", filename);  /* Includes errno */

if (invalid_input)
	errx(1, "invalid input: %s", input);  /* No errno */

warn("couldn't process %s", filename);  /* Non-fatal */

// NOT fprintf(stderr, ...) or perror()

// Random numbers - use arc4random(3)
uint32_t random_value = arc4random();
uint32_t bounded = arc4random_uniform(100);  /* 0-99 */

// NOT rand() or random()

// Lists - use queue(3) macros
#include <sys/queue.h>

LIST_HEAD(listhead, entry) head;
struct entry {
	int value;
	LIST_ENTRY(entry) entries;
};

LIST_INIT(&head);
LIST_INSERT_HEAD(&head, item, entries);

// NOT handrolled linked lists

// Parsing numbers - use strtonum(3)
const char *errstr;
long long num = strtonum(input, 0, INT_MAX, &errstr);
if (errstr != NULL)
	errx(1, "number is %s: %s", errstr, input);

// NOT atoi() or strtol() without error checking
```

### 7. Types & Constants

```c
// GOOD
unsigned int count;  /* explicit */
const char *str = "string";

#define MAXPATH 1024
#define DEFAULT_PORT 8080

// Use NULL for null pointers
char *ptr = NULL;

// No casting of void * returns
ptr = malloc(sizeof(*ptr));

// BAD
unsigned count;  /* implicit int */
typedef struct foo foo_t;  /* _t suffix reserved */

#define maxpath 1024  /* lowercase macro */

char *ptr = 0;  /* use NULL */
ptr = (char *)malloc(size);  /* unnecessary cast */
```

### 8. Comments

Explain **WHY**, never WHAT. Multi-line comments use `/* ... */`.

```c
// GOOD
/*
 * We need to flush the buffer here because the hardware
 * can't handle more than 64 bytes at once.
 */
flush_buffer();

/* Special case: zero means unlimited. */
if (limit == 0)
	limit = INT_MAX;

// BAD
/* Flush the buffer. */  /* This is obvious */
flush_buffer();

// Increment counter.  /* Don't describe WHAT code does */
counter++;
```

### 9. Kernel vs Userspace Differences

**Kernel code:** NEVER use `static` (it's incompatible with the debugger). Use `KASSERT()` for assertions.

**Userspace code:** Local functions should be `static`. Use `assert()` from `<assert.h>`.

```c
// Userspace
#include <assert.h>

static int
local_helper(int x)
{
	assert(x > 0);
	return x * 2;
}

// Kernel
#include <sys/systm.h>

int  /* No static! */
kernel_helper(int x)
{
	KASSERT(x > 0);
	return x * 2;
}
```

## Validation Steps

**YOU MUST complete all validation before considering work done:**

**Automated validation script:**
```bash
bash "$HOME/.claude/skills/openbsd-knf-style/scripts/validate.sh" yourfile.c
```

This performs:
- knfmt compliance check
- Tab indentation verification
- Banned function detection (strcpy, strncpy, strcat, strncat, atoi, rand, srand)
- 80-column limit check
- Compiler warning check with recommended flags

**Manual validation:**

1. Run `knfmt -d yourfile.c` — output should be empty (zero diff)
2. Compile with `-Wall -Wpointer-arith -Wuninitialized -Wstrict-prototypes -Wmissing-prototypes -Wunused -Wsign-compare -Wshadow` — zero warnings
3. Run `grep -n '	 \| 	' yourfile.c` — no mixed tabs and spaces
4. Manual checklist (see `assets/knf-checklist.md`):
   - [ ] 8-char tabs, no spaces for indentation
   - [ ] Return type on separate line
   - [ ] Include ordering correct
   - [ ] Using err(3), strlcpy(3), queue(3), arc4random(3)
   - [ ] No typedef struct with _t suffix
   - [ ] Comments explain WHY
5. If OpenBSD target: check pledge()/unveil() usage (see `references/pledge-patterns.md`)

## References

- Complete style(9) man page: `references/style9-complete.md`
- OpenBSD API usage: `references/openbsd-apis.md`
- pledge() and unveil() patterns: `references/pledge-patterns.md`
- Common porting issues: `references/porting-gotchas.md`
- knfmt usage and limitations: `references/knfmt-guide.md`
