---
name: "build-release"
tags: [ci-cd, docker, podman, build, release, deploy, container, nginx, liberica]
description: |
  Build & Release skill for the "Build & Release" phase of the SDLC.
  Provides containerization, CI/CD pipeline generation, version management,
  release automation, and deployment strategies for the full-stack architecture:

  - **Frontend**: SolidJS SSG → Bun build → nginx:stable-alpine container
  - **Backend**: Micronaut → Shadow JAR → Liberica CRaC container

  Trigger phrases:
    - "build container"
    - "create dockerfile"
    - "set up CI/CD"
    - "deploy"
    - "release version"
    - "build pipeline"
    - "containerize"
---

# Build & Release

This is the **build and release skill** for the agentden SDLC framework. It handles containerization, CI/CD pipelines, version management, and deployment for the full-stack architecture:

- **Frontend**: Bun + SolidJS SSG → nginx:stable-alpine (static hosting)
- **Backend**: Micronaut + Gradle → Shadow JAR → Liberica CRaC runtime

## Commands

| Command | Description |
|---|---|
| `/build frontend` | Build and containerize frontend (SolidJS SSG → nginx) |
| `/build backend` | Build and containerize backend (Micronaut → Liberica CRaC) |
| `/build pipeline` | Generate CI/CD pipeline configuration |
| `/build release` | Create release with changelog |
| `/build deploy` | Deploy to staging/production |
| `/build rollback` | Rollback to previous version |

---

## Command: `/build frontend`

Builds the frontend application and produces an optimized nginx container image.

### Prerequisites

- Bun 1.2+ installed (or run inside the build container)
- `package.json` and `bun.lockb` present
- SolidStart configured with `preset: "static"`

### Build Steps

1. **Verify project structure**: Confirm `app.config.ts` has `preset: "static"`.
2. **Install dependencies**: `bun install --frozen-lockfile`
3. **Build**: `bun run build` — produces static output in `.output/public/`
4. **Build container image**: Use the Dockerfile below
5. **Verify**: Run the container and check `http://localhost:8080/health` returns `ok`

### Frontend Dockerfile

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
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

### nginx.conf

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
    gzip_vary on;

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
        add_header Cache-Control "no-cache, no-store, must-revalidate" always;
        add_header Pragma "no-cache" always;
        add_header Expires "0" always;
        try_files $uri $uri/ /index.html;
    }

    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;
}
```

### Frontend .dockerignore

```
node_modules/
.output/
dist/
.git/
*.md
.env*
.vscode/
coverage/
```

### Build & Run Commands

```bash
# Build the container image
docker build -t frontend:latest .

# Run locally
docker run --rm -p 8080:80 frontend:latest

# Verify health
curl -sf http://localhost:8080/health

# Verify security headers
curl -sI http://localhost:8080 | grep -E "X-Frame|X-Content|Referrer"
```

### Build with Podman

```bash
podman build -t frontend:latest .
podman run --rm -p 8080:80 frontend:latest
```

### Multi-stage Build Arguments

```dockerfile
FROM oven/bun:1 AS build
ARG NODE_ENV=production
ENV NODE_ENV=${NODE_ENV}
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile
COPY . .
RUN bun run build

FROM nginx:stable-alpine AS runtime
ARG VERSION=dev
LABEL org.opencontainers.image.version="${VERSION}"
COPY --from=build /app/.output/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
HEALTHCHECK --interval=30s --timeout=3s --retries=3 \
  CMD wget -qO- http://localhost/health || exit 1
CMD ["nginx", "-g", "daemon off;"]
```

```bash
docker build --build-arg VERSION=v1.2.3 -t frontend:v1.2.3 .
```

---

## Command: `/build backend`

Builds the backend application and produces an optimized Liberica CRaC container image.

### Prerequisites

- Java 21 JDK installed (or run inside the build container)
- Gradle wrapper present (`gradlew`)
- `build.gradle.kts` configured with `com.gradleup.shadow` plugin

### Build Steps

1. **Verify project structure**: Confirm `build.gradle.kts` has the shadow plugin and Micronaut AOT configured.
2. **Resolve dependencies**: `./gradlew dependencies --no-daemon`
3. **Build fat JAR**: `./gradlew shadowJar --no-daemon` — produces `build/libs/*-all.jar`
4. **Build container image**: Use the Dockerfile below
5. **Verify**: Run the container and check `http://localhost:8080/api/v1/health` returns `{"status":"UP"}`

### Backend Dockerfile

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

### Backend .dockerignore

```
build/
.gradle/
.idea/
*.iml
.git/
*.md
.env*
```

### Build & Run Commands

```bash
# Build the container image
docker build -t backend:latest .

# Run locally
docker run --rm -p 8080:8080 backend:latest

# Verify health
curl -sf http://localhost:8080/api/v1/health
```

### JVM Flags Explained

| Flag | Purpose |
|------|---------|
| `--enable-preview` | Enables Java 21 preview features (virtual threads, pattern matching) |
| `-XX:+UseCompactObjectHeaders` | Reduces memory overhead with smaller object headers (Liberica-specific) |

### Multi-stage Build with Version

```dockerfile
FROM bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl AS build
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts gradle.properties ./
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon || true
COPY . .
ARG VERSION=0.0.0
RUN ./gradlew shadowJar --no-daemon -Pversion=${VERSION}

FROM bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl AS runtime
ARG VERSION=dev
LABEL org.opencontainers.image.version="${VERSION}"
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

```bash
docker build --build-arg VERSION=1.2.3 -t backend:v1.2.3 .
```

---

## Command: `/build pipeline`

Generates CI/CD pipeline configuration files for GitHub Actions.

### Prerequisites

- GitHub repository configured
- Container registry accessible (Docker Hub, GitHub Container Registry, or private)
- Secrets configured in repository settings

### Required GitHub Secrets

```
Secrets to configure:
├── DOCKER_REGISTRY       # e.g., ghcr.io
├── DOCKER_USERNAME       # registry username
├── DOCKER_PASSWORD       # registry password/token
├── DEPLOY_HOST_STAGING   # staging server hostname
├── DEPLOY_HOST_PROD      # production server hostname
├── DEPLOY_SSH_KEY        # SSH private key for deployment
└── DEPLOY_USER           # SSH user for deployment
```

### Frontend CI/CD Pipeline

`.github/workflows/frontend.yml`:

```yaml
name: Frontend CI/CD

on:
  push:
    branches: [main]
    paths:
      - "frontend/**"
  pull_request:
    branches: [main]
    paths:
      - "frontend/**"

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/frontend

jobs:
  lint-and-test:
    name: Lint & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4

      - uses: oven-sh/setup-bun@v2
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Lint
        run: bun run lint

      - name: Type check
        run: bun run typecheck

      - name: Format check
        run: bun run format:check

      - name: Test
        run: bun test

  build-and-push:
    name: Build & Push Image
    needs: lint-and-test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    defaults:
      run:
        working-directory: frontend
    steps:
      - uses: actions/checkout@v4

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: ./frontend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST_STAGING }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            docker stop frontend || true
            docker rm frontend || true
            docker run -d \
              --name frontend \
              --restart unless-stopped \
              -p 80:80 \
              ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

### Backend CI/CD Pipeline

`.github/workflows/backend.yml`:

```yaml
name: Backend CI/CD

on:
  push:
    branches: [main]
    paths:
      - "backend/**"
  pull_request:
    branches: [main]
    paths:
      - "backend/**"

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/backend

jobs:
  lint-and-test:
    name: Lint & Test
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4

      - name: Set up JDK 21
        uses: actions/setup-java@v4
        with:
          java-version: "21"
          distribution: "liberica"

      - name: Setup Gradle
        uses: gradle/actions/setup-gradle@v4

      - name: Grant execute permission
        run: chmod +x gradlew

      - name: Lint
        run: ./gradlew checkstyleMain --no-daemon

      - name: Test
        run: ./gradlew test --no-daemon

      - name: Upload test results
        if: always()
        uses: actions/upload-artifact@v4
        with:
          name: test-results
          path: backend/build/reports/tests/

  build-and-push:
    name: Build & Push Image
    needs: lint-and-test
    if: github.event_name == 'push' && github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    defaults:
      run:
        working-directory: backend
    steps:
      - uses: actions/checkout@v4

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Extract metadata
        id: meta
        uses: docker/metadata-action@v5
        with:
          images: ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}
          tags: |
            type=sha,prefix=
            type=raw,value=latest,enable={{is_default_branch}}
            type=semver,pattern={{version}}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: ./backend
          push: true
          tags: ${{ steps.meta.outputs.tags }}
          labels: ${{ steps.meta.outputs.labels }}
          build-args: |
            VERSION=${{ github.ref_name }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  deploy-staging:
    name: Deploy to Staging
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: staging
    steps:
      - name: Deploy via SSH
        uses: appleboy/ssh-action@v1
        with:
          host: ${{ secrets.DEPLOY_HOST_STAGING }}
          username: ${{ secrets.DEPLOY_USER }}
          key: ${{ secrets.DEPLOY_SSH_KEY }}
          script: |
            docker pull ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            docker stop backend || true
            docker rm backend || true
            docker run -d \
              --name backend \
              --restart unless-stopped \
              -p 8080:8080 \
              ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
```

### Release Pipeline

`.github/workflows/release.yml`:

```yaml
name: Release

on:
  push:
    tags:
      - "v*.*.*"

permissions:
  contents: write
  packages: write

jobs:
  create-release:
    name: Create Release
    runs-on: ubuntu-latest
    outputs:
      version: ${{ steps.version.outputs.version }}
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: Extract version
        id: version
        run: echo "version=${GITHUB_REF#refs/tags/v}" >> $GITHUB_OUTPUT

      - name: Generate changelog
        id: changelog
        run: |
          PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")
          if [ -z "$PREVIOUS_TAG" ]; then
            COMMITS=$(git log --pretty=format:"- %s (%h)" HEAD)
          else
            COMMITS=$(git log --pretty=format:"- %s (%h)" ${PREVIOUS_TAG}..HEAD)
          fi

          {
            echo "## What's Changed"
            echo ""
            echo "$COMMITS" | grep -E "^- (feat|add)" | sed 's/^- feat/- 🚀 feat/' | sed 's/^- add/- 🚀 add/' || true
            echo ""
            echo "### Fixes"
            echo "$COMMITS" | grep -E "^- fix" | sed 's/^- fix/- 🐛 fix/' || true
            echo ""
            echo "### Other Changes"
            echo "$COMMITS" | grep -vE "^- (feat|add|fix)" || true
          } > CHANGELOG.md

      - name: Create GitHub Release
        uses: softprops/action-gh-release@v2
        with:
          body_path: CHANGELOG.md
          draft: false
          prerelease: ${{ contains(steps.version.outputs.version, '-rc') || contains(steps.version.outputs.version, '-beta') }}

  build-frontend:
    name: Build Frontend Image
    needs: create-release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: ./frontend
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/frontend:${{ needs.create-release.outputs.version }}
            ghcr.io/${{ github.repository }}/frontend:latest
          build-args: |
            VERSION=${{ needs.create-release.outputs.version }}

  build-backend:
    name: Build Backend Image
    needs: create-release
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v6
        with:
          context: ./backend
          push: true
          tags: |
            ghcr.io/${{ github.repository }}/backend:${{ needs.create-release.outputs.version }}
            ghcr.io/${{ github.repository }}/backend:latest
          build-args: |
            VERSION=${{ needs.create-release.outputs.version }}
```

---

## Command: `/build release`

Creates a new version release with an auto-generated changelog.

### Version Management (SemVer)

This project follows [Semantic Versioning 2.0.0](https://semver.org/):

```
MAJOR.MINOR.PATCH[-PRERELEASE]

Examples:
  1.0.0       → first stable release
  1.1.0       → new feature (backward compatible)
  1.1.1       → bug fix (backward compatible)
  2.0.0       → breaking change
  2.0.0-rc.1  → release candidate
```

### Conventional Commits

All commits **must** follow the [Conventional Commits](https://www.conventionalcommits.org/) specification:

```
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
```

**Types:**

| Type | Description | SemVer Impact |
|------|-------------|---------------|
| `feat` | New feature | MINOR (or MAJOR with `!`) |
| `fix` | Bug fix | PATCH |
| `docs` | Documentation only | None |
| `style` | Formatting, whitespace | None |
| `refactor` | Code restructuring | None |
| `perf` | Performance improvement | PATCH |
| `test` | Adding/updating tests | None |
| `ci` | CI/CD changes | None |
| `chore` | Build, tooling, deps | None |
| `revert` | Revert a commit | Varies |

**Breaking changes:** Use `!` after type/scope or add `BREAKING CHANGE:` in footer.

```
feat(api)!: change authentication flow
feat(ui): add dark mode toggle
fix(api): resolve null pointer in user service
docs: update API documentation
ci: add frontend build pipeline
```

### Release Process

1. **Verify clean state**: Ensure all changes are committed and tests pass.
2. **Determine version**: Analyze commits since last tag using conventional commit rules.
3. **Update version**:
   - Frontend: Update `version` in `package.json`
   - Backend: Update `version` in `build.gradle.kts`
4. **Generate changelog**: Collect conventional commits into categorized changelog.
5. **Create git tag**: `git tag -a v{VERSION} -m "Release v{VERSION}"`
6. **Push tag**: `git push origin v{VERSION}` — triggers the release pipeline.

### Version Bump Commands

```bash
# Determine current version
git describe --tags --abbrev=0

# Patch release (bug fixes)
npm version patch -m "chore(release): v%s"        # frontend
# or manually update build.gradle.kts version       # backend

# Minor release (new features)
npm version minor -m "chore(release): v%s"

# Major release (breaking changes)
npm version major -m "chore(release): v%s"

# Push tag to trigger release
git push --follow-tags
```

### Changelog Template

```markdown
# Changelog

## [VERSION] - DATE

### Features
- scope: description (#pr) @contributor
- scope: description (#pr) @contributor

### Bug Fixes
- scope: description (#pr) @contributor
- scope: description (#pr) @contributor

### Performance
- scope: description (#pr) @contributor

### Breaking Changes
- **scope**: description and migration guide

### Dependencies
- Updated dependency-name from X.Y.Z to A.B.C

### CI/CD
- description of pipeline changes
```

### Auto-generate Changelog from Commits

```bash
#!/bin/bash
# generate-changelog.sh
# Usage: ./generate-changelog.sh v1.2.3

VERSION=$1
PREVIOUS_TAG=$(git describe --tags --abbrev=0 HEAD^ 2>/dev/null || echo "")

if [ -z "$PREVIOUS_TAG" ]; then
  RANGE="HEAD"
else
  RANGE="${PREVIOUS_TAG}..HEAD"
fi

echo "# Changelog"
echo ""
echo "## [${VERSION#v}] - $(date +%Y-%m-%d)"
echo ""

echo "### Features"
git log --pretty=format:"- %s" $RANGE | grep "^- feat" | \
  sed 's/^- feat(\(.*\)): /- **\1** /' | \
  sed 's/^- feat: /- /' || true
echo ""

echo "### Bug Fixes"
git log --pretty=format:"- %s" $RANGE | grep "^- fix" | \
  sed 's/^- fix(\(.*\)): /- **\1** /' | \
  sed 's/^- fix: /- /' || true
echo ""

echo "### Other Changes"
git log --pretty=format:"- %s" $RANGE | \
  grep -vE "^- (feat|fix)" | \
  grep -v "^- chore(release)" || true
echo ""
```

---

## Command: `/build deploy`

Deploys container images to staging or production environments.

### Deployment Environments

| Environment | Purpose | URL Pattern | Auto-deploy |
|-------------|---------|-------------|-------------|
| Staging | Pre-production validation | `staging.example.com` | On push to `main` |
| Production | Live traffic | `example.com` | On tag `v*` |

### Deployment Strategy: Blue-Green

Blue-green deployment maintains two identical environments. Traffic is switched atomically between them.

```bash
#!/bin/bash
# deploy-blue-green.sh
# Usage: ./deploy-blue-green.sh frontend v1.2.3 staging

SERVICE=$1
VERSION=$2
ENVIRONMENT=$3
REGISTRY="ghcr.io/org/project"
CURRENT=$(docker inspect --format='{{.Config.Labels.slot}}' ${SERVICE}-${ENVIRONMENT}-active 2>/dev/null || echo "blue")

if [ "$CURRENT" = "blue" ]; then
  NEXT="green"
else
  NEXT="blue"
fi

echo "Deploying ${SERVICE}:${VERSION} to ${NEXT} slot (${ENVIRONMENT})..."

# Start new version on inactive slot
docker run -d \
  --name ${SERVICE}-${ENVIRONMENT}-${NEXT} \
  --label slot=${NEXT} \
  --label version=${VERSION} \
  --restart unless-stopped \
  -p $([ "$NEXT" = "blue" ] && echo "8081:80" || echo "8082:80") \
  ${REGISTRY}/${SERVICE}:${VERSION}

# Wait for health check
echo "Waiting for health check..."
for i in $(seq 1 30); do
  PORT=$([ "$NEXT" = "blue" ] && echo "8081" || echo "8082")
  if curl -sf http://localhost:${PORT}/health > /dev/null 2>&1; then
    echo "Health check passed!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Health check failed! Rolling back..."
    docker stop ${SERVICE}-${ENVIRONMENT}-${NEXT}
    docker rm ${SERVICE}-${ENVIRONMENT}-${NEXT}
    exit 1
  fi
  sleep 2
done

# Switch traffic (update reverse proxy config)
echo "Switching traffic to ${NEXT}..."
# Update your reverse proxy (nginx/traefik/haproxy) configuration here
# Example: update upstream to point to new container

# Stop old version
docker stop ${SERVICE}-${ENVIRONMENT}-${CURRENT} || true
docker rm ${SERVICE}-${ENVIRONMENT}-${CURRENT} || true

echo "Deployment complete. Active slot: ${NEXT}"
```

### Deployment Strategy: Canary

Canary deployment gradually routes a percentage of traffic to the new version.

```bash
#!/bin/bash
# deploy-canary.sh
# Usage: ./deploy-canary.sh backend v1.2.3 10

SERVICE=$1
VERSION=$2
CANARY_PERCENT=$3
REGISTRY="ghcr.io/org/project"

echo "Deploying ${SERVICE}:${VERSION} as canary (${CANARY_PERCENT}%)..."

# Deploy canary version
docker run -d \
  --name ${SERVICE}-canary \
  --label type=canary \
  --label version=${VERSION} \
  --restart unless-stopped \
  -p 8081:8080 \
  ${REGISTRY}/${SERVICE}:${VERSION}

# Wait for health check
echo "Waiting for health check..."
for i in $(seq 1 30); do
  if curl -sf http://localhost:8081/api/v1/health > /dev/null 2>&1; then
    echo "Health check passed!"
    break
  fi
  if [ $i -eq 30 ]; then
    echo "Health check failed! Removing canary..."
    docker stop ${SERVICE}-canary
    docker rm ${SERVICE}-canary
    exit 1
  fi
  sleep 2
done

echo "Canary deployed. Route ${CANARY_PERCENT}% of traffic to port 8081."
echo "Monitor for errors, then run: ./promote-canary.sh ${SERVICE} ${VERSION}"
```

### Health Check Verification

After every deployment, verify health endpoints:

```bash
#!/bin/bash
# verify-deployment.sh
# Usage: ./verify-deployment.sh https://staging.example.com

BASE_URL=$1
MAX_RETRIES=30
RETRY_INTERVAL=2

echo "Verifying deployment at ${BASE_URL}..."

for i in $(seq 1 $MAX_RETRIES); do
  HTTP_CODE=$(curl -sf -o /dev/null -w "%{http_code}" ${BASE_URL}/health 2>/dev/null || echo "000")
  
  if [ "$HTTP_CODE" = "200" ]; then
    echo "Health check passed! (attempt ${i}/${MAX_RETRIES})"
    
    # Verify security headers
    HEADERS=$(curl -sI ${BASE_URL})
    echo ""
    echo "Security headers:"
    echo "$HEADERS" | grep -E "X-Frame-Options|X-Content-Type-Options|X-XSS-Protection|Referrer-Policy" || echo "  WARNING: Missing security headers"
    
    # Verify backend health
    BACKEND_CODE=$(curl -sf -o /dev/null -w "%{http_code}" ${BASE_URL}/api/v1/health 2>/dev/null || echo "000")
    echo ""
    echo "Backend health: HTTP ${BACKEND_CODE}"
    
    exit 0
  fi
  
  echo "Waiting... (attempt ${i}/${MAX_RETRIES}, HTTP ${HTTP_CODE})"
  sleep $RETRY_INTERVAL
done

echo "ERROR: Health check failed after ${MAX_RETRIES} attempts"
exit 1
```

### Docker Compose for Full Stack

`docker-compose.yml`:

```yaml
services:
  frontend:
    image: ghcr.io/org/project/frontend:latest
    ports:
      - "80:80"
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    labels:
      - "org.opencontainers.image.version=${VERSION:-latest}"

  backend:
    image: ghcr.io/org/project/backend:latest
    ports:
      - "8080:8080"
    restart: unless-stopped
    environment:
      - MICRONAUT_ENVIRONMENT=production
    healthcheck:
      test: ["CMD", "wget", "-qO-", "http://localhost:8080/api/v1/health"]
      interval: 30s
      timeout: 3s
      retries: 3
    labels:
      - "org.opencontainers.image.version=${VERSION:-latest}"
```

```bash
# Deploy full stack
VERSION=v1.2.3 docker compose up -d

# Verify
docker compose ps
curl -sf http://localhost/health
curl -sf http://localhost:8080/api/v1/health
```

---

## Command: `/build rollback`

Rolls back to a previous known-good version.

### Quick Rollback

```bash
#!/bin/bash
# rollback.sh
# Usage: ./rollback.sh frontend v1.2.2

SERVICE=$1
TARGET_VERSION=$2
REGISTRY="ghcr.io/org/project"

echo "Rolling back ${SERVICE} to ${TARGET_VERSION}..."

# Pull the target version
docker pull ${REGISTRY}/${SERVICE}:${TARGET_VERSION}

# Stop current container
docker stop ${SERVICE} || true
docker rm ${SERVICE} || true

# Start with target version
case $SERVICE in
  frontend)
    docker run -d \
      --name frontend \
      --restart unless-stopped \
      -p 80:80 \
      ${REGISTRY}/${SERVICE}:${TARGET_VERSION}
    HEALTH_URL="http://localhost/health"
    ;;
  backend)
    docker run -d \
      --name backend \
      --restart unless-stopped \
      -p 8080:8080 \
      ${REGISTRY}/${SERVICE}:${TARGET_VERSION}
    HEALTH_URL="http://localhost:8080/api/v1/health"
    ;;
esac

# Verify health
for i in $(seq 1 30); do
  if curl -sf ${HEALTH_URL} > /dev/null 2>&1; then
    echo "Rollback successful! ${SERVICE} running ${TARGET_VERSION}"
    exit 0
  fi
  sleep 2
done

echo "ERROR: Rollback health check failed!"
exit 1
```

### Rollback via Git Tag

```bash
# List recent tags
git tag --sort=-version:refname | head -10

# Rollback frontend to previous tag
PREVIOUS=$(git tag --sort=-version:refname | sed -n '2p')
echo "Rolling back to: ${PREVIOUS}"

# Re-run the release pipeline for the previous tag
git checkout ${PREVIOUS}
git tag -f ${PREVIOUS} ${PREVIOUS}
git push origin ${PREVIOUS} --force
```

### Rollback Decision Tree

```
Rollback triggered
│
├── Health check failing?
│   ├── Yes → Immediate rollback to previous version
│   └── No → Continue monitoring
│
├── Error rate > 1%?
│   ├── Yes → Rollback to previous version
│   └── No → Continue monitoring
│
├── Latency p99 > 2s?
│   ├── Yes → Rollback to previous version
│   └── No → Continue monitoring
│
└── Business logic error?
    ├── Yes → Assess impact, rollback if critical
    └── No → Continue monitoring
```

### Post-Rollback Checklist

```
Post-Rollback Checklist
═══════════════════════

[ ] Previous version is running and healthy
[ ] Health endpoints returning 200
[ ] Error rate returned to baseline
[ ] Latency returned to baseline
[ ] Users can access the application
[ ] Incident ticket created
[ ] Root cause analysis scheduled
[ ] Fix branch created
[ ] Monitoring dashboards checked
[ ] Stakeholders notified
```

---

## Docker Compose for Local Development

`docker-compose.dev.yml`:

```yaml
services:
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    ports:
      - "3000:80"
    volumes:
      - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8080:8080"
    environment:
      - MICRONAUT_ENVIRONMENT=development
    volumes:
      - ./backend/src:/app/src:ro
```

```bash
# Build and run locally
docker compose -f docker-compose.dev.yml up --build

# Rebuild after changes
docker compose -f docker-compose.dev.yml up --build -d
```

---

## Image Optimization

### Frontend Image Size Optimization

```dockerfile
# Multi-stage with minimal runtime
FROM oven/bun:1 AS build
WORKDIR /app
COPY package.json bun.lockb ./
RUN bun install --frozen-lockfile --production
COPY . .
RUN bun run build

FROM nginx:stable-alpine AS runtime
RUN apk add --no-cache tzdata && \
    cp /usr/share/zoneinfo/UTC /etc/localtime && \
    echo "UTC" > /etc/timezone && \
    apk del tzdata
COPY --from=build /app/.output/public /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Backend Image Size Optimization

```dockerfile
# Layer caching with dependency resolution first
FROM bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl AS build
WORKDIR /app
COPY gradle/ gradle/
COPY gradlew build.gradle.kts settings.gradle.kts gradle.properties ./
RUN chmod +x gradlew && ./gradlew dependencies --no-daemon || true
COPY src/ src/
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
  "-XX:MaxRAMPercentage=75.0", \
  "-XX:+UseG1GC", \
  "-jar", "app.jar"]
```

---

## Workflow

When invoked, follow this decision tree:

```
/build [command]
       │
       ├── frontend ──────► Build frontend container
       │                     ├── Verify SolidStart preset: "static"
       │                     ├── bun install --frozen-lockfile
       │                     ├── bun run build → .output/public/
       │                     ├── docker build (Bun → nginx)
       │                     └── Verify /health endpoint
       │
       ├── backend ────────► Build backend container
       │                     ├── Verify Gradle + Shadow plugin
       │                     ├── ./gradlew shadowJar
       │                     ├── docker build (Liberica CRaC)
       │                     └── Verify /api/v1/health endpoint
       │
       ├── pipeline ───────► Generate CI/CD configuration
       │                     ├── Ask: GitHub Actions / GitLab CI / other?
       │                     ├── Ask: Container registry?
       │                     ├── Generate workflow YAML files
       │                     ├── Configure secrets list
       │                     └── Document pipeline stages
       │
       ├── release ────────► Create version release
       │                     ├── Analyze commits since last tag
       │                     ├── Determine SemVer bump
       │                     ├── Update version in package files
       │                     ├── Generate changelog
       │                     ├── Create git tag
       │                     └── Push tag to trigger pipeline
       │
       ├── deploy ─────────► Deploy to environment
       │                     ├── Ask: staging or production?
       │                     ├── Ask: deployment strategy (blue-green/canary)?
       │                     ├── Pull latest image
       │                     ├── Deploy with health check
       │                     ├── Verify security headers
       │                     └── Report deployment status
       │
       └── rollback ───────► Rollback to previous version
                             ├── List recent versions/tags
                             ├── Ask: target version?
                             ├── Stop current container
                             ├── Start previous version
                             ├── Verify health check
                             └── Generate post-rollback report
```

---

## Reference Files

Reference files contain extended templates and examples. Consult these for the most current patterns:

| Reference | Content |
|-----------|---------|
| `references/frontend-dockerfile.md` | Complete frontend Dockerfile, nginx.conf variants, .dockerignore |
| `references/backend-dockerfile.md` | Complete backend Dockerfile, JVM tuning, .dockerignore |
| `references/ci-cd-pipeline-template.md` | Full GitHub Actions workflow templates |
| `references/release-checklist.md` | Pre-release verification checklist |
| `references/changelog-template.md` | Changelog format and generation scripts |

---

## Rules

1. **Always use multi-stage builds** — build dependencies must not be in the runtime image
2. **Pin base image versions** — use `oven/bun:1`, `nginx:stable-alpine`, `bellsoft/liberica-runtime-container:jdk-21-crac-cds-slim-musl`
3. **Health check every container** — frontend `/health`, backend `/api/v1/health`
4. **Security headers on every response** — X-Frame-Options, X-Content-Type-Options, X-XSS-Protection, Referrer-Policy
5. **Cache headers by asset type** — `immutable` for hashed assets, `no-cache` for HTML
6. **Never commit secrets** — use CI/CD secrets, `.env` files in `.gitignore`
7. **Tag images with version** — always include SemVer tag alongside `latest`
8. **Test locally before push** — build and run container, verify health endpoint
9. **Conventional commits required** — all commits must follow the conventional commit format
10. **Rollback plan for every deploy** — know the previous version tag before deploying
