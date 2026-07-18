---
name: kernel-dev-workflow
description: >-
  Linux kernel development workflow including coding style, testing, and patch submission.
  Use when developing kernel modules, drivers, or contributing to mainline kernel.
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Write Edit Bash(make *) Bash(git *) Bash(checkpatch.pl *)
---

# Kernel Development Workflow

## When to Use This Skill

- You're writing a new kernel module or driver and need to follow mainline submission standards
- You want to check an existing patch against kernel coding style before sending it to LKML
- You're preparing a patch series for submission and need to run checkpatch, find maintainers, and format emails correctly
- You're adding KUnit tests to kernel code and need the test structure and build configuration
- You've received review feedback on a kernel patch and are preparing a v2 or v3 revision

Develop Linux kernel code following mainline standards. Write clean patches, test thoroughly, submit correctly.

## Quick Start

**Essential workflow:**
1. **Follow coding style** — Run checkpatch.pl on every commit
2. **Write KUnit tests** — Test code before submission
3. **One logical change per patch** — Don't mix features and fixes
4. **Good commit messages + correct reviewers** — 50-char summary, detailed body, use get_maintainer.pl

Every patch goes through: write → test → checkpatch → format-patch → send-email.

## Coding Style

Linux kernel has strict style requirements (Documentation/process/coding-style.rst):

### Indentation

**Tabs, not spaces:**
```c
// GOOD
int function(void)
{
	int x;  // Tab indentation
	if (condition) {
		do_something();  // Tab
	}
}

// BAD - spaces
int function(void)
{
    int x;  // Spaces - rejected
}
```

8-character tabs. If your code goes past column 80, it's time to refactor.

### Braces

**K&R style:**
```c
// GOOD
if (condition) {
	action();
}

// Also OK for single statement
if (condition)
	action();

// BAD - opening brace on new line (except functions)
if (condition)
{
	action();
}
```

Functions have opening brace on new line:
```c
int function(int arg)
{
	// body
}
```

### Naming

**Lowercase with underscores:**
```c
// GOOD
int process_buffer(struct device *dev)
{
	unsigned long flags;
	spin_lock_irqsave(&dev->lock, flags);
}

// BAD - CamelCase
int ProcessBuffer(struct Device *Dev)
```

### Line Length

Aim for 80 columns, hard limit at 100 for statements that won't be clear if broken.

**GOOD:**
```c
if (condition1 && condition2 && condition3 &&
    condition4 && condition5) {
	action();
}
```

**BAD:**
```c
if (condition1 && condition2 && condition3 && condition4 && condition5) {
	action();
}
```

## checkpatch.pl

Run on every patch:

```bash
scripts/checkpatch.pl 0001-my-patch.patch
```

**Common errors:**

```
ERROR: trailing whitespace
ERROR: space required after that ',' (ctx:VxV)
WARNING: line over 80 characters
WARNING: Missing Signed-off-by: line(s)
```

Fix all ERRORS. Fix WARNINGs unless there's a good reason (document in commit message if ignored).

**Check a commit:**
```bash
git format-patch -1 HEAD
scripts/checkpatch.pl 0001-*.patch
```

**Check unstaged changes:**
```bash
git diff | scripts/checkpatch.pl -
```

## KUnit Testing

Write tests for new code. You can't skip this:

### Simple Test

```c
// my_module_test.c
#include <kunit/test.h>
#include "my_module.h"

static void test_buffer_init(struct kunit *test)
{
	struct buffer *buf = buffer_create(1024);

	KUNIT_EXPECT_NOT_NULL(test, buf);
	KUNIT_EXPECT_EQ(test, buf->size, 1024);

	buffer_destroy(buf);
}

static struct kunit_case my_module_cases[] = {
	KUNIT_CASE(test_buffer_init),
	{}
};

static struct kunit_suite my_module_suite = {
	.name = "my_module",
	.test_cases = my_module_cases,
};

kunit_test_suite(my_module_suite);
```

### Run Tests

```bash
# Build with KUnit
./tools/testing/kunit/kunit.py run --kunitconfig=./drivers/my_module

# Or manually
make ARCH=um O=build_kunit menuconfig  # Enable KUnit and module
make ARCH=um O=build_kunit
build_kunit/vmlinux
```

**Output:**
```
TAP version 14
1..1
ok 1 - my_module
# Totals: pass:1 fail:0 skip:0 total:1
```

## Commit Messages

### Format

```
subsystem: brief description (50 chars max)

More detailed explanation. Wrap at 72 characters. Explain what and why,
not how (code shows how).

If this fixes a bug, reference it:
Fixes: 1234abcd5678 ("original commit title")

Reported-by: Reporter Name <email@example.com>
Signed-off-by: Your Name <your@email.com>
```

### Example

```
net: Fix buffer overflow in packet parsing

The packet parser doesn't validate length before copying data,
allowing attackers to overflow the stack buffer with crafted packets.

Add length check before memcpy(). Reject packets that claim
size larger than MAX_PACKET_SIZE.

Fixes: abcd1234ef56 ("net: Add packet parsing support")
Reported-by: Security Researcher <sec@example.com>
Signed-off-by: Developer Name <dev@email.com>
```

**First line rules:**
- Subsystem prefix (net:, drivers/usb:, mm:, etc.)
- Present tense ("Fix" not "Fixed")
- No period at end
- Under 50 characters

**Body:**
- Explain problem and solution
- Why this change is needed
- Reference related commits with Fixes: tag
- Wrap at 72 columns

## Patch Submission

### Create Patch

```bash
# Single commit
git format-patch -1 HEAD

# Last 3 commits as series
git format-patch -3 HEAD --cover-letter

# Edit cover letter
vim 0000-cover-letter.patch
```

**Cover letter for series:**
```
[PATCH 0/3] Improve error handling in widget driver

This series improves error handling in the widget driver:

Patch 1: Add missing error checks in initialization
Patch 2: Fix resource leak on error path
Patch 3: Add KUnit tests for error conditions

Tested on hardware foo-board with kernel 6.1.

Your Name (3):
  widget: Add error checks to init
  widget: Fix resource leak
  widget: Add KUnit tests
```

### Find Maintainers

```bash
scripts/get_maintainer.pl 0001-my-patch.patch
```

Output:
```
Jane Maintainer <jane@kernel.org> (maintainer:WIDGET DRIVER)
John Reviewer <john@company.com> (reviewer:WIDGET DRIVER)
linux-kernel@vger.kernel.org (open list)
```

### Send Patch

```bash
git send-email --to="jane@kernel.org" \
               --cc="john@company.com" \
               --cc="linux-kernel@vger.kernel.org" \
               0001-my-patch.patch
```

**Configure git send-email:**
```bash
git config sendemail.from "Your Name <you@email.com>"
git config sendemail.smtpserver smtp.gmail.com
git config sendemail.smtpserverport 587
git config sendemail.smtpencryption tls
git config sendemail.smtpuser you@gmail.com
```

## Static Analysis

### Sparse

Check for type errors:

```bash
make C=2 drivers/my_module/
```

**Warnings:**
```
drivers/my_module/main.c:45:28: warning: incorrect type in argument 1
drivers/my_module/main.c:45:28:    expected void [noderef] __iomem *addr
drivers/my_module/main.c:45:28:    got void *ptr
```

Fix by adding proper annotations:
```c
void __iomem *addr = ioremap(phys_addr, size);
```

### Smatch

Find logic bugs:

```bash
~/smatch/smatch_scripts/build_kernel.sh
~/smatch/smatch_scripts/test_kernel.sh drivers/my_module/
```

### Coccinelle

Semantic patches for patterns:

```bash
make coccicheck MODE=report
```

## Kernel Sanitizers

### KASAN (AddressSanitizer)

Detects memory errors:

```make
CONFIG_KASAN=y
CONFIG_KASAN_INLINE=y
```

Boot with KASAN, run tests. Catches:
- Use-after-free
- Out-of-bounds access
- Double-free

### UBSAN (UndefinedBehaviorSanitizer)

Detects undefined behavior:

```make
CONFIG_UBSAN=y
CONFIG_UBSAN_TRAP=y
```

### KMSAN (MemorySanitizer)

Detects uninitialized memory:

```make
CONFIG_KMSAN=y
```

### KCSAN (ConcurrencySanitizer)

Detects data races:

```make
CONFIG_KCSAN=y
```

Run full test suite with sanitizers enabled.

## Common Mistakes

### Mistake 1: Mixed Changes

**BAD:**
```
Fix bug and refactor code

- Fix null pointer dereference
- Rename variables for clarity
- Add new feature
```

**GOOD:**
Split into separate patches:
1. Fix null pointer dereference
2. Rename variables
3. Add new feature
4. Update documentation for the new feature

### Mistake 2: No Signed-off-by

Every patch needs your sign-off. You'll regret forgetting this:

```bash
git commit -s
```

This adds:
```
Signed-off-by: Your Name <you@email.com>
```

### Mistake 3: Ignoring checkpatch

If checkpatch complains, fix it. Don't send patches with style errors.

### Mistake 4: No Testing

Document testing in commit message:
```
Tested on x86_64 with hardware device XYZ.
Tested with KUnit test suite (all pass).
```

## Development Cycle

1. **Write code** following style guide
2. **Write KUnit tests** for new functionality
3. **Run tests** (KUnit, kselftest if applicable)
4. **Run checkpatch** and fix issues
5. **Run sparse/smatch** if touching tricky code
6. **Test with sanitizers** (KASAN/UBSAN)
7. **Commit with good message**
8. **Format patch** with git format-patch
9. **Find maintainers** with get_maintainer.pl
10. **Send patch** with git send-email
11. **Address review feedback** and resend (v2, v3, etc.)

See [references/kernel-analysis-tools.md](references/kernel-analysis-tools.md) for detailed usage of checkpatch.pl, Sparse, Smatch, Coccinelle, and kernel sanitizers (KASAN, UBSAN, KMSAN, KCSAN).

## Writing Style

Patch descriptions and commit messages are permanent documentation. Apply `natural-writing-style`:

- Follow kernel commit message conventions: imperative mood, 72-char subject, body explains WHY
- Don't claim patches "fix all instances" unless you've audited every call site
- Be specific about what was tested (which configs, architectures) and what wasn't
- Use contractions in cover letters and review comments; match LKML discourse style

## Resources

- `references/coding-style-full.md` — Complete kernel coding style guide
- `references/kunit-guide.md` — In-depth KUnit test writing
- `references/patch-submission.md` — Detailed submission process
- `assets/commit-template.txt` — Template for commit messages
