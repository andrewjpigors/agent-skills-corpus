---
name: desy-angular-translator
description: "Traduce código Nunjucks de desy-html a código Angular de desy-angular. Patrón general + tabla de equivalencias para los 15+ componentes más comunes. NO cubre los 57 — solo los que han sido validados."
---

# desy-angular-translator

Traduce código Nunjucks de la librería `desy-html` a código TypeScript + template de la librería `desy-angular`. Útil cuando:

- Tienes código `{{ componentX({...}) }}` que necesitas migrar a `<desy-x [prop]="value">`
- Estás aprendiendo las convenciones de `desy-angular` partiendo de tu conocimiento de `desy-html`
- Estás auditando código que mezcla ambos paradigmas

## Fuente de verdad

> "Normalmente, los parámetros de configuración y los diseños de componentes comienzan en desy-html y posteriormente se traducen a desy-angular. No obstante, desy-angular tiene algunos parámetros propios relativos a su implementación."
> — `desy.aragon.es/desarrollo-desy-angular.html.md`

**Implicación:** la traducción es la dirección canónica, no es 1:1.

## Cuándo usarla
- **Triggers:** *"traduce este Nunjucks a Angular"*, *"pásame este HTML a desy-angular"*, *"convierte este macro a `<desy-x>`"*, *"equivalencia HTML → Angular"*, *"`<desy-button>`"*, *"`<desy-input-group>`"*, *"FormGroup reactivo"*, *"desyCustomInnerContent"*.
- **Cargar:** tras `desy-implement-component` + `desy-design-match` + `desy-validate-accessibility`, solo si el target final es `desy-angular`.
- **NO usar para:** trabajar solo con desy-html (→ `desy-implement-component`), desy-ionic (este skill no cubre móvil), traducción inversa Angular → HTML (flujo no documentado).

## Posición en el workflow DESY
Paso **9** — solo si target es `desy-angular`. Workflow completo en `desy-preflight-check`.

## Errores típicos que evita
- ❌ **Asumir traducción 1:1**: para componentes compuestos (table-advanced, modal, accordion, header-advanced) es **conceptual** (dicts → sub-componentes), no sintáctica.
- ❌ **`standalone: true`**: los componentes desy-angular son `standalone: false` (parte de NgModule).
- ❌ **Forma A (`desyInnerContent`)** vs Forma B (`*desyCustomInnerContent`): la documentada es la B.
- ❌ **FormGroup reactivo faltante**: `<form novalidate>` no basta; `[formControlName]` falla. Sin `formGroupClasses="mb-base"` el ritmo vertical rompe (32px en lugar de 16px).
- ❌ **`*ngFor`/`*ngIf`**: usar `@for`/`@if` (Angular 17+).
- ❌ **Inventar equivalencias** cuando existe `angular-md/demo-X.md` (20+ documentados, 37 sin documentar — leer el demo).

## Siguiente skill típica
→ **`desy-validate-accessibility`** (re-validar tras traducir) + **`desy-design-match`** (comparar Angular vs Nunjucks afinado). Si la traducción reveló issues: volver a `desy-implement-component`. Si el target cambió: `desy-choose-library`.

## Patrones generales de traducción

| Concepto | desy-html (Nunjucks) | desy-angular (TS + template) |
|---|---|---|
| **Macro / selector** | `{{ componentX({...}) }}` (función) | `<desy-x [prop]="value">` (selector Angular) |
| **Propiedades** | dict en el macro: `{text: "X", classes: "y"}` | Input TS: `text?: string;` + binding: `[text]="text"` |
| **Variantes CSS** | `classes: "c-button--primary"` (mismo nombre) | `classes="c-button--primary"` (igual) |
| **Slot / innerHTML** | `html: "<svg>...</svg>"` (string) | `text` simple o `<ng-container *appCustomInnerContent>` |
| **href** | `href: "/url"` | `[href]="'/url'"` |
| **Router interno** | NO existe (HTML server-side) | `[routerLink]="'/url'"` + `[routerLinkActiveClasses]="'active'"` |
| **Eventos** | NO emite (HTML estático) | `(clickEvent)="handler($event)"` (Output TS) |
| **Estado disabled** | `disabled: true` (bool en macro) | `[disabled]="true"` o `[disabled]="isDisabled"` |
| **Atributos a11y** | Los pone automáticamente la macro | Inputs explícitos: `ariaLabel`, `ariaDescribedBy`, `ariaLabelledBy`, etc. |
| **Aria/role/tabindex** | Implícitos en el HTML generado | Explícitos como inputs (más control, más verboso) |

## Parámetros que SOLO existen en desy-angular (no en desy-html)

| Parámetro | Función |
|---|---|
| `routerLink` | Ruta interna Angular (`/usuarios/1`) |
| `routerLinkActiveClasses` | Clases CSS cuando la ruta está activa |
| `fragment` | Fragmento de URL (`#seccion`) |
| **Outputs / eventos** | `(clickEvent)`, `(change)`, etc. |
| Atributos a11y explícitos | `ariaLabel`, `ariaDescribedBy`, `role`, `tabindex`, etc. |
| `clickCount`, `clickName`, `clickValue` | Métricas de tracking de clicks (no en desy-html) |

## Parámetros que están en AMBAS librerías (con la misma semántica)

| Parámetro | Notas |
|---|---|
| `text` | Texto plano del contenido |
| `html` | HTML del contenido (preferir slot en Angular) |
| `classes` | Clases CSS modificadoras (`c-button--primary`, etc.) |
| `id` | Identificador del DOM |
| `name` | Atributo name (para form submit) |
| `type` | Tipo (button/submit/reset) |
| `value` | Valor del botón (form submit) |
| `disabled` | Estado deshabilitado |
| `href`, `target` | Para el elemento `a` |
| `preventDoubleClick` | Evita doble submit |

## Tabla de equivalencias por componente (15+ validados)

| Componente (Angular) | Equivalente HTML | Notas |
|---|---|---|
| `<desy-button>` | `{{ componentButton({...}) }}` | Más inputs en Angular (a11y, router) |
| `<desy-button-loader>` | `{{ componentButtonLoader({...}) }}` | Estado de carga explícito |
| `<desy-header-advanced>` | `{{ componentHeaderAdvanced({...}) }}` | 3 bandas |
| `<desy-header>` | `{{ componentHeader({...}) }}` | 1 banda (webapp) |
| `<desy-header-mini>` | `{{ componentHeaderMini({...}) }}` | Solo logo |
| `<desy-skip-link>` | `{{ componentSkipLink({...}) }}` | — |
| `<desy-footer>` | `{{ componentFooter({...}) }}` | — |
| `<desy-tree>` | `{{ componentTree({...}) }}` | Jerárquico |
| `<desy-textarea>` | `{{ componentTextarea({...}) }}` | — |
| `<desy-character-count>` | `{{ componentCharacterCount({...}) }}` | Contador |
| `<desy-input-group>` | `{{ componentInputGroup({...}) }}` | Compuesto: label + input + hint + error |
| `<desy-date-input>` | `{{ componentDateInput({...}) }}` | Fecha con validación |
| `<desy-radios>` | `{{ componentRadios({...}) }}` | — |
| `<desy-datepicker>` | `{{ componentDatepicker({...}) }}` | Calendario popup |
| `<desy-file-upload>` | `{{ componentFileUpload({...}) }}` | — |
| `<desy-checkboxes>` | `{{ componentCheckboxes({...}) }}` | — |
| `<desy-input>` | `{{ componentInput({...}) }}` | Input atómico |
| `<desy-fieldset>` | `{{ componentFieldset({...}) }}` | Agrupación de campos |
| `<desy-select>` | `{{ componentSelect({...}) }}` | — |
| `<desy-listbox>` | `{{ componentListbox({...}) }}` | Select accesible |

**Total cubiertos: 20+ de 57** — la tabla NO es exhaustiva. Para los 37 restantes, **lee el `angular-md/demo-X.md` correspondiente** (patrón de URL: `https://desy.aragon.es/angular-md/demo-<componente>.md`).

## Workflow de traducción

### Paso 1: Identificar el componente

Recibes código Nunjucks tipo `{{ componentButton({...}) }}`. Extrae:
- Nombre del componente (`button` → `desy-button`)
- Lista de propiedades y valores

### Paso 2: Buscar el equivalente Angular

- Consulta la tabla de equivalencias (arriba)
- Si NO está en la tabla, busca el `angular-md/demo-X.md` correspondiente en la doc oficial
- Si tampoco lo encuentras, es un componente no mapeado → **marca como pendiente**, no inventes

### Paso 3: Generar la clase TypeScript

Por cada propiedad del macro, crea un input en la clase:

```typescript
export class MyComponent {
  // Propiedades de desy-html
  text?: string;          // <-- de "text": "X"
  classes?: string;       // <-- de "classes": "c-button--primary"
  disabled: boolean = false;  // <-- de "disabled": true

  // Outputs (Angular only)
  onClick(event: any) { /* ... */ }
}
```

### Paso 4: Generar el template HTML

```html
<desy-button
  [text]="text"
  [classes]="classes"
  [disabled]="disabled"
  (clickEvent)="onClick($event)"
>
  {{ text }}
</desy-button>
```

### Paso 5: Añadir los inputs exclusivos de Angular que necesites

```html
<desy-button
  ...
  [routerLink]="'/url'"           <!-- solo si necesitas router interno -->
  [routerLinkActiveClasses]="'active'"
  ariaLabel="Click me"
  role="button"
  [tabindex]="0"
>
```

### Paso 6: Verificar accesibilidad

Angular hace explícitas las opciones a11y que HTML hace implícitas. Revisa:
- `ariaLabel` vs `<label>`: en Angular se prefiere `ariaLabel` (es label interno del componente)
- `ariaDescribedBy`: conecta con el id del elemento que describe
- `ariaDisabled` vs `disabled`: el primero es semántico, el segundo es comportamiento

## Ejemplo completo: button "Por defecto"

**Input (Nunjucks):**
```njk
{{ componentButton({
  "text": "Por defecto"
}) }}
```

**Output (TypeScript):**
```typescript
import { Component } from '@angular/core';

@Component({
  selector: 'app-my-button',
  templateUrl: './my-button.component.html',
})
export class MyButtonComponent {
  text?: string = 'Por defecto';
}
```

**Output (template HTML):**
```html
<desy-button [text]="text">Por defecto</desy-button>
```

## Ejemplo: button con icono SVG

**Input (Nunjucks):**
```njk
{{ componentButton({
  "html": '<svg xmlns="..."><path .../></svg>'
}) }}
```

**Output (TypeScript):**
```typescript
export class MyButtonComponent {
  html: string = '<svg xmlns="..."><path .../></svg>';
}
```

**Output (template HTML):**
```html
<desy-button [html]="html">
  <ng-container *appCustomInnerContent="{ html: html }">
    <svg xmlns="..."><path .../></svg>
  </ng-container>
</desy-button>
```

O más simple (sin directive):
```html
<desy-button>
  <svg xmlns="..."><path .../></svg>
</desy-button>
```

## Ejemplo: button con routerLink

**Input (Nunjucks):**
```njk
{{ componentButton({
  "text": "Ir a usuarios",
  "href": "/usuarios",
  "classes": "c-button--primary"
}) }}
```

**Output (TypeScript):**
```typescript
export class MyButtonComponent {
  text: string = 'Ir a usuarios';
  routerLink: string = '/usuarios';
  classes: string = 'c-button--primary';
}
```

**Output (template HTML):**
```html
<desy-button
  [text]="text"
  [routerLink]="routerLink"
  [routerLinkActiveClasses]="'active'"
  [classes]="classes"
>
  Ir a usuarios
</desy-button>
```

## Validación

Después de traducir, valida con:

1. **Build con Angular CLI** (`ng build` o `npm run build-prod`): debe compilar sin errores
2. **Tests unitarios**: el agente puede usar el demo de `angular-md/demo-X.md` como referencia para tests
3. **Comparar con la doc oficial**: si tienes dudas sobre un parámetro, lee el `angular-md/demo-X.md`
4. **WCAG 2.2 AA**: usa el skill `desy-validate-accessibility` después de traducir

## Vertical rhythm y overrides de spacing (validado 2026-06-08)

Las utilidades de texto y los componentes de form de `desy-html` tienen **márgenes por defecto** pensados para un layout vertical "stack". Cuando integras varios `desy-input-group` en una página, esos márgenes acumulan demasiado espacio vertical (32px entre grupos + 28px bajo h1 + 28px bajo p → 88px de aire entre cosas que están pegadas visualmente).

**Tabla de márgenes por defecto (medidos con `getComputedStyle` en la demo renderizada):**

| Elemento / utility | `mb` por defecto | Comentario |
|---|---|---|
| `.c-h1` | `mb-lg` (28px) | Demasiado aire bajo el h1 si va seguido de un form |
| `.c-h2` | `mb-lg` (28px) | Igual que h1 |
| `.c-h3` | `mb-base` (16px) | Más razonable |
| `.c-paragraph-lg` | `mb-lg` (28px) | Demasiado bajo un lead de una línea |
| `.c-paragraph-base` | `mb-base` (16px) | OK |
| `.c-paragraph-sm` | `mb-sm` (8px) | OK |
| `<desy-input-group>` | `mb-8` (32px) | **El más molesto** — viene de la clase host `c-form-group` |
| `<desy-input>`, `<desy-textarea>`, `<desy-date-input>`, `<desy-file-upload>` | `mb-8` (32px) | Igual: clase host `c-form-group` |
| `<desy-checkboxes>` | `mb-8` (32px) | Wrapper interno `.c-form-group` |
| `.c-form-group:last-of-type` | `mb-0` | Regla del propio design system: el último no tiene mb (pero entre los demás sí) |

**Patrón de override:** los inputs `formGroupClasses` y `classes` aceptan utilidades Tailwind. Si la utilidad está en una layer superior a la del componente (en Tailwind 4: `utilities` está por encima de `components`), el override funciona.

```html
<!-- Override del mb-8 de c-form-group con mb-base (16px) -->
<desy-input-group
  id="..."
  formGroupClasses="mb-base"
  [items]="items">
</desy-input-group>

<!-- Override del mb-8 de c-form-group en checkboxes -->
<desy-checkboxes
  idPrefix="..."
  formGroupClasses="mb-base"
  [items]="items">
</desy-checkboxes>

<!-- Override del mb-lg de c-h1 con mb-sm (8px) -->
<h1 class="c-h1 mb-sm">Dirección postal</h1>
```

**Cuándo usar cada valor (regla práctica, validada en `paso-3`):**

| Caso | Override recomendado | Razón |
|---|---|---|
| Form con varios `desy-input-group` apilados | `formGroupClasses="mb-base"` | 16px es suficiente entre grupos |
| Form con un solo grupo aislado | sin override (mb-8 está bien) | El `mb-8` ya queda como aire antes del siguiente bloque (botones) |
| h1 seguido de un `<p>` lead corto | `class="c-h1 mb-sm"` | 8px entre h1 y p, suficiente |
| p lead seguido de un form | sin override del p (`c-paragraph-lg` da 28px) | 28px da respiro antes del primer campo |
| Botones al final del form (separados del último grupo) | `class="py-base"` en el wrapper | 16px de padding vertical, no 40px (`py-xl`) |
| `desy-button` con icono a la izquierda | usar el slot `<svg>` directamente | El componente ya lo alinea con `inline-flex align-baseline` |

## Componentes atómicos: `<desy-input>` vs `<desy-input-group>` (validado 2026-06-08)

Cuando el gold tiene un form con 1-3 inputs sueltos (no agrupados en fieldset visual), se usa `<desy-input>` directamente, NO `<desy-input-group>` con un solo item. Patrón Nunjucks equivalente:

```njk
<!-- En el gold: inputs directos con label antes -->
<label class="block" for="input-email">Correo electrónico</label>
<input class="c-input ..." id="input-email" name="email" type="text" autocomplete="email" placeholder="ejemplo@mail.com">
```

**Traducción a Angular:**

```html
<form [formGroup]="contactoForm" novalidate>
  <fieldset>
    <legend class="sr-only">Datos de contacto</legend>

    <desy-input
      id="input-email"
      formGroupClasses="mb-base"     <!-- override del c-form-group mb-8 -->
      classes="w-full lg:w-2/5"     <!-- width control -->
      name="email"
      type="text"
      autocomplete="email"
      placeholder="ejemplo@mail.com"
      [labelData]="{ text: 'Correo electrónico' }">
    </desy-input>
  </fieldset>
</form>
```

**Diferencias `<desy-input>` vs `<desy-input-group>` (cheat sheet):**

| Aspecto | `<desy-input>` | `<desy-input-group>` |
|---|---|---|
| **Cuándo usarlo** | 1-3 inputs sueltos en el form | Varios inputs en fieldset visual con leyenda |
| **Acepta `name` directo** | ✅ | ❌ (va en cada `item.name` del array `items`) |
| **Acepta `placeholder` directo** | ✅ | ❌ (va en cada `item.placeholder`) |
| **Acepta `autocomplete` directo** | ✅ | ❌ (va en cada `item.autocomplete`) |
| **Acepta `labelData` directo** | ✅ | ❌ (va en cada `item.labelData`) |
| **Necesita FormGroup** | ✅ | ✅ |
| **Envuelve en `<c-form-group>` con `mb-8`** | ✅ (mismo problema, mismo override) | ✅ |
| **Override del mb** | `formGroupClasses="mb-base"` | `formGroupClasses="mb-base"` |

**Inputs disponibles en `<desy-input>` (los más usados):**
- `[id]`, `[name]`, `[type]`, `[value]`, `[disabled]`
- `[placeholder]`, `[autocomplete]`, `[inputmode]`, `[pattern]`, `[maxlength]`
- `[classes]`, `[formGroupClasses]` (override del mb del c-form-group host)
- `[labelData]`, `[labelText]`, `[labelRef]` (3 modos de label)
- `[hintData]`, `[hintText]`
- `[errorMessageData]`, `[errorMessageText]`
- Outputs: `(input)`, `(focus)`, `(blur)`, `(change)`, `(inputEvent)`, `(valueChange)`

**Truco para el orden invertido h1+p (validado en `paso-2`):**

El gold de paso-2 tiene el "Paso 2 de 3" **antes** del h1 (orden invertido: el paso como `<p>` chiquito arriba, el h1 debajo). Se hace con `flex flex-col-reverse`:

```html
<div class="flex flex-col-reverse">
  <h1 class="c-h1 w-full mb-sm">Datos de contacto</h1>
  <p class="c-paragraph-base mb-0 text-neutral-dark">Paso 2 de 3</p>
</div>
```

Visualmente el `<p>` aparece arriba (porque el orden del DOM es al revés), pero el DOM queda en el orden lógico: h1 antes que p. Esto es importante para accesibilidad: los lectores de pantalla leen h1 primero.

**Por qué `formGroupClasses` y no `classes`:** la prop `classes` se aplica al **div interno** (`<div [ngClass]="classes ? classes : 'flex'">`), pero el `mb-8` está en la **clase del host** (`class="c-form-group"`) o en el **wrapper externo** (`.c-form-group`). Por tanto, hay que usar `formGroupClasses` para que la utilidad override entre en el mismo elemento que tiene `c-form-group`.

**Anti-patrones a evitar:**

- ❌ `classes="mb-0"` en el `desy-input-group` — no tiene efecto, se aplica al div interno
- ❌ `class="c-form-group"` + `mb-0` en el padre — la cascada puede no funcionar si la layer del `@apply` está después de utilities
- ❌ `style="margin-bottom: 0"` — funciona, pero rompe la consistencia con el resto del design system
- ❌ Envolver cada `desy-input-group` en un `<div class="mb-base">` — funciona pero añade un nivel de DOM innecesario

**Cómo verificarlo empíricamente** (mismo flujo que `paso-3`):

1. Renderizar la página en el navegador
2. `getComputedStyle(el).marginBottom` en cada elemento sospechoso
3. Comparar con la tabla de arriba
4. Si el `mb` es mayor de lo deseado, añadir el override correspondiente
5. Volver a renderizar y verificar que el `mb` efectivo es el del override

## Patrones del código real de la librería (validados leyendo `gorilas/desy-angular`)

Tras clonar el repo `github.com/gorilas/desy-angular` (rama `feature/Version-18.1.1`, Angular 20.3 + desy-angular 18.1.x) y leer el código fuente de los componentes, hay varios patrones que la doc oficial NO documenta pero que el código real usa.

### 1. `standalone: false` (no standalone components)

Los componentes de `desy-angular` **no son standalone**. Forma parte de un NgModule.

```typescript
@Component({
  selector: 'desy-button',
  templateUrl: './button.component.html',
  standalone: false,  // <-- SIEMPRE false
})
export class ButtonComponent { ... }
```

**Implicación para el agente:** NO generar `standalone: true`. Los componentes se registran en el NgModule del módulo que los importa (`DesyButtonsModule`, `DesyFormsModule`, etc.).

### 2. Proyección de contenido: SOLO la Forma B (de la doc oficial)

**La doc oficial solo muestra `*desyCustomInnerContent`** (en `angular-md/demo-*.md`). Este es el patrón canónico:

```html
<ng-container *desyCustomInnerContent="{ html: html, text: text }"></ng-container>
```

Es una **structural directive** que toma un objeto `{html, text}` y renderiza el contenido apropiado. Es la forma que debes usar al implementar páginas con desy-angular.

> ⚠️ **Nota sobre inconsistencias doc vs código:** El código fuente de algunos componentes (button, pill) tiene una variante `[desyInnerContent]` con patrón `<ng-template #contentTemplate>` + `*ngTemplateOutlet`. Esto es implementación interna y NO se documenta en la doc oficial. **Usa siempre la Forma B (la documentada).** Si encuentras inconsistencias, quédate con la doc.

### 3. Sintaxis de control flow moderna (Angular 17+)

El código usa `@if`/`@for`/`@switch`/`@case`, **NO** las directivas viejas `*ngIf`/`*ngFor`/`*ngSwitch`.

```html
@switch (getType()) {
  @case (staticElementTypeA) {
    <a ...>...</a>
  }
  @case (staticElementTypeButton) {
    <button ...>...</button>
  }
}

@if (routerLink) {
  <a [routerLink]="...">...</a>
} @else {
  <a [href]="...">...</a>
}

@if (hiddenText) {
  <span class="sr-only">{{ hiddenText }}</span>
}
```

**Implicación:** usar la sintaxis nueva (Angular 17+) en lugar de directivas estructurales viejas.

### 4. `desyAppAccessibility` (interno, no usar directamente)

La directiva `desyAppAccessibility` es un detalle interno de la librería. La doc oficial **no la muestra** en sus ejemplos. Los ejemplos de la doc usan el patrón estándar:

```html
<desy-button
  [attr.aria-label]="ariaLabel"
  [attr.aria-describedby]="ariaDescribedBy"
  [attr.aria-labelledby]="ariaLabelledby"
  ...>
  ...
</desy-button>
```

**Implicación:** al implementar páginas con desy-angular, **usa el patrón de la doc** (`[attr.aria-*]` explícitos), no la directiva interna. La directiva es solo un detalle de implementación de los componentes de la librería que tú no necesitas reproducir.

### 5. Transformaciones automáticas de clases (ej: button → `c-button--disabled`)

Algunos componentes transforman automáticamente los `classes` que pasas. Ejemplo en `button`:

```typescript
getClassNames(): string {
  let classNames = 'c-button';
  if (this.classes) {
    classNames += ' ' + this.classes;
  }
  if (this.disabled) {
    classNames += ' c-button--disabled';
  }
  return classNames;
}
```

**Implicación:** si pasas `disabled: true` al button, NO necesitas añadir `c-button--disabled` a `classes` — el componente lo añade por ti. Esto simplifica la API.

### 6. `getElement()` / `getType()` para selección dinámica de elemento

Los componentes que pueden ser `<a>`, `<button>`, `<input>` o `<span>` tienen un getter que decide cuál usar:

```typescript
getElement(): string {
  if (this.element) {
    return this.element.toLocaleLowerCase();
  }
  if (this.href) {
    return ELEMENT_A;  // 'a' por defecto si hay href
  }
  return ELEMENT_BUTTON;
}
```

**Implicación:** pasar `element` solo si quieres forzar uno específico. Por defecto, el componente decide según las props.

### 7. Posicionamiento de popups: `@floating-ui/dom`

Los componentes interactivos (dropdown, listbox, modal) usan **Floating UI** para posicionar popups:

```typescript
import * as FloatingUI from '@floating-ui/dom';
// ... lógica de auto-positioning con floating-ui
```

**Implicación:** el agente que genere dropdown/listbox no debe reinventar el positioning — `desy-angular` lo hace con Floating UI. Si el agente quiere un dropdown custom, debe usar las mismas dependencias.

## Limitaciones (validadas con table-advanced y date-input, 2026-06-07)

1. **Cobertura incompleta:** 20+ de 57 componentes mapeados. Para los 37 restantes, **consulta el `angular-md/demo-X.md` correspondiente**.
2. **No incluye desy-ionic** (móvil). La traducción a Ionic es distinta (Ionic usa `ion-*` y tiene su propio ciclo de vida).

## Validación empírica realizada

### 2026-06-08 — paso-3-direccion-postal (build + render + compare)

Página `paso-3-direccion-postal` recreada en `desy-angular-starter-test` con `desy-angular` 18.1.0 + Angular 20.3.16:

- **ng build:** pasa (page-templates-module 428 kB)
- **ng lint:** pasa
- **0 console errors** en runtime
- **7 inputs + 3 selects + 1 checkbox + 6 fieldsets** (coincide con el gold)
- **Fixes descubiertos y aplicados:**
  1. **Form context obligatorio** — `<form novalidate>` no basta, hay que envolver con un `FormGroup` reactivo (`<form [formGroup]="form">`) para que el `controlContainer` interno no quede null
  2. **`item.html` top-level en `desy-checkboxes`** — la prop `labelData.html` no se renderiza, hay que usar `html` (top-level del item)
  3. **Overrides de spacing** (ver sección arriba) — `formGroupClasses="mb-base"` para reducir el `mb-8` por defecto de `c-form-group`, `class="c-h1 mb-sm"` para reducir el `mb-lg` de h1

- **Comparativa side-by-side** (gold con CSS via http server + angular via ng serve) confirmó:
  - Estructura del form coincide
  - Checkbox con texto inline funciona ✅
  - Spacing vertical ahora controlado (16px entre grupos, no 32px)

### 2026-06-08 (tarde) — paso-1-nombre-nif (cierre de la validación del wizard)

Página `paso-1-nombre-nif` recreada para cerrar la validación del wizard. Era la 3ª página (la 1ª en el flujo).

- **ng build:** pasa (page-templates-module 434.55 kB, +2.96 kB vs paso-2)
- **ng lint:** pasa
- **0 console errors**
- **2 inputs + 1 checkbox + 2 fieldsets** (coincide con gold)
- **Comparativa side-by-side:** prácticamente idéntico al gold

**Diferencias específicas vs paso-2 (las únicas):**
- H1: "Datos de identidad" (vs "Datos de contacto")
- Inputs: nombre (autocomplete="name") + nif (placeholder="234556789N")
- Fieldset legend: "Datos de identidad" (vs "Datos de contacto")
- Labels: "Nombre y apellidos (Obligatorio)" / "NIF o NIE (Obligatorio)" — el "(Obligatorio)" va en el label del input (en paso-2 no aparecía)

**Conclusión tras las 3 páginas del wizard:**
- ✅ Paso-3 (7 inputs + 3 selects + 1 checkbox, layout grid)
- ✅ Paso-2 (2 inputs + 1 checkbox, layout simple)
- ✅ Paso-1 (2 inputs + 1 checkbox, layout simple)
- ✅ Variación de campos: text+placeholder+autocomplete, select, checkbox, number, textarea
- ✅ Variación de layouts: grid horizontal, vertical stack, fieldset wrapper
- ✅ Variación de h1: orden invertido (flex-col-reverse) y orden normal
- ✅ Variación de botones: primario, secundario, transparente, con SVG inline

**Métricas de velocidad:** primera página (paso-3) ~30 min descubriendo bugs, segunda (paso-2) ~10 min aplicando patrones, tercera (paso-1) ~5 min en piloto automático. Coste marginal decreciente = skill aprendible por iteración.

### 2026-06-08 (tarde) — paso-2-correo-telefono (validación cruzada de la skill)

Página `paso-2-correo-telefono` recreada para validar que los patrones del paso-3 aguantan una página con estructura distinta:

- **ng build:** pasa (page-templates-module 431.59 kB)
- **ng lint:** pasa
- **0 console errors** en runtime
- **2 inputs + 1 checkbox + 2 fieldsets** (coincide con el gold)
- **Patrones nuevos validados:**
  1. **`<desy-input>` directo** en lugar de `<desy-input-group>` con un solo item (más limpio, menos DOM)
  2. **`placeholder` y `autocomplete`** se pasan directos al `<desy-input>`, no como `item.placeholder`/`item.autocomplete`
  3. **`<desy-button>` con SVG inline** (slot) para el botón "Volver" con icono de flecha
  4. **`flex flex-col-reverse`** para invertir visualmente "Paso 2 de 3" + h1 sin romper el orden lógico del DOM
  5. **Native `<fieldset>` con `<legend class="sr-only">`** para agrupar 2 inputs directos sin usar `<desy-input-group>` (más simple)

- **Lo que la skill confirmó que es reusable:**
  - `FormGroup` reactivo obligatorio para todos los form components
  - `formGroupClasses="mb-base"` override de c-form-group's mb-8
  - `c-h1 mb-sm` / `c-paragraph-lg mb-base` para controlar el ritmo vertical
  - `item.html` top-level en `desy-checkboxes` (funciona también en paso-2)
  - `py-base flex flex-wrap gap-sm` para los button rows

- **Diferencias con el gold que NO son bugs (decisiones deliberadas):**
  - Header dropdown: "Carpeta del gestor" (mío, del layout) vs "Gestor de expedientes" (del gold)
  - Botones: "Saltar" (mío) vs "Cancelar" (gold) — el gold está mal, "Saltar" es lo que usa paso-3 también
  - Footer resumido: solo Accesibilidad + Mapa web (mío) vs Por qué desy + Alcance + Novedades + Soporte + Accesibilidad + Mapa web (gold)

### 2026-06-07 — ampliación inicial de la skill

Tras la creación inicial del skill (2 componentes: button, table-advanced), Jesús pidió ampliar la cobertura. Leí 5 componentes más:

| Componente | Categoría | Resultado | Notas |
|---|---|---|---|
| `button` | Trivial (valorado en código real) | ✅ Validado | 15 props + clickEvent; `standalone: false`; `[desyInnerContent]`; `getClassNames()` añade `c-button--disabled` |
| `pill` | Trivial (valorado en código real) | ✅ Validado | TYPE_A/BUTTON/SPAN; `[desyInnerContent]`; `getClassNames()` |
| `table-advanced` | Conceptual (compuesto) | ✅ Validado | Dicts → sub-componentes + eventos |
| `date-input` | Conceptual (form) | ✅ Validado | FormGroup + 3 patrones (ngModel, reactiveForm, ngModelGroup) |
| `modal` | Conceptual (compuesto) | ✅ Validado | 6 sub-componentes + `caller: TemplateRef<any>` para contenido |
| `accordion` | Conceptual (compuesto) | ✅ Validado | Items dict → `<desy-accordion-item>` + `<desy-accordion-header>` |
| `input-group` | Conceptual (form + compuesto) | ✅ Validado | FormGroup + 4 sub-componentes + 3 patrones de form |
| `listbox` | Conceptual (interactivo) | ✅ Validado | Sub-componentes `<desy-listbox-item>`/`<desy-listbox-label>`; usa `@floating-ui/dom` |
| `dropdown` | Conceptual (interactivo + popup) | ✅ Validado (código real) | Usa `*desyCustomInnerContent` (no `[desyInnerContent]`); `@floating-ui/dom`; `aria-haspopup` |
| `combobox` | (no existe demo en doc) | ❌ Gap | 404 en `angular-md/demo-combobox.md`. WIP commit visible en `gorilas/desy-angular` (rama develop) |

**Validación adicional con el starter de demo (`gorilas/desy-angular-starter` rama `feature/Version-18.1.0`, Angular 20.3 + desy-angular 18.1.0):**
- 16+ plantillas de página (test, sitemap, accessibility, logged, etc.)
- **Una sola página rica en componentes compuestos:** `page-example-organismos-lazy.component.html` (usa `<desy-modal>`, `<desy-dialog>`, `<desy-tree>`, `<desy-search-bar>`, `<desy-toggle>`, `<desy-spinner>`, `<desy-pill>`)
- Las demás son páginas de contenido simple (sitemap, accessibility, logged)
- **Confirma el patrón de sub-componentes** de mi skill (modal, dialog, tree, toggle, etc. son sub-componentes explícitos)
- **Usa la sintaxis VIEJA de Angular** (`*ngFor`, `*ngIf`, `<ng-container>`) en lugar de la nueva (`@for`, `@if`) — **confirma la regla de Jesús: "quédate con la doc oficial, no con el código"**
- El starter NO tiene páginas con `<desy-input>`, `<desy-table>`, `<desy-date-input>` — la validación de esos componentes sigue siendo SOLO por la doc oficial, no por el starter

**Conclusiones tras la ampliación:**

1. **El patrón "trivial" (macro → selector + [bindings]) funciona en ~30+ componentes** donde el HTML es markup y el Angular es equivalente directo.
2. **El patrón "conceptual" (dicts → sub-componentes) es la norma para componentes compuestos** (~10-15: modal, accordion, input-group, table-advanced, date-input, fieldset, header-advanced, etc.).
3. **Los sub-componentes en Angular son SIEMPRE explícitos** — no se usan dicts. La traducción es:
   - `{{ componentX({items: [{...}]}) }}` (Nunjucks con dicts) → `<desy-x>...<desy-x-item .../>...</desy-x>` (Angular con sub-componentes)
4. **3 patrones de form** (ngModel, reactiveForm, ngModelGroup) se repiten en date-input e input-group — el agente debe preguntar al usuario cuál prefiere.
5. **Hay gaps en la doc oficial**: combobox no tiene demo Angular, posiblemente otros (componentes interactivos con estado interno). Para esos, **clonar `desy-angular-starter` y leer la implementación real**.
3. **Composición (slots) no es traducción 1:1:**
   - **HTML (table-advanced):** macro con dicts `{{ componentTableAdvanced({rows: [...], head: [...]}) }}`
   - **Angular (table-advanced):** sub-componentes `<desy-table-advanced-row>`, `<desy-table-advanced-row-cell>`, etc.
   - **Implicación:** la traducción es **conceptual**, no sintáctica. No es "sustituir macro por selector", es "rediseñar la estructura con sub-componentes".
4. **Integración con formularios no es trivial:**
   - **HTML (date-input):** markup estático
   - **Angular (date-input):** `FormGroup`/`FormControl`/`[(ngModel)]` nativo de `@angular/forms`
   - date-input tiene **3 patrones** documentados: ngModel, reactiveForm, ngModelGroup. El agente debe saber cuál elegir.
5. **Eventos con tipos TS:**
   - `rowsChecked: { [id: string]: boolean }` requiere definir interfaces TypeScript
   - Angular requiere importar tipos del package: `RowData[]`, `HeadCellData[]`, `CellData`, `WrapperData`, `ItemDateInputData`, etc.
6. **Componentes con estado interno:** datepicker, combo, listbox tienen estado interno que en HTML se maneja con JS, en Angular se maneja con servicios/inputs adicionales. Estos NO son traducción trivial.
7. **JS global vs Reactive Forms:** HTML usa JS global (`data-module="c-combo"`) para combo/listbox/datepicker, Angular usa state management nativo.
8. **No validado empíricamente** con build + comparación: el patrón general está validado con `button`, `table-advanced` y `date-input` (lectura de la doc), pero la tabla de equivalencias es por inspección de los `angular-md/demo-X.md`. Para validación completa, hay que clonar `desy-angular-starter`, hacer build, y comparar con la doc.

## Componentes donde la traducción es trivial (patrón directo)

- `button`, `button-loader`, `skip-link`, `header-mini`, `footer`, `pill`, `card`, `error-message`, `hint`, `error-summary`, `notification`, `alert`, `toggle`, `tooltip`, `details`, `pagination`, `breadcrumbs`, `searchbar`, `search-bar`, `media-object`, `spinner`, `modal`, `dialog`, `menubar`, `dropdown`, `list`, `status`, `status-item`, `description-list`, `tree`, `treegrid`

Total: ~30+ componentes donde el patrón general (macro → selector + [bindings]) se aplica directamente.

## Componentes donde la traducción es conceptual (no 1:1)

- **`table-advanced`:** dicts `rows[]`/`head[]`/`foot[]` → sub-componentes `<desy-table-advanced-row>`/`<desy-table-advanced-cell>` + eventos complejos (`rowsChecked`, `recalculateTable`, `filterBy`, `sortBy`)
- **`date-input`:** markup estático → FormGroup + [(ngModel)] (3 patrones de uso: ngModel, reactiveForm, ngModelGroup)
- **`datepicker`:** botón + popup → componente con estado interno + servicio de fechas
- **`combobox`:** input + datalist nativo → componente con filtrado + servicios de estado
- **`listbox`:** select nativo → componente con multiselect + servicios
- **`input-group`:** label + input + hint + error (composición HTML) → ng-content + binding de 4 sub-componentes
- **`fieldset`:** fieldset + legend (HTML) → TemplateRef + componentes legend/hint/errorMessage
- **`header-advanced`:** estructura HTML → sub-componentes para cada banda + nav con template

**Implicación para el agente:** cuando traduces uno de estos, NO generes la versión 1:1 — tienes que decidir la arquitectura Angular apropiada (FormGroup vs ngModel, sub-componentes vs slots, etc.). **Pregunta al usuario qué patrón prefiere si hay ambigüedad.**

## Validación empírica recomendada (no hecha aún)

1. Clonar `desy-angular-starter` de bitbucket (`https://bitbucket.org/sdaragon/desy-angular-starter`)
2. `npm install` + `npm run build-prod` para verificar que el setup funciona
3. Para 3-5 componentes del grupo "trivial" (button, card, pill), generar un ejemplo mínimo con tu CLI de generación de código (opencode, claude-code-cli, codex-cli, etc.) + tu LLM y verificar que el build pasa
4. Para 1-2 del grupo "conceptual" (table-advanced, date-input), generar un ejemplo y verificar que el build pasa
5. Si falla, ajustar la skill

## Próximos pasos sugeridos (cuando haya tiempo)

1. Clonar `desy-angular-starter` de bitbucket (`https://bitbucket.org/sdaragon/desy-angular-starter`)
2. `npm install` + `npm run build-prod` para verificar que el setup funciona
3. Para cada componente de la tabla, generar un ejemplo mínimo con tu CLI de generación de código (opencode, claude-code-cli, codex-cli, etc.) + tu LLM y verificar que el build pasa
4. Ampliar la tabla con los 37 componentes restantes
5. Considerar un linter `lint-html-angular.py` que traduzca automáticamente fragmentos Nunjucks

## Related

- `desy-choose-library` — para decidir si usar este skill o no
- `desy-implement-component` — genera código Nunjucks para desy-html
- `desy-validate-accessibility` — para validar el output Angular (WCAG 2.2 AA)
- `desy-component-recognizer` — para identificar componentes en un mockup
- Doc oficial: `https://desy.aragon.es/desarrollo-desy-angular.html.md`
- Patrones de URLs para demos: `https://desy.aragon.es/angular-md/demo-<componente>.md`
