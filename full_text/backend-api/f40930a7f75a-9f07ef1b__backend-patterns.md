---
name: backend-patterns
description: Backend architecture patterns, API design, database optimization, and server-side best practices for Node.js, Express, and Next.js API routes.
metadata:
  origin: AgentPowerHouse - APH
---

# Backend Development Patterns

Architecture patterns and best practices for scalable Spring Boot applications consumed by React frontends.

---

## When to Activate

- Designing REST API endpoints in Spring Boot
- Implementing repository, service, or controller layers
- Optimizing database queries (N+1, indexing, connection pooling)
- Adding caching (Redis, Spring Cache, HTTP cache headers)
- Setting up background jobs or async processing
- Structuring error handling and validation for APIs
- Building middleware (auth, logging, rate limiting)

---

## API Design Patterns

### RESTful API Structure

```java
// Resource-based URLs with Spring MVC
@RestController
@RequestMapping("/api/v1/markets")
public class MarketController {

    @GetMapping              // GET /api/v1/markets
    @GetMapping("/{id}")     // GET /api/v1/markets/{id}
    @PostMapping             // POST /api/v1/markets
    @PutMapping("/{id}")     // PUT /api/v1/markets/{id}
    @PatchMapping("/{id}")   // PATCH /api/v1/markets/{id}
    @DeleteMapping("/{id}")  // DELETE /api/v1/markets/{id}
}

// Query parameters for filtering, sorting, pagination
// GET /api/v1/markets?status=active&sort=volume,desc&size=20&page=0
```

### Repository Pattern

Spring Data JPA generates the implementation; you define the interface.

```java
// Domain model
@Entity
@Table(name = "markets")
public class Market {
    @Id @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;
    private String name;
    private String status;
    private BigDecimal volume;
    private LocalDateTime createdAt;
    // getters, setters, or use Lombok @Data
}

// Repository interface — Spring Data provides the implementation
public interface MarketRepository extends JpaRepository<Market, UUID>,
        JpaSpecificationExecutor<Market> {

    List<Market> findByStatus(String status);

    @Query("SELECT m FROM Market m WHERE m.status = :status ORDER BY m.volume DESC")
    Page<Market> findActiveByVolume(@Param("status") String status, Pageable pageable);

    // Projection query — only the columns you need
    @Query("SELECT m.id AS id, m.name AS name, m.status AS status, m.volume AS volume " +
           "FROM Market m WHERE m.status = :status")
    Page<MarketSummary> findSummariesByStatus(@Param("status") String status, Pageable pageable);
}

// Projection interface (no extra class needed)
public interface MarketSummary {
    UUID getId();
    String getName();
    String getStatus();
    BigDecimal getVolume();
}
```

### Service Layer Pattern

```java
// Business logic separated from data access
@Service
@RequiredArgsConstructor
@Transactional(readOnly = true)   // default: read-only; override per method
public class MarketService {

    private final MarketRepository marketRepo;
    private final EmbeddingService embeddingService;

    public Page<MarketDto> listMarkets(MarketFilters filters, Pageable pageable) {
        Specification<Market> spec = Specification
            .where(MarketSpec.hasStatus(filters.status()))
            .and(MarketSpec.volumeAtLeast(filters.minVolume()));

        return marketRepo.findAll(spec, pageable).map(MarketDto::from);
    }

    public List<MarketDto> searchMarkets(String query, int limit) {
        float[] embedding = embeddingService.embed(query);

        // Vector search returns IDs + scores
        List<VectorResult> results = embeddingService.search(embedding, limit);
        List<UUID> ids = results.stream().map(VectorResult::id).toList();

        // Batch fetch by IDs (1 query)
        Map<UUID, Market> marketMap = marketRepo.findAllById(ids)
            .stream()
            .collect(Collectors.toMap(Market::getId, Function.identity()));

        // Reassemble in score order
        return results.stream()
            .map(r -> marketMap.get(r.id()))
            .filter(Objects::nonNull)
            .map(MarketDto::from)
            .toList();
    }

    @Transactional   // write operation — overrides class-level readOnly
    public MarketDto create(CreateMarketRequest request) {
        if (marketRepo.existsByName(request.name())) {
            throw new DuplicateResourceException("Market name already exists: " + request.name());
        }
        Market market = new Market(request.name(), request.status());
        return MarketDto.from(marketRepo.save(market));
    }
}
```

### Middleware: Filters and Interceptors

Spring has two hook points: `Filter` (servlet level) and `HandlerInterceptor` (MVC level).

```java
// Filter — runs for every request, including static resources
@Component
@Order(1)
public class RequestIdFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {

        String requestId = Optional.ofNullable(req.getHeader("X-Request-Id"))
            .orElse(UUID.randomUUID().toString());

        MDC.put("requestId", requestId);        // attach to log context
        res.addHeader("X-Request-Id", requestId);

        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();
        }
    }
}

// HandlerInterceptor — runs only for controller routes
@Component
@RequiredArgsConstructor
public class AuthInterceptor implements HandlerInterceptor {

    private final JwtService jwtService;

    @Override
    public boolean preHandle(HttpServletRequest req,
            HttpServletResponse res, Object handler) {

        if (handler instanceof HandlerMethod hm &&
                hm.hasMethodAnnotation(PublicEndpoint.class)) {
            return true;   // skip auth for @PublicEndpoint methods
        }

        String token = Optional.ofNullable(req.getHeader("Authorization"))
            .map(h -> h.replace("Bearer ", ""))
            .orElse(null);

        if (token == null) {
            res.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return false;
        }

        try {
            UserPrincipal principal = jwtService.verify(token);
            req.setAttribute("principal", principal);
            return true;
        } catch (JwtException e) {
            res.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            return false;
        }
    }
}

// Register the interceptor
@Configuration
@RequiredArgsConstructor
public class WebConfig implements WebMvcConfigurer {

    private final AuthInterceptor authInterceptor;

    @Override
    public void addInterceptors(InterceptorRegistry registry) {
        registry.addInterceptor(authInterceptor)
                .addPathPatterns("/api/**")
                .excludePathPatterns("/api/v1/auth/**");
    }
}
```

---

## Database Patterns

### Query Optimization — Projections over `select *`

```java
// BAD: fetches every column and maps to full entity
List<Market> all = marketRepository.findAll();

// GOOD: projection — only id, name, status, volume reach the JDBC layer
Page<MarketSummary> summaries = marketRepository
    .findSummariesByStatus("active", pageable);

// GOOD: native query with explicit column list when JPQL isn't enough
@Query(value = "SELECT id, name, status, volume FROM markets WHERE status = :status",
       nativeQuery = true)
List<MarketProjection> findActiveNative(@Param("status") String status);
```

### N+1 Query Prevention

```java
// BAD: N+1 — one query for markets, then one per market for creator
List<Market> markets = marketRepository.findAll();
markets.forEach(m -> m.getCreator().getName()); // triggers N lazy loads

// GOOD option 1: JPQL JOIN FETCH
@Query("SELECT m FROM Market m JOIN FETCH m.creator WHERE m.status = :status")
List<Market> findWithCreator(@Param("status") String status);

// GOOD option 2: @EntityGraph (no query string needed)
@EntityGraph(attributePaths = {"creator", "category"})
List<Market> findByStatus(String status);

// GOOD option 3: batch-fetch by IDs (when joining would cause cartesian products)
List<UUID> ids = marketRepository.findIdsByStatus("active");
Map<UUID, User> creatorMap = userRepository.findAllById(creatorIds)
    .stream()
    .collect(Collectors.toMap(User::getId, Function.identity()));
```

> **Hibernate tip:** enable `spring.jpa.properties.hibernate.format_sql=true` and `logging.level.org.hibernate.SQL=DEBUG` in development to catch N+1 issues early. Use [Hypersistence Optimizer](https://github.com/vladmihalcea/hypersistence-optimizer) or [Datasource Proxy](https://github.com/ttddyy/datasource-proxy) in CI.

### Transaction Pattern

```java
// Simple service-level transaction
@Service
public class MarketService {

    @Transactional
    public MarketWithPosition createMarketWithPosition(
            CreateMarketRequest marketReq,
            CreatePositionRequest positionReq) {

        Market market = marketRepository.save(new Market(marketReq));
        Position position = positionRepository.save(new Position(market, positionReq));
        // If either save throws, the whole transaction rolls back automatically
        return new MarketWithPosition(market, position);
    }
}

// Explicit rollback rules
@Transactional(rollbackOn = Exception.class,
               noRollbackOn = OptimisticLockException.class)
public void processMarket(UUID id) { /* ... */ }

// Programmatic transaction (when declarative isn't granular enough)
@Service
@RequiredArgsConstructor
public class BulkService {

    private final TransactionTemplate txTemplate;

    public void bulkCreate(List<CreateMarketRequest> requests) {
        requests.forEach(req ->
            txTemplate.executeWithoutResult(status -> {
                try {
                    marketRepository.save(new Market(req));
                } catch (DataIntegrityViolationException e) {
                    status.setRollbackOnly();
                    log.warn("Skipped duplicate market: {}", req.name());
                }
            })
        );
    }
}
```

### Connection Pool Configuration

```yaml
# application.yml — HikariCP (Spring Boot default)
spring:
  datasource:
    url: jdbc:postgresql://localhost:5432/mydb
    username: ${DB_USERNAME}
    password: ${DB_PASSWORD}
    hikari:
      maximum-pool-size: 20          # tune to (core_count * 2) + effective_spindle_count
      minimum-idle: 5
      connection-timeout: 30000      # ms — fail fast rather than queue indefinitely
      idle-timeout: 600000
      max-lifetime: 1800000
      leak-detection-threshold: 60000
```

---

## Caching Strategies

### Spring Cache Abstraction (Redis-backed)

```java
// Enable caching
@SpringBootApplication
@EnableCaching
public class Application { /* ... */ }
```

```yaml
# application.yml
spring:
  cache:
    type: redis
  data:
    redis:
      host: ${REDIS_HOST:localhost}
      port: 6379
      timeout: 2000ms
```

```java
// Configure TTLs per cache
@Configuration
public class CacheConfig {

    @Bean
    public RedisCacheManagerBuilderCustomizer redisCacheCustomizer() {
        return builder -> builder
            .withCacheConfiguration("markets",
                RedisCacheConfiguration.defaultCacheConfig()
                    .entryTtl(Duration.ofMinutes(5))
                    .disableCachingNullValues())
            .withCacheConfiguration("market-summaries",
                RedisCacheConfiguration.defaultCacheConfig()
                    .entryTtl(Duration.ofMinutes(10)));
    }
}

// Apply caching at the service layer — not the controller or repository
@Service
public class MarketService {

    @Cacheable(value = "markets", key = "#id")
    public MarketDto findById(UUID id) {
        return marketRepository.findById(id)
            .map(MarketDto::from)
            .orElseThrow(() -> new ResourceNotFoundException("Market not found: " + id));
    }

    @CacheEvict(value = "markets", key = "#id")
    @Transactional
    public MarketDto update(UUID id, UpdateMarketRequest request) {
        Market market = marketRepository.findById(id)
            .orElseThrow(() -> new ResourceNotFoundException("Market not found: " + id));
        market.apply(request);
        return MarketDto.from(marketRepository.save(market));
    }

    @CacheEvict(value = "markets", allEntries = true)
    @Transactional
    public void delete(UUID id) {
        marketRepository.deleteById(id);
    }
}
```

### Cache-Aside Pattern (Manual / Redis Template)

```java
@Service
@RequiredArgsConstructor
public class MarketCacheService {

    private final MarketRepository marketRepository;
    private final RedisTemplate<String, MarketDto> redisTemplate;

    private static final Duration TTL = Duration.ofMinutes(5);

    public MarketDto getMarket(UUID id) {
        String key = "market:" + id;

        // 1. Try cache
        MarketDto cached = redisTemplate.opsForValue().get(key);
        if (cached != null) return cached;

        // 2. Cache miss — hit the database
        MarketDto dto = marketRepository.findById(id)
            .map(MarketDto::from)
            .orElseThrow(() -> new ResourceNotFoundException("Market not found: " + id));

        // 3. Populate cache
        redisTemplate.opsForValue().set(key, dto, TTL);
        return dto;
    }

    public void invalidate(UUID id) {
        redisTemplate.delete("market:" + id);
    }
}
```

---

## Error Handling Patterns

### Custom Exception Hierarchy

```java
// Base exception — marks it as a known, operational error
public abstract class ApiException extends RuntimeException {
    private final HttpStatus status;
    private final String code;

    protected ApiException(HttpStatus status, String code, String message) {
        super(message);
        this.status = status;
        this.code = code;
    }

    public HttpStatus getStatus() { return status; }
    public String getCode() { return code; }
}

public class ResourceNotFoundException extends ApiException {
    public ResourceNotFoundException(String message) {
        super(HttpStatus.NOT_FOUND, "not_found", message);
    }
}

public class DuplicateResourceException extends ApiException {
    public DuplicateResourceException(String message) {
        super(HttpStatus.CONFLICT, "conflict", message);
    }
}

public class ForbiddenException extends ApiException {
    public ForbiddenException(String message) {
        super(HttpStatus.FORBIDDEN, "forbidden", message);
    }
}
```

### Centralized Error Handler

```java
@RestControllerAdvice
@Slf4j
public class GlobalExceptionHandler {

    // Bean Validation failures (@Valid)
    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<ErrorResponse> handleValidation(
            MethodArgumentNotValidException ex) {

        List<FieldError> details = ex.getBindingResult().getFieldErrors().stream()
            .map(e -> new FieldError(e.getField(), e.getDefaultMessage(), "invalid_value"))
            .toList();

        return ResponseEntity.unprocessableEntity()
            .body(ErrorResponse.of("validation_error", "Request validation failed", details));
    }

    // Constraint violations (e.g., @Validated on service methods)
    @ExceptionHandler(ConstraintViolationException.class)
    public ResponseEntity<ErrorResponse> handleConstraintViolation(
            ConstraintViolationException ex) {

        List<FieldError> details = ex.getConstraintViolations().stream()
            .map(v -> new FieldError(
                v.getPropertyPath().toString(),
                v.getMessage(),
                "constraint_violation"))
            .toList();

        return ResponseEntity.unprocessableEntity()
            .body(ErrorResponse.of("validation_error", "Constraint violation", details));
    }

    // All operational exceptions
    @ExceptionHandler(ApiException.class)
    public ResponseEntity<ErrorResponse> handleApiException(ApiException ex) {
        return ResponseEntity.status(ex.getStatus())
            .body(ErrorResponse.of(ex.getCode(), ex.getMessage()));
    }

    // Malformed JSON / type mismatch
    @ExceptionHandler(HttpMessageNotReadableException.class)
    public ResponseEntity<ErrorResponse> handleBadJson(
            HttpMessageNotReadableException ex) {
        return ResponseEntity.badRequest()
            .body(ErrorResponse.of("invalid_json", "Malformed request body"));
    }

    // Optimistic lock conflicts
    @ExceptionHandler(OptimisticLockingFailureException.class)
    public ResponseEntity<ErrorResponse> handleOptimisticLock(
            OptimisticLockingFailureException ex) {
        return ResponseEntity.status(HttpStatus.CONFLICT)
            .body(ErrorResponse.of("conflict", "Resource was modified by another request. Retry."));
    }

    // Catch-all — never expose internal details
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleUnexpected(Exception ex) {
        log.error("Unexpected error", ex);
        return ResponseEntity.internalServerError()
            .body(ErrorResponse.of("internal_error", "An unexpected error occurred"));
    }
}
```

### Retry with Exponential Backoff — Spring Retry

```java
// Add spring-retry + spring-aspects to pom.xml, enable on the app class
@SpringBootApplication
@EnableRetry
public class Application { /* ... */ }

// Annotate the operation to retry
@Service
public class EmbeddingService {

    @Retryable(
        retryFor = { HttpServerErrorException.class, ResourceAccessException.class },
        maxAttempts = 3,
        backoff = @Backoff(delay = 1000, multiplier = 2)   // 1s, 2s, 4s
    )
    public float[] embed(String text) {
        return callExternalEmbeddingApi(text);
    }

    @Recover
    public float[] embedFallback(Exception ex, String text) {
        log.error("Embedding failed after retries for text: {}", text, ex);
        throw new ServiceUnavailableException("Embedding service unavailable");
    }
}

// Programmatic retry (when annotation isn't flexible enough)
@Bean
public RetryTemplate retryTemplate() {
    return RetryTemplate.builder()
        .maxAttempts(3)
        .exponentialBackoff(1000, 2, 8000)
        .retryOn(HttpServerErrorException.class)
        .build();
}

// Usage
retryTemplate.execute(ctx -> embeddingClient.embed(text));
```

---

## Authentication & Authorization

### JWT with Spring Security

```java
// JWT service
@Service
public class JwtService {

    @Value("${app.jwt.secret}")
    private String secret;

    @Value("${app.jwt.expiration-ms:3600000}")
    private long expirationMs;

    public String generate(UserPrincipal principal) {
        return Jwts.builder()
            .subject(principal.id().toString())
            .claim("email", principal.email())
            .claim("role", principal.role().name())
            .issuedAt(new Date())
            .expiration(new Date(System.currentTimeMillis() + expirationMs))
            .signWith(getKey())
            .compact();
    }

    public UserPrincipal verify(String token) {
        Claims claims = Jwts.parser()
            .verifyWith(getKey())
            .build()
            .parseSignedClaims(token)
            .getPayload();

        return new UserPrincipal(
            UUID.fromString(claims.getSubject()),
            claims.get("email", String.class),
            Role.valueOf(claims.get("role", String.class))
        );
    }

    private SecretKey getKey() {
        return Keys.hmacShaKeyFor(Decoders.BASE64.decode(secret));
    }
}

// JWT filter
@Component
@RequiredArgsConstructor
public class JwtAuthFilter extends OncePerRequestFilter {

    private final JwtService jwtService;
    private final UserDetailsService userDetailsService;

    @Override
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {

        String authHeader = req.getHeader("Authorization");
        if (authHeader == null || !authHeader.startsWith("Bearer ")) {
            chain.doFilter(req, res);
            return;
        }

        try {
            String token = authHeader.substring(7);
            UserPrincipal principal = jwtService.verify(token);

            UsernamePasswordAuthenticationToken auth =
                new UsernamePasswordAuthenticationToken(
                    principal, null,
                    List.of(new SimpleGrantedAuthority("ROLE_" + principal.role().name())));

            SecurityContextHolder.getContext().setAuthentication(auth);
        } catch (JwtException e) {
            res.setStatus(HttpServletResponse.SC_UNAUTHORIZED);
            res.getWriter().write("{\"error\":{\"code\":\"invalid_token\",\"message\":\"Invalid or expired token\"}}");
            return;
        }

        chain.doFilter(req, res);
    }
}
```

### Role-Based Access Control

```java
// Enum-based roles
public enum Role { ADMIN, MODERATOR, USER }

// Method security — enable once in a @Configuration
@Configuration
@EnableMethodSecurity
public class SecurityConfig { /* ... */ }

// Controller annotations
@RestController
@RequestMapping("/api/v1/markets")
public class MarketController {

    @GetMapping          // any authenticated user
    public Page<MarketDto> list(Pageable pageable) { /* ... */ }

    @PostMapping         // any authenticated user
    public ResponseEntity<MarketDto> create(@Valid @RequestBody CreateMarketRequest req) { /* ... */ }

    @DeleteMapping("/{id}")
    @PreAuthorize("hasRole('ADMIN')")   // admin only
    public ResponseEntity<Void> delete(@PathVariable UUID id) { /* ... */ }

    @PatchMapping("/{id}/resolve")
    @PreAuthorize("hasAnyRole('ADMIN', 'MODERATOR')")
    public ResponseEntity<MarketDto> resolve(@PathVariable UUID id) { /* ... */ }
}

// Ownership check in service layer (finer-grained than annotations)
@Service
public class MarketService {

    @Transactional
    public void delete(UUID marketId, UserPrincipal principal) {
        Market market = marketRepository.findById(marketId)
            .orElseThrow(() -> new ResourceNotFoundException("Market not found: " + marketId));

        boolean isOwner = market.getCreatorId().equals(principal.id());
        boolean isAdmin = principal.role() == Role.ADMIN;

        if (!isOwner && !isAdmin) {
            throw new ForbiddenException("You do not have permission to delete this market");
        }

        marketRepository.delete(market);
    }
}
```

---

## Rate Limiting

Rate limiting must use a shared store such as Redis, a gateway, or the platform's native limiter. Do not use per-process in-memory counters for production: they reset on deploy, split across replicas, and fail open in multi-instance or serverless environments.

```java
// Bucket4j with Redis (see api-design doc for full implementation)
@Component
@RequiredArgsConstructor
public class RateLimitFilter extends OncePerRequestFilter {

    private final BucketRepository bucketRepository;  // Redis-backed

    private static final Map<String, BandwidthDefinition> TIERS = Map.of(
        "anonymous",     Bandwidth.classic(30,  Refill.intervally(30,  Duration.ofMinutes(1))),
        "authenticated", Bandwidth.classic(100, Refill.intervally(100, Duration.ofMinutes(1))),
        "premium",       Bandwidth.classic(1000,Refill.intervally(1000,Duration.ofMinutes(1)))
    );

    @Override
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {

        String tier = resolveTier(req);
        String key  = resolveKey(req, tier);
        Bucket bucket = bucketRepository.getOrCreate(key, TIERS.get(tier));

        ConsumptionProbe probe = bucket.tryConsumeAndReturnRemaining(1);
        res.addHeader("X-RateLimit-Remaining", String.valueOf(probe.getRemainingTokens()));

        if (!probe.isConsumed()) {
            res.setStatus(429);
            res.addHeader("Retry-After", "60");
            return;
        }
        chain.doFilter(req, res);
    }

    private String resolveTier(HttpServletRequest req) {
        if (req.getHeader("X-API-Key") != null) return "premium";
        if (SecurityContextHolder.getContext().getAuthentication() != null) return "authenticated";
        return "anonymous";
    }
}
```

---

## Background Jobs & Async Processing

### Spring @Async (fire-and-forget)

```java
@SpringBootApplication
@EnableAsync
public class Application { /* ... */ }

// Thread pool configuration
@Configuration
public class AsyncConfig {

    @Bean("taskExecutor")
    public Executor taskExecutor() {
        ThreadPoolTaskExecutor executor = new ThreadPoolTaskExecutor();
        executor.setCorePoolSize(4);
        executor.setMaxPoolSize(10);
        executor.setQueueCapacity(100);
        executor.setThreadNamePrefix("async-");
        executor.setRejectedExecutionHandler(new ThreadPoolExecutor.CallerRunsPolicy());
        executor.initialize();
        return executor;
    }
}

// Async service method
@Service
@Slf4j
public class IndexingService {

    @Async("taskExecutor")
    public CompletableFuture<Void> indexMarket(UUID marketId) {
        try {
            Market market = marketRepository.findById(marketId)
                .orElseThrow(() -> new ResourceNotFoundException("Market not found"));
            vectorStore.upsert(market.getId(), embeddingService.embed(market.toText()));
            log.info("Indexed market {}", marketId);
        } catch (Exception e) {
            log.error("Failed to index market {}", marketId, e);
        }
        return CompletableFuture.completedFuture(null);
    }
}

// Controller: respond immediately, index in background
@PostMapping
public ResponseEntity<MarketDto> create(@Valid @RequestBody CreateMarketRequest req) {
    MarketDto created = marketService.create(req);
    indexingService.indexMarket(created.id());   // non-blocking
    return ResponseEntity.status(HttpStatus.CREATED).body(created);
}
```

### Scheduled Jobs — Spring @Scheduled

```java
@Component
@Slf4j
@RequiredArgsConstructor
public class MarketSyncJob {

    private final MarketSyncService syncService;

    @Scheduled(cron = "0 0 * * * *")         // top of every hour
    public void syncActiveMarkets() {
        log.info("Starting market sync");
        try {
            int synced = syncService.syncAll();
            log.info("Synced {} markets", synced);
        } catch (Exception e) {
            log.error("Market sync failed", e);
        }
    }

    @Scheduled(fixedDelay = 30_000, initialDelay = 10_000)  // every 30s
    public void processQueue() {
        syncService.drainQueue();
    }
}

// Enable scheduling
@SpringBootApplication
@EnableScheduling
public class Application { /* ... */ }
```

### Durable Queues with Spring Events + Outbox Pattern

For operations that must survive restarts, use a transactional outbox instead of `@Async`:

```java
// 1. Save the job atomically with the triggering transaction
@Transactional
public MarketDto create(CreateMarketRequest request) {
    Market market = marketRepository.save(new Market(request));
    outboxRepository.save(new OutboxEvent("market.created", market.getId().toString()));
    return MarketDto.from(market);
}

// 2. Poll the outbox table and dispatch
@Scheduled(fixedDelay = 5_000)
@Transactional
public void processOutbox() {
    List<OutboxEvent> pending = outboxRepository.findPendingWithLock(10);
    pending.forEach(event -> {
        try {
            dispatch(event);
            event.markProcessed();
        } catch (Exception e) {
            event.incrementRetries();
            log.error("Failed to dispatch event {}", event.getId(), e);
        }
    });
}
```

---

## Logging & Monitoring

### Structured Logging with SLF4J + Logback + MDC

```java
// logback-spring.xml — JSON output for log aggregators (Datadog, Loki, CloudWatch)
// Use logstash-logback-encoder:
// <dependency>
//   <groupId>net.logstash.logback</groupId>
//   <artifactId>logstash-logback-encoder</artifactId>
// </dependency>
```

```xml
<!-- logback-spring.xml -->
<appender name="JSON" class="ch.qos.logback.core.ConsoleAppender">
  <encoder class="net.logstash.logback.encoder.LogstashEncoder">
    <includeMdcKeyName>requestId</includeMdcKeyName>
    <includeMdcKeyName>userId</includeMdcKeyName>
    <includeMdcKeyName>traceId</includeMdcKeyName>
  </encoder>
</appender>

<root level="INFO">
  <appender-ref ref="JSON"/>
</root>
```

```java
// Request filter — populate MDC for every request
@Component
@Order(Ordered.HIGHEST_PRECEDENCE)
public class MdcFilter extends OncePerRequestFilter {

    @Override
    protected void doFilterInternal(HttpServletRequest req,
            HttpServletResponse res, FilterChain chain)
            throws ServletException, IOException {

        String requestId = Optional.ofNullable(req.getHeader("X-Request-Id"))
            .orElse(UUID.randomUUID().toString());

        MDC.put("requestId", requestId);
        MDC.put("method", req.getMethod());
        MDC.put("path", req.getRequestURI());

        // If JWT is already parsed, attach userId
        Authentication auth = SecurityContextHolder.getContext().getAuthentication();
        if (auth != null && auth.getPrincipal() instanceof UserPrincipal p) {
            MDC.put("userId", p.id().toString());
        }

        try {
            chain.doFilter(req, res);
        } finally {
            MDC.clear();   // critical — thread pool reuse means stale MDC leaks
        }
    }
}

// Service-level logging — MDC fields are added automatically
@Service
@Slf4j
public class MarketService {

    public MarketDto findById(UUID id) {
        log.info("Fetching market");   // requestId, userId added by MDC filter
        return marketRepository.findById(id)
            .map(MarketDto::from)
            .orElseThrow(() -> {
                log.warn("Market not found: {}", id);
                return new ResourceNotFoundException("Market not found: " + id);
            });
    }
}
```

### Actuator & Health Checks

```yaml
# application.yml
management:
  endpoints:
    web:
      exposure:
        include: health, info, metrics, prometheus
      base-path: /internal
  endpoint:
    health:
      show-details: when-authorized
  metrics:
    tags:
      application: ${spring.application.name}
```

```java
// Custom health indicator
@Component
@RequiredArgsConstructor
public class VectorStoreHealthIndicator implements HealthIndicator {

    private final VectorStore vectorStore;

    @Override
    public Health health() {
        try {
            vectorStore.ping();
            return Health.up().withDetail("vectorStore", "reachable").build();
        } catch (Exception e) {
            return Health.down().withDetail("vectorStore", e.getMessage()).build();
        }
    }
}
```

---

## React: Consuming Backend Patterns

### Retry and Error Boundary

```tsx
// src/components/AsyncBoundary.tsx — wraps TanStack Query errors
import { QueryErrorResetBoundary } from "@tanstack/react-query";
import { ErrorBoundary } from "react-error-boundary";

export function AsyncBoundary({ children }: { children: React.ReactNode }) {
  return (
    <QueryErrorResetBoundary>
      {({ reset }) => (
        <ErrorBoundary
          onReset={reset}
          fallbackRender={({ error, resetErrorBoundary }) => (
            <div role="alert">
              <p>Something went wrong: {error.message}</p>
              <button onClick={resetErrorBoundary}>Retry</button>
            </div>
          )}
        >
          {children}
        </ErrorBoundary>
      )}
    </QueryErrorResetBoundary>
  );
}
```

### Optimistic Updates

```tsx
// src/hooks/useMarkets.ts
export function useDeleteMarket() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: marketsApi.delete,

    onMutate: async (id: string) => {
      await queryClient.cancelQueries({ queryKey: marketKeys.list() });
      const previous = queryClient.getQueryData(marketKeys.list());

      // Optimistically remove from list
      queryClient.setQueryData(marketKeys.list(), (old: PagedResponse<MarketDto>) => ({
        ...old,
        data: old.data.filter((m) => m.id !== id),
      }));

      return { previous };
    },

    onError: (_err, _id, context) => {
      // Rollback on failure
      queryClient.setQueryData(marketKeys.list(), context?.previous);
    },

    onSettled: () => {
      queryClient.invalidateQueries({ queryKey: marketKeys.list() });
    },
  });
}
```

### Background Refetching and Polling

```tsx
// Poll for a resource until its status changes (e.g., async job completion)
export function useMarket(id: string) {
  return useQuery({
    queryKey: marketKeys.detail(id),
    queryFn: () => marketsApi.getById(id),
    refetchInterval: (query) => {
      const status = query.state.data?.status;
      // Stop polling once the job finishes
      return status === "indexing" ? 3000 : false;
    },
  });
}
```

---

## Architecture Layering Reference

```
Controller        — HTTP binding (@RestController, @Valid, ResponseEntity)
     ↓
Service           — Business logic, @Transactional, @Cacheable
     ↓
Repository        — Data access (JpaRepository, @Query, Specification)
     ↓
Database          — PostgreSQL / Redis / Vector store
```

**Rules:**
- Controllers never call repositories directly — only services.
- Services own transactions; repositories are transaction-aware but don't define them.
- DTOs cross the controller ↔ service boundary; domain entities stay in service ↔ repository.
- Never expose JPA entities in API responses — mapper to DTO first.

---

## Checklist

Before shipping a new feature:

- [ ] Controller delegates to service — no business logic in `@RestController`
- [ ] `@Transactional(readOnly = true)` on service class, `@Transactional` on mutating methods only
- [ ] N+1 queries eliminated — verified with SQL logging enabled
- [ ] Projections used for list endpoints instead of full entities
- [ ] `@Valid` on all `@RequestBody` parameters
- [ ] `@RestControllerAdvice` handles all exception types
- [ ] `@Cacheable` / `@CacheEvict` applied at service layer, not controller
- [ ] Async jobs (`@Async`) don't swallow exceptions — use `CompletableFuture` or a recovery method
- [ ] MDC populated per-request and cleared in `finally`
- [ ] No JPA entities serialized to JSON — always map to DTOs
- [ ] React query keys follow `[resource, action, params]` structure
- [ ] Optimistic updates with rollback for destructive mutations
- [ ] `AsyncBoundary` wraps all data-fetching subtrees