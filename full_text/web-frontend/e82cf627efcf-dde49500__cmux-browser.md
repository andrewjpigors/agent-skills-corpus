---
name: cmux-browser
description: Drive browser surfaces inside cmux (Flow, Weixin, Xiaohongshu, Douyin, ChatGPT) via snapshot refs (e1,e2). Use when target already open in cmux. Pass surface as surface:N (not bare int).
---

<!-- archived-description (auto-shortened 2026-05-06):
Drive browser surfaces inside cmux (Google Flow, Weixin Channels, Xiaohongshu Creator, Douyin Creator, ChatGPT, etc.) using snapshot-based element refs (e1, e2, …). Use when the user references a browser they already have open in cmux ("the Flow tab I have open", "the Xiaohongshu tab"), when authenticated session reuse matters (cookies persist across cmux app restarts), or when generally automating any cmux browser surface. Prefer this over Playwright when the target site is already open in cmux; prefer opencli-browser when the same site is logged in inside the user's real Chrome and not yet imported into cmux. Key trick: pass surface as `surface:N` ref form, never bare integer index.
-->

# Browser automation in cmux

cmux's in-app browser is a WKWebView with a Playwright-style automation API ported from agent-browser. Auth is imported once from Chrome/Firefox/Arc/etc. and persists across cmux launches, so anything the user is logged into in their real browser can be re-used here.

## When to reach for this

| Situation | Tool |
|-----------|------|
| Site already open as a cmux browser surface, plain inputs/textareas | **cmux-browser** ✓ |
| **Site uses Slate/Lexical/ProseMirror/TipTap/Quill rich-text editor** (Google Flow, Notion, Linear, modern Gmail/Docs) | **opencli-browser** (real Chrome — see "Slate limitation" below) |
| Site logged into in real Chrome, not yet in cmux | opencli-browser |
| One-shot scrape of a public site, no auth needed | playwright |
| Need devtools / network mocking / CDP-only feature | playwright (cmux can't, see Limits) |

### Detect rich-text editors before committing

**Always run this check first** when the prompt input is suspicious (placeholder reappears with text, submit no-ops, etc.):

```bash
cmux browser surface:N eval --script '
const slate = document.querySelector("[data-slate-editor]");
const lexical = document.querySelector("[data-lexical-editor]");
const ce = document.querySelectorAll("[contenteditable=true]").length;
JSON.stringify({slate: !!slate, lexical: !!lexical, contentEditableCount: ce})
'
```

If `slate` or `lexical` is true, **switch tools now**. cmux-browser will populate the DOM but the editor's internal state stays empty, and submit will silently no-op. This is a hard WKWebView limitation, not a cmux bug.

## Stable agent loop

```
identify → goto/get url → wait → snapshot --interactive → act → snapshot
```

**Always re-snapshot after a click that mutates the DOM.** Element refs (e1, e2…) are tied to the snapshot they came from; they go stale after navigation or DOM updates.

## Fast start

```bash
# 1. Find your target browser surface
cmux tree --all | grep browser

# 2. Confirm URL before doing anything
cmux browser surface:7 get url

# 3. Wait until page is stable, then snapshot
cmux browser surface:7 wait --load-state complete --timeout-ms 15000
cmux browser surface:7 snapshot --interactive
# → returns accessibility tree with refs e1, e2, e3...

# 4. Act on a ref
cmux browser surface:7 fill e1 "hello world"
cmux --json browser surface:7 click e2 --snapshot-after

# 5. Verify
cmux browser surface:7 get url
cmux browser surface:7 get text e3
```

## Open a new browser surface

```bash
# Open in current workspace, return the surface ref as JSON
cmux --json browser open https://labs.google/fx/tools/flow

# Open as a split next to current surface
cmux --json browser open-split https://example.com

# Target a specific workspace/window
cmux --json browser open https://example.com --workspace workspace:2 --window window:1
```

The JSON output includes the new `surface:N` — capture it for follow-up commands.

## All the browser commands

```bash
# Navigation
cmux browser surface:N goto <url> [--snapshot-after]
cmux browser surface:N back | forward | reload [--snapshot-after]
cmux browser surface:N get url | title

# Snapshot (the foundation of everything)
cmux browser surface:N snapshot                     # text-only
cmux browser surface:N snapshot --interactive       # adds refs e1, e2...
cmux browser surface:N snapshot --compact           # smaller token cost
cmux browser surface:N snapshot --max-depth 6
cmux browser surface:N snapshot --selector "main"   # subtree only

# Find-by-attribute (returns ref)
cmux browser surface:N find role "button" --name "Submit"
cmux browser surface:N find text "Sign in"
cmux browser surface:N find label "Email"
cmux browser surface:N find placeholder "Search..."
cmux browser surface:N find testid "header-cta"

# Wait
cmux browser surface:N wait --load-state complete --timeout-ms 15000
cmux browser surface:N wait --selector "#ready" --timeout-ms 10000
cmux browser surface:N wait --text "Success" --timeout-ms 10000
cmux browser surface:N wait --url-contains "/dashboard"
cmux browser surface:N wait --function "document.readyState === 'complete'"

# Act on element (selector OR ref)
cmux browser surface:N click  e2 [--snapshot-after]
cmux browser surface:N dblclick "button.submit"
cmux browser surface:N hover  e3
cmux browser surface:N focus  e4
cmux browser surface:N fill   e5 "text"
cmux browser surface:N type   e5 "text"      # types char-by-char (some sites need this)
cmux browser surface:N press  "Enter"
cmux browser surface:N select e6 "option-value"
cmux browser surface:N check e7 / uncheck e7
cmux browser surface:N scroll-into-view e8
cmux browser surface:N scroll --dy 500

# Read state
cmux browser surface:N get text  e9
cmux browser surface:N get html  e9
cmux browser surface:N get value e5
cmux browser surface:N get attr  e9 --attr href
cmux browser surface:N get count "li.item"
cmux browser surface:N get box   e9
cmux browser surface:N is visible e9
cmux browser surface:N is enabled e9
cmux browser surface:N is checked e7

# Capture
cmux browser surface:N screenshot --out /tmp/page.png

# JS escape hatch
cmux browser surface:N eval --script "return document.title"
```

## Auth & session state

cmux imports cookies from Chrome/Firefox/Arc/etc. on first install. Once you log into a site inside a cmux browser, the session persists across app restarts. To save/load explicitly:

```bash
# Save current auth state to a file (after logging in)
cmux rpc browser.state.save '{"workspace_id":"...","surface_id":"...","path":"~/auth/site.json"}'

# Load it later (e.g., in a different surface or after a clear)
cmux rpc browser.state.load '{"workspace_id":"...","surface_id":"...","path":"~/auth/site.json"}'

# Get/set/clear cookies
cmux rpc browser.cookies.get   '{"workspace_id":"...","surface_id":"..."}'
cmux rpc browser.cookies.set   '{"workspace_id":"...","surface_id":"...","cookies":[...]}'
cmux rpc browser.cookies.clear '{"workspace_id":"...","surface_id":"..."}'
```

## Common recipes

### Drive a Google Flow image generation

```bash
# 1. Confirm the Flow tab
cmux tree --all | grep -i flow
# → surface:7 [browser] "Flow - ..." https://labs.google/fx/zh/tools/flow/...

cmux browser surface:7 get url
cmux browser surface:7 wait --load-state complete --timeout-ms 15000
cmux browser surface:7 snapshot --interactive

# 2. Find the prompt textarea and submit button (use the snapshot output to pick refs)
cmux browser surface:7 fill e_prompt "三界军师之苟钰，水墨国风，手持账本与算盘"
cmux --json browser surface:7 click e_submit --snapshot-after

# 3. Wait for output, screenshot
cmux browser surface:7 wait --selector "img[data-generated]" --timeout-ms 60000
cmux browser surface:7 screenshot --out /tmp/flow_output.png
```

### Form submit + verification

```bash
cmux --json browser open https://example.com/signup
cmux browser surface:7 wait --load-state complete --timeout-ms 15000
cmux browser surface:7 snapshot --interactive
cmux browser surface:7 fill e1 "Jane Doe"
cmux browser surface:7 fill e2 "jane@example.com"
cmux --json browser surface:7 click e3 --snapshot-after
cmux browser surface:7 wait --url-contains "/welcome" --timeout-ms 15000
```

## Gotchas (all verified by failed runs against Google Flow on 2026-04-27)

1. **Surface ref form, not bare index.** `--surface 3` may be parsed as the 3rd-browser-surface index, not `surface:3`. **Always use `surface:N` ref form**, e.g. `cmux browser surface:7 click e1`.

2. **Always pass `--text` and `--selector` as explicit flags, never positional.** The CLI parser will silently bleed trailing flags into the text value:
   ```bash
   # ❌ BUG: " --snapshot-after" gets appended to the prompt as literal text
   cmux browser surface:7 fill e1 "my prompt" --snapshot-after

   # ✓ Correct
   cmux browser surface:7 fill --selector e1 --text "my prompt" --snapshot-after
   ```
   Always verify with `cmux browser surface:N get value e1` after fill.

3. **Refs renumber project-wide on every snapshot.** After `--snapshot-after` or any explicit snapshot, e428 → e447 → e466 → ... across the whole tree, not just the touched subtree. **Always re-snapshot and re-find your target by name/role before each action.**

4. **Slate / Lexical / ProseMirror / TipTap editors silently no-op submit.** This is the big one — see "Detect rich-text editors" above. Symptoms:
   - `fill` returns OK and `get value` shows your text, BUT
   - The placeholder text still appears in the next snapshot's accessibility name
   - Submit click registers OK but no generation/network activity happens
   - `eval` confirms `[contenteditable=true]` exists with your text in `textContent`

   **Why:** Slate maintains its own state tree, separate from DOM textContent. It listens for `beforeinput` events but only updates state for `isTrusted: true` events. WKWebView synthetic events are never trusted, and `browser.input_keyboard` returns `not_supported` on WKWebView. So cmux can write the visible DOM but cannot write the editor's internal state.

   **Fix:** switch to `opencli-browser` (real Chrome → trusted events) or `playwright` (Chromium with CDP injection).

5. **Cross-domain navigation can break refs.** Sites that redirect via new tabs (e.g., labs.google → Flow editor often opens in a different surface) — after such navigation, run `cmux tree --all` again and treat the result as a new surface.

6. **Don't `click` for cross-domain redirects.** Use `goto <url>` directly when you know the destination URL.

7. **`eval` returns `js_error` if the script uses `return` at the top level.** Use a final expression instead:
   ```bash
   # ❌ js_error
   cmux browser surface:N eval --script 'const x = 1; return x;'
   # ✓ Works
   cmux browser surface:N eval --script 'const x = 1; x'
   ```

8. **Closing a browser surface drops the session for that surface.** Reuse existing browser surfaces rather than open/close cycles.

9. **Don't trust accessibility-tree snapshots blindly.** The textbox node may show concatenated `placeholder + your text` after a partially-applied fill, masking the fact that the editor's real state is empty. Pair snapshot checks with `eval` to inspect actual DOM state.

## Limits (WKWebView, not Chrome)

These return `not_supported`:
- viewport emulation
- offline emulation
- trace / screencast recording
- network route interception/mocking
- raw input injection (use the high-level `click`/`fill`/`press`/`scroll` instead)

For any of those, fall back to `playwright`.

## Recovery from `js_error`

Heavy or hostile pages can break `snapshot --interactive` or `eval`. Fallback chain:

```bash
cmux browser surface:N get url            # confirm where you are
cmux browser surface:N get text body      # raw text
cmux browser surface:N get html body      # raw HTML
# If still broken, navigate to a simpler intermediate page and retry
```

## Reference

- Canonical skill: https://github.com/manaflow-ai/cmux/blob/main/skills/cmux-browser/SKILL.md
- Full API capabilities: `cmux capabilities` (search for `browser.*` methods)
