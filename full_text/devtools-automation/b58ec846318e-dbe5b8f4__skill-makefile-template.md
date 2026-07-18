---
name: skill-makefile-template
description: >
  Generate the three-file Makefile pattern (config.mk / rules.mk / Makefile)
  for GLib/GObject C projects. Trigger when creating build systems, new projects,
  or Makefile infrastructure for C libraries, executables, or module systems.
---

# Skill: Three-File Makefile Template Generator

Generates the exact three-file Makefile pattern used in bacon, libreclaw, and gst: `config.mk` (project configuration and compiler flags), `rules.mk` (generic compilation and installation rules), and `Makefile` (source lists and high-level targets). All output uses GNU Make and GCC with pkg-config integration.

## When to Use

- When creating a new GLib/GObject C project from scratch
- When the user says "create a build system", "add a Makefile", or "set up the project"
- When migrating a single-file Makefile to the three-file pattern
- When adding library, test, or module build support to an existing project

## Instructions

### 1. Gather Requirements

| Parameter | Required | Default | Description |
|-----------|----------|---------|-------------|
| **Project name** | Yes | — | e.g., `bacon`, `gst`, `my-project` |
| **Library name** | No | `lib{project}-1.0` | Shared library name |
| **API version** | No | `1.0` | Library API version |
| **Build type** | No | both | `library`, `executable`, or `both` |
| **pkg-config deps** | Yes | `glib-2.0 gobject-2.0` | Space-separated package names |
| **Optional deps** | No | none | Conditional features (e.g., Wayland, MCP) |
| **Bundled deps** | No | none | Deps built from source in `deps/` |
| **Module support** | No | no | Whether to build `.so` plugin modules |
| **GIR support** | No | no | GObject Introspection generation |
| **Test support** | No | yes | Build and run GTest binaries |

### 2. Generate config.mk

This file contains ALL project configuration: version, paths, compiler flags, dependency detection, and build options.

```makefile
# ============================================================================
# config.mk — Project configuration for {project}
# ============================================================================

# Version
VERSION_MAJOR := 0
VERSION_MINOR := 1
VERSION_MICRO := 0
VERSION       := $(VERSION_MAJOR).$(VERSION_MINOR).$(VERSION_MICRO)
API_VERSION   := 1.0

# Project identity
PROJECT_NAME := {project}
LIB_NAME     := {project}-$(API_VERSION)

# ---- Installation directories ----

PREFIX     ?= /usr/local
BINDIR     := $(PREFIX)/bin
INCLUDEDIR := $(PREFIX)/include
DATADIR    := $(PREFIX)/share

# Auto-detect lib vs lib64
ifeq ($(shell [ -d /usr/lib64 ] && echo yes),yes)
LIBDIR := $(PREFIX)/lib64
else
LIBDIR := $(PREFIX)/lib
endif

PKGCONFIGDIR := $(LIBDIR)/pkgconfig
MODULEDIR    := $(LIBDIR)/$(PROJECT_NAME)/modules

# ---- Build directories ----

BUILDDIR       := build
DEBUG          ?= 0

ifeq ($(DEBUG),1)
BUILD_TYPE     := debug
else
BUILD_TYPE     := release
endif

OUTDIR         := $(BUILDDIR)/$(BUILD_TYPE)
OBJDIR         := $(OUTDIR)/obj

# ---- Build options ----

ASAN           ?= 0
UBSAN          ?= 0
BUILD_TESTS    ?= 1
BUILD_MODULES  ?= 1
BUILD_GIR      ?= 0

# ---- Compiler setup ----

CC         := gcc
AR         := ar
PKG_CONFIG := pkg-config
INSTALL    := install
MKDIR_P    := mkdir -p

# ---- C standard and warnings ----

CSTD     := -std=gnu89
WARNINGS := -Wall -Wextra -Wno-unused-parameter -Wformat=2 -Wshadow

CFLAGS_BASE := $(CSTD) $(WARNINGS) -fPIC \
	-D$(shell echo $(PROJECT_NAME) | tr '[:lower:]-' '[:upper:]_')_COMPILATION \
	-DVERSION=\"$(VERSION)\"

# ---- Debug vs release ----

ifeq ($(DEBUG),1)
CFLAGS_BUILD := -g -O0 -DDEBUG
else
CFLAGS_BUILD := -O2 -DNDEBUG
endif

# ---- Sanitizers ----

ifeq ($(ASAN),1)
CFLAGS_BUILD += -fsanitize=address -fno-omit-frame-pointer
LDFLAGS      += -fsanitize=address
endif

ifeq ($(UBSAN),1)
CFLAGS_BUILD += -fsanitize=undefined
LDFLAGS      += -fsanitize=undefined
endif

# ---- Dependencies (pkg-config) ----

DEPS_REQUIRED := glib-2.0 gobject-2.0 gio-2.0

DEPS_CFLAGS := $(shell $(PKG_CONFIG) --cflags $(DEPS_REQUIRED))
DEPS_LIBS   := $(shell $(PKG_CONFIG) --libs $(DEPS_REQUIRED))

# ---- Bundled dependencies (if any) ----
# Example:
# YAMLGLIB_DIR    := deps/yaml-glib
# YAMLGLIB_CFLAGS := -I$(YAMLGLIB_DIR)/src
# YAMLGLIB_STATIC := $(YAMLGLIB_DIR)/build/libyaml-glib.a

# ---- Include paths ----

CFLAGS_INC := -Isrc

# ---- Final flags ----

CFLAGS  := $(CFLAGS_BASE) $(CFLAGS_BUILD) $(CFLAGS_INC) $(DEPS_CFLAGS)
LDFLAGS += $(DEPS_LIBS)

# ---- Library output names ----

LIB_STATIC     := $(OUTDIR)/lib$(LIB_NAME).a
LIB_SHARED_FULL := $(OUTDIR)/lib$(LIB_NAME).so.$(VERSION)
LIB_SHARED_MAJOR := $(OUTDIR)/lib$(LIB_NAME).so.$(VERSION_MAJOR)
LIB_SHARED      := $(OUTDIR)/lib$(LIB_NAME).so

LDFLAGS_SHARED := -shared -Wl,-soname,lib$(LIB_NAME).so.$(VERSION_MAJOR)

# ---- Module compilation flags ----

MODULE_CFLAGS := $(CFLAGS) -I$(CURDIR)/src
MODULE_LDFLAGS := -shared -L$(CURDIR)/$(OUTDIR) -l$(LIB_NAME) -Wl,-rpath,'$$ORIGIN/..'

# ---- GObject Introspection ----

ifeq ($(BUILD_GIR),1)
GIR_SCANNER  := g-ir-scanner
GIR_COMPILER := g-ir-compiler
GIR_NAMESPACE := $(shell echo $(PROJECT_NAME) | sed 's/.*/\u&/')
GIR_VERSION   := $(VERSION_MAJOR).$(VERSION_MINOR)
GIRDIR        := $(DATADIR)/gir-1.0
TYPELIBDIR    := $(LIBDIR)/girepository-1.0
endif

# ---- Distro package names (for install-deps target) ----

FEDORA_DEPS := gcc make pkgconf-pkg-config glib2-devel
UBUNTU_DEPS := gcc make pkg-config libglib2.0-dev
ARCH_DEPS   := gcc make pkgconf glib2
```

**Key conventions:**
- `VERSION_MAJOR/MINOR/MICRO` as separate variables, reconstructed into `VERSION`
- Auto-detect `lib` vs `lib64` for LIBDIR
- `DEBUG` flag selects build type (debug/release)
- Sanitizers are opt-in via `ASAN=1` / `UBSAN=1`
- `CFLAGS` composed from Base + Build + Includes + Dependencies
- Module flags use `$(CURDIR)` for absolute paths (needed for out-of-dir builds)
- `-D{PROJECT}_COMPILATION` added automatically (used by header guards)

### 3. Generate rules.mk

This file contains generic compilation rules, library creation, and installation targets.

```makefile
# ============================================================================
# rules.mk — Generic build rules for {project}
# ============================================================================

# ---- Directory creation ----

$(OBJDIR):
	@$(MKDIR_P) $(OBJDIR)

# ---- Pattern rules (one per source subdirectory) ----

$(OBJDIR)/%.o: src/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/core/%.o: src/core/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/interfaces/%.o: src/interfaces/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

$(OBJDIR)/tests/%.o: tests/%.c | $(OBJDIR)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(CFLAGS) -MMD -MP -c $< -o $@

# ---- Static library ----

$(LIB_STATIC): $(LIB_OBJS)
	@$(MKDIR_P) $(dir $@)
	$(AR) rcs $@ $^

# ---- Shared library ----

$(LIB_SHARED_FULL): $(LIB_OBJS)
	@$(MKDIR_P) $(dir $@)
	$(CC) $(LDFLAGS_SHARED) -o $@ $^ $(LDFLAGS)
	cd $(OUTDIR) && ln -sf $(notdir $(LIB_SHARED_FULL)) $(notdir $(LIB_SHARED_MAJOR))
	cd $(OUTDIR) && ln -sf $(notdir $(LIB_SHARED_FULL)) $(notdir $(LIB_SHARED))

# ---- Generated version header ----

src/{project}-version.h: src/{project}-version.h.in config.mk
	sed -e 's/@VERSION_MAJOR@/$(VERSION_MAJOR)/g' \
	    -e 's/@VERSION_MINOR@/$(VERSION_MINOR)/g' \
	    -e 's/@VERSION_MICRO@/$(VERSION_MICRO)/g' \
	    -e 's/@VERSION@/$(VERSION)/g' \
	    $< > $@

# ---- pkg-config file ----

$(OUTDIR)/$(LIB_NAME).pc: {project}.pc.in config.mk
	@$(MKDIR_P) $(dir $@)
	sed -e 's|@PREFIX@|$(PREFIX)|g' \
	    -e 's|@LIBDIR@|$(LIBDIR)|g' \
	    -e 's|@INCLUDEDIR@|$(INCLUDEDIR)|g' \
	    -e 's|@VERSION@|$(VERSION)|g' \
	    -e 's|@LIB_NAME@|$(LIB_NAME)|g' \
	    -e 's|@DEPS_REQUIRED@|$(DEPS_REQUIRED)|g' \
	    $< > $@

# ---- Installation ----

install-lib: $(LIB_SHARED_FULL) $(LIB_STATIC)
	$(MKDIR_P) $(DESTDIR)$(LIBDIR)
	$(INSTALL) -m 755 $(LIB_SHARED_FULL) $(DESTDIR)$(LIBDIR)/
	cd $(DESTDIR)$(LIBDIR) && ln -sf $(notdir $(LIB_SHARED_FULL)) $(notdir $(LIB_SHARED_MAJOR))
	cd $(DESTDIR)$(LIBDIR) && ln -sf $(notdir $(LIB_SHARED_FULL)) $(notdir $(LIB_SHARED))
	$(INSTALL) -m 644 $(LIB_STATIC) $(DESTDIR)$(LIBDIR)/

install-headers:
	$(MKDIR_P) $(DESTDIR)$(INCLUDEDIR)/$(PROJECT_NAME)-$(API_VERSION)/$(PROJECT_NAME)
	$(INSTALL) -m 644 $(PUBLIC_HEADERS) \
		$(DESTDIR)$(INCLUDEDIR)/$(PROJECT_NAME)-$(API_VERSION)/$(PROJECT_NAME)/

install-pc: $(OUTDIR)/$(LIB_NAME).pc
	$(MKDIR_P) $(DESTDIR)$(PKGCONFIGDIR)
	$(INSTALL) -m 644 $(OUTDIR)/$(LIB_NAME).pc $(DESTDIR)$(PKGCONFIGDIR)/

install-bin: $(OUTDIR)/$(PROJECT_NAME)
	$(MKDIR_P) $(DESTDIR)$(BINDIR)
	$(INSTALL) -m 755 $(OUTDIR)/$(PROJECT_NAME) $(DESTDIR)$(BINDIR)/

install: install-lib install-headers install-pc install-bin

# ---- Uninstall ----

uninstall:
	rm -f $(DESTDIR)$(LIBDIR)/lib$(LIB_NAME).*
	rm -f $(DESTDIR)$(PKGCONFIGDIR)/$(LIB_NAME).pc
	rm -rf $(DESTDIR)$(INCLUDEDIR)/$(PROJECT_NAME)-$(API_VERSION)
	rm -f $(DESTDIR)$(BINDIR)/$(PROJECT_NAME)

# ---- Clean ----

clean:
	rm -rf $(BUILDDIR)/$(BUILD_TYPE)

clean-all:
	rm -rf $(BUILDDIR)

.PHONY: install install-lib install-headers install-pc install-bin uninstall clean clean-all
```

**Key conventions:**
- One pattern rule per source subdirectory (allows per-directory compilation)
- `-MMD -MP` flags generate dependency tracking files
- Static library via `ar rcs`, shared via `gcc -shared -Wl,-soname,...`
- Shared library creates soname and unversioned symlinks
- Version header generated from `.h.in` template via `sed`
- Installation uses `$(DESTDIR)` prefix for packaging
- Clean only removes current build type; `clean-all` removes everything

### 4. Generate Makefile

This file defines source lists, includes the other two, and provides high-level targets.

```makefile
# ============================================================================
# Makefile — {project}
# ============================================================================

include config.mk

# ---- Source files (explicit list, NOT wildcard) ----

LIB_SRCS := \
	src/core/{project}-app.c \
	src/core/{project}-config.c \
	src/interfaces/{project}-runnable.c

MAIN_SRC := src/main.c

# ---- Object file mapping ----

LIB_OBJS  := $(patsubst src/%.c,$(OBJDIR)/%.o,$(LIB_SRCS))
MAIN_OBJ  := $(OBJDIR)/main.o

# ---- Public headers (for installation and GIR) ----

PUBLIC_HEADERS := \
	src/{project}.h \
	src/core/{project}-app.h \
	src/core/{project}-config.h \
	src/interfaces/{project}-runnable.h

# ---- Test sources ----

ifeq ($(BUILD_TESTS),1)
TEST_SRCS := \
	tests/test-app.c \
	tests/test-config.c

TEST_BINS := $(patsubst tests/%.c,$(OUTDIR)/%,$(TEST_SRCS))
endif

# ---- Module directories ----

ifeq ($(BUILD_MODULES),1)
MODULE_DIRS := $(wildcard modules/*)
endif

# ---- All dependency files ----

ALL_DEPS := $(LIB_OBJS:.o=.d) $(MAIN_OBJ:.o=.d)

# ---- Include generic rules ----

include rules.mk

# ---- High-level targets ----

.PHONY: all lib $(PROJECT_NAME) modules test check-deps help

all: lib $(PROJECT_NAME)
ifeq ($(BUILD_MODULES),1)
all: modules
endif

lib: src/{project}-version.h $(LIB_STATIC) $(LIB_SHARED_FULL) $(OUTDIR)/$(LIB_NAME).pc

$(PROJECT_NAME): lib $(OUTDIR)/$(PROJECT_NAME)

$(OUTDIR)/$(PROJECT_NAME): $(MAIN_OBJ) $(LIB_SHARED_FULL)
	$(CC) -o $@ $(MAIN_OBJ) -L$(OUTDIR) -l$(LIB_NAME) $(LDFLAGS) -Wl,-rpath,'$$ORIGIN'

# ---- Modules ----

ifeq ($(BUILD_MODULES),1)
modules: lib
	@$(MKDIR_P) $(OUTDIR)/modules
	@for dir in $(MODULE_DIRS); do \
		$(MAKE) -C $$dir \
			OUTDIR=$(abspath $(OUTDIR)/modules) \
			LIBDIR=$(abspath $(OUTDIR)) \
			CC='$(CC)' \
			CFLAGS='$(MODULE_CFLAGS)' \
			LDFLAGS='$(MODULE_LDFLAGS)'; \
	done
endif

# ---- Tests ----

ifeq ($(BUILD_TESTS),1)
TEST_LDFLAGS := -L$(OUTDIR) -l$(LIB_NAME) $(LDFLAGS) -Wl,-rpath,$(OUTDIR)

$(OUTDIR)/test-%: $(OBJDIR)/tests/test-%.o $(LIB_SHARED_FULL)
	$(CC) -o $@ $< $(TEST_LDFLAGS)

test: lib $(TEST_BINS)
	@echo "Running tests..."
	@failures=0; \
	for t in $(TEST_BINS); do \
		echo "  $$(basename $$t)"; \
		LD_LIBRARY_PATH=$(OUTDIR) $$t || failures=$$((failures + 1)); \
	done; \
	if [ $$failures -gt 0 ]; then \
		echo ""; \
		echo "$$failures test suite(s) FAILED"; \
		exit 1; \
	fi; \
	echo ""; \
	echo "All tests passed."
endif

# ---- Dependency tracking ----

SKIP_DEP_CHECK := clean clean-all help
ifeq ($(filter $(SKIP_DEP_CHECK),$(MAKECMDGOALS)),)
-include $(ALL_DEPS)
endif

# ---- Help ----

help:
	@echo "$(PROJECT_NAME) $(VERSION) — build targets:"
	@echo ""
	@echo "  make              Build library + binary"
	@echo "  make lib          Build library only"
	@echo "  make modules      Build plugin modules"
	@echo "  make test         Build and run tests"
	@echo "  make install      Install to $(PREFIX)"
	@echo "  make uninstall    Remove installed files"
	@echo "  make clean        Remove $(BUILD_TYPE) build"
	@echo "  make clean-all    Remove all builds"
	@echo ""
	@echo "Options:"
	@echo "  DEBUG=1           Debug build (-g -O0)"
	@echo "  ASAN=1            Address sanitizer"
	@echo "  UBSAN=1           Undefined behavior sanitizer"
	@echo "  PREFIX=/path      Installation prefix (default: /usr/local)"
```

**Key conventions:**
- Source files are hardcoded lists (never `wildcard`) for build control
- `include config.mk` first, source lists, then `include rules.mk`
- High-level targets: `all`, `lib`, `$(PROJECT_NAME)`, `modules`, `test`
- Modules invoked via `$(MAKE) -C` with absolute paths for `OUTDIR`, `LIBDIR`, `CFLAGS`, `LDFLAGS`
- Test binaries link against shared library with `-Wl,-rpath,$(OUTDIR)`
- Tests run with `LD_LIBRARY_PATH` set
- Dependency `.d` files conditionally included (skipped during clean)
- Tests count failures and report summary

### 5. Module Makefile Template

For plugin modules that get built as shared objects:

```makefile
# modules/{module-name}/Makefile

MODULE_NAME := {module-name}
MODULE_SRC  := {module-name}-module.c

CC      ?= gcc
CFLAGS  ?= -std=gnu89 -Wall -Wextra -fPIC
LDFLAGS ?= -shared
OUTDIR  ?= .

.PHONY: all clean

all: $(OUTDIR)/$(MODULE_NAME).so

$(OUTDIR)/$(MODULE_NAME).so: $(MODULE_SRC)
	$(CC) $(CFLAGS) $(LDFLAGS) -o $@ $^

clean:
	rm -f $(OUTDIR)/$(MODULE_NAME).so
```

### 6. Conditional Feature Pattern

For optional dependencies (e.g., Wayland support, MCP integration):

```makefile
# In config.mk:
BUILD_WAYLAND ?= 0

ifeq ($(BUILD_WAYLAND),1)
WAYLAND_DEPS := wayland-client wayland-cursor xkbcommon
WAYLAND_CHECK := $(shell $(PKG_CONFIG) --exists $(WAYLAND_DEPS) 2>/dev/null && echo yes)
ifeq ($(WAYLAND_CHECK),yes)
WAYLAND_AVAILABLE := 1
CFLAGS_BASE += -DHAVE_WAYLAND=1
DEPS_CFLAGS += $(shell $(PKG_CONFIG) --cflags $(WAYLAND_DEPS))
DEPS_LIBS   += $(shell $(PKG_CONFIG) --libs $(WAYLAND_DEPS))
endif
endif

# In Makefile:
ifeq ($(WAYLAND_AVAILABLE),1)
LIB_SRCS += \
	src/wayland/wl-window.c \
	src/wayland/wl-seat.c
endif
```

## Output Format

Three files at the project root:

1. `config.mk` — Project configuration, flags, dependency detection
2. `rules.mk` — Generic compilation rules, installation targets
3. `Makefile` — Source lists, high-level targets, module/test orchestration

Optionally:
- `modules/{name}/Makefile` — Per-module build file
- `{project}.pc.in` — pkg-config template
- `src/{project}-version.h.in` — Version header template

## Examples

**Input:** "Create a build system for a new GLib project called `my-tool` that builds a shared library and executable, depends on glib-2.0, gobject-2.0, and json-glib-1.0, and has a test suite"

**Output:**
- `config.mk` with `DEPS_REQUIRED := glib-2.0 gobject-2.0 json-glib-1.0`
- `rules.mk` with compilation rules for `src/`, `src/core/`, `tests/`
- `Makefile` with `LIB_SRCS`, `MAIN_SRC`, `TEST_SRCS`, targets for `all`, `lib`, `my-tool`, `test`

## Constraints

- Never use wildcards for source file lists (`$(wildcard src/*.c)`) — always explicit lists
- Never hardcode absolute paths in config.mk — use `$(CURDIR)` or relative paths
- Never omit `-fPIC` for library compilation
- Never skip the soname/symlink creation for shared libraries
- Always use `$(DESTDIR)` prefix in installation targets (for packaging)
- Always auto-detect lib vs lib64 for LIBDIR
- Always use `-MMD -MP` for dependency tracking
- Always provide `clean` and `clean-all` targets
