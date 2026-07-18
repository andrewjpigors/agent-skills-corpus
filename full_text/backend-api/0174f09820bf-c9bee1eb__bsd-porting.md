---
name: bsd-porting
description: >-
  Ports software from Linux to BSD systems with syscall and API mapping. Use when adapting
  Linux-specific code to run on OpenBSD, FreeBSD, or other BSD variants.
license: MIT
metadata:
  version: 1.0.0
  author: Original skill
allowed-tools: Read Grep Glob AskUserQuestion
---

# BSD Porting

Port Linux software to BSD without breaking existing functionality. You'll map Linux-specific syscalls and APIs to BSD equivalents.

## Quick Start

Before diving into specific API mappings, scan the codebase to understand the scope. Then **use `AskUserQuestion`** to confirm: "I found [X Linux-specific patterns] in [Y files]. Which BSD target are you porting to — OpenBSD, FreeBSD, or NetBSD? And do you want full portability or just one platform?"

**Most common changes:**
1. **epoll/inotify → kqueue** — Event notification and file monitoring
2. **Linux-specific headers** — Add BSD alternatives
3. **GNU make → BSD make** — Build system syntax
4. **glibc extensions → BSD libc** — String functions, etc.

Check `config.h` or autotools output for Linux-specific defines. Don't skip this step.

## When to Use This Skill

- Adapting Linux-specific software to run on OpenBSD, FreeBSD, or NetBSD
- Replacing epoll/inotify/signalfd with kqueue equivalents
- Migrating build systems from GNU make to BSD make or CMake
- Mapping glibc extensions (getline, asprintf, strsep) to BSD libc equivalents

## Event Notification: epoll → kqueue

### epoll (Linux)

```c
int epfd = epoll_create1(0);
struct epoll_event ev;
ev.events = EPOLLIN;
ev.data.fd = sockfd;
epoll_ctl(epfd, EPOLL_CTL_ADD, sockfd, &ev);

struct epoll_event events[10];
int nfds = epoll_wait(epfd, events, 10, -1);
for (int i = 0; i < nfds; i++) {
    if (events[i].events & EPOLLIN) {
        // Handle read
    }
}
```

### kqueue (BSD)

```c
int kq = kqueue();
struct kevent kev;
EV_SET(&kev, sockfd, EVFILT_READ, EV_ADD, 0, 0, NULL);
kevent(kq, &kev, 1, NULL, 0, NULL);

struct kevent events[10];
int nev = kevent(kq, NULL, 0, events, 10, NULL);
for (int i = 0; i < nev; i++) {
    if (events[i].filter == EVFILT_READ) {
        // Handle read
    }
}
```

### Mapping

| epoll | kqueue |
|-------|--------|
| `EPOLLIN` | `EVFILT_READ` |
| `EPOLLOUT` | `EVFILT_WRITE` |
| `EPOLLERR` | `EV_ERROR` flag |
| `EPOLLHUP` | `EV_EOF` flag |
| `EPOLLET` (edge-triggered) | `EV_CLEAR` |
| `EPOLLONESHOT` | `EV_ONESHOT` |

## File Monitoring: inotify → kqueue EVFILT_VNODE

### inotify (Linux)

```c
int ifd = inotify_init();
int wd = inotify_add_watch(ifd, "/path/to/file", IN_MODIFY | IN_CREATE);

struct inotify_event event;
read(ifd, &event, sizeof(event));
if (event.mask & IN_MODIFY) {
    // File modified
}
```

### kqueue EVFILT_VNODE (BSD)

```c
int fd = open("/path/to/file", O_RDONLY);
int kq = kqueue();

struct kevent kev;
EV_SET(&kev, fd, EVFILT_VNODE,
       EV_ADD | EV_CLEAR,
       NOTE_WRITE | NOTE_DELETE,
       0, NULL);
kevent(kq, &kev, 1, NULL, 0, NULL);

struct kevent event;
kevent(kq, NULL, 0, &event, 1, NULL);
if (event.fflags & NOTE_WRITE) {
    // File modified
}
```

### Mapping

| inotify | kqueue |
|---------|--------|
| `IN_MODIFY` | `NOTE_WRITE` |
| `IN_ATTRIB` | `NOTE_ATTRIB` |
| `IN_DELETE` | `NOTE_DELETE` |
| `IN_CREATE` | `NOTE_WRITE` on directory |
| `IN_MOVED_FROM` | `NOTE_RENAME` |
| `IN_MOVED_TO` | `NOTE_WRITE` |

## Header Files

### Linux-specific headers

```c
#include <sys/epoll.h>    // epoll
#include <sys/inotify.h>  // inotify
#include <linux/limits.h> // PATH_MAX
#include <endian.h>       // htole32, etc.
#include <error.h>        // error()
```

### BSD equivalents

```c
#include <sys/event.h>    // kqueue
// inotify → use kqueue EVFILT_VNODE
#include <sys/syslimits.h> // PATH_MAX (or use limits.h)
#include <sys/endian.h>   // htole32 on FreeBSD
#include <machine/endian.h> // on OpenBSD
#include <err.h>          // err(), warn() - BSD standard
```

### Portable approach

```c
#if defined(__linux__)
#include <linux/limits.h>
#include <endian.h>
#elif defined(__OpenBSD__) || defined(__FreeBSD__) || defined(__NetBSD__)
#include <sys/syslimits.h>
#include <machine/endian.h>  // OpenBSD
// or <sys/endian.h> for FreeBSD
#else
#include <limits.h>
#endif
```

## String Functions

### glibc extensions

```c
// GNU-specific functions not in POSIX
strchrnul()    // Find char or end of string
mempcpy()      // Like memcpy but returns end pointer
rawmemchr()    // Like memchr without length limit
```

### BSD alternatives

```c
// strchrnul replacement
static inline char *strchrnul(const char *s, int c) {
    char *p = strchr(s, c);
    return p ? p : (char *)s + strlen(s);
}

// mempcpy replacement
static inline void *mempcpy(void *dst, const void *src, size_t n) {
    return (char *)memcpy(dst, src, n) + n;
}

// rawmemchr - just use memchr with known length
```

## Build System: GNU make → BSD make

### GNU make features

```makefile
# GNU make supports +=, ?=, pattern rules with %
CFLAGS += -Wall
LIBS ?= -lpthread

%.o: %.c
	$(CC) -c $< -o $@
```

### BSD make

```makefile
# BSD make uses different syntax
CFLAGS = -Wall ${EXTRA_CFLAGS}
LIBS ?= -lpthread

.SUFFIXES: .c .o
.c.o:
	${CC} -c ${CFLAGS} $< -o $@
```

### Portable Makefile

```makefile
# Works on both GNU and BSD make
CC ?= cc
CFLAGS = -Wall -Wextra
LDFLAGS =

all: program

program: main.o util.o
	${CC} ${LDFLAGS} -o $@ main.o util.o

.c.o:
	${CC} ${CFLAGS} -c $<

clean:
	rm -f *.o program
```

## Library Differences

### Threading

**Linux (glibc):**
```c
#include <pthread.h>
// Link with -lpthread
```

**BSD:**
```c
#include <pthread.h>
// Threading built into libc, no -lpthread needed
```

### Realtime

**Linux:**
```c
#include <time.h>
clock_gettime(CLOCK_MONOTONIC, &ts);
// Link with -lrt on old systems
```

**BSD:**
```c
#include <time.h>
clock_gettime(CLOCK_MONOTONIC, &ts);
// No -lrt needed
```

## OpenBSD Security Features

When porting to OpenBSD, you'll want to add security features:

### pledge

Restrict syscall access:

```c
#ifdef __OpenBSD__
#include <unistd.h>

// After initialization, drop privileges
if (pledge("stdio rpath wpath cpath", NULL) == -1) {
    err(1, "pledge");
}
#endif
```

Common promises:
- `stdio` — Basic I/O, malloc
- `rpath` — Read files
- `wpath` — Write files
- `cpath` — Create files
- `inet` — Network sockets
- `dns` — DNS lookups
- `exec` — Execute programs

### unveil

Restrict filesystem access:

```c
#ifdef __OpenBSD__
// Allow access only to /etc/config and /var/data
unveil("/etc/config", "r");      // Read-only
unveil("/var/data", "rwc");      // Read, write, create
unveil(NULL, NULL);              // Lock it down

if (pledge("stdio rpath wpath cpath", NULL) == -1) {
    err(1, "pledge");
}
#endif
```

## Common Porting Issues

Here's a rundown of the most frequent problems you'll hit.

### Issue 1: Missing `error()` function

BSD doesn't have glibc's `error()` -- use `err()` instead.

**Linux:**
```c
#include <error.h>
error(1, errno, "failed to open %s", filename);
```

**BSD alternative:**
```c
#include <err.h>
err(1, "failed to open %s", filename);
```

### Issue 2: `__u32`, `__s32` types

**Linux kernel headers:**
```c
__u32 value;
__s32 signed_val;
```

**Portable:**
```c
#include <stdint.h>
uint32_t value;
int32_t signed_val;
```

### Issue 3: `TEMP_FAILURE_RETRY` macro

This macro isn't available on BSD. Rewrite the retry loop manually.

**Linux glibc:**
```c
ssize_t n = TEMP_FAILURE_RETRY(read(fd, buf, len));
```

**Portable:**
```c
ssize_t n;
do {
    n = read(fd, buf, len);
} while (n == -1 && errno == EINTR);
```

### Issue 4: `program_invocation_short_name`

This isn't portable -- BSD uses `getprogname()` instead.

**Linux:**
```c
extern char *program_invocation_short_name;
fprintf(stderr, "%s: error\n", program_invocation_short_name);
```

**Portable:**
```c
// Use getprogname() on BSD
const char *progname;

#if defined(__OpenBSD__) || defined(__FreeBSD__)
progname = getprogname();
#else
extern char *__progname;  // Available on most systems
progname = __progname;
#endif
```

## Testing Strategy

1. **Test on Linux first** — Ensure original functionality works
2. **Test on OpenBSD** — Strictest platform, catches most issues
3. **Test on FreeBSD** — Different from OpenBSD in some APIs
4. **Test on NetBSD** — (optional) — Very portable, good validation

## Autotools Detection

```autoconf
# configure.ac
AC_CHECK_HEADERS([sys/epoll.h sys/event.h sys/inotify.h])

AC_CHECK_FUNCS([kqueue epoll_create inotify_init])
AC_CHECK_FUNCS([strlcpy strlcat pledge unveil])

# Define HAVE_KQUEUE, HAVE_EPOLL, etc.
```

Then in code:

```c
#if defined(HAVE_KQUEUE)
// Use kqueue
#elif defined(HAVE_EPOLL)
// Use epoll
#else
#error "No event notification mechanism available"
#endif
```

## Writing Style

Porting guides help developers work across OS boundaries. Apply `natural-writing-style`:

- Reference specific syscall names, header paths, and man page sections — not vague "API differences"
- Don't claim a port is "complete" without listing which functions were mapped and which remain
- State what was tested on which BSD version and what wasn't
- Use contractions; porting docs should read as practical guides, not academic papers

## Resources

- `references/syscall-mapping.md` — Complete Linux→BSD syscall reference
- `references/kqueue-guide.md` — In-depth kqueue usage
- `references/pledge-unveil-guide.md` — OpenBSD security integration
- `assets/porting-checklist.md` — Step-by-step porting checklist
