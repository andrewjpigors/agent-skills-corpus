---
name: seo
description: Optimize for search engine visibility and ranking. Use when asked to "improve SEO", "optimize for search", "fix meta tags", "add structured data", "sitemap optimization", or "search engine optimization".
license: MIT
metadata:
  author: web-quality-skills
  version: "1.0"
---

# SEO optimization

Search engine optimization based on Lighthouse SEO audits and Google Search guidelines. Focus on technical SEO, on-page optimization, and structured data.

## SEO fundamentals

Search ranking factors (approximate influence):

| Factor | Influence | This Skill |
|--------|-----------|------------|
| Content quality & relevance | ~40% | Partial (structure) |
| Backlinks & authority | ~25% | ✗ |
| Technical SEO | ~15% | ✓ |
| Page experience (Core Web Vitals) | ~10% | See [Core Web Vitals](../core-web-vitals/SKILL.md) |
| On-page SEO | ~10% | ✓ |

---

## Technical SEO

### Crawlability

**robots.txt:**
```text
# /robots.txt
User-agent: *
Allow: /

# Block admin/private areas
Disallow: /admin/
Disallow: /api/
Disallow: /private/

# Don't block resources needed for rendering
# ❌ Disallow: /static/

Sitemap: https://example.com/sitemap.xml
```

**Meta robots:**
```html
<!-- Default: indexable, followable -->
<meta name="robots" content="index, follow">

<!-- Noindex specific pages -->
<meta name="robots" content="noindex, nofollow">

<!-- Indexable but don't follow links -->
<meta name="robots" content="index, nofollow">

<!-- Control snippets -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**Canonical URLs:**
```html
<!-- Prevent duplicate content issues -->
<link rel="canonical" href="https://example.com/page">

<!-- Self-referencing canonical (recommended) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- For paginated content -->
<link rel="canonical" href="https://example.com/products">
<!-- Or use rel="prev" / rel="next" for explicit pagination -->
```

### XML sitemap

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>daily</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/products</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>weekly</changefreq>
    <priority>0.8</priority>
  </url>
</urlset>
```

**Sitemap best practices:**
- Maximum 50,000 URLs or 50MB per sitemap
- Use sitemap index for larger sites
- Include only canonical, indexable URLs
- Update `lastmod` when content changes
- Submit to Google Search Console

### URL structure

```
✅ Good URLs:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Poor URLs:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**URL guidelines:**
- Use hyphens, not underscores
- Lowercase only
- Keep short (< 75 characters)
- Include target keywords naturally
- Avoid parameters when possible
- Use HTTPS always

### HTTPS & security

```html
<!-- Ensure all resources use HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Not: -->
<img src="http://example.com/image.jpg">
```

**Security headers for SEO trust signals:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
```

---

## On-page SEO

### Title tags

```html
<!-- ❌ Missing or generic -->
<title>Page</title>
<title>Home</title>

<!-- ✅ Descriptive with primary keyword -->
<title>Blue Widgets for Sale | Premium Quality | Example Store</title>
```

**Title tag guidelines:**
- 50-60 characters (Google truncates ~60)
- Primary keyword near the beginning
- Unique for every page
- Brand name at end (unless homepage)
- Action-oriented when appropriate

### Meta descriptions

```html
<!-- ❌ Missing or duplicate -->
<meta name="description" content="">

<!-- ✅ Compelling and unique -->
<meta name="description" content="Shop premium blue widgets with free shipping. 30-day returns. Rated 4.9/5 by 10,000+ customers. Order today and save 20%.">
```

**Meta description guidelines:**
- 150-160 characters
- Include primary keyword naturally
- Compelling call-to-action
- Unique for every page
- Matches page content

### Heading structure

```html
<!-- ❌ Poor structure -->
<h2>Welcome to Our Store</h2>
<h4>Products</h4>
<h1>Contact Us</h1>

<!-- ✅ Proper hierarchy -->
<h1>Blue Widgets - Premium Quality</h1>
  <h2>Product Features</h2>
    <h3>Durability</h3>
    <h3>Design</h3>
  <h2>Customer Reviews</h2>
  <h2>Pricing</h2>
```

**Heading guidelines:**
- Single `<h1>` per page (the main topic)
- Logical hierarchy (don't skip levels)
- Include keywords naturally
- Descriptive, not generic

### Image SEO

```html
<!-- ❌ Poor image SEO -->
<img src="IMG_12345.jpg">

<!-- ✅ Optimized image -->
<img src="blue-widget-product-photo.webp"
     alt="Blue widget with chrome finish, side view showing control panel"
     width="800"
     height="600"
     loading="lazy">
```

**Image guidelines:**
- Descriptive filenames with keywords
- Alt text describes the image content
- Compressed and properly sized
- WebP/AVIF with fallbacks
- Lazy load below-fold images

### Internal linking

```html
<!-- ❌ Non-descriptive -->
<a href="/products">Click here</a>
<a href="/widgets">Read more</a>

<!-- ✅ Descriptive anchor text -->
<a href="/products/blue-widgets">Browse our blue widget collection</a>
<a href="/guides/widget-maintenance">Learn how to maintain your widgets</a>
```

**Linking guidelines:**
- Descriptive anchor text with keywords
- Link to relevant internal pages
- Reasonable number of links per page
- Fix broken links promptly
- Use breadcrumbs for hierarchy

---

## Structured data (JSON-LD)

### Organization

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "Example Company",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telephone": "+1-555-123-4567",
    "contactType": "customer service"
  }
}
</script>
```

### Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "How to Choose the Right Widget",
  "description": "Complete guide to selecting widgets for your needs.",
  "image": "https://example.com/article-image.jpg",
  "author": {
    "@type": "Person",
    "name": "Jane Smith",
    "url": "https://example.com/authors/jane-smith"
  },
  "publisher": {
    "@type": "Organization",
    "name": "Example Blog",
    "logo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20"
}
</script>
```

### Product

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "Blue Widget Pro",
  "image": "https://example.com/blue-widget.jpg",
  "description": "Premium blue widget with advanced features.",
  "brand": {
    "@type": "Brand",
    "name": "WidgetCo"
  },
  "offers": {
    "@type": "Offer",
    "price": "49.99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1250"
  }
}
</script>
```

### FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What colors are available?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "Our widgets come in blue, red, and green."
      }
    },
    {
      "@type": "Question",
      "name": "What is the warranty?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "All widgets include a 2-year warranty."
      }
    }
  ]
}
</script>
```

### Breadcrumbs

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "position": 1,
      "name": "Home",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "position": 2,
      "name": "Products",
      "item": "https://example.com/products"
    },
    {
      "@type": "ListItem",
      "position": 3,
      "name": "Blue Widgets",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Validation

Test structured data at:
- [Google Rich Results Test](https://search.google.com/test/rich-results)
- [Schema.org Validator](https://validator.schema.org/)

---

## Mobile SEO

### Responsive design

```html
<!-- ❌ Not mobile-friendly -->
<meta name="viewport" content="width=1024">

<!-- ✅ Responsive viewport -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Tap targets

```css
/* ❌ Too small for mobile */
.small-link {
  padding: 4px;
  font-size: 12px;
}

/* ✅ Adequate tap target */
.mobile-friendly-link {
  padding: 12px;
  font-size: 16px;
  min-height: 48px;
  min-width: 48px;
}
```

### Font sizes

```css
/* ❌ Too small on mobile */
body {
  font-size: 10px;
}

/* ✅ Readable without zooming */
body {
  font-size: 16px;
  line-height: 1.5;
}
```

---

## International SEO

### Hreflang tags

```html
<!-- For multi-language sites -->
<link rel="alternate" hreflang="en" href="https://example.com/page">
<link rel="alternate" hreflang="es" href="https://example.com/es/page">
<link rel="alternate" hreflang="fr" href="https://example.com/fr/page">
<link rel="alternate" hreflang="x-default" href="https://example.com/page">
```

### Language declaration

```html
<html lang="en">
<!-- or -->
<html lang="es-MX">
```

---

## SEO audit checklist

### Critical
- [ ] HTTPS enabled
- [ ] robots.txt allows crawling
- [ ] No `noindex` on important pages
- [ ] Title tags present and unique
- [ ] Single `<h1>` per page

### High priority
- [ ] Meta descriptions present
- [ ] Sitemap submitted
- [ ] Canonical URLs set
- [ ] Mobile-responsive
- [ ] Core Web Vitals passing

### Medium priority
- [ ] Structured data implemented
- [ ] Internal linking strategy
- [ ] Image alt text
- [ ] Descriptive URLs
- [ ] Breadcrumb navigation

### Ongoing
- [ ] Fix crawl errors in Search Console
- [ ] Update sitemap when content changes
- [ ] Monitor ranking changes
- [ ] Check for broken links
- [ ] Review Search Console insights

---

## Tools

| Tool | Use |
|------|-----|
| Google Search Console | Monitor indexing, fix issues |
| Google PageSpeed Insights | Performance + Core Web Vitals |
| Rich Results Test | Validate structured data |
| Lighthouse | Full SEO audit |
| Screaming Frog | Crawl analysis |

## References

- [Google Search Central](https://developers.google.com/search)
- [Schema.org](https://schema.org/)
- [Core Web Vitals](../core-web-vitals/SKILL.md)
- [Web Quality Audit](../web-quality-audit/SKILL.md)

---
nombre: seo
Descripción: Optimizar para la visibilidad y clasificación en los motores de búsqueda. Úselo cuando se le solicite "mejorar el SEO", "optimizar para la búsqueda", "corregir metaetiquetas", "agregar datos estructurados", "optimización del mapa del sitio" u "optimización del motor de búsqueda".
licencia: MIT
metadatos:
  autor: habilidades-de-calidad-web
  versión: "1.0"
---

# Optimización SEO

Optimización de motores de búsqueda basada en auditorías Lighthouse SEO y pautas de Búsqueda de Google. Concéntrese en SEO técnico, optimización en la página y datos estructurados.

## Fundamentos de SEO

Factores de clasificación de búsqueda (influencia aproximada):

| factor | Influencia | Esta habilidad |
|--------|-----------|------------|
| Calidad y relevancia del contenido | ~40% | Parcial (estructura) |
| Vínculos de retroceso y autoridad | ~25% | ✗ |
| SEO técnico | ~15% | ✓ |
| Experiencia de página (Core Web Vitals) | ~10% | Consulte [Core Web Vitals](../core-web-vitals/SKILL.md) |
| SEO en la página | ~10% | ✓ |

---

## SEO técnico

### Rastreabilidad

**robots.txt:**
```texto
# /robots.txt
Agente de usuario: *
Permitir: /

# Bloquear administración/áreas privadas
No permitir: /admin/
No permitir: /api/
No permitir: /privado/

# No bloquear los recursos necesarios para el renderizado
# ❌ No permitir: /estático/

Mapa del sitio: https://example.com/sitemap.xml
```

**Metarobots:**
```html
<!-- Predeterminado: indexable, seguido -->
<meta nombre="robots" contenido="índice, seguir">

<!-- Páginas específicas de Noindex -->
<meta nombre="robots" contenido="noindex, nofollow">

<!-- Indexable pero no sigue enlaces -->
<meta nombre="robots" contenido="índice, nofollow">

<!-- Fragmentos de control -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**URL canónicas:**
```html
<!-- Evite problemas de contenido duplicado -->
<enlace rel="canonical" href="https://example.com/page">

<!-- Canónico autorreferencial (recomendado) -->
<enlace rel="canonical" href="https://example.com/current-page">

<!-- Para contenido paginado -->
<enlace rel="canonical" href="https://example.com/products">
<!-- O utilice rel="prev" / rel="next" para paginación explícita -->
```

### Mapa del sitio XML

```xml
<?xml versión="1.0" codificación="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://ejemplo.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>diario</changefreq>
    <prioridad>1.0</prioridad>
  </url>
  <url>
    <loc>https://ejemplo.com/productos</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>semanal</changefreq>
    <prioridad>0,8</prioridad>
  </url>
</urlset>
```

**Prácticas recomendadas para mapas del sitio:**
- Máximo 50.000 URL o 50 MB por mapa de sitio
- Utilice el índice del mapa del sitio para sitios más grandes
- Incluir sólo URL canónicas e indexables.
- Actualiza `lastmod` cuando cambia el contenido.
- Enviar a Google Search Console

### estructura de URL

```
✅ Buenas URL:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ URL deficientes:
https://ejemplo.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Directrices de URL:**
- Utilice guiones, no guiones bajos.
- Sólo minúsculas
- Sea breve (< 75 caracteres)
- Incluya palabras clave objetivo de forma natural
- Evite los parámetros cuando sea posible.
- Utilice HTTPS siempre

### HTTPS y seguridad

```html
<!-- Asegúrese de que todos los recursos utilicen HTTPS -->
<img src="https://ejemplo.com/imagen.jpg">

<!-- No: -->
<img src="http://ejemplo.com/imagen.jpg">
```

**Encabezados de seguridad para señales de confianza de SEO:**
```
Estricta seguridad en el transporte: edad máxima = 31536000; incluirSubDominios
Opciones de tipo de contenido X: nosniff
Opciones de X-Frame: DENEGAR
```

---

## SEO en la página

### Etiquetas de título

```html
<!-- ❌ Faltante o genérico -->
<título>Página</título>
<título>Inicio</título>

<!-- ✅ Descriptivo con palabra clave principal -->
<title>Blue Widgets a la venta | Calidad Premium | Tienda de ejemplo</title>
```

**Directrices para las etiquetas de título:**
- 50-60 caracteres (Google trunca ~60)
- Palabra clave principal cerca del principio
- Único para cada página
- Nombre de la marca al final (a menos que sea la página de inicio)
- Orientado a la acción cuando sea apropiado.

### Meta descripciones

```html
<!-- ❌ Falta o duplicado -->
<meta nombre="descripción" contenido="">

<!-- ✅ Convincente y único -->
<meta name="description" content="Compre widgets azules premium con envío gratis. Devoluciones en 30 días. Calificación 4.9/5 por más de 10,000 clientes. Haga su pedido hoy y ahorre un 20%.">
```

**Pautas de meta descripción:**
- 150-160 caracteres
- Incluir la palabra clave principal de forma natural
- Llamado a la acción convincente
- Único para cada página
- Coincide con el contenido de la página

### Estructura de encabezado

```html
<!-- ❌ Mala estructura -->
<h2>Bienvenido a nuestra tienda</h2>
<h4>Productos</h4>
<h1>Contáctenos</h1>

<!-- ✅ Jerarquía adecuada -->
<h1>Widgets azules: calidad premium</h1>
  <h2>Características del producto</h2>
    <h3>Durabilidad</h3>
    <h3>Diseño</h3>
  <h2>Opiniones de clientes</h2>
  <h2>Precios</h2>
```

**Directrices de encabezado:**
- Un solo `<h1>` por página (el tema principal)
- Jerarquía lógica (no te saltes niveles)
- Incluir palabras clave de forma natural
- Descriptivo, no genérico.

### SEO de imágenes

```html
<!-- ❌ Mala imagen SEO -->
<img src="IMG_12345.jpg">

<!-- ✅ Imagen optimizada -->
<img src="widget-azul-foto-producto.webp"
     alt="Widget azul con acabado cromado, vista lateral que muestra el panel de control"
     ancho="800"
     altura="600"
     cargando="perezoso">
```

**Pautas de imagen:**
- Nombres de archivos descriptivos con palabras clave.
- El texto alternativo describe el contenido de la imagen.
- Comprimido y dimensionado adecuadamente
- WebP/AVIF con respaldos
- Carga diferida de imágenes en la parte inferior

### Enlace interno

```html
<!-- ❌ No descriptivo -->
<a href="/products">Haga clic aquí</a>
<a href="/widgets">Leer más</a>

<!-- ✅ Texto de anclaje descriptivo -->
<a href="/products/blue-widgets">Explore nuestra colección de widgets azules</a>
<a href="/guides/widget-maintenance">Aprenda cómo mantener sus widgets</a>
```

**Pautas de vinculación:**
- Texto de anclaje descriptivo con palabras clave.
- Enlace a páginas internas relevantes.
- Número razonable de enlaces por página.
- Reparar enlaces rotos rápidamente
- Utilice rutas de navegación para la jerarquía

---

## Datos estructurados (JSON-LD)

### Organización

```html
<tipo de script="aplicación/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organización",
  "nombre": "Empresa de ejemplo",
  "url": "https://ejemplo.com",
  "logotipo": "https://ejemplo.com/logo.png",
  "igual que": [
    "https://twitter.com/ejemplo",
    "https://linkedin.com/empresa/ejemplo"
  ],
  "punto de contacto": {
    "@type": "Punto de contacto",
    "teléfono": "+1-555-123-4567",
    "contactType": "servicio al cliente"
  }
}
</script>
```

### Artículo

```html
<tipo de script="aplicación/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Artículo",
  "headline": "Cómo elegir el widget adecuado",
  "description": "Guía completa para seleccionar widgets según tus necesidades.",
  "imagen": "https://example.com/article-image.jpg",
  "autor": {
    "@tipo": "Persona",
    "nombre": "Jane Smith",
    "url": "https://ejemplo.com/autores/jane-smith"
  },
  "editor": {
    "@type": "Organización",
    "nombre": "Blog de ejemplo",
    "logotipo": {
      "@type": "ObjetoImagen",
      "url": "https://ejemplo.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "2024-01-20"
}
</script>
```

### Producto

```html
<tipo de script="aplicación/ld+json">
{
  "@context": "https://schema.org",
  "@tipo": "Producto",
  "nombre": "Blue Widget Pro",
  "imagen": "https://example.com/blue-widget.jpg",
  "description": "Widget azul premium con funciones avanzadas.",
  "marca": {
    "@tipo": "Marca",
    "nombre": "WidgetCo"
  },
  "ofertas": {
    "@type": "Oferta",
    "precio": "49,99",
    "precioCurrency": "USD",
    "disponibilidad": "https://schema.org/InStock",
    "url": "https://ejemplo.com/products/blue-widget"
  },
  "calificación agregada": {
    "@type": "Calificación Agregada",
    "ratingValue": "4.8",
    "reviewCount": "1250"
  }
}
</script>
```

### Preguntas frecuentes

```html
<tipo de script="aplicación/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Página de preguntas frecuentes",
  "entidad principal": [
    {
      "@type": "Pregunta",
      "name": "¿Qué colores están disponibles?",
      "Respuestaaceptada": {
        "@type": "Respuesta",
        "text": "Nuestros widgets vienen en azul, rojo y verde."
      }
    },
    {
      "@type": "Pregunta",
      "name": "¿Cuál es la garantía?",
      "Respuestaaceptada": {
        "@type": "Respuesta",
        "text": "Todos los widgets incluyen una garantía de 2 años."
      }
    }
  ]
}
</script>
```

### Pan rallado

```html
<tipo de script="aplicación/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Lista de rutas de navegación",
  "itemListElement": [
    {
      "@type": "ListItem",
      "posición": 1,
      "nombre": "Inicio",
      "elemento": "https://ejemplo.com"
    },
    {
      "@type": "ListItem",
      "posición": 2,
      "nombre": "Productos",
      "artículo": "https://example.com/products"
    },
    {
      "@type": "ListItem",
      "posición": 3,
      "nombre": "Widgets azules",
      "elemento": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Validación

Pruebe los datos estructurados en:
- [Prueba de resultados enriquecidos de Google](https://search.google.com/test/rich-results)
- [Validador de Schema.org](https://validator.schema.org/)

---

## SEO móvil

### Diseño responsivo

```html
<!-- ❌ No compatible con dispositivos móviles -->
<meta nombre="viewport" content="ancho=1024">

<!-- ✅ Ventana gráfica responsiva -->
<meta nombre="viewport" content="ancho=ancho-dispositivo, escala-inicial=1">
```

### Toca objetivos

```css
/* ❌ Demasiado pequeño para dispositivos móviles */
.enlace pequeño {
  relleno: 4px;
  tamaño de fuente: 12px;
}

/* ✅ Objetivo de toque adecuado */
.enlace compatible con dispositivos móviles {
  relleno: 12px;
  tamaño de fuente: 16px;
  altura mínima: 48px;
  ancho mínimo: 48px;
}
```

### Tamaños de fuente

```css
/* ❌ Demasiado pequeño en dispositivos móviles */
cuerpo {
  tamaño de fuente: 10px;
}

/* ✅ Legible sin hacer zoom */
cuerpo {
  tamaño de fuente: 16px;
  altura de línea: 1,5;
}
```
---
nom : référencement
description : Optimiser pour la visibilité et le classement des moteurs de recherche. À utiliser lorsqu'on vous demande « améliorer le référencement », « optimiser pour la recherche », « corriger les balises méta », « ajouter des données structurées », « optimiser le plan du site » ou « optimiser les moteurs de recherche ».
licence : MIT
métadonnées :
  auteur : web-quality-compétences
  version : "1.0"
---

# Optimisation SEO

Optimisation des moteurs de recherche basée sur les audits Lighthouse SEO et les directives de recherche Google. Concentrez-vous sur le référencement technique, l'optimisation sur la page et les données structurées.

## Fondamentaux du référencement

Facteurs de classement de recherche (influence approximative) :

| Facteur | Influence | Cette compétence |
|--------|-----------|------------|
| Qualité et pertinence du contenu | ~40% | Partielle (structure) |
| Backlinks et autorité | ~25% | ✗ |
| Référencement technique | ~15% | ✓ |
| Expérience de page (Core Web Vitals) | ~10% | Voir [Core Web Vitals](../core-web-vitals/SKILL.md) |
| Référencement sur la page | ~10% | ✓ |

---

## Référencement technique

### Crawlabilité

**robots.txt :**
```texte
# /robots.txt
Agent utilisateur : *
Autoriser : /

# Bloquer les zones administratives/privées
Interdire : /admin/
Interdire : /api/
Interdire : /privé/

# Ne bloquez pas les ressources nécessaires au rendu
# ❌ Interdire : /static/

Plan du site : https://example.com/sitemap.xml
```

**Métarobots :**
```html
<!-- Par défaut : indexable, suivi -->
<meta name="robots" content="index, follow">

<!-- Pages spécifiques sans index -->
<meta name="robots" content="noindex, nofollow">

<!-- Indexable mais ne suivez pas les liens -->
<meta name="robots" content="index, nofollow">

<!-- Extraits de contrôle -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**URL canoniques :**
```html
<!-- Prévenir les problèmes de contenu en double -->
<link rel="canonical" href="https://example.com/page">

<!-- Canonique auto-référencé (recommandé) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Pour le contenu paginé -->
<link rel="canonical" href="https://example.com/products">
<!-- Ou utilisez rel="prev" / rel="next" pour une pagination explicite -->
```

### Plan du site XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <URL>
    <loc>https://exemple.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>quotidiennement</changefreq>
    <priorité>1.0</priorité>
  </url>
  <URL>
    <loc>https://example.com/products</loc>
    <derniermod>2024-01-14</derniermod>
    <changefreq>hebdomadaire</changefreq>
    <priorité>0,8</priorité>
  </url>
</urlset>
```

**Bonnes pratiques en matière de plan du site :**
- Maximum 50 000 URL ou 50 Mo par plan de site
- Utiliser l'index du plan du site pour les sites plus grands
- Inclure uniquement les URL canoniques et indexables
- Mettre à jour `lastmod` lorsque le contenu change
- Soumettre à Google Search Console

### Structure des URL

```
✅ Bonnes URL :
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Mauvaises URL :
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Consignes relatives aux URL :**
- Utilisez des traits d'union, pas des traits de soulignement
- Minuscules uniquement
- Soyez bref (< 75 caractères)
- Inclure naturellement des mots-clés cibles
- Évitez les paramètres lorsque cela est possible
- Utilisez toujours HTTPS

### HTTPS et sécurité

```html
<!-- Assurez-vous que toutes les ressources utilisent HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Non : -->
<img src="http://example.com/image.jpg">
```

**En-têtes de sécurité pour les signaux de confiance SEO :**
```
Sécurité stricte des transports : âge maximum = 3 153 6000 ; inclure des sous-domaines
Options de type de contenu X : nosniff
Options X-Frame : REFUSER
```

---

## SEO sur la page

### Balises de titre

```html
<!-- ❌ Manquant ou générique -->
<titre>Page</titre>
<title>Accueil</title>

<!-- ✅ Descriptif avec mot-clé principal -->
<title>Widgets bleus à vendre | Qualité supérieure | Exemple de magasin</title>
```

**Consignes relatives aux balises de titre :**
- 50 à 60 caractères (Google tronque ~ 60)
- Mot-clé principal vers le début
- Unique pour chaque page
- Nom de la marque à la fin (sauf page d'accueil)
- Orienté vers l'action le cas échéant

### Méta descriptions

```html
<!-- ❌ Manquant ou en double -->
<meta name="description" content="">

<!-- ✅ Convaincant et unique -->
<meta name="description" content="Achetez des widgets bleus premium avec livraison gratuite. Retours sous 30 jours. Noté 4,9/5 par plus de 10 000 clients. Commandez aujourd'hui et économisez 20 %.">
```

**Consignes relatives aux méta-descriptions :**
- 150-160 caractères
- Inclure naturellement le mot-clé principal
- Appel à l'action convaincant
- Unique pour chaque page
- Correspond au contenu de la page

### Structure des titres

```html
<!-- ❌ Mauvaise structure -->
<h2>Bienvenue dans notre magasin</h2>
<h4>Produits</h4>
<h1>Contactez-nous</h1>

<!-- ✅ Hiérarchie appropriée -->
<h1>Widgets bleus - Qualité Premium</h1>
  <h2>Caractéristiques du produit</h2>
    <h3>Durabilité</h3>
    <h3>Conception</h3>
  <h2>Avis clients</h2>
  <h2>Tarifs</h2>
```

**Consignes de titre :**
- Un seul `<h1>` par page (le sujet principal)
- Hiérarchie logique (ne sautez pas de niveaux)
- Incluez naturellement des mots-clés
- Descriptif, pas générique

### Référencement des images

```html
<!-- ❌ Mauvais référencement des images -->
<img src="IMG_12345.jpg">

<!-- ✅Image optimisée -->
<img src="bleu-widget-product-photo.webp"
     alt="Widget bleu avec finition chromée, vue latérale montrant le panneau de commande"
     largeur="800"
     hauteur="600"
     chargement="paresseux">
```

**Consignes relatives aux images :**
- Noms de fichiers descriptifs avec mots-clés
- Le texte alternatif décrit le contenu de l'image
- Comprimé et correctement dimensionné
- WebP/AVIF avec solutions de repli
- Chargement paresseux des images sous le pli

### Liens internes

```html
<!-- ❌ Non descriptif -->
<a href="/products">Cliquez ici</a>
<a href="/widgets">En savoir plus</a>

<!-- ✅ Texte d'ancrage descriptif -->
<a href="/products/blue-widgets">Parcourez notre collection de widgets bleus</a>
<a href="/guides/widget-maintenance">Découvrez comment gérer vos widgets</a>
```

**Consignes relatives aux liens :**
- Texte d'ancrage descriptif avec mots-clés
- Lien vers les pages internes pertinentes
- Nombre raisonnable de liens par page
- Réparez rapidement les liens brisés
- Utiliser le fil d'Ariane pour la hiérarchie

---

## Données structurées (JSON-LD)

### Organisation

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organisation",
  "name": "Exemple de société",
  "url": "https://exemple.com",
  "logo": "https://example.com/logo.png",
  "identique": [
    "https://twitter.com/exemple",
    "https://linkedin.com/company/example"
  ],
  "point de contact": {
    "@type": "Point de contact",
    "téléphone": "+1-555-123-4567",
    "contactType": "service client"
  }
}
</script>
```

### Article

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "Comment choisir le bon widget",
  "description": "Guide complet pour sélectionner les widgets adaptés à vos besoins.",
  "image": "https://exemple.com/article-image.jpg",
  "auteur": {
    "@type": "Personne",
    "nom": "Jane Smith",
    "url": "https://exemple.com/authors/jane-smith"
  },
  "éditeur": {
    "@type": "Organisation",
    "name": "Exemple de blog",
    "logo": {
      "@type": "ObjetImage",
      "url": "https://exemple.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "20/01/2024"
}
</script>
```

### Produit

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Produit",
  "name": "Blue Widget Pro",
  "image": "https://example.com/blue-widget.jpg",
  "description": "Widget bleu premium avec fonctionnalités avancées.",
  "marque": {
    "@type": "Marque",
    "nom": "WidgetCo"
  },
  "offres": {
    "@type": "Offre",
    "prix": "49,99",
    "prixCurrency": "USD",
    "disponibilité": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4,8",
    "reviewCount": "1250"
  }
}
</script>
```

###FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Page FAQ",
  "Entité principale": [
    {
      "@type": "Question",
      "name": "Quelles couleurs sont disponibles ?",
      "réponseacceptée": {
        "@type": "Réponse",
        "text": "Nos widgets sont disponibles en bleu, rouge et vert."
      }
    },
    {
      "@type": "Question",
      "name": "Quelle est la garantie ?",
      "réponseacceptée": {
        "@type": "Réponse",
        "text": "Tous les widgets incluent une garantie de 2 ans."
      }
    }
  ]
}
</script>
```

### Fil d'Ariane

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Liste de fil d'Ariane",
  "itemListElement": [
    {
      "@type": "ListeItem",
      "position": 1,
      "name": "Accueil",
      "élément": "https://exemple.com"
    },
    {
      "@type": "ListeItem",
      "position": 2,
      "name": "Produits",
      "élément": "https://example.com/products"
    },
    {
      "@type": "ListeItem",
      "position": 3,
      "name": "Widgets bleus",
      "élément": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Validation

Testez les données structurées sur :
- [Test des résultats enrichis Google](https://search.google.com/test/rich-results)
- [Validateur Schema.org](https://validator.schema.org/)

---

## Référencement mobile

### Conception réactive

```html
<!-- ❌ Pas adapté aux mobiles -->
<meta name="viewport" content="width=1024">

<!-- ✅ Fenêtre d'affichage réactive -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Appuyez sur les cibles

```css
/* ❌ Trop petit pour mobile */
.petit-lien {
  remplissage : 4 px ;
  taille de police : 12 px ;
}

/* ✅ Cible de tapotement adéquate */
.lien adapté aux mobiles {
  remplissage : 12 px ;
  taille de police : 16 px ;
  hauteur minimale : 48 px ;
  largeur minimale : 48 px ;
}
```

### Tailles de police

```css
/* ❌ Trop petit sur mobile */
corps {
  taille de police : 10 px ;
}

/* ✅ Lisible sans zoomer */
corps {
  taille de police : 16 px ;
  hauteur de ligne : 1,5 ;
}
```
---
Name: SEO
Beschreibung: Für Sichtbarkeit und Ranking in Suchmaschinen optimieren. Verwenden Sie diese Option, wenn Sie nach „SEO verbessern“, „Suchoptimierung“, „Meta-Tags korrigieren“, „strukturierte Daten hinzufügen“, „Sitemap-Optimierung“ oder „Suchmaschinenoptimierung“ gefragt werden.
Lizenz: MIT
Metadaten:
  Autor: Web-Quality-Skills
  Version: „1.0“
---

# SEO-Optimierung

Suchmaschinenoptimierung basierend auf Lighthouse-SEO-Audits und Google-Suchrichtlinien. Konzentrieren Sie sich auf technisches SEO, On-Page-Optimierung und strukturierte Daten.

## SEO-Grundlagen

Faktoren für das Suchranking (ungefährer Einfluss):

| Faktor | Einfluss | Diese Fähigkeit |
|--------|-----------|------------|
| Inhaltsqualität und Relevanz | ~40% | Teilweise (Struktur) |
| Backlinks & Autorität | ~25 % | ✗ |
| Technisches SEO | ~15% | ✓ |
| Seitenerlebnis (Core Web Vitals) | ~10 % | Siehe [Core Web Vitals](../core-web-vitals/SKILL.md) |
| On-Page-SEO | ~10 % | ✓ |

---

## Technisches SEO

### Crawlbarkeit

**robots.txt:**
„Text
# /robots.txt
Benutzeragent: *
Erlauben: /

# Admin-/private Bereiche blockieren
Nicht zulassen: /admin/
Nicht zulassen: /api/
Nicht zulassen: /privat/

# Blockieren Sie nicht die für das Rendern benötigten Ressourcen
# ❌ Nicht zulassen: /static/

Sitemap: https://example.com/sitemap.xml
„

**Meta-Roboter:**
```html
<!-- Standard: indexierbar, folgebar -->
<meta name="robots" content="index, follow">

<!-- Noindex-spezifische Seiten -->
<meta name="robots" content="noindex, nofollow">

<!-- Indexierbar, aber Links nicht folgen -->
<meta name="robots" content="index, nofollow">

<!-- Kontrollschnipsel -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
„

**Kanonische URLs:**
```html
<!-- Probleme mit doppeltem Inhalt verhindern -->
<link rel="canonical" href="https://example.com/page">

<!-- Selbstreferenzierend kanonisch (empfohlen) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Für paginierten Inhalt -->
<link rel="canonical" href="https://example.com/products">
<!-- Oder verwenden Sie rel="prev" / rel="next" für explizite Paginierung -->
„

### XML-Sitemap

„xml
<?xml version="1.0"kodierung="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <URL>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>täglich</changefreq>
    <priority>1.0</priority>
  </url>
  <URL>
    <loc>https://example.com/products</loc>
    <lastmod>14.01.2024</lastmod>
    <changefreq>wöchentlich</changefreq>
    <priority>0,8</priority>
  </url>
</urlset>
„

**Best Practices für Sitemaps:**
- Maximal 50.000 URLs oder 50 MB pro Sitemap
- Verwenden Sie den Sitemap-Index für größere Websites
- Schließen Sie nur kanonische, indizierbare URLs ein
- Aktualisieren Sie „lastmod“, wenn sich der Inhalt ändert
- An die Google Search Console senden

### URL-Struktur

„
✅ Gute URLs:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Schlechte URLs:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
„

**URL-Richtlinien:**
- Verwenden Sie Bindestriche, keine Unterstriche
- Nur Kleinbuchstaben
- Halten Sie sich kurz (< 75 Zeichen)
- Fügen Sie auf natürliche Weise Zielschlüsselwörter hinzu
- Vermeiden Sie nach Möglichkeit Parameter
- Verwenden Sie immer HTTPS

### HTTPS und Sicherheit

```html
<!-- Stellen Sie sicher, dass alle Ressourcen HTTPS verwenden -->
<img src="https://example.com/image.jpg">

<!-- Nicht: -->
<img src="http://example.com/image.jpg">
„

**Sicherheitsheader für SEO-Vertrauenssignale:**
„
Strenge Transportsicherheit: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
X-Frame-Optionen: DENY
„

---

## On-Page-SEO

### Titel-Tags

```html
<!-- ❌ Fehlt oder generisch -->
<title>Seite</title>
<title>Zuhause</title>

<!-- ✅ Beschreibend mit primärem Schlüsselwort -->
<title>Blaue Widgets zum Verkauf | Premium-Qualität | Beispielshop</title>
„

**Richtlinien für Titel-Tags:**
- 50–60 Zeichen (Google kürzt ~60)
- Primäres Schlüsselwort am Anfang
- Einzigartig für jede Seite
- Markenname am Ende (außer Homepage)
- Gegebenenfalls handlungsorientiert

### Meta-Beschreibungen

```html
<!-- ❌ Fehlt oder ist doppelt vorhanden -->
<meta name="description" content="">

<!-- ✅ Überzeugend und einzigartig -->
<meta name="description" content="Kaufen Sie blaue Premium-Widgets mit kostenlosem Versand. 30-tägige Rückgabe. Von über 10.000 Kunden mit 4,9/5 bewertet. Bestellen Sie noch heute und sparen Sie 20 %.">
„

**Meta-Beschreibungsrichtlinien:**
- 150-160 Zeichen
- Fügen Sie das primäre Schlüsselwort auf natürliche Weise hinzu
- Überzeugender Call-to-Action
- Einzigartig für jede Seite
- Entspricht dem Seiteninhalt

### Überschriftenstruktur

```html
<!-- ❌ Schlechte Struktur -->
<h2>Willkommen in unserem Shop</h2>
<h4>Produkte</h4>
<h1>Kontaktieren Sie uns</h1>

<!-- ✅ Richtige Hierarchie -->
<h1>Blaue Widgets – Premium-Qualität</h1>
  <h2>Produktmerkmale</h2>
    <h3>Haltbarkeit</h3>
    <h3>Design</h3>
  <h2>Kundenrezensionen</h2>
  <h2>Preise</h2>
„

**Richtlinien für Überschriften:**
- Einzelnes „<h1>“ pro Seite (das Hauptthema)
- Logische Hierarchie (Ebenen nicht überspringen)
- Fügen Sie Schlüsselwörter auf natürliche Weise ein
- Beschreibend, nicht allgemein

### Bild-SEO

```html
<!-- ❌ Schlechte Bild-SEO -->
<img src="IMG_12345.jpg">

<!-- ✅ Optimiertes Bild -->
<img src="blue-widget-product-photo.webp"
     alt="Blaues Widget mit Chromoberfläche, Seitenansicht mit Bedienfeld"
     Breite="800"
     Höhe="600"
     wird geladen="faul">
„

**Bildrichtlinien:**
- Beschreibende Dateinamen mit Schlüsselwörtern
- Alt-Text beschreibt den Bildinhalt
- Komprimiert und richtig dimensioniert
- WebP/AVIF mit Fallbacks
- Lazy Load von Below-Fold-Bildern

### Interne Verlinkung

```html
<!-- ❌ Nicht beschreibend -->
<a href="/products">Klicken Sie hier</a>
<a href="/widgets">Weitere Informationen</a>

<!-- ✅ Beschreibender Ankertext -->
<a href="/products/blue-widgets">Durchsuchen Sie unsere blaue Widget-Sammlung</a>
<a href="/guides/widget-maintenance">Erfahren Sie, wie Sie Ihre Widgets warten</a>
„

**Verlinkungsrichtlinien:**
- Beschreibender Ankertext mit Schlüsselwörtern
- Link zu relevanten internen Seiten
- Angemessene Anzahl von Links pro Seite
- Beheben Sie defekte Links umgehend
- Verwenden Sie Breadcrumbs für die Hierarchie

---

## Strukturierte Daten (JSON-LD)

### Organisation

```html
<script type="application/ld+json">
{
  „@context“: „https://schema.org“,
  „@type“: „Organisation“,
  „name“: „Beispielunternehmen“,
  „url“: „https://example.com“,
  „logo“: „https://example.com/logo.png“,
  „sameAs“: [
    „https://twitter.com/example“,
    „https://linkedin.com/company/example“
  ],
  „contactPoint“: {
    „@type“: „ContactPoint“,
    „telephone“: „+1-555-123-4567“,
    „contactType“: „Kundendienst“
  }
}
</script>
„

### Artikel

```html
<script type="application/ld+json">
{
  „@context“: „https://schema.org“,
  „@type“: „Artikel“,
  „headline“: „So wählen Sie das richtige Widget aus“,
  „description“: „Vollständige Anleitung zur Auswahl von Widgets für Ihre Bedürfnisse.“,
  „image“: „https://example.com/article-image.jpg“,
  „Autor“: {
    „@type“: „Person“,
    „Name“: „Jane Smith“,
    „url“: „https://example.com/authors/jane-smith“
  },
  „Herausgeber“: {
    „@type“: „Organisation“,
    „name“: „Beispielblog“,
    "Logo": {
      „@type“: „ImageObject“,
      „url“: „https://example.com/logo.png“
    }
  },
  „datePublished“: „2024-01-15“,
  „dateModified“: „20.01.2024“
}
</script>
„

### Produkt

```html
<script type="application/ld+json">
{
  „@context“: „https://schema.org“,
  „@type“: „Produkt“,
  „name“: „Blue Widget Pro“,
  „image“: „https://example.com/blue-widget.jpg“,
  „description“: „Premium blaues Widget mit erweiterten Funktionen.“,
  „Marke“: {
    „@type“: „Marke“,
    „name“: „WidgetCo“
  },
  „Angebote“: {
    „@type“: „Angebot“,
    „Preis“: „49,99“,
    „priceCurrency“: „USD“,
    „Verfügbarkeit“: „https://schema.org/InStock“,
    „url“: „https://example.com/products/blue-widget“
  },
  „aggregateRating“: {
    „@type“: „AggregateRating“,
    „ratingValue“: „4,8“,
    „reviewCount“: „1250“
  }
}
</script>
„

### FAQ

```html
<script type="application/ld+json">
{
  „@context“: „https://schema.org“,
  "@type": "FAQPage",
  „mainEntity“: [
    {
      „@type“: „Frage“,
      "name": "Welche Farben sind verfügbar?",
      „acceptedAnswer“: {
        „@type“: „Antwort“,
        „text“: „Unsere Widgets gibt es in Blau, Rot und Grün.“
      }
    },
    {
      „@type“: „Frage“,
      „name“: „Was ist die Garantie?“,
      „acceptedAnswer“: {
        „@type“: „Antwort“,
        „text“: „Alle Widgets beinhalten eine 2-Jahres-Garantie.“
      }
    }
  ]
}
</script>
„

### Semmelbrösel

```html
<script type="application/ld+json">
{
  „@context“: „https://schema.org“,
  „@type“: „BreadcrumbList“,
  „itemListElement“: [
    {
      „@type“: „ListItem“,
      "Position": 1,
      „name“: „Zuhause“,
      „item“: „https://example.com“
    },
    {
      „@type“: „ListItem“,
      "Position": 2,
      „name“: „Produkte“,
      „item“: „https://example.com/products“
    },
    {
      „@type“: „ListItem“,
      "Position": 3,
      „name“: „Blaue Widgets“,
      „item“: „https://example.com/products/blue-widgets“
    }
  ]
}
</script>
„

### Validierung

Testen Sie strukturierte Daten unter:
- [Google Rich-Suchergebnisse-Test](https://search.google.com/test/rich-results)
- [Schema.org-Validator](https://validator.schema.org/)

---

## Mobile SEO

### Responsives Design

```html
<!-- ❌ Nicht mobilfreundlich -->
<meta name="viewport" content="width=1024">

<!-- ✅ Responsives Ansichtsfenster -->
<meta name="viewport" content="width=device-width, initial-scale=1">
„

### Tippen Sie auf Ziele

„css
/* ❌ Zu klein für Mobilgeräte */
.small-link {
  Polsterung: 4px;
  Schriftgröße: 12px;
}

/* ✅ Angemessenes Tippziel */
.mobile-freundlicher-link {
  Polsterung: 12px;
  Schriftgröße: 16px;
  Mindesthöhe: 48 Pixel;
  Mindestbreite: 48 Pixel;
}
„

### Schriftgrößen

„css
/* ❌ Auf Mobilgeräten zu klein */
Körper {
  Schriftgröße: 10px;
}

/* ✅ Ohne Zoom lesbar */
Körper {
  Schriftgröße: 16px;
  Zeilenhöhe: 1,5;
}
„
---
名前：ソ
説明: 検索エンジンの可視性とランキングを最適化します。 「SEOの改善」、「検索の最適化」、「メタタグの修正」、「構造化データの追加」、「サイトマップの最適化」、または「検索エンジンの最適化」を求められた場合に使用します。
ライセンス: MIT
メタデータ:
  著者: ウェブ品質スキル
  バージョン：「1.0」
---

# SEOの最適化

Lighthouse SEO 監査と Google 検索ガイドラインに基づいた検索エンジンの最適化。技術的な SEO、ページ上の最適化、構造化データに重点​​を置きます。

## SEO の基礎

検索ランキング要因 (おおよその影響):

|係数 |影響 |このスキル |
|----------|-----------|---------------|
|コンテンツの品質と関連性 | ~40% |部分（構造） |
|バックリンクとオーソリティ | ~25% | ✗ |
|テクニカルSEO | ~15% | ✓ |
|ページ エクスペリエンス (コア Web バイタル) | ~10% | [Core Web Vitals](../core-web-vitals/SKILL.md) を参照してください。
|オンページSEO | ~10% | ✓ |

---

## テクニカル SEO

### クロール可能性

**robots.txt:**
```テキスト
# /robots.txt
ユーザーエージェント: *
許可: /

# 管理エリア/プライベートエリアをブロックする
許可しない: /admin/
禁止: /api/
禁止: /private/

# レンダリングに必要なリソースをブロックしないでください
# ❌ 許可しない: /static/

サイトマップ: https://example.com/sitemap.xml
「」

**メタロボット:**
```html
<!-- デフォルト: インデックス可能、フォロー可能 -->
<meta name="ロボット" content="インデックス、フォロー">

<!-- Noindex 固有のページ -->
<meta name="ロボット" content="noindex, nofollow">

<!-- インデックス可能ですがリンクをたどらない -->
<meta name="ロボット" content="index, nofollow">

<!-- コントロール スニペット -->
<meta name="ロボット" content="max-snippet:150, max-image-preview:large">
「」

**正規 URL:**
```html
<!-- 重複コンテンツの問題を防ぐ -->
<link rel="canonical" href="https://example.com/page">

<!-- 自己参照の正規 (推奨) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- ページ分割されたコンテンツの場合 -->
<link rel="canonical" href="https://example.com/products">
<!-- または、明示的なページネーションには rel="prev" / rel="next" を使用します -->
「」

### XML サイトマップ

```xml
<?xml バージョン="1.0" エンコーディング="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <URL>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>毎日</changefreq>
    <優先順位>1.0</優先>
  </url>
  <URL>
    <loc>https://example.com/products</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>毎週</changefreq>
    <優先度>0.8</優先度>
  </url>
</urlset>
「」

**サイトマップのベスト プラクティス:**
- 最大 50,000 個の URL、またはサイトマップごとに 50MB
- 大規模なサイトにはサイトマップ インデックスを使用します
- 正規のインデックス可能な URL のみを含めます
- コンテンツが変更された場合は「lastmod」を更新します
- Google Search Consoleに送信する

### URL 構造

「」
✅ 良い URL:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ 不適切な URL:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
「」

**URL ガイドライン:**
- アンダースコアではなくハイフンを使用してください
- 小文字のみ
- 短くしてください (75 文字未満)
- ターゲットキーワードを自然に含める
- 可能な限りパラメータを避けてください
- 常に HTTPS を使用する

### HTTPS とセキュリティ

```html
<!-- すべてのリソースが HTTPS を使用していることを確認します -->
<img src="https://example.com/image.jpg">

<!-- 違います: -->
<img src="http://example.com/image.jpg">
「」

**SEO 信頼シグナルのセキュリティ ヘッダー:**
「」
厳格なトランスポート セキュリティ: max-age=31536000;サブドメインを含む
X-Content-Type-Options: nosniff
X フレーム オプション: 拒否
「」

---

## オンページ SEO

### タイトルタグ

```html
<!-- ❌ 欠落または汎用 -->
<title>ページ</title>
<title>ホーム</title>

<!-- ✅ 主なキーワードで説明的 -->
<title>青いウィジェットが販売中 |プレミアム品質 |ストアの例</title>
「」

**タイトルタグのガイドライン:**
- 50～60 文字 (Google は最大 60 文字を切り捨てます)
- 先頭付近の主なキーワード
- ページごとに一意です
- 末尾にブランド名 (ホームページを除く)
- 適切な場合は行動指向

### メタディスクリプション

```html
<!-- ❌ 欠落または重複 -->
<meta name="説明" content="">

<!-- ✅ 魅力的でユニーク -->
<meta name="description" content="プレミアム ブルー ウィジェットを送料無料で購入できます。30 日間返品可能。10,000 人以上の顧客から 4.9/5 の評価を受けています。今すぐ注文すると 20% 割引になります。">
「」

**メタディスクリプションのガイドライン:**
- 150～160文字
- 主なキーワードを自然に含める
- 説得力のある行動喚起
- ページごとに一意です
- ページのコンテンツと一致する

### 見出し構造

```html
<!-- ❌ 構造が貧弱 -->
<h2>当店へようこそ</h2>
<h4>製品</h4>
<h1>お問い合わせ</h1>

<!-- ✅ 適切な階層 -->
<h1>青いウィジェット - プレミアム品質</h1>
  <h2>製品の特徴</h2>
    <h3>耐久性</h3>
    <h3>デザイン</h3>
  <h2>お客様のレビュー</h2>
  <h2>価格</h2>
「」

**見出しのガイドライン:**
- ページごとに 1 つの `<h1>` (メイントピック)
- 論理階層 (レベルをスキップしないでください)
- キーワードを自然に含める
- 一般的ではなく説明的なもの

### 画像SEO

```html
<!-- ❌ 画像の SEO が不十分 -->
<img src="IMG_12345.jpg">

<!-- ✅ 最適化された画像 -->
<img src="blue-widget-product-photo.webp"
     alt="クロム仕上げの青いウィジェット、コントロール パネルを示す側面図"
     幅="800"
     高さ="600"
     読み込み中 = "怠惰">
「」

**画像のガイドライン:**
- キーワードを含むわかりやすいファイル名
- 代替テキストは画像の内容を説明します
- 圧縮され、適切なサイズに設定されています
- フォールバックを備えた WebP/AVIF
- スクロールせずに見える画像を遅延読み込みする

### 内部リンク

```html
<!-- ❌ 説明的ではありません -->
<a href="/products">ここをクリック</a>
<a href="/widgets">詳細</a>

<!-- ✅ 説明的なアンカー テキスト -->
<a href="/products/blue-widgets">青色のウィジェット コレクションを参照する</a>
<a href="/guides/widget-maintenance">ウィジェットのメンテナンス方法を学ぶ</a>
「」

**リンクのガイドライン:**
- キーワードを含む説明的なアンカー テキスト
- 関連する内部ページへのリンク
- ページごとの適切なリンク数
- 壊れたリンクをすぐに修正する
- 階層にブレッドクラムを使用する

---

## 構造化データ (JSON-LD)

### 組織

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "組織",
  "name": "会社例",
  "url": "https://example.com",
  "ロゴ": "https://example.com/logo.png",
  "同じ": [
    "https://twitter.com/example",
    「https://linkedin.com/company/example」
  ]、
  "連絡先": {
    "@type": "連絡先",
    "電話": "+1-555-123-4567",
    "contactType": "カスタマーサービス"
  }
}
</script>
「」

### 記事

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "記事",
  "headline": "適切なウィジェットを選択する方法",
  "description": "ニーズに合ったウィジェットを選択するための完全なガイド。",
  "画像": "https://example.com/article-image.jpg",
  「著者」: {
    "@type": "人",
    "名前": "ジェーン・スミス",
    "url": "https://example.com/authors/jane-smith"
  }、
  「出版社」: {
    "@type": "組織",
    "name": "サンプルブログ",
    「ロゴ」: {
      "@type": "イメージオブジェクト",
      "url": "https://example.com/logo.png"
    }
  }、
  "公開日": "2024-01-15",
  "dateModified": "2024-01-20"
}
</script>
「」

### 製品

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "製品",
  "名前": "ブルーウィジェットプロ",
  "画像": "https://example.com/blue-widget.jpg",
  "description": "高度な機能を備えたプレミアムブルーのウィジェット。",
  「ブランド」: {
    "@type": "ブランド",
    "名前": "ウィジェットCo"
  }、
  「オファー」: {
    "@type": "オファー",
    "価格": "49.99",
    "価格通貨": "USD",
    "可用性": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  }、
  "集計評価": {
    "@type": "AggregateRating",
    "評価値": "4.8",
    "レビュー数": "1250"
  }
}
</script>
「」

### よくある質問

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "FAQページ",
  "メインエンティティ": [
    {
      "@type": "質問",
      "name": "何色がありますか?",
      "受け入れられた回答": {
        "@type": "回答",
        "text": "ウィジェットには青、赤、緑があります。"
      }
    }、
    {
      "@type": "質問",
      "name": "保証とは何ですか?",
      "受け入れられた回答": {
        "@type": "回答",
        "text": "すべてのウィジェットには 2 年間の保証が付いています。"
      }
    }
  ]
}
</script>
「」

### ブレッドクラム

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "パンくずリスト",
  "アイテムリスト要素": [
    {
      "@type": "ListItem",
      「位置」: 1、
      "名前": "家",
      "アイテム": "https://example.com"
    }、
    {
      "@type": "ListItem",
      「位置」: 2、
      "名前": "製品",
      "アイテム": "https://example.com/products"
    }、
    {
      "@type": "ListItem",
      「位置」: 3、
      "名前": "青いウィジェット",
      "アイテム": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
「」

### 検証

構造化データを次の場所でテストします。
- [Google リッチリザルト テスト](https://search.google.com/test/rich-results)
- [Schema.org バリデーター](https://validator.schema.org/)

---

## モバイル SEO

### レスポンシブデザイン

```html
<!-- ❌ モバイル対応ではありません -->
<meta name="viewport" content="width=1024">

<!-- ✅ レスポンシブビューポート -->
<meta name="viewport" content="width=device-width、initial-scale=1">
「」

### ターゲットをタップ

```css
/* ❌ 携帯するには小さすぎます */
.small-link {
  パディング: 4px;
  フォントサイズ: 12px;
}

/* ✅ 適切なタップターゲット */
.モバイルフレンドリーリンク {
  パディング: 12px;
  フォントサイズ: 16px;
  最小高さ: 48px;
  最小幅: 48px;
}
「」

### フォントサイズ

```css
/* ❌ モバイルでは小さすぎます */
ボディ{
  フォントサイズ: 10px;
}

/* ✅ 拡大縮小せずに読むことができます */
ボディ{
  フォントサイズ: 16px;
  行の高さ: 1.5;
}
「」
---
名称： 搜索引擎优化
描述：优化搜索引擎可见性和排名。当被要求“改进 SEO”、“优化搜索”、“修复元标记”、“添加结构化数据”、“站点地图优化”或“搜索引擎优化”时使用。
许可证：麻省理工学院
元数据：
  作者：网络质量技能
  版本：“1.0”
---

# SEO 优化

基于 Lighthouse SEO 审核和 Google 搜索指南的搜索引擎优化。专注于技术搜索引擎优化、页面优化和结构化数据。

## SEO 基础知识

搜索排名因素（大致影响）：

|因素 |影响力 |这个技能|
|--------|------------|------------|
|内容质量和相关性 | ~40% |部分（结构）|
|反向链接和权威 | 〜25% | ✗ |
|技术搜索引擎优化 | ~15% | ✓ |
|页面体验（核心网络生命）| 〜10% |请参阅 [核心 Web Vitals](../core-web-vitals/SKILL.md) |
|页面搜索引擎优化 | 〜10% | ✓ |

---

## 技术搜索引擎优化

### 可爬行性

**机器人.txt：**
````文本
# /机器人.txt
用户代理：*
允许：/

# 阻止管理/私人区域
禁止：/admin/
禁止：/api/
禁止：/私人/

# 不要阻塞渲染所需的资源
# ❌ 禁止：/static/

站点地图：https://example.com/sitemap.xml
````

**元机器人：**
````html
<!-- 默认值：可索引、可跟随 -->
<meta name="robots" content="index, follow">

<!-- Noindex 特定页面 -->
<meta name="robots" content="noindex, nofollow">

<!-- 可索引但不跟踪链接 -->
<meta name="robots" content="index, nofollow">

<!-- 控制片段 -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
````

**规范网址：**
````html
<!-- 防止重复内容问题 -->
<link rel="canonical" href="https://example.com/page">

<!-- 自引用规范（推荐）-->
<link rel="canonical" href="https://example.com/current-page">

<!-- 对于分页内容 -->
<link rel="canonical" href="https://example.com/products">
<!-- 或者使用 rel="prev" / rel="next" 进行显式分页 -->
````

### XML 站点地图

```xml
<?xml 版本=“1.0”编码=“UTF-8”?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <网址>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>每日</changefreq>
    <优先级>1.0</优先级>
  </网址>
  <网址>
    <loc>https://example.com/products</loc>
    <最后修改>2024-01-14</最后修改>
    <changefreq>每周</changefreq>
    <优先级>0.8</优先级>
  </网址>
</网址集>
````

**站点地图最佳实践：**
- 每个站点地图最多 50,000 个 URL 或 50MB
- 对较大的站点使用站点地图索引
- 仅包含规范的、可索引的 URL
- 内容更改时更新“lastmod”
- 提交到 Google 搜索控制台

### 网址结构

````
✅ 好的网址：
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ 糟糕的网址：
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
````

**网址指南：**
- 使用连字符，而不是下划线
- 仅小写
- 保持简短（< 75 个字符）
- 自然地包含目标关键词
- 尽可能避免使用参数
- 始终使用 HTTPS

### HTTPS 和安全

````html
<!-- 确保所有资源都使用 HTTPS -->
<img src="https://example.com/image.jpg">

<!-- 不是：-->
<img src="http://example.com/image.jpg">
````

**SEO 信任信号的安全标头：**
````
严格传输安全：max-age=31536000；包含子域
X-内容类型选项：nosniff
X 帧选项：拒绝
````

---

## 页面搜索引擎优化

### 标题标签

````html
<!-- ❌ 缺失或通用 -->
<标题>页面</标题>
<标题>首页</标题>

<!-- ✅ 使用主要关键字进行描述 -->
<title>蓝色小部件待售|优质品质 |示例商店</title>
````

**标题标签指南：**
- 50-60 个字符（Google 截断约 60 个）
- 开头附近的主要关键字
- 每个页面都是独一无二的
- 结尾处有品牌名称（主页除外）
- 适当时以行动为导向

### 元描述

````html
<!-- ❌ 缺失或重复 -->
<元名称=“描述”内容=“”>

<!-- ✅ 引人注目且独特 -->
<meta name="description" content="购买优质蓝色小部件，免运费。30 天退货。超过 10,000 名客户评价为 4.9/5。立即订购可节省 20%。">
````

**元描述指南：**
- 150-160 个字符
- 自然地包含主要关键字
- 引人注目的号召性用语
- 每个页面都是独一无二的
- 匹配页面内容

### 标题结构

````html
<!-- ❌ 结构不佳 -->
<h2>欢迎来到我们的商店</h2>
<h4>产品</h4>
<h1>联系我们</h1>

<!-- ✅ 正确的层次结构 -->
<h1>蓝色小部件 - 高品质</h1>
  <h2>产品功能</h2>
    <h3>耐用性</h3>
    <h3>设计</h3>
  <h2>客户评论</h2>
  <h2>定价</h2>
````

**标题指南：**
- 每页单个`<h1>`（主要主题）
- 逻辑层次结构（不要跳过级别）
- 自然地包含关键词
- 描述性的，而不是通用的

### 图片搜索引擎优化

````html
<!-- ❌ 糟糕的形象 SEO -->
<img src="IMG_12345.jpg">

<!-- ✅ 优化图像 -->
<img src="blue-widget-product-photo.webp"
     alt="带有镀铬饰面的蓝色小部件，侧视图显示控制面板"
     宽度=“800”
     高度=“600”
     加载=“懒惰”>
````

**图像指南：**
- 带关键字的描述性文件名
- 替代文本描述图像内容
- 压缩且大小合适
- 具有后备功能的 WebP/AVIF
- 延迟加载下屏图像

### 内部链接

````html
<!-- ❌非描述性 -->
<a href="/products">点击此处</a>
<a href="/widgets">了解更多</a>

<!-- ✅ 描述性锚文本 -->
<a href="/products/blue-widgets">浏览我们的蓝色小部件集合</a>
<a href="/guides/widget-maintenance">了解如何维护您的小部件</a>
````

**链接指南：**
- 带有关键词的描述性锚文本
- 相关内部页面的链接
- 每页的链接数量合理
- 及时修复损坏的链接
- 使用面包屑进行层次结构

---

## 结构化数据（JSON-LD）

### 组织

````html
<脚本类型=“应用程序/ld+json”>
{
  "@context": "https://schema.org",
  "@type": "组织",
  "name": "示例公司",
  "url": "https://example.com",
  “标志”：“https://example.com/logo.png”，
  “相同”：[
    “https://twitter.com/example”，
    “https://linkedin.com/company/example”
  ],
  “接触点”：{
    "@type": "接触点",
    “电话”：“+1-555-123-4567”，
    "contactType": "客户服务"
  }
}
</脚本>
````

### 文章

````html
<脚本类型=“应用程序/ld+json”>
{
  "@context": "https://schema.org",
  "@type": "文章",
  "headline": "如何选择合适的小部件",
  "description": "根据您的需求选择小部件的完整指南。",
  “图片”：“https://example.com/article-image.jpg”，
  “作者”：{
    "@type": "人",
    “姓名”：“简·史密斯”，
    “url”：“https://example.com/authors/jane-smith”
  },
  “出版商”：{
    "@type": "组织",
    "name": "示例博客",
    “标志”：{
      "@type": "图像对象",
      “url”：“https://example.com/logo.png”
    }
  },
  "发布日期": "2024-01-15",
  “修改日期”：“2024-01-20”
}
</脚本>
````

### 产品

````html
<脚本类型=“应用程序/ld+json”>
{
  "@context": "https://schema.org",
  "@type": "产品",
  "name": "Blue Widget Pro",
  “图像”：“https://example.com/blue-widget.jpg”，
  "description": "具有高级功能的高级蓝色小部件。",
  “品牌”：{
    "@type": "品牌",
    “名称”：“WidgetCo”
  },
  “优惠”：{
    "@type": "报价",
    “价格”：“49.99”，
    “价格货币”：“美元”，
    “可用性”：“https://schema.org/InStock”，
    “url”：“https://example.com/products/blue-widget”
  },
  “聚合评级”：{
    "@type": "聚合评级",
    “评级值”：“4.8”，
    “评论数”：“1250”
  }
}
</脚本>
````

### 常见问题解答

````html
<脚本类型=“应用程序/ld+json”>
{
  "@context": "https://schema.org",
  "@type": "常见问题解答页面",
  “主要实体”：[
    {
      "@type": "问题",
      "name": "有哪些颜色可供选择？",
      “接受答案”：{
        "@type": "回答",
        "text": "我们的小部件有蓝色、红色和绿色。"
      }
    },
    {
      "@type": "问题",
      "name": "保修是什么？",
      “接受答案”：{
        "@type": "回答",
        "text": "所有小部件均提供 2 年保修。"
      }
    }
  ]
}
</脚本>
````

### 面包屑

````html
<脚本类型=“应用程序/ld+json”>
{
  "@context": "https://schema.org",
  "@type": "面包屑列表",
  “项目列表元素”：[
    {
      "@type": "列表项",
      “位置”：1，
      “名称”：“家”，
      “项目”：“https://example.com”
    },
    {
      "@type": "列表项",
      “位置”：2，
      “名称”：“产品”，
      “项目”：“https://example.com/products”
    },
    {
      "@type": "列表项",
      “位置”：3，
      "name": "蓝色小部件",
      “项目”：“https://example.com/products/blue-widgets”
    }
  ]
}
</脚本>
````

### 验证

测试结构化数据：
- [Google 富媒体搜索结果测试](https://search.google.com/test/rich-results)
- [Schema.org 验证器](https://validator.schema.org/)

---

## 移动搜索引擎优化

### 响应式设计

````html
<!-- ❌ 不适合移动设备 -->
<元名称=“视口”内容=“宽度= 1024”>

<!-- ✅ 响应式视口 -->
<meta name =“viewport”content =“width = device-width，initial-scale = 1”>
````

### 点击目标

````CSS
/* ❌ 对于移动设备来说太小 */
.小链接{
  内边距：4px；
  字体大小：12px；
}

/* ✅ 足够的点击目标 */
.移动友好链接{
  内边距：12px；
  字体大小：16px；
  最小高度：48px；
  最小宽度：48px；
}
````

### 字体大小

````CSS
/* ❌ 在移动设备上太小 */
身体{
  字体大小：10px；
}

/* ✅ 无需缩放即可阅读 */
身体{
  字体大小：16px；
  行高：1.5；
}
````
---
назва: seo
опис: оптимізація для видимості в пошуковій системі та рейтингу. Використовуйте, коли запитують «покращити SEO», «оптимізувати для пошуку», «виправити мета-теги», «додати структуровані дані», «оптимізувати карту сайту» або «оптимізувати пошукову систему».
ліцензія: MIT
метадані:
  автор: web-quality-skills
  версія: "1.0"
---

# SEO оптимізація

Пошукова оптимізація на основі аудиту Lighthouse SEO та вказівок Google Search. Зосередьтеся на технічному SEO, оптимізації на сторінці та структурованих даних.

## Основи SEO

Фактори ранжування в пошуку (приблизний вплив):

| Фактор | Вплив | Цей навик |
|--------|-----------|------------|
| Якість і релевантність вмісту | ~40% | Часткова (структура) |
| Зворотні посилання та авторитет | ~25% | ✗ |
| Технічне SEO | ~15% | ✓ |
| Взаємодія зі сторінкою (Core Web Vitals) | ~10% | Див. [Core Web Vitals](../core-web-vitals/SKILL.md) |
| SEO на сторінці | ~10% | ✓ |

---

## Технічне SEO

### Можливість сканування

**robots.txt:**
```текст
# /robots.txt
Користувач-агент: *
Дозволити: /

# Блокувати адмін/приватні області
Заборонити: /admin/
Заборонити: /api/
Заборонити: /приватне/

# Не блокуйте ресурси, необхідні для візуалізації
# ❌ Заборонити: /static/

Карта сайту: https://example.com/sitemap.xml
```

**Мета-роботи:**
```html
<!-- Типове значення: індексується, слідкується -->
<meta name="robots" content="index, follow">

<!-- Спеціальні сторінки Noindex -->
<meta name="robots" content="noindex, nofollow">

<!-- Можна індексувати, але не переходити за посиланнями -->
<meta name="robots" content="index, nofollow">

<!-- Контрольні фрагменти -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**Канонічні URL-адреси:**
```html
<!-- Запобігайте проблемам із дублюванням вмісту -->
<link rel="canonical" href="https://example.com/page">

<!-- Канонічні самопосилання (рекомендовано) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Для розбитого на сторінки вмісту -->
<link rel="canonical" href="https://example.com/products">
<!-- Або використовуйте rel="prev" / rel="next" для явного розбиття на сторінки -->
```

### XML карта сайту

```xml
<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>2024-01-15</lastmod>
    <changefreq>щодня</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://example.com/products</loc>
    <lastmod>2024-01-14</lastmod>
    <changefreq>щотижня</changefreq>
    <пріоритет>0,8</пріоритет>
  </url>
</urlset>
```

**Найкращі методи роботи з картою сайту:**
- Максимум 50 000 URL-адрес або 50 Мб на карту сайту
- Використовуйте індекс карти сайту для великих сайтів
- Включайте лише канонічні URL-адреси, які можна індексувати
- Оновлювати `lastmod`, коли вміст змінюється
- Надіслати в Google Search Console

### Структура URL

```
✅ Хороші URL-адреси:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Погані URL-адреси:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Вказівки щодо URL-адреси:**
- Використовуйте дефіси, а не підкреслення
- Лише малі літери
- Коротко (< 75 символів)
- Додайте цільові ключові слова природно
- Уникайте параметрів, коли це можливо
- Завжди використовуйте HTTPS

### HTTPS і безпека

```html
<!-- Переконайтеся, що всі ресурси використовують HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Ні: -->
<img src="http://example.com/image.jpg">
```

**Заголовки безпеки для сигналів довіри SEO:**
```
Strict-Transport-Security: max-age=31536000; includeSubDomains
X-Content-Type-Options: nosniff
Параметри X-Frame: ВІДМОВИТИ
```

---

## SEO на сторінці

### Теги заголовків

```html
<!-- ❌ Відсутній або загальний -->
<title>Сторінка</title>
<title>Додому</title>

<!-- ✅ Опис із основним ключовим словом -->
<title>Сині віджети на продаж | Преміальна якість | Магазин прикладів</title>
```

**Вказівки щодо тегу заголовка:**
- 50-60 символів (Google скорочує ~60)
- Основне ключове слово на початку
- Унікальний для кожної сторінки
- Назва бренду в кінці (крім домашньої сторінки)
- Орієнтований на дії, коли це необхідно

### Мета описи

```html
<!-- ❌ Відсутній або дублікат -->
<meta name="description" content="">

<!-- ✅ Переконливий і унікальний -->
<meta name="description" content="Купуйте сині віджети преміум-класу з безкоштовною доставкою. Повернення протягом 30 днів. Оцінка 4,9/5 від 10 000+ клієнтів. Замовляйте сьогодні та заощаджуйте 20%">
```

**Вказівки щодо метаопису:**
- 150-160 символів
- Додайте основне ключове слово природно
- Переконливий заклик до дії
- Унікальний для кожної сторінки
- Відповідає вмісту сторінки

### Структура заголовка

```html
<!-- ❌ Погана структура -->
<h2>Ласкаво просимо до нашого магазину</h2>
<h4>Продукція</h4>
<h1>Зв'яжіться з нами</h1>

<!-- ✅ Правильна ієрархія -->
<h1>Сині віджети – преміальна якість</h1>
  <h2>Функції продукту</h2>
    <h3>Довговічність</h3>
    <h3>Дизайн</h3>
  <h2>Відгуки клієнтів</h2>
  <h2>Ціни</h2>
```

**Вказівки щодо заголовків:**
- Один `<h1>` на сторінку (основна тема)
- Логічна ієрархія (не пропускайте рівні)
- Додайте ключові слова природно
- Описовий, не загальний

### SEO зображення

```html
<!-- ❌ Погане SEO SEO -->
<img src="IMG_12345.jpg">

<!-- ✅ Оптимізоване зображення -->
<img src="blue-widget-product-photo.webp"
     alt="Синій віджет із хромованим покриттям, панель керування збоку"
     ширина="800"
     висота="600"
     loading="lazy">
```

**Вказівки щодо зображення:**
— Описові назви файлів із ключовими словами
- Альтернативний текст описує вміст зображення
- Стиснутий і відповідного розміру
- WebP/AVIF із запасними варіантами
- Відкладене завантаження зображень нижньої частини

### Внутрішнє посилання

```html
<!-- ❌ Без опису -->
<a href="/products">Натисніть тут</a>
<a href="/widgets">Докладніше</a>

<!-- ✅ Описовий прив’язний текст -->
<a href="/products/blue-widgets">Перегляньте нашу колекцію синіх віджетів</a>
<a href="/guides/widget-maintenance">Дізнайтеся, як підтримувати свої віджети</a>
```

**Правила зв’язування:**
- Описовий прив'язний текст із ключовими словами
- Посилання на відповідні внутрішні сторінки
- Розумна кількість посилань на сторінку
- Швидко виправляйте пошкоджені посилання
- Використовуйте панірувальні сухарі для ієрархії

---

## Структуровані дані (JSON-LD)

### Організація

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Організація",
  "name": "Приклад компанії",
  "url": "https://example.com",
  "logo": "https://example.com/logo.png",
  "sameAs": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "Точка контакту",
    "telephone": "+1-555-123-4567",
    "contactType": "обслуговування клієнтів"
  }
}
</script>
```

### Стаття

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Стаття",
  "headline": "Як вибрати правильний віджет",
  "description": "Повний посібник із вибору віджетів для ваших потреб.",
  "image": "https://example.com/article-image.jpg",
  "автор": {
    "@type": "Особа",
    "name": "Джейн Сміт",
    "url": "https://example.com/authors/jane-smith"
  },
  "видавець": {
    "@type": "Організація",
    "name": "Приклад блогу",
    "логотип": {
      "@type": "Об'єкт зображення",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "2024-01-15",
  "dateModified": "20.01.2024"
}
</script>
```

### Продукт

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Продукт",
  "name": "Blue Widget Pro",
  "image": "https://example.com/blue-widget.jpg",
  "description": "Преміальний синій віджет із розширеними функціями.",
  "бренд": {
    "@type": "Бренд",
    "name": "WidgetCo"
  },
  "пропозиції": {
    "@type": "Пропозиція",
    "ціна": "49,99",
    "priceCurrency": "USD",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4,8",
    "reviewCount": "1250"
  }
}
</script>
```

### FAQ

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Сторінка поширених запитань",
  "mainEntity": [
    {
      "@type": "Питання",
      "name": "Які кольори доступні?",
      "acceptedAnswer": {
        "@type": "Відповідь",
        "text": "Наші віджети доступні в синьому, червоному та зеленому кольорах."
      }
    },
    {
      "@type": "Питання",
      "name": "Яка гарантія?",
      "acceptedAnswer": {
        "@type": "Відповідь",
        "text": "На всі віджети надається 2-річна гарантія."
      }
    }
  ]
}
</script>
```

### Панірувальні сухарі

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Список навігації",
  "itemListElement": [
    {
      "@type": "Елемент списку",
      "позиція": 1,
      "name": "Дім",
      "item": "https://example.com"
    },
    {
      "@type": "Елемент списку",
      "позиція": 2,
      "name": "Продукція",
      "item": "https://example.com/products"
    },
    {
      "@type": "Елемент списку",
      "позиція": 3,
      "name": "Сині віджети",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Перевірка

Тестуйте структуровані дані за адресою:
- [Тест Google Rich Results](https://search.google.com/test/rich-results)
- [Перевірка Schema.org](https://validator.schema.org/)

---

## Мобільний SEO

### Адаптивний дизайн

```html
<!-- ❌ Не оптимізовано для мобільних пристроїв -->
<meta name="viewport" content="width=1024">

<!-- ✅ Чуйне вікно перегляду -->
<meta name="viewport" content="width=device-width, initial-scale=1">
```

### Торкніться мішеней

```css
/* ❌ Замалий для мобільного */
.small-link {
  відступ: 4px;
  розмір шрифту: 12px;
}

/* ✅ Адекватний елемент дотику */
.mobile-friendly-link {
  відступ: 12 пікселів;
  розмір шрифту: 16px;
  min-height: 48px;
  min-width: 48px;
}
```

### Розміри шрифту

```css
/* ❌ Замалий на мобільному пристрої */
тіло {
  розмір шрифту: 10px;
}

/* ✅ Читається без масштабування */
тіло {
  розмір шрифту: 16px;
  висота лінії: 1,5;
}
```
---
имя: сео
описание: Оптимизация для видимости и рейтинга в поисковых системах. Используйте, когда вас просят «улучшить SEO», «оптимизировать для поиска», «исправить метатеги», «добавить структурированные данные», «оптимизировать карту сайта» или «поисковую оптимизацию».
лицензия: Массачусетский технологический институт
метаданные:
  автор: web-quality-skills
  версия: "1.0"
---

# SEO-оптимизация

Поисковая оптимизация на основе SEO-аудита Lighthouse и рекомендаций Google Search. Сосредоточьтесь на техническом SEO, оптимизации страниц и структурированных данных.

## Основы SEO

Факторы ранжирования в поиске (приблизительное влияние):

| Фактор | Влияние | Этот навык |
|--------|-----------|------------|
| Качество и релевантность контента | ~40% | Частичная (структура) |
| Обратные ссылки и авторитет | ~25% | ✗ |
| Техническое SEO | ~15% | ✓ |
| Опыт страницы (основные веб-показатели) | ~10% | См. [Основные веб-показатели](../core-web-vitals/SKILL.md) |
| Внутреннее SEO | ~10% | ✓ |

---

## Техническое SEO

### Сканируемость

**robots.txt:**
```текст
# /robots.txt
Пользовательский агент: *
Разрешить: /

# Блокировать административные/частные области
Запретить: /admin/
Запретить: /api/
Запретить: /частный/

# Не блокируйте ресурсы, необходимые для рендеринга
# ❌ Запретить: /static/

Карта сайта: https://example.com/sitemap.xml.
```

**Мета-роботы:**
```html
<!-- По умолчанию: индексируемый, отслеживаемый -->
<meta name="robots" content="index, Follow">

<!-- Определенные страницы не индексируются -->
<meta name="robots" content="noindex, nofollow">

<!-- Можно индексировать, но не переходить по ссылкам -->
<meta name="robots" content="index, nofollow">

<!-- Управляющие фрагменты -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**Канонические URL:**
```html
<!-- Предотвратите проблемы с дублированием контента -->
<link rel="canonical" href="https://example.com/page">

<!-- Каноническая ссылка на самого себя (рекомендуется) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Для содержимого с разбивкой на страницы -->
<link rel="canonical" href="https://example.com/products">
<!-- Или используйте rel="prev" / rel="next" для явной нумерации страниц -->
```

### XML-карта сайта

```xml
<?xml версия="1.0" кодировка="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://example.com/</loc>
    <lastmod>15 января 2024 г.</lastmod>
    <changefreq>ежедневно</changefreq>
    <приоритет>1.0</приоритет>
  </url>
  <url>
    <loc>https://example.com/products</loc>
    <lastmod>14 января 2024</lastmod>
    <changefreq>еженедельно</changefreq>
    <приоритет>0,8</приоритет>
  </url>
</urlset>
```

**Рекомендации по использованию файлов Sitemap:**
- Максимум 50 000 URL-адресов или 50 МБ на карту сайта.
- Используйте индекс карты сайта для больших сайтов.
– Включайте только канонические индексируемые URL-адреса.
- Обновлять «lastmod» при изменении контента.
- Отправить в консоль поиска Google

### структура URL

```
✅ Хорошие URL-адреса:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ Плохие URL-адреса:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Рекомендации по URL:**
- Используйте дефисы, а не подчеркивания.
- Только строчные буквы
- Будьте краткими (< 75 символов)
– Включайте целевые ключевые слова естественным образом.
- Избегайте параметров, когда это возможно.
- Всегда используйте HTTPS

### HTTPS и безопасность

```html
<!-- Убедитесь, что все ресурсы используют HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Не: -->
<img src="http://example.com/image.jpg">
```

**Заголовки безопасности для сигналов доверия SEO:**
```
Строгая транспортная безопасность: максимальный возраст = 31536000; включить поддомены
X-Content-Type-Options: nosniff
Параметры X-Frame: DENY
```

---

## SEO на странице

### Теги заголовков

```html
<!-- ❌ Отсутствует или является общим -->
<title>Страница</title>
<title>Главная</title>

<!-- ✅ Описательное с основным ключевым словом -->
<title>Продажа синих виджетов | Премиальное качество | Пример магазина</title>
```

**Правила использования тегов заголовков:**
- 50–60 символов (Google обрезает примерно 60 символов).
- Основное ключевое слово в начале
- Уникальный для каждой страницы
- Название бренда в конце (кроме домашней страницы)
- Ориентированность на действия, когда это необходимо.

### Мета-описания

```html
<!-- ❌ Отсутствует или повторяется -->
<meta name="description" content="">

<!-- ✅ Привлекательный и уникальный -->
<meta name="description" content="Покупайте синие виджеты премиум-класса с бесплатной доставкой. Возврат в течение 30 дней. Оценка 4,9/5 от более чем 10 000 клиентов. Закажите сегодня и сэкономьте 20 %.">
```

**Рекомендации по метаописаниям:**
- 150-160 символов
– Включите основное ключевое слово естественным образом.
- Убедительный призыв к действию
- Уникальный для каждой страницы
- Соответствует содержимому страницы.

### Структура заголовка

```html
<!-- ❌ Плохая структура -->
<h2>Добро пожаловать в наш магазин</h2>
<h4>Продукты</h4>
<h1>Свяжитесь с нами</h1>

<!-- ✅ Правильная иерархия -->
<h1>Синие виджеты – высочайшее качество</h1>
  <h2>Характеристики продукта</h2>
    <h3>Долговечность</h3>
    <h3>Дизайн</h3>
  <h2>Отзывы клиентов</h2>
  <h2>Цены</h2>
```

**Рекомендации по заголовкам:**
- Один `<h1>` на странице (основная тема)
- Логическая иерархия (не пропускайте уровни)
- Включайте ключевые слова естественным образом
- Описательный, а не общий.

### SEO изображений

```html
<!-- ❌ Плохое SEO изображений -->
<img src="IMG_12345.jpg">

<!-- ✅ Оптимизированное изображение -->
<img src="blue-widget-product-photo.webp"
     alt="Синий виджет с хромированной отделкой, вид сбоку с панелью управления"
     ширина = "800"
     высота="600"
     loading="ленивый">
```

**Рекомендации по изображениям:**
- Описательные имена файлов с ключевыми словами
- Альтернативный текст описывает содержимое изображения.
- Сжат и имеет правильный размер.
- WebP/AVIF с резервными вариантами
- Ленивая загрузка изображений ниже сгиба.

### Внутренние ссылки

```html
<!-- ❌ Неописательный -->
<a href="/products">Нажмите здесь</a>
<a href="/widgets">Подробнее</a>

<!-- ✅ Описательный текст привязки -->
<a href="/products/blue-widgets">Просмотрите нашу коллекцию синих виджетов</a>
<a href="/guides/widget-maintenance">Узнайте, как обслуживать виджеты</a>
```

**Правила по созданию ссылок:**
- Описательный текст привязки с ключевыми словами.
- Ссылки на соответствующие внутренние страницы.
- Разумное количество ссылок на страницу.
- Быстрое исправление неработающих ссылок
- Используйте хлебные крошки для иерархии

---

## Структурированные данные (JSON-LD)

### Организация

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Организация",
  "name": "Пример компании",
  "url": "https://example.com",
  "логотип": "https://example.com/logo.png",
  "то же, что и": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "телефон": "+1-555-123-4567",
    "contactType": "служба поддержки клиентов"
  }
}
</скрипт>
```

### Статья

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Статья",
  "headline": "Как выбрать правильный виджет",
  "description": "Полное руководство по выбору виджетов для ваших нужд.",
  "image": "https://example.com/article-image.jpg",
  "автор": {
    "@type": "Человек",
    "name": "Джейн Смит",
    "url": "https://example.com/authors/jane-smith"
  },
  "издатель": {
    "@type": "Организация",
    "name": "Пример блога",
    "логотип": {
      "@type": "Объект изображения",
      "url": "https://example.com/logo.png"
    }
  },
  "datePublished": "15.01.2024",
  "dateModified": "20 января 2024 г."
}
</скрипт>
```

### Продукт

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Продукт",
  "name": "Blue Widget Pro",
  "image": "https://example.com/blue-widget.jpg",
  "description": "Премиум-синий виджет с расширенными функциями.",
  "бренд": {
    "@type": "Бренд",
    "name": "ВиджетКо"
  },
  "предложения": {
    "@type": "Предложение",
    "цена": "49,99",
    "priceCurrency": "доллар США",
    "availability": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "агрегатРейтинг": {
    "@type": "Совокупный рейтинг",
    "ratingValue": "4,8",
    "reviewCount": "1250"
  }
}
</скрипт>
```

### Часто задаваемые вопросы

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Страница часто задаваемых вопросов",
  "mainEntity": [
    {
      "@type": "Вопрос",
      "name": "Какие цвета доступны?",
      "acceptedAnswer": {
        "@type": "Ответ",
        "text": "Наши виджеты имеют синий, красный и зеленый цвета."
      }
    },
    {
      "@type": "Вопрос",
      "name": "Какая гарантия?",
      "acceptedAnswer": {
        "@type": "Ответ",
        "text": "На все виджеты предоставляется 2-летняя гарантия."
      }
    }
  ]
}
</скрипт>
```

### Панировочные сухари

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Хлебный список",
  "itemListElement": [
    {
      "@type": "ListItem",
      «позиция»: 1,
      "имя": "Дом",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      «позиция»: 2,
      "name": "Продукты",
      "item": "https://example.com/products"
    },
    {
      "@type": "ListItem",
      «позиция»: 3,
      "name": "Синие виджеты",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</скрипт>
```

### Проверка

Протестируйте структурированные данные по адресу:
– [Тест расширенных результатов Google](https://search.google.com/test/rich-results)
- [Валидатор Schema.org](https://validator.schema.org/)

---

## Мобильное SEO

### Адаптивный дизайн

```html
<!-- ❌ Не подходит для мобильных устройств -->
<meta name="viewport" content="width=1024">

<!-- ✅ Адаптивная область просмотра -->
<meta name="viewport" content="width=device-width, Initial-scale=1">
```

### Нажмите на цель

``` CSS
/* ❌ Слишком мал для мобильных устройств */
.small-ссылка {
  отступ: 4 пикселя;
  размер шрифта: 12 пикселей;
}

/* ✅ Адекватная цель касания */
.mobile-Friendly-ссылка {
  отступ: 12 пикселей;
  размер шрифта: 16 пикселей;
  минимальная высота: 48 пикселей;
  минимальная ширина: 48 пикселей;
}
```

### Размеры шрифта

``` CSS
/* ❌ Слишком маленький на мобильных устройствах */
тело {
  размер шрифта: 10 пикселей;
}

/* ✅ Читабельно без масштабирования */
тело {
  размер шрифта: 16 пикселей;
  высота строки: 1,5;
}
```
---
nome: seo
descrizione: Ottimizza per la visibilità e il posizionamento sui motori di ricerca. Utilizzare quando viene richiesto di "migliorare il SEO", "ottimizzare per la ricerca", "correggere i meta tag", "aggiungere dati strutturati", "ottimizzazione della mappa del sito" o "ottimizzazione dei motori di ricerca".
licenza: MIT
metadati:
  autore: competenze di qualità web
  versione: "1.0"
---

#Ottimizzazione SEO

Ottimizzazione per i motori di ricerca basata sugli audit SEO di Lighthouse e sulle linee guida di ricerca di Google. Concentrati sulla SEO tecnica, sull'ottimizzazione della pagina e sui dati strutturati.

## Fondamenti SEO

Fattori di ranking della ricerca (influenza approssimativa):

| Fattore | Influenza | Questa abilità |
|--------|-----------|----|
| Qualità e pertinenza dei contenuti | ~40% | Parziale (struttura) |
| Backlink e autorità | ~25% | ✗ |
| SEO tecnico | ~15% | ✓ |
| Esperienza sulla pagina (Core Web Vitals) | ~10% | Vedi [Core Web Vitals](../core-web-vitals/SKILL.md) |
| SEO on-page | ~10% | ✓ |

---

## SEO tecnica

### Scansione

**robot.txt:**
"testo".
# /robot.txt
Agente utente: *
Consenti: /

# Blocca aree amministrative/private
Non consentire: /admin/
Non consentire: /api/
Non consentire: /privato/

# Non bloccare le risorse necessarie per il rendering
# ❌ Disallow: /statico/

Mappa del sito: https://example.com/sitemap.xml
```

**Meta robot:**
```html
<!-- Predefinito: indicizzabile, seguibile -->
<meta name="robots" content="index, follow">

<!-- Pagine specifiche di Noindex -->
<meta name="robots" content="noindex, nofollow">

<!-- Indicizzabile ma non seguire i link -->
<meta name="robots" content="index, nofollow">

<!-- Snippet di controllo -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**URL canonici:**
```html
<!-- Previeni problemi relativi ai contenuti duplicati -->
<link rel="canonical" href="https://example.com/page">

<!-- Canonica autoreferenziale (consigliata) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Per contenuti impaginati -->
<link rel="canonical" href="https://example.com/products">
<!-- Oppure usa rel="prev" / rel="next" per l'impaginazione esplicita -->
```

### Mappa del sito XML

```xml
<?xml versione="1.0" codifica="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <url>
    <loc>https://esempio.com/</loc>
    <lastmod>15-01-2024</lastmod>
    <changefreq>giornaliero</changefreq>
    <priority>1.0</priority>
  </url>
  <url>
    <loc>https://esempio.com/prodotti</loc>
    <lastmod>14-01-2024</lastmod>
    <changefreq>settimanale</changefreq>
    <priorità>0.8</priority>
  </url>
</urlset>
```

**Best practice per la mappa del sito:**
- Massimo 50.000 URL o 50 MB per mappa del sito
- Utilizza l'indice della mappa del sito per i siti più grandi
- Includere solo URL canonici e indicizzabili
- Aggiorna `lastmod` quando il contenuto cambia
- Invia a Google Search Console

### Struttura dell'URL

```
✅ Buoni URL:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ URL scadenti:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Linee guida URL:**
- Utilizzare i trattini, non i caratteri di sottolineatura
- Solo minuscolo
- Mantienilo breve (< 75 caratteri)
- Includi parole chiave target in modo naturale
- Evitare i parametri quando possibile
- Utilizza sempre HTTPS

### HTTPS e sicurezza

```html
<!-- Assicurati che tutte le risorse utilizzino HTTPS -->
<img src="https://example.com/immagine.jpg">

<!-- Non: -->
<img src="http://example.com/immagine.jpg">
```

**Intestazioni di sicurezza per segnali di fiducia SEO:**
```
Sicurezza di trasporto rigorosa: età massima = 31536000; includeSottodomini
Opzioni tipo contenuto X: nosniff
Opzioni X-Frame: NEGA
```

---

## SEO on-page

### Tag del titolo

```html
<!-- ❌ Mancante o generico -->
<title>Pagina</title>
<title>Casa</title>

<!-- ✅ Descrittivo con parola chiave primaria -->
<title>Widget blu in vendita | Qualità Premium | Negozio di esempio</title>
```

**Linee guida sui tag del titolo:**
- 50-60 caratteri (Google tronca ~60)
- Parola chiave principale vicino all'inizio
- Unico per ogni pagina
- Nome del marchio alla fine (a meno che non sia la home page)
- Orientato all'azione quando appropriato

### Meta descrizioni

```html
<!-- ❌ Mancante o duplicato -->
<meta nome="descrizione" contenuto="">

<!-- ✅ Avvincente e unico -->
<meta name="description" content="Acquista widget blu premium con spedizione gratuita. Resi entro 30 giorni. Valutato 4,9/5 da oltre 10.000 clienti. Ordina oggi e risparmia il 20%.">
```

**Linee guida per la meta descrizione:**
- 150-160 caratteri
- Includi la parola chiave principale in modo naturale
- Invito all'azione convincente
- Unico per ogni pagina
- Corrisponde al contenuto della pagina

### Struttura dell'intestazione

```html
<!-- ❌Struttura pessima -->
<h2>Benvenuti nel nostro negozio</h2>
<h4>Prodotti</h4>
<h1>Contattaci</h1>

<!-- ✅ Gerarchia corretta -->
<h1>Widget blu: qualità premium</h1>
  <h2>Caratteristiche del prodotto</h2>
    <h3>Durabilità</h3>
    <h3>Progettazione</h3>
  <h2>Recensioni dei clienti</h2>
  <h2>Prezzi</h2>
```

**Linee guida per le intestazioni:**
- Singolo `<h1>` per pagina (l'argomento principale)
- Gerarchia logica (non saltare i livelli)
- Includi parole chiave in modo naturale
- Descrittivo, non generico

### SEO delle immagini

```html
<!-- ❌ SEO dell'immagine scadente -->
<img src="IMG_12345.jpg">

<!-- ✅ Immagine ottimizzata -->
<img src="blue-widget-prodotto-foto.webp"
     alt="Widget blu con finitura cromata, vista laterale che mostra il pannello di controllo"
     larghezza="800"
     altezza="600"
     caricamento="pigro">
```

**Linee guida per le immagini:**
- Nomi di file descrittivi con parole chiave
- Il testo alternativo descrive il contenuto dell'immagine
- Compresso e di dimensioni adeguate
- WebP/AVIF con fallback
- Caricamento lento delle immagini sotto la piega

### Collegamento interno

```html
<!-- ❌ Non descrittivo -->
<a href="/products">Fai clic qui</a>
<a href="/widgets">Ulteriori informazioni</a>

<!-- ✅ Testo di ancoraggio descrittivo -->
<a href="/products/blue-widgets">Sfoglia la nostra raccolta di widget blu</a>
<a href="/guides/widget-maintenance">Scopri come mantenere i tuoi widget</a>
```

**Linee guida per il collegamento:**
- Testo di ancoraggio descrittivo con parole chiave
- Collegamento alle pagine interne pertinenti
- Numero ragionevole di collegamenti per pagina
- Risolvi tempestivamente i collegamenti interrotti
- Usa il breadcrumb per la gerarchia

---

## Dati strutturati (JSON-LD)

### Organizzazione

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organizzazione",
  "nome": "Azienda di esempio",
  "url": "https://esempio.com",
  "logo": "https://example.com/logo.png",
  "uguale a": [
    "https://twitter.com/esempio",
    "https://linkedin.com/azienda/esempio"
  ],
  "punto di contatto": {
    "@type": "ContactPoint",
    "telefono": "+1-555-123-4567",
    "contactType": "servizio clienti"
  }
}
</script>
```

###Articolo

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Articolo",
  "headline": "Come scegliere il widget giusto",
  "description": "Guida completa per selezionare i widget per le tue esigenze.",
  "immagine": "https://example.com/articolo-immagine.jpg",
  "autore": {
    "@type": "Persona",
    "nome": "Jane Smith",
    "url": "https://example.com/authors/jane-smith"
  },
  "editore": {
    "@type": "Organizzazione",
    "name": "Blog di esempio",
    "logo": {
      "@type": "OggettoImmagine",
      "url": "https://example.com/logo.png"
    }
  },
  "dataPubblicazione": "2024-01-15",
  "dateModified": "2024-01-20"
}
</script>
```

### Prodotto

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Prodotto",
  "nome": "Blue Widget Pro",
  "immagine": "https://example.com/blue-widget.jpg",
  "description": "Widget blu premium con funzionalità avanzate.",
  "marca": {
    "@type": "Marca",
    "nome": "WidgetCo"
  },
  "offerte": {
    "@type": "Offerta",
    "prezzo": "49,99",
    "priceCurrency": "USD",
    "disponibilità": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "aggregateRating": {
    "@type": "AggregateRating",
    "ratingValue": "4.8",
    "reviewCount": "1250"
  }
}
</script>
```

### Domande frequenti

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "PaginaFAQ",
  "entitàprincipale": [
    {
      "@type": "Domanda",
      "name": "Quali colori sono disponibili?",
      "risposta accettata": {
        "@type": "Rispondi",
        "text": "I nostri widget sono disponibili in blu, rosso e verde."
      }
    },
    {
      "@type": "Domanda",
      "name": "Qual è la garanzia?",
      "risposta accettata": {
        "@type": "Rispondi",
        "text": "Tutti i widget includono una garanzia di 2 anni."
      }
    }
  ]
}
</script>
```

### Pangrattato

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Lista breadcrumb",
  "ElementoListaArticoli": [
    {
      "@type": "ElementoLista",
      "posizione": 1,
      "nome": "Casa",
      "elemento": "https://example.com"
    },
    {
      "@type": "ElementoLista",
      "posizione": 2,
      "nome": "Prodotti",
      "articolo": "https://example.com/prodotti"
    },
    {
      "@type": "ElementoLista",
      "posizione": 3,
      "nome": "Widget blu",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Convalida

Testare i dati strutturati su:
- [Test dei risultati avanzati di Google](https://search.google.com/test/rich-results)
- [Convalidatore di Schema.org](https://validator.schema.org/)

---

## SEO mobile

### Design reattivo

```html
<!-- ❌ Non ottimizzato per i dispositivi mobili -->
<meta name="viewport" content="width=1024">

<!-- ✅ Visualizzazione reattiva -->
<meta name="viewport" content="width=larghezza-dispositivo, scala-iniziale=1">
```

### Tocca i target

```css
/* ❌ Troppo piccolo per i dispositivi mobili */
.piccolo collegamento {
  imbottitura: 4px;
  dimensione carattere: 12px;
}

/* ✅ Target di tocco adeguato */
.link ottimizzato per dispositivi mobili {
  imbottitura: 12px;
  dimensione carattere: 16px;
  altezza minima: 48px;
  larghezza minima: 48px;
}
```

### Dimensioni dei caratteri

```css
/* ❌ Troppo piccolo sul cellulare */
corpo {
  dimensione carattere: 10px;
}

/* ✅ Leggibile senza zoom */
corpo {
  dimensione carattere: 16px;
  altezza della linea: 1,5;
}
```
---
nome: seo
descrição: Otimize para visibilidade e classificação em mecanismos de pesquisa. Use quando solicitado a "melhorar SEO", "otimizar para pesquisa", "corrigir meta tags", "adicionar dados estruturados", "otimização de mapa de site" ou "otimização de mecanismo de pesquisa".
licença: MIT
metadados:
  autor: habilidades de qualidade na web
  versão: "1.0"
---

# Otimização SEO

Otimização de mecanismos de pesquisa com base nas auditorias Lighthouse SEO e nas diretrizes da Pesquisa Google. Concentre-se em SEO técnico, otimização on-page e dados estruturados.

## Fundamentos de SEO

Fatores de classificação de pesquisa (influência aproximada):

| Fator | Influência | Esta habilidade |
|--------|-----------|-----------|
| Qualidade e relevância do conteúdo | ~40% | Parcial (estrutura) |
| Backlinks e autoridade | ~25% | ✗ |
| SEO técnico | ~15% | ✓ |
| Experiência de página (Core Web Vitals) | ~10% | Consulte [Core Web Vitals](../core-web-vitals/SKILL.md) |
| SEO na página | ~10% | ✓ |

---

## SEO Técnico

### Rastreabilidade

**robôs.txt:**
```texto
# /robôs.txt
Agente do usuário: *
Permitir: /

# Bloquear áreas administrativas/privadas
Proibir: /admin/
Não permitir: /api/
Proibir: /privado/

# Não bloqueie recursos necessários para renderização
# ❌ Proibir: /static/

Mapa do site: https://example.com/sitemap.xml
```

**Meta-robôs:**
```html
<!-- Padrão: indexável, seguivel -->
<meta name="robôs" content="index, follow">

<!-- Páginas específicas do Noindex -->
<meta name="robôs" content="noindex, nofollow">

<!-- Indexável, mas não segue links -->
<meta name="robôs" content="index, nofollow">

<!-- Trechos de controle -->
<meta name="robots" content="max-snippet:150, max-image-preview:large">
```

**URLs canônicos:**
```html
<!-- Evite problemas de conteúdo duplicado -->
<link rel="canonical" href="https://example.com/page">

<!-- Auto-referência canônica (recomendado) -->
<link rel="canonical" href="https://example.com/current-page">

<!-- Para conteúdo paginado -->
<link rel="canonical" href="https://example.com/products">
<!-- Ou use rel="prev" / rel="next" para paginação explícita -->
```

### Mapa do site XML

```xml
<?xml versão="1.0" codificação="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
  <URL>
    <loc>https://example.com/</loc>
    <lastmod>15/01/2024</lastmod>
    <changefreq>diariamente</changefreq>
    <prioridade>1.0</prioridade>
  </url>
  <URL>
    <loc>https://example.com/products</loc>
    <lastmod>14/01/2024</lastmod>
    <changefreq>semanalmente</changefreq>
    <prioridade>0,8</prioridade>
  </url>
</urlset>
```

**Práticas recomendadas para mapas de site:**
- Máximo de 50.000 URLs ou 50 MB por sitemap
- Use o índice do mapa do site para sites maiores
- Incluir apenas URLs canônicos e indexáveis
- Atualize `lastmod` quando o conteúdo mudar
- Enviar para o Google Search Console

### Estrutura de URL

```
✅ Bons URLs:
https://example.com/products/blue-widget
https://example.com/blog/how-to-use-widgets

❌ URLs ruins:
https://example.com/p?id=12345
https://example.com/products/item/category/subcategory/blue-widget-2024-sale-discount
```

**Diretrizes de URL:**
- Use hífens, não sublinhados
- Somente letras minúsculas
- Seja breve (<75 caracteres)
- Incluir palavras-chave alvo naturalmente
- Evite parâmetros quando possível
- Use HTTPS sempre

### HTTPS e segurança

```html
<!-- Certifique-se de que todos os recursos usem HTTPS -->
<img src="https://example.com/image.jpg">

<!-- Não: -->
<img src="http://example.com/image.jpg">
```

**Cabeçalhos de segurança para sinais de confiança de SEO:**
```
Segurança de transporte estrita: idade máxima = 31536000; incluirSubDomínios
Opções de tipo de conteúdo X: nosniff
Opções de quadro X: NEGAR
```

---

## SEO na página

### Tags de título

```html
<!-- ❌ Ausente ou genérico -->
<título>Página</título>
<title>Página inicial</title>

<!-- ✅ Descritivo com palavra-chave primária -->
<title>Widgets azuis à venda | Qualidade Premium | Exemplo de loja</title>
```

**Diretrizes para tags de título:**
- 50-60 caracteres (o Google trunca aproximadamente 60)
- Palavra-chave primária perto do início
- Único para cada página
- Nome da marca no final (exceto na página inicial)
- Orientado para a ação quando apropriado

### Meta descrições

```html
<!-- ❌ Ausente ou duplicado -->
<meta name="descrição" content="">

<!-- ✅ Atraente e único -->
<meta name="description" content="Compre widgets azuis premium com frete grátis. Devoluções em 30 dias. Classificação 4,9/5 por mais de 10.000 clientes. Faça seu pedido hoje e economize 20%.">
```

**Diretrizes para meta descrição:**
- 150-160 caracteres
- Incluir palavra-chave primária naturalmente
- Chamada para ação atraente
- Único para cada página
- Corresponde ao conteúdo da página

### Estrutura do título

```html
<!-- ❌ Estrutura ruim -->
<h2>Bem-vindo à nossa loja</h2>
<h4>Produtos</h4>
<h1>Entre em contato conosco</h1>

<!-- ✅ Hierarquia adequada -->
<h1>Widgets azuis - qualidade premium</h1>
  <h2>Recursos do produto</h2>
    <h3>Durabilidade</h3>
    <h3>Projeto</h3>
  <h2>Avaliações de clientes</h2>
  <h2>Preços</h2>
```

**Diretrizes de título:**
- Único `<h1>` por página (o tópico principal)
- Hierarquia lógica (não pule níveis)
- Incluir palavras-chave naturalmente
- Descritivo, não genérico

### SEO de imagem

```html
<!-- ❌ SEO de imagem ruim -->
<img src="IMG_12345.jpg">

<!-- ✅ Imagem otimizada -->
<img src="blue-widget-product-photo.webp"
     alt="Widget azul com acabamento cromado, vista lateral mostrando o painel de controle"
     largura = "800"
     altura = "600"
     carregando="preguiçoso">
```

**Diretrizes de imagem:**
- Nomes de arquivos descritivos com palavras-chave
- O texto alternativo descreve o conteúdo da imagem
- Compactado e dimensionado adequadamente
- WebP/AVIF com substitutos
- Carregamento lento de imagens abaixo da dobra

### Link interno

```html
<!-- ❌ Não descritivo -->
<a href="/products">Clique aqui</a>
<a href="/widgets">Leia mais</a>

<!-- ✅ Texto âncora descritivo -->
<a href="/products/blue-widgets">Navegue em nossa coleção de widgets azuis</a>
<a href="/guides/widget-maintenance">Aprenda como manter seus widgets</a>
```

**Diretrizes de vinculação:**
- Texto âncora descritivo com palavras-chave
- Link para páginas internas relevantes
- Número razoável de links por página
- Corrija links quebrados imediatamente
- Use breadcrumbs para hierarquia

---

## Dados estruturados (JSON-LD)

### Organização

```html
<script type="application/ld+json">
{
  "@contexto": "https://schema.org",
  "@type": "Organização",
  "nome": "Empresa Exemplo",
  "url": "https://example.com",
  "logotipo": "https://example.com/logo.png",
  "mesmos": [
    "https://twitter.com/example",
    "https://linkedin.com/company/example"
  ],
  "contactPoint": {
    "@type": "ContactPoint",
    "telefone": "+1-555-123-4567",
    "contactType": "atendimento ao cliente"
  }
}
</script>
```

### Artigo

```html
<script type="application/ld+json">
{
  "@contexto": "https://schema.org",
  "@type": "Artigo",
  "headline": "Como escolher o widget certo",
  "description": "Guia completo para selecionar widgets de acordo com suas necessidades.",
  "imagem": "https://example.com/article-image.jpg",
  "autor": {
    "@type": "Pessoa",
    "nome": "Jane Smith",
    "url": "https://example.com/authors/jane-smith"
  },
  "editor": {
    "@type": "Organização",
    "nome": "Exemplo de blog",
    "logotipo": {
      "@type": "ImageObject",
      "url": "https://example.com/logo.png"
    }
  },
  "data de publicação": "15/01/2024",
  "dataModificada": "2024-01-20"
}
</script>
```

### Produto

```html
<script type="application/ld+json">
{
  "@contexto": "https://schema.org",
  "@type": "Produto",
  "nome": "Blue Widget Pro",
  "imagem": "https://example.com/blue-widget.jpg",
  "description": "Widget azul premium com recursos avançados.",
  "marca": {
    "@type": "Marca",
    "nome": "WidgetCo"
  },
  "ofertas": {
    "@type": "Oferta",
    "preço": "49,99",
    "preçoMoeda": "USD",
    "disponibilidade": "https://schema.org/InStock",
    "url": "https://example.com/products/blue-widget"
  },
  "agregaçãoRating": {
    "@type": "AgregaçãoRating",
    "avaliaçãoValor": "4,8",
    "reviewCount": "1250"
  }
}
</script>
```

### Perguntas frequentes

```html
<script type="application/ld+json">
{
  "@contexto": "https://schema.org",
  "@type": "FAQPágina",
  "entidade principal": [
    {
      "@type": "Pergunta",
      "nome": "Quais cores estão disponíveis?",
      "aceitaResposta": {
        "@type": "Responder",
        "text": "Nossos widgets vêm em azul, vermelho e verde."
      }
    },
    {
      "@type": "Pergunta",
      "nome": "Qual é a garantia?",
      "aceitaResposta": {
        "@type": "Responder",
        "text": "Todos os widgets incluem garantia de 2 anos."
      }
    }
  ]
}
</script>
```

### Pão ralado

```html
<script type="application/ld+json">
{
  "@contexto": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {
      "@type": "ListItem",
      "posição": 1,
      "nome": "Casa",
      "item": "https://example.com"
    },
    {
      "@type": "ListItem",
      "posição": 2,
      "nome": "Produtos",
      "item": "https://example.com/products"
    },
    {
      "@type": "ListItem",
      "posição": 3,
      "nome": "Widgets Azuis",
      "item": "https://example.com/products/blue-widgets"
    }
  ]
}
</script>
```

### Validação

Teste dados estruturados em:
- [Teste de pesquisa aprimorada do Google](https://search.google.com/test/rich-results)
- [Validador Schema.org](https://validator.schema.org/)

---

## SEO móvel

### Design responsivo

```html
<!-- ❌ Não compatível com dispositivos móveis -->
<meta name="viewport" content="width=1024">

<!-- ✅ Janela de visualização responsiva -->
<meta name="viewport" content="largura=largura do dispositivo, escala inicial=1">
```

### Toque nos alvos

```css
/* ❌ Muito pequeno para celular */
.link pequeno {
  preenchimento: 4px;
  tamanho da fonte: 12px;
}

/* ✅ Alvo de toque adequado */
.link compatível com dispositivos móveis {
  preenchimento: 12px;
  tamanho da fonte: 16px;
  altura mínima: 48px;
  largura mínima: 48px;
}
```

### Tamanhos de fonte

```css
/* ❌ Muito pequeno no celular */
corpo {
  tamanho da fonte: 10px;
}

/* ✅ Legível sem zoom */
corpo {
  tamanho da fonte: 16px;
  altura da linha: 1,5;
}
```