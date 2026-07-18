---
name: Part X - Database and Data Management
version: 1.0.0
description: Comprehensive database architecture, data management, and operational standards for AI systems. This skill establishes the foundational principles for database design, query optimization, data integrity, and lifecycle management.
scope: database, data-management, storage, persistence, data-lifecycle
authority: AI Constitution - Directive Principles
enforcement: MANDATORY
review_cycle: quarterly
---

# PART X: DATABASE AND DATA MANAGEMENT

## CONSTITUTIVE PRINCIPLES

### Article 1: Data as a Strategic Asset

**1.1** Data shall be treated as a strategic asset of the organization, with appropriate governance, protection, and stewardship.

**1.2** All data management activities must align with organizational objectives and regulatory requirements.

**1.3** Data quality, integrity, and availability are fundamental obligations of all database operations.

**1.4** The principle of data minimization shall guide collection and retention decisions.

### Article 2: Database Sovereignty

**2.1** Each database system shall have clearly defined ownership, stewardship, and accountability structures.

**2.2** Database owners are responsible for:

   (a) Ensuring appropriate access controls and authorization
   
   (b) Maintaining data quality and integrity
   
   (c) Implementing backup and recovery procedures
   
   (d) Ensuring compliance with retention policies
   
   (e) Responding to data subject rights requests

**2.3** Database administrators shall have operational responsibilities but must operate under the principle of least privilege.

### Article 3: Database Independence

**3.1** Application logic must be independent of specific database implementations where possible.

**3.2** Database abstraction layers must be used to minimize vendor lock-in.

**3.3** Standard SQL must be preferred over database-specific extensions.

**3.4** Portability considerations must be incorporated into database selection and schema design.

---

## CHAPTER I: POSTGRESQL BEST PRACTICES

### Article 4: PostgreSQL Installation and Configuration

**4.1** Installation Standards:

   (a) Use official PostgreSQL packages or trusted distribution channels
   
   (b) Install the latest stable minor version within the current major version
   
   (c) Apply security updates within established SLAs
   
   (d) Use system package managers where available for easier maintenance

**4.2** Configuration Principles:

   (a) PostgreSQL configuration must be optimized for the workload characteristics
   
   (b) Default configurations must not be used in production
   
   (c) Configuration changes must be documented with rationale
   
   (d) Configuration should be managed through infrastructure-as-code

**4.3** Essential Configuration Parameters:

   ```
   # Memory Settings
   shared_buffers = 25% of available RAM (for dedicated servers)
   effective_cache_size = 75% of available RAM
   work_mem = (available RAM - shared_buffers) / (max_connections * complexity)
   maintenance_work_mem = 10% of available RAM (up to 8GB)
   
   # Write Optimization
   wal_buffers = 16MB - 64MB
   checkpoint_completion_target = 0.9
   max_wal_size = 1GB - 4GB
   
   # Query Planner
   random_page_cost = 1.1 (for SSDs) or 4.0 (for HDDs)
   effective_io_concurrency = 200 (for SSDs)
   default_statistics_target = 100 - 400
   
   # Concurrency
   max_connections = 100 - 500 (based on expected usage)
   max_worker_processes = number of CPU cores
   max_parallel_workers_per_gather = 4 (based on cores)
   max_parallel_workers = number of CPU cores
   
   # Logging
   log_destination = 'stderr'
   logging_collector = on
   log_directory = 'log'
   log_filename = 'postgresql-%Y-%m-%d_%H%M%S.log'
   log_rotation_age = 1d
   log_rotation_size = 100MB
   log_min_duration_statement = 1000 (ms, for slow query logging)
   log_line_prefix = '%t [%p]: [%l-1] user=%u,db=%d,app=%a,client=%h'
   ```

### Article 5: Schema Design Standards

**5.1** Naming Conventions:

   (a) Use lowercase names with underscores (snake_case)
   
   (b) Use descriptive, non-abbreviated names
   
   (c) Table names: plural form (users, orders, order_items)
   
   (d) Column names: singular form (user_id, order_id, created_at)
   
   (e) Primary keys: id or {table_singular}_id
   
   (f) Foreign keys: {referenced_table_singular}_id
   
   (g) Indexes: idx_{table}_{column(s)} or idx_{table}_{column(s)}_covering
   
   (h) Constraints: chk_{table}_{description}, fk_{table}_{referenced_table}

**5.2** Table Design Principles:

   (a) Tables must have a primary key defined
   
   (b) Each row must have a unique identifier
   
   (c) Use appropriate data types (never use TEXT when VARCHAR with limit is appropriate)
   
   (d) Avoid NULL where possible; use default values instead
   
   (e) Separate frequently queried fields from rarely queried fields

**5.3** Data Type Selection Guidelines:

   (a) **Identifiers**: Use BIGINT for primary keys expected to grow large
   
   (b) **Character Data**:
       - VARCHAR(n) for fields with known maximum length
       - TEXT for unlimited length text (descriptions, comments)
       - CITEXT for case-insensitive text comparisons
   
   (c) **Numeric Data**:
       - INTEGER for typical counts and IDs
       - BIGINT for large counts, sums, or IDs
       - NUMERIC(p,s) for monetary and precise decimal values
       - REAL/DOUBLE PRECISION for approximate values only
   
   (d) **Date/Time**:
       - TIMESTAMP WITH TIME ZONE for most timestamps (preferred)
       - DATE for dates without time
       - TIME for times without date
       - Avoid TIMESTAMP WITHOUT TIME ZONE unless explicitly required
   
   (e) **Boolean**: Use BOOLEAN, never use INTEGER as substitute
   
   (f) **JSON**: Use JSONB for searchable JSON; JSON for validated-only storage
   
   (g) **Arrays**: Use ARRAY for simple arrays; use normalized tables for complex structures
   
   (h) **UUID**: Use UUID for globally unique identifiers across systems

**5.4** Constraint Design:

   (a) Declare NOT NULL constraints where values are required
   
   (b) Use CHECK constraints for business rules
   
   (c) Use UNIQUE constraints for natural unique columns
   
   (d) Use EXCLUDE constraints for preventing conflicts
   
   (e) Name all constraints explicitly for better error messages

**5.5** Example Schema Patterns:

```sql
-- Standard ID column with sequence
CREATE TABLE users (
    id BIGSERIAL PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    username VARCHAR(50) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW()
);

-- Standard audit columns pattern
CREATE TABLE audit_example (
    -- Primary key
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    
    -- Business columns
    name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'active',
    
    -- Standard audit columns
    created_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    created_by BIGINT REFERENCES users(id),
    updated_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    updated_by BIGINT REFERENCES users(id),
    deleted_at TIMESTAMP WITH TIME ZONE,
    deleted_by BIGINT REFERENCES users(id),
    version INTEGER NOT NULL DEFAULT 1  -- For optimistic locking
);

-- Soft delete pattern
CREATE TABLE soft_delete_example (
    id BIGINT GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    is_deleted BOOLEAN NOT NULL DEFAULT FALSE,
    deleted_at TIMESTAMP WITH TIME ZONE,
    
    CONSTRAINT idx_soft_delete_active_only 
        CHECK (NOT is_deleted OR deleted_at IS NOT NULL)
);
```

### Article 6: Query Standards

**6.1** Query Writing Principles:

   (a) Always specify columns explicitly rather than using SELECT *
   
   (b) Use table aliases for readability in complex queries
   
   (c) Format queries consistently for maintainability
   
   (d) Include comments for complex logic
   
   (e) Avoid functions on indexed columns in WHERE clauses

**6.2** Query Structure Standards:

```sql
-- Good: Explicit columns, proper formatting
SELECT 
    u.id,
    u.email,
    u.full_name,
    COUNT(o.id) AS order_count
FROM users u
LEFT JOIN orders o ON o.user_id = u.id
WHERE u.email_verified = TRUE
    AND u.created_at >= '2024-01-01'
GROUP BY u.id, u.email, u.full_name
HAVING COUNT(o.id) > 5
ORDER BY order_count DESC
LIMIT 100;

-- Good: Window function example
SELECT 
    id,
    email,
    department,
    salary,
    AVG(salary) OVER (PARTITION BY department) AS dept_avg_salary,
    salary - AVG(salary) OVER (PARTITION BY department) AS salary_diff
FROM employees
WHERE is_active = TRUE;
```

**6.3** Common Query Patterns:

   (a) **Pagination**: Use cursor-based pagination for large datasets
   
   ```sql
   -- Offset pagination (acceptable for small datasets)
   SELECT * FROM users ORDER BY id LIMIT 20 OFFSET 40;
   
   -- Cursor-based pagination (preferred for large datasets)
   SELECT * FROM users 
   WHERE id > :last_seen_id 
   ORDER BY id 
   LIMIT 20;
   ```
   
   (b) **Upsert Pattern**: Use ON CONFLICT for insert-or-update
   
   ```sql
   INSERT INTO users (id, email, updated_at)
   VALUES (:id, :email, NOW())
   ON CONFLICT (id) 
   DO UPDATE SET 
       email = EXCLUDED.email,
       updated_at = EXCLUDED.updated_at;
   ```
   
   (c) **Soft Delete with Filter**:
   
   ```sql
   -- Use a view or function for consistent soft delete filtering
   CREATE OR REPLACE FUNCTION get_active_users()
   RETURNS SETOF users AS $$
   BEGIN
       RETURN QUERY 
       SELECT * FROM users 
       WHERE deleted_at IS NULL;
   END;
   $$ LANGUAGE plpgsql STABLE;
   ```

**6.4** Query Anti-Patterns to Avoid:

   (a) **SELECT *** in application code
   
   (b) **Correlated subqueries** for large datasets (use JOINs instead)
   
   (c) **Functions on indexed columns** (breaks index usage)
   
   (d) **Implicit type casts** that prevent index usage
   
   (e) **Unanchored LIKE patterns** (LIKE '%something') for large tables
   
   (f) **OR conditions** that prevent index usage (use UNION or IN instead)
   
   (g) **Cartesian products** from missing JOIN conditions

### Article 7: Transaction Standards

**7.1** Transaction Boundaries:

   (a) Keep transactions as short as possible
   
   (b) Avoid user-interactable operations within transactions
   
   (c) Do not start transactions before validating input
   
   (d) Handle lock timeouts gracefully with retry logic

**7.2** Transaction Isolation Levels:

   (a) **READ COMMITTED** (default): Use for most operations
   
   (b) **REPEATABLE READ**: Use for financial calculations and inventory
   
   (c) **SERIALIZABLE**: Use only when absolutely required (performance impact)
   
   (d) Never use READ UNCOMMITTED

**7.3** Locking Best Practices:

   (a) Use SELECT ... FOR UPDATE for row-level locks when needed
   
   (b) Use advisory locks for application-level locking
   
   (c) Avoid long-running transactions that hold locks
   
   (d) Use SKIP LOCKED for queue-like processing
   
   ```sql
   -- Row-level lock example
   BEGIN;
   SELECT * FROM inventory 
   WHERE product_id = :product_id 
   FOR UPDATE;
   -- Update inventory...
   UPDATE inventory SET quantity = quantity - :amount 
   WHERE product_id = :product_id;
   COMMIT;
   
   -- Advisory lock example
   SELECT pg_advisory_lock(:lock_id);
   -- Critical section...
   PERFORM pg_advisory_unlock(:lock_id);
   ```

**7.4** Error Handling in Transactions:

   (a) Always use explicit ROLLBACK on errors
   
   (b) Implement retry logic for transient errors (deadlocks, connection loss)
   
   (c) Log transaction failures for monitoring

### Article 8: Stored Procedure and Function Standards

**8.1** When to Use Stored Procedures/Functions:

   (a) Complex business logic that benefits from being close to data
   
   (b) Operations requiring multiple round-trips
   
   (c) Data transformation for reporting
   
   (d) Automated maintenance tasks

**8.2** Function/Procedure Standards:

   (a) Use LANGUAGE plpgsql for complex logic
   
   (b) Use LANGUAGE sql for simple queries
   
   (c) Always specify volatility (IMMUTABLE, STABLE, VOLATILE)
   
   (d) Use RETURNS TABLE or SETOF for multiple row returns
   
   (e) Handle NULL inputs explicitly

**8.3** Security Considerations:

   (a) Use SECURITY DEFINER functions sparingly and carefully
   
   (b) Set search_path to prevent search_path hijacking
   
   (c) Validate all inputs within functions
   
   ```sql
   CREATE OR REPLACE FUNCTION get_user_by_id(
       p_user_id BIGINT
   ) RETURNS SETOF users AS $$
   BEGIN
       -- Input validation
       IF p_user_id IS NULL OR p_user_id <= 0 THEN
           RAISE EXCEPTION 'Invalid user ID';
       END IF;
       
       RETURN QUERY 
       SELECT * FROM users 
       WHERE id = p_user_id 
           AND deleted_at IS NULL;
   END;
   $$ LANGUAGE plpgsql STABLE SECURITY DEFINER;
   
   -- Reset search_path in SECURITY DEFINER functions
   CREATE OR REPLACE FUNCTION privileged_operation()
   RETURNS VOID AS $$
   BEGIN
       -- Explicitly set search_path
       PERFORM set_config('search_path', 'app_schema', true);
       -- Function logic...
   END;
   $$ LANGUAGE plpgsql SECURITY DEFINER;
   ```

---

## CHAPTER II: MULTI-TENANCY AND ROW-LEVEL SECURITY

### Article 9: Multi-Tenancy Architecture

**9.1** Multi-Tenancy Models:

   (a) **Database per tenant**: Maximum isolation, higher cost
   
   (b) **Schema per tenant**: Good isolation, moderate cost
   
   (c) **Row-level security**: Shared infrastructure, tenant data separated by tenant_id

**9.2** Selection Criteria:

   (a) Consider tenant count, data isolation requirements, and cost constraints
   
   (b) Row-level security preferred for most SaaS applications
   
   (c) Database per tenant for highly regulated industries or enterprise requirements

**9.3** Tenant Identification:

   (a) Every tenant-specific table must have a tenant_id column
   
   (b) tenant_id must be the first column in all indexes
   
   (c) tenant_id must be non-nullable with a foreign key to tenant registry

### Article 10: Row-Level Security Implementation

**10.1** RLS Policy Design:

   (a) Create separate policies for SELECT, INSERT, UPDATE, DELETE
   
   (b) Use descriptive policy names following pattern: {operation}_{table}_{context}
   
   (c) Policies must be simple and performant

**10.2** RLS Implementation Pattern:

```sql
-- Enable RLS on table
ALTER TABLE documents ENABLE ROW LEVEL SECURITY;

-- Create policy for tenant isolation
CREATE POLICY tenant_isolation_select ON documents
    FOR SELECT
    USING (tenant_id = current_setting('app.current_tenant_id')::BIGINT);

CREATE POLICY tenant_isolation_insert ON documents
    FOR INSERT
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::BIGINT);

CREATE POLICY tenant_isolation_update ON documents
    FOR UPDATE
    USING (tenant_id = current_setting('app.current_tenant_id')::BIGINT)
    WITH CHECK (tenant_id = current_setting('app.current_tenant_id')::BIGINT);

CREATE POLICY tenant_isolation_delete ON documents
    FOR DELETE
    USING (tenant_id = current_setting('app.current_tenant_id')::BIGINT);

-- Bypass RLS for privileged operations
ALTER TABLE documents FORCE ROW LEVEL SECURITY;
```

**10.3** Setting Tenant Context:

```sql
-- Set tenant context at session start
SET app.current_tenant_id = '123';

-- Application-level pattern
SET LOCAL app.current_tenant_id = :tenant_id;
BEGIN;
-- Operations within transaction use tenant context
COMMIT;
```

**10.4** Cross-Tenant Operations:

   (a) Cross-tenant operations must be explicitly designed and reviewed
   
   (b) Use SECURITY DEFINER functions with explicit tenant validation
   
   (c) Audit all cross-tenant data access

### Article 11: Tenant Data Isolation Verification

**11.1** Isolation Testing:

   (a) Automated tests must verify tenant data cannot access other tenant's data
   
   (b) Security tests must attempt cross-tenant access and verify rejection
   
   (c) Penetration testing scope must include tenant isolation

**11.2** Monitoring:

   (a) Log queries that access multiple tenants
   
   (b) Alert on suspicious cross-tenant access patterns

---

## CHAPTER III: MIGRATION SAFETY RULES

### Article 12: Migration Philosophy

**12.1** Database migrations are irreversible operations that require careful planning and execution.

**12.2** Zero-downtime migrations are the standard expectation for production systems.

**12.3** All migrations must be reversible or accompanied by verified rollback procedures.

**12.4** Migrations must be tested in environments that mirror production.

### Article 13: Migration Patterns for Zero-Downtime

**13.1** Expand-Contract Pattern for Column Changes:

```sql
-- Phase 1: Expand - Add new column
ALTER TABLE users ADD COLUMN phone_number VARCHAR(20);

-- Phase 2: Migrate - Update application to write to both columns
-- Deploy application version that writes to both

-- Phase 3: Backfill - Copy data from old to new
UPDATE users SET phone_number = legacy_phone WHERE phone_number IS NULL;

-- Phase 4: Contract - Remove old column (after verification)
ALTER TABLE users DROP COLUMN legacy_phone;
```

**13.2** Expand-Contract Pattern for Index Creation:

```sql
-- Create index CONCURRENTLY to avoid locking
CREATE INDEX CONCURRENTLY idx_users_email ON users(email);

-- Remove old index after verification
DROP INDEX CONCURRENTLY idx_users_email_old;
```

**13.3** Safe Column Operations:

   (a) **Adding columns**: Safe (with default value in PostgreSQL 11+)
   
   (b) **Renaming columns**: Use expand-contract pattern
   
   (c) **Changing column type**: Use expand-contract pattern
   
   (d) **Dropping columns**: Use expand-contract pattern (mark as unused first)
   
   (e) **Adding NOT NULL**: Must have default, use expand-contract for large tables
   
   (f) **Adding constraints**: Use NOT VALID initially, then validate

**13.4** Safe Table Operations:

   (a) **Adding tables**: Safe, always do first
   
   (b) **Renaming tables**: Use views with expand-contract
   
   (c) **Splitting tables**: Create new table, populate, add FK, drop old columns
   
   (d) **Merging tables**: Create new table, populate from both, switch references

**13.5** Constraint Implementation:

```sql
-- Adding check constraint without locking
ALTER TABLE orders ADD CONSTRAINT chk_orders_positive_amount 
    CHECK (amount > 0) NOT VALID;

-- Validate existing rows
ALTER TABLE orders VALIDATE CONSTRAINT chk_orders_positive_amount;

-- Adding foreign key without locking
ALTER TABLE order_items ADD CONSTRAINT fk_order_items_order
    FOREIGN KEY (order_id) REFERENCES orders(id) NOT VALID;

-- Validate existing rows
ALTER TABLE order_items VALIDATE CONSTRAINT fk_order_items_order;
```

### Article 14: Migration Execution Standards

**14.1** Pre-Migration Checklist:

   (a) Review migration for potential locking operations
   
   (b) Estimate execution time for large table operations
   
   (c) Verify backup availability
   
   (d) Schedule maintenance window if required
   
   (e) Notify stakeholders of migration plan
   
   (f) Prepare rollback procedures

**14.2** Migration Execution:

   (a) Run migrations during low-traffic periods
   
   (b) Execute migrations as transactions (except CONCURRENTLY operations)
   
   (c) Monitor for locks and long-running queries
   
   (d) Verify row counts before and after data migrations

**14.3** Post-Migration Verification:

   (a) Verify application functionality
   
   (b) Check for performance degradation
   
   (c) Verify data integrity
   
   (d) Update documentation

### Article 15: Migration Tools and Versioning

**15.1** Migration Tool Requirements:

   (a) Use established migration frameworks (Flyway, Liquibase, Alembic)
   
   (b) Maintain migration history in version control
   
   (c) Ensure migrations are idempotent where possible
   
   (d) Use sequential or timestamp-based versioning

**15.2** Migration File Standards:

```
migrations/
├── V001__create_users_table.sql
├── V002__create_orders_table.sql
├── V003__add_email_index_to_users.sql
└── V004__add_phone_to_users.sql
```

**15.3** Migration Content Standards:

```sql
-- Migration file header
-- Migration: V005__add_status_to_orders.sql
-- Author: developer@example.com
-- Date: 2024-01-15
-- Description: Add status column to orders table for order workflow

BEGIN;

-- Add column with default
ALTER TABLE orders ADD COLUMN status VARCHAR(20) NOT NULL DEFAULT 'pending';

-- Add index for status queries
CREATE INDEX CONCURRENTLY idx_orders_status ON orders(status);

-- Add check constraint for valid statuses
ALTER TABLE orders ADD CONSTRAINT chk_orders_status 
    CHECK (status IN ('pending', 'processing', 'shipped', 'delivered', 'cancelled'));

-- Add comment for documentation
COMMENT ON COLUMN orders.status IS 'Current status of the order in the fulfillment workflow';

COMMIT;

-- Verify
-- SELECT status, COUNT(*) FROM orders GROUP BY status;
```

---

## CHAPTER IV: INDEXING AND PERFORMANCE STANDARDS

### Article 16: Index Design Principles

**16.1** Index Creation Guidelines:

   (a) Create indexes for columns frequently used in:
       - WHERE clauses
       - JOIN conditions
       - ORDER BY clauses
   
   (b) Indexes have a cost: slower writes, more storage, memory usage
   
   (c) Each index should have documented justification
   
   (d) Remove unused indexes regularly

**16.2** Index Type Selection:

   (a) **B-tree (default)**: Range queries, equality, sorting
   
   (b) **Hash**: Equality comparisons only (memcached-style)
   
   (c) **GiST**: Full-text search, geometric types, range types
   
   (d) **GIN**: JSONB, arrays, full-text search (inverted index)
   
   (e) **BRIN**: Very large tables with natural ordering (logs, time-series)

**16.3** Composite Index Design:

   (a) Order columns by selectivity (most selective first)
   
   (b) Consider query patterns when ordering
   
   (c) Use covering indexes to eliminate table access
   
   ```sql
   -- Composite index for common query pattern
   CREATE INDEX idx_orders_user_status ON orders(user_id, status);
   
   -- Covering index to include frequently selected columns
   CREATE INDEX idx_orders_user_status_covering 
       ON orders(user_id, status) 
       INCLUDE (total_amount, created_at);
   ```

### Article 17: Query Performance Standards

**17.1** Query Performance Requirements:

   (a) All queries must have execution plans analyzed before deployment
   
   (b) Queries touching more than 1000 rows should have appropriate indexes
   
   (c) Complex queries should be reviewed by database specialists
   
   (d) EXPLAIN ANALYZE must be used for performance investigation

**17.2** Performance Anti-Patterns:

   (a) **N+1 Queries**: Use JOINs or batch queries
   
   (b) **Missing indexes**: Analyze slow queries and add indexes
   
   (c) **Functions on columns**: Create functional indexes instead
   
   (d) **Excessive pagination**: Use keyset pagination
   
   (e) **Unnecessary ORDER BY**: Remove if not needed

**17.3** Query Optimization Examples:

```sql
-- Bad: N+1 pattern
SELECT * FROM orders;
-- Then for each order:
SELECT * FROM customers WHERE id = orders.customer_id;

-- Good: Single query with JOIN
SELECT o.*, c.name, c.email 
FROM orders o
JOIN customers c ON c.id = o.customer_id;

-- Bad: Function on indexed column
SELECT * FROM users WHERE LOWER(email) = LOWER(:email);

-- Good: Functional index
CREATE INDEX idx_users_email_lower ON users(LOWER(email));
SELECT * FROM users WHERE LOWER(email) = LOWER(:email);

-- Bad: Unanchored LIKE
SELECT * FROM products WHERE name LIKE '%laptop%';

-- Good: Full-text search with GIN index
CREATE INDEX idx_products_name_fts ON products USING GIN(to_tsvector('english', name));
SELECT * FROM products WHERE to_tsvector('english', name) @@ plainto_tsquery('english', :search_term);
```

### Article 18: Performance Monitoring

**18.1** Key Performance Metrics:

   (a) Query execution time (p50, p95, p99)
   
   (b) Connection pool utilization
   
   (c) Index hit ratio
   
   (d) Cache hit ratio (shared_buffers, OS cache)
   
   (e) Lock wait time
   
   (f) Replication lag (for replica configurations)

**18.2** Monitoring Queries:

```sql
-- Long-running queries
SELECT 
    pid,
    now() - pg_stat_activity.query_start AS duration,
    usename,
    query,
    state
FROM pg_stat_activity
WHERE (now() - pg_stat_activity.query_start) > interval '5 minutes'
    AND state = 'active'
ORDER BY duration DESC;

-- Index usage statistics
SELECT 
    schemaname,
    tablename,
    indexname,
    idx_tup_read,
    idx_tup_fetch,
    idx_scan
FROM pg_stat_user_indexes
ORDER BY idx_scan ASC;

-- Table bloat estimation
SELECT 
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename)) AS bloat
FROM pg_stat_user_tables
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) - pg_relation_size(schemaname||'.'||tablename) DESC;
```

---

## CHAPTER V: BACKUP AND RECOVERY PROTOCOLS

### Article 19: Backup Requirements

**19.1** Backup Strategy Principles:

   (a) Follow the 3-2-1 rule: 3 copies, 2 different media types, 1 offsite
   
   (b) Test backups regularly for recoverability
   
   (c) Document recovery procedures
   
   (d) Automate backup processes

**19.2** Backup Types:

   (a) **Full backups**: Complete database dump (weekly minimum)
   
   (b) **Incremental backups**: Changes since last backup (daily minimum)
   
   (c) **WAL archiving**: Continuous archiving for point-in-time recovery

**19.3** PostgreSQL Backup Methods:

```bash
# Full backup using pg_dump
pg_dump -Fc -f backup.dump -j 4 -Z 6 database_name

# Full backup using pg_basebackup (for PITR)
pg_basebackup -h localhost -D /backup/base -Ft -z -P -v

# Point-in-time recovery using WAL
# Configure wal_level = replica in postgresql.conf
# Set archive_mode = on
# Set archive_command = 'cp %p /archive/%f'
```

**19.4** Backup Verification:

   (a) Verify backup completion and size
   
   (b) Test restore to non-production environment monthly
   
   (c) Document backup restoration procedures
   
   (d) Maintain backup retention logs

### Article 20: Recovery Procedures

**20.1** Recovery Time Objectives (RTO) and Recovery Point Objectives (RPO):

   (a) Define RTO and RPO for each database system
   
   (b) RTO: Maximum acceptable downtime
   
   (c) RPO: Maximum acceptable data loss (time-based)

**20.2** Recovery Procedures:

```bash
# Point-in-time recovery

# 1. Stop PostgreSQL
sudo systemctl stop postgresql

# 2. Backup current data directory
cp -r /var/lib/postgresql/data /backup/pre-pitr-restore

# 3. Clear data directory
rm -rf /var/lib/postgresql/data/*

# 4. Restore base backup
pg_restore -d postgres --clean --create /backup/base

# 5. Create recovery.conf (PostgreSQL 12-) or recovery.signal (PostgreSQL 13+)
touch /var/lib/postgresql/data/recovery.signal

# 6. Configure recovery.conf for PITR
# postgresql.conf auto-recovery mode:
# restore_command = 'cp /archive/%f "%p"'
# recovery_target_time = '2024-01-15 14:30:00 UTC'

# 7. Start PostgreSQL
sudo systemctl start postgresql

# 8. Verify recovery
psql -c "SELECT pg_is_in_recovery();"
```

**20.3** Recovery Testing:

   (a) Conduct full recovery test quarterly
   
   (b) Test point-in-time recovery monthly
   
   (c) Document and time each recovery procedure
   
   (d) Train team members on recovery procedures

### Article 21: Replication and High Availability

**21.1** Replication Configuration:

   (a) Use streaming replication for high availability
   
   (b) Configure synchronous replication for critical data
   
   (c) Monitor replication lag continuously
   
   (d) Plan for automatic failover

**21.2** High Availability Patterns:

   (a) **Streaming replication with failover**: Primary + replica(s) with automatic failover
   
   (b) **Cascading replication**: Replicas of replicas for geographic distribution
   
   (c) **Logical replication**: For selective replication and version migration

**21.3** Failover Procedures:

   (a) Document automatic failover triggers
   
   (b) Document manual failover procedures
   
   (c) Test failover procedures regularly
   
   (d) Update DNS/connection strings after failover

---

## CHAPTER VI: DATA RETENTION AND DISPOSAL

### Article 22: Data Retention Policies

**22.1** Retention Policy Framework:

   (a) Define retention periods for each data category
   
   (b) Document legal and regulatory retention requirements
   
   (c) Implement automated retention enforcement
   
   (d) Review retention policies annually

**22.2** Retention Period Examples:

   (a) **Transaction logs**: 7 years (depending on regulations)
   
   (b) **Application logs**: 90 days (operational), 1 year (security)
   
   (c) **Audit logs**: 7 years (compliance)
   
   (d) **User sessions**: 30 days
   
   (e) **Temporary data**: Immediate deletion after use

**22.3** Retention Implementation:

```sql
-- Partitioned table for time-based retention
CREATE TABLE events (
    id BIGSERIAL,
    event_type VARCHAR(50),
    event_data JSONB,
    created_at TIMESTAMP WITH TIME ZONE NOT NULL
) PARTITION BY RANGE (created_at);

-- Create monthly partitions
CREATE TABLE events_2024_01 PARTITION OF events
    FOR VALUES FROM ('2024-01-01') TO ('2024-02-01');

-- Create partitions for upcoming months
-- Automated via scheduled job

-- Drop old partitions (after retention period)
DROP TABLE events_2023_01;
```

### Article 23: Data Archiving

**23.1** Archival Strategy:

   (a) Archive data that exceeds active retention but must be preserved
   
   (b) Use compressed, immutable storage for archives
   
   (c) Maintain searchable index of archived data
   
   (d) Verify archive integrity regularly

**23.2** Archival Procedures:

```sql
-- Move old data to archive table
INSERT INTO events_archive 
SELECT * FROM events 
WHERE created_at < '2023-01-01';

-- Verify row count match
DELETE FROM events 
WHERE created_at < '2023-01-01'
    AND id IN (SELECT id FROM events_archive);

-- Vacuum to reclaim space
VACUUM events;
```

### Article 24: Data Disposal

**24.1** Disposal Requirements:

   (a) Data must be securely disposed when no longer needed
   
   (b) Disposal must follow regulatory requirements
   
   (c) Document disposal actions for audit trail

**24.2** Secure Deletion:

```sql
-- Standard deletion (data remains until VACUUM)
DELETE FROM users WHERE id = :user_id;

-- Immediate space reclamation
DELETE FROM users WHERE id = :user_id;
VACUUM users;

-- Table destruction (use with caution)
DROP TABLE users;

-- Destroy encryption keys (for encrypted data)
-- Key destruction makes data unrecoverable
```

**24.3** Disposal Documentation:

   (a) Record date, method, and reason for disposal
   
   (b) Include data classification and volume
   
   (c) Document approval for disposal
   
   (d) Maintain records according to retention requirements

---

## CHAPTER VII: CACHING STANDARDS

### Article 25: Caching Architecture

**25.1** Caching Strategy:

   (a) Cache expensive computations and frequently accessed data
   
   (b) Implement cache invalidation strategies
   
   (c) Use appropriate cache tiers (local, distributed)
   
   (d) Monitor cache hit rates and adjust accordingly

**25.2** Cache Layer Design:

   (a) **Application cache**: In-memory caches (Redis, Memcached)
   
   (b) **Query cache**: Cached query results (use judiciously)
   
   (c) **Result cache**: Cached API responses
   
   (d) **CDN cache**: Static assets and edge caching

### Article 26: Cache Implementation Standards

**26.1** Cache Key Design:

   (a) Use consistent, hierarchical key naming: {service}:{entity}:{id}:{version}
   
   (b) Include version or timestamp for cache busting
   
   (c) Keep keys short but descriptive

**26.2** Cache TTL (Time-to-Live) Standards:

   (a) User sessions: 15-30 minutes (with refresh)
   
   (b) Reference data: 1-24 hours
   
   (c) Computed results: 5-30 minutes
   
   (d) Static configuration: Until change notification

**26.3** Cache Invalidation:

   (a) Implement event-driven invalidation where possible
   
   (b) Use cache tags for selective invalidation
   
   (c) Implement maximum cache lifetimes as safety net
   
   (d) Use write-through or write-behind for critical data

**26.4** Redis Implementation Pattern:

```python
# Cache-aside pattern with invalidation
def get_user(user_id: int) -> User:
    cache_key = f"user:{user_id}"
    
    # Try cache first
    cached = redis.get(cache_key)
    if cached:
        return User.from_json(cached)
    
    # Cache miss - fetch from database
    user = db.query(User).filter_by(id=user_id).first()
    if user:
        redis.setex(cache_key, 3600, user.to_json())
    
    return user

def update_user(user_id: int, data: dict) -> User:
    user = db.query(User).filter_by(id=user_id).update(data)
    db.commit()
    
    # Invalidate cache
    redis.delete(f"user:{user_id}")
    
    return user

def invalidate_user_pattern(user_id: int) -> None:
    """Pattern for invalidating all related caches"""
    pattern = f"user:{user_id}:*"
    for key in redis.scan_iter(pattern):
        redis.delete(key)
```

### Article 27: Cache Security

**27.1** Cache Access Controls:

   (a) Restrict cache access to authorized services
   
   (b) Use authentication for cache connections
   
   (c) Implement network segmentation for cache infrastructure

**27.2** Cache Data Protection:

   (a) Do not cache sensitive data unless necessary
   
   (b) Encrypt cached sensitive data
   
   (c) Set appropriate TTLs to limit exposure

**27.3** Cache Monitoring:

   (a) Monitor cache hit/miss ratios
   
   (b) Alert on cache exhaustion
   
   (c) Monitor memory usage and evictions

---

## CHAPTER VIII: DATA INTEGRITY AND CONSISTENCY

### Article 28: Data Integrity Constraints

**28.1** Constraint Implementation:

   (a) Use database constraints as primary integrity mechanism
   
   (b) Implement application-level validation as defense-in-depth
   
   (c) Never disable constraints for convenience

**28.2** Constraint Categories:

   (a) **NOT NULL**: Mandatory fields
   
   (b) **UNIQUE**: Single-column and multi-column uniqueness
   
   (c) **PRIMARY KEY**: Row identity
   
   (d) **FOREIGN KEY**: Referential integrity
   
   (e) **CHECK**: Business rule validation
   
   (f) **EXCLUDE**: Complex constraints (no overlapping bookings)

**28.3** Trigger-Based Integrity:

   (a) Use triggers sparingly and document extensively
   
   (b) Implement audit logging via triggers
   
   (c) Maintain trigger code in version control

### Article 29: Consistency Patterns

**29.1** ACID Transactions:

   (a) Use transactions for operations requiring atomicity
   
   (b) Choose appropriate isolation levels
   
   (c) Handle deadlock scenarios gracefully

**29.2** Eventual Consistency:

   (a) Accept eventual consistency for performance-critical operations
   
   (b) Document consistency guarantees
   
   (c) Provide mechanisms for checking consistency

**29.3** Distributed Transactions:

   (a) Use the Saga pattern for distributed transactions
   
   (b) Implement compensation actions for rollback
   
   (c) Consider idempotency in all operations

```python
# Saga pattern example
class OrderCreationSaga:
    def execute(self, order_data: dict) -> Order:
        try:
            # Step 1: Reserve inventory
            inventory_reserved = self.reserve_inventory(order_data)
            
            # Step 2: Create order
            order = self.create_order(order_data)
            
            # Step 3: Process payment
            payment_processed = self.process_payment(order)
            
            return order
            
        except InsufficientInventory:
            # Compensate: Release inventory reservation
            self.release_inventory(inventory_reserved)
            raise
            
        except PaymentFailed:
            # Compensate: Cancel order, release inventory
            self.cancel_order(order)
            self.release_inventory(inventory_reserved)
            raise
```

---

## CHAPTER IX: CONNECTION MANAGEMENT

### Article 30: Connection Pool Standards

**30.1** Connection Pool Configuration:

   (a) Size pools appropriately for workload (typically 10-100 connections)
   
   (b) Configure minimum and maximum pool sizes
   
   (c) Set appropriate connection timeouts
   
   (d) Configure idle connection timeout

**30.2** Connection Pool Best Practices:

```python
# Example: Database connection pool configuration
from sqlalchemy import create_engine
from sqlalchemy.pool import QueuePool

engine = create_engine(
    "postgresql://user:pass@localhost/dbname",
    poolclass=QueuePool,
    pool_size=20,
    max_overflow=10,  # Additional connections beyond pool_size
    pool_timeout=30,  # Seconds to wait for connection
    pool_recycle=3600,  # Recycle connections after 1 hour
    pool_pre_ping=True,  # Test connections before use
)
```

**30.3** Connection Monitoring:

   (a) Monitor active connections and pool utilization
   
   (b) Alert on connection exhaustion
   
   (c) Log slow connection acquisition

### Article 31: Query Connection Patterns

**31.1** Connection Usage:

   (a) Acquire connections as late as possible
   
   (b) Release connections as early as possible
   
   (c) Never hold connections during user think time
   
   (d) Use read replicas for read-heavy workloads

**31.2** Read/Write Splitting:

   (a) Route read queries to replicas
   
   (b) Route write queries to primary
   
   (c) Handle replication lag in read-after-write scenarios

---

## CHAPTER X: DATA MODELING PATTERNS

### Article 32: Common Patterns

**32.1** Audit Trail Pattern:

```sql
CREATE TABLE audit_log (
    id BIGSERIAL PRIMARY KEY,
    table_name VARCHAR(100) NOT NULL,
    record_id BIGINT NOT NULL,
    action VARCHAR(20) NOT NULL,  -- INSERT, UPDATE, DELETE
    old_data JSONB,
    new_data JSONB,
    changed_by BIGINT REFERENCES users(id),
    changed_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    ip_address INET
);

CREATE INDEX idx_audit_log_table_record 
    ON audit_log(table_name, record_id);
CREATE INDEX idx_audit_log_changed_at 
    ON audit_log(changed_at);
```

**32.2** Soft Delete Pattern:

```sql
-- Add to all tenant-scoped tables
ALTER TABLE orders ADD COLUMN deleted_at TIMESTAMP WITH TIME ZONE;
ALTER TABLE orders ADD COLUMN deleted_by BIGINT REFERENCES users(id);

-- Create index for active records
CREATE INDEX idx_orders_active 
    ON orders(tenant_id) 
    WHERE deleted_at IS NULL;

-- Function to filter deleted records
CREATE OR REPLACE FUNCTION is_record_active(
    deleted_at_param TIMESTAMP WITH TIME ZONE
) RETURNS BOOLEAN AS $$
BEGIN
    RETURN deleted_at_param IS NULL;
END;
$$ LANGUAGE plpgsql IMMUTABLE;
```

**32.3** UUID Primary Key Pattern:

```sql
-- Generate UUIDs efficiently
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    -- other columns...
);

-- Or use gen_random_uuid() (PostgreSQL 13+)
CREATE TABLE orders (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    -- other columns...
);
```

**32.4** Enumeration Pattern:

```sql
-- Use ENUM type for fixed sets
CREATE TYPE order_status AS ENUM (
    'pending',
    'confirmed',
    'processing',
    'shipped',
    'delivered',
    'cancelled',
    'refunded'
);

ALTER TABLE orders ADD COLUMN status order_status NOT NULL DEFAULT 'pending';

-- Adding values to ENUM (safe operation)
ALTER TYPE order_status ADD VALUE IF NOT EXISTS 'partially_shipped';
```

**32.5** Full-Text Search Pattern:

```sql
-- Create search vector
ALTER TABLE articles ADD COLUMN search_vector tsvector;

-- Populate search vector
UPDATE articles SET 
    search_vector = to_tsvector('english', title || ' ' || content);

-- Create GIN index
CREATE INDEX idx_articles_search ON articles USING GIN(search_vector);

-- Keep search vector updated with trigger
CREATE OR REPLACE FUNCTION articles_search_trigger() RETURNS trigger AS $$
BEGIN
    NEW.search_vector := 
        to_tsvector('english', coalesce(NEW.title, '') || ' ' || coalesce(NEW.content, ''));
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER articles_search_update
    BEFORE INSERT OR UPDATE ON articles
    FOR EACH ROW EXECUTE FUNCTION articles_search_trigger();

-- Search query
SELECT id, title, ts_rank(search_vector, query) AS rank
FROM articles, to_tsquery('english', 'postgresql & optimization') query
WHERE search_vector @@ query
ORDER BY rank DESC;
```

---

## SCHEDULES AND ANNEXURES

### Schedule I: Database Security Checklist

**Access Control:**
- [ ] Database users follow least privilege principle
- [ ] Application uses dedicated database user
- [ ] Administrative access is restricted and logged
- [ ] Connection credentials are in secret management
- [ ] SSL/TLS is enforced for all connections

**Configuration:**
- [ ] SSL/TLS is enabled and configured
- [ ] Password authentication is strong (md5 is disabled)
- [ ] Unnecessary extensions are disabled
- [ ] Unnecessary functions are disabled
- [ ] Network access is restricted

### Schedule II: Performance Tuning Checklist

**Index Maintenance:**
- [ ] Unused indexes are removed
- [ ] Missing indexes are identified for critical queries
- [ ] Index bloat is monitored and addressed
- [ ] Composite indexes are optimized for query patterns

**Query Optimization:**
- [ ] Slow queries are monitored
- [ ] EXPLAIN ANALYZE is used for optimization
- [ ] N+1 queries are eliminated
- [ ] Batch operations are used where appropriate

### Schedule III: Common SQL Patterns Reference

**Pattern: Upsert with Conflict Detection**
```sql
INSERT INTO table (id, data)
VALUES (:id, :data)
ON CONFLICT (id) DO UPDATE SET
    data = EXCLUDED.data,
    updated_at = NOW();
```

**Pattern: Batch Insert**
```sql
INSERT INTO users (email, name)
SELECT email, name FROMunnest(:emails, :names);
```

**Pattern: Soft Delete with Filter**
```sql
-- Application view for consistent filtering
CREATE VIEW active_users AS
SELECT * FROM users WHERE deleted_at IS NULL;
```

**Pattern: Conditional Aggregation**
```sql
SELECT 
    user_id,
    COUNT(*) FILTER (WHERE status = 'active') AS active_count,
    COUNT(*) FILTER (WHERE status = 'inactive') AS inactive_count
FROM subscriptions
GROUP BY user_id;
```

---

## ENFORCEMENT AND INTERPRETATION

### Article 33: Enforcement

**33.1** All requirements in this skill are MANDATORY unless explicitly stated as RECOMMENDED.

**33.2** Database schema changes must follow the migration standards defined herein.

**33.3** Performance regressions must be addressed before production deployment.

### Article 34: Interpretation

**34.1** Database administrators have authority to enforce these standards.

**34.2** Exceptions require documented justification and security review.

**34.3** Consultation with database specialists is recommended for complex schema changes.

### Article 35: Updates and Amendments

**35.1** This skill must be reviewed quarterly.

**35.2** Best practices updates will be incorporated as they emerge.

**35.3** Breaking changes will be communicated with adequate notice.

---

*End of Part X: Database and Data Management*
