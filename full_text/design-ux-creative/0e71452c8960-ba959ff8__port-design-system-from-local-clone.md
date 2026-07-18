---
name: port-design-system-from-local-clone
description: "CLON LITERAL PIXEL-PERFECT v6.0 FINAL. DS-FIRST + SCRIPTS EMBEBIDOS: analiza el repo DS local antes de cualquier código, luego ejecuta los 23 scripts RAW en MCP (código embebido — nunca inventar). Usa EXCLUSIVAMENTE cn() + CVA + tokens @theme inline. Nunca screenshots como evidencia. Scope flexible: página única, lista o sitio completo. Declaración de fidelidad numérica obligatoria. Fidelidad < 0.5% o FAIL."
---

# /port-design-system-from-local-clone v6.0 FINAL

## 0. PROMPT MAESTRO — INSTRUCCIÓN PRINCIPAL

> Se aplica antes que cualquier otra regla. Nunca se resume, nunca se salta.

**ROLE**: Clonador web pixel-perfect con disciplina de design system.

**Misión dual**:
- (A) El target debe ser INDISTINGUIBLE del source — tolerancia cero.
- (B) Construido EXCLUSIVAMENTE con los componentes y tokens del DS del repo target.

**Protocolo anti-atajos** (leer antes de cada acción):
- ❌ NUNCA usar `take_screenshot` como fuente de verdad de layout, animaciones o scroll.
- ❌ NUNCA inventar output de un script — ejecutarlo en MCP y esperar el JSON real.
- ❌ NUNCA avanzar de fase sin completar la fase actual.
- ❌ NUNCA escribir código antes de completar FASE 0.5 + FASE 0.6 + FASE 1.
- ✅ SIEMPRE usar `mcp__chrome-devtools__evaluate_script` para ejecutar scripts en browser.
- ✅ SIEMPRE esperar el JSON real de cada script antes de continuar.
- ✅ SIEMPRE declarar fidelidad estimada antes de FASE 3.

**Auto-detección de atajos**: Si en cualquier momento te encuentras a punto de:
- Escribir código sin haber visto JSON de extracción real → STOP → ejecutar script primero
- Usar un screenshot para verificar scroll/animación → STOP → ejecutar `recordScrollBehavior()` en MCP
- Inventar un valor CSS sin referencia en los JSONs → STOP → `getComputedStyle` en MCP

---

## 1. INVOCACIÓN

```txt
/port-design-system-from-local-clone "<target-path>" "<source-url>" [scope]
```

**scope** (opcional):
- Omitido o `all` → descubrir todas las páginas automáticamente (crawler + sitemap)
- `/` o `home` → solo homepage
- `/about,/services,/contact` → páginas específicas (separadas por coma)
- `single` → solo la URL exacta proporcionada, sin crawler

Ejemplos:
```txt
/port-design-system-from-local-clone "/Users/javi/granja" "https://jobyaviation.com" all
/port-design-system-from-local-clone "/Users/javi/granja" "https://jobyaviation.com" /
/port-design-system-from-local-clone "/Users/javi/granja" "https://jobyaviation.com" /,/aircraft,/about
```

---

## 2. REGLA ABSOLUTA — TOLERANCIA CERO

La source-url es la ÚNICA fuente de verdad visual. Criterios de FAIL numérico:

- Color / backgroundColor fuera de match exacto → FAIL
- fontFamily distinto, fontSize delta > 0px, fontWeight distinto → FAIL
- padding / margin / gap delta > 0px → FAIL
- transform / opacity / filter / boxShadow / borderRadius delta medible → FAIL
- Animación ausente o duration/easing/delay distintos → FAIL
- Hover/focus/active sin mismos valores computados → FAIL
- Scroll sin el mismo efecto (parallax, pin, video scrub, CSS var update) → FAIL
- Layout grid/flex con columnas, gap, orden o alignment distintos → FAIL
- Responsive con layout diferente en mobile/tablet → FAIL
- Diferencia visual > 0.5% en cualquier viewport o scroll position → FAIL

---

## 3. QUÉ SE CONSERVA — INMUTABLE

**DISEÑO** (100% del source): CSS tokens, custom properties, tipografía, colores, espaciado, sombras, gradientes, border-radius, z-index, breakpoints, grid/flexbox layout, animaciones, assets decorativos, hover/focus/active states, dark mode tokens, @font-face, estructura JSX, keyframes, IntersectionObserver configs, RAF loops, scroll-driven CSS variables, pseudo-elements.

**TEXTO Y NEGOCIO** (100% del target): Strings visibles en UI, hrefs de negocio, nombres del negocio, rutas, API routes, server actions, auth, middleware, DB, env vars.

**BACKEND = INTOCABLE.** `app/api/*`, `middleware.ts`, `server/*`, `auth/*`, `db/*` → STOP INMEDIATO.

---

## 4. REGLA DS-FIRST — CRÍTICA

### 4.1 Prohibiciones absolutas

- ❌ Copiar class names del source en JSX (ej: `"Navigation-module__abc123"`)
- ❌ Crear archivos `.css` o `.module.css` con clases extraídas del source
- ❌ Instalar librerías sin aprobación explícita del usuario
- ❌ Valores hardcodeados no extraídos de los JSONs de extracción

### 4.2 Obligaciones absolutas

- ✅ Tokens del source → `globals.css` bloque `@theme inline` con prefijo `pds-`
- ✅ Keyframes del source → `globals.css` con prefijo `pds-` + valores EXACTOS
- ✅ `cn()` de `src/lib/utils.ts` para composición de clases
- ✅ CVA para variantes de cada componente nuevo
- ✅ Reutilizar / extender componentes DS existentes
- ✅ `next/font` para fuentes
- ✅ Dynamic imports (`ssr: false`) para libs pesadas

### 4.3 Patrón DS correcto

```tsx
// ❌ NUNCA:
<section className="SectionHeroMedia-module__abc123">

// ✅ SIEMPRE:
const heroVariants = cva("relative w-full overflow-hidden", {
  variants: {
    theme: { dark: "bg-pds-dark-blue text-pds-white", light: "bg-pds-white text-pds-black" },
    height: { full: "h-dvh", auto: "h-auto min-h-dvh" }
  },
  defaultVariants: { theme: "dark", height: "full" }
})
export function HeroSection({ theme, height, className, children }: HeroSectionProps) {
  return <section className={cn(heroVariants({ theme, height }), className)}>{children}</section>
}
```

---

## 5. MCP TOOL MAPPING — NUNCA IMPROVISAR

| Acción | Tool MCP a usar |
|---|---|
| Ejecutar script en browser (source) | `mcp__chrome-devtools__evaluate_script` en tab source |
| Ejecutar script en browser (target) | `mcp__chrome-devtools__evaluate_script` en tab target |
| Navegar a URL | `mcp__chrome-devtools__navigate_page` |
| Abrir nueva pestaña | `mcp__chrome-devtools__new_page` |
| Cambiar tamaño viewport | `mcp__chrome-devtools__emulate` |
| Screenshot (solo evidencia visual humana) | `mcp__chrome-devtools__take_screenshot` |
| Ver consola JS | `mcp__chrome-devtools__list_console_messages` |
| Ver requests de red | `mcp__chrome-devtools__list_network_requests` |

**Regla de oro**: Si el output de un `evaluate_script` es `undefined` o error → reportar el error exacto al usuario, NO inventar el resultado.

---

## 6. CHECKLIST BLOQUEANTE — MOSTRAR EN CADA RESPUESTA

```
CHECKLIST DS-FIRST PIXEL-PERFECT v6.0

FASE 0.5 — ANÁLISIS DS LOCAL:
[ ] src/components/** leído con Glob + Read
[ ] globals.css leído — tokens @theme inline inventariados
[ ] package.json leído — animation libs detectadas
[ ] src/hooks/** leído
[ ] ds-component-map.json generado y guardado

FASE 0.6 — RAW SOURCE:
[ ] preExpandContent() ejecutado en MCP (output JSON real recibido)
[ ] Script RAW maestro ejecutado en MCP (JSON real recibido)
[ ] allCSS capturado (o CORS_BLOCKED documentado)

FASE 1 — 23 SCRIPTS:
[ ] extractFullDesignSystem() → JSON real recibido
[ ] detectAnimationImplementation() → JSON real recibido — BLOQUEANTE
[ ] extractAnimationSystem() → JSON real recibido
[ ] recordScrollBehavior() source → JSON real recibido — BLOQUEANTE
[ ] extractSectionInventory() → JSON real recibido — BLOQUEANTE
[ ] extractDeepVisualFingerprint() → JSON real recibido
[ ] Restantes 17 scripts ejecutados

POST FASE 1:
[ ] ds-section-mapping.json generado
[ ] ANIMATION_MANIFEST.md generado
[ ] Fidelidad estimada declarada (visual %, behavioral %)

VIEWPORTS (Fase 4):
[ ] 1920x1080 — 21 scroll positions — getComputedStyle todos los visibles
[ ] 768x1024  — 21 scroll positions
[ ] 375x812   — 21 scroll positions

DS-FIRST:
[ ] Tokens source en @theme inline con prefijo pds-
[ ] Cero class names del source en JSX
[ ] Cero .css/.module.css externos
[ ] KEY-MAPPINGS table en esta respuesta

QA:
[ ] compareScrollBehavior() passRate >= 95%
[ ] Build PASS (exit 0, cero errores TS)
[ ] Consola JS: cero errores
[ ] Diferencia visual < 0.5% en 3 viewports
```

Si cualquier ítem en ❌ o ⚠️: `STATUS: NO APROBADO — razón: <descripción numérica>`.

---

## 7. KEY-MAPPINGS — OBLIGATORIO EN CADA RESPUESTA CON CÓDIGO

```markdown
| Sección Source | Componente DS | Tokens (source → pds-) | Animación | Gap / Solución |
|---|---|---|---|---|
| SectionHeroMedia | src/components/sections/HeroSection.tsx (nuevo CVA) | --color-dark-blue → --color-pds-dark-blue | GSAP ScrollTrigger scrub | ✅ gsap instalado |
| Navigation | src/components/layout/Nav.tsx (nuevo CVA) | --color-white → --color-pds-white | CSS transition 200ms | JS scroll nativo |
| Button CTA | <Button> + variante pds-cta en buttonVariants | --color-orange → --color-pds-orange | CSS transition ease | ✅ DS nativo |
```

---

## 8. VIEWPORTS — BLOQUEANTES

| Viewport | Ancho | Alto | Device |
|---|---|---|---|
| Desktop | 1920 | 1080 | Full emulation |
| Tablet | 768 | 1024 | iPad emulation |
| Mobile | 375 | 812 | iPhone emulation |

Emular con `mcp__chrome-devtools__emulate`. Los tres son BLOQUEANTES.

---

## 9. FASE 0 — SETUP

### 9.1 Dual MCP

```
MCP-REF (source):   tab 1 → <source-url>
MCP-TARGET (target): tab 2 → http://localhost:3001
```

Abrir con `mcp__chrome-devtools__new_page` + `mcp__chrome-devtools__navigate_page`. Mantener abiertos hasta `MIGRATION_COMPLETE.md`.

### 9.2 Scope → PAGE_MAPPING.md

Según el parámetro `scope`:
- `all`: crawler `<a href>` + `fetch('/sitemap.xml')`. MAX_PAGES=50, MAX_DEPTH=3.
- Lista de paths: usar directamente.
- `single` / `home`: solo la URL base.

Output: `PAGE_MAPPING.md` — BLOQUEANTE para cualquier código.

### 9.3 Anti-bot + recovery

- Cloudflare/hCaptcha: esperar 10s. Si persiste, reportar. NUNCA bypassear.
- MCP crash: volcar `docs/pds/extraction/_checkpoint.json` con `{lastPhase, lastScript, lastPage, completedPages, timestamp}`.

---

## 10. FASE 0.5 — ANÁLISIS PROFUNDO DEL REPO LOCAL (BLOQUEANTE)

Ejecutar con herramientas de archivos (Read, Glob, Grep) — NO en browser.
Sin `ds-component-map.json` completo: NO avanzar.

### 10.1 Pasos

```bash
# A. Inventario de componentes
Glob: src/components/**/*.tsx
→ Para cada archivo: Read → extraer exports, props, variantes CVA, primitivos base

# B. Tokens del DS
Read: src/app/globals.css
→ Extraer bloque @theme inline completo
→ Identificar: --color-*, --radius-*, --font-*, --spacing-*, easing functions

# C. Animation libs instaladas
Read: package.json
→ Grep: gsap, @gsap/, lenis, framer-motion, motion, rive-canvas, @rive-app/, lottie-web, three, @react-three/

# D. Hooks y utilities
Glob: src/hooks/**/*.{ts,tsx}
Glob: src/lib/**/*.{ts,tsx}
→ Detectar: useScrollProgress, useGSAP, useInView, cn, etc.
```

### 10.2 ds-component-map.json

```json
{
  "_metadata": { "version": "6.0", "timestamp": "...", "targetPath": "..." },
  "dsComponents": [
    {
      "path": "src/components/ui/button.tsx",
      "exports": ["Button", "buttonVariants"],
      "variants": { "variant": ["default","outline","secondary","ghost","destructive","link"], "size": ["default","xs","sm","lg","icon"] },
      "canExtendWith": ["pds-cta", "pds-ghost-dark"],
      "primitive": "@base-ui/react/button"
    }
  ],
  "dsTokenSystem": { "type": "tailwind-v4-theme-inline", "colors": [], "radius": [], "fonts": [] },
  "dsAnimationLibs": [],
  "dsHooks": [],
  "tailwindVersion": 4
}
```

---

## 11. FASE 0.6 — INSPECCIÓN RAW SOURCE (BLOQUEANTE)

### 11.1 preExpandContent — ejecutar PRIMERO en MCP-REF

```javascript
// Ejecutar via: mcp__chrome-devtools__evaluate_script
(async () => {
  const steps = Array.from({length: 20}, (_, i) => (i + 1) * 0.05);
  for (const pct of steps) {
    window.scrollTo({ top: document.body.scrollHeight * pct, behavior: 'instant' });
    await new Promise(r => setTimeout(r, 200));
  }
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    img.loading = 'eager';
    if (img.dataset.src) img.src = img.dataset.src;
    if (img.dataset.srcset) img.srcset = img.dataset.srcset;
  });
  document.querySelectorAll('video').forEach(v => {
    if (v.paused && v.readyState >= 2) v.play().catch(() => {});
  });
  window.scrollTo({ top: 0, behavior: 'instant' });
  await new Promise(r => setTimeout(r, 500));
  return { ok: true, finalHeight: document.body.scrollHeight, totalElements: document.querySelectorAll('*').length };
})();
```

Si `finalHeight` crece: re-ejecutar.

### 11.2 Script RAW maestro

```javascript
// Ejecutar via: mcp__chrome-devtools__evaluate_script
// Guardar output en: docs/pds/extraction/raw-extraction-<page>.json
(async () => {
  const data = {
    _metadata: { version: '6.0', url: location.href, timestamp: Date.now(), viewport: `${window.innerWidth}x${window.innerHeight}`, userAgent: navigator.userAgent },
    url: location.href, fullHTML: document.documentElement.outerHTML,
    allCSS: [], jsBehaviors: [], assets: [], scrollData: [], animations: []
  };
  for (let sheet of document.styleSheets) {
    try {
      if (sheet.href) {
        const css = await fetch(sheet.href).then(r => r.text()).catch(() => 'CORS_BLOCKED');
        data.allCSS.push({ href: sheet.href, content: css });
      } else if (sheet.cssRules) {
        let rules = '';
        for (let rule of sheet.cssRules) rules += rule.cssText + '\n';
        data.allCSS.push({ href: 'inline', content: rules });
      }
    } catch(e) {}
  }
  document.querySelectorAll('img,video,source,svg,audio').forEach(el => {
    if (el.src || el.currentSrc) data.assets.push(el.src || el.currentSrc);
  });
  const positions = Array.from({length: 21}, (_, i) => i * 0.05);
  for (let pos of positions) {
    window.scrollTo({ top: document.body.scrollHeight * pos, behavior: 'instant' });
    await new Promise(r => setTimeout(r, 150));
    data.scrollData.push({ scrollPercent: pos * 100, scrollY: window.scrollY,
      visibleElements: Array.from(document.querySelectorAll('*')).filter(el => el.getBoundingClientRect().height > 0).length });
  }
  window.scrollTo({ top: 0, behavior: 'instant' });
  return data;
})();
```

Campos obligatorios: `_metadata`, `url`, `fullHTML`, `allCSS`, `assets`, `scrollData`. Si falta alguno: STOP + re-ejecutar.

---

## 12. FASE 1 — 23 SCRIPTS RAW (código embebido para los 7 críticos)

Todos los scripts via `mcp__chrome-devtools__evaluate_script`. Todos los JSONs incluyen `_metadata`.

### SCRIPT 1: extractFullDesignSystem()

```javascript
// Output: docs/pds/extraction/design-tokens.json
(function extractFullDesignSystem() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, customProperties:{}, typography:{}, keyframes:{}, fontFaces:[], breakpoints:[], modernCSS:{} };

  // Custom properties de :root / html
  const rootStyles = getComputedStyle(document.documentElement);
  const allRules = Array.from(document.styleSheets).flatMap(s => { try { return Array.from(s.cssRules||[]); } catch { return []; } });
  allRules.filter(r => r.selectorText === ':root' || r.selectorText === 'html')
    .flatMap(r => Array.from(r.style))
    .forEach(prop => { if (prop.startsWith('--')) result.customProperties[prop] = rootStyles.getPropertyValue(prop).trim(); });

  // @keyframes
  allRules.forEach(rule => {
    if (rule.type === CSSRule.KEYFRAMES_RULE) {
      const frames = {};
      Array.from(rule.cssRules).forEach(kf => { frames[kf.keyText] = kf.cssText; });
      result.keyframes[rule.name] = frames;
    }
    if (rule.type === CSSRule.FONT_FACE_RULE) result.fontFaces.push(rule.cssText);
    if (rule.type === CSSRule.MEDIA_RULE) {
      const m = rule.conditionText || rule.media?.mediaText;
      if (m && !result.breakpoints.includes(m)) result.breakpoints.push(m);
    }
  });

  // Tipografía por selector
  ['h1','h2','h3','h4','p','a','button','span','label'].forEach(sel => {
    const el = document.querySelector(sel);
    if (!el) return;
    const cs = getComputedStyle(el);
    result.typography[sel] = { fontFamily:cs.fontFamily, fontSize:cs.fontSize, fontWeight:cs.fontWeight,
      lineHeight:cs.lineHeight, letterSpacing:cs.letterSpacing, textTransform:cs.textTransform,
      color:cs.color, fontVariationSettings:cs.fontVariationSettings };
  });

  // Modern CSS detection
  const cssText = allRules.map(r => r.cssText||'').join('\n');
  result.modernCSS = {
    usesDvh: cssText.includes('dvh'),
    usesLvh: cssText.includes('lvh'),
    usesColorMix: cssText.includes('color-mix('),
    usesAtProperty: allRules.some(r => r.type === 7),
    usesStartingStyle: cssText.includes('@starting-style'),
    usesWebkitTextStroke: cssText.includes('-webkit-text-stroke'),
    usesScrollTimeline: cssText.includes('scroll-timeline') || cssText.includes('animation-timeline'),
    usesViewTimeline: cssText.includes('view-timeline'),
    usesContainerQuery: allRules.some(r => r.type === CSSRule.SUPPORTS_RULE && r.conditionText?.includes('container')),
    scrollDrivenVars: (cssText.match(/--(progress|scroll-[a-z-]+|translate-[a-z-]*)[:\s]/g)||[]).map(m=>m.replace(/[:\s]/,''))
  };

  return result;
})();
```

### SCRIPT 20: detectAnimationImplementation() — BLOQUEANTE

```javascript
// Output: docs/pds/extraction/animation-implementation.json
// BLOQUEANTE: FASE 3 no puede comenzar sin este output real
(function detectAnimationImplementation() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, libraries:{}, nativePatterns:{}, cssPatterns:{}, recommendation:'' };

  // GSAP
  result.libraries.gsap = {
    present: typeof window.gsap !== 'undefined',
    version: window.gsap?.version || null,
    plugins: {
      ScrollTrigger: typeof window.ScrollTrigger !== 'undefined',
      ScrollSmoother: typeof window.ScrollSmoother !== 'undefined',
      SplitText: typeof window.SplitText !== 'undefined',
      Flip: typeof window.Flip !== 'undefined',
    },
    scrollTriggerInstances: window.ScrollTrigger ? ScrollTrigger.getAll().length : 0,
    scrollTriggerDetails: window.ScrollTrigger ? ScrollTrigger.getAll().map(st => ({
      trigger: st.trigger?.tagName?.toLowerCase() || 'unknown',
      start: st.vars?.start, end: st.vars?.end,
      scrub: st.vars?.scrub, pin: !!st.vars?.pin,
      toggleActions: st.vars?.toggleActions
    })) : []
  };

  // Lenis
  const lenisDetected = typeof window.Lenis !== 'undefined' || !!window.__lenis || !!document.querySelector('[data-lenis-prevent]');
  result.libraries.lenis = { present: lenisDetected, config: window.__lenis ? { duration: window.__lenis.duration, lerp: window.__lenis.lerp } : null };

  // Framer Motion
  result.libraries.framerMotion = { present: !!document.querySelector('[data-framer-appear-id],[data-framer-component-type]') };

  // CSS patterns
  const allCSS = Array.from(document.styleSheets).flatMap(s => { try { return Array.from(s.cssRules||[]); } catch { return []; } }).map(r=>r.cssText||'').join('\n');
  result.cssPatterns = {
    hasScrollTimeline: allCSS.includes('animation-timeline') || allCSS.includes('scroll-timeline'),
    hasViewTimeline: allCSS.includes('view-timeline'),
    hasScrollDrivenVars: /--progress|--scroll-|--translate-y/.test(allCSS),
    hasCSSKeyframes: !!document.querySelector('[class*="animate"], [class*="motion"]') || /animation:\s*\w/.test(allCSS)
  };

  // Native JS patterns
  result.nativePatterns = {
    hasVideoScrub: Array.from(document.querySelectorAll('video')).some(v => v.getBoundingClientRect().width >= window.innerWidth * 0.8),
    hasIntersectionObserver: !!window.IntersectionObserver,
    hasRAF: allCSS.includes('requestAnimationFrame') || false
  };

  // Recommendation
  if (result.libraries.gsap.present && result.libraries.gsap.plugins.ScrollTrigger) {
    result.recommendation = 'GSAP + ScrollTrigger — target MUST use GSAP. Substituting is FAIL.';
  } else if (result.libraries.gsap.present) {
    result.recommendation = 'GSAP (sin ScrollTrigger) — target debe usar GSAP.';
  } else if (lenisDetected) {
    result.recommendation = 'Lenis smooth scroll — target debe usar Lenis o equivalent scroll behavior.';
  } else if (result.cssPatterns.hasScrollTimeline) {
    result.recommendation = 'CSS Scroll-driven animations — replicar con CSS nativo, NO con JS.';
  } else if (result.cssPatterns.hasScrollDrivenVars) {
    result.recommendation = 'JS scroll listener actualizando CSS vars — replicar con hook nativo.';
  } else {
    result.recommendation = 'Native JS + CSS — replicar con IO + CSS transitions nativas.';
  }

  return result;
})();
```

### SCRIPT 19: recordScrollBehavior() — BLOQUEANTE

```javascript
// Output: docs/pds/extraction/scroll-behavior-<page>.json
// Ejecutar en MCP-REF (source) Y MCP-TARGET (target) por separado
// Usar clave ESTRUCTURAL (section[N], video[N]) — NUNCA CSS class name
(async function recordScrollBehavior() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, positions: [] };
  const totalScrollable = document.body.scrollHeight - window.innerHeight;

  for (let i = 0; i <= 20; i++) {
    const pct = i * 5;
    window.scrollTo({ top: totalScrollable * (pct / 100), behavior: 'instant' });
    await new Promise(r => setTimeout(r, 300));
    const snapshot = { scrollPercent: pct, scrollY: Math.round(window.scrollY), elements: {} };

    // Secciones por índice estructural
    document.querySelectorAll('section, [data-section], main > div, main > article').forEach((el, idx) => {
      const cs = getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      snapshot.elements[`section[${idx}]`] = {
        visible: rect.height > 0 && rect.bottom > 0 && rect.top < window.innerHeight,
        rect: { top: Math.round(rect.top), height: Math.round(rect.height) },
        backgroundColor: cs.backgroundColor,
        opacity: cs.opacity,
        transform: cs.transform,
        position: cs.position
      };
    });

    // Videos por índice estructural
    document.querySelectorAll('video').forEach((v, idx) => {
      snapshot.elements[`video[${idx}]`] = {
        currentTime: v.currentTime, paused: v.paused, duration: v.duration,
        rect: (() => { const r = v.getBoundingClientRect(); return { top: Math.round(r.top), height: Math.round(r.height) }; })()
      };
    });

    // Nav
    const nav = document.querySelector('nav, header');
    if (nav) {
      const cs = getComputedStyle(nav);
      snapshot.elements['nav[0]'] = {
        position: cs.position, backgroundColor: cs.backgroundColor,
        backdropFilter: cs.backdropFilter, transform: cs.transform, opacity: cs.opacity
      };
    }

    result.positions.push(snapshot);
  }

  window.scrollTo({ top: 0, behavior: 'instant' });
  return result;
})();
```

### SCRIPT para compareScrollBehavior() (ejecutar post-reconstrucción)

```javascript
// Pasar sourceData y targetData (los JSONs de recordScrollBehavior de source y target)
function compareScrollBehavior(sourceData, targetData) {
  const result = { passCount: 0, failCount: 0, passRate: 0, diffs: [] };
  const props = ['backgroundColor', 'opacity', 'transform', 'position'];

  sourceData.positions.forEach((srcPos, posIdx) => {
    const tgtPos = targetData.positions[posIdx];
    if (!tgtPos) { result.diffs.push({ pos: srcPos.scrollPercent, type: 'POSITION_MISSING' }); result.failCount++; return; }

    Object.keys(srcPos.elements).forEach(key => {
      const srcEl = srcPos.elements[key];
      const tgtEl = tgtPos.elements[key];
      if (!tgtEl) { result.diffs.push({ pos: srcPos.scrollPercent, key, type: 'ELEMENT_MISSING' }); result.failCount++; return; }

      props.forEach(prop => {
        const s = srcEl[prop], t = tgtEl[prop];
        if (s && t && s !== t) {
          result.diffs.push({ pos: srcPos.scrollPercent, key, prop, source: s, target: t, type: prop.toUpperCase() + '_MISMATCH' });
          result.failCount++;
        } else if (s === t) { result.passCount++; }
      });
    });
  });

  const total = result.passCount + result.failCount;
  result.passRate = total > 0 ? Math.round((result.passCount / total) * 100) : 0;
  result.pass = result.passRate >= 95;
  return result;
}
```

### SCRIPT 23: extractSectionInventory() — BLOQUEANTE

```javascript
// Output: docs/pds/extraction/section-inventory-<page>.json
(function extractSectionInventory() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, totalSections: 0, sections: [] };
  const totalPageHeight = document.body.scrollHeight;

  document.querySelectorAll('section, [data-section], main > div[class], main > article[class]').forEach((el, idx) => {
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    result.sections.push({
      index: idx, tag: el.tagName.toLowerCase(),
      heightPx: Math.round(rect.height),
      heightRatio: (rect.height / totalPageHeight).toFixed(3),
      backgroundColor: cs.backgroundColor,
      backgroundImage: cs.backgroundImage.substring(0, 150),
      display: cs.display,
      layoutType: cs.display.includes('grid') ? 'grid' : cs.display.includes('flex') ? 'flex' : 'block',
      gridTemplateColumns: cs.gridTemplateColumns,
      position: cs.position,
      hasVideo: !!el.querySelector('video'),
      hasCanvas: !!el.querySelector('canvas'),
      hasIframe: !!el.querySelector('iframe'),
      childCount: el.children.length
    });
  });

  result.totalSections = result.sections.length;
  return result;
})();
```

### SCRIPT 13: extractDeepVisualFingerprint() — SIN LÍMITE DE ELEMENTOS

```javascript
// Output: docs/pds/extraction/visual-fingerprint-<page>.json
// ADVERTENCIA: output puede ser muy grande. Usar con scroll position 0.
(function extractDeepVisualFingerprint() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, elements: [] };

  Array.from(document.querySelectorAll('*')).filter(el => {
    const r = el.getBoundingClientRect();
    return r.width > 0 && r.height > 0;
  }).forEach(el => {
    const cs = getComputedStyle(el);
    const rect = el.getBoundingClientRect();
    result.elements.push({
      tag: el.tagName.toLowerCase(), id: el.id || null,
      rect: { x:Math.round(rect.x), y:Math.round(rect.y), w:Math.round(rect.width), h:Math.round(rect.height) },
      styles: {
        color:cs.color, backgroundColor:cs.backgroundColor,
        fontFamily:cs.fontFamily, fontSize:cs.fontSize, fontWeight:cs.fontWeight,
        lineHeight:cs.lineHeight, letterSpacing:cs.letterSpacing,
        fontVariationSettings:cs.fontVariationSettings,
        padding:cs.padding, margin:cs.margin, gap:cs.gap,
        display:cs.display, gridTemplateColumns:cs.gridTemplateColumns, flexDirection:cs.flexDirection,
        position:cs.position, zIndex:cs.zIndex,
        transform:cs.transform, opacity:cs.opacity,
        borderRadius:cs.borderRadius, boxShadow:cs.boxShadow,
        filter:cs.filter, backdropFilter:cs.backdropFilter,
        transition:cs.transition, animation:cs.animation,
        clipPath:cs.clipPath, mixBlendMode:cs.mixBlendMode,
        maxWidth:cs.maxWidth, overflow:cs.overflow,
        textDecoration:cs.textDecoration,
        webkitTextStroke:cs.webkitTextStroke,
        touchAction:cs.touchAction, userSelect:cs.userSelect,
        containerType:cs.containerType, colorScheme:cs.colorScheme
      }
    });
  });

  return result;
})();
```

### SCRIPT 4: extractAnimationSystem()

```javascript
// Output: docs/pds/extraction/animations.json
(function extractAnimationSystem() {
  const meta = { version:'6.0', url:location.href, timestamp:Date.now(), viewport:`${window.innerWidth}x${window.innerHeight}`, userAgent:navigator.userAgent };
  const result = { _metadata: meta, gsap:null, lenis:null, cssKeyframes:{}, cssTransitions:[], cssScrollDriven:[], videoScrub:[], intersectionObservers:[] };
  const allRules = Array.from(document.styleSheets).flatMap(s => { try { return Array.from(s.cssRules||[]); } catch { return []; } });

  // GSAP detail
  if (window.gsap) {
    result.gsap = {
      version: gsap.version,
      scrollTriggers: window.ScrollTrigger ? ScrollTrigger.getAll().map(st => ({
        trigger: st.trigger?.tagName + (st.trigger?.className ? '.'+st.trigger.className.split(' ')[0] : ''),
        start: st.vars.start, end: st.vars.end, scrub: st.vars.scrub, pin: !!st.vars.pin,
        toggleActions: st.vars.toggleActions, markers: st.vars.markers
      })) : [],
      matchMedia: window.gsap.matchMedia ? true : false
    };
  }

  // Lenis
  if (window.__lenis) {
    result.lenis = { duration: window.__lenis.duration, easing: window.__lenis.easing?.toString().slice(0,100), lerp: window.__lenis.lerp };
  }

  // CSS keyframes + transitions
  allRules.forEach(rule => {
    if (rule.type === CSSRule.KEYFRAMES_RULE) {
      const frames = {};
      Array.from(rule.cssRules).forEach(kf => { frames[kf.keyText] = kf.cssText; });
      result.cssKeyframes[rule.name] = frames;
    }
    if (rule.style?.transition && rule.style.transition !== 'none 0s ease 0s') {
      result.cssTransitions.push({ selector: rule.selectorText, transition: rule.style.transition });
    }
    if (rule.cssText?.includes('animation-timeline') || rule.cssText?.includes('scroll-timeline')) {
      result.cssScrollDriven.push({ selector: rule.selectorText, rule: rule.cssText.slice(0,400) });
    }
  });

  // Video scrub
  document.querySelectorAll('video').forEach((v, idx) => {
    const rect = v.getBoundingClientRect();
    result.videoScrub.push({
      index: idx, src: v.src || v.currentSrc,
      coversViewport: rect.width >= window.innerWidth * 0.8,
      autoplay: v.autoplay, loop: v.loop, muted: v.muted, duration: v.duration
    });
  });

  return result;
})();
```

### Scripts restantes (16 sin código embebido — ejecutar igualmente)

| # | Script | Output |
|---|---|---|
| 2 | `fetchCrossOriginCSS()` | `cross-origin-css.json` |
| 3 | `extractShadowStyles()` | `shadow-styles.json` |
| 5 | `captureIntersectionObserverConfigs()` | dentro de `animations.json` |
| 6 | `extractLottieRiveSpline()` | `lottie-rive-spline.json` |
| 7 | `extractScrollScrubTrace()` | `scroll-scrub-trace-<page>.json` |
| 8 | `extractDOMStructure()` | `structure.json` |
| 9 | `extractInteractions()` | `interactions.json` |
| 10 | `extractAssets()` | `assets.json` |
| 11 | `extractThreeJSScene()` | `three-scene.json` |
| 12 | `extractDarkMode()` | `dark-mode.json` |
| 14 | `extractAdvancedPatterns()` | `advanced-patterns.json` |
| 15 | `extractFullCSSRules()` | `css-rules.json` |
| 16 | `extractScrollSnapshot()` | `scroll-snapshots-<page>.json` |
| 17 | `extractAccessibility()` | `accessibility.json` |
| 18 | Scroll narrative textual | `scroll-narrative-<page>.md` |
| 21 | `extractElementStyleMap()` | `element-style-map-<page>.json` |
| 22 | `extractNetworkProfile()` | `network-profile.json` |

Todos los JSONs incluyen `_metadata: { version, url, timestamp, viewport, userAgent }`.

**Deliverable BLOQUEANTE de FASE 1**: `ANIMATION_MANIFEST.md` con cada animación/efecto del source, tipo, valores numéricos.

---

## 13. POST FASE 1 — ds-section-mapping.json + Declaración de Fidelidad

### 13.1 ds-section-mapping.json

Cruzar datos de `section-inventory-<page>.json` + `animation-implementation.json` con `ds-component-map.json`:

```json
{
  "_metadata": { "version": "6.0", "timestamp": "...", "sourceUrl": "..." },
  "sections": {
    "SectionHeroMedia": {
      "sourceFeatures": ["full-viewport video", "GSAP ScrollTrigger scrub", "16-col grid"],
      "dsMapping": "NUEVO src/components/sections/HeroSection.tsx — CVA: theme, height",
      "dsTokensToAdd": ["--color-pds-dark-blue: #1c3f99", "--pds-base-padding: 4rem"],
      "dsComponentsReused": [],
      "dsAnimationStrategy": "GSAP ScrollTrigger — detectado en source. DS NO tiene gsap instalado → PROPUESTA: instalar gsap",
      "fidelityRisk": "HIGH — video scrub imposible sin GSAP o RAF nativo",
      "gapSolution": "Instalar gsap (preguntar usuario) o RAF nativo como fallback"
    }
  },
  "overallFidelityEstimate": { "visual": "XX%", "behavioral": "XX%", "gaps": [] }
}
```

### 13.2 Declaración de fidelidad OBLIGATORIA (antes de FASE 3)

```
FIDELIDAD ESTIMADA — <page>:
- Visual: XX% (razón si < 95%: ...)
- Behavioral (animaciones, scroll, hover): XX% (razón si < 90%: ...)
- Gaps declarados:
  1. [gap] — propuesta: [solución]
  2. ...
STATUS: APROBADO / REQUIERE DECISIÓN DEL USUARIO
```

Si visual < 95% o behavioral < 90%: STOP + esperar decisión antes de FASE 3.

---

## 14. FASE 2 — ANÁLISIS DEL TARGET

- Build baseline (`next build`) antes de tocar nada.
- Extracción de strings de texto del target.
- Detección de arquitectura: monorepo, i18n, Tailwind v3/v4, UI library.
- Verificar libs DS vs libs source (`animation-implementation.json`). Solo instalar si source las usa Y usuario aprueba.
- Renombrar font names del source brand.
- `target-architecture.json` obligatorio.

---

## 15. FASE 3 — RECONSTRUCCIÓN DS-FIRST

Orden: tokens → tailwind → fonts → animation libs → navbar → footer → páginas → compartidos.

### 15.1 Tokens en globals.css

```css
/* globals.css — DENTRO del bloque @theme inline existente */
@theme inline {
  /* ... tokens DS existentes ... */

  /* tokens source (prefijo pds-) — valores EXACTOS de design-tokens.json */
  --color-pds-white: #f5f4df;
  --color-pds-black: #0e1620;
  --color-pds-blue: #007ae5;
  --color-pds-dark-blue: #1c3f99;
  --color-pds-orange: #eb6110;
  --pds-ease-out-cubic: cubic-bezier(0.33, 1, 0.68, 1);
  --pds-ease-power4-inout: cubic-bezier(0.77, 0, 0.175, 1);
  --pds-ease-snappy: cubic-bezier(0.6, 0.6, 0, 1);
  --pds-base-padding: 4rem;
  --pds-gutter-width: 1.6rem;
}

/* Keyframes source — DESPUÉS del @theme block, con prefijo pds- */
@keyframes pds-fade-in { /* valores EXACTOS de cssKeyframes en animations.json */ }
@keyframes pds-translate-out-in-x { /* valores EXACTOS */ }
```

### 15.2 Animaciones — fidelidad de comportamiento

**Scroll JS listener → hook nativo** (cuando source usa JS para actualizar CSS vars):
```typescript
// src/hooks/usePdsScrollProgress.ts
'use client'
import { useEffect, type RefObject } from 'react'
export function usePdsScrollProgress(ref: RefObject<HTMLElement>) {
  useEffect(() => {
    const el = ref.current; if (!el) return
    const onScroll = () => {
      const rect = el.getBoundingClientRect()
      // Fórmula EXACTA del source (de jsBehaviors en raw-extraction.json)
      const progress = Math.max(0, Math.min(1, -rect.top / (rect.height - window.innerHeight)))
      el.style.setProperty('--progress', String(progress))
    }
    window.addEventListener('scroll', onScroll, { passive: true })
    return () => window.removeEventListener('scroll', onScroll)
  }, [ref])
}
```

**CSS scroll-driven** (cuando source usa `animation-timeline: scroll()`):
```css
/* Copiar LITERAL en globals.css — nunca reemplazar por JS */
.pds-section-scroll-driven {
  animation: pds-scroll-anim linear;
  animation-timeline: scroll();
  animation-range: 0% 100%;
}
```

**GSAP ScrollTrigger** (cuando DS lo tiene instalado):
```typescript
'use client'
import { useGSAP } from '@gsap/react'
import gsap from 'gsap'; import ScrollTrigger from 'gsap/ScrollTrigger'
gsap.registerPlugin(ScrollTrigger)
export function usePdsVideoScrub(containerRef: RefObject<HTMLElement>, videoRef: RefObject<HTMLVideoElement>) {
  useGSAP(() => {
    if (!containerRef.current || !videoRef.current) return
    ScrollTrigger.create({
      trigger: containerRef.current, start: 'top top', end: 'bottom bottom', scrub: true,
      // valores EXACTOS de scrollTriggerDetails en animation-implementation.json
      onUpdate: (self) => { if (videoRef.current) videoRef.current.currentTime = self.progress * (videoRef.current.duration || 0) }
    })
  }, { scope: containerRef })
}
```

**GSAP ScrollTrigger** (cuando DS NO lo tiene): → STOP. Declarar gap. Esperar aprobación.

**Botones / hover states** (valores EXACTOS de css-rules.json):
```tsx
// Extender buttonVariants con variante pds-cta
"pds-cta": [
  "bg-pds-orange text-pds-white",
  "transition-[color,background-color,opacity]",
  "duration-[200ms]",
  "ease-[var(--pds-ease-out-cubic)]",
  "hover:opacity-90"
].join(" "),
```

**IntersectionObserver** (valores EXACTOS de captureIntersectionObserverConfigs):
```typescript
const observer = new IntersectionObserver(callback, {
  threshold: [0.1], // EXACTO del source
  rootMargin: '0px 0px -100px 0px' // EXACTO del source
})
```

### 15.3 Assets — HOTLINK obligatorio

Por defecto: `<img src="https://source.com/assets/hero.jpg" />` (URL original del source).
CORS: descargar a `public/pds-source-assets/`.
Branding incrustado: hotlink + prompt IA en `docs/pds/assets-reemplazo-ia.md`.
CERO assets del target como diseño.

### 15.4 Loop por sección

1. INSPECT → leer JSONs de extracción
2. BUILD → JSX + tokens en globals.css
3. SWAP → reemplazar strings visibles con texto del target
4. BUILD verify → `next build` exit 0
5. VERIFY → `recordScrollBehavior()` source + target → `compareScrollBehavior()` passRate >= 95%

### 15.5 Next.js App Router

- `'use client'` si hay hooks / event handlers / browser APIs / animation libs
- Dynamic imports (`ssr: false`) para GSAP, Lenis, Three.js, Lottie, Rive
- `next/font` para todas las fuentes
- `next/image` con `sizes` y `priority`
- `suppressHydrationWarning` o `useIsClient` para prevenir hydration mismatch

### 15.6 Reglas de build

- BUILD-1: archivo modificado → build inmediato
- BUILD-2: falla → corregir antes de tocar otro
- BUILD-3: 3 fallos consecutivos en mismo archivo → STOP + reporte
- BUILD-4: cero imports de `.next/server/` o hashes
- BUILD-5: exit 0, cero errores TS, cero warnings nuevos

---

## 16. FASE 4 — QA PROGRAMÁTICA (GATE HUMANO ENTRE PÁGINAS)

### 16.1 Dual-MCP sync scroll

```javascript
// Ejecutar getComputedStyle comparativo en ambos MCPs
// En cada posición: delta en color, fontSize, padding, transform, opacity
// Si delta > 0.5%: STOP + corregir
```

### 16.2 recordScrollBehavior + compareScrollBehavior

- Ejecutar Script 19 en source Y target
- `compareScrollBehavior(sourceData, targetData)` → `passRate >= 95%`
- Guardar `docs/pds/extraction/scroll-behavior-diff-<page>.json`

### 16.3 Interactions testing

```javascript
// Por cada elemento interactivo en MCP-TARGET:
element.dispatchEvent(new MouseEvent('mouseover', { bubbles: true }));
await new Promise(r => setTimeout(r, 100));
const afterHover = getComputedStyle(element);
// Comparar con source hover state de css-rules.json
```

### 16.4 Motion trace

DOWN (0→100%) + UP (100→0%) para cada `video`, `canvas`, `STICKY`, `PARALLAX`, `PIN`.
Capturar `video.currentTime`, transforms, opacity. Delta ≤ 2%.

### 16.5 Verificaciones adicionales

- Consola JS: CERO errores (`mcp__chrome-devtools__list_console_messages`)
- Assets: 200 OK (`mcp__chrome-devtools__list_network_requests`)
- Stacking contexts, accesibilidad, `prefers-reduced-motion`

---

## 17. FASE 5 — RECORRIDO VISUAL FINAL (GATE HUMANO)

- 21 posiciones × 3 viewports por página
- Side-by-side source/target + diff numérico
- Bucle de corrección inmediata si delta > 0.5%
- `diff-report.md`
- Gate de aprobación humana explícita antes de `MIGRATION_COMPLETE.md`

---

## 18. FASE 6 — ENTREGABLES

```
PAGE_MAPPING.md
ANIMATION_MANIFEST.md
docs/pds/extraction/ds-component-map.json
docs/pds/extraction/ds-section-mapping.json
docs/pds/extraction/raw-extraction-*.json
docs/pds/extraction/design-tokens.json
docs/pds/extraction/animations.json
docs/pds/extraction/animation-implementation.json
docs/pds/extraction/section-inventory-*.json
docs/pds/extraction/visual-fingerprint-*.json
docs/pds/extraction/scroll-behavior-*.json
docs/pds/extraction/scroll-behavior-diff-*.json
docs/pds/extraction/structure.json
docs/pds/extraction/interactions.json
docs/pds/extraction/assets.json
docs/pds/extraction/css-rules.json
docs/pds/extraction/cross-origin-css.json
docs/pds/extraction/element-style-map-*.json
docs/pds/extraction/network-profile.json
docs/pds/extraction/scroll-scrub-trace-*.json
docs/pds/extraction/scroll-snapshots-*.json
docs/pds/extraction/scroll-narrative-*.md
docs/pds/extraction/advanced-patterns.json
docs/pds/extraction/accessibility.json
docs/pds/extraction/dark-mode.json
docs/pds/extraction/target-architecture.json
docs/pds/assets-reemplazo-ia.md
docs/pds/diff-report.md
docs/pds/qa-evidence/
MIGRATION_COMPLETE.md   (solo si TODO PASS)
```

---

## 19. STOP CONDITIONS DEFINITIVAS

**DS-First:**
- `ds-component-map.json` no generado → STOP
- `ds-section-mapping.json` no generado antes de FASE 3 → STOP
- Fidelidad estimada no declarada antes de FASE 3 → STOP
- Fidelidad < 95% visual o < 90% behavioral sin aprobación → STOP
- Class name del source copiado en JSX → STOP + refactorizar
- Archivo `.css`/`.module.css` externo creado → STOP + migrar
- Tokens fuera de `@theme inline` → STOP + mover
- Componente nuevo sin `cn()` + CVA → STOP + refactorizar
- KEY-MAPPINGS table ausente en respuesta con código → STOP + incluir
- Lib instalada sin aprobación del usuario → STOP + desinstalar

**Extracción:**
- Screenshot estático como única evidencia → STOP + ejecutar script en MCP
- JSON de extracción inventado (sin output real de MCP) → STOP + re-ejecutar
- `raw-extraction-<page>.json` incompleto → STOP
- JSON sin `_metadata` → STOP
- `detectAnimationImplementation()` no ejecutado → STOP (BLOQUEANTE FASE 3)
- `recordScrollBehavior()` no ejecutado → STOP
- `extractSectionInventory()` no ejecutado → STOP
- `preExpandContent()` no ejecutado → STOP
- Cross-origin CSS no extraída → STOP
- `PAGE_MAPPING.md` inexistente → STOP

**QA:**
- `compareScrollBehavior()` passRate < 95% → STOP + corregir
- Diferencia > 0.5% durante recorrido final → STOP + corregir
- Consola JS con errores → STOP + corregir
- Hydration mismatch → STOP + corregir
- 3 builds fallidos en mismo archivo → STOP + reporte
- Viewport faltante (3 obligatorios) → STOP
- Gate humano no obtenido entre páginas → STOP
- FASE 5 no completa antes de `MIGRATION_COMPLETE.md` → STOP

**Backend / estructura:**
- Archivo backend modificado → STOP INMEDIATO
- Section inventory mismatch → STOP
- Layout type mismatch (grid vs flex) → STOP
- Background color sección difiere → STOP
- `@starting-style` source sustituido por JS → STOP
- Source usa `100dvh` y target usa `100vh` → STOP
- `-webkit-text-stroke` source no replicado → STOP
- `ScrollSmoother` + `Lenis` simultáneamente → STOP
- Iframes/embeds source ausentes en target → STOP
- `detectAnimationImplementation()` ignorado (source usa GSAP, target no) → STOP

---

## 20. CRITERIOS DE COMPLETITUD

### Visual
- CERO diferencias > 0.5% en 3 viewports, 21 posiciones por página

### DS-First
- `ds-component-map.json` y `ds-section-mapping.json` usados en todas las decisiones
- Cero class names del source en JSX
- Todos los tokens en `@theme inline` con prefijo `pds-`
- Todos los componentes nuevos: `cn()` + CVA + Tailwind

### Animaciones
- `ANIMATION_MANIFEST.md` 100% verificado
- Video scrub: `currentTime` ligado a scroll
- Hover/focus/active: deltas 0 vs source
- Scroll-driven CSS vars: misma lógica que source
- Librería de animación: misma que source (o gap declarado y aprobado)
- `prefers-reduced-motion` respetado

### Técnico
- Build PASS, cero errores TS, cero warnings
- Consola JS: cero errores
- Assets source: hotlinkeados o descargados (cero assets del target)
- Backend intocable

---

## 21. CÓMO USAR — PASO A PASO

1. Dev server del target en `http://localhost:3001`
2. Chrome DevTools MCP conectado a un tab de Chrome
3. Invocar: `/port-design-system-from-local-clone "<target>" "<source>" [scope]`
4. **FASE 0**: Dual MCP + scope → PAGE_MAPPING.md
5. **FASE 0.5**: Análisis DS local (Read/Glob/Grep) → ds-component-map.json
6. **FASE 0.6**: preExpandContent() en MCP + script RAW → raw-extraction-<page>.json
7. **FASE 1**: 23 scripts en MCP (código embebido arriba para los 7 críticos)
8. **Post-FASE 1**: ds-section-mapping.json + declaración de fidelidad
9. **FASE 2**: Build baseline + arquitectura + target-architecture.json
10. **FASE 3**: tokens → tailwind → fonts → animation libs → navbar → footer → páginas
11. **FASE 4**: QA dual MCP (21 scroll × 3 viewports) — gate humano entre páginas
12. **FASE 5**: Recorrido visual final — gate humano
13. **FASE 6**: Entregables → MIGRATION_COMPLETE.md

En cada respuesta con código: CHECKLIST + KEY-MAPPINGS + STATUS.

---

## 22. MANTENIMIENTO

Fuente de verdad: `.claude/skills/port-design-system-from-local-clone/SKILL.md`
Sync: `node scripts/sync-skills.mjs && bash scripts/sync-agent-rules.sh`
