---
name: "monitoring"
tags: [observability, logging, metrics, tracing, alerts, incidents, grafana, prometheus, runbook]
description: |
  Monitoring & Observability skill for the SDLC "Operations" phase. Configures the three
  pillars of observability (logs, metrics, traces) for the agentden tech stack, generates
  Grafana dashboards, Prometheus alert rules, operational runbooks, and guides incident
  response. Covers health checks, structured logging, alerting strategy, and post-mortem
  workflows.

  Trigger phrases:
    - "set up monitoring"
    - "configure logging"
    - "create alert"
    - "incident response"
    - "observability"
    - "health check"
    - "dashboard"
    - "runbook"
    - "alert rules"
    - "post-mortem"
    - "on-call"
    - "SLO"
    - "SLI"
    - "error budget"
    - "trace correlation"

  Tech stack assumptions:
    Frontend — nginx:stable-alpine (static SSG), nginx-prometheus-exporter
    Backend  — Java 21 + Micronaut 4.7 + Micrometer + Logback + OpenTelemetry
    Metrics  — Prometheus + Grafana
    Tracing  — OpenTelemetry SDK + W3C Trace Context propagation
    Alerting — Prometheus Alertmanager + Grafana Alerting
license: MIT
metadata:
  compatible_agents:
    - claude-code
  author: agentden
  version: "1.0.0"
  category: sdlc-operations
  tech_stack:
    frontend: "nginx:stable-alpine + nginx-prometheus-exporter"
    backend: "Java 21 + Micronaut 4.7 + Micrometer + Logback + OpenTelemetry"
    metrics: "Prometheus + Grafana"
    tracing: "OpenTelemetry + W3C Trace Context"
    alerting: "Prometheus Alertmanager + Grafana Alerting"
---

# Monitoring & Observability

This skill governs the **Monitoring & Observability** phase of the SDLC. It configures the three pillars of observability — logs, metrics, and traces — for the full agentden stack, generates operational dashboards and alert rules, produces runbooks, and guides incident response from detection through post-mortem.

## Commands

| Command | Description |
|---|---|
| `/monitor setup` | Configure logging, metrics, and tracing for the full stack |
| `/monitor dashboard` | Generate Grafana dashboard JSON configuration |
| `/monitor alerts` | Generate Prometheus alert rules and Alertmanager routing |
| `/monitor runbook` | Generate operational runbook for a service or incident type |
| `/monitor incident` | Walk through structured incident response process |
| `/monitor health` | Verify all health checks and observability endpoints |

## Announce

When this skill activates, announce:

> "Using the **monitoring** skill to configure observability for your stack."

---

## Three Pillars of Observability

```
┌──────────────────────────────────────────────────────────────────────┐
│                      Observability Platform                          │
│                                                                      │
│   ┌─────────────┐    ┌──────────────┐    ┌──────────────────────┐   │
│   │    LOGS      │    │   METRICS     │    │      TRACES          │   │
│   │             │    │              │    │                      │   │
│   │ Frontend:   │    │ Prometheus   │    │ OpenTelemetry SDK    │   │
│   │  nginx      │    │  + Grafana   │    │  + W3C Trace Context │   │
│   │  access/    │    │              │    │                      │   │
│   │  error log  │    │ Frontend:    │    │ Backend:             │   │
│   │             │    │  nginx-      │    │  OTel Java Agent     │   │
│   │ Backend:    │    │  prometheus- │    │  + Micrometer        │   │
│   │  Micronaut  │    │  exporter    │    │  bridge              │   │
│   │  structured │    │              │    │                      │   │
│   │  JSON via   │    │ Backend:     │    │ Correlation:         │   │
│   │  Logback    │    │  Micrometer  │    │  trace_id in logs    │   │
│   │             │    │  + Prometheus│    │  + span_id in logs   │   │
│   └─────────────┘    └──────────────┘    └──────────────────────┘   │
│                                                                      │
│   Correlation Key: trace_id propagated across all three pillars      │
└──────────────────────────────────────────────────────────────────────┘
```

### Pillar 1: Logs

**Frontend (nginx)**

| Log Type | Format | Location |
|----------|--------|----------|
| Access log | Combined + JSON (custom) | `/var/log/nginx/access.log` |
| Error log | Standard nginx error format | `/var/log/nginx/error.log` |

nginx structured access log configuration:

```nginx
log_format json_combined escape=json
    '{'
    '"time":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"request":"$request",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_response_time":"$upstream_response_time",'
    '"http_referer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"request_id":"$request_id"'
    '}';

access_log /var/log/nginx/access.log json_combined;
```

**Backend (Micronaut + Logback)**

Structured JSON logging via `logstash-logback-encoder`. Every log entry includes `trace_id` and `span_id` for cross-pillar correlation.

See the full Logback configuration in [Command: `/monitor setup`](#command-monitor-setup) below.

### Pillar 2: Metrics

| Component | Exporter | Scrape Target | Key Metrics |
|-----------|----------|---------------|-------------|
| nginx | `nginx-prometheus-exporter` (sidecar) | `:9113/metrics` | `nginx_http_requests_total`, `nginx_upstream_response_time`, `nginx_connections_active` |
| Micronaut | Micrometer + `micrometer-registry-prometheus` | `:8080/metrics` (via `micronaut-management`) | `http_server_requests_seconds`, `jvm_memory_used`, `system_cpu_usage` |

**Micrometer configuration** (application.yml):

```yaml
micronaut:
  metrics:
    enabled: true
    export:
      prometheus:
        enabled: true
        step: PT30S
        descriptions: true
    tags:
      application: ${micronaut.application.name}
```

### Pillar 3: Traces

**OpenTelemetry + W3C Trace Context**

| Component | Configuration | Propagation |
|-----------|--------------|-------------|
| Backend | OTel Java Agent (`-javaagent`) or Micronaut OTel integration | W3C `traceparent` + `tracestate` headers |
| Frontend | nginx passes `traceparent` header upstream (no modification) | Header passthrough |

**Micronaut OpenTelemetry integration:**

```yaml
# build.gradle.kts
# implementation("io.micronaut.tracing:micronaut-tracing-opentelemetry-http")

# application.yml
otel:
  traces:
    exporter: otlp
    exporter:
      otlp:
        endpoint: http://otel-collector:4317
    resource:
      attributes:
        service.name: ${micronaut.application.name}
        service.version: ${app.version:unknown}
    propagation:
      enabled: true
```

**Trace-log correlation:** Every log statement automatically includes `trace_id` and `span_id` via MDC (Mapped Diagnostic Context) when a trace is active. This allows jumping from a Grafana/Loki log line directly to the corresponding Jaeger/Tempo trace.

---

## Health Checks

### Frontend Health Check: `GET /health`

nginx serves a lightweight JSON health response:

```nginx
location /health {
    access_log off;
    default_type application/json;
    return 200 '{"status":"UP","service":"frontend","timestamp":"$time_iso8601"}';
}
```

**Response:**

```json
{
  "status": "UP",
  "service": "frontend",
  "timestamp": "2026-04-22T14:30:00+00:00"
}
```

### Backend Health Checks

Micronaut provides two health endpoints via the `management` endpoint:

**`GET /health`** — Micronaut built-in health endpoint:

```yaml
micronaut:
  endpoints:
    health:
      enabled: true
      sensitive: false
      details-visible: ANONYMOUS
  endpoint:
    health:
      enabled: true
```

**Response:**

```json
{
  "status": "UP",
  "details": {
    "compositeDiscoveryClient": { "status": "UP" },
    "diskSpace": {
      "status": "UP",
      "details": {
        "total": 107374182400,
        "free": 53687091200,
        "threshold": 10485760
      }
    },
    "jdbc": { "status": "UP" },
    "ping": { "status": "UP" }
  }
}
```

**`GET /api/v1/health`** — Application-level health endpoint:

```java
@Controller("/api/v1")
public class HealthController {

    @Get("/health")
    public HttpResponse<HealthResponse> health() {
        return HttpResponse.ok(new HealthResponse(
            "UP",
            micronautApplication.getName(),
            Instant.now(),
            Runtime.version().toString()
        ));
    }

    @Serdeable
    public record HealthResponse(
        String status,
        String service,
        Instant timestamp,
        String jvm
    ) {}
}
```

### Health Check Verification Checklist

```
Health Check Verification
═════════════════════════

Frontend:
  [ ] GET https://<frontend>/health → 200 {"status":"UP"}
  [ ] Response time < 50ms
  [ ] No access log entry (access_log off)

Backend:
  [ ] GET https://<backend>/health → 200 {"status":"UP"}
  [ ] GET https://<backend>/api/v1/health → 200 {"status":"UP"}
  [ ] Disk space check returns > threshold
  [ ] Database connectivity confirmed (jdbc: UP)
  [ ] Response time < 100ms

Infrastructure:
  [ ] Prometheus can scrape /metrics on backend:8080
  [ ] Prometheus can scrape nginx-exporter on :9113
  [ ] Grafana can query Prometheus datasource
  [ ] Alertmanager receives alerts from Prometheus
  [ ] OTel Collector receives traces from backend
```

---

## Alerting Strategy

### Severity Levels

| Severity | Label | Response Time | Notification | Example |
|----------|-------|---------------|-------------|---------|
| **P1** | Critical | < 5 minutes | Page on-call (phone + Slack) | Service completely down, data loss |
| **P2** | High | < 15 minutes | Slack alert + on-call notification | Error rate > 5%, health check failing |
| **P3** | Medium | < 1 hour | Slack alert (business hours) | Latency p95 > threshold, disk > 80% |
| **P4** | Low | < 24 hours | Slack channel, ticket created | Certificate expiring in 30 days, minor anomaly |

### Alert Routing Matrix

```yaml
# Alertmanager routing configuration
route:
  receiver: 'default'
  group_by: ['alertname', 'cluster', 'service']
  group_wait: 10s
  group_interval: 5m
  repeat_interval: 4h
  routes:
    - match:
        severity: critical
      receiver: 'on-call-pager'
      group_wait: 5s
      repeat_interval: 15m
    - match:
        severity: high
      receiver: 'on-call-slack'
      group_wait: 30s
      repeat_interval: 30m
    - match:
        severity: medium
      receiver: 'team-slack'
      repeat_interval: 2h
    - match:
        severity: low
      receiver: 'notifications-channel'
      repeat_interval: 24h

receivers:
  - name: 'on-call-pager'
    pagerduty_configs:
      - service_key: <PAGERDUTY_SERVICE_KEY>
    slack_configs:
      - channel: '#incidents-critical'
  - name: 'on-call-slack'
    slack_configs:
      - channel: '#incidents'
  - name: 'team-slack'
    slack_configs:
      - channel: '#monitoring'
  - name: 'notifications-channel'
    slack_configs:
      - channel: '#notifications'
  - name: 'default'
    slack_configs:
      - channel: '#monitoring'
```

### Alert Quality Rules

Every alert must be:

1. **Actionable** — There is a clear remediation step. If nobody knows what to do, it should not alert.
2. **Accurate** — Low false-positive rate. Noise desensitizes on-call.
3. **Adequate** — Covers the critical failure modes. No blind spots on user-facing impact.
4. **Annotated** — Every alert rule includes `summary`, `description`, `runbook_url`, and `severity` labels.

---

## Dashboard Design

### Method 1: RED — For Services (Request-oriented)

**R**ate, **E**rrors, **D**uration — apply to every HTTP service.

| Metric | Prometheus Query | Panel Type | Threshold |
|--------|-----------------|------------|-----------|
| **Rate** (throughput) | `rate(http_server_requests_seconds_count[5m])` | Time series / Stat | Baseline ± 50% |
| **Errors** (error rate) | `rate(http_server_requests_seconds_count{status=~"5.."}[5m]) / rate(http_server_requests_seconds_count[5m])` | Gauge + Trend | > 1% = warning, > 5% = critical |
| **Duration** (latency) | `histogram_quantile(0.95, rate(http_server_requests_seconds_bucket[5m]))` | Time series | p95 < 500ms |

### Method 2: USE — For Resources (Utilization-oriented)

**U**tilization, **S**aturation, **E**rrors — apply to CPU, memory, disk, network, connections.

| Resource | Utilization | Saturation | Errors |
|----------|-------------|------------|--------|
| **CPU** | `system_cpu_usage` | `process_cpu_usage` trend | N/A |
| **Memory** | `jvm_memory_used_bytes / jvm_memory_max_bytes` | GC pause time | OOM kill events |
| **Disk** | `disk_total_bytes - disk_free_bytes` | I/O wait queue depth | Disk I/O errors |
| **Network** | Bandwidth used / capacity | TCP retransmits, connection resets | Dropped packets |
| **Connections** | `nginx_connections_active / nginx_connections_max` | Connection queue length | Connection refused |

### Method 3: Core Web Vitals — For Frontend

| Vital | Metric | Target | Source |
|-------|--------|--------|--------|
| **LCP** (Largest Contentful Paint) | Time to render largest content | < 2.5s | Real User Monitoring (RUM) or Lighthouse |
| **INP** (Interaction to Next Paint) | Responsiveness to user input | < 200ms | RUM |
| **CLS** (Cumulative Layout Shift) | Visual stability | < 0.1 | RUM |

### Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────┐
│  Service Overview Dashboard                                         │
├───────────────┬───────────────┬───────────────┬─────────────────────┤
│  Uptime       │  Request Rate │  Error Rate   │  p95 Latency        │
│  (stat)       │  (time series)│  (gauge)      │  (time series)      │
│  99.9%        │               │  0.3%         │                     │
├───────────────┴───────────────┴───────────────┴─────────────────────┤
│  Request Rate (5m) — by endpoint                                    │
│  [time series: stacked area by URI path]                            │
├──────────────────────────────┬──────────────────────────────────────┤
│  Latency Heatmap             │  Error Rate by Status Code           │
│  [heatmap: p50, p90, p95]   │  [stacked bar: 4xx vs 5xx]          │
├──────────────────────────────┴──────────────────────────────────────┤
│  Resource Utilization (USE Method)                                  │
│  ┌──────────────┬──────────────┬──────────────┬──────────────────┐ │
│  │ CPU %        │ Memory %     │ Disk %       │ Active Conn.     │ │
│  │ (gauge)      │ (gauge)      │ (stat)       │ (time series)    │ │
│  └──────────────┴──────────────┴──────────────┴──────────────────┘ │
├─────────────────────────────────────────────────────────────────────┤
│  Core Web Vitals (Frontend)                                         │
│  ┌──────────────┬──────────────┬──────────────┐                    │
│  │ LCP          │ INP          │ CLS          │                    │
│  │ 1.8s ✓      │ 120ms ✓     │ 0.05 ✓      │                    │
│  └──────────────┴──────────────┴──────────────┘                    │
├─────────────────────────────────────────────────────────────────────┤
│  Top 10 Slowest Endpoints (table)                                   │
│  ┌────────────────────────┬─────────┬──────────┬──────────────────┐│
│  │ Endpoint               │ p95 (ms)│ Req/min  │ Error %          ││
│  ├────────────────────────┼─────────┼──────────┼──────────────────┤│
│  │ /api/v1/reports        │ 1,200   │ 12       │ 0.5%             ││
│  │ /api/v1/users          │ 340     │ 45       │ 0.1%             ││
│  └────────────────────────┴─────────┴──────────┴──────────────────┘│
└─────────────────────────────────────────────────────────────────────┘
```

---

## Incident Response Process

### Process Flow

```
  Detect ──▶ Triage ──▶ Investigate ──▶ Mitigate ──▶ Resolve ──▶ Post-mortem
     │          │           │              │            │            │
     ▼          ▼           ▼              ▼            ▼            ▼
  Alert      Classify    Root cause    Stop the      Confirm      Learn &
  triggered  severity    analysis     bleeding      fix works    improve
```

### Phase 1: Detect

- Alert fires via Prometheus → Alertmanager
- On-call receives notification ( PagerDuty / Slack / phone )
- Alternatively: user report, anomaly detection, health check failure

**Detection checklist:**
- [ ] Alert triggered automatically (not relying on user reports)
- [ ] Alert includes `runbook_url` annotation linking to the runbook
- [ ] On-call acknowledges within the target response time for severity
- [ ] Incident channel created (if P1 or P2)

### Phase 2: Triage

Classify the incident:

| Field | Values |
|-------|--------|
| **Severity** | P1 (Critical) / P2 (High) / P3 (Medium) / P4 (Low) |
| **Scope** | Single user / Subset / All users / Internal only |
| **Impact** | Data loss / Revenue loss / Degraded experience / No user impact |
| **Type** | Availability / Performance / Correctness / Security |

**Triage decision tree:**

```
Is the service completely down or losing data?
  ├── Yes → P1 Critical
  └── No → Is user-facing functionality impaired?
              ├── Yes → Are > 10% of users affected?
              │           ├── Yes → P1 Critical
              │           └── No → P2 High
              └── No → Is there degraded performance or risk?
                          ├── Yes → P3 Medium
                          └── No → P4 Low
```

### Phase 3: Investigate

1. **Check dashboards** — Open the service overview dashboard, look for anomalies in the RED metrics
2. **Check logs** — Search Loki/ELK for `trace_id` from affected requests, look for ERROR/WARN entries
3. **Check traces** — Find slow or failed traces in Jaeger/Tempo using the `trace_id` from logs
4. **Check recent deployments** — Correlate timing with recent deploys (`git log --since="2 hours ago"`)
5. **Check infrastructure** — CPU, memory, disk, network on the USE dashboard
6. **Form hypothesis** — Based on evidence, state the most likely cause

**Investigation commands (runbook-style):**

```bash
# Check backend health
curl -s https://backend/health | jq .

# Check recent logs for errors
curl -s 'http://loki:3100/loki/api/v1/query_range' \
  --data-urlencode 'query={service="backend"} |= "ERROR"' \
  --data-urlencode "start=$(date -d '1 hour ago' +%s)000000000" \
  --data-urlencode "end=$(date +%s)000000000" | jq .

# Check Prometheus for high error rate
curl -s 'http://prometheus:9090/api/v1/query' \
  --data-urlencode 'query=rate(http_server_requests_seconds_count{status=~"5.."}[5m])' | jq .

# Check recent deployments
git log --oneline --since="4 hours ago"

# Check pod/container status
kubectl get pods -l app=backend
docker ps --filter "name=backend"
```

### Phase 4: Mitigate

Goal: **stop the bleeding** as fast as possible. Root cause analysis can wait.

| Mitigation Strategy | When to Use | Example |
|---------------------|-------------|---------|
| **Rollback** | Recent deploy caused the issue | `kubectl rollout undo deployment/backend` |
| **Scale out** | Resource exhaustion | Increase replica count |
| **Feature flag off** | New feature causing errors | Disable the feature flag |
| **Circuit break** | Downstream dependency failing | Enable circuit breaker |
| **DNS failover** | Regional outage | Switch to healthy region |
| **Rate limit** | Overload from traffic spike | Apply emergency rate limits |
| **Restart** | Stuck process, memory leak | Rolling restart of pods |

### Phase 5: Resolve

- Confirm mitigation resolved the user-facing issue
- Verify metrics return to baseline (RED dashboard)
- Monitor for at least 30 minutes after mitigation
- Communicate resolution to stakeholders
- Update incident ticket with timeline and actions taken

### Phase 6: Post-mortem

Conduct a blameless post-mortem within 48 hours of P1/P2 incidents. Use the template in `references/incident-post-mortem-template.md`.

**Post-mortem structure:**

```markdown
# Incident Post-Mortem: [INCIDENT-ID]

## Summary
- **Date:** YYYY-MM-DD
- **Duration:** X hours Y minutes
- **Severity:** P1/P2
- **Impact:** [Who was affected, how many, what broke]

## Timeline (all times UTC)
| Time | Event | Source |
|------|-------|--------|
| HH:MM | Alert triggered | PagerDuty |
| HH:MM | On-call acknowledged | Slack |
| HH:MM | Root cause identified | Investigation |
| HH:MM | Mitigation applied | Runbook step |
| HH:MM | Service restored | Monitoring |

## Root Cause
[Detailed technical explanation]

## Contributing Factors
1. [Factor 1]
2. [Factor 2]

## What Went Well
- [Detection was fast because...]
- [Runbook was followed correctly...]

## What Could Be Improved
- [Alert fired too late because...]
- [Runbook was missing step for...]

## Action Items
| Action | Owner | Priority | Due Date | Status |
|--------|-------|----------|----------|--------|
| Add alert for [condition] | @engineer | P2 | YYYY-MM-DD | Open |
| Update runbook section X | @engineer | P3 | YYYY-MM-DD | Open |
| Add circuit breaker for [dependency] | @engineer | P2 | YYYY-MM-DD | Open |
```

---

## Command: `/monitor setup`

Configure logging, metrics, and tracing for the full stack.

### Instructions

1. **Determine scope**: Ask which services to configure (frontend, backend, or both). Default: both.
2. **Determine environment**: Ask for target environment (dev, staging, production). Default: production.
3. **Generate configurations** for all three pillars.
4. **Verify connectivity** between components.

### Output Files

| File | Location | Purpose |
|------|----------|---------|
| `logback.xml` | `backend/src/main/resources/logback.xml` | Structured JSON logging with trace correlation |
| `application.yml` additions | `backend/src/main/resources/application.yml` | Health endpoints, metrics, tracing config |
| `nginx.conf` additions | `frontend/nginx.conf` | JSON access log, health endpoint, OTel headers |
| `docker-compose.monitoring.yml` | Project root | Prometheus, Grafana, Alertmanager, OTel Collector |
| `prometheus.yml` | `monitoring/prometheus/` | Scrape configuration |
| `otel-collector-config.yml` | `monitoring/otel-collector/` | Trace pipeline configuration |

### Backend: `logback.xml` (Structured JSON with Trace Correlation)

```xml
<configuration>
    <springProperty scope="context" name="APP_NAME" source="micronaut.application.name" defaultValue="backend"/>

    <appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
        <encoder class="net.logstash.logback.encoder.LogstashEncoder">
            <customFields>{
                "service":"${APP_NAME}",
                "environment":"${ENV:-production}"
            }</customFields>
            <includeMdcKeyName>trace_id</includeMdcKeyName>
            <includeMdcKeyName>span_id</includeMdcKeyName>
            <includeMdcKeyName>trace_flags</includeMdcKeyName>
            <includeContext>true</includeContext>
            <includeStructuredArguments>true</includeStructuredArguments>
            <includeNonStructuredArguments>false</includeNonStructuredArguments>
            <includeTags>true</includeTags>
            <throwableConverter class="net.logstash.logback.stacktrace.ShortenedThrowableConverter">
                <maxDepthPerThrowable>20</maxDepthPerThrowable>
                <maxLength>2048</maxLength>
                <shortenedClassNameLength>30</shortenedClassNameLength>
                <exclude>sun\.reflect\..*</exclude>
                <exclude>java\.lang\.reflect\..*</exclude>
                <exclude>org\.springframework\..*</exclude>
                <exclude>io\.netty\..*</exclude>
            </throwableConverter>
        </encoder>
    </appender>

    <appender name="STDOUT" class="ch.qos.logback.core.ConsoleAppender">
        <encoder>
            <pattern>%d{HH:mm:ss.SSS} [%thread] %-5level %logger{36} [trace=%X{trace_id:-none}] - %msg%n</pattern>
        </encoder>
    </appender>

    <logger name="io.micronaut" level="INFO"/>
    <logger name="com.example" level="DEBUG"/>
    <logger name="io.opentelemetry" level="WARN"/>

    <if condition='property("ENV").equals("production")'>
        <then>
            <root level="INFO">
                <appender-ref ref="JSON"/>
            </root>
        </then>
        <else>
            <root level="INFO">
                <appender-ref ref="STDOUT"/>
            </root>
        </else>
    </if>
</configuration>
```

**Dependencies to add** (`build.gradle.kts`):

```kotlin
dependencies {
    implementation("ch.qos.logback:logback-classic")
    implementation("net.logstash.logback:logstash-logback-encoder:8.0")
    implementation("io.micronaut.micrometer:micronaut-micrometer-registry-prometheus")
    implementation("io.micronaut.tracing:micronaut-tracing-opentelemetry-http")
    runtimeOnly("io.opentelemetry:opentelemetry-exporter-otlp")
}
```

### Backend: `application.yml` Additions

```yaml
micronaut:
  application:
    name: backend
  server:
    port: 8080
  endpoints:
    health:
      enabled: true
      sensitive: false
      details-visible: ANONYMOUS
    metrics:
      enabled: true
      sensitive: false
    prometheus:
      enabled: true
      sensitive: false
  metrics:
    enabled: true
    export:
      prometheus:
        enabled: true
        step: PT30S
        descriptions: true
    tags:
      application: ${micronaut.application.name}
      environment: ${ENV:production}
    binders:
      jvm:
        enabled: true
      processor:
        enabled: true
      uptime:
        enabled: true
      files:
        enabled: true
      logback:
        enabled: true
      http:
        enabled: true
        server:
          request:
            enabled: true
          response:
            enabled: true
    web:
      server:
        request:
          autotime:
            enabled: true
            percentiles: "0.5,0.9,0.95,0.99"
            histogram:
              enabled: true

otel:
  traces:
    exporter: otlp
    exporter:
      otlp:
        endpoint: ${OTEL_EXPORTER_OTLP_ENDPOINT:http://otel-collector:4317}
    resource:
      attributes:
        service.name: ${micronaut.application.name}
        service.version: ${APP_VERSION:unknown}
        deployment.environment: ${ENV:production}
    propagation:
      enabled: true

logger:
  levels:
    root: INFO
    io.micronaut: INFO
    io.micronaut.http: DEBUG
    com.example: DEBUG
    io.opentelemetry: WARN
```

### Frontend: `nginx.conf` Additions

```nginx
# Add to existing nginx.conf server block

# Structured JSON access log
log_format json_combined escape=json
    '{'
    '"time":"$time_iso8601",'
    '"remote_addr":"$remote_addr",'
    '"request":"$request",'
    '"method":"$request_method",'
    '"uri":"$request_uri",'
    '"status":$status,'
    '"body_bytes_sent":$body_bytes_sent,'
    '"request_time":$request_time,'
    '"upstream_response_time":"$upstream_response_time",'
    '"http_referer":"$http_referer",'
    '"http_user_agent":"$http_user_agent",'
    '"request_id":"$request_id",'
    '"traceparent":"$http_traceparent"'
    '}';

access_log /var/log/nginx/access.log json_combined;
error_log /var/log/nginx/error.log warn;

# Health endpoint (JSON response)
location /health {
    access_log off;
    default_type application/json;
    return 200 '{"status":"UP","service":"frontend","timestamp":"$time_iso8601"}';
}

# Pass trace headers to backend
location /api/ {
    proxy_pass http://backend:8080;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_set_header traceparent $http_traceparent;
    proxy_set_header tracestate $http_tracestate;
}
```

### Docker Compose for Monitoring Stack

```yaml
# docker-compose.monitoring.yml
version: "3.8"

services:
  prometheus:
    image: prom/prometheus:v2.55.0
    container_name: prometheus
    ports:
      - "9090:9090"
    volumes:
      - ./monitoring/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./monitoring/prometheus/alerts:/etc/prometheus/alerts
      - prometheus-data:/prometheus
    command:
      - "--config.file=/etc/prometheus/prometheus.yml"
      - "--storage.tsdb.retention.time=30d"
      - "--storage.tsdb.retention.size=10GB"
      - "--web.enable-lifecycle"
    networks:
      - monitoring

  grafana:
    image: grafana/grafana:11.4.0
    container_name: grafana
    ports:
      - "3001:3000"
    environment:
      GF_SECURITY_ADMIN_USER: admin
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD:-admin}
      GF_USERS_ALLOW_SIGN_UP: "false"
      GF_AUTH_ANONYMOUS_ENABLED: "false"
    volumes:
      - ./monitoring/grafana/provisioning:/etc/grafana/provisioning
      - grafana-data:/var/lib/grafana
    depends_on:
      - prometheus
    networks:
      - monitoring

  alertmanager:
    image: prom/alertmanager:v0.27.0
    container_name: alertmanager
    ports:
      - "9093:9093"
    volumes:
      - ./monitoring/alertmanager/alertmanager.yml:/etc/alertmanager/alertmanager.yml
    networks:
      - monitoring

  otel-collector:
    image: otel/opentelemetry-collector-contrib:0.112.0
    container_name: otel-collector
    command: ["--config=/etc/otelcol/config.yml"]
    volumes:
      - ./monitoring/otel-collector/config.yml:/etc/otelcol/config.yml
    ports:
      - "4317:4317"
      - "4318:4318"
    networks:
      - monitoring

  nginx-exporter:
    image: nginx/nginx-prometheus-exporter:1.3.0
    container_name: nginx-exporter
    ports:
      - "9113:9113"
    environment:
      NGINX_STATUS: http://frontend:80/stub_status
    depends_on:
      - frontend
    networks:
      - monitoring

volumes:
  prometheus-data:
  grafana-data:

networks:
  monitoring:
    driver: bridge
```

### Prometheus Scrape Configuration

```yaml
# monitoring/prometheus/prometheus.yml
global:
  scrape_interval: 30s
  evaluation_interval: 30s
  external_labels:
    cluster: ${CLUSTER_NAME:-default}
    environment: ${ENV:-production}

rule_files:
  - /etc/prometheus/alerts/*.yml

alerting:
  alertmanagers:
    - static_configs:
        - targets: ["alertmanager:9093"]

scrape_configs:
  - job_name: "backend"
    metrics_path: "/metrics"
    scrape_interval: 15s
    static_configs:
      - targets: ["backend:8080"]
        labels:
          service: "backend"
          team: "platform"

  - job_name: "nginx"
    metrics_path: "/metrics"
    scrape_interval: 15s
    static_configs:
      - targets: ["nginx-exporter:9113"]
        labels:
          service: "frontend"
          team: "platform"

  - job_name: "prometheus"
    static_configs:
      - targets: ["localhost:9090"]

  - job_name: "grafana"
    static_configs:
      - targets: ["grafana:3000"]

  - job_name: "alertmanager"
    static_configs:
      - targets: ["alertmanager:9093"]

  - job_name: "otel-collector"
    static_configs:
      - targets: ["otel-collector:8889"]
```

### Setup Verification Checklist

```
Monitoring Setup Verification
═════════════════════════════

Logging:
  [ ] Backend produces structured JSON logs to stdout
  [ ] JSON logs include trace_id and span_id when trace is active
  [ ] nginx produces JSON access logs
  [ ] Log levels configured correctly per environment

Metrics:
  [ ] Backend /metrics endpoint returns Prometheus format
  [ ] nginx-exporter scrapes nginx stub_status
  [ ] Prometheus scrapes all targets successfully
  [ ] Grafana can query Prometheus datasource

Tracing:
  [ ] Backend sends traces to OTel Collector
  [ ] W3C Trace Context headers propagated through nginx → backend
  [ ] Trace ID appears in structured log entries
  [ ] Jaeger/Tempo can display traces end-to-end

Health Checks:
  [ ] GET /health on frontend returns 200 JSON
  [ ] GET /health on backend returns 200 with details
  [ ] GET /api/v1/health returns application health
  [ ] Docker HEALTHCHECK configured for backend container

Alerting:
  [ ] Alert rules loaded into Prometheus
  [ ] Alertmanager receives and routes alerts
  [ ] Test alert fires and notification is received
  [ ] Alert annotations include runbook_url
```

---

## Command: `/monitor dashboard`

Generate Grafana dashboard JSON configuration.

### Instructions

1. **Determine scope**: Ask which service(s) to create dashboards for. Default: all services.
2. **Determine panels**: Use the RED method for services, USE method for resources, Core Web Vitals for frontend.
3. **Generate the dashboard JSON** following the layout defined in [Dashboard Design](#dashboard-design).
4. **Output** to `monitoring/grafana/dashboards/`.

### Dashboard JSON Template (Service Overview)

```json
{
  "annotations": { "list": [] },
  "editable": true,
  "fiscalYearStartMonth": 0,
  "graphTooltip": 1,
  "id": null,
  "links": [],
  "panels": [
    {
      "title": "Uptime",
      "type": "stat",
      "gridPos": { "h": 4, "w": 6, "x": 0, "y": 0 },
      "targets": [
        {
          "expr": "avg(up{service=\"backend\"})",
          "legendFormat": "Uptime"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "mappings": [
            { "type": "value", "options": { "1": { "text": "UP", "color": "green" }, "0": { "text": "DOWN", "color": "red" } } }
          ],
          "thresholds": { "steps": [{ "color": "red", "value": null }, { "color": "green", "value": 1 }] }
        }
      }
    },
    {
      "title": "Request Rate",
      "type": "timeseries",
      "gridPos": { "h": 4, "w": 6, "x": 6, "y": 0 },
      "targets": [
        {
          "expr": "sum(rate(http_server_requests_seconds_count{service=\"backend\"}[5m]))",
          "legendFormat": "req/s"
        }
      ]
    },
    {
      "title": "Error Rate",
      "type": "gauge",
      "gridPos": { "h": 4, "w": 6, "x": 12, "y": 0 },
      "targets": [
        {
          "expr": "sum(rate(http_server_requests_seconds_count{service=\"backend\",status=~\"5..\"}[5m])) / sum(rate(http_server_requests_seconds_count{service=\"backend\"}[5m]))",
          "legendFormat": "error %"
        }
      ],
      "fieldConfig": {
        "defaults": {
          "unit": "percentunit",
          "thresholds": { "steps": [{ "color": "green", "value": null }, { "color": "yellow", "value": 0.01 }, { "color": "red", "value": 0.05 }] },
          "max": 0.1
        }
      }
    },
    {
      "title": "p95 Latency",
      "type": "timeseries",
      "gridPos": { "h": 4, "w": 6, "x": 18, "y": 0 },
      "targets": [
        {
          "expr": "histogram_quantile(0.95, sum(rate(http_server_requests_seconds_bucket{service=\"backend\"}[5m])) by (le))",
          "legendFormat": "p95"
        }
      ],
      "fieldConfig": {
        "defaults": { "unit": "s" }
      }
    }
  ],
  "schemaVersion": 39,
  "tags": ["service", "red-method"],
  "templating": {
    "list": [
      {
        "name": "service",
        "type": "query",
        "query": "label_values(up, service)",
        "refresh": 2
      }
    ]
  },
  "time": { "from": "now-1h", "to": "now" },
  "title": "Service Overview",
  "uid": "service-overview"
}
```

### Provisioning Configuration

```yaml
# monitoring/grafana/provisioning/dashboards/dashboards.yml
apiVersion: 1
providers:
  - name: "default"
    orgId: 1
    folder: ""
    type: file
    disableDeletion: false
    editable: true
    options:
      path: /var/lib/grafana/dashboards
      foldersFromFilesStructure: true

# monitoring/grafana/provisioning/datasources/datasources.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    isDefault: true
    editable: false
  - name: Loki
    type: loki
    access: proxy
    url: http://loki:3100
    editable: false
  - name: Jaeger
    type: jaeger
    access: proxy
    url: http://jaeger:16686
    editable: false
```

---

## Command: `/monitor alerts`

Generate Prometheus alert rules and Alertmanager routing configuration.

### Instructions

1. **Determine services**: Ask which services need alert rules.
2. **Determine thresholds**: Review SLOs and agree on thresholds per metric.
3. **Generate alert rules** following the alerting strategy above.
4. **Generate Alertmanager routing** based on severity levels.
5. **Output** to `monitoring/prometheus/alerts/` and `monitoring/alertmanager/`.

### Alert Rules Template

```yaml
# monitoring/prometheus/alerts/backend.yml
groups:
  - name: backend.availability
    rules:
      - alert: BackendDown
        expr: up{service="backend"} == 0
        for: 1m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Backend service is down"
          description: "Backend service {{ $labels.instance }} has been down for more than 1 minute."
          runbook_url: "https://runbooks.internal/backend/down"

      - alert: BackendHealthCheckFailing
        expr: probe_success{service="backend"} == 0
        for: 2m
        labels:
          severity: high
          team: platform
        annotations:
          summary: "Backend health check is failing"
          description: "Health check for backend {{ $labels.instance }} has been failing for 2 minutes."
          runbook_url: "https://runbooks.internal/backend/health-check"

  - name: backend.errors
    rules:
      - alert: HighErrorRate
        expr: |
          sum(rate(http_server_requests_seconds_count{service="backend",status=~"5.."}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="backend"}[5m]))
          > 0.05
        for: 5m
        labels:
          severity: high
          team: platform
        annotations:
          summary: "Backend error rate above 5%"
          description: "Backend error rate is {{ $value | humanizePercentage }} (threshold: 5%). Check logs for 5xx errors."
          runbook_url: "https://runbooks.internal/backend/high-error-rate"

      - alert: ElevatedErrorRate
        expr: |
          sum(rate(http_server_requests_seconds_count{service="backend",status=~"5.."}[5m]))
          /
          sum(rate(http_server_requests_seconds_count{service="backend"}[5m]))
          > 0.01
        for: 10m
        labels:
          severity: medium
          team: platform
        annotations:
          summary: "Backend error rate above 1%"
          description: "Backend error rate is {{ $value | humanizePercentage }} (threshold: 1%). Monitor closely."
          runbook_url: "https://runbooks.internal/backend/elevated-error-rate"

  - name: backend.latency
    rules:
      - alert: HighLatencyP95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_server_requests_seconds_bucket{service="backend"}[5m])) by (le)
          ) > 2.0
        for: 5m
        labels:
          severity: high
          team: platform
        annotations:
          summary: "Backend p95 latency above 2 seconds"
          description: "p95 latency is {{ $value }}s (threshold: 2s). Investigate slow endpoints."
          runbook_url: "https://runbooks.internal/backend/high-latency"

      - alert: ElevatedLatencyP95
        expr: |
          histogram_quantile(0.95,
            sum(rate(http_server_requests_seconds_bucket{service="backend"}[5m])) by (le)
          ) > 0.5
        for: 10m
        labels:
          severity: medium
          team: platform
        annotations:
          summary: "Backend p95 latency above 500ms"
          description: "p95 latency is {{ $value }}s (threshold: 500ms). Check resource utilization."
          runbook_url: "https://runbooks.internal/backend/elevated-latency"

  - name: backend.resources
    rules:
      - alert: HighMemoryUsage
        expr: |
          jvm_memory_used_bytes{service="backend",area="heap"}
          /
          jvm_memory_max_bytes{service="backend",area="heap"}
          > 0.90
        for: 10m
        labels:
          severity: high
          team: platform
        annotations:
          summary: "Backend JVM heap usage above 90%"
          description: "Heap usage is {{ $value | humanizePercentage }}. Risk of OOM. Consider increasing heap or investigating memory leak."
          runbook_url: "https://runbooks.internal/backend/high-memory"

      - alert: HighCPUUsage
        expr: system_cpu_usage{service="backend"} > 0.90
        for: 15m
        labels:
          severity: medium
          team: platform
        annotations:
          summary: "Backend CPU usage above 90%"
          description: "CPU usage is {{ $value | humanizePercentage }} for 15 minutes. Consider scaling."
          runbook_url: "https://runbooks.internal/backend/high-cpu"

      - alert: DiskSpaceLow
        expr: |
          (node_filesystem_avail_bytes{mountpoint="/"}
          /
          node_filesystem_size_bytes{mountpoint="/"}) < 0.20
        for: 5m
        labels:
          severity: medium
          team: platform
        annotations:
          summary: "Disk space below 20%"
          description: "Available disk space is {{ $value | humanizePercentage }}. Clean up logs or expand volume."
          runbook_url: "https://runbooks.internal/backend/disk-space"

  - name: frontend.availability
    rules:
      - alert: FrontendDown
        expr: up{service="frontend"} == 0
        for: 2m
        labels:
          severity: critical
          team: platform
        annotations:
          summary: "Frontend (nginx) is down"
          description: "Frontend service {{ $labels.instance }} has been down for 2 minutes."
          runbook_url: "https://runbooks.internal/frontend/down"

      - alert: NginxHighConnectionCount
        expr: nginx_connections_active{service="frontend"} > 10000
        for: 5m
        labels:
          severity: medium
          team: platform
        annotations:
          summary: "Nginx active connections above 10,000"
          description: "Active connections: {{ $value }}. May indicate traffic spike or connection leak."
          runbook_url: "https://runbooks.internal/frontend/high-connections"
```

### Alert Rules Quality Checklist

```
Alert Quality Review
════════════════════

Per alert:
  [ ] Has severity label (critical/high/medium/low)
  [ ] Has team label for routing
  [ ] Has summary annotation (short, searchable)
  [ ] Has description annotation (includes current value via $value)
  [ ] Has runbook_url annotation (links to runbook)
  [ ] Has appropriate `for:` duration (avoids noise from transient spikes)
  [ ] Threshold is realistic and based on SLOs
  [ ] Alert has been tested (can fire with a manual trigger)

Overall:
  [ ] Coverage: every SLO has a corresponding alert
  [ ] No overlap: alerts don't duplicate notifications
  [ ] Routing: every severity level has a defined receiver
  [ ] Inhibition: P1 alerts suppress related P2/P3 alerts where applicable
  [ ] Silences: documented process for planned maintenance windows
```

---

## Command: `/monitor runbook`

Generate an operational runbook for a service or incident type.

### Instructions

1. **Determine scope**: Ask which service or failure mode to create a runbook for.
2. **Gather context**: Review existing alerts, dashboards, and known failure modes.
3. **Generate the runbook** following the template below.
4. **Output** to `docs/runbooks/<service>-<topic>.md`.

### Runbook Template

```markdown
# Runbook: [Service] — [Failure Mode]

**Service:** [service name]
**Owner:** [team name]
**Last Reviewed:** YYYY-MM-DD
**Dashboard:** [link to Grafana dashboard]
**Alert:** [alert name that triggers this runbook]

## Overview

[1-2 sentences describing what this runbook covers and when it's triggered.]

## Symptoms

- [Observable symptom 1 — e.g., "Error rate > 5% on /api/v1/users"]
- [Observable symptom 2 — e.g., "p95 latency > 2 seconds"]
- [Observable symptom 3 — e.g., "Health check returning 503"]

## Investigation Steps

### Step 1: Check Service Health

```bash
curl -s https://[service]/health | jq .
curl -s https://[service]/api/v1/health | jq .
```

Expected: `{"status":"UP",...}`

### Step 2: Check Recent Logs

```bash
# Search for ERROR logs in the last hour
# Replace with your log query tool (Loki, ELK, CloudWatch, etc.)
# Loki example:
logcli query '{service="[service]"} |= "ERROR"' --limit=50 --since=1h
```

### Step 3: Check Metrics

Open the dashboard: [link]

Key panels to check:
- Request rate (is it spiking?)
- Error rate (which endpoints?)
- Latency (which endpoints are slow?)
- Resource utilization (CPU, memory, disk)

### Step 4: Check Recent Changes

```bash
git log --oneline --since="4 hours ago"
kubectl rollout history deployment/[service]
```

### Step 5: Check Dependencies

```bash
# Database connectivity
curl -s https://[service]/health | jq '.details.jdbc'

# External API availability
curl -s -o /dev/null -w "%{http_code}" https://external-api.example.com/health
```

## Mitigation Actions

### Action A: [Most Common Mitigation]

When: [condition that warrants this action]

```bash
# Commands to execute
kubectl rollout undo deployment/[service]
```

Verify: [how to confirm it worked]

### Action B: [Scale Out]

When: Resource exhaustion (high CPU/memory)

```bash
kubectl scale deployment/[service] --replicas=[N]
```

Verify: [how to confirm it worked]

### Action C: [Feature Flag / Circuit Breaker]

When: Specific feature causing errors

```bash
# Disable the problematic feature
curl -X PATCH https://config-service/flags/[feature] -d '{"enabled":false}'
```

Verify: [how to confirm it worked]

## Escalation

If none of the mitigation actions resolve the issue:

1. **Escalate to:** [team or individual]
2. **Contact via:** [Slack channel, phone, PagerDuty escalation]
3. **Provide:** Incident timeline, investigation findings, attempted mitigations

## Post-Incident

After resolution:
- [ ] Confirm metrics returned to baseline
- [ ] Monitor for 30 minutes
- [ ] Create post-mortem document (use `/monitor incident`)
- [ ] Update this runbook with any new findings
```

---

## Command: `/monitor incident`

Walk through the structured incident response process.

### Instructions

1. **Acknowledge the incident**: Record start time, reporter, initial symptoms.
2. **Classify severity**: Use the triage decision tree from [Incident Response Process](#incident-response-process).
3. **Guide investigation**: Walk through each investigation step from the relevant runbook.
4. **Record mitigation**: Document what was done and when.
5. **Confirm resolution**: Verify metrics returned to baseline.
6. **Generate post-mortem**: Produce a post-mortem document from the template.

### Incident Timeline Template

```markdown
# Incident: [INCIDENT-ID]

**Opened:** YYYY-MM-DD HH:MM UTC
**Closed:** YYYY-MM-DD HH:MM UTC
**Duration:** X hours Y minutes
**Severity:** P1/P2/P3/P4
**Commander:** [Name]
**On-call:** [Name]

## Timeline

| Time (UTC) | Event | Action | By |
|------------|-------|--------|----|
| HH:MM | Alert triggered: [alert name] | — | System |
| HH:MM | On-call acknowledged | Begin investigation | [Name] |
| HH:MM | Severity classified: P[X] | Notify stakeholders | [Name] |
| HH:MM | Incident channel opened: #inc-[ID] | — | [Name] |
| HH:MM | Root cause hypothesis: [description] | — | [Name] |
| HH:MM | Mitigation: [action taken] | Apply fix | [Name] |
| HH:MM | Metrics returning to baseline | Monitor | [Name] |
| HH:MM | Incident resolved | Close channel | [Name] |

## Impact Assessment

- **Users affected:** [count or percentage]
- **Requests failed:** [count from metrics]
- **Revenue impact:** [if applicable]
- **Data impact:** [any data loss or corruption]

## Root Cause

[Technical explanation of what happened and why]

## Actions Taken

1. [Action 1 with timestamp]
2. [Action 2 with timestamp]
3. [Action 3 with timestamp]

## Follow-up Actions

| Action | Owner | Due Date | Priority |
|--------|-------|----------|----------|
| [Action 1] | @owner | YYYY-MM-DD | P2 |
| [Action 2] | @owner | YYYY-MM-DD | P3 |
```

### Incident Response Checklist (Quick Reference)

```
INCIDENT RESPONSE CHECKLIST
═══════════════════════════

IMMEDIATE (0-5 min):
  [ ] Acknowledge alert
  [ ] Classify severity (P1-P4)
  [ ] Open incident channel (P1/P2)
  [ ] Start incident timeline
  [ ] Notify stakeholders if P1/P2

INVESTIGATE (5-30 min):
  [ ] Check service health endpoints
  [ ] Check dashboards for anomalies
  [ ] Search logs for errors (use trace_id if available)
  [ ] Check traces for slow/failed requests
  [ ] Check recent deployments / changes
  [ ] Form root cause hypothesis

MITIGATE (30-60 min):
  [ ] Execute mitigation from runbook
  [ ] Verify mitigation is taking effect
  [ ] Communicate status to stakeholders
  [ ] Monitor for regression

RESOLVE (60+ min):
  [ ] Confirm metrics at baseline for 30+ minutes
  [ ] Communicate resolution
  [ ] Close incident channel
  [ ] Schedule post-mortem (P1/P2: within 48 hours)

POST-MORTEM:
  [ ] Write incident summary
  [ ] Document timeline
  [ ] Identify root cause
  [ ] List contributing factors
  [ ] Document what went well
  [ ] Document what to improve
  [ ] Create action items with owners and due dates
  [ ] Review with team
  [ ] Update runbook
```

---

## Command: `/monitor health`

Verify all health checks and observability endpoints are functioning.

### Instructions

1. **Run all health check endpoints** against the configured targets.
2. **Verify Prometheus scrape targets** are all UP.
3. **Verify trace pipeline** by generating a test trace.
4. **Verify alert pipeline** by checking Alertmanager status.
5. **Report** a comprehensive health status.

### Health Check Script

```bash
#!/usr/bin/env bash
# monitor-health-check.sh
set -euo pipefail

PASS=0
FAIL=0
WARN=0

check() {
  local label="$1" url="$2" expected_status="${3:-200}"
  local start elapsed

  start=$(date +%s%N)
  status=$(curl -s -o /dev/null -w "%{http_code}" --max-time 5 "$url" 2>/dev/null) || status="000"
  elapsed=$(( ($(date +%s%N) - start) / 1000000 ))

  if [ "$status" = "$expected_status" ]; then
    echo "  ✅ $label — HTTP $status (${elapsed}ms)"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $label — HTTP $status (expected $expected_status, ${elapsed}ms)"
    FAIL=$((FAIL + 1))
  fi
}

echo "╔══════════════════════════════════════════════════════════╗"
echo "║         Monitoring Health Check Report                  ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

FRONTEND_URL="${FRONTEND_URL:-http://localhost:80}"
BACKEND_URL="${BACKEND_URL:-http://localhost:8080}"
PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
GRAFANA_URL="${GRAFANA_URL:-http://localhost:3001}"
ALERTMANAGER_URL="${ALERTMANAGER_URL:-http://localhost:9093}"

echo "Frontend (nginx):"
check "Health endpoint" "$FRONTEND_URL/health"
echo ""

echo "Backend (Micronaut):"
check "API health" "$BACKEND_URL/api/v1/health"
check "Management health" "$BACKEND_URL/health"
check "Metrics endpoint" "$BACKEND_URL/metrics"
echo ""

echo "Monitoring Infrastructure:"
check "Prometheus" "$PROMETHEUS_URL/-/healthy"
check "Grafana" "$GRAFANA_URL/api/health"
check "Alertmanager" "$ALERTMANAGER_URL/-/healthy"
echo ""

echo "Prometheus Targets:"
targets=$(curl -s "$PROMETHEUS_URL/api/v1/targets" 2>/dev/null | jq -r '.data.activeTargets[] | "\(.labels.service // .labels.job) \(.health)"' 2>/dev/null || echo "Unable to query targets")
echo "$targets" | while read -r service health; do
  if [ "$health" = "up" ]; then
    echo "  ✅ $service — UP"
    PASS=$((PASS + 1))
  else
    echo "  ❌ $service — $health"
    FAIL=$((FAIL + 1))
  fi
done
echo ""

echo "╔══════════════════════════════════════════════════════════╗"
echo "║  Summary: $PASS passed, $FAIL failed, $WARN warnings"
echo "╚══════════════════════════════════════════════════════════╝"

[ "$FAIL" -eq 0 ] || exit 1
```

---

## SLO/SLI Framework

### Definitions

| Term | Definition |
|------|-----------|
| **SLI** (Service Level Indicator) | A quantitative measure of service behavior (e.g., request latency, error rate) |
| **SLO** (Service Level Objective) | A target value for an SLI (e.g., p95 latency < 500ms) |
| **SLA** (Service Level Agreement) | A contractual commitment based on SLOs (with consequences for breach) |
| **Error Budget** | 1 - SLO; the acceptable amount of unreliability in a time window |

### Recommended SLOs

| SLI | SLO | Error Budget (30d) | Alert Threshold |
|-----|-----|--------------------|-----------------|
| Availability (successful requests) | 99.9% | 43.2 minutes | Alert at 50% budget consumed |
| Latency (p95 < 500ms) | 99.5% | 216 minutes above 500ms | Alert at 50% budget consumed |
| Error rate (5xx responses) | < 0.1% | 43.2 minutes at > 0.1% | Alert when rate > 0.1% for 5m |

### Error Budget Burn Rate Alerting

```yaml
# Fast burn — 2% error budget consumed in 1 hour
- alert: ErrorBudgetBurningFast
  expr: |
    (
      1 - (
        sum(rate(http_server_requests_seconds_count{service="backend",status!~"5.."}[1h]))
        /
        sum(rate(http_server_requests_seconds_count{service="backend"}[1h]))
      )
    )
    >
    (1 - 0.999) * 14.4
  for: 5m
  labels:
    severity: high
  annotations:
    summary: "Error budget burning too fast"
    description: "Consuming error budget at 14.4x normal rate. SLO breach likely within hours."

# Slow burn — 5% error budget consumed in 3 days
- alert: ErrorBudgetBurningSlow
  expr: |
    (
      1 - (
        sum(rate(http_server_requests_seconds_count{service="backend",status!~"5.."}[3d]))
        /
        sum(rate(http_server_requests_seconds_count{service="backend"}[3d]))
      )
    )
    >
    (1 - 0.999) * 1.0
  for: 1h
  labels:
    severity: medium
  annotations:
    summary: "Error budget slowly depleting"
    description: "Consuming error budget at 1x rate over 3 days. Monitor closely."
```

---

## Workflow

When invoked, follow this decision tree:

```
/monitor [command]
        │
        ├── setup ────────► Determine scope (frontend/backend/both)
        │                     │
        │                     ├── Generate logback.xml (structured JSON + trace correlation)
        │                     ├── Generate application.yml (health, metrics, tracing)
        │                     ├── Generate nginx.conf additions (JSON logs, health, OTel headers)
        │                     ├── Generate docker-compose.monitoring.yml
        │                     ├── Generate prometheus.yml (scrape config)
        │                     └── Verify connectivity between all components
        │
        ├── dashboard ─────► Determine services to dashboard
        │                     │
        │                     ├── RED method panels (Rate/Errors/Duration)
        │                     ├── USE method panels (CPU/Memory/Disk/Connections)
        │                     ├── Core Web Vitals panels (LCP/INP/CLS)
        │                     ├── Top slowest endpoints table
        │                     └── Output Grafana dashboard JSON to monitoring/grafana/dashboards/
        │
        ├── alerts ────────► Determine services and SLOs
        │                     │
        │                     ├── Generate availability alerts (service down)
        │                     ├── Generate error rate alerts (5xx thresholds)
        │                     ├── Generate latency alerts (p95/p99 thresholds)
        │                     ├── Generate resource alerts (CPU/memory/disk)
        │                     ├── Generate error budget burn rate alerts
        │                     ├── Generate Alertmanager routing (by severity)
        │                     └── Output to monitoring/prometheus/alerts/ + monitoring/alertmanager/
        │
        ├── runbook ───────► Determine service and failure mode
        │                     │
        │                     ├── Gather context (alerts, dashboards, known issues)
        │                     ├── Generate investigation steps
        │                     ├── Generate mitigation actions
        │                     ├── Generate escalation path
        │                     └── Output to docs/runbooks/<service>-<topic>.md
        │
        ├── incident ──────► Begin incident response process
        │                     │
        │                     ├── Acknowledge and classify severity
        │                     ├── Guide investigation (follow runbook)
        │                     ├── Record mitigation actions
        │                     ├── Confirm resolution
        │                     └── Generate post-mortem document
        │
        └── health ────────► Run comprehensive health verification
                              │
                              ├── Check frontend /health endpoint
                              ├── Check backend /health and /api/v1/health
                              ├── Check backend /metrics endpoint
                              ├── Check Prometheus targets (all UP?)
                              ├── Check Grafana health
                              ├── Check Alertmanager health
                              └── Generate health report
```

---

## Reference Files

| Reference | Content |
|-----------|---------|
| `references/logging-configuration.md` | Detailed Logback, nginx log format, and Loki shipping configuration |
| `references/metrics-configuration.md` | Micrometer registry setup, custom metrics, Prometheus scrape tuning |
| `references/alert-rules-template.md` | Complete alert rule library for backend, frontend, and infrastructure |
| `references/runbook-template.md` | Runbook template with investigation steps and mitigation actions |
| `references/incident-post-mortem-template.md` | Post-mortem document template with timeline, root cause, and action items |

---

## Rules

1. **Every alert must be actionable** — If there is no clear remediation, do not create the alert.
2. **Correlate across pillars** — Logs, metrics, and traces must share `trace_id` for cross-referencing.
3. **Structure all logs as JSON** — Parseable, searchable, and machine-readable. No free-form text in production.
4. **Health checks must be lightweight** — < 100ms response time, no external dependency calls that could cascade.
5. **Dashboards answer questions** — Design each panel to answer a specific operational question.
6. **Runbooks stay current** — After every P1/P2 incident, update the relevant runbook.
7. **Alert fatigue is real** — Prefer few high-quality alerts over many noisy ones. Tune aggressively.
8. **Blast-radius scoping** — Labels on metrics and alerts must include `service`, `environment`, and `team`.
9. **Test the alert pipeline** — Periodically trigger a test alert to verify end-to-end delivery.
10. **Post-mortems are blameless** — Focus on system failures, not individual mistakes.
