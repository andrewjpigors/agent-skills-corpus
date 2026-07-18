---
name: skill-new-c-project
description: >
  Scaffold a complete GLib/GObject C project with three-file Makefile system,
  umbrella headers, version template, optional module/plugin system, GTest harness,
  pkg-config, YAML+C config system, container support, and git submodule integration.
  Trigger when: creating a new C project, starting a GObject library, scaffolding a
  GLib application, bootstrapping a C project, or when the user says "new project",
  "create project", "scaffold", "bootstrap", "init project", or "new C project".
---

# Skill: GLib/GObject C Project Scaffolder

Generates a complete, buildable GLib/GObject C project skeleton following conventions
proven across multiple production projects (yaml-glib, bacon, gst, libreclaw, podomation).
Supports three build modes — library-only, executable-only, or both — with optional
module/plugin system, YAML+C configuration, container deployment, and GObject Introspection.
The output is a ready-to-build project with a single initial GObject type, test scaffold,
documentation structure, and all build infrastructure in place.

## GObject Design Principles

The scaffolded project should be designed for extensibility from the start. Follow these
GObject type system patterns when expanding beyond the initial scaffold:

- **Prefer derivable types (`G_DECLARE_DERIVABLE_TYPE`) over final types** for any class
  that may need specialization later. Use `G_DECLARE_FINAL_TYPE` only for leaf types that
  will never be subclassed (e.g., a concrete module implementation). The initial `{Prefix}App`
  type is generated as derivable so it can be extended.
- **Use GInterfaces liberally** for cross-cutting capabilities. If multiple unrelated types
  need the same behavior (e.g., serialization, event handling, configuration), define a
  GInterface rather than forcing a common base class. Modules implement interfaces to
  declare their capabilities — the module manager auto-detects them via `g_type_is_a()`.
- **Use GObject signals** for decoupled event notification. Any type that emits events
  (state changes, lifecycle events, data arrival) should define signals. This allows
  consumers to connect without the emitter knowing about them. The initial `{Prefix}App`
  type includes example signals (`started`, `stopped`) as a pattern to follow.
- **Use boxed types (`G_DEFINE_BOXED_TYPE`)** for lightweight value types that don't need
  the full GObject machinery (properties, signals, ref-counting via GObject). Boxed types
  are ideal for: messages, tokens, configuration entries, result structs, keys, and any
  data passed through signals or stored in collections. They support `g_autoptr()` cleanup
  and GObject Introspection.  Place boxed types in `src/boxed/`.
- **Use GObject properties** for configuration values on types. Properties enable
  introspection, data binding, and notification via `notify::property-name` signals.
- **ABI stability**: All derivable class structs must include `gpointer padding[7]` for
  future virtual method additions. New virtual methods consume padding slots from the end
  (padding[6] first, then [5], etc.) — this allows library updates without recompiling
  subclasses.

These patterns are what allow the reference projects to scale to 50-70+ modules and
55K+ lines of code while remaining maintainable.

## When to Use

- Creating a new GLib/GObject C project from scratch
- User says "new project", "create project", "scaffold", "bootstrap"
- Starting a new library, CLI tool, daemon, or application using GObject
- Setting up a project with the three-file Makefile system (config.mk / rules.mk / Makefile)
- When module/plugin system scaffolding is needed

## Prerequisites

- `gcc` compiler
- `pkg-config`
- GLib 2.0 development headers (`glib2-devel` on Fedora, `libglib2.0-dev` on Debian)
- `git` (for repo initialization and submodules)
- GNU `make`
- For config system: `libyaml-devel` (yaml-0.1 pkg-config)

## Instructions

### Step 1: Gather Requirements

Collect the following parameters. Items marked with a default can be inferred if not provided.

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Project name** | Yes | — | kebab-case (e.g., `my-tool`, `bacon`, `gst`) |
| **Prefix** | Yes | — | Short UPPER prefix for macros/types (e.g., `BACON`, `GST`, `LC`, `POD`) |
| **Description** | Yes | — | One-line project description |
| **Build mode** | No | `both` | `library`, `executable`, or `both` |
| **API version** | No | `1.0` | Library API version (used in soname and pkg-config) |
| **pkg-config deps** | No | `glib-2.0 gobject-2.0 gio-2.0` | Space-separated package names |
| **Module system** | No | `no` | Enable plugin/module support (`yes`/`no`) |
| **Config system** | No | `no` for lib, `yes` for exe/both | YAML + C config via crispy/yaml-glib |
| **Data folder** | No | `no` for lib, `yes` for exe/both | data/ with logo, examples, default configs |
| **Examples dir** | No | `yes` for lib, `no` otherwise | examples/ with compilable sample programs |
| **GIR support** | No | `no` | GObject Introspection generation |
| **Container support** | No | `no` | Containerfile for podman deployment |
| **Git remote** | No | none | Remote URL for git origin |

**Decision Matrix — what gets generated per mode:**

| File/Directory | library | executable | both |
|---------------|---------|-----------|------|
| `src/main.c` | — | Yes | Yes |
| Static + shared library | Yes | — | Yes |
| pkg-config `.pc.in` | Yes | — | Yes |
| Header installation | Yes | — | Yes |
| `examples/` | Optional | — | Optional |
| `data/` | — | Optional | Optional |
| Config system (crispy/yaml-glib) | — | Optional | Optional |
| Module system | Optional | Optional | Optional |
| Container support | — | Optional | Optional |

---

### Step 2: Derive Naming Conventions

From the project name and prefix, derive all naming forms used throughout the templates.
**All templates below use these placeholders.**

Given project name `my-tool` and prefix `MT`:

| Placeholder | Value | Usage |
|-------------|-------|-------|
| `{project}` | `my-tool` | File names, directory name, pkg-config name |
| `{project_under}` | `my_tool` | C function prefix when prefix is multi-word |
| `{prefix}` | `mt` | C function prefix (lowercase) |
| `{PREFIX}` | `MT` | Macros, type check macros, defines |
| `{Prefix}` | `Mt` | GObject type names (PascalCase) |
| `{api_version}` | `1.0` | Soname, pkg-config version |
| `{description}` | `My Tool description` | .pc file, README |
| `{deps}` | `glib-2.0 gobject-2.0 gio-2.0` | pkg-config Requires |
| `{LIB_NAME}` | `my-tool-1.0` | Library base name |
| `{INSIDE_GUARD}` | `MT_INSIDE` | Umbrella header guard |
| `{COMPILATION_DEF}` | `MT_COMPILATION` | Compilation define |
| `{GIR_NAMESPACE}` | `MyTool` | GIR namespace (PascalCase, no separator) |

---

### Step 3: Create Directory Structure

Create the base directories. Conditionally add directories based on mode and features.

**All modes:**
```
{project}/
├── src/
│   └── core/
├── tests/
├── docs/
```

**If build mode is `library` or `both`:**
No additional src/ subdirectories needed beyond core/.

**If build mode is `executable` or `both`:**
```
├── src/main.c          (for simple projects)
```

**If module system is enabled:**
```
├── src/interfaces/
├── src/module/
├── modules/
│   └── example/
```

**If config system is enabled:**
```
├── deps/
```

**If data folder is enabled:**
```
├── data/
│   └── examples/
```

**If examples directory is enabled (library projects):**
```
├── examples/
```

**If container support is enabled:**
```
├── container/
```

Run:
```bash
mkdir -p {project}/src/core {project}/tests {project}/docs
# Add conditional directories as needed per the above
```

---

### Step 4: Generate `config.mk`

Create `config.mk` with the following template. Sections marked with `[IF ...]` are
conditional — include only when the condition is met.

```makefile
# config.mk - {project} Configuration
# {description}
#
# Copyright (C) {year}
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# This file contains all configurable build options.
# Override any variable on the command line:
#   make DEBUG=1
#   make PREFIX=/usr/local

# ── Project info ──────────────────────────────────────────────────────
PROJECT_NAME := {project}
VERSION_MAJOR := 0
VERSION_MINOR := 1
VERSION_MICRO := 0
VERSION := $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_MICRO)
API_VERSION := {api_version}

# Git SHA for version traceability
GIT_SHA := $(shell git rev-parse --short HEAD 2>/dev/null || echo "unknown")
GIT_DIRTY := $(shell git diff --quiet 2>/dev/null || echo "-UNSTAGED")
VERSION_FULL := $(VERSION)-$(GIT_SHA)$(GIT_DIRTY)

# ── Installation directories ─────────────────────────────────────────
PREFIX ?= /usr/local
BINDIR ?= $(PREFIX)/bin

# Auto-detect lib vs lib64 for 64-bit systems (Fedora, RHEL, SUSE, etc.)
# Override with: make LIBDIR=/usr/local/lib
LIBDIR_SUFFIX := $(shell if [ -d /usr/lib64 ]; then echo lib64; else echo lib; fi)
LIBDIR ?= $(PREFIX)/$(LIBDIR_SUFFIX)

INCLUDEDIR ?= $(PREFIX)/include
DATADIR ?= $(PREFIX)/share
SYSCONFDIR ?= /etc
PKGCONFIGDIR ?= $(LIBDIR)/pkgconfig
GIRDIR ?= $(DATADIR)/gir-1.0
TYPELIBDIR ?= $(LIBDIR)/girepository-1.0

# [IF module system enabled]
MODULEDIR ?= $(LIBDIR)/{project}/modules

# ── Build directories ────────────────────────────────────────────────
BUILDDIR := build
OBJDIR_DEBUG := $(BUILDDIR)/debug/obj
OBJDIR_RELEASE := $(BUILDDIR)/release/obj
BINDIR_DEBUG := $(BUILDDIR)/debug
BINDIR_RELEASE := $(BUILDDIR)/release

# ── Build options (0 or 1) ───────────────────────────────────────────
DEBUG ?= 0
ASAN ?= 0
UBSAN ?= 0
BUILD_GIR ?= 0
BUILD_TESTS ?= 1
# [IF module system enabled]
BUILD_MODULES ?= 1
# [IF examples directory enabled]
BUILD_EXAMPLES ?= 1

# Select build directories based on DEBUG
ifeq ($(DEBUG),1)
    OBJDIR := $(OBJDIR_DEBUG)
    OUTDIR := $(BINDIR_DEBUG)
    BUILD_TYPE := debug
else
    OBJDIR := $(OBJDIR_RELEASE)
    OUTDIR := $(BINDIR_RELEASE)
    BUILD_TYPE := release
endif

# ── Compiler and tools ───────────────────────────────────────────────
CC := gcc
AR := ar
PKG_CONFIG ?= pkg-config
GIR_SCANNER ?= g-ir-scanner
GIR_COMPILER ?= g-ir-compiler
INSTALL := install
INSTALL_PROGRAM := $(INSTALL) -m 755
INSTALL_DATA := $(INSTALL) -m 644
MKDIR_P := mkdir -p

# ── C standard and warnings ─────────────────────────────────────────
CSTD := -std=gnu89
WARNINGS := -Wall -Wextra -Wno-unused-parameter -Wformat=2 -Wshadow

# ── Base compiler flags ──────────────────────────────────────────────
CFLAGS_BASE := $(CSTD) $(WARNINGS)
CFLAGS_BASE += -fPIC
CFLAGS_BASE += -D{PREFIX}_VERSION=\"$(VERSION)\"
CFLAGS_BASE += -D{PREFIX}_VERSION_FULL=\"$(VERSION_FULL)\"
CFLAGS_BASE += -D{PREFIX}_VERSION_MAJOR=$(VERSION_MAJOR)
CFLAGS_BASE += -D{PREFIX}_VERSION_MINOR=$(VERSION_MINOR)
CFLAGS_BASE += -D{PREFIX}_VERSION_MICRO=$(VERSION_MICRO)
CFLAGS_BASE += -DG_LOG_DOMAIN=\"{Prefix}\"
# [IF module system enabled]
CFLAGS_BASE += -D{PREFIX}_MODULEDIR=\"$(MODULEDIR)\"
CFLAGS_BASE += -D{PREFIX}_DEV_MODULE_DIR=\"$(CURDIR)/$(OUTDIR)/modules\"
# [IF config system or data folder enabled]
CFLAGS_BASE += -D{PREFIX}_SYSCONFDIR=\"$(SYSCONFDIR)\"
CFLAGS_BASE += -D{PREFIX}_DATADIR=\"$(DATADIR)\"

# ── Debug/Release flags ──────────────────────────────────────────────
ifeq ($(DEBUG),1)
    CFLAGS_BUILD := -g -O0 -DDEBUG
else
    CFLAGS_BUILD := -O2 -DNDEBUG
endif

# AddressSanitizer (requires DEBUG=1)
ifeq ($(ASAN),1)
    CFLAGS_BUILD += -fsanitize=address -fno-omit-frame-pointer
    LDFLAGS_ASAN := -fsanitize=address
endif

# UndefinedBehaviorSanitizer
ifeq ($(UBSAN),1)
    CFLAGS_BUILD += -fsanitize=undefined
    LDFLAGS_UBSAN := -fsanitize=undefined
endif

# ── Dependencies (pkg-config) ────────────────────────────────────────
DEPS_REQUIRED := {deps}
# [IF module system enabled, add gmodule-2.0 to deps]

# Check for required dependencies
define check_dep
$(if $(shell $(PKG_CONFIG) --exists $(1) && echo yes),,$(error Missing dependency: $(1)))
endef

# Get flags from pkg-config
CFLAGS_DEPS := $(shell $(PKG_CONFIG) --cflags $(DEPS_REQUIRED) 2>/dev/null)
LDFLAGS_DEPS := $(shell $(PKG_CONFIG) --libs $(DEPS_REQUIRED) 2>/dev/null)

# [IF config system enabled]
# ── Crispy integration ───────────────────────────────────────────────
CRISPY_DIR := deps/crispy
CRISPY_CFLAGS := -I$(CRISPY_DIR)/src -DCRISPY_COMPILATION

# ── yaml-glib integration ───────────────────────────────────────────
YAMLGLIB_DIR := deps/yaml-glib
YAMLGLIB_CFLAGS := -I$(YAMLGLIB_DIR)/src
# [END IF config system]

# ── Include paths ────────────────────────────────────────────────────
CFLAGS_INC := -I. -Isrc -I$(OUTDIR)
# [IF config system enabled]
CFLAGS_INC += $(CRISPY_CFLAGS) $(YAMLGLIB_CFLAGS)

# ── Combine all CFLAGS ───────────────────────────────────────────────
CFLAGS := $(CFLAGS_BASE) $(CFLAGS_BUILD) $(CFLAGS_INC) $(CFLAGS_DEPS)

# ── Linker flags ─────────────────────────────────────────────────────
LDFLAGS := $(LDFLAGS_DEPS) $(LDFLAGS_ASAN) $(LDFLAGS_UBSAN)
LDFLAGS_SHARED := -shared -Wl,-soname,lib{project}-$(API_VERSION).so.$(VERSION_MAJOR)

# ── Library names ────────────────────────────────────────────────────
LIB_NAME := {project}-$(API_VERSION)
LIB_STATIC := lib$(LIB_NAME).a
LIB_SHARED := lib$(LIB_NAME).so
LIB_SHARED_FULL := lib$(LIB_NAME).so.$(VERSION)
LIB_SHARED_MAJOR := lib$(LIB_NAME).so.$(VERSION_MAJOR)

# ── GIR settings ─────────────────────────────────────────────────────
GIR_NAMESPACE := {GIR_NAMESPACE}
GIR_VERSION := $(API_VERSION)
GIR_FILE := $(GIR_NAMESPACE)-$(GIR_VERSION).gir
TYPELIB_FILE := $(GIR_NAMESPACE)-$(GIR_VERSION).typelib

# ── Test framework ───────────────────────────────────────────────────
TEST_CFLAGS := $(CFLAGS) $(shell $(PKG_CONFIG) --cflags glib-2.0)
TEST_LDFLAGS := $(LDFLAGS) -L$(OUTDIR) -l$(LIB_NAME) -Wl,-rpath,$(OUTDIR)

# [IF module system enabled]
# ── Module flags (absolute include paths for out-of-tree compilation) ─
MODULE_CFLAGS_INC := -I$(CURDIR) -I$(CURDIR)/src
# [IF config system enabled]
MODULE_CFLAGS_INC += -I$(CURDIR)/$(CRISPY_DIR)/src -I$(CURDIR)/$(YAMLGLIB_DIR)/src
# [END IF]
MODULE_CFLAGS := $(CFLAGS_BASE) $(CFLAGS_BUILD) $(MODULE_CFLAGS_INC) $(CFLAGS_DEPS)
MODULE_LDFLAGS := -shared -fPIC
# [END IF module system]

# ── Print configuration ──────────────────────────────────────────────
.PHONY: show-config
show-config:
	@echo "{PROJECT_NAME} Build Configuration"
	@echo "========================"
	@echo "Version:        $(VERSION_FULL)"
	@echo "API Version:    $(API_VERSION)"
	@echo "Build type:     $(BUILD_TYPE)"
	@echo "Compiler:       $(CC)"
	@echo "CFLAGS:         $(CFLAGS)"
	@echo "LDFLAGS:        $(LDFLAGS)"
	@echo "PREFIX:         $(PREFIX)"
	@echo "LIBDIR:         $(LIBDIR)"
	@echo "DEBUG:          $(DEBUG)"
	@echo "ASAN:           $(ASAN)"
	@echo "UBSAN:          $(UBSAN)"
	@echo "BUILD_GIR:      $(BUILD_GIR)"
	@echo "BUILD_TESTS:    $(BUILD_TESTS)"

# ── Package names for install-deps ───────────────────────────────────

# Fedora / RHEL / CentOS
FEDORA_DEPS_TOOLS := gcc make pkgconf-pkg-config
FEDORA_DEPS_REQUIRED := glib2-devel
# [Add distro-specific package names for all deps in DEPS_REQUIRED]
FEDORA_DEPS_GIR := gobject-introspection-devel

# Ubuntu / Debian
UBUNTU_DEPS_TOOLS := gcc make pkg-config
UBUNTU_DEPS_REQUIRED := libglib2.0-dev
UBUNTU_DEPS_GIR := gobject-introspection libgirepository1.0-dev

# Arch Linux
ARCH_DEPS_TOOLS := gcc make pkgconf
ARCH_DEPS_REQUIRED := glib2
ARCH_DEPS_GIR := gobject-introspection

# Detect distro and install
.PHONY: install-deps
install-deps:
	@if command -v dnf >/dev/null 2>&1; then \
		echo "Detected Fedora/RHEL (dnf)"; \
		sudo dnf install -y $(FEDORA_DEPS_TOOLS) $(FEDORA_DEPS_REQUIRED) \
			$(if $(filter 1,$(BUILD_GIR)),$(FEDORA_DEPS_GIR)); \
	elif command -v apt-get >/dev/null 2>&1; then \
		echo "Detected Ubuntu/Debian (apt)"; \
		sudo apt-get install -y $(UBUNTU_DEPS_TOOLS) $(UBUNTU_DEPS_REQUIRED) \
			$(if $(filter 1,$(BUILD_GIR)),$(UBUNTU_DEPS_GIR)); \
	elif command -v pacman >/dev/null 2>&1; then \
		echo "Detected Arch Linux (pacman)"; \
		sudo pacman -S --needed $(ARCH_DEPS_TOOLS) $(ARCH_DEPS_REQUIRED) \
			$(if $(filter 1,$(BUILD_GIR)),$(ARCH_DEPS_GIR)); \
	else \
		echo "Unknown distro. Required packages:"; \
		echo "  {deps}"; \
		exit 1; \
	fi
```

**Customize the distro package lists** to match the actual `DEPS_REQUIRED` packages for the project.

---

### Step 5: Generate `rules.mk`

Create `rules.mk` with the following template.

```makefile
# rules.mk - {project} Build Rules
# Pattern rules and common build recipes
#
# Copyright (C) {year}
# SPDX-License-Identifier: AGPL-3.0-or-later

# ── Source dependencies on generated headers ─────────────────────────
$(LIB_OBJS): src/{project}-version.h
# [IF executable or both mode]
$(MAIN_OBJ): src/{project}-version.h
# [IF config system enabled]
$(LIB_OBJS) $(MAIN_OBJ): deps/crispy/src/crispy-version.h

# ── Object file compilation ──────────────────────────────────────────

$(OBJDIR)/%.o: src/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/core/%.o: src/core/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

# [IF module system enabled]
$(OBJDIR)/interfaces/%.o: src/interfaces/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/module/%.o: src/module/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
# [END IF module system]

# ── Test compilation ─────────────────────────────────────────────────

$(OBJDIR)/tests/%.o: tests/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(TEST_CFLAGS) -MMD -MP -c $< -o $@

# Prevent make from deleting intermediate test objects
.PRECIOUS: $(OBJDIR)/tests/%.o

# [IF config system enabled]
# ── Dependency compilation: yaml-glib ────────────────────────────────

$(OBJDIR)/deps/yaml-glib/src/%.o: deps/yaml-glib/src/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

# ── Dependency compilation: crispy ───────────────────────────────────

$(OBJDIR)/deps/crispy/src/interfaces/%.o: deps/crispy/src/interfaces/%.c deps/crispy/src/crispy-version.h | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/deps/crispy/src/core/%.o: deps/crispy/src/core/%.c deps/crispy/src/crispy-version.h | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@
# [END IF config system]

# ── Static library ───────────────────────────────────────────────────

$(OUTDIR)/$(LIB_STATIC): $(LIB_OBJS) $(DEP_OBJS)
	@$(MKDIR_P) $(dir $@)
	$(AR) rcs $@ $^

# ── Shared library ───────────────────────────────────────────────────

$(OUTDIR)/$(LIB_SHARED_FULL): $(LIB_OBJS) $(DEP_OBJS)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(LDFLAGS_SHARED) -o $@ $^ $(LDFLAGS)
	cd $(OUTDIR) && ln -sf $(LIB_SHARED_FULL) $(LIB_SHARED_MAJOR)
	cd $(OUTDIR) && ln -sf $(LIB_SHARED_MAJOR) $(LIB_SHARED)

# [IF executable or both mode]
# ── Executable ───────────────────────────────────────────────────────

$(OUTDIR)/{project}: $(MAIN_OBJ) $(OUTDIR)/$(LIB_SHARED_FULL)
	$(CC) -o $@ $(MAIN_OBJ) -L$(OUTDIR) -l$(LIB_NAME) $(LDFLAGS) -Wl,-rpath,'$$ORIGIN'
# [END IF executable]

# ── GIR generation ───────────────────────────────────────────────────

$(OUTDIR)/$(GIR_FILE): $(LIB_SRCS) $(LIB_HDRS) | $(OUTDIR)/$(LIB_SHARED_FULL)
	$(GIR_SCANNER) \
		--namespace=$(GIR_NAMESPACE) \
		--nsversion=$(GIR_VERSION) \
		--library=$(LIB_NAME) \
		--library-path=$(OUTDIR) \
		--include=GLib-2.0 \
		--include=GObject-2.0 \
		--include=Gio-2.0 \
		--pkg=glib-2.0 \
		--pkg=gobject-2.0 \
		--pkg=gio-2.0 \
		--output=$@ \
		--warn-all \
		-Isrc \
		$(LIB_HDRS) $(LIB_SRCS)

$(OUTDIR)/$(TYPELIB_FILE): $(OUTDIR)/$(GIR_FILE)
	$(GIR_COMPILER) --output=$@ $<

# ── Generated files ──────────────────────────────────────────────────

# Version header
src/{project}-version.h: src/{project}-version.h.in
	sed \
		-e 's|@{PREFIX}_VERSION_MAJOR@|$(VERSION_MAJOR)|g' \
		-e 's|@{PREFIX}_VERSION_MINOR@|$(VERSION_MINOR)|g' \
		-e 's|@{PREFIX}_VERSION_MICRO@|$(VERSION_MICRO)|g' \
		-e 's|@{PREFIX}_VERSION@|$(VERSION)|g' \
		$< > $@

# [IF config system enabled]
# Crispy version header
deps/crispy/src/crispy-version.h: deps/crispy/src/crispy-version.h.in
	sed \
		-e 's|@CRISPY_VERSION_MAJOR@|0|g' \
		-e 's|@CRISPY_VERSION_MINOR@|2|g' \
		-e 's|@CRISPY_VERSION_MICRO@|0|g' \
		-e 's|@CRISPY_VERSION@|0.2.0|g' \
		$< > $@

# Embedded default config (YAML → C header constant)
$(OUTDIR)/{project}-default-config.h: data/default-config.yaml | $(OUTDIR)
	@echo "Generating embedded default config..."
	@echo '/* Auto-generated — do not edit */' > $@
	@echo 'static const char {PREFIX}_DEFAULT_CONFIG[] =' >> $@
	@sed 's/\\/\\\\/g; s/"/\\"/g; s/^/"/; s/$$/\\n"/' $< >> $@
	@echo ';' >> $@
# [END IF config system]

# [IF library or both mode]
# pkg-config file
$(OUTDIR)/{project}-$(API_VERSION).pc: {project}-$(API_VERSION).pc.in | $(OUTDIR)
	sed \
		-e 's|@PREFIX@|$(PREFIX)|g' \
		-e 's|@LIBDIR@|$(LIBDIR)|g' \
		-e 's|@INCLUDEDIR@|$(INCLUDEDIR)|g' \
		-e 's|@VERSION@|$(VERSION)|g' \
		-e 's|@API_VERSION@|$(API_VERSION)|g' \
		$< > $@
# [END IF library]

# ── Directory creation ───────────────────────────────────────────────

$(BUILDDIR):
	@$(MKDIR_P) $(BUILDDIR)

$(OBJDIR): | $(BUILDDIR)
	@$(MKDIR_P) $(OBJDIR)
	@$(MKDIR_P) $(OBJDIR)/core
	@$(MKDIR_P) $(OBJDIR)/tests
# [IF module system enabled]
	@$(MKDIR_P) $(OBJDIR)/interfaces
	@$(MKDIR_P) $(OBJDIR)/module
# [IF config system enabled]
	@$(MKDIR_P) $(OBJDIR)/deps/yaml-glib/src
	@$(MKDIR_P) $(OBJDIR)/deps/crispy/src/core
	@$(MKDIR_P) $(OBJDIR)/deps/crispy/src/interfaces

$(OUTDIR):
	@$(MKDIR_P) $(OUTDIR)

# [IF module system enabled]
$(OUTDIR)/modules:
	@$(MKDIR_P) $(OUTDIR)/modules

# ── Clean rules ──────────────────────────────────────────────────────

.PHONY: clean clean-all

clean:
	rm -rf $(BUILDDIR)/$(BUILD_TYPE)
	rm -f src/{project}-version.h
# [IF config system enabled]
	rm -f deps/crispy/src/crispy-version.h

clean-all:
	rm -rf $(BUILDDIR)
	rm -f src/{project}-version.h
# [IF config system enabled]
	rm -f deps/crispy/src/crispy-version.h

# ── Installation rules ───────────────────────────────────────────────

.PHONY: install uninstall

# [IF library or both mode]
install: install-lib install-headers install-pc
# [IF executable or both mode]
install: install-bin
# [END IF]
ifeq ($(BUILD_GIR),1)
install: install-gir
endif
# [IF module system enabled]
ifeq ($(BUILD_MODULES),1)
install: install-modules
endif

install-lib: $(OUTDIR)/$(LIB_STATIC) $(OUTDIR)/$(LIB_SHARED_FULL)
	$(MKDIR_P) $(DESTDIR)$(LIBDIR)
	$(INSTALL_DATA) $(OUTDIR)/$(LIB_STATIC) $(DESTDIR)$(LIBDIR)/
	$(INSTALL_PROGRAM) $(OUTDIR)/$(LIB_SHARED_FULL) $(DESTDIR)$(LIBDIR)/
	cd $(DESTDIR)$(LIBDIR) && ln -sf $(LIB_SHARED_FULL) $(LIB_SHARED_MAJOR)
	cd $(DESTDIR)$(LIBDIR) && ln -sf $(LIB_SHARED_MAJOR) $(LIB_SHARED)
	@if [ -z "$(DESTDIR)" ] && command -v ldconfig >/dev/null 2>&1; then \
		echo "Updating shared library cache..."; \
		ldconfig; \
	fi

# [IF executable or both mode]
install-bin: $(OUTDIR)/{project}
	$(MKDIR_P) $(DESTDIR)$(BINDIR)
	$(INSTALL_PROGRAM) $(OUTDIR)/{project} $(DESTDIR)$(BINDIR)/

install-headers:
	$(MKDIR_P) $(DESTDIR)$(INCLUDEDIR)/{project}
	$(INSTALL_DATA) src/{project}-version.h $(DESTDIR)$(INCLUDEDIR)/{project}/
	@for dir in core; do \
		if ls src/$$dir/*.h >/dev/null 2>&1; then \
			$(MKDIR_P) $(DESTDIR)$(INCLUDEDIR)/{project}/$$dir; \
			$(INSTALL_DATA) src/$$dir/*.h $(DESTDIR)$(INCLUDEDIR)/{project}/$$dir/; \
		fi; \
	done
	@if ls src/*.h >/dev/null 2>&1; then \
		$(INSTALL_DATA) src/*.h $(DESTDIR)$(INCLUDEDIR)/{project}/; \
	fi

install-pc: $(OUTDIR)/{project}-$(API_VERSION).pc
	$(MKDIR_P) $(DESTDIR)$(PKGCONFIGDIR)
	$(INSTALL_DATA) $(OUTDIR)/{project}-$(API_VERSION).pc $(DESTDIR)$(PKGCONFIGDIR)/

install-gir: $(OUTDIR)/$(GIR_FILE) $(OUTDIR)/$(TYPELIB_FILE)
	$(MKDIR_P) $(DESTDIR)$(GIRDIR)
	$(MKDIR_P) $(DESTDIR)$(TYPELIBDIR)
	$(INSTALL_DATA) $(OUTDIR)/$(GIR_FILE) $(DESTDIR)$(GIRDIR)/
	$(INSTALL_DATA) $(OUTDIR)/$(TYPELIB_FILE) $(DESTDIR)$(TYPELIBDIR)/

# [IF module system enabled]
install-modules:
	$(MKDIR_P) $(DESTDIR)$(MODULEDIR)
	@for mod in $(OUTDIR)/modules/*.so; do \
		if [ -f "$$mod" ]; then \
			$(INSTALL_DATA) "$$mod" $(DESTDIR)$(MODULEDIR)/; \
		fi; \
	done

uninstall:
	rm -f $(DESTDIR)$(BINDIR)/{project}
	rm -f $(DESTDIR)$(LIBDIR)/$(LIB_STATIC)
	rm -f $(DESTDIR)$(LIBDIR)/$(LIB_SHARED_FULL)
	rm -f $(DESTDIR)$(LIBDIR)/$(LIB_SHARED_MAJOR)
	rm -f $(DESTDIR)$(LIBDIR)/$(LIB_SHARED)
	rm -rf $(DESTDIR)$(INCLUDEDIR)/{project}
	rm -f $(DESTDIR)$(PKGCONFIGDIR)/{project}-$(API_VERSION).pc
	rm -f $(DESTDIR)$(GIRDIR)/$(GIR_FILE)
	rm -f $(DESTDIR)$(TYPELIBDIR)/$(TYPELIB_FILE)
	rm -rf $(DESTDIR)$(MODULEDIR)
```

**Adapt the install-headers rule** to include all source subdirectories that contain public
headers (interfaces/, module/, boxed/, etc.) as the project grows.

---

### Step 6: Generate `Makefile`

Create the top-level `Makefile` with the following template.

```makefile
# Makefile - {project}
# {description}
#
# Copyright (C) {year}
# SPDX-License-Identifier: AGPL-3.0-or-later
#
# Usage:
#   make             - Build all (lib{, {project}}{, modules})
#   make lib         - Build static and shared libraries
#   make test        - Run the test suite
#   make install     - Install to PREFIX
#   make clean       - Clean build artifacts
#   make DEBUG=1     - Build with debug symbols
#   make ASAN=1      - Build with AddressSanitizer

.DEFAULT_GOAL := all
.PHONY: all lib test check-deps help

# [IF executable or both mode]
.PHONY: {project}
# [IF module system enabled]
.PHONY: modules
# [IF GIR support]
.PHONY: gir

# Include configuration
include config.mk

# Check dependencies before anything else (skip for targets that don't need them)
SKIP_DEP_CHECK_TARGETS := install-deps help check-deps show-config clean clean-all
ifeq ($(filter $(SKIP_DEP_CHECK_TARGETS),$(MAKECMDGOALS)),)
$(foreach dep,$(DEPS_REQUIRED),$(call check_dep,$(dep)))
endif

# ── Source files: Library ────────────────────────────────────────────

LIB_SRCS := \
	src/{project}-types.c \
	src/core/{project}-app.c
# [IF module system enabled]
LIB_SRCS += \
	src/interfaces/{project}-example-hook.c \
	src/module/{project}-module.c \
	src/module/{project}-module-manager.c

# ── Header files (for GIR scanner and installation) ──────────────────

LIB_HDRS := $(shell find src/ -name '*.h' ! -name '*-private.h' 2>/dev/null)

# [IF config system enabled]
# ── Dependency sources: yaml-glib ────────────────────────────────────

YAMLGLIB_SRCS := \
	deps/yaml-glib/src/yaml-builder.c \
	deps/yaml-glib/src/yaml-document.c \
	deps/yaml-glib/src/yaml-generator.c \
	deps/yaml-glib/src/yaml-gobject.c \
	deps/yaml-glib/src/yaml-mapping.c \
	deps/yaml-glib/src/yaml-node.c \
	deps/yaml-glib/src/yaml-parser.c \
	deps/yaml-glib/src/yaml-schema.c \
	deps/yaml-glib/src/yaml-sequence.c \
	deps/yaml-glib/src/yaml-serializable.c

# ── Dependency sources: crispy ───────────────────────────────────────

CRISPY_SRCS := \
	deps/crispy/src/interfaces/crispy-compiler.c \
	deps/crispy/src/interfaces/crispy-cache-provider.c \
	deps/crispy/src/core/crispy-gcc-compiler.c \
	deps/crispy/src/core/crispy-file-cache.c \
	deps/crispy/src/core/crispy-plugin-engine.c \
	deps/crispy/src/core/crispy-script.c \
	deps/crispy/src/core/crispy-source-utils-private.c \
	deps/crispy/src/core/crispy-config-context.c \
	deps/crispy/src/core/crispy-config-loader.c
# [END IF config system]

# ── Test sources ─────────────────────────────────────────────────────

TEST_SRCS := $(wildcard tests/test-*.c)

# [IF module system enabled]
# ── Module directories ───────────────────────────────────────────────

MODULE_DIRS := $(wildcard modules/*)
# [END IF module system]

# ── Object file mappings ─────────────────────────────────────────────

LIB_OBJS := $(patsubst src/%.c,$(OBJDIR)/%.o,$(LIB_SRCS))

# [IF config system enabled]
YAMLGLIB_OBJS := $(patsubst deps/%.c,$(OBJDIR)/deps/%.o,$(YAMLGLIB_SRCS))
CRISPY_OBJS := $(patsubst deps/%.c,$(OBJDIR)/deps/%.o,$(CRISPY_SRCS))
DEP_OBJS := $(YAMLGLIB_OBJS) $(CRISPY_OBJS)
# [ELSE]
DEP_OBJS :=
# [END IF config system]

# [IF executable or both mode]
MAIN_OBJ := $(OBJDIR)/main.o
# [END IF]

TEST_OBJS := $(patsubst tests/%.c,$(OBJDIR)/tests/%.o,$(TEST_SRCS))
TEST_BINS := $(patsubst tests/%.c,$(OUTDIR)/%,$(TEST_SRCS))

# Include build rules
include rules.mk

# ── Default target ───────────────────────────────────────────────────

all: src/{project}-version.h lib
# [IF config system enabled]
all: deps/crispy/src/crispy-version.h
# [IF executable or both mode]
all: {project}
# [IF module system enabled]
ifeq ($(BUILD_MODULES),1)
all: modules
endif
# [IF GIR support]
ifeq ($(BUILD_GIR),1)
all: gir
endif

# ── Build the library ────────────────────────────────────────────────

lib: src/{project}-version.h \
     $(OUTDIR)/$(LIB_STATIC) $(OUTDIR)/$(LIB_SHARED_FULL)
# [IF library or both mode]
lib: $(OUTDIR)/{project}-$(API_VERSION).pc

# [IF executable or both mode]
# ── Build the executable ─────────────────────────────────────────────

{project}: lib $(OUTDIR)/{project}
# [END IF executable]

# ── Build GIR/typelib ────────────────────────────────────────────────

gir: $(OUTDIR)/$(GIR_FILE) $(OUTDIR)/$(TYPELIB_FILE)

# [IF module system enabled]
# ── Build all modules ────────────────────────────────────────────────

modules: lib $(OUTDIR)/modules
	@for dir in $(MODULE_DIRS); do \
		if [ -d "$$dir" ] && [ -f "$$dir/Makefile" ]; then \
			echo "Building module: $$(basename $$dir)"; \
			$(MAKE) -C "$$dir" \
				OUTDIR=$(abspath $(OUTDIR)/modules) \
				LIBDIR=$(abspath $(OUTDIR)) \
				CFLAGS='$(MODULE_CFLAGS)' \
				LDFLAGS='$(MODULE_LDFLAGS)'; \
		fi; \
	done
# [END IF module system]

# ── Build and run tests ──────────────────────────────────────────────

$(OUTDIR)/test-%: $(OBJDIR)/tests/test-%.o $(OUTDIR)/$(LIB_SHARED_FULL)
	$(CC) -o $@ $< $(TEST_LDFLAGS)

test: lib $(TEST_BINS)
	@echo "Running tests..."
	@failed=0; \
	total=0; \
	passed=0; \
	for test in $(TEST_BINS); do \
		total=$$((total + 1)); \
		echo "  Running $$(basename $$test)..."; \
		if LD_LIBRARY_PATH=$(OUTDIR) $$test; then \
			echo "    PASS"; \
			passed=$$((passed + 1)); \
		else \
			echo "    FAIL"; \
			failed=$$((failed + 1)); \
		fi; \
	done; \
	echo ""; \
	echo "Results: $$passed/$$total passed"; \
	if [ $$failed -gt 0 ]; then \
		echo "$$failed test(s) failed"; \
		exit 1; \
	else \
		echo "All tests passed"; \
	fi

# ── Check dependencies ───────────────────────────────────────────────

check-deps:
	@echo "Checking dependencies..."
	@for dep in $(DEPS_REQUIRED); do \
		if $(PKG_CONFIG) --exists $$dep; then \
			ver=$$($(PKG_CONFIG) --modversion $$dep 2>/dev/null); \
			echo "  $$dep: OK ($$ver)"; \
		else \
			echo "  $$dep: MISSING"; \
		fi; \
	done

# ── Help ─────────────────────────────────────────────────────────────

.PHONY: help
help:
	@echo "{project} - {description}"
	@echo ""
	@echo "Build targets:"
	@echo "  all          - Build everything (default)"
	@echo "  lib          - Build static and shared libraries"
	@echo "  test         - Build and run the test suite"
	@echo "  install      - Install to PREFIX ($(PREFIX))"
	@echo "  uninstall    - Remove installed files"
	@echo "  clean        - Remove build artifacts for current build type"
	@echo "  clean-all    - Remove all build directories"
	@echo ""
	@echo "Build options (set on command line):"
	@echo "  DEBUG=1         - Enable debug build (-g -O0)"
	@echo "  ASAN=1          - Enable AddressSanitizer"
	@echo "  UBSAN=1         - Enable UndefinedBehaviorSanitizer"
	@echo "  BUILD_GIR=1     - Enable GObject Introspection generation"
	@echo "  BUILD_TESTS=0   - Disable test building"
	@echo "  PREFIX=path     - Set installation prefix (default: /usr/local)"
	@echo ""
	@echo "Utility targets:"
	@echo "  install-deps  - Install build dependencies (auto-detects distro)"
	@echo "  check-deps    - Check for required pkg-config dependencies"
	@echo "  show-config   - Show current build configuration"
	@echo "  help          - Show this help message"

# ── Dependency tracking (incremental builds) ─────────────────────────

ALL_DEPS := $(LIB_OBJS:.o=.d) $(TEST_OBJS:.o=.d)
# [IF config system enabled]
ALL_DEPS += $(YAMLGLIB_OBJS:.o=.d) $(CRISPY_OBJS:.o=.d)
# [IF executable or both mode]
ifneq ($(MAIN_OBJ),)
ALL_DEPS += $(MAIN_OBJ:.o=.d)
endif

ifeq ($(filter clean clean-all,$(MAKECMDGOALS)),)
-include $(ALL_DEPS)
endif
```

---

### Step 7: Generate `src/` Boilerplate Files

#### 7a. Umbrella Header — `src/{project}.h`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}.h - Umbrella header for {description} */

#ifndef {PREFIX}_H
#define {PREFIX}_H

/**
 * SECTION:{project}
 * @title: {Prefix}
 * @short_description: {description}
 *
 * To use the library, include only this header:
 * |[<!-- language="C" -->
 * #include <{project}.h>
 * ]|
 */

#define {PREFIX}_INSIDE

/* Common types and enumerations */
#include "{project}-types.h"
#include "{project}-error.h"
#include "{project}-version.h"

/* Core types */
#include "core/{project}-app.h"

/* Boxed types — add boxed type headers here as they are created */
/* #include "boxed/{project}-result.h" */

/* [IF module system enabled] */
/* Interfaces */
#include "interfaces/{project}-example-hook.h"

/* Module system */
#include "module/{project}-module.h"
#include "module/{project}-module-manager.h"
/* [END IF module system] */

#undef {PREFIX}_INSIDE

#endif /* {PREFIX}_H */
```

#### 7b. Types Header — `src/{project}-types.h`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-types.h - Forward declarations and common types */

#ifndef {PREFIX}_TYPES_H
#define {PREFIX}_TYPES_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib.h>
#include <glib-object.h>

G_BEGIN_DECLS

/* ---- Final type forward declarations ---- */

typedef struct _{Prefix}App         {Prefix}App;
typedef struct _{Prefix}AppClass    {Prefix}AppClass;

/* ---- Boxed type forward declarations ---- */
/* Add boxed types here as the project grows (see src/boxed/) */

/* [IF module system enabled] */
/* ---- Interface forward declarations ---- */

typedef struct _{Prefix}ExampleHook           {Prefix}ExampleHook;
typedef struct _{Prefix}ExampleHookInterface  {Prefix}ExampleHookInterface;

/* ---- Module forward declarations (derivable) ---- */

typedef struct _{Prefix}Module          {Prefix}Module;
typedef struct _{Prefix}ModuleClass     {Prefix}ModuleClass;

/* ---- Module manager ---- */

typedef struct _{Prefix}ModuleManager   {Prefix}ModuleManager;
/* [END IF module system] */

G_END_DECLS

#endif /* {PREFIX}_TYPES_H */
```

#### 7c. Error Header — `src/{project}-error.h`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-error.h - Error domain and codes */

#ifndef {PREFIX}_ERROR_H
#define {PREFIX}_ERROR_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib.h>

G_BEGIN_DECLS

/**
 * {PREFIX}_ERROR:
 *
 * Error domain for {project} operations.
 * Errors in this domain will be from the #{Prefix}Error enumeration.
 */
#define {PREFIX}_ERROR ({prefix}_error_quark())

GQuark {prefix}_error_quark (void);

/**
 * {Prefix}Error:
 * @{PREFIX}_ERROR_CONFIG_PARSE: Failed to parse configuration file.
 * @{PREFIX}_ERROR_CONFIG_INVALID: Configuration value is invalid.
 * @{PREFIX}_ERROR_GENERAL: General error.
 *
 * Error codes for the %{PREFIX}_ERROR domain.
 * Add new codes organized by subsystem as the project grows.
 */
typedef enum
{
    {PREFIX}_ERROR_CONFIG_PARSE = 1,
    {PREFIX}_ERROR_CONFIG_INVALID,
    {PREFIX}_ERROR_GENERAL,
    /* [IF module system enabled] */
    {PREFIX}_ERROR_MODULE_LOAD,
    {PREFIX}_ERROR_MODULE_SYMBOL,
    {PREFIX}_ERROR_MODULE_TYPE,
    {PREFIX}_ERROR_MODULE_REGISTER,
} {Prefix}Error;

G_END_DECLS

#endif /* {PREFIX}_ERROR_H */
```

#### 7d. Error Source — `src/{project}-types.c`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-types.c - Error quark and common type registration */

#define {PREFIX}_COMPILATION
#include "{project}.h"

/**
 * {prefix}_error_quark:
 *
 * Returns the #GQuark for the {project} error domain.
 *
 * Returns: the error quark
 */
GQuark
{prefix}_error_quark(void)
{
    return g_quark_from_static_string("{project}-error-quark");
}
```

#### 7e. Version Header Template — `src/{project}-version.h.in`

```c
/*
 * {project}-version.h.in - Version Information Template
 *
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * This file is processed by the build system to generate {project}-version.h
 */

#ifndef {PREFIX}_VERSION_H
#define {PREFIX}_VERSION_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib.h>

G_BEGIN_DECLS

/**
 * {PREFIX}_VERSION_MAJOR:
 *
 * The major version component.
 */
#ifndef {PREFIX}_VERSION_MAJOR
#define {PREFIX}_VERSION_MAJOR (@{PREFIX}_VERSION_MAJOR@)
#endif

/**
 * {PREFIX}_VERSION_MINOR:
 *
 * The minor version component.
 */
#ifndef {PREFIX}_VERSION_MINOR
#define {PREFIX}_VERSION_MINOR (@{PREFIX}_VERSION_MINOR@)
#endif

/**
 * {PREFIX}_VERSION_MICRO:
 *
 * The micro version component.
 */
#ifndef {PREFIX}_VERSION_MICRO
#define {PREFIX}_VERSION_MICRO (@{PREFIX}_VERSION_MICRO@)
#endif

/**
 * {PREFIX}_VERSION_STRING:
 *
 * The full version string.
 */
#define {PREFIX}_VERSION_STRING "@{PREFIX}_VERSION@"

/**
 * {PREFIX}_CHECK_VERSION:
 * @major: the major version to check for
 * @minor: the minor version to check for
 * @micro: the micro version to check for
 *
 * Checks whether the library version is at least the requested version.
 *
 * Returns: %TRUE if the version is satisfied
 */
#define {PREFIX}_CHECK_VERSION(major, minor, micro) \
    (({PREFIX}_VERSION_MAJOR > (major)) || \
     ({PREFIX}_VERSION_MAJOR == (major) && {PREFIX}_VERSION_MINOR > (minor)) || \
     ({PREFIX}_VERSION_MAJOR == (major) && {PREFIX}_VERSION_MINOR == (minor) && \
      {PREFIX}_VERSION_MICRO >= (micro)))

/**
 * {prefix}_get_version:
 * @major: (out) (optional): location for major version
 * @minor: (out) (optional): location for minor version
 * @micro: (out) (optional): location for micro version
 *
 * Retrieves the runtime version of the library.
 */
void {prefix}_get_version (guint *major, guint *minor, guint *micro);

/**
 * {prefix}_get_version_string:
 *
 * Retrieves the runtime version string.
 *
 * Returns: (transfer none): the version string
 */
const gchar *{prefix}_get_version_string (void);

G_END_DECLS

#endif /* {PREFIX}_VERSION_H */
```

#### 7f. Initial Core Type — `src/core/{project}-app.h`

Generate the initial core type using conventions from `skill-gobject-type`.
This is a **derivable** GObject type — derivable so it can be extended later.
It includes example signals (`started`, `stopped`) to demonstrate the signal
pattern that all event-emitting types should follow.

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-app.h - Main application object */

#ifndef {PREFIX}_APP_H
#define {PREFIX}_APP_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define {PREFIX}_TYPE_APP ({prefix}_app_get_type())

/*
 * Derivable type — allows subclassing for specialized applications.
 * Use G_DECLARE_FINAL_TYPE only for leaf types that will never be subclassed.
 */
G_DECLARE_DERIVABLE_TYPE({Prefix}App, {prefix}_app, {PREFIX}, APP, GObject)

/**
 * {Prefix}AppClass:
 * @parent_class: the parent class
 * @started: class handler for the #started signal
 * @stopped: class handler for the #stopped signal
 * @padding: reserved for future virtual methods — consume slots from the
 *           end (padding[6] first, then [5], etc.) for ABI stability
 *
 * Virtual function table for #{Prefix}App. Subclasses can override
 * the signal class handlers to customize lifecycle behavior.
 */
struct _{Prefix}AppClass
{
    GObjectClass parent_class;

    /* signals */
    void (*started) ({Prefix}App *self);
    void (*stopped) ({Prefix}App *self);

    /*< private >*/
    gpointer padding[7];
};

/**
 * {prefix}_app_new:
 *
 * Creates a new #{Prefix}App instance.
 *
 * Returns: (transfer full): a new #{Prefix}App
 */
{Prefix}App *{prefix}_app_new (void);

/**
 * {prefix}_app_start:
 * @self: a #{Prefix}App
 *
 * Starts the application. Emits the #{Prefix}App::started signal.
 */
void {prefix}_app_start ({Prefix}App *self);

/**
 * {prefix}_app_stop:
 * @self: a #{Prefix}App
 *
 * Stops the application. Emits the #{Prefix}App::stopped signal.
 */
void {prefix}_app_stop ({Prefix}App *self);

G_END_DECLS

#endif /* {PREFIX}_APP_H */
```

#### 7g. Initial Core Type Source — `src/core/{project}-app.c`

Demonstrates: derivable type with private data, GObject signals, and properties.
This is the pattern all core types should follow.

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-app.c - Main application object implementation */

#define {PREFIX}_COMPILATION
#include "{project}.h"

typedef struct
{
    gboolean running;
} {Prefix}AppPrivate;

G_DEFINE_TYPE_WITH_PRIVATE({Prefix}App, {prefix}_app, G_TYPE_OBJECT)

/* ── Signal IDs ───────────────────────────────────────────────────── */

enum
{
    SIGNAL_STARTED,
    SIGNAL_STOPPED,
    N_SIGNALS
};

static guint signals[N_SIGNALS] = { 0 };

/* ── Property IDs ─────────────────────────────────────────────────── */

enum
{
    PROP_0,
    PROP_RUNNING,
    N_PROPS
};

static GParamSpec *properties[N_PROPS] = { NULL };

/* ── GObject overrides ────────────────────────────────────────────── */

static void
{prefix}_app_get_property(
    GObject    *object,
    guint       prop_id,
    GValue     *value,
    GParamSpec *pspec
){
    {Prefix}App *self;
    {Prefix}AppPrivate *priv;

    self = {PREFIX}_APP(object);
    priv = {prefix}_app_get_instance_private(self);

    switch (prop_id) {
    case PROP_RUNNING:
        g_value_set_boolean(value, priv->running);
        break;
    default:
        G_OBJECT_WARN_INVALID_PROPERTY_ID(object, prop_id, pspec);
    }
}

static void
{prefix}_app_class_init({Prefix}AppClass *klass)
{
    GObjectClass *object_class;

    object_class = G_OBJECT_CLASS(klass);
    object_class->get_property = {prefix}_app_get_property;

    /**
     * {Prefix}App:running:
     *
     * Whether the application is currently running.
     */
    properties[PROP_RUNNING] =
        g_param_spec_boolean(
            "running",
            "Running",
            "Whether the application is currently running",
            FALSE,
            G_PARAM_READABLE | G_PARAM_STATIC_STRINGS);

    g_object_class_install_properties(object_class, N_PROPS, properties);

    /**
     * {Prefix}App::started:
     * @self: the #{Prefix}App that emitted the signal
     *
     * Emitted when the application has started.
     * Connect to this signal to perform post-startup initialization.
     */
    signals[SIGNAL_STARTED] =
        g_signal_new("started",
                     G_TYPE_FROM_CLASS(klass),
                     G_SIGNAL_RUN_LAST,
                     G_STRUCT_OFFSET({Prefix}AppClass, started),
                     NULL, NULL, NULL,
                     G_TYPE_NONE, 0);

    /**
     * {Prefix}App::stopped:
     * @self: the #{Prefix}App that emitted the signal
     *
     * Emitted when the application is stopping.
     * Connect to this signal to perform cleanup before shutdown.
     */
    signals[SIGNAL_STOPPED] =
        g_signal_new("stopped",
                     G_TYPE_FROM_CLASS(klass),
                     G_SIGNAL_RUN_LAST,
                     G_STRUCT_OFFSET({Prefix}AppClass, stopped),
                     NULL, NULL, NULL,
                     G_TYPE_NONE, 0);
}

static void
{prefix}_app_init({Prefix}App *self)
{
    {Prefix}AppPrivate *priv;

    priv = {prefix}_app_get_instance_private(self);
    priv->running = FALSE;
}

/* ── Public API ───────────────────────────────────────────────────── */

/**
 * {prefix}_app_new:
 *
 * Creates a new #{Prefix}App instance.
 *
 * Returns: (transfer full): a new #{Prefix}App
 */
{Prefix}App *
{prefix}_app_new(void)
{
    return g_object_new({PREFIX}_TYPE_APP, NULL);
}

/**
 * {prefix}_app_start:
 * @self: a #{Prefix}App
 *
 * Starts the application and emits the #{Prefix}App::started signal.
 */
void
{prefix}_app_start({Prefix}App *self)
{
    {Prefix}AppPrivate *priv;

    g_return_if_fail({PREFIX}_IS_APP(self));

    priv = {prefix}_app_get_instance_private(self);
    priv->running = TRUE;
    g_object_notify_by_pspec(G_OBJECT(self), properties[PROP_RUNNING]);
    g_signal_emit(self, signals[SIGNAL_STARTED], 0);
}

/**
 * {prefix}_app_stop:
 * @self: a #{Prefix}App
 *
 * Stops the application and emits the #{Prefix}App::stopped signal.
 */
void
{prefix}_app_stop({Prefix}App *self)
{
    {Prefix}AppPrivate *priv;

    g_return_if_fail({PREFIX}_IS_APP(self));

    priv = {prefix}_app_get_instance_private(self);
    g_signal_emit(self, signals[SIGNAL_STOPPED], 0);
    priv->running = FALSE;
    g_object_notify_by_pspec(G_OBJECT(self), properties[PROP_RUNNING]);
}

/*
 * Version info implementation — placed here since this is always compiled.
 */

void
{prefix}_get_version(
    guint *major,
    guint *minor,
    guint *micro
){
    if (major) *major = {PREFIX}_VERSION_MAJOR;
    if (minor) *minor = {PREFIX}_VERSION_MINOR;
    if (micro) *micro = {PREFIX}_VERSION_MICRO;
}

const gchar *
{prefix}_get_version_string(void)
{
    return {PREFIX}_VERSION_STRING;
}
```

#### 7h. Boxed Type Example (optional, recommended)

When the project needs lightweight value types (messages, tokens, result structs),
create them in `src/boxed/`. Here is the pattern. Refer to `skill-gobject-type`
for the full boxed type template.

```c
/* In the header (src/boxed/{project}-result.h): */

#define {PREFIX}_TYPE_RESULT ({prefix}_result_get_type())

typedef struct _{Prefix}Result {Prefix}Result;

struct _{Prefix}Result
{
    gboolean success;
    gchar   *message;
    gint     code;
};

GType          {prefix}_result_get_type (void) G_GNUC_CONST;
{Prefix}Result *{prefix}_result_new     (gboolean     success,
                                         const gchar *message,
                                         gint         code);
{Prefix}Result *{prefix}_result_copy    (const {Prefix}Result *src);
void            {prefix}_result_free    ({Prefix}Result *self);

G_DEFINE_AUTOPTR_CLEANUP_FUNC({Prefix}Result, {prefix}_result_free)

/* In the source (src/boxed/{project}-result.c): */

G_DEFINE_BOXED_TYPE({Prefix}Result, {prefix}_result,
                    {prefix}_result_copy, {prefix}_result_free)
```

Boxed types are ideal for data passed through signals, stored in collections,
or returned from functions where full GObject overhead is unnecessary. Use them
instead of raw structs to get: `g_autoptr()` cleanup, GObject Introspection
support, and GValue/signal compatibility.

---

### Step 8: Generate `src/main.c` (executable and both modes only)

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* main.c - {project} entry point */

#define {PREFIX}_COMPILATION

#include <glib.h>
#include <glib-object.h>
#include <stdio.h>
#include <stdlib.h>

#include "{project}-types.h"
#include "{project}-version.h"
#include "core/{project}-app.h"
/* [IF module system enabled] */
#include "module/{project}-module-manager.h"

/* Version info */
#ifndef {PREFIX}_VERSION
#define {PREFIX}_VERSION "0.1.0"
#endif

/* --- Command-line option variables --- */

static gboolean opt_version = FALSE;
static gboolean opt_license = FALSE;
/* [IF config system enabled] */
static gchar *opt_config = NULL;
/* [IF module system enabled] */
static gchar *opt_module_dir = NULL;

static GOptionEntry option_entries[] = {
    {
        "version", 'v', 0, G_OPTION_ARG_NONE, &opt_version,
        "Show version", NULL
    },
    {
        "license", 0, 0, G_OPTION_ARG_NONE, &opt_license,
        "Show license", NULL
    },
    /* [IF config system enabled] */
    {
        "config", 'c', 0, G_OPTION_ARG_STRING, &opt_config,
        "Configuration file path", "PATH"
    },
    /* [IF module system enabled] */
    {
        "module-dir", 'M', 0, G_OPTION_ARG_STRING, &opt_module_dir,
        "Add module search path", "PATH"
    },
    { NULL }
};

static void
print_license(void)
{
    g_print(
        "{project} - {description}\n"
        "Copyright (C) {year}\n"
        "\n"
        "This program is free software: you can redistribute it and/or modify\n"
        "it under the terms of the GNU Affero General Public License as published by\n"
        "the Free Software Foundation, either version 3 of the License, or\n"
        "(at your option) any later version.\n"
        "\n"
        "This program is distributed in the hope that it will be useful,\n"
        "but WITHOUT ANY WARRANTY; without even the implied warranty of\n"
        "MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the\n"
        "GNU Affero General Public License for more details.\n"
        "\n"
        "You should have received a copy of the GNU Affero General Public License\n"
        "along with this program. If not, see <https://www.gnu.org/licenses/>.\n"
    );
}

int
main(
    int     argc,
    char  **argv
){
    g_autoptr(GOptionContext) context = NULL;
    g_autoptr(GError) error = NULL;
    g_autoptr({Prefix}App) app = NULL;

    context = g_option_context_new("- {description}");
    g_option_context_add_main_entries(context, option_entries, NULL);

    if (!g_option_context_parse(context, &argc, &argv, &error)) {
        g_printerr("Option parsing failed: %s\n", error->message);
        return 1;
    }

    if (opt_version) {
        g_print("{project} %s\n", {PREFIX}_VERSION);
        return 0;
    }

    if (opt_license) {
        print_license();
        return 0;
    }

    /* Create main application object */
    app = {prefix}_app_new();

    /* TODO: Initialize configuration, modules, and main loop */

    return 0;
}
```

---

### Step 9: Generate Module System (if enabled)

#### 9a. Module Base Class Header — `src/module/{project}-module.h`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-module.h - Abstract base class for all modules */

#ifndef {PREFIX}_MODULE_H
#define {PREFIX}_MODULE_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define {PREFIX}_TYPE_MODULE ({prefix}_module_get_type())

G_DECLARE_DERIVABLE_TYPE({Prefix}Module, {prefix}_module, {PREFIX}, MODULE, GObject)

/**
 * {Prefix}ModulePriority:
 * @{PREFIX}_MODULE_PRIORITY_FIRST: Run before all other modules.
 * @{PREFIX}_MODULE_PRIORITY_HIGH: Run early in the hook chain.
 * @{PREFIX}_MODULE_PRIORITY_NORMAL: Default priority.
 * @{PREFIX}_MODULE_PRIORITY_LOW: Run late in the hook chain.
 * @{PREFIX}_MODULE_PRIORITY_LAST: Run after all other modules.
 *
 * Well-known priority values for module ordering. Lower numeric
 * values run first.
 */
typedef enum
{
    {PREFIX}_MODULE_PRIORITY_FIRST  = -1000,
    {PREFIX}_MODULE_PRIORITY_HIGH   = -500,
    {PREFIX}_MODULE_PRIORITY_NORMAL = 0,
    {PREFIX}_MODULE_PRIORITY_LOW    = 500,
    {PREFIX}_MODULE_PRIORITY_LAST   = 1000
} {Prefix}ModulePriority;

/**
 * {Prefix}ModuleClass:
 * @parent_class: the parent class
 * @activate: called when the module is activated; return %TRUE on success
 * @deactivate: called when the module is deactivated
 * @get_name: return the module's human-readable name
 * @get_description: return a short description of the module
 * @configure: apply a configuration blob to the module
 * @padding: reserved for future virtual methods — new virtuals consume
 *           slots from the end (padding[6] first, then padding[5], etc.)
 *           to maintain ABI stability without recompiling modules
 *
 * The virtual function table for #{Prefix}Module.
 */
struct _{Prefix}ModuleClass
{
    GObjectClass parent_class;

    /* virtual methods */
    gboolean     (*activate)        ({Prefix}Module *self);
    void         (*deactivate)      ({Prefix}Module *self);
    const gchar *(*get_name)        ({Prefix}Module *self);
    const gchar *(*get_description) ({Prefix}Module *self);
    void         (*configure)       ({Prefix}Module *self,
                                     gpointer       config);

    /*< private >*/
    gpointer padding[7];
};

gboolean     {prefix}_module_activate        ({Prefix}Module *self);
void         {prefix}_module_deactivate      ({Prefix}Module *self);
const gchar *{prefix}_module_get_name        ({Prefix}Module *self);
const gchar *{prefix}_module_get_description ({Prefix}Module *self);
void         {prefix}_module_configure       ({Prefix}Module *self,
                                              gpointer       config);
gint         {prefix}_module_get_priority    ({Prefix}Module *self);
void         {prefix}_module_set_priority    ({Prefix}Module *self,
                                              gint           priority);
gboolean     {prefix}_module_is_active       ({Prefix}Module *self);

G_END_DECLS

#endif /* {PREFIX}_MODULE_H */
```

#### 9b. Module Base Class Source — `src/module/{project}-module.c`

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-module.c - Abstract base class for all modules */

#define {PREFIX}_COMPILATION
#include "{project}.h"

typedef struct
{
    gint     priority;
    gboolean active;
} {Prefix}ModulePrivate;

G_DEFINE_TYPE_WITH_PRIVATE({Prefix}Module, {prefix}_module, G_TYPE_OBJECT)

static void
{prefix}_module_class_init({Prefix}ModuleClass *klass)
{
    (void)klass;
}

static void
{prefix}_module_init({Prefix}Module *self)
{
    {Prefix}ModulePrivate *priv;

    priv = {prefix}_module_get_instance_private(self);
    priv->priority = {PREFIX}_MODULE_PRIORITY_NORMAL;
    priv->active = FALSE;
}

gboolean
{prefix}_module_activate({Prefix}Module *self)
{
    {Prefix}ModuleClass *klass;
    {Prefix}ModulePrivate *priv;

    g_return_val_if_fail({PREFIX}_IS_MODULE(self), FALSE);

    klass = {PREFIX}_MODULE_GET_CLASS(self);
    priv = {prefix}_module_get_instance_private(self);

    if (klass->activate && klass->activate(self)) {
        priv->active = TRUE;
        return TRUE;
    }

    return FALSE;
}

void
{prefix}_module_deactivate({Prefix}Module *self)
{
    {Prefix}ModuleClass *klass;
    {Prefix}ModulePrivate *priv;

    g_return_if_fail({PREFIX}_IS_MODULE(self));

    klass = {PREFIX}_MODULE_GET_CLASS(self);
    priv = {prefix}_module_get_instance_private(self);

    if (klass->deactivate)
        klass->deactivate(self);

    priv->active = FALSE;
}

const gchar *
{prefix}_module_get_name({Prefix}Module *self)
{
    {Prefix}ModuleClass *klass;

    g_return_val_if_fail({PREFIX}_IS_MODULE(self), NULL);

    klass = {PREFIX}_MODULE_GET_CLASS(self);
    if (klass->get_name)
        return klass->get_name(self);

    return "unnamed";
}

const gchar *
{prefix}_module_get_description({Prefix}Module *self)
{
    {Prefix}ModuleClass *klass;

    g_return_val_if_fail({PREFIX}_IS_MODULE(self), NULL);

    klass = {PREFIX}_MODULE_GET_CLASS(self);
    if (klass->get_description)
        return klass->get_description(self);

    return "";
}

void
{prefix}_module_configure(
    {Prefix}Module *self,
    gpointer       config
){
    {Prefix}ModuleClass *klass;

    g_return_if_fail({PREFIX}_IS_MODULE(self));

    klass = {PREFIX}_MODULE_GET_CLASS(self);
    if (klass->configure)
        klass->configure(self, config);
}

gint
{prefix}_module_get_priority({Prefix}Module *self)
{
    {Prefix}ModulePrivate *priv;

    g_return_val_if_fail({PREFIX}_IS_MODULE(self), 0);

    priv = {prefix}_module_get_instance_private(self);
    return priv->priority;
}

void
{prefix}_module_set_priority(
    {Prefix}Module *self,
    gint           priority
){
    {Prefix}ModulePrivate *priv;

    g_return_if_fail({PREFIX}_IS_MODULE(self));

    priv = {prefix}_module_get_instance_private(self);
    priv->priority = priority;
}

gboolean
{prefix}_module_is_active({Prefix}Module *self)
{
    {Prefix}ModulePrivate *priv;

    g_return_val_if_fail({PREFIX}_IS_MODULE(self), FALSE);

    priv = {prefix}_module_get_instance_private(self);
    return priv->active;
}
```

#### 9c. Module Manager

Generate `src/module/{project}-module-manager.h` and `.c` following the pattern
from `bacon/src/module/bacon-module-manager.h`. The manager should:

- Be a final GObject type
- Load `.so` files from a directory using `g_module_open()`
- Look for the symbol `{prefix}_module_register` which returns a `GType`
- Instantiate the module, register it, auto-detect interfaces via `g_type_is_a()`
- Provide `load_from_directory()`, `register()`, `unregister()`, `activate_all()`, `deactivate_all()`

Refer to `skill-gobject-type` for the full GObject boilerplate pattern.

#### 9d. Sample Interface — `src/interfaces/{project}-example-hook.h`

Generate a sample GInterface using conventions from `skill-gobject-interface`.

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-example-hook.h - Example hook interface for modules */

#ifndef {PREFIX}_EXAMPLE_HOOK_H
#define {PREFIX}_EXAMPLE_HOOK_H

#if !defined({PREFIX}_INSIDE) && !defined({PREFIX}_COMPILATION)
#error "Only <{project}.h> can be included directly."
#endif

#include <glib-object.h>

G_BEGIN_DECLS

#define {PREFIX}_TYPE_EXAMPLE_HOOK ({prefix}_example_hook_get_type())

G_DECLARE_INTERFACE({Prefix}ExampleHook, {prefix}_example_hook, {PREFIX}, EXAMPLE_HOOK, GObject)

/**
 * {Prefix}ExampleHookInterface:
 * @parent_iface: parent interface
 * @on_event: called when an event occurs; return %TRUE if handled
 * @padding: reserved for future methods
 *
 * Interface for modules that want to handle example events.
 */
struct _{Prefix}ExampleHookInterface
{
    GTypeInterface parent_iface;

    gboolean (*on_event) ({Prefix}ExampleHook *self,
                          const gchar        *event_name);

    /*< private >*/
    gpointer padding[3];
};

gboolean {prefix}_example_hook_on_event ({Prefix}ExampleHook *self,
                                         const gchar        *event_name);

G_END_DECLS

#endif /* {PREFIX}_EXAMPLE_HOOK_H */
```

Generate the corresponding `.c` file with `G_DEFINE_INTERFACE` and the public API wrapper.

#### 9e. Sample Module — `modules/example/`

**`modules/example/Makefile`:**
```makefile
MODULE_NAME := example
MODULE_SRC  := {project}-example-module.c

CC      ?= gcc

.PHONY: all
all: $(OUTDIR)/$(MODULE_NAME).so

$(OUTDIR)/$(MODULE_NAME).so: $(MODULE_SRC)
	$(CC) $(CFLAGS) -o $@ $^ $(LDFLAGS)
```

**`modules/example/{project}-example-module.c`:**
```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* {project}-example-module.c - Example module demonstrating the plugin system */

#include <glib-object.h>
#include <gmodule.h>
#include <{project}.h>

/* ── Type declaration ─────────────────────────────────────────────── */

#define {PREFIX}_TYPE_EXAMPLE_MODULE ({prefix}_example_module_get_type())

G_DECLARE_FINAL_TYPE({Prefix}ExampleModule, {prefix}_example_module, {PREFIX}, EXAMPLE_MODULE, {Prefix}Module)

struct _{Prefix}ExampleModule
{
    {Prefix}Module parent_instance;
};

/* ── Interface implementations ────────────────────────────────────── */

static gboolean
{prefix}_example_module_on_event(
    {Prefix}ExampleHook *hook,
    const gchar        *event_name
){
    (void)hook;
    g_message("Example module received event: %s", event_name);
    return FALSE;
}

static void
{prefix}_example_module_example_hook_init({Prefix}ExampleHookInterface *iface)
{
    iface->on_event = {prefix}_example_module_on_event;
}

/* ── GObject boilerplate ──────────────────────────────────────────── */

G_DEFINE_FINAL_TYPE_WITH_CODE({Prefix}ExampleModule, {prefix}_example_module, {PREFIX}_TYPE_MODULE,
    G_IMPLEMENT_INTERFACE({PREFIX}_TYPE_EXAMPLE_HOOK, {prefix}_example_module_example_hook_init))

static gboolean
{prefix}_example_module_activate({Prefix}Module *mod)
{
    (void)mod;
    g_message("Example module activated");
    return TRUE;
}

static void
{prefix}_example_module_deactivate({Prefix}Module *mod)
{
    (void)mod;
    g_message("Example module deactivated");
}

static const gchar *
{prefix}_example_module_get_name({Prefix}Module *mod)
{
    (void)mod;
    return "example";
}

static const gchar *
{prefix}_example_module_get_description({Prefix}Module *mod)
{
    (void)mod;
    return "Example module demonstrating the plugin system";
}

static void
{prefix}_example_module_class_init({Prefix}ExampleModuleClass *klass)
{
    {Prefix}ModuleClass *mod_class;

    mod_class = {PREFIX}_MODULE_CLASS(klass);
    mod_class->activate = {prefix}_example_module_activate;
    mod_class->deactivate = {prefix}_example_module_deactivate;
    mod_class->get_name = {prefix}_example_module_get_name;
    mod_class->get_description = {prefix}_example_module_get_description;
}

static void
{prefix}_example_module_init({Prefix}ExampleModule *self)
{
    (void)self;
}

/* ── Module entry point ───────────────────────────────────────────── */

/**
 * {prefix}_module_register:
 *
 * Entry point called by the module manager when loading this .so.
 * Returns the #GType of the module implementation.
 *
 * Returns: the #GType of #{Prefix}ExampleModule
 */
G_MODULE_EXPORT GType
{prefix}_module_register(void)
{
    return {PREFIX}_TYPE_EXAMPLE_MODULE;
}
```

---

### Step 10: Generate Test Scaffold

Create `tests/test-app.c` using patterns from `skill-gtest-scaffold`.

```c
/*
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 */

/* test-app.c - Tests for {Prefix}App */

#include <glib.h>
#include <glib-object.h>
#include "{project}.h"

static void
test_app_new(void)
{
    g_autoptr({Prefix}App) app = NULL;

    app = {prefix}_app_new();
    g_assert_nonnull(app);
    g_assert_true({PREFIX}_IS_APP(app));
}

static void
test_app_is_derivable(void)
{
    /* Verify the type is derivable (not final) */
    g_assert_true(G_TYPE_IS_DERIVABLE({PREFIX}_TYPE_APP));
}

/* ── Signal tests ─────────────────────────────────────────────────── */

static gboolean started_called = FALSE;

static void
on_started(
    {Prefix}App *app,
    gpointer    user_data
){
    (void)user_data;
    (void)app;
    started_called = TRUE;
}

static void
test_app_started_signal(void)
{
    g_autoptr({Prefix}App) app = NULL;

    app = {prefix}_app_new();
    started_called = FALSE;

    g_signal_connect(app, "started", G_CALLBACK(on_started), NULL);
    {prefix}_app_start(app);

    g_assert_true(started_called);
}

/* ── Property tests ───────────────────────────────────────────────── */

static void
test_app_running_property(void)
{
    g_autoptr({Prefix}App) app = NULL;
    gboolean running;

    app = {prefix}_app_new();

    g_object_get(app, "running", &running, NULL);
    g_assert_false(running);

    {prefix}_app_start(app);
    g_object_get(app, "running", &running, NULL);
    g_assert_true(running);

    {prefix}_app_stop(app);
    g_object_get(app, "running", &running, NULL);
    g_assert_false(running);
}

/* ── Version tests ────────────────────────────────────────────────── */

static void
test_version(void)
{
    guint major, minor, micro;
    const gchar *version_string;

    {prefix}_get_version(&major, &minor, &micro);
    g_assert_cmpuint(major, ==, {PREFIX}_VERSION_MAJOR);
    g_assert_cmpuint(minor, ==, {PREFIX}_VERSION_MINOR);
    g_assert_cmpuint(micro, ==, {PREFIX}_VERSION_MICRO);

    version_string = {prefix}_get_version_string();
    g_assert_nonnull(version_string);
}

int
main(
    int     argc,
    char  **argv
){
    g_test_init(&argc, &argv, NULL);

    g_test_add_func("/app/new", test_app_new);
    g_test_add_func("/app/is-derivable", test_app_is_derivable);
    g_test_add_func("/app/signal/started", test_app_started_signal);
    g_test_add_func("/app/property/running", test_app_running_property);
    g_test_add_func("/version/check", test_version);

    return g_test_run();
}
```

Refer to `skill-gtest-scaffold` for additional test patterns (fixtures, signals,
properties, boxed types, error checking, etc.) as the project grows.

---

### Step 11: Generate `data/` Contents (if data folder enabled)

#### `data/default-config.yaml`

```yaml
# {project} Default Configuration
# ~/.config/{project}/config.yaml

# General settings
general:
  log_level: info          # debug, info, warning, error

# Add project-specific configuration sections here
```

#### `data/default-config.c` (if config system enabled)

```c
/*
 * {project} - Default C Configuration
 *
 * Copyright (C) {year}
 * SPDX-License-Identifier: AGPL-3.0-or-later
 *
 * Install: cp default-config.c ~/.config/{project}/config.c
 * Auto-compile: {project} (compiles with content-hash caching via crispy)
 *
 * The CRISPY_PARAMS define below is optional. If present, the
 * config compiler extracts it and passes the value as extra flags
 * to gcc.
 */

/* #define CRISPY_PARAMS "-I/custom/path -lmylib" */

#include <{project}/{project}.h>

/*
 * {prefix}_config_init:
 *
 * Entry point called after YAML config is loaded.
 * Any values set here override YAML. You have full access
 * to all GObject APIs and any library you link against.
 *
 * Returns: TRUE on success, FALSE to fall back to YAML-only config.
 */
G_MODULE_EXPORT gboolean
{prefix}_config_init(void)
{
    /* Override YAML settings here using C logic */
    /* Example:
     *   if (g_file_test("/path/to/something", G_FILE_TEST_EXISTS))
     *       {prefix}_config_set_value(config, "key", "value");
     */

    return TRUE;
}
```

Create `data/examples/.gitkeep` as an empty file.

---

### Step 12: Generate `docs/` Scaffold

#### `docs/README.md`

```markdown
# {project} Documentation

## Contents

- [Architecture](architecture.md) — High-level design and directory structure
- [Building](building.md) — Build instructions and dependencies
```

#### `docs/architecture.md`

```markdown
# Architecture

## Directory Structure

| Directory | Purpose |
|-----------|---------|
| `src/` | Library source code |
| `src/core/` | Core types and logic |
| `tests/` | GTest unit tests |
| `docs/` | Documentation |
| `build/` | Compiled output (debug/release) |
```

Extend the table based on enabled features (modules/, data/, deps/, etc.).

#### `docs/building.md`

```markdown
# Building

## Prerequisites

Install build dependencies:

```bash
make install-deps
```

## Quick Start

```bash
make                    # Release build
make DEBUG=1            # Debug build
make test               # Run tests
make install PREFIX=/usr/local
```

## Build Options

| Option | Default | Description |
|--------|---------|-------------|
| `DEBUG=1` | 0 | Debug build with symbols |
| `ASAN=1` | 0 | AddressSanitizer |
| `UBSAN=1` | 0 | UndefinedBehaviorSanitizer |
| `BUILD_GIR=1` | 0 | GObject Introspection |
| `PREFIX=path` | `/usr/local` | Installation prefix |
```

---

### Step 13: Generate Root Files

#### `{project}-{api_version}.pc.in` (library and both modes)

```
prefix=@PREFIX@
libdir=@LIBDIR@
includedir=@INCLUDEDIR@

Name: {project}-@API_VERSION@
Description: {description}
Version: @VERSION@
Requires: {deps}
Libs: -L${libdir} -l{project}-@API_VERSION@
Cflags: -I${includedir}/{project}
```

#### `LICENSE`

Use the full text of the GNU Affero General Public License v3.0.

#### `README.md`

```markdown
# {project}

{description}

## Building

```bash
make install-deps       # Install build dependencies
make                    # Build (release)
make test               # Run tests
```

## License

AGPL-3.0-or-later. See [LICENSE](LICENSE) for details.
```

#### `CLAUDE.md`

Generate project-level AI agent instructions:

```markdown
# {project} — Project Instructions

## Build

```bash
make                    # Release build
make DEBUG=1            # Debug build
make DEBUG=1 ASAN=1     # AddressSanitizer
make test               # Run tests
make show-config        # Show build configuration
make check-deps         # Verify dependencies
make install-deps       # Auto-install dependencies
```

## Code Style

- C standard: `-std=gnu89` (K&R-compatible)
- Comments: `/* */` only — never `//`
- Indentation: TAB (4-space width)
- Naming: `{Prefix}PascalCase` for types, `{prefix}_snake_case()` for functions, `{PREFIX}_UPPER_CASE` for macros
- Memory: use `g_autoptr()`, `g_steal_pointer()` — avoid manual ref/unref where possible
- Headers: include only `<{project}.h>` — individual headers have `{PREFIX}_INSIDE` guards
- GObject Introspection: all public API must have GTK-Doc comments with transfer/nullable annotations

## Key Files

- `src/{project}.h` — Umbrella header (include only this)
- `src/{project}-types.h` — Forward declarations
- `src/{project}-error.h` — Error domain and codes
- `src/core/{project}-app.h` — Main application type
- `config.mk` — Build configuration
- `rules.mk` — Build rules
- `Makefile` — Build orchestration

## Testing

- Framework: GLib GTest (`g_test_*`)
- Test files: `tests/test-*.c`
- Run: `make test` or `LD_LIBRARY_PATH=build/debug ./build/debug/test-app`
```

#### `.gitignore`

```
build/
src/{project}-version.h
*.o
*.d
*.so
*.a
*.pc
```

#### `.gitmodules` (if config system enabled)

```
[submodule "deps/crispy"]
	path = deps/crispy
	url = git@gitlab.com:zachpodbielniak/crispy.git
[submodule "deps/yaml-glib"]
	path = deps/yaml-glib
	url = git@gitlab.com:copyleft-games/yaml-glib
```

---

### Step 13b: Generate Container Support (if enabled)

#### `Containerfile`

```dockerfile
# Stage 1: Builder
FROM registry.fedoraproject.org/fedora-minimal:43 AS builder

RUN microdnf install -y \
    gcc make pkgconf-pkg-config \
    glib2-devel \
    && microdnf clean all

WORKDIR /build
COPY . .

RUN make -j$(nproc) all && \
    make install DESTDIR=/install PREFIX=/usr

# Stage 2: Runtime
FROM registry.fedoraproject.org/fedora-minimal:43

RUN microdnf install -y \
    glib2 \
    && microdnf clean all

COPY --from=builder /install /

# Refresh shared library cache
RUN ldconfig

ENTRYPOINT ["{project}"]
```

Extend the `microdnf install` lines to include all runtime dependencies.

#### `.containerignore`

```
build/
.git/
*.o
*.d
```

---

### Step 14: Initialize Git and Submodules

```bash
cd {project}
git init
git checkout -b master

# If config system enabled, add submodules
git submodule add git@gitlab.com:zachpodbielniak/crispy.git deps/crispy
git submodule add git@gitlab.com:copyleft-games/yaml-glib deps/yaml-glib

git add -A
git commit -m "feat: initial project scaffold"
```

If a git remote was provided:
```bash
git remote add origin {remote_url}
```

---

## Output Format

### Library-only mode generates:

```
{project}/
├── src/{project}.h
├── src/{project}-types.h
├── src/{project}-types.c
├── src/{project}-error.h
├── src/{project}-version.h.in
├── src/core/{project}-app.h
├── src/core/{project}-app.c
├── tests/test-app.c
├── docs/README.md
├── docs/architecture.md
├── docs/building.md
├── config.mk
├── rules.mk
├── Makefile
├── {project}-{api_version}.pc.in
├── LICENSE
├── README.md
├── CLAUDE.md
└── .gitignore
```

### Both mode + modules + config generates:

```
{project}/
├── src/{project}.h
├── src/{project}-types.h
├── src/{project}-types.c
├── src/{project}-error.h
├── src/{project}-version.h.in
├── src/main.c
├── src/core/{project}-app.h
├── src/core/{project}-app.c
├── src/interfaces/{project}-example-hook.h
├── src/interfaces/{project}-example-hook.c
├── src/module/{project}-module.h
├── src/module/{project}-module.c
├── src/module/{project}-module-manager.h
├── src/module/{project}-module-manager.c
├── modules/example/Makefile
├── modules/example/{project}-example-module.c
├── tests/test-app.c
├── deps/crispy/                (submodule)
├── deps/yaml-glib/             (submodule)
├── data/default-config.yaml
├── data/default-config.c
├── data/examples/.gitkeep
├── docs/README.md
├── docs/architecture.md
├── docs/building.md
├── config.mk
├── rules.mk
├── Makefile
├── {project}-{api_version}.pc.in
├── .gitmodules
├── LICENSE
├── README.md
├── CLAUDE.md
└── .gitignore
```

---

## Examples

### Example 1: Library-only project

**Input:** "Create a new GObject library called `libhyacinth` with prefix `HY`, API version 1.0,
depends on glib-2.0 and gobject-2.0, no modules, no config system."

**Parameters:**
- Project name: `libhyacinth`
- Prefix: `HY` / `Hy` / `hy`
- Build mode: `library`
- API version: `1.0`
- Deps: `glib-2.0 gobject-2.0`
- Modules: no
- Config: no

**Result:** Creates a project with `libhyacinth-1.0.so`, `libhyacinth-1.0.a`,
`libhyacinth-1.0.pc`, umbrella header `libhyacinth.h`, one `HyApp` type in
`src/core/`, and a test file. No `main.c`, no `deps/`, no `data/`.

### Example 2: Full application with modules and config

**Input:** "Create a project called `falcon` with prefix `FALCON`, build both library and
executable, with module system and config system, depends on glib-2.0, gobject-2.0,
gio-2.0, and gmodule-2.0."

**Parameters:**
- Project name: `falcon`
- Prefix: `FALCON` / `Falcon` / `falcon`
- Build mode: `both`
- API version: `1.0`
- Deps: `glib-2.0 gobject-2.0 gio-2.0 gmodule-2.0`
- Modules: yes
- Config: yes

**Result:** Full project with `libfalcon-1.0.so`, `falcon` executable, module system
(`FalconModule` base class, `FalconModuleManager`, example hook interface, example module
in `modules/example/`), config system (`deps/crispy`, `deps/yaml-glib`,
`data/default-config.yaml`, `data/default-config.c`), and all infrastructure files.

---

## Constraints

### Code Style
- Never use `//` comments — always `/* */`
- Always use gnu89 (`-std=gnu89`), TAB indentation (4-space width)
- Default git branch is always `master`
- License is always AGPL-3.0-or-later unless the user explicitly specifies otherwise
- Always include the `{PREFIX}_INSIDE` / `{PREFIX}_COMPILATION` header guard pattern
- All public headers must use the `#if !defined(...INSIDE) && !defined(...COMPILATION)` guard
- Private headers (suffixed `-private.h`) are NOT installed

### GObject Type Design
- **Prefer derivable types** (`G_DECLARE_DERIVABLE_TYPE` with `G_DEFINE_TYPE_WITH_PRIVATE`) for any type that others may need to extend — this includes base classes, core application types, and service types. Use `G_DECLARE_FINAL_TYPE` only for concrete leaf types (e.g., a specific module implementation, a specific command handler).
- **Use GInterfaces** for cross-cutting behavior: if two or more unrelated types need the same capability, define a GInterface — do not force a shared base class. Interfaces are the primary extensibility mechanism for the module system.
- **Use GObject signals** on any type that emits events. Signals decouple the emitter from consumers. Define them in `class_init` with `g_signal_new()` and include class handler slots in the class struct for subclass overrides.
- **Use boxed types** (`G_DEFINE_BOXED_TYPE`) for lightweight value types: messages, tokens, results, configuration entries, keys. Place them in `src/boxed/`. Boxed types are cheaper than GObject and work with `g_autoptr()`, GValue, signals, and GObject Introspection.
- **Use GObject properties** for introspectable configuration on types. Prefer `g_param_spec_*` with `G_PARAM_READABLE`/`G_PARAM_READWRITE` and `G_PARAM_STATIC_STRINGS`. Notify via `g_object_notify_by_pspec()`.
- **ABI stability**: All derivable class structs must include `gpointer padding[7]`. New virtual methods consume padding from the end (padding[6] first, then [5], etc.) — this lets the library add virtual methods without breaking existing compiled subclasses.
- **All enum types used in signals, properties, or GIR** should be registered with `G_DEFINE_ENUM_TYPE` or equivalent, not left as plain C enums.

### Build System
- No wildcards in Makefile source file lists — list each `.c` file explicitly
- Always use `$(DESTDIR)` prefix in installation targets
- Always auto-detect lib vs lib64 for LIBDIR
- Always use `Containerfile` (not `Dockerfile`), `podman` (not `docker`)
- Never include the generated `{project}-version.h` in the repo — only the `.h.in` template
- Git submodules always go in `deps/`
- Module entry point is always `G_MODULE_EXPORT GType {prefix}_module_register(void)`
- Always include `--version` and `--license` CLI options for executables
- Always include `-h`/`--help` (automatic via GOptionContext)

### Related Skills
- Reference `skill-gobject-type` for full derivable, final, and boxed type templates
- Reference `skill-gobject-interface` for full GInterface templates
- Reference `skill-gtest-scaffold` for additional test patterns (signal testing, property testing, boxed type testing)
- Reference `skill-makefile-template` for Makefile convention details
