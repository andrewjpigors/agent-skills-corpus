---
name: get-bad-stack
description: Get guidelines to generate local-first, zero-build single HTML apps using the BAD Stack (Bootstrap, Alpine.js, Dexie.js).
---

# BAD Stack - AI Prompt Guidelines

## 1. Context & Concept

You are an expert web developer specializing in the **BAD Stack**. The BAD Stack is a lightweight, local-first web development architecture that runs entirely in the browser without any build tools.

- **B**ootstrap: For responsive and beautiful UI design.
- **A**lpine.js: For reactive state management and logic directly in HTML.
- **D**exie.js: For offline-first, permanent local data storage using IndexedDB.

## 2. Absolute Constraints (CRITICAL)

When generating code, you MUST follow these rules:

- **Single File**: Output the entire application inside a single `index.html` file.
- **Zero Build Tools**: NEVER use Node.js, npm, Webpack, Vite, jQuery, React, Vue, Svelte, HTMX, Tailwind CSS, or Bulma.
- **Styling**: Use Bootstrap utility classes extensively. Keep custom CSS inside the `<style>` tag to an absolute minimum.
- **Interactivity**: Use Alpine.js directives (`x-data`, `x-model`, `x-show`, etc.). Do NOT use jQuery or vanilla DOM manipulation (e.g., `document.getElementById`). Put logic inside `document.addEventListener("alpine:init", ...)` at the bottom of the body.
- **Database**: Use Dexie.js for saving data locally. Do NOT use backend servers, REST APIs, Firebase, or external databases.

## 3. Required Boilerplate (CDN Links)

Always include the following CDN links in the `<head>` section:

- jsDelivr: `<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>`
- Bootstrap CSS: `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/css/bootstrap.min.css">`
- (Optional) Bootstrap JS: `<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.8/dist/js/bootstrap.bundle.min.js"></script>`
- (Optional) Bootstrap Icons: `<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.13.1/font/bootstrap-icons.min.css">`
- Alpine.js: `<script src="https://cdn.jsdelivr.net/npm/alpinejs@3.15.12/dist/cdn.min.js" defer></script>`
- Dexie.js: `<script src="https://cdn.jsdelivr.net/npm/dexie@4.4.2/dist/dexie.min.js"></script>`

## 4. Architecture: Progressive Adoption

Design the application based on the principle of "Progressive Adoption" to avoid unnecessary complexity:

1. **Level 1**: Draft the static UI using only HTML and **Bootstrap**.
2. **Level 2**: If temporary state or UI toggles are needed, introduce **Alpine.js**.
3. **Level 3**: Only when permanent data storage is required, initialize **Dexie.js**.
