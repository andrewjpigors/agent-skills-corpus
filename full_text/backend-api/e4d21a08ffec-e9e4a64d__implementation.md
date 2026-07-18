---
name: "implementation"
tags: [coding, scaffold, solidjs, micronaut, bun, java, typescript, tailwindcss, iconify]
description: |
  Full-stack implementation skill for the "Implementation (Coding)" phase of the SDLC.
  Provides complete project scaffolds, code generators, and convention audits for
  SolidJS + SolidStart (frontend) and Micronaut (backend) projects.

  Trigger phrases:
    - "scaffold project"
    - "create component"
    - "implement feature"
    - "generate code"
    - "create API endpoint"
    - "solidjs component"
    - "micronaut controller"
    - "add a route"
    - "create service"
    - "generate DTO"
    - "scaffold frontend"
    - "scaffold backend"
    - "check code conventions"
---

# Implementation (Coding)

This is the **primary implementation skill** for the agentden SDLC framework. It contains complete project scaffolds and code generators for the full-stack architecture:

- **Frontend**: Bun + TypeScript + SolidJS + SolidStart + TailwindCSS 4 + Iconify
- **Backend**: Java 21 + Micronaut 4 + Gradle Kotlin DSL + Shadow JAR

## Commands

| Command | Description |
|---|---|
| `/impl scaffold-frontend` | Scaffold complete frontend project from template |
| `/impl scaffold-backend` | Scaffold complete backend project from template |
| `/impl component` | Generate a SolidJS component with TypeScript |
| `/impl route` | Generate a SolidStart route page |
| `/impl controller` | Generate a Micronaut controller with CRUD |
| `/impl service` | Generate a Micronaut service class |
| `/impl repository` | Generate a Micronaut data repository |
| `/impl dto` | Generate Java 21 record DTOs |
| `/impl check` | Audit code against project conventions |

## Tech Stack Reference

### Frontend Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Runtime | Bun | 1.2+ | Package manager, bundler, test runner |
| Language | TypeScript | 5.8+ | Strict mode enabled (`strict: true`) |
| Framework | SolidJS | 1.9+ | Fine-grained reactivity, no virtual DOM |
| Meta Framework | SolidStart | Latest | SSG mode (`preset: "static"`) |
| Routing | @solidjs/router | Latest | File-based routing via `src/routes/` |
| Meta Tags | @solidjs/meta | Latest | `<Title>`, `<Meta>`, `<Link>` components |
| Styling | TailwindCSS | 4.1+ | CSS-first config (`@import "tailwindcss"`, `@theme` in CSS) |
| Icons | @iconify-icon/solid | 2.x | `<Icon icon="...">` component |
| Unit Tests | Vitest | Latest | With `@solidjs/testing-library` |
| E2E Tests | Playwright | Latest | Browser automation |
| Linting | ESLint | 9+ | Flat config (`eslint.config.js`) |
| Formatting | Prettier | 3+ | With `prettier-plugin-tailwindcss` |
| Build | Vinxi | Latest | Powers SolidStart's build pipeline |
| Container | nginx | stable-alpine | Static file serving, gzip, security headers |

### Backend Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Language | Java | 21 (LTS) | Records, sealed interfaces, virtual threads, pattern matching |
| Framework | Micronaut | 4.7+ | Compile-time DI, AOT, low memory footprint |
| Build | Gradle | 8.13+ | Kotlin DSL (`build.gradle.kts`) |
| Packaging | Shadow JAR | 8.3.6 | Fat JAR via `com.gradleup.shadow` |
| Serialization | micronaut-serde-jackson | — | Compile-time JSON serialization |
| Validation | micronaut-validation | — | With `jakarta.validation-api` |
| Logging | Logback | — | Configured via `logback.xml` |
| Testing | JUnit 5 | — | With `micronaut-test-junit5` |
| HTTP Client | micronaut-http-client | — | Declarative HTTP client for tests |
| Container | Liberica CRaC | jdk-21 | CRaC + CDS + musl for minimal image |

### Java 21 Features (Required)

All Java code **must** use these features where applicable:

```java
// Records for DTOs (no Lombok)
public record CreatePersonRequest(
    @NotBlank String name,
    @Email String email,
    @NotNull LocalDate birthDate
) {}

// Sealed interfaces for domain modeling
public sealed interface Result<T> {
    record Success<T>(T data) implements Result<T> {}
    record Failure<T>(String error, int status) implements Result<T> {}
}

// Pattern matching for switch
String formatted = switch (status) {
    case 200 -> "OK";
    case 404 -> "Not Found";
    case 500 -> "Server Error";
    default -> "Unknown";
};

// Virtual threads (enabled via --enable-preview + micronaut config)
// Pattern matching for instanceof
if (response instanceof ErrorResponse(var message, var status)) {
    log.error("Error: {} - {}", status, message);
}
```

JVM flags in Dockerfile: `--enable-preview -XX:+UseCompactObjectHeaders`

---

## Command: `/impl scaffold-frontend`

Scaffolds a complete frontend project from the template in `references/frontend-scaffold/`.

### Instructions

1. **Determine target directory**: Ask the user for the project name or target directory. Default: `frontend/` in the current workspace root.

2. **Copy template files**: Copy all files from `references/frontend-scaffold/` to the target directory. This includes:
   ```
   frontend/
   ├── app.config.ts
   ├── package.json
   ├── tsconfig.json
   ├── vitest.config.ts
   ├── eslint.config.js
   ├── .prettierrc
   ├── Dockerfile
   ├── nginx.conf
   ├── .dockerignore
   ├── .gitignore
   ├── env.d.ts
   ├── public/
   │   └── robots.txt
   ├── test/
   │   └── setup.ts
   └── src/
       ├── entry-client.tsx
       ├── entry-server.tsx
       ├── app.tsx
       ├── app.css
       └── routes/
           └── index.tsx
   ```

3. **Customize package.json**: Replace `"name": "frontend-app"` with the user's project name.

4. **Install dependencies**: Run `bun install` in the target directory.

5. **Verify**: Run `bun run build` to confirm the scaffold compiles. Report success or errors.

### Post-scaffold Verification Checklist

- [ ] `bun install` completed without errors
- [ ] `bun run dev` starts dev server on port 3000
- [ ] `bun run build` produces output in `.output/public/`
- [ ] `bun run lint` passes with no errors
- [ ] `bun run format` runs without errors
- [ ] `bun test` passes (if tests exist)

### Template File: `app.config.ts`

```typescript
import { defineConfig } from "@solidjs/start/config";
import tailwindcss from "@tailwindcss/vite";

export default defineConfig({
  server: {
    preset: "static",
  },
  vite: {
    plugins: [tailwindcss()],
    resolve: {
      alias: {
        "~": new URL("./src", import.meta.url).pathname,
      },
    },
  },
});
```

### Template File: `package.json`

```json
{
  "name": "frontend-app",
  "type": "module",
  "scripts": {
    "dev": "vinxi dev",
    "build": "vinxi build",
    "start": "vinxi start",
    "lint": "eslint . --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,css,json}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,css,json}\"",
    "test": "vitest run",
    "test:watch": "vitest",
    "test:coverage": "vitest run --coverage",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "solid-js": "^1.9.5",
    "@solidjs/start": "^1.1.3",
    "@solidjs/router": "^0.15.3",
    "@solidjs/meta": "^0.29.4",
    "@iconify-icon/solid": "^2.1.0",
    "vinxi": "^0.6.3"
  },
  "devDependencies": {
    "tailwindcss": "^4.1.4",
    "@tailwindcss/vite": "^4.1.4",
    "typescript": "^5.8.3",
    "vitest": "^3.1.2",
    "@solidjs/testing-library": "^0.8.10",
    "eslint": "^9.24.0",
    "eslint-plugin-solid": "^0.14.5",
    "@typescript-eslint/eslint-plugin": "^8.30.1",
    "@typescript-eslint/parser": "^8.30.1",
    "prettier": "^3.5.3",
    "prettier-plugin-tailwindcss": "^0.6.11",
    "@playwright/test": "^1.52.0",
    "jsdom": "^26.1.0"
  }
}
```

### Template File: `tsconfig.json`

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ESNext",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "jsxImportSource": "solid-js",
    "types": ["vinxi/types/client"],
    "noEmit": true,
    "isolatedModules": true,
    "esModuleInterop": true,
    "forceConsistentCasingInFileNames": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "paths": {
      "~/*": ["./src/*"]
    }
  },
  "include": ["src/**/*.ts", "src/**/*.tsx", "env.d.ts"]
}
```

### Template File: `vitest.config.ts`

```typescript
import { defineConfig } from "vitest/config";
import solidPlugin from "vite-plugin-solid";

export default defineConfig({
  plugins: [solidPlugin()],
  test: {
    environment: "jsdom",
    setupFiles: ["./test/setup.ts"],
    globals: true,
    include: ["src/**/*.test.{ts,tsx}"],
  },
  resolve: {
    alias: {
      "~": new URL("./src", import.meta.url).pathname,
    },
  },
});
```

### Template File: `eslint.config.js`

```javascript
import eslint from "@typescript-eslint/eslint-plugin";
import tsParser from "@typescript-eslint/parser";
import solidPlugin from "eslint-plugin-solid";

export default [
  {
    files: ["**/*.{ts,tsx}"],
    languageOptions: {
      parser: tsParser,
      parserOptions: {
        ecmaVersion: "latest",
        sourceType: "module",
        ecmaFeatures: { jsx: true },
      },
    },
    plugins: {
      "@typescript-eslint": eslint,
      solid: solidPlugin,
    },
    rules: {
      ...eslint.configs.recommended.rules,
      ...solidPlugin.configs.recommended.rules,
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/no-unused-vars": [
        "error",
        { argsIgnorePattern: "^_" },
      ],
    },
  },
  {
    ignores: [".output/", "node_modules/", "dist/"],
  },
];
```

### Template File: `.prettierrc`

```json
{
  "semi": true,
  "singleQuote": false,
  "tabWidth": 2,
  "trailingComma": "all",
  "printWidth": 80,
  "plugins": ["prettier-plugin-tailwindcss"]
}
```

### Template File: `Dockerfile`

```dockerfile
FROM oven/bun:1 AS build
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM nginx:stable-alpine AS runtime
COPY --from=build /app/.output/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Template File: `nginx.conf`

```nginx
server {
    listen 80;
    server_name _;
    root /usr/share/nginx/html;
    index index.html;

    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml text/javascript image/svg+xml;
    gzip_min_length 256;
    gzip_comp_level 6;

    location /assets/ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff2)$ {
        expires 30d;
        add_header Cache-Control "public, no-transform";
    }

    location /health {
        access_log off;
        return 200 'ok';
        add_header Content-Type text/plain;
    }

    location / {
        try_files $uri $uri/ /index.html;
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

### Template File: `.dockerignore`

```
node_modules/
.output/
dist/
.git/
*.md
.env*
.vscode/
```

### Template File: `.gitignore`

```
node_modules/
.output/
dist/
.env
.env.local
*.log
.DS_Store
coverage/
```

### Template File: `env.d.ts`

```typescript
/// <reference types="vinxi/types/client" />
```

### Template File: `public/robots.txt`

```
User-agent: *
Allow: /
```

### Template File: `test/setup.ts`

```typescript
import "@solidjs/testing-library";
```

### Template File: `src/entry-client.tsx`

```tsx
// @refresh reload
import { mount, StartClient } from "@solidjs/start/client";

mount(() => <StartClient />, document.getElementById("app")!);
```

### Template File: `src/entry-server.tsx`

```tsx
// @refresh reload
import { createHandler, StartServer } from "@solidjs/start/server";

export default createHandler(() => (
  <StartServer
    document={({ assets, children, scripts }) => (
      <html lang="en">
        <head>
          <meta charset="utf-8" />
          <meta
            name="viewport"
            content="width=device-width, initial-scale=1"
          />
          <link rel="icon" href="/favicon.ico" />
          {assets}
        </head>
        <body>
          <div id="app">{children}</div>
          {scripts}
        </body>
      </html>
    )}
  />
));
```

### Template File: `src/app.tsx`

```tsx
import { Router } from "@solidjs/router";
import { FileRoutes } from "@solidjs/start/router";
import { Suspense } from "solid-js";
import { Title } from "@solidjs/meta";
import "./app.css";

export default function App() {
  return (
    <Router root={(props) => (
      <>
        <Title>App</Title>
        <nav class="border-b border-gray-200 bg-white px-6 py-4">
          <div class="mx-auto flex max-w-6xl items-center justify-between">
            <a href="/" class="text-xl font-bold text-gray-900">App</a>
            <div class="flex gap-6">
              <a href="/" class="text-gray-600 hover:text-gray-900">Home</a>
            </div>
          </div>
        </nav>
        <main class="mx-auto max-w-6xl px-6 py-8">
          <Suspense
            fallback={
              <div class="flex items-center justify-center py-12">
                <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-blue-600" />
              </div>
            }
          >
            {props.children}
          </Suspense>
        </main>
        <footer class="border-t border-gray-200 bg-gray-50 px-6 py-6 text-center text-sm text-gray-500">
          &copy; {new Date().getFullYear()} App. All rights reserved.
        </footer>
      </>
    )}>
      <FileRoutes />
    </Router>
  );
}
```

### Template File: `src/app.css`

```css
@import "tailwindcss";

@theme {
  --color-primary-50: oklch(0.97 0.02 260);
  --color-primary-100: oklch(0.93 0.04 260);
  --color-primary-200: oklch(0.87 0.08 260);
  --color-primary-300: oklch(0.78 0.12 260);
  --color-primary-400: oklch(0.68 0.16 260);
  --color-primary-500: oklch(0.55 0.20 260);
  --color-primary-600: oklch(0.48 0.20 260);
  --color-primary-700: oklch(0.40 0.18 260);
  --color-primary-800: oklch(0.33 0.14 260);
  --color-primary-900: oklch(0.27 0.10 260);

  --font-sans: "Inter", ui-sans-serif, system-ui, sans-serif;
}

body {
  font-family: var(--font-sans);
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}
```

### Template File: `src/routes/index.tsx`

```tsx
import { Title } from "@solidjs/meta";
import { Icon } from "@iconify-icon/solid";

const features = [
  {
    icon: "lucide:zap",
    title: "Lightning Fast",
    description: "Built on SolidJS fine-grained reactivity for optimal performance.",
  },
  {
    icon: "lucide:shield-check",
    title: "Type Safe",
    description: "Full TypeScript strict mode with end-to-end type safety.",
  },
  {
    icon: "lucide:palette",
    title: "Modern Styling",
    description: "TailwindCSS 4 with CSS-first configuration and custom themes.",
  },
];

export default function Home() {
  return (
    <>
      <Title>Home - App</Title>
      <div class="py-12">
        <div class="mx-auto max-w-3xl text-center">
          <h1 class="text-4xl font-bold tracking-tight text-gray-900">
            Welcome to App
          </h1>
          <p class="mt-4 text-lg text-gray-600">
            A modern full-stack application built with SolidJS and Micronaut.
          </p>
        </div>
        <div class="mt-16 grid gap-8 sm:grid-cols-3">
          <For each={features}>
            {(feature) => (
              <div class="rounded-lg border border-gray-200 bg-white p-6 shadow-sm">
                <div class="mb-4 flex h-12 w-12 items-center justify-center rounded-lg bg-primary-50">
                  <Icon icon={feature.icon} class="text-2xl text-primary-600" />
                </div>
                <h3 class="text-lg font-semibold text-gray-900">
                  {feature.title}
                </h3>
                <p class="mt-2 text-sm text-gray-600">
                  {feature.description}
                </p>
              </div>
            )}
          </For>
        </div>
      </div>
    </>
  );
}
```

---

## Command: `/impl scaffold-backend`

Scaffolds a complete backend project from the template in `references/backend-scaffold/`.

### Instructions

1. **Determine target directory**: Ask the user for the project name or target directory. Default: `backend/` in the current workspace root.

2. **Determine base package**: Ask for the Java base package. Default: `com.example`.

3. **Copy template files**: Copy all files from `references/backend-scaffold/` to the target directory. Adjust the package structure to match the user's base package.

   ```
   backend/
   ├── build.gradle.kts
   ├── settings.gradle.kts
   ├── gradle.properties
   ├── micronaut-cli.yml
   ├── Dockerfile
   ├── .dockerignore
   ├── .gitignore
   ├── gradle/wrapper/
   │   └── gradle-wrapper.properties
   └── src/
       ├── main/java/com/example/
       │   ├── Application.java
       │   ├── controller/
       │   │   └── HealthController.java
       │   └── exception/
       │       └── GlobalExceptionHandler.java
       ├── main/resources/
       │   ├── application.yml
       │   └── logback.xml
       └── test/java/com/example/
           └── controller/
               └── HealthControllerTest.java
   ```

4. **Customize**: Replace `com.example` with the user's base package in all Java files, directory structure, and configuration.

5. **Build**: Run `./gradlew build` in the target directory.

6. **Verify**: Run `./gradlew test` to confirm the scaffold compiles and tests pass.

### Post-scaffold Verification Checklist

- [ ] `./gradlew build` completed without errors
- [ ] `./gradlew test` passes all tests
- [ ] `./gradlew run` starts the server on port 8080
- [ ] `/api/v1/health` returns `{"status":"UP"}` with HTTP 200
- [ ] `./gradlew shadowJar` produces a fat JAR in `build/libs/`

### Template File: `build.gradle.kts`

```kotlin
plugins {
    id("io.micronaut.application") version "4.5.2"
    id("io.micronaut.aot") version "4.5.2"
    id("com.gradleup.shadow") version "8.3.6"
}

version = "0.1.0"
group = "com.example"

repositories {
    mavenCentral()
}

dependencies {
    annotationProcessor("io.micronaut:micronaut-http-validation")
    annotationProcessor("io.micronaut.serde:micronaut-serde-processor")

    implementation("io.micronaut:micronaut-http-server-netty")
    implementation("io.micronaut.serde:micronaut-serde-jackson")
    implementation("io.micronaut.validation:micronaut-validation")
    implementation("jakarta.validation:jakarta.validation-api")
    implementation("ch.qos.logback:logback-classic")

    testImplementation("io.micronaut:micronaut-http-client")
    testImplementation("io.micronaut.test:micronaut-test-junit5")
    testImplementation("org.junit.jupiter:junit-jupiter-api")
    testRuntimeOnly("org.junit.jupiter:junit-jupiter-engine")
}

java {
    sourceCompatibility = JavaVersion.toVersion("21")
    targetCompatibility = JavaVersion.toVersion("21")
}

application {
    mainClass = "com.example.Application"
}

tasks.withType<JavaCompile> {
    options.encoding = "UTF-8"
    options.compilerArgs.addAll(listOf("--enable-preview"))
}

tasks.withType<JavaExec> {
    jvmArgs.addAll(listOf("--enable-preview"))
}

tasks.withType<Test> {
    jvmArgs.addAll(listOf("--enable-preview"))
    useJUnitPlatform()
}

micronaut {
    version = providers.gradleProperty("micronautVersion").get()
    runtime("netty")
    testRuntime("junit5")
    processing {
        incremental(true)
        annotations("com.example.*")
    }
    aot {
        optimizeServiceLoading = true
        convertYamlToJava = true
        precomputeOperations = true
        cacheEnvironment = true
        deduceEnvironment = true
    }
}
```

### Template File: `settings.gradle.kts`

```kotlin
rootProject.name = "backend"
```

### Template File: `gradle.properties`

```properties
micronautVersion=4.7.6
javaVersion=21
```

### Template File: `micronaut-cli.yml`

```yaml
profile: service
defaultPackage: com.example
testFramework: junit5
sourceLanguage: java
```

### Template File: `Dockerfile`

```dockerfile
FROM bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl AS build
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts gradle.properties ./
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon || true
COPY . .
RUN ./gradlew shadowJar --no-daemon

FROM bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl AS runtime
WORKDIR /app
COPY --from=build /app/build/libs/*-all.jar app.jar
EXPOSE 8080
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost:8080/api/v1/health || exit 1
ENTRYPOINT ["java", \
  "--enable-preview", \
  "-XX:+UseCompactObjectHeaders", \
  "-jar", "app.jar"]
```

### Template File: `.dockerignore`

```
build/
.gradle/
.idea/
*.iml
.git/
*.md
.env*
```

### Template File: `.gitignore`

```
.gradle/
build/
out/
.idea/
*.iml
*.class
.env
*.log
.DS_Store
```

### Template File: `gradle/wrapper/gradle-wrapper.properties`

```properties
distributionBase=GRADLE_USER_HOME
distributionPath=wrapper/dists
distributionUrl=https\://services.gradle.org/distributions/gradle-8.13-bin.zip
networkTimeout=10000
validateDistributionUrl=true
zipStoreBase=GRADLE_USER_HOME
zipStorePath=wrapper/dists
```

### Template File: `src/main/java/com/example/Application.java`

```java
package com.example;

import io.micronaut.runtime.Micronaut;

public class Application {
    public static void main(String[] args) {
        Micronaut.build(args)
            .banner(false)
            .start();
    }
}
```

### Template File: `src/main/java/com/example/controller/HealthController.java`

```java
package com.example.controller;

import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;
import io.micronaut.serde.annotation.Serdeable;

@Controller("/api/v1")
public class HealthController {

    @Get("/health")
    public HealthResponse health() {
        return new HealthResponse("UP");
    }

    @Serdeable
    public record HealthResponse(String status) {}
}
```

### Template File: `src/main/java/com/example/exception/GlobalExceptionHandler.java`

```java
package com.example.exception;

import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.server.exceptions.ExceptionHandler;
import io.micronaut.serde.annotation.Serdeable;
import jakarta.inject.Singleton;

@Singleton
@Produces
public class GlobalExceptionHandler implements ExceptionHandler<Exception, HttpResponse<ErrorResponse>> {

    @Override
    public HttpResponse<ErrorResponse> handle(HttpRequest request, Exception exception) {
        var status = determineStatus(exception);
        var error = new ErrorResponse(
            status.getCode(),
            status.getReason(),
            exception.getMessage(),
            request.getPath()
        );
        return HttpResponse.<ErrorResponse>status(status).body(error);
    }

    private io.micronaut.http.HttpStatus determineStatus(Exception exception) {
        return switch (exception) {
            case IllegalArgumentException e -> io.micronaut.http.HttpStatus.BAD_REQUEST;
            case jakarta.validation.ConstraintViolationException e -> io.micronaut.http.HttpStatus.BAD_REQUEST;
            default -> io.micronaut.http.HttpStatus.INTERNAL_SERVER_ERROR;
        };
    }

    @Serdeable
    public record ErrorResponse(
        int status,
        String title,
        String detail,
        String instance
    ) {}
}
```

### Template File: `src/main/resources/application.yml`

```yaml
micronaut:
  application:
    name: backend
  server:
    port: 8080
    cors:
      enabled: true
      configurations:
        all:
          allowedOrigins:
            - http://localhost:3000
          allowedMethods:
            - GET
            - POST
            - PUT
            - DELETE
            - PATCH
          allowedHeaders:
            - Content-Type
            - Authorization
          maxAge: 3600
  endpoints:
    health:
      enabled: true
      sensitive: false
  jackson:
    bean-introspection-module: true
    serialization-inclusion: non_null
    date-format: "yyyy-MM-dd'T'HH:mm:ss'Z'"
    time-zone: UTC

jackson:
  serialization:
    write-dates-as-timestamps: false

logger:
  levels:
    root: INFO
    io.micronaut: INFO
    com.example: DEBUG
```

### Template File: `src/main/resources/logback.xml`

```xml
<configuration>
    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} - %msg%n</pattern>
        </encoder>
    </appender>

    <logger name="io.micronaut" level="INFO"/>
    <logger name="com.example" level="DEBUG"/>

    <root level="INFO">
        <appender-ref ref="STDOUT"/>
    </root>
</configuration>
```

### Template File: `src/test/java/com/example/controller/HealthControllerTest.java`

```java
package com.example.controller;

import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpStatus;
import io.micronaut.http.client.HttpClient;
import io.micronaut.http.client.annotation.Client;
import io.micronaut.test.extensions.junit5.annotation.MicronautTest;
import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

@MicronautTest
class HealthControllerTest {

    @Test
    void testHealthEndpoint(@Client("/") HttpClient client) {
        var request = HttpRequest.GET("/api/v1/health");
        var response = client.toBlocking().exchange(request, HealthController.HealthResponse.class);

        assertEquals(HttpStatus.OK, response.getStatus());
        assertNotNull(response.body());
        assertEquals("UP", response.body().status());
    }
}
```

---

## Command: `/impl component`

Generates a SolidJS component with proper TypeScript types, following project conventions.

### Instructions

1. **Collect information**: Ask for the component name (PascalCase, e.g., `UserProfile`). Determine if it needs props, signals, or API integration.

2. **Determine location**: Place the component in `src/components/` directory. Create subdirectories for grouped components (e.g., `src/components/forms/`, `src/components/layout/`).

3. **Generate the component** following these conventions:
   - Named export (no default export)
   - Props defined as a typed interface
   - Signals for local state
   - Proper TypeScript types (no `any`)

### Component Template

```tsx
// src/components/{ComponentName}.tsx
import { type Component, createSignal, onCleanup } from "solid-js";
import { Icon } from "@iconify-icon/solid";

interface {ComponentName}Props {
  title: string;
  description?: string;
  onAction?: (id: string) => void;
}

const {ComponentName}: Component<{ComponentName}Props> = (props) => {
  const [isLoading, setIsLoading] = createSignal(false);

  return (
    <div class="rounded-lg border border-gray-200 bg-white p-6">
      <h3 class="text-lg font-semibold text-gray-900">{props.title}</h3>
      {props.description && (
        <p class="mt-2 text-sm text-gray-600">{props.description}</p>
      )}
    </div>
  );
};

export { {ComponentName} };
```

### Component with Data Fetching

```tsx
// src/components/UserList.tsx
import { type Component, createSignal, For, onMount, Show } from "solid-js";
import { Icon } from "@iconify-icon/solid";

interface User {
  id: string;
  name: string;
  email: string;
}

interface UserListProps {
  apiUrl?: string;
}

const UserList: Component<UserListProps> = (props) => {
  const [users, setUsers] = createSignal<User[]>([]);
  const [error, setError] = createSignal<string | null>(null);
  const [isLoading, setIsLoading] = createSignal(true);

  onMount(async () => {
    try {
      const response = await fetch(`${props.apiUrl ?? "/api/v1"}/users`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      const data: User[] = await response.json();
      setUsers(data);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to load users");
    } finally {
      setIsLoading(false);
    }
  });

  return (
    <div class="space-y-4">
      <Show when={isLoading()}>
        <div class="flex items-center justify-center py-8">
          <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-primary-600" />
        </div>
      </Show>

      <Show when={error()}>
        <div class="rounded-lg border border-red-200 bg-red-50 p-4">
          <p class="text-sm text-red-700">{error()}</p>
        </div>
      </Show>

      <For each={users()}>
        {(user) => (
          <div class="flex items-center gap-4 rounded-lg border border-gray-200 p-4">
            <div class="flex h-10 w-10 items-center justify-center rounded-full bg-primary-100">
              <Icon icon="lucide:user" class="text-primary-600" />
            </div>
            <div>
              <p class="font-medium text-gray-900">{user.name}</p>
              <p class="text-sm text-gray-500">{user.email}</p>
            </div>
          </div>
        )}
      </For>
    </div>
  );
};

export { UserList };
```

### Component with Context / Reactive Provider

```tsx
// src/components/ThemeProvider.tsx
import { type Component, createContext, useContext, createSignal, type JSX } from "solid-js";

interface Theme {
  mode: "light" | "dark";
}

interface ThemeContextValue {
  theme: () => Theme;
  toggle: () => void;
}

const ThemeContext = createContext<ThemeContextValue>();

function useTheme() {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme must be used within ThemeProvider");
  return ctx;
}

const ThemeProvider: Component<{ children: JSX.Element }> = (props) => {
  const [theme, setTheme] = createSignal<Theme>({ mode: "light" });

  const toggle = () => {
    setTheme((prev) => ({
      mode: prev.mode === "light" ? "dark" : "light",
    }));
  };

  const value: ThemeContextValue = { theme, toggle };

  return (
    <ThemeContext.Provider value={value}>
      {props.children}
    </ThemeContext.Provider>
  );
};

export { ThemeProvider, useTheme };
```

### Component File Organization

```
src/components/
├── layout/
│   ├── Header.tsx          # Named export
│   ├── Footer.tsx
│   └── Sidebar.tsx
├── forms/
│   ├── TextInput.tsx
│   ├── SelectInput.tsx
│   └── DatePicker.tsx
├── feedback/
│   ├── Spinner.tsx
│   ├── Toast.tsx
│   └── ErrorBoundary.tsx
├── data/
│   ├── DataTable.tsx
│   └── Pagination.tsx
└── index.ts                # Barrel re-exports
```

### Barrel Export Pattern (`src/components/index.ts`)

```typescript
export { Header } from "./layout/Header";
export { Footer } from "./layout/Footer";
export { Sidebar } from "./layout/Sidebar";
export { Spinner } from "./feedback/Spinner";
```

---

## Command: `/impl route`

Generates a SolidStart file-based route page.

### Instructions

1. **Collect information**: Ask for the route path (e.g., `/about`, `/users/[id]`, `/dashboard`).

2. **Determine file path**: Map the route path to a file under `src/routes/`:
   - `/` → `src/routes/index.tsx`
   - `/about` → `src/routes/about.tsx`
   - `/users/[id]` → `src/routes/users/[id].ts` (data) + `src/routes/users/[id].tsx` (page)
   - `/dashboard` → `src/routes/dashboard.tsx`
   - `/docs/[...slug]` → `src/routes/docs/[...slug].tsx` (catch-all)

3. **Generate the route** with proper meta tags, loading states, and layout integration.

### Simple Route Template

```tsx
// src/routes/about.tsx
import { Title, Meta } from "@solidjs/meta";

export default function AboutPage() {
  return (
    <>
      <Title>About - App</Title>
      <Meta name="description" content="Learn more about our application." />
      <div class="py-12">
        <h1 class="text-3xl font-bold text-gray-900">About</h1>
        <p class="mt-4 text-gray-600">
          This is the about page.
        </p>
      </div>
    </>
  );
}
```

### Dynamic Route with Data Loading

```tsx
// src/routes/users/[id].tsx
import { Title } from "@solidjs/meta";
import { useParams } from "@solidjs/router";
import { createResource, Show } from "solid-js";
import { Icon } from "@iconify-icon/solid";

interface User {
  id: string;
  name: string;
  email: string;
  role: string;
}

async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/v1/users/${id}`);
  if (!response.ok) throw new Error(`Failed to fetch user: ${response.status}`);
  return response.json();
}

export default function UserDetailPage() {
  const params = useParams<{ id: string }>();
  const [user] = createResource(() => params.id, fetchUser);

  return (
    <>
      <Title>{user()?.name ?? "User"} - App</Title>
      <div class="py-8">
        <Show
          when={user()}
          fallback={
            <div class="flex items-center justify-center py-12">
              <div class="h-8 w-8 animate-spin rounded-full border-4 border-gray-300 border-t-primary-600" />
            </div>
          }
        >
          {(userData) => (
            <div class="mx-auto max-w-2xl">
              <div class="rounded-lg border border-gray-200 bg-white p-6">
                <div class="flex items-center gap-4">
                  <div class="flex h-16 w-16 items-center justify-center rounded-full bg-primary-100">
                    <Icon icon="lucide:user" class="text-3xl text-primary-600" />
                  </div>
                  <div>
                    <h1 class="text-2xl font-bold text-gray-900">
                      {userData().name}
                    </h1>
                    <p class="text-gray-500">{userData().email}</p>
                  </div>
                </div>
                <div class="mt-6 border-t border-gray-100 pt-4">
                  <dl class="grid grid-cols-2 gap-4">
                    <div>
                      <dt class="text-sm font-medium text-gray-500">Role</dt>
                      <dd class="mt-1 text-sm text-gray-900">
                        {userData().role}
                      </dd>
                    </div>
                    <div>
                      <dt class="text-sm font-medium text-gray-500">ID</dt>
                      <dd class="mt-1 font-mono text-sm text-gray-900">
                        {userData().id}
                      </dd>
                    </div>
                  </dl>
                </div>
              </div>
            </div>
          )}
        </Show>
      </div>
    </>
  );
}
```

### Catch-All Route Template

```tsx
// src/routes/docs/[...slug].tsx
import { Title } from "@solidjs/meta";
import { useParams } from "@solidjs/router";
import { createMemo } from "solid-js";

export default function DocsPage() {
  const params = useParams<{ slug: string }>();
  const docPath = createMemo(() => params.slug ?? "index");

  return (
    <>
      <Title>Docs: {docPath()} - App</Title>
      <div class="grid grid-cols-[220px_1fr] gap-8 py-8">
        <nav class="space-y-1 text-sm">
          <a href="/docs/getting-started" class="block rounded px-3 py-2 text-gray-600 hover:bg-gray-100">
            Getting Started
          </a>
          <a href="/docs/api" class="block rounded px-3 py-2 text-gray-600 hover:bg-gray-100">
            API Reference
          </a>
        </nav>
        <article class="prose max-w-none">
          <h1>{docPath()}</h1>
          <p>Document content for {docPath()}.</p>
        </article>
      </div>
    </>
  );
}
```

### Route File Naming Reference

| URL | File Path | Type |
|-----|-----------|------|
| `/` | `src/routes/index.tsx` | Index |
| `/about` | `src/routes/about.tsx` | Static |
| `/users` | `src/routes/users.tsx` | Static |
| `/users/123` | `src/routes/users/[id].tsx` | Dynamic |
| `/docs/a/b/c` | `src/routes/docs/[...slug].tsx` | Catch-all |

---

## Command: `/impl controller`

Generates a Micronaut `@Controller` with full CRUD operations, validation, and `@Serdeable` DTOs.

### Instructions

1. **Collect information**: Ask for the entity name (e.g., `Person`, `Product`, `Order`), the API base path (default: `/api/v1/{entityLower}`), and the fields/attributes.

2. **Generate files**:
   - Controller class with CRUD endpoints
   - Request/Response DTOs as Java 21 records
   - Wire to the service layer (generate a service stub if it doesn't exist)

3. **Follow conventions**:
   - All responses wrapped in the controller
   - `@Validated` on input endpoints
   - `@Serdeable` on all DTOs
   - Proper HTTP status codes (201 Created, 204 No Content)
   - `@Status` annotations for response codes

### Controller Template

```java
// src/main/java/com/example/controller/PersonController.java
package com.example.controller;

import com.example.dto.CreatePersonRequest;
import com.example.dto.UpdatePersonRequest;
import com.example.dto.PersonResponse;
import com.example.service.PersonService;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.*;
import io.micronaut.http.uri.UriBuilder;
import io.micronaut.validation.Validated;
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotNull;
import java.util.List;
import java.util.UUID;

@Controller("/api/v1/persons")
@Validated
public class PersonController {

    private final PersonService personService;

    public PersonController(PersonService personService) {
        this.personService = personService;
    }

    @Get
    public HttpResponse<List<PersonResponse>> list() {
        return HttpResponse.ok(personService.findAll());
    }

    @Get("/{id}")
    public HttpResponse<PersonResponse> get(@NotNull UUID id) {
        return HttpResponse.ok(personService.findById(id));
    }

    @Post
    public HttpResponse<PersonResponse> create(@Body @Valid CreatePersonRequest request) {
        var person = personService.create(request);
        var location = UriBuilder.of("/api/v1/persons")
            .path(person.id().toString())
            .build();
        return HttpResponse.created(person, location);
    }

    @Put("/{id}")
    public HttpResponse<PersonResponse> update(
            @NotNull UUID id,
            @Body @Valid UpdatePersonRequest request) {
        return HttpResponse.ok(personService.update(id, request));
    }

    @Delete("/{id}")
    public HttpResponse<Void> delete(@NotNull UUID id) {
        personService.delete(id);
        return HttpResponse.noContent();
    }
}
```

### Controller with Query Parameters and Pagination

```java
// src/main/java/com/example/controller/PersonController.java (extended)
@Controller("/api/v1/persons")
@Validated
public class PersonController {

    private final PersonService personService;

    public PersonController(PersonService personService) {
        this.personService = personService;
    }

    @Get
    public HttpResponse<List<PersonResponse>> list(
            @QueryValue(defaultValue = "0") int page,
            @QueryValue(defaultValue = "20") int size,
            @QueryValue(defaultValue = "name") String sort,
            @QueryValue(defaultValue = "asc") String order,
            @QueryValue @Nullable String search) {
        return HttpResponse.ok(personService.findAll(page, size, sort, order, search));
    }
}
```

### Custom Exception Controller

```java
// src/main/java/com/example/exception/ResourceNotFoundException.java
package com.example.exception;

public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String resource, Object id) {
        super("%s not found with id: %s".formatted(resource, id));
    }
}

// src/main/java/com/example/exception/ResourceNotFoundExceptionHandler.java
package com.example.exception;

import io.micronaut.http.HttpRequest;
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Produces;
import io.micronaut.http.server.exceptions.ExceptionHandler;
import jakarta.inject.Singleton;

@Singleton
@Produces
public class ResourceNotFoundExceptionHandler
        implements ExceptionHandler<ResourceNotFoundException, HttpResponse<GlobalExceptionHandler.ErrorResponse>> {

    @Override
    public HttpResponse<GlobalExceptionHandler.ErrorResponse> handle(
            HttpRequest request,
            ResourceNotFoundException exception) {
        var error = new GlobalExceptionHandler.ErrorResponse(
            404,
            "Not Found",
            exception.getMessage(),
            request.getPath()
        );
        return HttpResponse.notFound(error);
    }
}
```

---

## Command: `/impl service`

Generates a Micronaut service class with constructor injection and business logic.

### Instructions

1. **Collect information**: Ask for the entity name (e.g., `Person`, `Product`). Determine if it needs repository integration, validation logic, or external API calls.

2. **Generate the service** with:
   - `@Singleton` annotation
   - Constructor injection (no field injection)
   - Proper exception handling (throw domain-specific exceptions)
   - Java 21 records for internal data transfer

### Service Template (Basic)

```java
// src/main/java/com/example/service/PersonService.java
package com.example.service;

import com.example.dto.CreatePersonRequest;
import com.example.dto.UpdatePersonRequest;
import com.example.dto.PersonResponse;
import com.example.exception.ResourceNotFoundException;
import com.example.repository.PersonRepository;
import jakarta.inject.Singleton;
import java.util.List;
import java.util.UUID;

@Singleton
public class PersonService {

    private final PersonRepository personRepository;

    public PersonService(PersonRepository personRepository) {
        this.personRepository = personRepository;
    }

    public List<PersonResponse> findAll() {
        return personRepository.findAll().stream()
            .map(this::toResponse)
            .toList();
    }

    public PersonResponse findById(UUID id) {
        return personRepository.findById(id)
            .map(this::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("Person", id));
    }

    public PersonResponse create(CreatePersonRequest request) {
        var entity = toEntity(request);
        var saved = personRepository.save(entity);
        return toResponse(saved);
    }

    public PersonResponse update(UUID id, UpdatePersonRequest request) {
        var existing = findById(id);
        var updated = mergeEntity(existing, request);
        var saved = personRepository.save(updated);
        return toResponse(saved);
    }

    public void delete(UUID id) {
        if (!personRepository.existsById(id)) {
            throw new ResourceNotFoundException("Person", id);
        }
        personRepository.deleteById(id);
    }

    private PersonResponse toResponse(/* entity */) {
        // Map entity to response DTO
    }

    private Object toEntity(CreatePersonRequest request) {
        // Map request DTO to entity
    }

    private Object mergeEntity(PersonResponse existing, UpdatePersonRequest request) {
        // Merge update into existing entity
    }
}
```

### Service with Business Logic

```java
// src/main/java/com/example/service/OrderService.java
package com.example.service;

import com.example.dto.CreateOrderRequest;
import com.example.dto.OrderResponse;
import com.example.exception.ResourceNotFoundException;
import com.example.exception.ValidationException;
import com.example.repository.OrderRepository;
import com.example.repository.ProductRepository;
import jakarta.inject.Singleton;
import java.math.BigDecimal;
import java.time.Instant;
import java.util.UUID;

@Singleton
public class OrderService {

    private final OrderRepository orderRepository;
    private final ProductRepository productRepository;

    public OrderService(
            OrderRepository orderRepository,
            ProductRepository productRepository) {
        this.orderRepository = orderRepository;
        this.productRepository = productRepository;
    }

    public OrderResponse createOrder(CreateOrderRequest request) {
        var product = productRepository.findById(request.productId())
            .orElseThrow(() -> new ResourceNotFoundException("Product", request.productId()));

        if (product.stock() < request.quantity()) {
            throw new ValidationException(
                "Insufficient stock. Available: %d, Requested: %d"
                    .formatted(product.stock(), request.quantity())
            );
        }

        var total = product.price().multiply(BigDecimal.valueOf(request.quantity()));
        // Create and save order
        // Return response
        return null;
    }
}
```

### Service Interface Pattern (for complex domains)

```java
// src/main/java/com/example/service/PersonService.java
package com.example.service;

import com.example.dto.CreatePersonRequest;
import com.example.dto.PersonResponse;
import java.util.List;
import java.util.UUID;

public interface PersonService {
    List<PersonResponse> findAll();
    PersonResponse findById(UUID id);
    PersonResponse create(CreatePersonRequest request);
    void delete(UUID id);
}

// src/main/java/com/example/service/DefaultPersonService.java
package com.example.service;

import com.example.dto.CreatePersonRequest;
import com.example.dto.PersonResponse;
import com.example.repository.PersonRepository;
import jakarta.inject.Singleton;
import java.util.List;
import java.util.UUID;

@Singleton
public class DefaultPersonService implements PersonService {

    private final PersonRepository personRepository;

    public DefaultPersonService(PersonRepository personRepository) {
        this.personRepository = personRepository;
    }

    @Override
    public List<PersonResponse> findAll() {
        return personRepository.findAll().stream()
            .map(this::toResponse)
            .toList();
    }

    @Override
    public PersonResponse findById(UUID id) {
        return personRepository.findById(id)
            .map(this::toResponse)
            .orElseThrow(() -> new ResourceNotFoundException("Person", id));
    }

    @Override
    public PersonResponse create(CreatePersonRequest request) {
        var entity = toEntity(request);
        var saved = personRepository.save(entity);
        return toResponse(saved);
    }

    @Override
    public void delete(UUID id) {
        personRepository.deleteById(id);
    }
}
```

---

## Command: `/impl repository`

Generates a Micronaut data repository for database access.

### Instructions

1. **Collect information**: Ask for the entity name, ID type (default: `UUID`), and any custom query methods needed.

2. **Generate the repository** interface extending the appropriate Micronaut Data base interface.

3. **Supported patterns**:
   - `CrudRepository` — basic CRUD
   - `PageableRepository` — CRUD + pagination
   - `JpaRepository` — full JPA with pagination

### Repository Template (Micronaut Data)

```java
// src/main/java/com/example/repository/PersonRepository.java
package com.example.repository;

import com.example.entity.Person;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.CrudRepository;
import java.util.List;
import java.util.Optional;
import java.util.UUID;

@JdbcRepository(dialect = Dialect.POSTGRES)
public interface PersonRepository extends CrudRepository<Person, UUID> {

    Optional<Person> findByEmail(String email);

    List<Person> findByNameContainingIgnoreCase(String name);

    List<Person> findByRole(String role);

    boolean existsByEmail(String email);

    @Query("SELECT * FROM persons WHERE created_at > :since ORDER BY created_at DESC")
    List<Person> findRecent(java.time.Instant since);

    long countByRole(String role);
}
```

### Entity Template

```java
// src/main/java/com/example/entity/Person.java
package com.example.entity;

import io.micronaut.data.annotation.*;
import java.time.Instant;
import java.util.UUID;

@MappedEntity("persons")
public record Person(
    @AutoPopulated @Id UUID id,
    String name,
    String email,
    String role,
    @DateCreated Instant createdAt,
    @DateUpdated Instant updatedAt
) {
    public Person {
        if (name == null || name.isBlank()) {
            throw new IllegalArgumentException("Name must not be blank");
        }
    }
}
```

### Repository with Pagination

```java
// src/main/java/com/example/repository/PersonRepository.java
package com.example.repository;

import com.example.entity.Person;
import io.micronaut.data.annotation.Query;
import io.micronaut.data.jdbc.annotation.JdbcRepository;
import io.micronaut.data.model.Page;
import io.micronaut.data.model.Pageable;
import io.micronaut.data.model.query.builder.sql.Dialect;
import io.micronaut.data.repository.PageableRepository;
import java.util.Optional;
import java.util.UUID;

@JdbcRepository(dialect = Dialect.POSTGRES)
public interface PersonRepository extends PageableRepository<Person, UUID> {

    Page<Person> findByNameContainingIgnoreCase(String name, Pageable pageable);

    Optional<Person> findByEmail(String email);

    @Query(
        value = "SELECT * FROM persons WHERE role = :role ORDER BY name",
        countQuery = "SELECT COUNT(*) FROM persons WHERE role = :role"
    )
    Page<Person> findByRole(String role, Pageable pageable);
}
```

---

## Command: `/impl dto`

Generates Java 21 record DTOs for request/response objects.

### Instructions

1. **Collect information**: Ask for the entity name and fields with their types. Determine which DTOs to generate:
   - `CreateRequest` — for POST bodies
   - `UpdateRequest` — for PUT bodies
   - `Response` — for API responses
   - `ListResponse` — for paginated lists

2. **Generate DTOs** using Java 21 records with:
   - `@Serdeable` for JSON serialization
   - `@Valid` / Jakarta validation annotations on request DTOs
   - Compact constructor for validation (where needed)
   - No Lombok — pure Java records

### DTO Templates

```java
// src/main/java/com/example/dto/CreatePersonRequest.java
package com.example.dto;

import io.micronaut.serde.annotation.Serdeable;
import jakarta.validation.constraints.*;
import java.time.LocalDate;

@Serdeable
public record CreatePersonRequest(
    @NotBlank(message = "Name is required")
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,

    @NotBlank(message = "Email is required")
    @Email(message = "Email must be valid")
    String email,

    @NotNull(message = "Birth date is required")
    @Past(message = "Birth date must be in the past")
    LocalDate birthDate,

    @Size(max = 500, message = "Bio must not exceed 500 characters")
    String bio
) {}

// src/main/java/com/example/dto/UpdatePersonRequest.java
package com.example.dto;

import io.micronaut.serde.annotation.Serdeable;
import jakarta.validation.constraints.*;
import java.time.LocalDate;

@Serdeable
public record UpdatePersonRequest(
    @Size(min = 2, max = 100, message = "Name must be between 2 and 100 characters")
    String name,

    @Email(message = "Email must be valid")
    String email,

    @Past(message = "Birth date must be in the past")
    LocalDate birthDate,

    @Size(max = 500, message = "Bio must not exceed 500 characters")
    String bio
) {}

// src/main/java/com/example/dto/PersonResponse.java
package com.example.dto;

import io.micronaut.serde.annotation.Serdeable;
import java.time.Instant;
import java.time.LocalDate;
import java.util.UUID;

@Serdeable
public record PersonResponse(
    UUID id,
    String name,
    String email,
    LocalDate birthDate,
    String bio,
    Instant createdAt,
    Instant updatedAt
) {}
```

### Paginated List Response DTO

```java
// src/main/java/com/example/dto/PaginatedResponse.java
package com.example.dto;

import io.micronaut.serde.annotation.Serdeable;
import java.util.List;

@Serdeable
public record PaginatedResponse<T>(
    List<T> items,
    int page,
    int size,
    long totalItems,
    int totalPages
) {
    public static <T> PaginatedResponse<T> of(List<T> items, int page, int size, long total) {
        return new PaginatedResponse<>(
            items,
            page,
            size,
            total,
            (int) Math.ceil((double) total / size)
        );
    }
}
```

### Sealed Interface for Result Types

```java
// src/main/java/com/example/dto/Result.java
package com.example.dto;

import io.micronaut.serde.annotation.Serdeable;

@Serdeable
public sealed interface Result<T> {

    @Serdeable
    record Success<T>(T data) implements Result<T> {}

    @Serdeable
    record Failure<T>(String error, int status) implements Result<T> {}

    static <T> Result<T> ok(T data) {
        return new Success<>(data);
    }

    static <T> Result<T> fail(String error, int status) {
        return new Failure<>(error, status);
    }
}
```

### Validation Annotations Reference

| Annotation | Use Case |
|---|---|
| `@NotNull` | Field must not be null |
| `@NotBlank` | String must not be null or blank |
| `@NotEmpty` | Collection/string must not be empty |
| `@Email` | Must be valid email format |
| `@Size(min, max)` | String/collection size bounds |
| `@Min`, `@Max` | Numeric bounds |
| `@Past`, `@Future` | Date temporal validation |
| `@Pattern(regexp)` | Regex pattern match |
| `@Positive`, `@PositiveOrZero` | Number must be > 0 or >= 0 |
| `@UUID` | Must be valid UUID string |

---

## Command: `/impl check`

Audits the codebase against project conventions and produces a report.

### Instructions

1. **Scan the project** for convention violations across both frontend and backend.

2. **Run automated checks**:
   - TypeScript strict mode enabled
   - No `any` types in TypeScript code
   - ESLint passes
   - Prettier formatting is consistent
   - TailwindCSS v4 patterns (`@import "tailwindcss"`, `@theme`)
   - Java 21 features used (records, sealed interfaces, pattern matching)
   - No Lombok annotations
   - Proper `@Serdeable` on DTOs
   - Constructor injection (no field injection)
   - Naming conventions followed
   - No `// TODO` or `// FIXME` comments left in code
   - No comments in code (policy: no-comments)
   - Import order follows conventions

3. **Generate a report** with:
   - Pass/Fail for each check
   - File paths and line numbers for violations
   - Suggested fixes

### Frontend Check Rules

| Rule | Description | Severity |
|---|---|---|
| `strict-typescript` | `strict: true` in tsconfig.json | Error |
| `no-any` | No `any` type usage in `.ts`/`.tsx` files | Error |
| `no-comments` | No `//` or `/* */` comments in source files | Warning |
| `named-exports` | Components use named exports (no default) | Error |
| `solid-signals` | Signals used correctly (no destructuring from props) | Error |
| `tailwind-v4` | CSS uses `@import "tailwindcss"` and `@theme` | Error |
| `no-inline-styles` | No `style={{ }}` in JSX; use TailwindCSS classes | Warning |
| `iconify-icons` | Icons use `@iconify-icon/solid` `<Icon>` component | Warning |
| `import-alias` | Uses `~/` path alias for local imports | Warning |
| `file-naming` | Components PascalCase, routes kebab-case | Error |

### Backend Check Rules

| Rule | Description | Severity |
|---|---|---|
| `java-21-records` | DTOs use `record` keyword, not classes with Lombok | Error |
| `serdeable-dtos` | All DTOs have `@Serdeable` annotation | Error |
| `constructor-injection` | Services/controllers use constructor injection | Error |
| `no-lombok` | No Lombok annotations (`@Data`, `@Getter`, etc.) | Error |
| `no-comments` | No `//` or `/* */` comments in Java source | Warning |
| `pattern-matching` | Switch uses arrow syntax and pattern matching | Warning |
| `proper-exceptions` | Domain-specific exceptions, not generic `RuntimeException` | Error |
| `validated-endpoints` | Input endpoints use `@Valid` and `@Validated` | Error |
| `http-status-codes` | Correct status codes (201 Created, 204 No Content) | Warning |
| `naming-conventions` | Packages lowercase, classes PascalCase, constants UPPER_SNAKE | Error |
| `api-versioning` | Controllers use `/api/v1/` prefix | Error |

### Check Execution Script

```bash
# Frontend checks
echo "=== Frontend Convention Check ==="
echo "[1/10] TypeScript strict mode..."
grep '"strict": true' frontend/tsconfig.json || echo "FAIL: strict mode not enabled"

echo "[2/10] No 'any' types..."
rg '\bany\b' frontend/src/ --type ts --type tsx -n || echo "PASS: no any types"

echo "[3/10] Named exports (components)..."
rg 'export default' frontend/src/components/ -n || echo "PASS: no default exports in components"

echo "[4/10] TailwindCSS v4 patterns..."
grep '@import "tailwindcss"' frontend/src/app.css || echo "FAIL: missing @import tailwindcss"
grep '@theme' frontend/src/app.css || echo "FAIL: missing @theme block"

echo "[5/10] ESLint..."
cd frontend && bun run lint 2>&1 || echo "FAIL: ESLint errors found"
cd ..

echo ""
echo "=== Backend Convention Check ==="
echo "[1/11] Java 21 records for DTOs..."
rg 'public record' backend/src/ -n || echo "FAIL: no records found"

echo "[2/11] No Lombok..."
rg '@Data|@Getter|@Setter|@Builder|@AllArgsConstructor' backend/src/ -n || echo "PASS: no Lombok"

echo "[3/11] @Serdeable on DTOs..."
rg 'public record.*\{' backend/src/ -l | while read f; do
  grep '@Serdeable' "$f" > /dev/null || echo "FAIL: missing @Serdeable in $f"
done

echo "[4/11] Constructor injection..."
rg '@Inject|@Autowired' backend/src/ -n || echo "PASS: no field injection annotations"

echo "[5/11] API versioning..."
rg '@Controller\("/api/v1' backend/src/ -n || echo "FAIL: missing /api/v1 prefix"

echo "[6/11] Build..."
cd backend && ./gradlew build --no-daemon 2>&1 | tail -5
cd ..
```

---

## Reference Files

The following reference files are available in `skills/implementation/references/`:

| File | Description |
|---|---|
| `references/frontend-scaffold/` | Complete frontend project template with all files listed above |
| `references/backend-scaffold/` | Complete backend project template with all files listed above |
| `references/frontend-conventions.md` | SolidJS reactivity rules, TypeScript strict, TailwindCSS v4 patterns |
| `references/backend-conventions.md` | Micronaut patterns, Java 21 features, error handling, DI patterns |
| `references/code-standards.md` | Naming conventions, import order, file organization, no-comments policy |

### references/frontend-conventions.md

```markdown
# Frontend Conventions

## SolidJS Reactivity Rules

1. **Signals are the primitive**: Use `createSignal` for local component state.
2. **Never destructure props**: Access props with `props.x` — destructuring breaks reactivity.
3. **Use `createMemo` for derived state**: Don't compute values in the render body.
4. **Use `createEffect` for side effects**: Not for data fetching — use `createResource`.
5. **`createResource` for async data**: Combine with route data for SSR/SSG.
6. **Fine-grained updates**: SolidJS updates only what changes — don't fight it with immutable patterns.

## TypeScript Standards

- `strict: true` always enabled
- No `any` types — use `unknown` and type narrowing
- Interfaces for props, type aliases for unions/intersections
- Generic types for reusable components
- Explicit return types on exported functions

## TailwindCSS v4 Patterns

- Use `@import "tailwindcss"` (not `@tailwind` directives)
- Use `@theme { }` for custom design tokens (colors, fonts, spacing)
- Use oklch color space for custom colors
- No `tailwind.config.js` — configuration is CSS-first
- Use `@apply` sparingly — prefer utility classes in markup
- Use `@variant` for custom variants if needed

## Component Structure

```tsx
// Imports: solid-js → @solidjs/* → @iconify-icon/* → local
import { type Component, createSignal, For, Show } from "solid-js";
import { Title } from "@solidjs/meta";
import { Icon } from "@iconify-icon/solid";
import { useCustomContext } from "~/context";

// Types
interface ComponentProps {
  // ...
}

// Component
const ComponentName: Component<ComponentProps> = (props) => {
  // 1. Signals
  // 2. Memos
  // 3. Effects / Resources
  // 4. Event handlers
  // 5. JSX return
  return (
    // ...
  );
};

// Named export only
export { ComponentName };
```

## Import Order

1. SolidJS core (`solid-js`)
2. SolidStart / Solid Router / Solid Meta (`@solidjs/*`)
3. Iconify (`@iconify-icon/solid`)
4. Local modules (`~/components/*`, `~/lib/*`, `~/types/*`)
5. CSS imports last
```

### references/backend-conventions.md

```markdown
# Backend Conventions

## Micronaut Patterns

1. **Compile-time DI**: Micronaut uses annotation processing — no runtime reflection.
2. **Constructor injection**: Always use constructor injection. Never use `@Inject` on fields.
3. **`@Singleton` by default**: Services are singletons unless scoped otherwise.
4. **`@Serdeable` on DTOs**: Required for compile-time JSON serialization.
5. **`@Validated` on controllers**: Enables method-level validation.
6. **`@Valid` on `@Body` params**: Triggers Jakarta Bean Validation.

## Java 21 Feature Requirements

### Records (Required for DTOs)
```java
@Serdeable
public record PersonResponse(UUID id, String name, String email) {}
```
No Lombok. No mutable DTOs. Records only.

### Sealed Interfaces (For Domain Modeling)
```java
public sealed interface PaymentResult {
    record Success(String transactionId, BigDecimal amount) implements PaymentResult {}
    record Failed(String errorCode, String message) implements PaymentResult {}
    record Pending(String transactionId, Instant estimatedCompletion) implements PaymentResult {}
}
```

### Pattern Matching (For Switch)
```java
return switch (status) {
    case 200 -> "OK";
    case 404 -> "Not Found";
    case 500 -> "Server Error";
    default -> "Unknown";
};
```

### Virtual Threads (Enabled via JVM flags)
```
--enable-preview
-XX:+UseCompactObjectHeaders
```

## Error Handling

### Exception Hierarchy
```
RuntimeException
├── ResourceNotFoundException    → 404
├── ValidationException          → 400
├── ConflictException            → 409
└── Exception                    → 500 (GlobalExceptionHandler)
```

### Exception Handler Pattern
```java
@Singleton
@Produces
public class CustomExceptionHandler implements ExceptionHandler<CustomException, HttpResponse<ErrorResponse>> {
    @Override
    public HttpResponse<ErrorResponse> handle(HttpRequest request, CustomException exception) {
        var error = new ErrorResponse(400, "Bad Request", exception.getMessage(), request.getPath());
        return HttpResponse.badRequest(error);
    }
}
```

## Dependency Injection

```java
// Correct: Constructor injection
@Singleton
public class PersonService {
    private final PersonRepository personRepository;
    private final EmailService emailService;

    public PersonService(PersonRepository personRepository, EmailService emailService) {
        this.personRepository = personRepository;
        this.emailService = emailService;
    }
}

// Wrong: Field injection — DO NOT USE
@Singleton
public class PersonService {
    @Inject
    private PersonRepository personRepository;
}
```

## API Response Format

### Error Response (RFC 7807 inspired)
```json
{
  "status": 404,
  "title": "Not Found",
  "detail": "Person not found with id: 550e8400-e29b-41d4-a716-446655440000",
  "instance": "/api/v1/persons/550e8400-e29b-41d4-a716-446655440000"
}
```

### Success Response
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "John Doe",
  "email": "john@example.com",
  "createdAt": "2025-01-15T10:30:00Z",
  "updatedAt": "2025-01-15T10:30:00Z"
}
```
```

### references/code-standards.md

```markdown
# Code Standards

## General

### No Comments Policy
Code should be self-documenting through clear naming and structure. Comments are NOT allowed unless:
- They are JSDoc/Javadoc for public API documentation
- They explain WHY (not WHAT) for non-obvious business logic decisions

### File Organization

**Frontend:**
```
src/
├── components/          # Reusable UI components
│   ├── layout/          # Header, Footer, Sidebar
│   ├── forms/           # Input, Select, DatePicker
│   ├── feedback/        # Spinner, Toast, ErrorBoundary
│   └── data/            # DataTable, Pagination
├── routes/              # File-based routing (SolidStart)
├── lib/                 # Utilities, helpers, constants
├── types/               # Shared TypeScript types/interfaces
├── context/             # SolidJS context providers
└── hooks/               # Custom reactive hooks (if used)
```

**Backend:**
```
src/main/java/com/example/
├── controller/          # HTTP endpoint handlers
├── service/             # Business logic layer
├── repository/          # Data access layer
├── entity/              # Database entities/records
├── dto/                 # Data Transfer Objects (request/response)
├── exception/           # Custom exceptions + handlers
├── config/              # Configuration classes
└── util/                # Utility classes
```

## Naming Conventions

### Frontend (TypeScript/SolidJS)

| Element | Convention | Example |
|---|---|---|
| Components | PascalCase | `UserProfile.tsx` |
| Props interfaces | PascalCase + Props | `UserProfileProps` |
| Hooks | camelCase with use prefix | `useAuth()` |
| Signals | camelCase with get/set | `[count, setCount]` |
| Event handlers | on + Event | `onClick`, `handleSubmit` |
| CSS classes | TailwindCSS utilities | `class="flex items-center"` |
| Files (components) | PascalCase | `UserProfile.tsx` |
| Files (routes) | kebab-case | `user-profile.tsx` |
| Files (utilities) | camelCase | `formatDate.ts` |
| Directories | kebab-case | `components/data-table/` |

### Backend (Java/Micronaut)

| Element | Convention | Example |
|---|---|---|
| Classes | PascalCase | `PersonService` |
| Interfaces | PascalCase | `PersonRepository` |
| Records | PascalCase | `PersonResponse` |
| Methods | camelCase | `findAll()`, `createOrder()` |
| Constants | UPPER_SNAKE | `MAX_RETRY_ATTEMPTS` |
| Packages | lowercase | `com.example.controller` |
| Fields | camelCase | `personRepository` |
| Files | Matches class name | `PersonService.java` |
| Directories | Matches package | `controller/`, `service/` |

## Import Order

### Frontend (TypeScript)

```typescript
// 1. SolidJS core
import { type Component, createSignal, For, Show } from "solid-js";

// 2. SolidStart / Solid ecosystem
import { Title, Meta } from "@solidjs/meta";
import { useParams } from "@solidjs/router";

// 3. Iconify
import { Icon } from "@iconify-icon/solid";

// 4. Local modules (use ~/ alias)
import { formatDate } from "~/lib/format";
import { type User } from "~/types/user";
import { UserCard } from "~/components/UserCard";

// 5. CSS imports (last)
import "./styles.css";
```

### Backend (Java)

```java
// 1. Package declaration
package com.example.controller;

// 2. Java standard library
import java.time.Instant;
import java.util.List;
import java.util.UUID;

// 3. Jakarta
import jakarta.validation.Valid;
import jakarta.validation.constraints.NotBlank;

// 4. Micronaut
import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.*;
import io.micronaut.serde.annotation.Serdeable;

// 5. Project imports
import com.example.dto.PersonResponse;
import com.example.service.PersonService;
```

## File Templates

### Frontend Component Minimum
```tsx
import { type Component } from "solid-js";

interface ComponentNameProps {}

const ComponentName: Component<ComponentNameProps> = (props) => {
  return <div></div>;
};

export { ComponentName };
```

### Backend Controller Minimum
```java
package com.example.controller;

import io.micronaut.http.HttpResponse;
import io.micronaut.http.annotation.Controller;
import io.micronaut.http.annotation.Get;

@Controller("/api/v1/resources")
public class ResourceController {

    @Get
    public HttpResponse<Void> list() {
        return HttpResponse.ok();
    }
}
```
```

---

## Workflow Integration

### Typical Implementation Session

```
1. /impl scaffold-frontend     → Create frontend project
2. /impl scaffold-backend      → Create backend project
3. /impl dto Person            → Generate DTOs for Person entity
4. /impl repository Person     → Generate PersonRepository
5. /impl service Person        → Generate PersonService
6. /impl controller Person     → Generate PersonController with CRUD
7. /impl component PersonList  → Generate SolidJS PersonList component
8. /impl route /persons        → Generate /persons route page
9. /impl check                 → Audit all code against conventions
```

### Dependency Order for Backend Code Generation

When generating backend code for a new entity, follow this order:

1. **DTOs** (`/impl dto`) — Request/response records
2. **Entity** — Database-mapped record
3. **Repository** (`/impl repository`) — Data access interface
4. **Service** (`/impl service`) — Business logic layer
5. **Controller** (`/impl controller`) — HTTP endpoint handler
6. **Exception Handler** — If custom error handling is needed
7. **Tests** — Unit tests for each layer

### File Generation Checklist

For each generated file:
- [ ] Follows naming conventions
- [ ] Uses correct import order
- [ ] No comments in code
- [ ] Proper TypeScript strict types / Java 21 features
- [ ] `@Serdeable` on all DTOs
- [ ] Constructor injection on all services/controllers
- [ ] Named exports (frontend) / proper package (backend)
- [ ] File is in the correct directory
