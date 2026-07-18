---
name: tailwind-react
description: Use when building React components with Tailwind CSS v4 and react-twc (TWC). Tailwind v4 only. Covers CSS-first configuration with @theme, design tokens, component creation with twc tagged templates, transient-prop variants via TwcComponentProps, dark mode, animations, and the asChild pattern. Use this skill whenever the user mentions Tailwind v4, TWC, react-twc, twc components, CSS-first Tailwind configuration, @theme blocks, or is building React UI components with Tailwind — even if they don't explicitly name TWC.
---

# Tailwind CSS v4 + react-twc

Build production-ready React components using Tailwind CSS v4's CSS-first configuration and react-twc for minimal boilerplate.

**Key docs:** [Tailwind v4](https://tailwindcss.com/docs) | [react-twc](https://react-twc.vercel.app)

## When to Use This Skill

- Creating React components styled with Tailwind CSS v4
- Setting up Tailwind v4 CSS-first configuration (`@theme`, `@import "tailwindcss"`)
- Using react-twc (`twc`) to create typed, reusable styled components
- Implementing design tokens, theming, and dark mode
- Building component variants with TWC transient props (`TwcComponentProps`)

## Required Reading

Before implementing, ALWAYS read these references:
- [references/advanced-patterns.md](references/advanced-patterns.md) - Animations, dark mode, custom utilities, theme modifiers, best practices

## Core Workflow

1. Read references - Review advanced-patterns.md for advanced patterns
2. Set up Tailwind - CSS-first config with `@theme`, semantic tokens in OKLCH
3. Configure TWC - Create `twx` instance with `tailwind-merge` for class conflict resolution
4. Build components - Use `twx` tagged templates; for variants, use `TwcComponentProps` with `$`-prefixed transient props
5. Add theming - Dark mode via `@custom-variant`, theme provider
6. Ensure accessibility - ARIA attributes, focus states, keyboard navigation

## CSS Configuration

```css
/* app.css */
@import "tailwindcss";

@theme {
  /* Semantic color tokens using OKLCH */
  --color-background: oklch(100% 0 0);
  --color-foreground: oklch(14.5% 0.025 264);

  --color-primary: oklch(14.5% 0.025 264);
  --color-primary-foreground: oklch(98% 0.01 264);

  --color-secondary: oklch(96% 0.01 264);
  --color-secondary-foreground: oklch(14.5% 0.025 264);

  --color-muted: oklch(96% 0.01 264);
  --color-muted-foreground: oklch(46% 0.02 264);

  --color-accent: oklch(96% 0.01 264);
  --color-accent-foreground: oklch(14.5% 0.025 264);

  --color-destructive: oklch(53% 0.22 27);
  --color-destructive-foreground: oklch(98% 0.01 264);

  --color-border: oklch(91% 0.01 264);
  --color-ring: oklch(14.5% 0.025 264);

  --color-card: oklch(100% 0 0);
  --color-card-foreground: oklch(14.5% 0.025 264);

  /* Radius tokens */
  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;
  --radius-xl: 0.75rem;

  /* Animation tokens */
  --animate-fade-in: fade-in 0.2s ease-out;
  --animate-fade-out: fade-out 0.2s ease-in;
  --animate-slide-in: slide-in 0.3s ease-out;

  @keyframes fade-in {
    from { opacity: 0; }
    to { opacity: 1; }
  }

  @keyframes fade-out {
    from { opacity: 1; }
    to { opacity: 0; }
  }

  @keyframes slide-in {
    from { transform: translateY(-0.5rem); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
  }
}

/* Class-based dark mode */
@custom-variant dark (&:where(.dark, .dark *));

.dark {
  --color-background: oklch(14.5% 0.025 264);
  --color-foreground: oklch(98% 0.01 264);
  --color-primary: oklch(98% 0.01 264);
  --color-primary-foreground: oklch(14.5% 0.025 264);
  --color-secondary: oklch(22% 0.02 264);
  --color-secondary-foreground: oklch(98% 0.01 264);
  --color-muted: oklch(22% 0.02 264);
  --color-muted-foreground: oklch(65% 0.02 264);
  --color-accent: oklch(22% 0.02 264);
  --color-accent-foreground: oklch(98% 0.01 264);
  --color-destructive: oklch(42% 0.15 27);
  --color-destructive-foreground: oklch(98% 0.01 264);
  --color-border: oklch(22% 0.02 264);
  --color-ring: oklch(83% 0.02 264);
  --color-card: oklch(14.5% 0.025 264);
  --color-card-foreground: oklch(98% 0.01 264);
}

@layer base {
  * {
    @apply border-border;
  }
  body {
    @apply bg-background text-foreground antialiased;
  }
}
```

## TWC Setup with tailwind-merge

Always configure a custom TWC instance with `tailwind-merge` and `clsx` so consumers can override classes without conflicts. The `cn` helper stays internal — all class merging goes through `twx`:

```typescript
// lib/twx.ts
import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { createTwc } from "react-twc";

function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const twx = createTwc({ compose: cn });
```

### Never Use clsx or cva Directly

- **`clsx` is only used inside `lib/twx.ts`** — it must not be imported anywhere else in the codebase. Never re-export `cn`, never build wrapper helpers around `clsx`.
- **Never import `classnames` or `class-variance-authority` (cva)** anywhere in the codebase. Do not add them to `package.json`.
- **All conditional/dynamic styling must go through `twx`** (or raw `twc` if `twx` is unavailable). Use Pattern 2 (dynamic styling via array-returning function) for conditional classes, and Pattern 3 (`.attrs()`) for default HTML attributes.
- **For variant components**, use `TwcComponentProps` with `$`-prefixed transient props and the array-return form of `twx` — this replaces every use case of `cva`.
- **Inline conditional classes in JSX** (`className={isActive ? "..." : "..."}`) are only acceptable for a single boolean toggle. Anything more complex must be lifted into a `twx` component.

## Component Patterns

### Pattern 1: Simple TWC Components

The simplest pattern — one-liner styled components with full ref forwarding and className merging:

```typescript
// components/ui/card.tsx
import { twx } from "@/lib/twx";

export const Card = twx.div`rounded-lg border border-border bg-card text-card-foreground shadow-sm`;
export const CardHeader = twx.div`flex flex-col space-y-1.5 p-6`;
export const CardTitle = twx.h3`text-2xl font-semibold leading-none tracking-tight`;
export const CardDescription = twx.p`text-sm text-muted-foreground`;
export const CardContent = twx.div`p-6 pt-0`;
export const CardFooter = twx.div`flex items-center p-6 pt-0`;

// Usage — className overrides are merged cleanly via tailwind-merge
<Card className="shadow-lg">
  <CardHeader>
    <CardTitle>Account</CardTitle>
    <CardDescription>Manage your settings</CardDescription>
  </CardHeader>
  <CardContent>...</CardContent>
</Card>
```

### Pattern 2: Dynamic Styling Based on Props

For conditional styling beyond variants, pass a function that returns class arrays:

```typescript
import { twx } from "@/lib/twx";
import { TwcComponentProps } from "react-twc";

type BadgeProps = TwcComponentProps<"span"> & {
  $status?: "success" | "warning" | "error" | "info";
};

export const Badge = twx.span<BadgeProps>((props) => [
  "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold",
  props.$status === "success" && "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
  props.$status === "warning" && "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
  props.$status === "error" && "bg-red-100 text-red-800 dark:bg-red-900 dark:text-red-200",
  props.$status === "info" && "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
  !props.$status && "bg-secondary text-secondary-foreground",
]);

// Usage
<Badge $status="success">Active</Badge>
```

### Pattern 3: TWC with Additional Attributes

Use `.attrs()` to set default HTML attributes, keeping components self-contained:

```typescript
// components/ui/input.tsx
import { twx } from "@/lib/twx";

export const Input = twx.input`flex h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50`;

export const Checkbox = twx.input.attrs({
  type: "checkbox",
})`appearance-none size-4 border-2 border-primary rounded-sm bg-white checked:bg-primary checked:border-primary focus-visible:ring-2 focus-visible:ring-ring`;

// External link with automatic rel/target
import { TwcComponentProps } from "react-twc";

type ExternalLinkProps = TwcComponentProps<"a"> & { $external?: boolean };

export const Anchor = twx.a.attrs<ExternalLinkProps>((props) =>
  props.$external ? { target: "_blank", rel: "noopener noreferrer" } : {}
)`underline text-primary hover:text-primary/80`;
```

### Pattern 4: TWC with asChild (Polymorphism)

Use `asChild` to apply TWC styles to a different underlying component — useful for routing links, Radix primitives, etc:

```typescript
import { twx } from "@/lib/twx";
import NextLink from "next/link";

export const StyledLink = twx.a`underline text-primary hover:text-primary/80 transition-colors`;

// Renders as Next.js Link but with StyledLink's classes
<StyledLink asChild>
  <NextLink href="/dashboard">Dashboard</NextLink>
</StyledLink>
```

### Pattern 5: TWC Wrapping Third-Party Components

TWC can wrap any React component, not just HTML elements:

```typescript
import { twx } from "@/lib/twx";
import * as DialogPrimitive from "@radix-ui/react-dialog";

export const DialogOverlay = twx(
  DialogPrimitive.Overlay
)`fixed inset-0 z-50 bg-black/80 data-[state=open]:animate-fade-in data-[state=closed]:animate-fade-out`;

export const DialogContent = twx(
  DialogPrimitive.Content
)`fixed left-1/2 top-1/2 z-50 grid w-full max-w-lg -translate-x-1/2 -translate-y-1/2 gap-4 border border-border bg-background p-6 shadow-lg sm:rounded-lg data-[state=open]:animate-fade-in data-[state=closed]:animate-fade-out`;
```

## Reference Guide

| File | Topics |
|------|--------|
| [references/advanced-patterns.md](references/advanced-patterns.md) | Animations, dark mode provider, custom @utility, theme modifiers, best practices |

<!-- Inspired by wshobson/agents — plugins/frontend-mobile-development/skills/tailwind-design-system -->
