---
name: skill-mcp-server
description: >
  Generate an MCP (Model Context Protocol) server skeleton using mcp-glib.
  Trigger when creating MCP servers, tool providers, or AI agent integrations
  in C with GLib/GObject.
---

# Skill: MCP Server Generator (mcp-glib)

Generates a complete, working MCP server skeleton using the mcp-glib library. The server communicates over stdio, registers tools with JSON Schema input definitions, and handles tool calls via GObject callbacks. All output follows gnu89 C conventions.

## When to Use

- When creating a new MCP server for AI tool integration
- When adding tool-call capabilities to a C/GLib application
- When the user says "create an MCP server", "add MCP tools", or "build a tool provider"
- When wrapping an existing C library or CLI tool as an MCP server

## Prerequisites

- `mcp-glib` library installed or available as a bundled dependency
- `pkg-config` entry: `mcp-glib-1.0`
- Depends on: `glib-2.0`, `gobject-2.0`, `gio-2.0`, `json-glib-1.0`

## Instructions

### 1. Gather Requirements

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Server name** | Yes | — | Human-readable name (e.g., `gdb-mcp-server`) |
| **Server version** | No | `0.1.0` | Semantic version |
| **Tools** | Yes | — | List of tools with names, descriptions, and parameters |
| **Resources** | No | none | Static resources to expose |
| **Prompts** | No | none | Prompt templates to expose |
| **Wrapper GObject** | No | yes | Whether to wrap McpServer in a custom GObject class |

### 2. Minimal Server (No Wrapper)

For simple servers with a few tools, no wrapper GObject is needed:

```c
#!/usr/bin/env crispy
#define CRISPY_PARAMS "-std=gnu89 -O2 $(pkg-config --cflags --libs glib-2.0 gobject-2.0 gio-2.0 json-glib-1.0 mcp-glib-1.0)"

/*
 * my-mcp-server — MCP server for {description}
 * Copyright (C) 2026  {Author} — AGPLv3
 */

#include <mcp.h>
#include <glib.h>
#include <json-glib/json-glib.h>
#include <stdio.h>

static GMainLoop *main_loop = NULL;

/* ================================================================
 * Tool: hello_world
 * ================================================================ */

static McpToolResult *
handle_hello(McpServer   *server,
             const gchar *tool_name,
             JsonObject  *arguments,
             gpointer     user_data)
{
	McpToolResult *result;
	const gchar *name;

	(void)server;
	(void)tool_name;
	(void)user_data;

	name = json_object_get_string_member_with_default(arguments, "name", "World");

	result = mcp_tool_result_new(FALSE);
	mcp_tool_result_add_text(result, g_strdup_printf("Hello, %s!", name));

	return result;
}

static McpTool *
create_hello_tool(void)
{
	McpTool *tool;
	JsonBuilder *builder;
	JsonNode *schema;

	/* Build JSON Schema for input parameters */
	builder = json_builder_new();
	json_builder_begin_object(builder);
	json_builder_set_member_name(builder, "type");
	json_builder_add_string_value(builder, "object");
	json_builder_set_member_name(builder, "properties");
	json_builder_begin_object(builder);
	json_builder_set_member_name(builder, "name");
	json_builder_begin_object(builder);
	json_builder_set_member_name(builder, "type");
	json_builder_add_string_value(builder, "string");
	json_builder_set_member_name(builder, "description");
	json_builder_add_string_value(builder, "Name to greet");
	json_builder_end_object(builder);
	json_builder_end_object(builder);
	json_builder_end_object(builder);

	schema = json_builder_get_root(builder);
	tool = mcp_tool_new("hello_world", "Say hello to someone", schema);

	json_node_unref(schema);
	g_object_unref(builder);

	return tool;
}

/* ================================================================
 * Server lifecycle
 * ================================================================ */

static void
on_client_disconnected(McpServer *server,
                       gpointer   user_data)
{
	(void)server;
	(void)user_data;

	g_main_loop_quit(main_loop);
}

int
main(int argc, char **argv)
{
	McpServer *server;
	McpTool *tool;

	(void)argc;
	(void)argv;

	main_loop = g_main_loop_new(NULL, FALSE);

	/* Create server */
	server = mcp_server_new("my-mcp-server", "0.1.0");

	/* Register tools */
	tool = create_hello_tool();
	mcp_server_add_tool(server, tool, handle_hello, NULL, NULL);
	g_object_unref(tool);

	/* Connect signals */
	g_signal_connect(server, "client-disconnected",
	                 G_CALLBACK(on_client_disconnected), NULL);

	/* Start on stdio */
	mcp_server_start_async(server,
	                       mcp_stdio_transport_new(),
	                       NULL, NULL, NULL);

	g_main_loop_run(main_loop);

	/* Cleanup */
	g_object_unref(server);
	g_main_loop_unref(main_loop);

	return 0;
}
```

### 3. GObject-Wrapped Server (Recommended for Complex Servers)

For servers with many tools, state management, and resource lifecycle:

#### Header: `my-mcp-server.h`

```c
#ifndef MY_MCP_SERVER_H
#define MY_MCP_SERVER_H

#include <mcp.h>
#include <glib-object.h>

G_BEGIN_DECLS

#define MY_TYPE_MCP_SERVER (my_mcp_server_get_type())

G_DECLARE_FINAL_TYPE(MyMcpServer, my_mcp_server, MY, MCP_SERVER, GObject)

MyMcpServer *
my_mcp_server_new(void);

McpServer *
my_mcp_server_get_mcp_server(MyMcpServer *self);

void
my_mcp_server_start(MyMcpServer *self);

G_END_DECLS

#endif /* MY_MCP_SERVER_H */
```

#### Source: `my-mcp-server.c`

```c
#include "my-mcp-server.h"
#include <json-glib/json-glib.h>

struct _MyMcpServer
{
	GObject    parent_instance;
	McpServer *server;

	/* Server state */
	GHashTable *sessions;  /* example: managed sessions */
};

G_DEFINE_FINAL_TYPE(MyMcpServer, my_mcp_server, G_TYPE_OBJECT)

/* ================================================================
 * Tool handlers
 * ================================================================ */

static McpToolResult *
handle_start(McpServer   *server,
             const gchar *tool_name,
             JsonObject  *arguments,
             gpointer     user_data)
{
	MyMcpServer *self;
	McpToolResult *result;
	const gchar *name;

	(void)server;
	(void)tool_name;

	self = MY_MCP_SERVER(user_data);
	name = json_object_get_string_member_with_default(arguments, "name", "default");

	/* Do something with self->sessions ... */
	g_hash_table_insert(self->sessions, g_strdup(name), g_strdup("active"));

	result = mcp_tool_result_new(FALSE);
	mcp_tool_result_add_text(result,
		g_strdup_printf("Started session: %s", name));

	return result;
}

static McpToolResult *
handle_stop(McpServer   *server,
            const gchar *tool_name,
            JsonObject  *arguments,
            gpointer     user_data)
{
	MyMcpServer *self;
	McpToolResult *result;
	const gchar *name;

	(void)server;
	(void)tool_name;

	self = MY_MCP_SERVER(user_data);
	name = json_object_get_string_member_with_default(arguments, "name", "default");

	if (!g_hash_table_contains(self->sessions, name)) {
		result = mcp_tool_result_new(TRUE);  /* is_error = TRUE */
		mcp_tool_result_add_text(result,
			g_strdup_printf("No session named '%s'", name));
		return result;
	}

	g_hash_table_remove(self->sessions, name);

	result = mcp_tool_result_new(FALSE);
	mcp_tool_result_add_text(result,
		g_strdup_printf("Stopped session: %s", name));

	return result;
}

/* ================================================================
 * Tool registration helpers
 * ================================================================ */

static JsonNode *
build_schema_object(const gchar *first_prop, ...)
{
	JsonBuilder *builder;
	JsonNode *schema;
	va_list args;
	const gchar *name;
	const gchar *type;
	const gchar *desc;

	builder = json_builder_new();
	json_builder_begin_object(builder);
	json_builder_set_member_name(builder, "type");
	json_builder_add_string_value(builder, "object");
	json_builder_set_member_name(builder, "properties");
	json_builder_begin_object(builder);

	va_start(args, first_prop);
	name = first_prop;
	while (name != NULL) {
		type = va_arg(args, const gchar *);
		desc = va_arg(args, const gchar *);

		json_builder_set_member_name(builder, name);
		json_builder_begin_object(builder);
		json_builder_set_member_name(builder, "type");
		json_builder_add_string_value(builder, type);
		json_builder_set_member_name(builder, "description");
		json_builder_add_string_value(builder, desc);
		json_builder_end_object(builder);

		name = va_arg(args, const gchar *);
	}
	va_end(args);

	json_builder_end_object(builder);
	json_builder_end_object(builder);

	schema = json_builder_get_root(builder);
	g_object_unref(builder);
	return schema;
}

static void
register_tool(MyMcpServer        *self,
              const gchar        *name,
              const gchar        *description,
              JsonNode           *schema,
              McpToolHandlerFunc  handler)
{
	McpTool *tool;

	tool = mcp_tool_new(name, description, schema);
	mcp_server_add_tool(self->server, tool, handler, self, NULL);
	g_object_unref(tool);
	json_node_unref(schema);
}

/* ================================================================
 * GObject lifecycle
 * ================================================================ */

static void
my_mcp_server_constructed(GObject *object)
{
	MyMcpServer *self;

	G_OBJECT_CLASS(my_mcp_server_parent_class)->constructed(object);

	self = MY_MCP_SERVER(object);

	/* Register all tools after construction */
	register_tool(self, "start", "Start a new session",
		build_schema_object(
			"name", "string", "Session name",
			NULL),
		handle_start);

	register_tool(self, "stop", "Stop a session",
		build_schema_object(
			"name", "string", "Session name to stop",
			NULL),
		handle_stop);
}

static void
my_mcp_server_finalize(GObject *object)
{
	MyMcpServer *self;

	self = MY_MCP_SERVER(object);

	g_clear_object(&self->server);
	g_hash_table_unref(self->sessions);

	G_OBJECT_CLASS(my_mcp_server_parent_class)->finalize(object);
}

static void
my_mcp_server_class_init(MyMcpServerClass *klass)
{
	GObjectClass *object_class;

	object_class = G_OBJECT_CLASS(klass);
	object_class->constructed = my_mcp_server_constructed;
	object_class->finalize = my_mcp_server_finalize;
}

static void
my_mcp_server_init(MyMcpServer *self)
{
	self->server = mcp_server_new("my-mcp-server", "0.1.0");
	self->sessions = g_hash_table_new_full(g_str_hash, g_str_equal,
	                                        g_free, g_free);
}

/* ================================================================
 * Public API
 * ================================================================ */

MyMcpServer *
my_mcp_server_new(void)
{
	return g_object_new(MY_TYPE_MCP_SERVER, NULL);
}

McpServer *
my_mcp_server_get_mcp_server(MyMcpServer *self)
{
	g_return_val_if_fail(MY_IS_MCP_SERVER(self), NULL);
	return self->server;
}

void
my_mcp_server_start(MyMcpServer *self)
{
	g_return_if_fail(MY_IS_MCP_SERVER(self));
	mcp_server_start_async(self->server,
	                       mcp_stdio_transport_new(),
	                       NULL, NULL, NULL);
}
```

#### Main: `main.c`

```c
#include "my-mcp-server.h"
#include <glib.h>
#include <signal.h>

static GMainLoop *main_loop = NULL;

static void
on_client_disconnected(McpServer *server,
                       gpointer   user_data)
{
	(void)server;
	(void)user_data;

	g_main_loop_quit(main_loop);
}

static void
handle_sigint(int signum)
{
	(void)signum;
	if (main_loop != NULL)
		g_main_loop_quit(main_loop);
}

int
main(int argc, char **argv)
{
	MyMcpServer *server;
	McpServer *mcp;

	(void)argc;
	(void)argv;

	signal(SIGINT, handle_sigint);
	signal(SIGTERM, handle_sigint);

	main_loop = g_main_loop_new(NULL, FALSE);

	server = my_mcp_server_new();
	mcp = my_mcp_server_get_mcp_server(server);

	g_signal_connect(mcp, "client-disconnected",
	                 G_CALLBACK(on_client_disconnected), NULL);

	my_mcp_server_start(server);

	g_main_loop_run(main_loop);

	g_object_unref(server);
	g_main_loop_unref(main_loop);

	return 0;
}
```

### 4. Tool Handler Patterns

#### Returning Text Results

```c
static McpToolResult *
handle_query(McpServer *server, const gchar *name,
             JsonObject *args, gpointer user_data)
{
	McpToolResult *result;

	(void)server;
	(void)name;
	(void)user_data;

	result = mcp_tool_result_new(FALSE);  /* FALSE = not an error */
	mcp_tool_result_add_text(result, g_strdup("Query result here"));

	return result;
}
```

#### Returning Errors

```c
static McpToolResult *
handle_risky(McpServer *server, const gchar *name,
             JsonObject *args, gpointer user_data)
{
	McpToolResult *result;
	const gchar *path;

	(void)server;
	(void)name;
	(void)user_data;

	path = json_object_get_string_member_with_default(args, "path", NULL);
	if (path == NULL) {
		result = mcp_tool_result_new(TRUE);  /* TRUE = error */
		mcp_tool_result_add_text(result, g_strdup("Missing required parameter: path"));
		return result;
	}

	/* ... do work ... */

	result = mcp_tool_result_new(FALSE);
	mcp_tool_result_add_text(result, g_strdup("Success"));
	return result;
}
```

#### Extracting Parameters

```c
/* String parameter */
const gchar *name = json_object_get_string_member_with_default(args, "name", "default");

/* Integer parameter */
gint64 count = json_object_get_int_member_with_default(args, "count", 10);

/* Boolean parameter */
gboolean verbose = json_object_get_boolean_member_with_default(args, "verbose", FALSE);

/* Required parameter (check existence) */
if (!json_object_has_member(args, "session_id")) {
	result = mcp_tool_result_new(TRUE);
	mcp_tool_result_add_text(result, g_strdup("Missing required: session_id"));
	return result;
}
const gchar *session_id = json_object_get_string_member(args, "session_id");
```

### 5. Build System

#### Makefile for MCP server:

```makefile
include config.mk

SRCS := src/main.c src/my-mcp-server.c
OBJS := $(patsubst src/%.c,$(OBJDIR)/%.o,$(SRCS))

CFLAGS += $(shell pkg-config --cflags mcp-glib-1.0 json-glib-1.0)
LDFLAGS += $(shell pkg-config --libs mcp-glib-1.0 json-glib-1.0)

all: $(OUTDIR)/my-mcp-server

$(OUTDIR)/my-mcp-server: $(OBJS)
	@mkdir -p $(dir $@)
	$(CC) -o $@ $^ $(LDFLAGS)

$(OBJDIR)/%.o: src/%.c
	@mkdir -p $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

clean:
	rm -rf $(BUILDDIR)

.PHONY: all clean
```

#### As bundled dependency (from another project):

```makefile
# In config.mk:
MCP_GLIB_DIR    := deps/mcp-glib
MCP_GLIB_STATIC := $(MCP_GLIB_DIR)/build/libmcp-glib-1.0.a
MCP_GLIB_CFLAGS := -I$(MCP_GLIB_DIR)/src
MCP_GLIB_LIBS   := $(MCP_GLIB_STATIC)

# In Makefile:
$(MCP_GLIB_STATIC):
	$(MAKE) -C $(MCP_GLIB_DIR) lib
```

## Output Format

For a minimal server: single `.c` file (crispy-compatible or standalone).

For a GObject-wrapped server:
1. `src/my-mcp-server.h` — Server wrapper GObject header
2. `src/my-mcp-server.c` — Server implementation with tool registration
3. `src/main.c` — Entry point with signal handling and GMainLoop
4. `Makefile` — Build system

## Examples

**Input:** "Create an MCP server called `mcp-docker` that has tools for listing containers, starting a container, and stopping a container"

**Output:** GObject-wrapped server with:
- `handle_list_containers` — runs `docker ps` and returns output
- `handle_start_container` — takes `container_id` param, runs `docker start`
- `handle_stop_container` — takes `container_id` param, runs `docker stop`
- JSON Schema for each tool's input parameters
- Proper error handling for missing params and failed commands

## Constraints

- Never generate code that uses `//` comments
- Never use C99 variable declarations mid-block
- Always use `mcp_tool_result_new(TRUE)` for error results (not NULL)
- Always free JsonNode/JsonBuilder objects after use
- Always handle the `client-disconnected` signal to quit the main loop
- Never block the GMainLoop — use async operations for long-running work
- Always validate required parameters before using them
