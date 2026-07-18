---
name: nix-style-review
description: >-
  Nix code review for nixpkgs contributions, NixOS modules, and derivations.
  Enforces RFC standards covering module design (RFC 0042: settings pattern, option count),
  security (RFC 0052: DynamicUser, dynamic IDs), package structure (RFC 0140),
  testing (RFC 0119), metadata (RFC 0089), documentation (RFC 0145, RFC 0072),
  formatting (RFC 0166), and breaking changes (RFC 0088).
  Triggers: nix review, nixpkgs PR, nix code quality, nixos module review, nix derivation review, module design, too many options, settings pattern
license: MIT
metadata:
  version: 1.1.0
  author: skills-repo
  changelog: Added RFC 0042 (module design), RFC 0052 (security), RFC 0072 (docs), RFC 0127 (problems), RFC 0146 (categories), RFC 0180 (removal policy)
allowed-tools: Bash(nixfmt* nixpkgs-fmt* nix*) Read Grep Edit
---

# Nix Style Review

Reviews Nix code for nixpkgs, NixOS, and Home Manager. We'll check against [RFC standards](https://github.com/NixOS/rfcs) to catch issues before you submit. Whether you're contributing packages or modules, this skill helps you avoid common pitfalls and follow community conventions.

## Quick Start

When reviewing Nix code, we'll check:

1. Code type (package, module, flake)
2. Module design ([RFC 0042](https://github.com/NixOS/rfcs/blob/master/rfcs/0042-config-option.md): `settings` pattern, option count)
3. Security & users ([RFC 0052](https://github.com/NixOS/rfcs/blob/master/rfcs/0052-dynamic-ids.md): `DynamicUser`, dynamic IDs)
4. Package structure ([RFC 0140](https://github.com/NixOS/rfcs/blob/master/rfcs/0140-simple-package-paths.md): `pkgs/by-name`)
5. Metadata ([RFC 0089](https://github.com/NixOS/rfcs/blob/master/rfcs/0089-collect-non-source-package-meta.md))
6. Testing strategy ([RFC 0119](https://github.com/NixOS/rfcs/blob/master/rfcs/0119-testing-conventions.md))
7. Doc-comments ([RFC 0145](https://github.com/NixOS/rfcs/blob/master/rfcs/0145-doc-strings.md), [RFC 0072](https://github.com/NixOS/rfcs/blob/master/rfcs/0072-commonmark-docs.md))
8. Formatting ([RFC 0166](https://github.com/NixOS/rfcs/blob/master/rfcs/0166-nix-formatting.md))

## When to Use This Skill

Use when:

- Reviewing [nixpkgs pull requests](https://github.com/NixOS/nixpkgs/pulls)
- Writing new NixOS modules
- Creating package derivations
- Before submitting contributions

## Review Workflow

### Step 1: Identify Code Type

**Package derivation:** Uses `stdenv.mkDerivation` or language-specific builder
**NixOS module:** Has `options` and `config` sections
**Flake:** Has `description`, `inputs`, and `outputs`

See [references/code-patterns.md](references/code-patterns.md) for complete templates.

### Step 2: Module Design (RFC 0042)

**For NixOS/Home Manager modules**, check the option count and design pattern:

**Use `settings` pattern instead of many individual options:**
```nix
{
  options.services.foo = {
    enable = lib.mkEnableOption "foo service";

    settings = lib.mkOption {
      type = lib.types.submodule {
        freeformType = settingsFormat.type;

        # Only create explicit options for valuable settings:
        options.port = lib.mkOption {
          type = lib.types.port;
          default = 8080;
          description = "Port to listen on.";
        };
      };
      default = {};
      description = "Configuration for foo. See <link xlink:href=\"https://example.com/docs\"/> for options.";
    };
  };
}
```

**Only create explicit options for "valuable" settings:**

| Type | Why | Examples |
|------|-----|----------|
| Main/popular | Basic usage, most users need these | `services.nginx.enable`, `services.postgresql.port` |
| Mandatory | Must be set for service to work | `services.hydra.hydraURL` |
| Sensitive | Avoid Nix store | `services.foo.passwordFile` (not `password`) |

**Check:**
- [ ] Module has >10-15 individual options? You'll want to use `settings` instead
- [ ] Using `extraConfig` string option? Migrate to `settings` with `pkgs.formats.*`
- [ ] Hardcoded defaults that can't be overridden? Use `settings` with `mkDefault`
- [ ] Config file format mappable to Nix? Use `pkgs.formats.json`, `.yaml`, `.toml`, `.ini`

**Why it matters:** Dozens of individual options create maintenance burden, fill option listings with noise, can't keep pace with upstream changes, and prevent users from overriding settings. The `settings` pattern solves all of these.

See [references/module-design.md](references/module-design.md) for complete examples and migration patterns.

### Step 3: Security & User Management (RFC 0052)

**For NixOS services**, check user/permission configuration:

**Prefer `DynamicUser` for systemd services:**
```nix
systemd.services.myservice = {
  serviceConfig = {
    DynamicUser = true;
    StateDirectory = "myservice";  # Creates /var/lib/myservice with correct permissions
  };
};
```

**When `DynamicUser` doesn't work** (state shared between services, specific user needed):
```nix
{
  users.users.myservice = {
    isSystemUser = true;  # Required for dynamic allocation
    group = "myservice";
    # Do NOT set uid - let NixOS allocate dynamically
  };
  users.groups.myservice = {};  # Do NOT set gid

  systemd.services.myservice.serviceConfig = {
    User = "myservice";
    StateDirectory = "myservice";  # /var/lib/myservice owned by myservice:myservice
  };
}
```

**Check:**
- [ ] Service uses `DynamicUser = true` when state's self-contained?
- [ ] If persistent user needed: uses dynamic allocation (`isSystemUser = true`, no `uid`/`gid`)?
- [ ] Uses `StateDirectory`/`CacheDirectory`/`LogsDirectory` instead of manual `chown`?
- [ ] Service doesn't run as root unnecessarily?
- [ ] Static UID/GID has explicit justification? (You'll almost never need this)

**Why it matters:** Static UIDs are exhausted (only 400 in reserved range), central mapping causes merge conflicts, and dynamic allocation with `StateDirectory` is simpler and more secure. You don't need to manage this manually.

See [references/security-hardening.md](references/security-hardening.md) for service hardening patterns.

**Complete quality gates:** See [assets/module-design-checklist.md](assets/module-design-checklist.md) for complete module design checklist covering all RFCs.

### Step 4: Package Structure (RFC 0140)

**For nixpkgs packages**, verify `pkgs/by-name` structure:

```bash
# Expected: pkgs/by-name/${shard}/${name}/package.nix
# Shard = lowercased first 2 letters
# Example: pkgs/by-name/he/hello/package.nix → pkgs.hello
```

**Requirements** ([official docs](https://github.com/NixOS/nixpkgs/blob/master/pkgs/README.md)):
- Self-contained (no file refs outside package dir)
- Name: ASCII alphanumerics + hyphens/underscores
- Unique when lowercased

Each package lives in its own directory and can't reach outside that boundary. CI enforces this using [nixpkgs-vet](https://github.com/NixOS/nixpkgs-vet).

### Step 5: Metadata (RFC 0089)

**Required meta attributes:**
```nix
meta = with lib; {
  description = "One-line description (no period)";
  homepage = "https://example.com";
  license = licenses.MIT;  # Use lib.licenses.* not strings
  maintainers = with maintainers; [ username ];
  platforms = platforms.linux;

  # For binary packages (REQUIRED):
  sourceProvenance = with sourceTypes; [
    binaryNativeCode
  ];
};
```

**Check:**
- [ ] description present and concise
- [ ] license uses `lib.licenses.*` ([list](https://github.com/NixOS/nixpkgs/blob/master/lib/licenses.nix))
- [ ] maintainers listed
- [ ] platforms specified
- [ ] sourceProvenance set for binaries

**Why it matters:** Metadata powers [search.nixos.org](https://search.nixos.org/), license compliance, and platform filtering.

### Step 6: Testing Strategy (RFC 0119)

**Three-tier hierarchy** ([official guide](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html)):

**1. checkPhase:** Fast unit tests (runs during build)
```nix
checkPhase = ''
  runHook preCheck
  make test
  runHook postCheck
'';
```

**2. installCheckPhase:** Post-install smoke tests
```nix
installCheckPhase = ''
  $out/bin/program --version
'';
```

**3. passthru.tests:** Integration tests (runs separately)
```nix
passthru.tests.integration = nixosTest {
  nodes.machine = { pkgs, ... }: {
    environment.systemPackages = [ pkgs.package-name ];
  };
  testScript = ''
    machine.succeed("package-name --version")
  '';
};
```

**Check:**
- [ ] Fast tests in checkPhase
- [ ] Expensive tests in passthru.tests
- [ ] Integration tests use [nixosTest](https://github.com/NixOS/nixpkgs/blob/master/nixos/doc/manual/development/writing-nixos-tests.section.md)

See [NixOS VM tests wiki](https://wiki.nixos.org/wiki/NixOS_VM_tests) for testing patterns.

### Step 7: Documentation (RFC 0145)

**Doc-comment format** (if functions are documented):
```nix
/**
  Brief description.

  # Examples

  ```nix
  funcName { arg = "value"; }
  => expectedResult
  ```
*/
functionName = { arg }: ...;
```

Use [CommonMark](https://commonmark.org/) (standard Markdown), not HTML. HTML tags won't work in man pages or other output formats.

### Step 8: Formatting (RFC 0166)

**Run formatter if available:**
```bash
nixfmt --check file.nix
```

The [official nixfmt](https://github.com/NixOS/nixfmt) implements RFC 0166.

**Manual checks:**
- [ ] 2 spaces per level (not tabs)
- [ ] 100 char soft limit
- [ ] Spaces inside brackets: `[ foo ]`, `{ bar = 1; }`
- [ ] Multi-line: all on one OR each on own line (no mixing)

See [references/rfc-summary.md](references/rfc-summary.md#formatting-details-rfc-0166) for complete formatting rules.

### Step 9: Breaking Changes (RFC 0088)

**If PR introduces breaking changes:**

Check the procedure's been followed ([official policy](https://github.com/NixOS/rfcs/blob/master/rfcs/0088-nixpkgs-breaking-change-policy.md)):
- [ ] Sample testing done (≥100 packages OR ≥3h build time)
- [ ] Affected maintainers notified
- [ ] Grace period provided (7 days minimum)
- [ ] Broken packages marked `broken = true;`

Use [nixpkgs-review](https://github.com/Mic92/nixpkgs-review) to test downstream impact:
```bash
nixpkgs-review pr 12345
```

**Staging branch check:**
If >500 rebuilds → should target `staging`, not `master` ([RFC 0026](https://github.com/NixOS/rfcs/blob/master/rfcs/0026-staging-workflow.md)). Don't merge mass rebuilds directly to master.

## Common Issues

See [references/common-mistakes.md](references/common-mistakes.md) for before/after examples.

**Top issues:**
- **Too many individual options** - should use `settings` pattern (RFC 0042)
- **Using `extraConfig` strings** - should use `settings` with `pkgs.formats.*` (RFC 0042)
- **Service running as root** - should use `DynamicUser` or dynamic IDs (RFC 0052)
- **Static UID/GID without justification** (RFC 0052)
- **Manual permission management** - should use `StateDirectory` (RFC 0052)
- Cross-package file references (violates RFC 0140)
- Hardcoded license strings (should use `lib.licenses.*`)
- Expensive tests in checkPhase (should be in passthru.tests)
- Missing sourceProvenance for binaries
- Using tabs instead of spaces
- No downstream testing for breaking changes

## Platform Considerations

**Support tiers** ([RFC 0046](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md)):
- **Tier 1** (x86_64-linux): Block updates until fixed
- **Tier 2** (aarch64-linux, x86_64-darwin): Investigate failures
- **Tier 3+** (other): Best effort

Prefer generic fixes over platform-specific hacks when you can.

## Validation Tools

**Check formatting:**
```bash
scripts/check-nix-format.sh path/to/file.nix
```

**Manual checks if no formatter's available:**
```bash
grep -P '\t' file.nix  # shouldn't find tabs
file file.nix | grep CRLF  # should be LF
```

## References

### RFCs
Detailed guidance in [references/rfc-summary.md](references/rfc-summary.md):

**Core Quality Gates:**
- [RFC 0042](https://github.com/NixOS/rfcs/blob/master/rfcs/0042-config-option.md): Module design (settings pattern, option count)
- [RFC 0052](https://github.com/NixOS/rfcs/blob/master/rfcs/0052-dynamic-ids.md): Security & user management (DynamicUser, dynamic IDs)
- [RFC 0140](https://github.com/NixOS/rfcs/blob/master/rfcs/0140-simple-package-paths.md): Package structure
- [RFC 0119](https://github.com/NixOS/rfcs/blob/master/rfcs/0119-testing-conventions.md): Testing conventions
- [RFC 0089](https://github.com/NixOS/rfcs/blob/master/rfcs/0089-collect-non-source-package-meta.md): Metadata requirements
- [RFC 0145](https://github.com/NixOS/rfcs/blob/master/rfcs/0145-doc-strings.md): Doc-comment format
- [RFC 0072](https://github.com/NixOS/rfcs/blob/master/rfcs/0072-commonmark-docs.md): Documentation format (CommonMark)
- [RFC 0166](https://github.com/NixOS/rfcs/blob/master/rfcs/0166-nix-formatting.md): Code formatting
- [RFC 0088](https://github.com/NixOS/rfcs/blob/master/rfcs/0088-nixpkgs-breaking-change-policy.md): Breaking changes

**Supplementary:**
- [RFC 0026](https://github.com/NixOS/rfcs/blob/master/rfcs/0026-staging-workflow.md): Staging workflow
- [RFC 0046](https://github.com/NixOS/rfcs/blob/master/rfcs/0046-platform-support-tiers.md): Platform tiers
- [RFC 0127](https://github.com/NixOS/rfcs/blob/master/rfcs/0127-issues-warnings.md): Problem declaration (meta.problems)
- [RFC 0146](https://github.com/NixOS/rfcs/blob/master/rfcs/0146-meta-categories.md): Package categories
- [RFC 0180](https://github.com/NixOS/rfcs/blob/master/rfcs/0180-broken-package-removal.md): Package removal policy

### Official Documentation
- [Nixpkgs Manual](https://nixos.org/manual/nixpkgs/stable/)
- [NixOS Manual](https://nixos.org/manual/nixos/stable/)
- [nixfmt Repository](https://github.com/NixOS/nixfmt)
- [Nix RFC Repository](https://github.com/NixOS/rfcs)
- [Nixpkgs Contributing Guide](https://github.com/NixOS/nixpkgs/blob/master/CONTRIBUTING.md)
- [nix.dev Tutorials](https://nix.dev/)

### Tutorials
- [Packaging Existing Software](https://nix.dev/tutorials/packaging-existing-software.html)
- [NixOS Module System](https://nix.dev/tutorials/module-system/)
- [Integration Testing with VMs](https://nix.dev/tutorials/nixos/integration-testing-using-virtual-machines.html)
- [Module System Deep Dive](https://nix.dev/tutorials/module-system/deep-dive.html)

### Tools
- [nixfmt-rfc-style](https://github.com/NixOS/nixfmt): Official formatter
- [nixpkgs-review](https://github.com/Mic92/nixpkgs-review): PR review automation
- [nixpkgs-vet](https://github.com/NixOS/nixpkgs-vet): CI validation
- [nix-review](https://github.com/Mic92/nix-review): Local PR testing

### Examples
See [references/real-examples.md](references/real-examples.md) for:
- Well-structured packages ([hello](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/he/hello/package.nix), [ripgrep](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/ri/ripgrep/package.nix), [bat](https://github.com/NixOS/nixpkgs/blob/master/pkgs/by-name/ba/bat/package.nix))
- Exemplary modules ([nginx](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/services/web-servers/nginx/default.nix), [postgresql](https://github.com/NixOS/nixpkgs/blob/master/nixos/modules/services/databases/postgresql.nix))
- Well-reviewed PRs

### Code Patterns
See [references/code-patterns.md](references/code-patterns.md) for complete templates:
- Package derivations (with finalAttrs pattern)
- NixOS modules (with security hardening)
- Flakes (with proper structure)
- Binary packages (with sourceProvenance)

### Common Mistakes
See [references/common-mistakes.md](references/common-mistakes.md) for before/after examples of:
- Package structure mistakes
- Testing mistakes
- Metadata mistakes
- Module mistakes
- Formatting mistakes
- Breaking change mistakes
- Platform-specific mistakes

## Community Resources

- [NixOS Discourse](https://discourse.nixos.org/) - Ask questions
- [NixOS Wiki](https://wiki.nixos.org/) - Community knowledge
- [Matrix: #nixos](https://matrix.to/#/#nixos:nixos.org) - Real-time chat
- [Matrix: #nixpkgs](https://matrix.to/#/#nixpkgs:nixos.org) - Package contributions
- [search.nixos.org](https://search.nixos.org/) - Search packages and options

## Integration

**Pre-commit hooks:**
```nix
# flake.nix
{
  devShells.default = pkgs.mkShell {
    packages = [ pkgs.nixfmt-rfc-style ];
  };
}
```

**CI validation:**
```bash
nixfmt --check **/*.nix  # Formatting
nix-build -A package     # Build
nix-build -A package.tests  # Tests
```

**Editor integration:**
- VSCode: [`jnoortheen.nix-ide`](https://marketplace.visualstudio.com/items?itemName=jnoortheen.nix-ide)
- Neovim: [null-ls](https://github.com/jose-elias-alvarez/null-ls.nvim) or [conform.nvim](https://github.com/stevearc/conform.nvim)
- Emacs: [nix-mode](https://github.com/NixOS/nix-mode)

## Nix Linting Tools

Beyond formatting, run these to catch anti-patterns and dead code:

```bash
statix check .          # Lint for anti-patterns (eta reduction, useless parens, manual inherit)
deadnix .               # Find unused variable bindings
nixfmt --check **/*.nix # Verify formatting matches RFC 166
```

For nixpkgs contributions, also run `nixpkgs-review pr <number>` to build affected packages.

See [references/nix-linting-tools.md](references/nix-linting-tools.md) for install commands, pre-commit integration, and detailed tool guidance.

## Writing Style

Review comments for nixpkgs contributions should be clear and constructive. Apply `natural-writing-style`:

- Reference specific RFC numbers and section citations, not vague "best practices"
- Don't claim a derivation is "fully compliant" — state which RFCs you checked against
- Use contractions naturally; the tone should be collegial, not bureaucratic
- Be direct about blockers vs. suggestions — reviewers need to know what must change

## Output Format

When reporting issues:

**Issue: [Category] (RFC XXX)**

Current:
```nix
# problematic code
```

Expected:
```nix
# fixed code
```

Why: [Brief explanation with RFC link]

**Categories:**
- Structure ([RFC 0140](https://github.com/NixOS/rfcs/blob/master/rfcs/0140-simple-package-paths.md))
- Metadata ([RFC 0089](https://github.com/NixOS/rfcs/blob/master/rfcs/0089-collect-non-source-package-meta.md))
- Testing ([RFC 0119](https://github.com/NixOS/rfcs/blob/master/rfcs/0119-testing-conventions.md))
- Documentation ([RFC 0145](https://github.com/NixOS/rfcs/blob/master/rfcs/0145-doc-strings.md))
- Formatting ([RFC 0166](https://github.com/NixOS/rfcs/blob/master/rfcs/0166-nix-formatting.md))
- Breaking Changes ([RFC 0088](https://github.com/NixOS/rfcs/blob/master/rfcs/0088-nixpkgs-breaking-change-policy.md))
