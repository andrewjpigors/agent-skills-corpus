---
name: zig-best-practices
description: Zig best practices for writing safe, performant, idiomatic Zig code. Targeted at Zig 0.16.0+ (std.Io era).
---

# Zig Best Practices

Safe, performant, idiomatic Zig. Target: **Zig 0.16.0+** (std.Io era).

## Local Documentation First

Run `zig env` to find install paths — no hardcoding. Key fields: `.lib_dir`, `.std_dir`, `.version`.

- **Language Reference**: `<lib_dir>/../doc/langref.html`
- **Std Library Source**: read files under `.std_dir` for API verification
- **Std Library Docs**: run `zig std` to start a local HTTP server

Check local docs before web search.

## Code Style

### Naming

- Modules: `snake_case` (`folded_data.zig`)
- Types: `PascalCase` (`FoldedRecord`)
- Functions/variables: `snake_case` (`fold_data()`, `record_count`)
- Constants: `SCREAMING_SNAKE_CASE` (`MAX_RECORDS`)
- Enums: `PascalCase` (`RecordType`)

### Formatting

- Use `zig fmt` for consistent formatting
- 4-space indentation
- One statement per line
- Group related declarations

## Project Structure

### Standard Layout

```
├── build.zig          # Build config
├── build.zig.zon      # Package manifest
├── zig-pkg/           # Fetched dependencies
├── src/
│   ├── lib.zig        # Core library - public API
│   ├── main.zig       # CLI entry point
│   └── c.h            # C headers for translation
├── tests/             # Integration tests
└── docs/              # Documentation
```

## Entry Point: Juicy Main

Use `std.process.Init` as preferred `main` param. Gives I/O, allocators, env vars, args.

```zig
const std = @import("std");

pub fn main(init: std.process.Init) !void {
    const gpa = init.gpa;
    const io = init.io;
    const arena = init.arena;

    // init.minimal.args — CLI args
    // init.environ_map — environment variables
    // init.preopens — WASI-style preopened files
}
```

### Alternative Signatures

- `pub fn main() !void` — bare, no args/env available
- `pub fn main(init: std.process.Init.Minimal) !void` — raw argv + environ only

### Environment Variables

Access only through `init`:

```zig
// Iterate env vars
for (init.environ_map.keys(), init.environ_map.values()) |key, value| {
    std.log.info("{s}={s}", .{ key, value });
}

// CLI arguments — lazy iteration
var args = init.args.iterate();
while (args.next()) |arg| {
    std.log.info("arg: {s}", .{arg});
}

// Or to slice (needs allocator)
const args_slice = try init.args.toSlice(arena.allocator());
```

Functions needing env vars accept `*const std.process.Environ.Map` or `std.process.Environ` as
param.

## Memory Management

### Allocator Discipline

- Use `ArenaAllocator` for scoped allocs (thread-safe, lock-free)
- Always defer cleanup: `defer arena.deinit()`
- Pass allocator explicitly; no global allocator in production
- Use `std.heap.DebugAllocator` for dev/debug (detects leaks, double-frees, mismatches)
- Use `std.heap.FixedBufferAllocator` for embedded/fixed-budget
- `deinit()` on `DebugAllocator` returns `std.heap.Check` (`.ok` or `.leak`) — check it

```zig
var da = std.heap.DebugAllocator(.{}){};
defer _ = da.deinit();
const allocator = da.allocator();

var arena = std.heap.ArenaAllocator.init(allocator);
defer arena.deinit();
const arena_alloc = arena.allocator();
```

### Choosing an Allocator

Decision flow:

1. **Library?** — accept `Allocator` as param; let caller decide.
2. **Linking libc?** — use `std.heap.c_allocator` as main allocator.
3. **Max bytes known at comptime?** — use `std.heap.FixedBufferAllocator`.
4. **CLI app, run start-to-end, free everything at end?** — use `ArenaAllocator` over
   `page_allocator`; no manual frees needed:

```zig
pub fn main() !void {
    var arena = std.heap.ArenaAllocator.init(std.heap.page_allocator);
    defer arena.deinit();
    const allocator = arena.allocator();

    const ptr = try allocator.create(i32);
    std.debug.print("ptr={*}\n", .{ptr});
}
```

5. **Cyclical pattern (game loop, web request handler)?** — use `ArenaAllocator`; call
   `reset(.retain_capacity)` at cycle end to reuse memory without re-allocating. If upper bound
   known, use `FixedBufferAllocator` instead.
6. **WebAssembly target?** — use `std.heap.wasm_allocator` (alias for
   `WasmAllocator`/`BrkAllocator`, single-threaded only).
7. **Linux embedded, exclusive `brk` access, no libc?** — use `std.heap.brk_allocator`.
8. **Testing OOM handling?** — use `std.testing.FailingAllocator`.
9. **Writing a test?** — use `std.testing.allocator`.
10. **General purpose (none of above)?**
    - **Debug mode**: `std.heap.DebugAllocator(.{})` — detects leaks, double-frees, use-after-free
    - **ReleaseFast mode**: `std.heap.smp_allocator` — lock-free per-thread freelists, scales to CPU
      count

### ArenaAllocator Reset Modes

Use `reset()` over `deinit()` + `init()` in cyclical workloads — cheaper, can preheat buffer:

```zig
// Free all memory, release pages to child allocator
_ = arena.reset(.free_all);

// Keep pages allocated for next cycle (preheating — avoids re-alloc on next burst)
_ = arena.reset(.retain_capacity);

// Keep pages up to a limit, release excess
_ = arena.reset(.{ .retain_with_limit = 64 * 1024 });
```

`retain_capacity` ideal for request handlers or game frames with stable working sets. Arena uses
1.5× exponential growth; steady-state workloads settle to one or two chunks, reset becomes O(1).

`deinit()` and `reset()` single-threaded; alloc/free/resize fully thread-safe via CAS.

### FixedBufferAllocator Thread Safety

`FixedBufferAllocator` has two separate allocator vtables — choose one at init, never mix:

```zig
var fba = std.heap.FixedBufferAllocator.init(&buf);

const allocator = fba.allocator();             // non-thread-safe, no atomics
const ts_allocator = fba.threadSafeAllocator(); // CAS-based, safe for concurrent use
```

Only most-recent allocation can be resized or freed. All other `free()` calls are no-ops.

### BufferFirstAllocator

Hybrid: allocates from fixed buffer first; falls back to child allocator when exhausted. Routes
resize/free to whichever allocator owns pointer.

```zig
var buf: [4096]u8 = undefined;
var bfa = std.heap.BufferFirstAllocator.init(&buf, std.heap.page_allocator);
const allocator = bfa.allocator();
```

Use when most allocs fit in stack/buffer but occasional large ones need heap.

### DebugAllocator Config

`DebugAllocator` takes comptime `Config` struct. Key fields:

| Field                 | Default            | Effect                                                                          |
| --------------------- | ------------------ | ------------------------------------------------------------------------------- |
| `stack_trace_frames`  | 6 (Debug), 0       | Stack frames captured per alloc/free                                            |
| `safety`              | true               | Track requested sizes/alignments, detect mismatches                             |
| `thread_safe`         | `!single_threaded` | Per-allocator mutex                                                             |
| `never_unmap`         | false              | Keep freed pages mapped; converts panics to log msgs                            |
| `retain_metadata`     | false              | Keep freed metadata for extended double-free detection (requires `never_unmap`) |
| `verbose_log`         | false              | Log every alloc/free/resize                                                     |
| `enable_memory_limit` | false              | Add `total_requested_bytes` field and enforce limit                             |

```zig
// Verbose debugging with memory limit
var da = std.heap.DebugAllocator(.{
    .verbose_log = true,
    .enable_memory_limit = true,
    .retain_metadata = true,
    .never_unmap = true,
}){};
defer _ = da.deinit();
```

Small allocs (< `largest_bucket_object_size`) bucketed by power-of-2 size class; large allocs go to
backing allocator. Resize cannot cross size-class boundaries.

### ArrayList Patterns

- Use `.initCapacity(allocator, n)` to create
- Allocator is first arg to all methods: `append(allocator, item)`, `deinit(allocator)`
- Use `ArrayListUnmanaged` when embedding in structs to avoid extra pointer indirection
- Call `ensureTotalCapacity(allocator, n)` before bulk insertions
- Use `toOwnedSlice(allocator)` to transfer ownership

```zig
var list = try std.ArrayList(u8).initCapacity(gpa, 16);
defer list.deinit(gpa);

try list.append(gpa, 'a');
try list.appendSlice(gpa, "hello");
try list.ensureTotalCapacity(gpa, 100);

const owned = try list.toOwnedSlice(gpa);
defer gpa.free(owned);
```

### MemoryPool

Single-type object pool backed by `ArenaAllocator`. Reuses freed objects via intrusive free list
(LIFO). Faster than general allocators for homogeneous allocation bursts.

- `MemoryPool(Item)` — natural alignment
- `memory_pool.Aligned(Item, alignment)` — custom alignment
- `memory_pool.Extra(Item, .{ .growable = false })` — fixed capacity, fails instead of growing
- `initCapacity(allocator, n)` — preallocate n slots
- `create(pool, allocator)` / `destroy(pool, ptr)` — allocator required every call
- `reset(pool, allocator, mode)` — batch-free with `ArenaAllocator.ResetMode`

```zig
var pool = try std.heap.MemoryPool(Node).initCapacity(gpa, 64);
defer pool.deinit(gpa);

const node = try pool.create(gpa);
node.* = .{ .value = 42 };
pool.destroy(node);
```

Caveats:

- `item_size = @max(@sizeOf(FreeListNode), @sizeOf(Item))` — tiny items have hidden overhead
- `create()` returns undefined memory — always initialize before use
- Not thread-safe
- Freed items reused LIFO; not cache-friendly if items large and access pattern random

### Page Size

`std.heap.page_size_min` and `std.heap.page_size_max` are comptime constants. Override via
`std.options` for exotic platforms:

```zig
// root file or build.zig
pub const std_options = std.Options{
    .page_size_min = 65536,
    .page_size_max = 65536,
};
```

Use `std.heap.pageSize()` for runtime value (cached after first query).

### c_allocator Alignment Behavior

`std.heap.c_allocator` handles alignment in three strategies:

- **≤ `max_align_t`**: plain `malloc` (alignment guaranteed by C ABI)
- **> `max_align_t` + `posix_memalign` available**: uses `posix_memalign`
- **> `max_align_t`, no `posix_memalign`**: manual over-allocation with stored unaligned pointer
  header

`remap()` (moving realloc) only works for plain `malloc` path; over-aligned allocs return `null`
from `remap`.

### Memory Locking

```zig
try std.process.lockMemory(slice, .{});
try std.process.lockMemory(slice, .{ .on_fault = true });
try std.process.lockMemoryAll(.{ .current = true, .future = true });
```

mmap/mprotect flags are type-safe structs: `.{ .READ = true, .WRITE = true }`

## Error Handling

### Explicit Error Handling

- Prefer explicit handling: `const result = try operation()`
- Error unions for fallible ops: `fn fetchData() !Data`
- Catch only when acceptable: handle with `catch |err|`
- Use `errdefer` for cleanup on error paths (runs only if function returns error)

```zig
pub fn doThing(allocator: std.Allocator) !*Thing {
    var thing = try allocator.create(Thing);
    errdefer allocator.destroy(thing);

    thing.buf = try allocator.alloc(u8, 256);
    errdefer allocator.free(thing.buf);

    return thing;
}
```

### Error Sets

- Use inferred error sets (`!T`) for public APIs; explicit error sets for stable interfaces
- Never use `anyerror` except at FFI boundaries
- Error sets cannot be reified; declare explicitly with `error{ ... }`
- Use `catch unreachable` only when error provably impossible
- Use `catch |err| switch(err)` for exhaustive handling

### Error Names

| Error                              | Meaning                            |
| ---------------------------------- | ---------------------------------- |
| `error.CrossDevice`                | Operation crosses mount points     |
| `error.FileBusy`                   | File is in use (sharing violation) |
| `error.EnvironmentVariableMissing` | Env var not found                  |
| `error.DirNotEmpty`                | Directory not empty on rename      |
| `error.StreamTooLong`              | Read exceeds limit                 |

## std.Io: Unified I/O

`std.Io` is interface-based I/O system. Thread `std.Io` through app — any function doing I/O, sleep,
random, or time needs `io` param.

### stdout / stderr

```zig
pub fn main(init: std.process.Init) !void {
    const io = init.io;

    // Direct streaming write
    try std.Io.File.stdout().writeStreamingAll(io, "Hello, world!\n");

    // Via writer interface
    var stdout_writer = std.Io.File.stdout().writer(&.{});
    try stdout_writer.interface.print("value: {d}\n", .{42});
}
```

### Fixed-Buffer Reader / Writer

```zig
// Reader from byte slice
var data = "line1\nline2\n";
var reader: std.Io.Reader = .fixed(data);

// Writer into a stack buffer
var buf: [256]u8 = undefined;
var writer: std.Io.Writer = .fixed(&buf);
try writer.interface.print("count: {d}", .{7});
const written = std.Io.Writer.buffered(&writer);
```

### File I/O

```zig
// Read entire file
const contents = try std.Io.Dir.cwd().readFileAlloc(io, "input.txt", gpa, .limited(1024 * 1024));
defer gpa.free(contents);

// Write file atomically
var atomic = try std.Io.File.Atomic.init(io, gpa, "output.txt");
try atomic.file_writer.interface.print("data: {s}\n", .{"hello"});
try atomic.commit(io);
```

### Directory Walking

- `std.Io.Dir.walk` for full traversal
- `std.Io.Dir.walkSelectively` for opt-in recursion per directory
- Both `Walker` and `SelectiveWalker` have `leave()` and `depth()`

### Networking

Use `std.Io.net` (types: `IpAddress`, `Stream`, `Server`, `UnixAddress`). Access via Io vtables:

```zig
io.vtable.netConnectIp(io, addr, port);
io.vtable.netListenIp(io, addr, port);
```

For tests, use `std.Io.net.Socket.createPair` for socketpair.

### Time / Random

```zig
// Time: use std.time.Timer or std.Io.Clock.now(clock, io)

// Random: use Io instance
init.io.random(&buf);

// Or standalone:
const io = std.Io.Threaded.global_single_threaded.ioBasic();
io.random(&buf);
```

### Threading: Io.Group

Use `std.Io.Group`, `std.Io.async`, or `std.Io.concurrent` for concurrent work:

```zig
fn doAllTheWork(io: std.Io) void {
    var g: std.Io.Group = .init;
    errdefer g.cancel(io);
    g.async(io, doSomeWork, .{ io, &g, first_work_item });
    g.wait(io);
}
```

Use `Io.Mutex`, `Io.Condition`, `Io.Event` for synchronization.

## Data Structures

### Slices vs Arrays

- Use `[]const T` for read-only slice params
- Use `[]T` for mutable slice params
- Use `*[N]T` when array length fixed and known at compile time
- Prefer slices over pointers for function params

### Optionals vs Errors

- Use `?T` when absence expected/normal (key not found, EOF)
- Use `!T` when operation can fail with recoverable error
- Never use `.?` (unwrap with panic) in production; use `orelse` or `if/else`

```zig
const val = map.get("key") orelse return Error.NotFound;
if (val) |v| {
    // use v
}
```

### HashMap

Use `.empty` decl literal for initialization. Unmanaged style preferred:

```zig
var map = std.StringHashMap(u32).empty;
defer map.deinit(gpa);

try map.put(gpa, "key", 42);
const val = map.get("key") orelse 0;
```

For array-backed maps: `array_hash_map.Auto`, `array_hash_map.String`, `array_hash_map.Custom`.

### PriorityQueue / PriorityDequeue

```zig
var queue = std.PriorityQueue(u32, void, lessThan).empty;
try queue.push(gpa, item);
const item = queue.pop();

var dq = std.PriorityDequeue(u32, void, lessThan).empty;
const min = dq.popMin();
const max = dq.popMax();
```

### BitSet / EnumSet

Use decl literals for initialization:

```zig
var set = std.EnumSet(MyEnum).empty;
var full = std.EnumSet(MyEnum).full;
```

## Comptime

### Compile-Time Execution

- Use `comptime` for type-level computation, code generation, compile-time checks
- Use `@typeInfo()` for reflection
- Use `inline for`/`inline while` for unrolled loops over comptime-known ranges
- Use `switch` on `@typeInfo()` for type-specialized code

### Type-Creating Builtin Functions

Use individual builtins to construct types dynamically:

```zig
// Integer type
const Bits = @Int(.unsigned, 10);

// Struct type
const MyStruct = @Struct(
    .auto,
    null,
    &.{ "x", "y" },
    &.{ f32, f32 },
    &@splat(.{}),
);

// Enum type
const MyEnum = @Enum(
    u8,
    .exhaustive,
    &.{ "first", "second" },
    &.{ 0, 1 },
);

// Pointer type
const MyPtr = @Pointer(.one, .{ .@"const" = true }, u8, null);

// Function type
const MyFn = @Fn(&.{i32, i32}, &@splat(.{}), i32, .{});

// Tuple type
const MyTuple = @Tuple(&.{ i32, bool });

// Enum literal type
const EnumLitType = @EnumLiteral();

// Union type
const MyUnion = @Union(
    .auto,
    Tag,
    &.{ "a", "b" },
    &.{ u32, f64 },
    &@splat(.{}),
);
```

### Packed Type Rules

- No pointers in `packed struct` or `packed union`
- All fields of `packed union` must have same `@bitSizeOf` as backing integer
- Use explicit backing integers: `packed union(u16) { ... }`
- Enum/packed types with implicit backing types forbidden in `extern` contexts

```zig
const Split16 = packed union(u16) {
    raw: packed struct(u16) { data: u8, padding: u8 = 0 },
    value: u16,
};
```

### Compile-Time Safety

- Use `@compileError()` for user-facing compile-time failures
- Use `@compileLog()` for debugging comptime logic (remove before shipping)
- Use `@setEvalBranchQuota()` when hitting comptime step limits
- Self-referential alignment queries (e.g. `align(@alignOf(@This()))`) error

## Performance

### Push Ifs Up and Fors Down

- **Push ifs up**: move conditional checks and error guards early — before allocs, before loops,
  before expensive computation. Fail fast.
- **Push fors down**: narrow loop scope to only code needing repetition. Don't wrap broad logic in
  `for`/`while` when only small part needs iteration.

```zig
// Bad — if buried deep, runs every iteration
for (items) |item| {
    if (item.kind == .skip) continue;
    const result = try expensiveComputation(item);
    // ...
}

// Good — push if up, filter before loop
for (items) |item| {
    if (item.kind == .skip) continue;
    // rest of loop body
}

// Bad — for wrapping too much
if (condition) {
    for (items) |item| {
        try processA(item);
        try processB(item);
    }
}

// Good — push for down, only iterate what needs it
if (condition) {
    for (items) |item| {
        try processA(item);
    }
}
for (items) |item| {
    try processB(item);
}
```

### Hot Path Optimization

- Use arena for request-scoped allocs
- Avoid allocs in loops; pre-allocate with `ensureTotalCapacity()`
- Use `@branchHint(.cold)` on error paths to help branch predictor
- Use `@branchHint(.unlikely)` for rare conditions

### SIMD

- Use `@Vector(N, T)` for SIMD operations
- Runtime vector indexing forbidden; coerce to array first
- Use `@splat()` for broadcasting scalar to vector
- Use `@reduce()` for horizontal reductions
- Use `@select()` for vectorized conditional

```zig
const Vec = @Vector(4, f32);
const a: Vec = @splat(1.0);
const b: Vec = @splat(2.0);
const c = a + b;
const sum = @reduce(.Add, c);
```

### Float/Integer Coercion

- Small integers coerce to floats automatically if no precision loss: `var f: f32 = small_int;`
- `@floor()`, `@ceil()`, `@round()`, `@trunc()` convert floats to integers directly
- Use `@trunc()` for float-to-int conversion
- Unary float builtins (`@sqrt`, `@sin`, `@cos`, `@tan`, `@exp`, `@log`, etc.) forward result type

## C Interop

### Build System Translation

Use `b.addTranslateC()` in build.zig (backed by arocc):

```zig
// src/c.h
#include <stdio.h>
#include <stdlib.h>
```

```zig
// build.zig
const translate_c = b.addTranslateC(.{
    .root_source_file = b.path("src/c.h"),
    .target = target,
    .optimize = optimize,
});
translate_c.linkSystemLibrary("glfw", .{});

const exe = b.addExecutable(.{
    .name = "myapp",
    .root_module = b.createModule(.{
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
        .imports = &.{
            .{ .name = "c", .module = translate_c.createModule() },
        },
    }),
});
```

```zig
// src/main.zig
const c = @import("c");
```

### Manual Extern Declarations

For minimal C interop, prefer manual `extern` declarations:

```zig
extern "c" fn malloc(size: usize) ?*anyopaque;
extern "c" fn free(ptr: ?*anyopaque) void;

const CStruct = extern struct {
    field: c_int,
    ptr: [*c]u8,
};
```

- Use `extern struct` for C-compatible layouts
- Use `[*c]T` for C pointers (allow null and pointer arithmetic)
- Use sentinel-terminated slices (`[:0]const u8`) for C string interop

## Build System

### build.zig.zon

Requires `fingerprint` field; `name` must be enum literal:

```zig
.{
    .name = .myproject,
    .fingerprint = 0x123456789abcdef0,
    .version = "0.1.0",
    .dependencies = .{},
}
```

### Package Management

- Dependencies fetched into local `zig-pkg/` directory (next to `build.zig`)
- Local overrides: `zig build --fork=/path/to/local/fork`
- Unit test timeouts: `zig build test --test-timeout 500ms`

### build.zig Patterns

```zig
pub fn build(b: *std.Build) void {
    const target = b.standardTargetOptions(.{});
    const optimize = b.standardOptimizeOption(.{});

    const exe = b.addExecutable(.{
        .name = "myapp",
        .root_source_file = b.path("src/main.zig"),
        .target = target,
        .optimize = optimize,
    });

    b.installArtifact(exe);
}
```

## Common Idioms

### JSON

```zig
// Parsing
const parsed = try std.json.parseFromSlice(MyStruct, gpa, json_str, .{});
defer parsed.deinit();

// Serialization
var out: std.Io.Writer.Allocating = .init(gpa);
defer out.deinit();
var stringify: std.json.Stringify = .{
    .writer = &out.writer,
    .options = .{},
};
try stringify.write(parsed.value);
const json_output = out.written();
```

### Leb128 (Binary Format)

```zig
const value = try reader.takeLeb128(u64);
```

### Format Options

- Use `std.fmt.Options` for formatting configuration
- Use `std.fmt.bufPrintSentinel` for sentinel-terminated buffer printing
- Call `writer.print` directly on writer interfaces

### Enum Conversion

```zig
const val = std.enums.fromInt(EnumType, value); // returns ?EnumType
```

### TLS Client Options

`std.crypto.tls.Client.Options` requires `entropy: *const [entropy_len]u8` and
`realtime_now_seconds: i64`. Fill entropy with `std.Io.randomSecure`; compute seconds with
`Io.Clock.now(.real, io)`.

## Testing

### Test Structure

- Use `test` blocks colocated with implementation
- Use `std.testing.allocator` for test allocs (detects leaks)
- Use `try` in tests to fail fast on errors
- Use `std.testing.expect()` and `std.testing.expectEqual()` for assertions

```zig
test "basic arithmetic" {
    try std.testing.expectEqual(4, 2 + 2);
    try std.testing.expectError(error.OutOfMemory, mightFail());
}

test "no leaks" {
    var da = std.heap.DebugAllocator(.{}){};
    defer std.testing.expect(da.deinit() == .ok) catch @panic("leak");
    const allocator = da.allocator();

    const ptr = try allocator.create(u32);
    defer allocator.destroy(ptr);
}
```

### Testing Adjustments

- For in-process client/server tests, use `std.Io.net.Socket.createPair` or raw `socketpair`
- Error sets tightened in many std.Io functions — remove unreachable branches accordingly
- Run `zig build test --test-timeout 500ms` to catch hanging tests early

### Fuzz Testing

- Use `test` with randomized inputs for property-based testing
- Use `std.testing.FailingAllocator` to test allocation failure paths

## Documentation

- Document all public API with `///` comments
- State params, returns, errors clearly
- Include usage examples for complex APIs
- Document error conditions and edge cases

```zig
/// Parses a folded record from the given byte slice.
///
/// Parameters:
///   allocator - used for any internal allocations
///   input - the byte slice to parse
///
/// Returns:
///   The parsed FoldedRecord on success
///
/// Errors:
///   Error.InvalidFormat - if input does not match expected format
///   Error.OutOfMemory - if allocation fails
pub fn parseRecord(allocator: std.Allocator, input: []const u8) !FoldedRecord {
    // ...
}
```

## Safety

### Runtime Safety

- Keep safety checks enabled in Debug/ReleaseSafe builds
- Use `@setRuntimeSafety(false)` only in proven hot paths after benchmarking
- Never disable safety globally; do per-function with justification
- Use `std.debug.assert()` for developer invariants (stripped in ReleaseFast)

### Undefined Behavior Prevention

- Always initialize variables before use
- Check bounds before array/slice access
- Use `@addWithOverflow()`, `@mulWithOverflow()` when overflow possible
- Use `std.math.maxInt(T)` / `std.math.minInt(T)` for bounds checks
- Never return pointers to local variables (compile error)
- Vectors and arrays don't support in-memory coercion — cast element-wise
- Explicitly-aligned pointer types distinct from naturally-aligned ones

## Common Error Messages

| Error                                        | Cause                      | Fix                                                          |
| -------------------------------------------- | -------------------------- | ------------------------------------------------------------ |
| `no field named 'getStdOut'`                 | Wrong I/O API              | Use `std.Io.File.stdout()`                                   |
| `expected 2 argument(s), found 1`            | Missing allocator          | Add allocator as first argument                              |
| `no member named 'Pool' in 'Thread'`         | Use Io for concurrency     | Use `std.Io.Group` + `Io.async`                              |
| `expected type '*const process.Environ.Map'` | Function needs env map     | Pass from `main(init)`                                       |
| `no member named 'fixedBufferStream'`        | Use Io fixed reader/writer | Use `std.Io.Reader.fixed(...)` or `std.Io.Writer.fixed(...)` |
| `no field named 'getCwd' in 'process'`       | Renamed API                | Use `std.process.currentPath*`                               |
| `fingerprint field missing`                  | Missing in build.zig.zon   | Add `.fingerprint` and use enum literal for `.name`          |
| `type depends on itself for alignment`       | Self-referential alignment | Remove `@alignOf(@This())` or restructure                    |

## Migration (0.15 → 0.16)

### Quick Reference

| Old (0.15)                           | New (0.16)                                               |
| ------------------------------------ | -------------------------------------------------------- |
| `@Type(.Int(...))`                   | `@Int(.signed, bits)`                                    |
| `@Type(.Struct(...))`                | `@Struct(layout, BackingInt, names, types, attrs)`       |
| `@Type(.Pointer(...))`               | `@Pointer(size, attrs, Element, sentinel)`               |
| `@Type(.Fn(...))`                    | `@Fn(param_types, param_attrs, ReturnType, attrs)`       |
| `@Type(.Tuple(...))`                 | `@Tuple(field_types)`                                    |
| `@Type(.enum_literal)`               | `@EnumLiteral()`                                         |
| `@cImport({...})`                    | `b.addTranslateC(...)` + `@import("c")`                  |
| `std.net`                            | `std.Io.net`                                             |
| `std.ArrayList.init(allocator)`      | `std.ArrayList.initCapacity(allocator, n)`               |
| `std.crypto.random`                  | `std.Io.randomSecure(io, buf)` or `io.random(&buf)`      |
| `std.meta.intToEnum`                 | `std.enums.fromInt`                                      |
| `std.fmt.FormatOptions`              | `std.fmt.Options`                                        |
| `std.fmt.bufPrintZ`                  | `std.fmt.bufPrintSentinel`                               |
| `std.io.fixedBufferStream`           | `std.Io.Writer.fixed(buf)` / `std.Io.Reader.fixed(data)` |
| `error.RenameAcrossMountPoints`      | `error.CrossDevice`                                      |
| `error.NotSameFileSystem`            | `error.CrossDevice`                                      |
| `error.SharingViolation`             | `error.FileBusy`                                         |
| `error.EnvironmentVariableNotFound`  | `error.EnvironmentVariableMissing`                       |
| `std.Thread.Pool`                    | `std.Io.Group` + `Io.async`                              |
| `std.heap.GeneralPurposeAllocator`   | `std.heap.DebugAllocator` (same config pattern)          |
| `std.heap.ThreadSafe`                | `std.heap.ArenaAllocator` (now thread-safe)              |
| `std.posix.mlock*`                   | `std.process.lockMemory*`                                |
| `std.posix.getCwd*`                  | `std.process.currentPath*`                               |
| `std.ArrayHashMap`                   | `array_hash_map.Auto` / `.String` / `.Custom`            |
| `std.heap.WasmAllocator`             | `std.heap.wasm_allocator` (singleton, single-threaded)   |
| `std.heap.BrkAllocator`              | `std.heap.brk_allocator` (Linux+WASM, single-threaded)   |
| `std.SegmentedList`                  | (removed)                                                |
| `std.meta.declList`                  | (removed)                                                |
| `std.fs.getAppDataDir`               | (removed)                                                |
| `std.Io.GenericReader` / `AnyReader` | `std.Io.Reader`                                          |
| `std.Io.GenericWriter` / `AnyWriter` | `std.Io.Writer`                                          |
| `std.Io.CountingReader`              | (track bytes manually)                                   |
| `std.Io.null_writer`                 | Use `std.Io.Writer` directly                             |

### Migration Steps

1. **Replace `@Type` calls** with specific builtins (`@Int`, `@Struct`, `@Union`, `@Enum`,
   `@Pointer`, `@Fn`, `@Tuple`, `@EnumLiteral`)
2. **Replace `@cImport`** with `addTranslateC` in `build.zig`
3. **Add `fingerprint` and fix `name`** in `build.zig.zon` (enum literal, not string)
4. **Thread `std.Io` through app** — any function doing I/O, sleep, random, or time needs `io` param
5. **Update `std.net` usages** to `std.Io.net` or raw syscalls
6. **Update `ArrayList` calls** — pass allocator explicitly, use `initCapacity`
7. **Fix error set names** — `CrossDevice`, `FileBusy`, `EnvironmentVariableMissing`, `DirNotEmpty`
8. **Replace `Thread.Pool`** with `Io.Group` + `Io.async`
9. **Replace `Thread.Mutex`/`Condition`/`ResetEvent`** with `Io.Mutex`/`Condition`/`Event`
10. **Run `zig build test --test-timeout 500ms`** to catch hanging tests early

## When to Use Zig Tools

- Use `zig build test` to run tests
- Use `zig build -Doptimize=ReleaseFast` for performance builds
- Use `zig build -Doptimize=ReleaseSafe` for production with safety
- Use `zig fmt` for formatting
- Use `zig build-exe -freference-trace` for detailed error traces
- Use `zig std` to browse standard library docs locally
