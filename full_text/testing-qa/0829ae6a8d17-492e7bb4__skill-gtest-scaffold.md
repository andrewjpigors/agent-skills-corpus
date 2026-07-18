---
name: skill-gtest-scaffold
description: >
  Generate GTest test file scaffolds with fixtures, setup/teardown, and proper
  Makefile integration. Trigger when creating tests for GLib/GObject C projects,
  writing test suites, or scaffolding test infrastructure.
---

# Skill: GTest Scaffold Generator

Generates production-quality GLib test files (`test-*.c`) with fixtures, assertions, temporary file handling, and Makefile integration. Follows the exact patterns used in bacon, libreclaw, and gst projects. All output follows gnu89 C conventions.

## When to Use

- When creating a new test file for a GLib/GObject C project
- When adding tests for an existing module or class
- When the user says "write tests", "add a test", or "scaffold test file"
- When creating a test harness for interfaces, signals, or properties

## Instructions

### 1. Gather Requirements

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Module under test** | Yes | — | What is being tested (e.g., `BaconParser`, `LcMessage`) |
| **Test type** | No | `simple` | `simple` (functions), `fixture` (setup/teardown), `gobject` (type testing) |
| **Project** | Yes | — | Which project (determines include paths, library linking) |
| **Test cases** | No | infer | Specific scenarios to test |

### 2. File Structure

Test files live in `tests/` at the project root. File naming: `test-{module-name}.c` (kebab-case).

```
project/
  src/
    core/
      my-type.c
      my-type.h
  tests/
    test-my-type.c    <-- new test file
  Makefile
```

### 3. Generate Simple Test File (No Fixtures)

For testing pure functions, enums, boxed types, and stateless operations:

```c
#include <glib.h>
#include <glib-object.h>
#include <string.h>

/* Project includes - adjust based on project structure */
#define BACON_COMPILATION
#include "../src/core/bacon-parser.h"

/* ================================================================
 * Test: /parser/tokenize-simple
 * ================================================================ */

static void
test_parser_tokenize_simple(void)
{
	BaconParser *parser;
	GPtrArray *tokens;

	parser = bacon_parser_new();
	g_assert_nonnull(parser);

	tokens = bacon_parser_tokenize(parser, "echo hello world");
	g_assert_nonnull(tokens);
	g_assert_cmpuint(tokens->len, ==, 3);
	g_assert_cmpstr(g_ptr_array_index(tokens, 0), ==, "echo");
	g_assert_cmpstr(g_ptr_array_index(tokens, 1), ==, "hello");
	g_assert_cmpstr(g_ptr_array_index(tokens, 2), ==, "world");

	g_ptr_array_unref(tokens);
	g_object_unref(parser);
}

/* ================================================================
 * Test: /parser/tokenize-empty
 * ================================================================ */

static void
test_parser_tokenize_empty(void)
{
	BaconParser *parser;
	GPtrArray *tokens;

	parser = bacon_parser_new();
	tokens = bacon_parser_tokenize(parser, "");
	g_assert_nonnull(tokens);
	g_assert_cmpuint(tokens->len, ==, 0);

	g_ptr_array_unref(tokens);
	g_object_unref(parser);
}

/* ================================================================
 * main
 * ================================================================ */

int
main(int argc, char *argv[])
{
	g_test_init(&argc, &argv, NULL);

	g_test_add_func("/parser/tokenize-simple", test_parser_tokenize_simple);
	g_test_add_func("/parser/tokenize-empty", test_parser_tokenize_empty);

	return g_test_run();
}
```

### 4. Generate Fixture-Based Test File

For tests that need shared setup/teardown (temporary files, database connections, complex state):

```c
#include <glib.h>
#include <glib-object.h>
#include <glib/gstdio.h>
#include <string.h>
#include <unistd.h>

#define BACON_COMPILATION
#include "../src/core/bacon-shell.h"
#include "../src/core/bacon-environment.h"

/* ================================================================
 * Fixture
 * ================================================================ */

static gchar *_original_dir = NULL;
static gchar *_tmpdir = NULL;

static void
setup_test_env(void)
{
	gchar *subdir;

	_original_dir = g_get_current_dir();
	_tmpdir = g_dir_make_tmp("bacon-test-XXXXXX", NULL);
	g_assert_nonnull(_tmpdir);

	/* Create directory structure for tests */
	subdir = g_build_filename(_tmpdir, "projects", NULL);
	g_mkdir_with_parents(subdir, 0755);
	g_free(subdir);
}

static void
teardown_test_env(void)
{
	gchar *cmd;

	if (_original_dir != NULL) {
		chdir(_original_dir);
		g_free(_original_dir);
		_original_dir = NULL;
	}
	if (_tmpdir != NULL) {
		cmd = g_strdup_printf("rm -rf '%s'", _tmpdir);
		system(cmd);
		g_free(cmd);
		g_free(_tmpdir);
		_tmpdir = NULL;
	}
}

/* ================================================================
 * Tests using fixture
 * ================================================================ */

static void
test_shell_working_directory(void)
{
	BaconShell *shell;

	setup_test_env();

	shell = bacon_shell_new(BACON_FLAG_NONE);
	g_assert_nonnull(shell);

	/* ... test with temporary directory ... */

	g_object_unref(shell);
	teardown_test_env();
}

int
main(int argc, char *argv[])
{
	g_test_init(&argc, &argv, NULL);

	g_test_add_func("/shell/working-directory", test_shell_working_directory);

	return g_test_run();
}
```

### 5. Generate GObject Testing Patterns

#### Testing GObject Properties

```c
static void
test_shell_properties(void)
{
	BaconShell *shell;
	gchar *name;
	gint count;

	shell = bacon_shell_new();
	g_assert_nonnull(shell);

	/* Test default values */
	g_object_get(shell, "name", &name, "count", &count, NULL);
	g_assert_null(name);
	g_assert_cmpint(count, ==, 0);

	/* Test setters */
	g_object_set(shell, "name", "test-shell", "count", 42, NULL);

	g_object_get(shell, "name", &name, "count", &count, NULL);
	g_assert_cmpstr(name, ==, "test-shell");
	g_assert_cmpint(count, ==, 42);

	g_free(name);
	g_object_unref(shell);
}
```

#### Testing GObject Signals

```c
typedef struct {
	gboolean received;
	gchar *last_value;
} SignalData;

static void
on_activated(GObject *obj, gpointer user_data)
{
	SignalData *data;

	(void)obj;
	data = (SignalData *)user_data;
	data->received = TRUE;
}

static void
test_shell_activated_signal(void)
{
	BaconShell *shell;
	SignalData data = { FALSE, NULL };
	gulong handler_id;

	shell = bacon_shell_new();
	handler_id = g_signal_connect(shell, "activated",
	                              G_CALLBACK(on_activated), &data);

	g_assert_false(data.received);

	g_signal_emit_by_name(shell, "activated");
	g_assert_true(data.received);

	g_signal_handler_disconnect(shell, handler_id);
	g_object_unref(shell);
}
```

#### Testing GEnum / GFlags Types

```c
static void
test_channel_state_type(void)
{
	GType type;
	GEnumClass *klass;
	GEnumValue *val;

	type = LC_TYPE_CHANNEL_STATE;
	g_assert_true(type != G_TYPE_INVALID);
	g_assert_true(G_TYPE_IS_ENUM(type));

	klass = g_type_class_ref(type);
	g_assert_nonnull(klass);

	val = g_enum_get_value(klass, LC_CHANNEL_STATE_CONNECTED);
	g_assert_nonnull(val);
	g_assert_cmpstr(val->value_nick, ==, "connected");

	g_type_class_unref(klass);
}
```

#### Testing Boxed Types

```c
static void
test_message_copy(void)
{
	LcInboundMessage *orig;
	LcInboundMessage *copy;

	orig = lc_inbound_message_new("matrix", "@alice:ex.com",
	                               "Alice", "!room:ex.com",
	                               NULL, "hello", 1700000000);
	g_assert_nonnull(orig);

	copy = lc_inbound_message_copy(orig);
	g_assert_nonnull(copy);
	g_assert_true(orig != copy);

	g_assert_cmpstr(lc_inbound_message_get_body(copy), ==, "hello");
	g_assert_cmpstr(lc_inbound_message_get_sender_id(copy), ==, "@alice:ex.com");

	lc_inbound_message_free(orig);
	lc_inbound_message_free(copy);
}
```

#### Testing Interface Implementations

Define minimal test GObjects that implement the interface:

```c
/* Define a test type that implements the interface */
typedef struct {
	GObject parent_instance;
	gboolean was_called;
} TestExecutable;

typedef struct {
	GObjectClass parent_class;
} TestExecutableClass;

static GType test_executable_get_type(void);

static gint
test_exec_execute(BaconExecutable *self, gint argc, gchar **argv, GError **error)
{
	TestExecutable *te;

	(void)argc;
	(void)argv;
	(void)error;

	te = (TestExecutable *)self;
	te->was_called = TRUE;
	return 0;
}

static const gchar *
test_exec_get_name(BaconExecutable *self)
{
	(void)self;
	return "test-exec";
}

static const gchar *
test_exec_get_description(BaconExecutable *self)
{
	(void)self;
	return "Test executable";
}

static void
test_exec_iface_init(BaconExecutableInterface *iface)
{
	iface->execute         = test_exec_execute;
	iface->get_name        = test_exec_get_name;
	iface->get_description = test_exec_get_description;
}

static void test_executable_class_init(TestExecutableClass *klass) { (void)klass; }
static void test_executable_init(TestExecutable *self) { self->was_called = FALSE; }

G_DEFINE_TYPE_WITH_CODE(TestExecutable, test_executable, G_TYPE_OBJECT,
    G_IMPLEMENT_INTERFACE(BACON_TYPE_EXECUTABLE, test_exec_iface_init))

/* Now test it */
static void
test_executable_interface(void)
{
	TestExecutable *te;
	gint ret;

	te = g_object_new(test_executable_get_type(), NULL);
	g_assert_true(BACON_IS_EXECUTABLE(te));
	g_assert_false(te->was_called);

	ret = bacon_executable_execute(BACON_EXECUTABLE(te), 0, NULL, NULL);
	g_assert_cmpint(ret, ==, 0);
	g_assert_true(te->was_called);
	g_assert_cmpstr(bacon_executable_get_name(BACON_EXECUTABLE(te)), ==, "test-exec");

	g_object_unref(te);
}
```

### 6. Advanced Patterns

#### Testing GError Handling

```c
static void
test_database_double_open_fails(void)
{
	LcDatabase *db;
	GError *error = NULL;
	gboolean ok;

	db = create_test_db();  /* helper, opens :memory: */

	ok = lc_database_open(db, ":memory:", &error);
	g_assert_false(ok);
	g_assert_nonnull(error);
	g_error_free(error);

	g_object_unref(db);
}
```

#### Conditional Test Skipping

```c
static void
test_compiler_new(void)
{
	GstConfigCompiler *compiler;
	GError *error = NULL;

	if (g_find_program_in_path("gcc") == NULL) {
		g_test_skip("gcc not found in PATH");
		return;
	}

	compiler = gst_config_compiler_new(&error);
	g_assert_no_error(error);
	g_assert_nonnull(compiler);

	g_object_unref(compiler);
}
```

#### Testing Expected Warnings

```c
static void
test_module_register_duplicate(void)
{
	GstModuleManager *mgr;
	GstModule *mod1;
	GstModule *mod2;

	mgr = gst_module_manager_new();
	mod1 = g_object_new(TEST_TYPE_MODULE, NULL);
	mod2 = g_object_new(TEST_TYPE_MODULE, NULL);

	g_assert_true(gst_module_manager_register(mgr, mod1));

	g_test_expect_message(NULL, G_LOG_LEVEL_WARNING, "*already registered*");
	g_assert_false(gst_module_manager_register(mgr, mod2));
	g_test_assert_expected_messages();

	g_object_unref(mod1);
	g_object_unref(mod2);
	g_object_unref(mgr);
}
```

#### Temporary File Helper

```c
static gchar *
write_temp_file(const gchar *suffix,
                const gchar *content)
{
	gchar *tmpl;
	gchar *path;
	GError *error = NULL;
	gint fd;

	tmpl = g_strdup_printf("test-XXXXXX%s", suffix);
	fd = g_file_open_tmp(tmpl, &path, &error);
	g_free(tmpl);
	g_assert_no_error(error);
	g_assert_cmpint(fd, >=, 0);

	g_assert_true(g_file_set_contents(path, content, -1, &error));
	g_assert_no_error(error);
	close(fd);

	return path;
}
```

### 7. Makefile Integration

Add to the project's `Makefile`:

```makefile
# Test sources
TEST_SRCS := \
	tests/test-parser.c \
	tests/test-shell.c \
	tests/test-my-type.c

TEST_BINS := $(patsubst tests/%.c,$(OUTDIR)/%,$(TEST_SRCS))

# Test compilation rule
$(OUTDIR)/test-%: $(OBJDIR)/tests/test-%.o $(OUTDIR)/$(LIB_SHARED_FULL)
	$(CC) -o $@ $< $(TEST_LDFLAGS)

# Test LDFLAGS
TEST_LDFLAGS := -L$(OUTDIR) -l$(LIB_NAME) $(LDFLAGS) -Wl,-rpath,$(OUTDIR)

# Run all tests
test: lib $(TEST_BINS)
	@echo "Running tests..."
	@failures=0; \
	for test in $(TEST_BINS); do \
		echo "  $$test"; \
		LD_LIBRARY_PATH=$(OUTDIR) $$test || failures=$$((failures + 1)); \
	done; \
	if [ $$failures -gt 0 ]; then \
		echo "$$failures test suite(s) failed"; \
		exit 1; \
	fi

.PHONY: test
```

### 8. Test Path Conventions

Organize test paths hierarchically:

```
/{module}/{operation}             — /parser/tokenize-simple
/{module}/{submodule}/{test}      — /message/inbound/new
/{module}/{feature}-{variant}     — /shell/cdpath-basic
/{type}/{test-description}        — /enums/channel-state
```

### 9. Assertion Quick Reference

| Assertion | Use For |
|-----------|---------|
| `g_assert_true(expr)` | Boolean conditions |
| `g_assert_false(expr)` | Negative conditions |
| `g_assert_null(ptr)` | Pointer is NULL |
| `g_assert_nonnull(ptr)` | Pointer is non-NULL |
| `g_assert_cmpint(a, op, b)` | Integer comparison (==, !=, <, >, <=, >=) |
| `g_assert_cmpuint(a, op, b)` | Unsigned integer comparison |
| `g_assert_cmpstr(a, op, b)` | String comparison |
| `g_assert_cmpfloat(a, op, b)` | Float comparison |
| `g_assert_no_error(error)` | GError is NULL |
| `g_test_skip(reason)` | Skip test with message |
| `g_test_expect_message(domain, level, pattern)` | Expect log message |
| `g_test_assert_expected_messages()` | Verify expected messages |

## Output Format

1. `tests/test-{module}.c` — Complete test source file
2. Additions to `Makefile` — New test source in `TEST_SRCS` list

## Examples

**Input:** "Create tests for BaconEnvironment covering set, get, unset, and export"

**Output:** `tests/test-environment.c` with:
- `test_environment_set_get` — set a variable, verify get returns it
- `test_environment_unset` — set then unset, verify get returns NULL
- `test_environment_export` — export a variable, verify it appears in exported list
- `test_environment_overwrite` — set same variable twice, verify latest value
- `test_environment_null_handling` — verify NULL key/value handling
- Proper main() with `g_test_init` and `g_test_run`

## Constraints

- Never generate code that uses `//` comments
- Never use C99 variable declarations mid-block
- Always clean up GObject instances with `g_object_unref`
- Always clean up boxed types with their `_free` function
- Always free GError with `g_error_free` after checking
- Always clean up temporary files and directories
- Never leave dangling pointers or leaked memory in tests
