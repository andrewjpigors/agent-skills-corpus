---
name: skill-port-to-crispy
description: >
  Port Python scripts to crispy C scripts using GLib/GObject conventions.
  Trigger when asked to port, convert, rewrite, or translate Python to C,
  when creating new crispy C scripts, or when the user mentions "crispy",
  "C script", "port to C", or "GLib C script". Also trigger when refactoring
  existing crispy C files.
---

# Skill: Port to Crispy

Port Python scripts to single-file crispy C scripts using GLib/GObject conventions. Crispy compiles and caches `.c` files on the fly — scripts execute like Python but run as native C. This skill covers the complete translation from Python idioms to GLib equivalents, including type mapping, pattern mapping, memory management, and common gotchas. Derived from porting 10,000+ line Python CLI tools to crispy C.

## When to Use

- Asked to port, convert, rewrite, or translate a Python script to C
- Creating a new crispy C script from scratch
- The user mentions "crispy", "C script", "port to C", or "GLib C script"
- Refactoring or extending an existing crispy C file

## Prerequisites

- `crispy` installed and on `$PATH`
- `gcc` compiler
- `pkg-config`
- GLib 2.0 development headers (`glib2-devel` or equivalent)
- Development headers for any additional libraries the script needs (json-glib, libsoup, etc.)

## Instructions

Consult the **Reference** section below for specific translation patterns at each step.

1. **Read the entire Python source.** Identify all imports, dependencies, and external tools used.
2. **Map each Python import to a C library.** Build the `CRISPY_PARAMS` define using `pkg-config` names from the library table in the Reference section.
3. **Write the shebang, params, license header, and includes.**
4. **Port all constants.** Convert Python constants to `#define` and `static const` values. Convert constant lists to sentinel-terminated string arrays.
5. **Port all enum types.** Create `typedef enum` with `_from_string()` converter functions.
6. **Port all `@dataclass` classes to structs** with `_free()` + `G_DEFINE_AUTOPTR_CLEANUP_FUNC`.
7. **Port utility/helper functions** — string manipulation, file I/O, parsing. Use the pattern mapping tables.
8. **Port core logic functions**, converting Python idioms per the type and pattern mapping tables.
9. **Port each command handler**, adding `GOptionContext` + `GOptionEntry` argument parsing.
10. **Build the dispatch table** (sentinel-terminated).
11. **Write `main()`** with two-pass argument parsing (global flags first, then subcommand).
12. **Review every allocation** — ensure each has a free path via `g_autoptr`, `g_autofree`, or explicit `g_free()`.
13. **Create the bash wrapper script** (no file extension) that `exec`s the `.c` file.
14. **Test:** `crispy path/to/script.c --help` — verify it compiles and runs.

## Reference

### What is Crispy

Crispy is a C script runner. It reads a `CRISPY_PARAMS` define from the source, compiles with `gcc`, caches the binary by content hash, and executes it. Scripts use `#!/usr/bin/env crispy` as their shebang. A thin bash wrapper (no extension) delegates to the `.c` file:

```bash
#!/bin/bash
exec "$(dirname "$(realpath "$0")")/my_tool.c" "$@"
```

Scripts are **single-file, self-contained** — no separate headers or compilation units. All code lives in one `.c` file.

Every crispy script starts with exactly this pattern:

```c
#!/usr/bin/env crispy
#define CRISPY_PARAMS "$(pkg-config --cflags --libs glib-2.0 json-glib-1.0) -Wno-unused-function"
```

`CRISPY_PARAMS` supports shell expansion. Common libraries and their pkg-config names:

| Library | pkg-config | Purpose |
|---------|-----------|---------|
| glib-2.0 | `glib-2.0` | Core (always included by crispy) |
| json-glib | `json-glib-1.0` | JSON parsing/building |
| yaml-glib | `yaml-glib-1.0` | YAML frontmatter |
| libsoup 3 | `libsoup-3.0` | HTTP server/client |
| mcp-glib | `mcp-glib-1.0` | MCP server |
| ncurses | `ncursesw` | TUI rendering |

### File Structure (Section Order)

Every crispy C file follows this exact section order:

1. `#!/usr/bin/env crispy` + `CRISPY_PARAMS`
2. License/copyright comment block
3. `#include` directives (library headers, then glib, then stdlib)
4. Section separator: `/* === Constants === */`
5. `static const` values and `#define` constants
6. Sentinel-terminated string arrays (`static const gchar *ITEMS[] = { ..., NULL }`)
7. Registry structs and static registry arrays (sentinel-terminated)
8. Enums with `_from_string()` converter functions
9. Forward declarations: `typedef struct _FooBar FooBar;`
10. Struct definitions with doc comments
11. Cleanup functions + `G_DEFINE_AUTOPTR_CLEANUP_FUNC`
12. Static globals (e.g., `static gboolean g_no_color = FALSE;`)
13. Utility/helper functions (prefixed with `_`)
14. Core implementation functions
15. Subcommand handler functions
16. Dispatch table (sentinel-terminated)
17. Usage printer
18. `main()` with two-pass argument parsing

### Code Style

- Standard: `gnu89` exclusively, compiled with `gcc`
- Indentation: TAB characters (4-space width)
- Comments: `/* comment */` only — never `//`
- Naming: defines `UPPERCASE_SNAKE_CASE`, structs `PrefixPascalCase`, variables/functions `lowercase_snake_case`, static helpers `_underscore_prefix`
- Defines use parentheses: `#define EXIT_CODE (1)`
- All functions must have GObject Introspection compatible doc comments
- Function signatures — return type on its own line, aligned parameters:

```c
static gchar *
my_item_get_title (MyItem   *item,
                   gboolean  with_id)
{
	/* implementation */
}
```

### Type Mapping

| Python | C (GLib) | Allocation | Free |
|--------|----------|------------|------|
| `str` | `gchar *` | `g_strdup()` | `g_free()` |
| `int` | `gint` | stack | — |
| `bool` | `gboolean` | stack (`TRUE`/`FALSE`) | — |
| `float` | `gdouble` | stack | — |
| `None` | `NULL` | — | — |
| `Optional[T]` | `T *` | check for `NULL` | same as `T` |
| `list[T]` | `GPtrArray *` | `g_ptr_array_new_with_free_func()` | `g_ptr_array_unref()` |
| `list[str]` | `GStrv` (`gchar **`) | `g_strdupv()` | `g_strfreev()` |
| `dict[K,V]` | `GHashTable *` | `g_hash_table_new_full()` | `g_hash_table_destroy()` |
| `datetime` | `GDateTime *` | `g_date_time_new_*()` | `g_date_time_unref()` |
| `date` | `GDate *` | `g_date_new()` | `g_date_free()` |
| `Enum` | `typedef enum { ... } Name;` | stack | — |
| `@dataclass` | struct + `_free()` + `G_DEFINE_AUTOPTR_CLEANUP_FUNC` | `g_new0()` | custom `_free()` |

### Pattern Mapping

#### Strings

| Python | C (GLib) |
|--------|----------|
| `f"text {var}"` | `g_strdup_printf ("text %s", var)` |
| `s.startswith("x")` | `g_str_has_prefix (s, "x")` |
| `s.endswith("x")` | `g_str_has_suffix (s, "x")` |
| `s.strip()` | `g_strstrip (g_strdup (s))` |
| `s.split(",")` | `g_strsplit (s, ",", -1)` → free with `g_strfreev()` |
| `",".join(lst)` | `g_strjoinv (",", strv)` |
| `s.lower()` | `g_ascii_strdown (s, -1)` |
| `s.upper()` | `g_ascii_strup (s, -1)` |
| `s.replace(a, b)` | `g_regex_replace_literal()` or manual |
| `"x" in s` | `strstr (s, "x") != NULL` |
| `s == other` | `g_strcmp0 (s, other) == 0` |
| `re.match(pat, s)` | `g_regex_new(); g_regex_match()` |
| string builder | `GString *buf = g_string_new (""); g_string_append_printf (buf, ...); g_string_free (buf, FALSE);` |

#### Collections

```c
/* GPtrArray (Python list) */
GPtrArray *arr = g_ptr_array_new_with_free_func ((GDestroyNotify) item_free);
g_ptr_array_add (arr, item);                        /* list.append() */
MyType *t = g_ptr_array_index (arr, i);              /* list[i] */
for (i = 0; i < arr->len; i++) { ... }              /* for x in list */
g_ptr_array_sort (arr, (GCompareFunc) cmp_func);     /* sorted() */
g_ptr_array_unref (arr);                             /* cleanup */

/* GHashTable (Python dict) */
GHashTable *ht = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, g_free);
g_hash_table_insert (ht, g_strdup (key), g_strdup (val));  /* dict[k] = v */
gchar *v = g_hash_table_lookup (ht, key);                  /* dict.get(k) */
gboolean has = g_hash_table_contains (ht, key);             /* k in dict */
g_hash_table_destroy (ht);                                  /* cleanup */

/* Sentinel-terminated arrays (Python tuple/frozen list of constants) */
static const gchar *ITEMS[] = { "a", "b", "c", NULL };
for (i = 0; ITEMS[i] != NULL; i++) { ... }
```

#### File I/O

| Python | C (GLib) |
|--------|----------|
| `open(p).read()` | `g_file_get_contents (p, &data, &len, &err)` |
| `open(p,'w').write(d)` | `g_file_set_contents (p, d, -1, &err)` |
| `Path(a) / b` | `g_build_filename (a, b, NULL)` |
| `p.parent` | `g_path_get_dirname (p)` |
| `p.name` | `g_path_get_basename (p)` |
| `p.exists()` | `g_file_test (p, G_FILE_TEST_EXISTS)` |
| `p.is_dir()` | `g_file_test (p, G_FILE_TEST_IS_DIR)` |
| `os.listdir()` | `GDir *d = g_dir_open(); while ((name = g_dir_read_name(d))) { ... }` |
| `os.makedirs()` | `g_mkdir_with_parents (path, 0755)` |

#### Error Handling

Python `try/except` becomes C return-value checking with `GError`:

```c
/* Python: raise ValueError("bad input") */
g_set_error (error, G_IO_ERROR, G_IO_ERROR_INVALID_DATA, "bad input");
return NULL;

/* Python: try: ... except: ... */
g_autoptr(GError) err = NULL;
if (!g_file_get_contents (path, &data, NULL, &err))
{
	g_printerr ("Error: %s\n", err->message);
	return EXIT_GENERAL_ERROR;
}

/* Python: print(msg, file=sys.stderr) */
g_printerr ("Error: %s\n", msg);

/* Python: print(msg) */
g_print ("%s\n", msg);
```

#### Argument Parsing

Python `argparse` → GLib `GOptionContext` with two-pass parsing for subcommands:

```c
/* 1. Define entries (sentinel-terminated) */
GOptionEntry entries[] = {
	{ "verbose", 'v', 0, G_OPTION_ARG_NONE, &verbose, "Verbose output", NULL },
	{ "output",  'o', 0, G_OPTION_ARG_STRING, &output, "Output file", "FILE" },
	{ NULL }
};

/* 2. Find command index (first non-flag arg) */
cmd_idx = find_command_index (argc, argv);

/* 3. Copy only global args for parsing */
gint global_argc = cmd_idx > 0 ? cmd_idx : argc;
gchar **global_argv = g_new0 (gchar *, global_argc + 1);
for (i = 0; i < global_argc; i++)
	global_argv[i] = g_strdup (argv[i]);

/* 4. Parse global args */
context = g_option_context_new ("<command> [options]");
g_option_context_add_main_entries (context, entries, NULL);
g_option_context_set_ignore_unknown_options (context, TRUE);
g_option_context_parse (context, &global_argc, &global_argv, &error);
g_strfreev (global_argv);

/* 5. Dispatch: cmd_argv = argv + cmd_idx */
```

#### JSON (json-glib)

```c
/* Python: json.dumps(data) -> C: JsonBuilder */
JsonBuilder *b = json_builder_new ();
json_builder_begin_object (b);
json_builder_set_member_name (b, "id");
json_builder_add_string_value (b, item->id);
json_builder_set_member_name (b, "count");
json_builder_add_int_value (b, 42);
json_builder_end_object (b);

JsonGenerator *gen = json_generator_new ();
json_generator_set_root (gen, json_builder_get_root (b));
json_generator_set_pretty (gen, TRUE);
g_autofree gchar *json_str = json_generator_to_data (gen, NULL);
g_object_unref (gen);
g_object_unref (b);

/* Python: json.loads(text) -> C: JsonParser */
JsonParser *parser = json_parser_new ();
json_parser_load_from_data (parser, text, -1, &error);
JsonObject *obj = json_node_get_object (json_parser_get_root (parser));
const gchar *id = json_object_get_string_member (obj, "id");
gint64 count = json_object_get_int_member (obj, "count");
g_object_unref (parser);
```

#### YAML (yaml-glib)

```c
/* Python: yaml.safe_load(text) */
YamlParser *parser = yaml_parser_new ();
yaml_parser_load_from_data (parser, yaml_str, -1, &error);
YamlNode *root = yaml_parser_get_root (parser);
YamlMapping *mapping = yaml_node_get_mapping (root);
const gchar *val = yaml_mapping_get_string_member (mapping, "key");

/* Python: yaml.dump(data) -- manual string building */
GString *buf = g_string_new ("---\n");
g_string_append_printf (buf, "id: %s\n", id);
g_string_append_printf (buf, "status: %s\n", status);
g_string_append (buf, "---\n");
```

#### HTTP Server (libsoup)

```c
/* Python: @app.route('/api/items', methods=['GET']) */
soup_server_add_handler (server, "/api/items", handle_get_items, app, NULL);

/* Handler signature */
static void
handle_get_items (SoupServer        *server,
                  SoupServerMessage *msg,
                  const gchar       *path,
                  GHashTable        *query,
                  gpointer           user_data)
{
	MyApp *app = (MyApp *) user_data;

	/* Build JSON response */
	g_autofree gchar *json = build_json_response (app);
	SoupMessageHeaders *hdrs = soup_server_message_get_response_headers (msg);
	soup_message_headers_replace (hdrs, "Content-Type", "application/json");
	SoupMessageBody *body = soup_server_message_get_response_body (msg);
	soup_message_body_append (body, SOUP_MEMORY_COPY, json, strlen (json));
	soup_server_message_set_status (msg, 200, NULL);
}
```

#### Subprocess

```c
/* Python: subprocess.run(["cmd", "arg"], capture_output=True, text=True) */
gchar *argv[] = { "cmd", "arg", NULL };
gchar *out = NULL, *err = NULL;
gint rc = 0;
g_spawn_sync (NULL, argv, NULL, G_SPAWN_SEARCH_PATH,
              NULL, NULL, &out, &err, &rc, &error);
```

#### Async / Event Loop

```c
/* Python: asyncio event loop -> GMainLoop */
GMainLoop *loop = g_main_loop_new (NULL, FALSE);
g_timeout_add (100, tick_callback, user_data);           /* periodic */
g_timeout_add_seconds (30, refresh_callback, user_data); /* periodic (sec) */

/* GIOChannel for stdin input (TUI key handling) */
GIOChannel *stdin_ch = g_io_channel_unix_new (STDIN_FILENO);
g_io_add_watch (stdin_ch, G_IO_IN, stdin_callback, user_data);

g_main_loop_run (loop);
```

#### Color Output

```c
static gboolean g_no_color = FALSE;

static gchar *
_c (const gchar *code, const gchar *text)
{
	if (g_no_color)
		return g_strdup (text);
	return g_strdup_printf ("\033[%sm%s\033[0m", code, text);
}

#define _red(t)    _c ("31", t)
#define _green(t)  _c ("32", t)
#define _yellow(t) _c ("33", t)
#define _cyan(t)   _c ("36", t)
#define _bold(t)   _c ("1", t)

/* Usage -- note: returns allocated string, use g_autofree */
g_autofree gchar *label = _red ("Error");
g_printerr ("%s: %s\n", label, msg);
```

### Memory Management

#### Rules

1. Every `g_new0()` / `g_strdup()` / `g_strdup_printf()` must have a free path
2. Use `g_autoptr(Type)` for automatic scope cleanup wherever possible
3. Use `g_autofree gchar *` for strings freed at scope exit
4. Use `g_steal_pointer(&var)` to transfer ownership out of an autoptr
5. Every struct needs a `_free()` function that checks `if (!ptr) return;` first
6. Every struct needs `G_DEFINE_AUTOPTR_CLEANUP_FUNC(Type, type_free)`
7. Use `g_clear_pointer()` for ref-counted types in free functions

#### Struct Lifecycle Pattern

```c
/* 1. Forward declare */
typedef struct _MyItem MyItem;

/* 2. Define */
struct _MyItem {
	gchar       *name;
	gint         count;
	GDateTime   *created;
	GPtrArray   *children;    /* element-type: MyItem* */
};

/* 3. Free function -- NULL-safe, frees every member */
static void
my_item_free (MyItem *item)
{
	if (!item) return;
	g_free (item->name);
	g_clear_pointer (&item->created, g_date_time_unref);
	g_clear_pointer (&item->children, g_ptr_array_unref);
	g_free (item);
}

/* 4. Enable g_autoptr */
G_DEFINE_AUTOPTR_CLEANUP_FUNC (MyItem, my_item_free)

/* 5. Usage */
g_autoptr(MyItem) item = g_new0 (MyItem, 1);
item->name = g_strdup ("example");
item->count = 5;
item->created = g_date_time_new_now_utc ();
item->children = g_ptr_array_new_with_free_func ((GDestroyNotify) my_item_free);
```

#### Cleanup Reference

| Type | Free Function |
|------|---------------|
| `gchar *` | `g_free()` or `g_autofree` |
| `gchar **` (GStrv) | `g_strfreev()` |
| `GPtrArray *` | `g_ptr_array_unref()` |
| `GHashTable *` | `g_hash_table_destroy()` |
| `GDateTime *` | `g_date_time_unref()` |
| `GDate *` | `g_date_free()` |
| `GString *` | `g_string_free (s, TRUE)` (or `FALSE` to keep chars) |
| `GRegex *` | `g_regex_unref()` |
| `GMatchInfo *` | `g_match_info_free()` |
| `GError *` | `g_error_free()` or `g_autoptr` |
| `GOptionContext *` | `g_option_context_free()` or `g_autoptr` |
| `JsonBuilder *` | `g_object_unref()` |
| `JsonParser *` | `g_object_unref()` |
| `JsonGenerator *` | `g_object_unref()` |

### Reusable Patterns

#### Subcommand Dispatch Table

```c
/* Function pointer type for command handlers */
typedef gint (*CmdFunc) (gint argc, gchar **argv, GlobalOpts *g, Config *c);

/* Dispatch table entry */
typedef struct {
	const gchar *name;
	const gchar *help;
	CmdFunc      handler;
} Subcommand;

/* Sentinel-terminated dispatch table */
static const Subcommand SUBCOMMANDS[] = {
	{ "init",   "Initialize project",  cmd_init },
	{ "list",   "List items",          cmd_list },
	{ "show",   "Show item details",   cmd_show },
	{ NULL, NULL, NULL }
};

/* Lookup in main() */
for (i = 0; SUBCOMMANDS[i].name != NULL; i++)
{
	if (g_strcmp0 (SUBCOMMANDS[i].name, cmd_name) == 0)
		return SUBCOMMANDS[i].handler (cmd_argc, cmd_argv, global, config);
}
```

#### Registry / Lookup Pattern

Python dicts of static config become sentinel-terminated struct arrays:

```c
/* Python:
 * PREFIXES = {"task": "PROJ", "bug": "BUG", "research": "RESEARCH"}
 */
typedef struct {
	const gchar *type;
	const gchar *prefix;
} TypePrefixEntry;

static const TypePrefixEntry PREFIXES[] = {
	{ "task",      "PROJ" },
	{ "bug",       "BUG" },
	{ "research",  "RESEARCH" },
	{ NULL, NULL }   /* sentinel */
};

static const gchar *
get_prefix_for_type (const gchar *type)
{
	gint i;
	for (i = 0; PREFIXES[i].type != NULL; i++)
	{
		if (g_strcmp0 (PREFIXES[i].type, type) == 0)
			return PREFIXES[i].prefix;
	}
	return NULL;
}
```

### Common Gotchas

1. **Missing sentinel**: Every `const gchar *[]`, `GOptionEntry[]`, and registry array MUST end with `{ NULL }`. Forgetting this causes segfaults.
2. **String comparison with `==`**: Always use `g_strcmp0()` — it handles NULL safely. Never compare strings with `==`.
3. **Ownership on insert**: `g_hash_table_insert()` takes ownership per the destroy functions passed to `_new_full()`. Always `g_strdup()` keys/values if the hash table frees them.
4. **`g_autoptr` scope**: The variable is freed at the end of the enclosing `{ }` block. Use `g_steal_pointer()` to keep it alive past that scope.
5. **`GOptionContext` mutates argv**: After `g_option_context_parse()`, `argc`/`argv` are modified (parsed args removed). Copy them first if you need the originals.
6. **`g_strdup_printf` allocates**: The return value is heap-allocated. Always assign to `g_autofree gchar *` or explicitly `g_free()`.
7. **`GString` free modes**: `g_string_free (buf, FALSE)` returns the `char *` data (caller owns). `g_string_free (buf, TRUE)` frees everything.
8. **Sort comparators**: `g_ptr_array_sort()` passes pointers-to-pointers. Dereference twice: `const Foo *a = *(const Foo **) pa;`
9. **Static literals vs allocated strings**: Registry entries use `const gchar *` (string literals, never freed). Dynamic data uses `gchar *` (must be freed). Don't `g_free()` a string literal.
10. **`g_clear_pointer` in free functions**: Use for ref-counted members (GDateTime, GPtrArray, GHashTable). It NULLs the pointer after freeing, preventing double-free.
11. **Forgetting `g_strfreev`**: After `g_strsplit()`, always free the result array with `g_strfreev()` — not `g_free()`.
12. **GLib integer types**: Use `gint`, `guint`, `gint64`, `gboolean` — not `int`, `unsigned`, `long`, `bool`. Stay in the GLib type system.

## Output Format

The skill produces two files in the same directory:

- **`<tool_name>.c`** — single-file crispy C script with `#!/usr/bin/env crispy` shebang and `CRISPY_PARAMS` define. Contains all code (no separate headers).
- **`<tool_name>`** — bash wrapper script (no file extension) that `exec`s the `.c` file:
  ```bash
  #!/bin/bash
  exec "$(dirname "$(realpath "$0")")/<tool_name>.c" "$@"
  ```

## Examples

### Example: Porting a simple file-counting CLI

**Input:** A Python script that counts files in a directory by extension.

```python
#!/usr/bin/env python3
"""Count files in a directory grouped by extension."""

import sys
import os
from pathlib import Path
from collections import Counter


def count_by_extension(directory: str) -> dict[str, int]:
    counts: Counter = Counter()
    for entry in os.listdir(directory):
        p = Path(directory) / entry
        if p.is_file():
            ext = p.suffix if p.suffix else "(none)"
            counts[ext] += 1
    return dict(counts)


def main() -> int:
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <directory>", file=sys.stderr)
        return 1

    directory = sys.argv[1]
    if not os.path.isdir(directory):
        print(f"Error: {directory} is not a directory", file=sys.stderr)
        return 1

    counts = count_by_extension(directory)
    for ext, count in sorted(counts.items()):
        print(f"  {ext:12s} {count}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
```

**Result:** `ext_count.c`

```c
#!/usr/bin/env crispy
#define CRISPY_PARAMS "$(pkg-config --cflags --libs glib-2.0) -Wno-unused-function"

/*
 * ext_count.c — Count files in a directory grouped by extension.
 * License: AGPLv3
 */

#include <glib.h>

/* === Constants === */

#define EXIT_SUCCESS_CODE (0)
#define EXIT_USAGE_ERROR  (1)

/**
 * count_by_extension:
 * @directory: path to the directory to scan
 *
 * Counts files grouped by their extension. Files with no extension
 * are grouped under "(none)".
 *
 * Returns: (transfer full): a hash table mapping extension strings to counts
 */
static GHashTable *
count_by_extension (const gchar *directory)
{
	GHashTable *counts;
	GDir *dir;
	const gchar *name;
	g_autoptr(GError) err = NULL;

	counts = g_hash_table_new_full (g_str_hash, g_str_equal, g_free, NULL);

	dir = g_dir_open (directory, 0, &err);
	if (!dir)
	{
		g_printerr ("Error: %s\n", err->message);
		return counts;
	}

	while ((name = g_dir_read_name (dir)) != NULL)
	{
		g_autofree gchar *path = g_build_filename (directory, name, NULL);

		if (!g_file_test (path, G_FILE_TEST_IS_REGULAR))
			continue;

		/* Find extension */
		const gchar *dot = strrchr (name, '.');
		const gchar *ext = dot ? dot : "(none)";

		gpointer val = g_hash_table_lookup (counts, ext);
		gint count = GPOINTER_TO_INT (val) + 1;
		g_hash_table_insert (counts, g_strdup (ext), GINT_TO_POINTER (count));
	}

	g_dir_close (dir);
	return counts;
}

/**
 * print_counts:
 * @counts: hash table of extension -> count
 *
 * Prints each extension and its count, sorted alphabetically.
 */
static void
print_counts (GHashTable *counts)
{
	GPtrArray *keys;
	GHashTableIter iter;
	gpointer key, val;
	guint i;

	keys = g_ptr_array_new ();
	g_hash_table_iter_init (&iter, counts);
	while (g_hash_table_iter_next (&iter, &key, NULL))
		g_ptr_array_add (keys, key);

	g_ptr_array_sort (keys, (GCompareFunc) g_ascii_strcasecmp);

	for (i = 0; i < keys->len; i++)
	{
		const gchar *ext = g_ptr_array_index (keys, i);
		val = g_hash_table_lookup (counts, ext);
		g_print ("  %-12s %d\n", ext, GPOINTER_TO_INT (val));
	}

	g_ptr_array_free (keys, TRUE);
}

gint
main (gint   argc,
      gchar *argv[])
{
	const gchar *directory;
	GHashTable *counts;

	if (argc != 2)
	{
		g_printerr ("Usage: %s <directory>\n", argv[0]);
		return EXIT_USAGE_ERROR;
	}

	directory = argv[1];
	if (!g_file_test (directory, G_FILE_TEST_IS_DIR))
	{
		g_printerr ("Error: %s is not a directory\n", directory);
		return EXIT_USAGE_ERROR;
	}

	counts = count_by_extension (directory);
	print_counts (counts);
	g_hash_table_destroy (counts);

	return EXIT_SUCCESS_CODE;
}
```

And the bash wrapper `ext_count`:

```bash
#!/bin/bash
exec "$(dirname "$(realpath "$0")")/ext_count.c" "$@"
```

## Constraints

- Comments: `/* */` only — never `//`
- Standard: `gnu89` only — no C99/C11 features
- Types: GLib types only (`gint`, `gboolean`, `gint64`) — never raw `int`, `bool`, `long`
- Strings: `g_strcmp0()` for comparison — never `==`
- Memory: every allocation must have a free path via `g_autoptr`, `g_autofree`, or explicit `g_free()`
- Arrays: every sentinel-terminated array must end with `{ NULL }`
- Single file: all code lives in one `.c` file — no separate headers or compilation units
