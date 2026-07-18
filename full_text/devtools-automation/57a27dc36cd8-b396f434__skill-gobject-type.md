---
name: skill-gobject-type
description: >
  Generate complete GObject type boilerplate (.h + .c files) for final types,
  derivable types, and boxed types. Trigger when creating new GObject classes,
  GLib types, or C type system boilerplate.
---

# Skill: GObject Type Generator

Generates complete, production-quality GObject type boilerplate for header and source files. Supports final types (no subclassing), derivable types (abstract base classes), and boxed types (opaque structs without GObject overhead). All output follows gnu89 C, GCC-only conventions with `/* */` comments and TAB indentation.

## When to Use

- When creating a new GObject-based class (.h + .c pair)
- When adding a new type to an existing GLib/GObject project
- When the user says "create a new GObject type", "add a class", or "new type"
- When scaffolding a component that needs properties, signals, or private data

## Instructions

### 1. Gather Requirements

Ask the user (or infer from context):

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Project prefix** | Yes | — | Namespace prefix (e.g., `BACON`, `LC`, `GST`) |
| **Type name** | Yes | — | PascalCase name (e.g., `BaconShell`, `LcApp`) |
| **Parent type** | No | `GObject` | What it inherits from |
| **Type kind** | No | `final` | `final`, `derivable`, or `boxed` |
| **Properties** | No | none | List of GObject properties |
| **Signals** | No | none | List of GObject signals |
| **Interfaces** | No | none | Interfaces to implement |
| **Private fields** | No | none | Struct fields for private data |
| **Include guard style** | No | `#ifndef` | `#ifndef` or `#pragma once` |

### 2. Derive Naming

From the project prefix and type name, derive all identifiers:

```
Project prefix:  BACON
Type name:       BaconShell
lowercase:       bacon_shell
UPPERCASE:       BACON_SHELL
get_type:        bacon_shell_get_type
TYPE macro:      BACON_TYPE_SHELL
```

**Rules:**
- Prefix + Name must decompose cleanly: `BaconShell` -> `BACON` + `SHELL`
- Functions use `lowercase_snake_case` with project prefix: `bacon_shell_new()`
- Type macro: `{PREFIX}_TYPE_{NAME}` -> `BACON_TYPE_SHELL`
- File names: `{prefix}-{name}.h` and `{prefix}-{name}.c` (kebab-case)

### 3. Generate Header File

#### Final Type Header

```c
#ifndef BACON_SHELL_H
#define BACON_SHELL_H

#if !defined(BACON_INSIDE) && !defined(BACON_COMPILATION)
#error "Only <bacon.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define BACON_TYPE_SHELL (bacon_shell_get_type())

G_DECLARE_FINAL_TYPE(BaconShell, bacon_shell, BACON, SHELL, GObject)

/**
 * bacon_shell_new:
 *
 * Creates a new #BaconShell instance.
 *
 * Returns: (transfer full): a new #BaconShell
 */
BaconShell *
bacon_shell_new(void);

G_END_DECLS

#endif /* BACON_SHELL_H */
```

#### Derivable Type Header

For derivable types, the class struct is declared in the header with virtual methods and padding:

```c
#ifndef BACON_COMMAND_H
#define BACON_COMMAND_H

#if !defined(BACON_INSIDE) && !defined(BACON_COMPILATION)
#error "Only <bacon.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define BACON_TYPE_COMMAND (bacon_command_get_type())

G_DECLARE_DERIVABLE_TYPE(BaconCommand, bacon_command, BACON, COMMAND, GObject)

/**
 * BaconCommandClass:
 * @parent_class: the parent class
 * @run: execute the command
 * @get_name: return the command name
 * @padding: reserved for future virtual methods
 *
 * The virtual function table for #BaconCommand.
 */
struct _BaconCommandClass
{
	GObjectClass parent_class;

	/* virtual methods */
	gint          (*run)       (BaconCommand  *self,
	                            gint           argc,
	                            gchar        **argv,
	                            GError       **error);

	const gchar * (*get_name)  (BaconCommand  *self);

	/*< private >*/
	gpointer padding[8];
};

gint
bacon_command_run(BaconCommand  *self,
                  gint           argc,
                  gchar        **argv,
                  GError       **error);

const gchar *
bacon_command_get_name(BaconCommand *self);

G_END_DECLS

#endif /* BACON_COMMAND_H */
```

#### Boxed Type Header

For lightweight value types without GObject overhead:

```c
#ifndef LC_MESSAGE_H
#define LC_MESSAGE_H

#if !defined(LC_INSIDE) && !defined(LC_COMPILATION)
#error "Only <libreclaw.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define LC_TYPE_INBOUND_MESSAGE (lc_inbound_message_get_type())

GType lc_inbound_message_get_type(void) G_GNUC_CONST;

LcInboundMessage *
lc_inbound_message_new(const gchar *channel_id,
                       const gchar *sender_id,
                       const gchar *body);

LcInboundMessage *
lc_inbound_message_copy(const LcInboundMessage *msg);

void
lc_inbound_message_free(LcInboundMessage *msg);

const gchar *
lc_inbound_message_get_channel_id(const LcInboundMessage *msg);

const gchar *
lc_inbound_message_get_sender_id(const LcInboundMessage *msg);

const gchar *
lc_inbound_message_get_body(const LcInboundMessage *msg);

G_DEFINE_AUTOPTR_CLEANUP_FUNC(LcInboundMessage, lc_inbound_message_free)

G_END_DECLS

#endif /* LC_MESSAGE_H */
```

### 4. Generate Source File

#### Final Type Source (with properties and signals)

```c
#define BACON_COMPILATION
#include "bacon-shell.h"

/**
 * SECTION:bacon-shell
 * @title: BaconShell
 * @short_description: Top-level shell object
 *
 * #BaconShell is the central object...
 */

typedef struct _BaconShellPrivate BaconShellPrivate;

struct _BaconShellPrivate
{
	gchar    *name;
	gint      count;
	gboolean  active;
};

struct _BaconShell
{
	GObject parent_instance;
};

enum
{
	PROP_0,
	PROP_NAME,
	PROP_COUNT,
	N_PROPERTIES
};

static GParamSpec *properties[N_PROPERTIES];

enum
{
	SIGNAL_ACTIVATED,
	N_SIGNALS
};

static guint signals[N_SIGNALS];

G_DEFINE_FINAL_TYPE_WITH_PRIVATE(BaconShell, bacon_shell, G_TYPE_OBJECT)

static void
bacon_shell_get_property(GObject    *object,
                         guint       prop_id,
                         GValue     *value,
                         GParamSpec *pspec)
{
	BaconShellPrivate *priv;

	priv = bacon_shell_get_instance_private(BACON_SHELL(object));

	switch (prop_id) {
	case PROP_NAME:
		g_value_set_string(value, priv->name);
		break;
	case PROP_COUNT:
		g_value_set_int(value, priv->count);
		break;
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
		break;
	}
}

static void
bacon_shell_set_property(GObject      *object,
                         guint         prop_id,
                         const GValue *value,
                         GParamSpec   *pspec)
{
	BaconShellPrivate *priv;

	priv = bacon_shell_get_instance_private(BACON_SHELL(object));

	switch (prop_id) {
	case PROP_NAME:
		g_free(priv->name);
		priv->name = g_value_dup_string(value);
		break;
	case PROP_COUNT:
		priv->count = g_value_get_int(value);
		break;
	default:
		G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
		break;
	}
}

static void
bacon_shell_finalize(GObject *object)
{
	BaconShellPrivate *priv;

	priv = bacon_shell_get_instance_private(BACON_SHELL(object));

	g_free(priv->name);

	G_OBJECT_CLASS(bacon_shell_parent_class)->finalize(object);
}

static void
bacon_shell_class_init(BaconShellClass *klass)
{
	GObjectClass *object_class;

	object_class = G_OBJECT_CLASS(klass);
	object_class->get_property = bacon_shell_get_property;
	object_class->set_property = bacon_shell_set_property;
	object_class->finalize = bacon_shell_finalize;

	/**
	 * BaconShell:name:
	 *
	 * The display name of the shell.
	 */
	properties[PROP_NAME] =
		g_param_spec_string("name",
		                     "Name",
		                     "The display name",
		                     NULL,
		                     G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS);

	/**
	 * BaconShell:count:
	 *
	 * An example integer property.
	 */
	properties[PROP_COUNT] =
		g_param_spec_int("count",
		                  "Count",
		                  "An example count",
		                  G_MININT, G_MAXINT, 0,
		                  G_PARAM_READWRITE | G_PARAM_STATIC_STRINGS);

	g_object_class_install_properties(object_class, N_PROPERTIES, properties);

	/**
	 * BaconShell::activated:
	 * @self: the shell
	 *
	 * Emitted when the shell is activated.
	 */
	signals[SIGNAL_ACTIVATED] =
		g_signal_new("activated",
		              G_TYPE_FROM_CLASS(klass),
		              G_SIGNAL_RUN_LAST,
		              0, NULL, NULL, NULL,
		              G_TYPE_NONE, 0);
}

static void
bacon_shell_init(BaconShell *self)
{
	BaconShellPrivate *priv;

	priv = bacon_shell_get_instance_private(self);
	priv->name = NULL;
	priv->count = 0;
	priv->active = FALSE;
}

BaconShell *
bacon_shell_new(void)
{
	return g_object_new(BACON_TYPE_SHELL, NULL);
}
```

#### Final Type with Interface Implementation

When the type implements a GInterface, use `G_DEFINE_FINAL_TYPE_WITH_CODE`:

```c
static void bacon_echo_executable_iface_init(BaconExecutableInterface *iface);

G_DEFINE_FINAL_TYPE_WITH_CODE(BaconEchoCommand, bacon_echo_command,
    BACON_TYPE_COMMAND,
    G_IMPLEMENT_INTERFACE(BACON_TYPE_EXECUTABLE,
                          bacon_echo_executable_iface_init))
```

#### Derivable Type Source

```c
G_DEFINE_ABSTRACT_TYPE_WITH_CODE(BaconCommand, bacon_command, G_TYPE_OBJECT,
    G_IMPLEMENT_INTERFACE(BACON_TYPE_EXECUTABLE,
                          bacon_command_executable_iface_init))

static gint
bacon_command_real_run(BaconCommand  *self,
                      gint           argc,
                      gchar        **argv,
                      GError       **error)
{
	(void)self;
	(void)argc;
	(void)argv;
	(void)error;
	return 1;
}

static void
bacon_command_class_init(BaconCommandClass *klass)
{
	klass->run      = bacon_command_real_run;
	klass->get_name = bacon_command_real_get_name;
}

static void
bacon_command_init(BaconCommand *self)
{
	(void)self;
}

gint
bacon_command_run(BaconCommand  *self,
                 gint           argc,
                 gchar        **argv,
                 GError       **error)
{
	BaconCommandClass *klass;

	g_return_val_if_fail(BACON_IS_COMMAND(self), 1);
	g_return_val_if_fail(error == NULL || *error == NULL, 1);

	klass = BACON_COMMAND_GET_CLASS(self);
	g_return_val_if_fail(klass->run != NULL, 1);

	return klass->run(self, argc, argv, error);
}
```

#### Boxed Type Source

```c
struct _LcInboundMessage
{
	gchar  *channel_id;
	gchar  *sender_id;
	gchar  *body;
};

G_DEFINE_BOXED_TYPE(LcInboundMessage, lc_inbound_message,
                    lc_inbound_message_copy, lc_inbound_message_free)

LcInboundMessage *
lc_inbound_message_new(const gchar *channel_id,
                       const gchar *sender_id,
                       const gchar *body)
{
	LcInboundMessage *msg;

	g_return_val_if_fail(channel_id != NULL, NULL);
	g_return_val_if_fail(body != NULL, NULL);

	msg = g_new0(LcInboundMessage, 1);
	msg->channel_id = g_strdup(channel_id);
	msg->sender_id  = g_strdup(sender_id);
	msg->body       = g_strdup(body);

	return msg;
}

LcInboundMessage *
lc_inbound_message_copy(const LcInboundMessage *msg)
{
	g_return_val_if_fail(msg != NULL, NULL);
	return lc_inbound_message_new(msg->channel_id, msg->sender_id, msg->body);
}

void
lc_inbound_message_free(LcInboundMessage *msg)
{
	if (msg == NULL)
		return;
	g_free(msg->channel_id);
	g_free(msg->sender_id);
	g_free(msg->body);
	g_free(msg);
}
```

### 5. Code Style Rules

These are **mandatory** for all generated code:

- **C standard:** gnu89 (`-std=gnu89`). Declare all variables at block top. No `for(int i=...)`.
- **Comments:** `/* */` only, never `//`.
- **Indentation:** TAB characters (4-space width).
- **Naming:** `lowercase_snake_case` for functions/variables, `PascalCase` for types, `UPPER_SNAKE_CASE` for macros/defines.
- **Return types on separate line** from function name in definitions.
- **Function parameters aligned** to opening parenthesis.
- **GTK-Doc annotations** on all public API: `(transfer none)`, `(transfer full)`, `(nullable)`, etc.
- **`g_return_val_if_fail` / `g_return_if_fail`** preconditions on all public methods.
- **`(void)param;`** to suppress unused parameter warnings.
- **`G_PARAM_STATIC_STRINGS`** on all property specs.
- **Private struct** declared in .c file only (never in header for final types).
- **Compilation guard:** `#define {PREFIX}_COMPILATION` at top of .c file.
- **Include guard:** `{PREFIX}_INSIDE` / `{PREFIX}_COMPILATION` check in header.
- **Zero warnings** under `-Wall -Wextra`.

## Output Format

Two files per type:

1. `{prefix}-{name}.h` — Header with type declaration, public API prototypes
2. `{prefix}-{name}.c` — Source with type definition, private struct, implementation

Files are placed alongside existing source files in the project's `src/` directory (or appropriate subdirectory).

## Examples

**Input:** "Create a final GObject type called GstRenderer in the GST namespace that has a `width` and `height` property and a `frame-ready` signal"

**Output:** `gst-renderer.h` + `gst-renderer.c` with:
- `G_DECLARE_FINAL_TYPE(GstRenderer, gst_renderer, GST, RENDERER, GObject)`
- `G_DEFINE_FINAL_TYPE_WITH_PRIVATE(GstRenderer, gst_renderer, G_TYPE_OBJECT)`
- Properties: `width` (uint), `height` (uint) with get/set
- Signal: `frame-ready` with `G_SIGNAL_RUN_LAST`
- `gst_renderer_new()` constructor
- `gst_renderer_finalize()` cleanup

## Constraints

- Never generate code that uses `//` comments
- Never use C99 variable declarations mid-block
- Never omit the compilation guard (`#define PREFIX_COMPILATION`)
- Never put private struct fields in the header for final types
- Never omit `G_BEGIN_DECLS` / `G_END_DECLS` in headers
- Never skip `g_return_val_if_fail` preconditions on public API
