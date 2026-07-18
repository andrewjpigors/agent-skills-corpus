---
name: redis-caching
description: Use when implementing Redis caching strategies, session management, pub/sub messaging, data structure operations, Lua scripting, transactions, clustering, persistence, and production Redis best practices. Covers all Redis data types, caching patterns, and client libraries.
license: MIT
---

# Redis Caching Skill — Data Structures, Caching Patterns, and Production Best Practices

## Overview

This skill provides comprehensive guidance for **implementing Redis caching strategies**, including all Redis data structures (strings, hashes, lists, sets, sorted sets, streams, bitmaps, hyperloglogs, geospatial), caching patterns (cache-aside, write-through, write-behind, write-around), session management, pub/sub messaging, Lua scripting, transactions, pipelines, clustering, Sentinel, replication, persistence (RDB, AOF), memory management, and production best practices across multiple client libraries.

## When to Use

**Use this skill when:**

- Implementing cache-aside, write-through, write-behind, or write-around caching patterns
- Managing Redis sessions for web applications
- Using Redis pub/sub for real-time messaging
- Working with Redis Streams for message queuing
- Performing string operations (GET, SET, INCR, DECR, APPEND)
- Managing hash operations (HSET, HGET, HGETALL, HDEL)
- Using list operations (LPUSH, RPUSH, LPOP, RPOP, LRANGE)
- Implementing set operations (SADD, SREM, SMEMBERS, SINTER, SUNION)
- Working with sorted sets (ZADD, ZREM, ZRANGE, ZREVRANGE, ZINCRBY)
- Implementing stream processing (XADD, XREAD, XGROUP, XACK)
- Using bitmap operations (SETBIT, GETBIT, BITCOUNT)
- Implementing hyperloglog counting (PFADD, PFCOUNT, PFMERGE)
- Using geospatial operations (GEOADD, GEORADIUS, GEOHASH)
- Writing Lua scripts for atomic operations
- Implementing transactions with MULTI/EXEC
- Using pipelines for batch operations
- Setting up Redis clustering for horizontal scaling
- Configuring Redis Sentinel for high availability
- Implementing Redis replication for read scaling
- Configuring RDB persistence
- Setting up AOF persistence
- Managing memory and maxmemory configuration
- Implementing eviction policies (LRU, LFU, random, ttl)
- Managing TTL expiration strategies
- Setting up connection pooling with connection managers
- Using Redisson, Lettuce, Jedis, ioredis, node-redis, or redis-py clients

**Do NOT use this skill when:**

- Building a relational database schema (use database-design skill)
- Implementing application business logic (use backend-developer skill)
- Setting up message queues like RabbitMQ or Kafka (use microservices-architecture skill)
- Configuring full-text search (use elasticsearch or meilisearch)
- Implementing object storage (use cloud storage solutions)
- Setting up graph databases (use Neo4j or Amazon Neptune)
- Building time-series databases (use InfluxDB or TimescaleDB)

**Why avoid:** Redis is an in-memory data store optimized for caching, sessions, and real-time operations. It is not a replacement for relational databases, search engines, or object storage. Use the right tool for the job.

## Core Concepts

### Redis Data Structures

| Structure       | Use Case                               | Time Complexity | Memory Efficiency          |
| --------------- | -------------------------------------- | --------------- | -------------------------- |
| **String**      | Counter, cache, rate limiting          | O(1)            | High                       |
| **Hash**        | Object storage, user profiles          | O(1)            | High (sparse optimization) |
| **List**        | Queue, stack, feed                     | O(1) push/pop   | Medium                     |
| **Set**         | Tags, unique members, intersections    | O(1) add/remove | High                       |
| **Sorted Set**  | Leaderboards, rankings, priority queue | O(log N)        | Medium                     |
| **Stream**      | Message queue, event sourcing          | O(1) add        | Low (append-only)          |
| **Bitmap**      | Feature flags, presence tracking       | O(1)            | Very High                  |
| **HyperLogLog** | Unique visitor counting                | O(1)            | Very High (12KB per key)   |
| **Geospatial**  | Location-based queries                 | O(log N)        | Medium                     |

### Caching Patterns

| Pattern           | Write Strategy                           | Read Strategy                                  | Best For                   |
| ----------------- | ---------------------------------------- | ---------------------------------------------- | -------------------------- |
| **Cache-Aside**   | App writes to DB, invalidates cache      | App reads cache first, falls back to DB        | Most common, simple        |
| **Write-Through** | App writes to cache and DB synchronously | App reads from cache                           | Data consistency critical  |
| **Write-Behind**  | App writes to cache, async write to DB   | App reads from cache                           | Write performance critical |
| **Write-Around**  | App writes directly to DB                | App reads cache, falls back to DB, writes back | Reduce cache pollution     |

### Persistence Options

| Option        | Mechanism               | Durability                                | Performance | Recovery Time   |
| ------------- | ----------------------- | ----------------------------------------- | ----------- | --------------- |
| **RDB**       | Point-in-time snapshots | Lower (can lose data since last snapshot) | Higher      | Faster          |
| **AOF**       | Append-only command log | Higher (can configure fsync frequency)    | Lower       | Slower (replay) |
| **RDB + AOF** | Both mechanisms         | Highest                                   | Medium      | Medium          |

### Client Libraries by Language

| Language    | Recommended Client | Alternative     | Features                       |
| ----------- | ------------------ | --------------- | ------------------------------ |
| **Node.js** | ioredis            | node-redis      | Clustering, Sentinel, Lua      |
| **Python**  | redis-py           | redis.asyncio   | Pipelines, Pub/Sub, Streams    |
| **Java**    | Lettuce            | Jedis, Redisson | Reactive, clustering, Sentinel |
| **Go**      | go-redis           | redigo          | Pipelines, pub/sub, scripting  |
| **Ruby**    | redis-rb           | redis-namespace | Connection pooling, scripting  |

## Caching Pattern Implementations

### Cache-Aside Pattern (Lazy Loading)

The most common caching pattern. Application is responsible for loading data into cache.

```python
# Python (redis-py) - Cache-Aside Pattern
import redis
import json

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    # 1. Try cache first
    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # 2. Cache miss - load from database
    user = database.query("SELECT * FROM users WHERE id = %s", (user_id,))
    if not user:
        return None

    # 3. Store in cache with TTL
    redis_client.setex(cache_key, 3600, json.dumps(user))  # 1 hour TTL

    return user

def update_user(user_id: int, user_data: dict):
    # 1. Update database first
    database.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (user_data['name'], user_data['email'], user_id)
    )

    # 2. Invalidate cache
    redis_client.delete(f"user:{user_id}")
```

```javascript
// Node.js (ioredis) - Cache-Aside Pattern
const Redis = require('ioredis');
const redis = new Redis({ host: 'localhost', port: 6379 });

async function getProduct(productId) {
  const cacheKey = `product:${productId}`;

  // Try cache first
  let cached = await redis.get(cacheKey);
  if (cached) {
    return JSON.parse(cached);
  }

  // Cache miss - load from database
  const product = await db.products.findById(productId);
  if (!product) {
    return null;
  }

  // Store in cache with TTL
  await redis.setex(cacheKey, 3600, JSON.stringify(product));

  return product;
}

async function updateProduct(productId, productData) {
  await db.products.update(productId, productData);
  await redis.del(`product:${productId}`); // Invalidate cache
}
```

### Write-Through Pattern

Application writes to both cache and database synchronously.

```python
# Python - Write-Through Pattern
def save_user(user_id: int, user_data: dict):
    cache_key = f"user:{user_id}"

    # Write to both cache and database
    serialized = json.dumps(user_data)

    # 1. Write to cache
    redis_client.setex(cache_key, 3600, serialized)

    # 2. Write to database (synchronous)
    database.execute(
        "INSERT INTO users (id, name, email) VALUES (%s, %s, %s) "
        "ON CONFLICT (id) DO UPDATE SET name = %s, email = %s",
        (user_id, user_data['name'], user_data['email'],
         user_data['name'], user_data['email'])
    )
```

```javascript
// Node.js - Write-Through Pattern
async function saveProduct(productId, productData) {
  const cacheKey = `product:${productId}`;
  const serialized = JSON.stringify(productData);

  // Write to both cache and database
  await redis.setex(cacheKey, 3600, serialized);
  await db.products.upsert(productId, productData);
}
```

### Write-Behind Pattern (Write-Back)

Application writes to cache only, database is updated asynchronously.

```python
# Python - Write-Behind Pattern (using background thread)
import threading
import queue

write_queue = queue.Queue()

def background_writer():
    """Background thread that batches writes to database"""
    batch = []
    while True:
        try:
            item = write_queue.get(timeout=1)
            batch.append(item)

            # Flush batch every 100 items or every second
            if len(batch) >= 100:
                database.batch_update(batch)
                batch.clear()
        except queue.Empty:
            if batch:
                database.batch_update(batch)
                batch.clear()

# Start background writer thread
threading.Thread(target=background_writer, daemon=True).start()

def update_user_async(user_id: int, user_data: dict):
    cache_key = f"user:{user_id}"

    # 1. Write to cache immediately
    redis_client.setex(cache_key, 3600, json.dumps(user_data))

    # 2. Queue for async database write
    write_queue.put((user_id, user_data))
```

### Write-Around Pattern

Application writes directly to database, cache is populated on read.

```python
# Python - Write-Around Pattern
def update_user(user_id: int, user_data: dict):
    # Write directly to database, bypass cache
    database.execute(
        "UPDATE users SET name = %s, email = %s WHERE id = %s",
        (user_data['name'], user_data['email'], user_id)
    )

    # Delete from cache if it exists (will be re-populated on next read)
    redis_client.delete(f"user:{user_id}")

def get_user(user_id: int) -> dict:
    cache_key = f"user:{user_id}"

    cached = redis_client.get(cache_key)
    if cached:
        return json.loads(cached)

    # Load from database and populate cache
    user = database.query("SELECT * FROM users WHERE id = %s", (user_id,))
    if user:
        redis_client.setex(cache_key, 3600, json.dumps(user))

    return user
```

## Redis Data Structure Operations

### String Operations

```python
# Basic string operations
redis_client.set("key", "value")              # SET key value
redis_client.get("key")                       # GET key -> "value"
redis_client.setex("key", 3600, "value")      # SETEX key 3600 value (with TTL)
redis_client.setnx("lock:key", "locked")      # SETNX (set if not exists)
redis_client.append("key", " suffix")         # APPEND key " suffix"
redis_client.mset({"k1": "v1", "k2": "v2"})  # MSET k1 v1 k2 v2
redis_client.mget(["k1", "k2"])              # MGET k1 k2 -> ["v1", "v2"]

# Atomic counters
redis_client.incr("page:views")               # INCR -> 1
redis_client.incrby("page:views", 10)         # INCRBY 10 -> 11
redis_client.decr("page:views")               # DECR -> 10
redis_client.incrbyfloat("price", 2.5)        # INCRBYFLOAT 2.5
```

### Hash Operations

```python
# Hash operations - ideal for object storage
redis_client.hset("user:1001", mapping={      # HSET multiple fields
    "name": "John Doe",
    "email": "john@example.com",
    "age": "30"
})
redis_client.hget("user:1001", "name")        # HGET -> "John Doe"
redis_client.hgetall("user:1001")             # HGETALL -> {name, email, age}
redis_client.hdel("user:1001", "age")         # HDEL field
redis_client.hincrby("user:1001", "age", 1)   # HINCRBY field 1
redis_client.hexists("user:1001", "email")    # HEXISTS -> True
redis_client.hlen("user:1001")                # HLEN -> 2
redis_client.hkeys("user:1001")               # HKEYS -> [name, email]
```

### List Operations

```python
# List operations - queue and stack patterns
redis_client.lpush("queue:tasks", "task1")    # LPUSH -> 1
redis_client.rpush("queue:tasks", "task2")    # RPUSH -> 2
redis_client.lpop("queue:tasks")              # LPOP -> "task1" (FIFO queue)
redis_client.rpop("queue:tasks")              # RPOP -> "task2" (LIFO stack)
redis_client.lrange("queue:tasks", 0, -1)     # LRANGE 0 -1 -> all elements
redis_client.llen("queue:tasks")              # LLEN -> length
redis_client.lindex("queue:tasks", 0)         # LINDEX 0 -> first element

# Blocking pop (for consumer queues)
redis_client.blpop("queue:tasks", timeout=5)  # BLPOP with 5s timeout
redis_client.brpop("queue:tasks", timeout=5)  # BRPOP with 5s timeout
```

### Set Operations

```python
# Set operations - unique members and set algebra
redis_client.sadd("post:1:tags", "python", "redis", "caching")  # SADD
redis_client.srem("post:1:tags", "caching")                      # SREM
redis_client.smembers("post:1:tags")                             # SMEMBERS -> {python, redis}
redis_client.sismember("post:1:tags", "python")                  # SISMEMBER -> True
redis_client.scard("post:1:tags")                                # SCARD -> 2

# Set algebra
redis_client.sadd("user:1:interests", "tech", "sports", "music")
redis_client.sadd("user:2:interests", "tech", "gaming", "music")
redis_client.sinter("user:1:interests", "user:2:interests")      # SINTER -> {tech, music}
redis_client.sunion("user:1:interests", "user:2:interests")      # SUNION -> {tech, sports, music, gaming}
redis_client.sdiff("user:1:interests", "user:2:interests")       # SDIFF -> {sports}
```

### Sorted Set Operations

```python
# Sorted set operations - leaderboards and rankings
redis_client.zadd("leaderboard", {           # ZADD multiple members
    "player1": 1500,
    "player2": 2300,
    "player3": 1800
})
redis_client.zincrby("leaderboard", 100, "player1")  # ZINCRBY -> 1600
redis_client.zrem("leaderboard", "player3")           # ZREM member

# Range queries
redis_client.zrange("leaderboard", 0, -1)             # ZRANGE (ascending)
redis_client.zrevrange("leaderboard", 0, -1)          # ZREVRANGE (descending)
redis_client.zrange("leaderboard", 0, 9, withscores=True)  # Top 10 with scores

# Rankings
redis_client.zrank("leaderboard", "player1")          # ZRANK (ascending)
redis_client.zrevrank("leaderboard", "player1")       # ZREVRANK (descending)
redis_client.zscore("leaderboard", "player1")         # ZSCORE -> 1600.0
redis_client.zcard("leaderboard")                     # ZCARD -> count
```

### Stream Operations

```python
# Stream operations - message queuing
redis_client.xadd("orders:stream", {"order_id": "123", "amount": "99.99"})
# -> "1697012345678-0"

redis_client.xadd("orders:stream", {"order_id": "124", "amount": "149.99"})
# -> "1697012345679-0"

# Read stream
redis_client.xread({"orders:stream": "0-0"}, count=10)  # Read from beginning
redis_client.xread({"orders:stream": "$"}, count=10, block=5000)  # Block for new entries

# Consumer groups
redis_client.xgroup_create("orders:stream", "workers", id="0-0", mkstream=True)
redis_client.xreadgroup("workers", "worker-1", {"orders:stream": ">-"}, count=1)
redis_client.xack("orders:stream", "workers", ["1697012345678-0"])

# Stream info
redis_client.xlen("orders:stream")  # Stream length
```

### Bitmap Operations

```python
# Bitmap operations - feature flags and presence tracking
redis_client.setbit("user:active:2024:01", 15, 1)   # User 15 active on Jan 15
redis_client.setbit("user:active:2024:01", 16, 1)   # User 16 active on Jan 16
redis_client.getbit("user:active:2024:01", 15)      # -> 1 (active)
redis_client.bitcount("user:active:2024:01")         # -> 2 (active users in January)

# Feature flags
redis_client.setbit("feature:dark_mode:enabled", 1001, 1)  # Enable for user 1001
redis_client.getbit("feature:dark_mode:enabled", 1001)      # -> 1
```

### HyperLogLog Operations

```python
# HyperLogLog - unique visitor counting (approximate)
redis_client.pfadd("website:visitors:2024:01", "user1", "user2", "user3")
redis_client.pfadd("website:visitors:2024:01", "user2")     # Duplicate ignored
redis_client.pfcount("website:visitors:2024:01")            # -> 3

# Merge multiple HyperLogLogs
redis_client.pfadd("site:a:visitors", "user1", "user2")
redis_client.pfadd("site:b:visitors", "user2", "user3")
redis_client.pfmerge("total:visitors", ["site:a:visitors", "site:b:visitors"])
redis_client.pfcount("total:visitors")                       # -> 3
```

### Geospatial Operations

```python
# Geospatial operations - location-based queries
redis_client.geoadd("cities", {
    "rome": (12.49, 41.90),
    "milan": (9.19, 45.46),
    "naples": (14.25, 40.85)
})

# Distance query
redis_client.geodist("cities", "rome", "milan", unit="km")   # -> 504.27 km

# Radius query
redis_client.georadius("cities", 13.0, 41.0, 200, unit="km", withdist=True, withcoord=True)

# Geo hash
redis_client.geohash("cities", "rome", "milan")              # -> ["sqc8b49rYG0", "sqdtr74hvu0"]
```

## Session Management with Redis

### Basic Session Store

```python
# Python - Redis session management
import uuid
import json
from datetime import datetime, timedelta

SESSION_PREFIX = "session:"
SESSION_TTL = 3600  # 1 hour

def create_session(user_id: int, user_data: dict) -> str:
    session_id = str(uuid.uuid4())
    session_key = f"{SESSION_PREFIX}{session_id}"

    session_data = {
        "user_id": user_id,
        "data": user_data,
        "created_at": datetime.utcnow().isoformat(),
        "expires_at": (datetime.utcnow() + timedelta(seconds=SESSION_TTL)).isoformat()
    }

    redis_client.setex(
        session_key,
        SESSION_TTL,
        json.dumps(session_data)
    )

    return session_id

def get_session(session_id: str) -> dict:
    session_key = f"{SESSION_PREFIX}{session_id}"
    data = redis_client.get(session_key)

    if not data:
        return None

    session = json.loads(data)

    # Refresh TTL on access
    redis_client.expire(session_key, SESSION_TTL)

    return session

def delete_session(session_id: str):
    session_key = f"{SESSION_PREFIX}{session_id}"
    redis_client.delete(session_key)
```

### Distributed Session with Express (Node.js)

```javascript
// Node.js - Express session with connect-redis
const express = require('express');
const session = require('express-session');
const RedisStore = require('connect-redis').default;
const Redis = require('ioredis');

const redis = new Redis({ host: 'localhost', port: 6379 });
const app = express();

app.use(
  session({
    store: new RedisStore({ client: redis }),
    secret: 'your-secret-key',
    resave: false,
    saveUninitialized: false,
    cookie: {
      secure: true, // HTTPS only
      httpOnly: true, // No JavaScript access
      maxAge: 3600000, // 1 hour
      sameSite: 'strict',
    },
  })
);
```

## Pub/Sub Messaging

### Basic Pub/Sub

```python
# Python - Redis pub/sub
import redis
import threading

redis_client = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Publisher
def publish_message(channel: str, message: str):
    redis_client.publish(channel, message)
    print(f"Published to {channel}: {message}")

# Subscriber
class MessageSubscriber:
    def __init__(self, channels: list):
        self.pubsub = redis_client.pubsub()
        self.pubsub.subscribe(*channels)
        self.running = True

    def listen(self):
        while self.running:
            message = self.pubsub.get_message(ignore_subscribe_messages=True)
            if message:
                print(f"Received on {message['channel']}: {message['data']}")
                # Process message...

    def stop(self):
        self.running = False
        self.pubsub.unsubscribe()
        self.pubsub.close()

# Start subscriber in background thread
subscriber = MessageSubscriber(['notifications', 'alerts'])
threading.Thread(target=subscriber.listen, daemon=True).start()

# Publish messages
publish_message('notifications', 'New message received')
publish_message('alerts', 'System alert triggered')
```

```javascript
// Node.js - Redis pub/sub with ioredis
const Redis = require('ioredis');

const publisher = new Redis();
const subscriber = new Redis();

// Subscribe to channels
subscriber.subscribe('news:tech', 'news:science', (err, count) => {
  console.log(`Subscribed to ${count} channels`);
});

// Handle messages
subscriber.on('message', (channel, message) => {
  console.log(`${channel}: ${message}`);
});

// Publish messages
publisher.publish('news:tech', 'Redis 7.0 released');
publisher.publish('news:science', 'New quantum computing breakthrough');

// Pattern matching
subscriber.psubscribe('news:*', (err, count) => {
  console.log(`Subscribed to pattern: news:*`);
});
```

### Pattern Subscriptions

```python
# Pattern subscriptions - subscribe to multiple channels with wildcards
pubsub = redis_client.pubsub()
pubsub.psubscribe('user:*:activity', 'order:*:status')

for message in pubsub.listen():
    if message['type'] == 'pmessage':
        pattern = message['pattern']
        channel = message['channel']
        data = message['data']
        print(f"[{pattern}] {channel}: {data}")
```

## Lua Scripting for Atomic Operations

### Why Lua Scripting?

Lua scripts execute atomically on the Redis server, eliminating race conditions without client-side locking.

```python
# Atomic increment with conditional update
lua_script = """
local current = redis.call('GET', KEYS[1])
if current then
    current = tonumber(current)
    if current < tonumber(ARGV[1]) then  -- max limit
        current = current + 1
        redis.call('SET', KEYS[1], current)
        return current
    end
    return -1  -- limit reached
end
-- Key doesn't exist, create it
redis.call('SET', KEYS[1], 1)
return 1
"""

# Register script for reuse
atomic_incr = redis_client.register_script(lua_script)

# Execute atomically
result = atomic_incr(keys=["rate_limit:user:1001"], args=[100])  # max 100 requests
if result == -1:
    print("Rate limit exceeded!")
```

### Distributed Lock with Lua

```python
# Distributed lock implementation
acquire_lock_script = """
if redis.call('SETNX', KEYS[1], ARGV[1]) == 1 then
    redis.call('PEXPIRE', KEYS[1], ARGV[2])
    return 1
end
return 0
"""

release_lock_script = """
if redis.call('GET', KEYS[1]) == ARGV[1] then
    return redis.call('DEL', KEYS[1])
end
return 0
"""

import uuid

acquire_lock = redis_client.register_script(acquire_lock_script)
release_lock = redis_client.register_script(release_lock_script)

def acquire_distributed_lock(lock_name: str, timeout_ms: int = 5000) -> str:
    lock_id = str(uuid.uuid4())
    success = acquire_lock(keys=[f"lock:{lock_name}"], args=[lock_id, timeout_ms])
    if success:
        return lock_id
    return None

def release_distributed_lock(lock_name: str, lock_id: str):
    release_lock(keys=[f"lock:{lock_name}"], args=[lock_id])

# Usage
lock_id = acquire_distributed_lock("critical_operation", timeout_ms=10000)
if lock_id:
    try:
        # Critical section
        perform_critical_operation()
    finally:
        release_distributed_lock("critical_operation", lock_id)
```

### Cache-Aside with Atomic Check-and-Set

```python
# Prevent cache stampede with Lua scripting
lua_cache_script = """
local cached = redis.call('GET', KEYS[1])
if cached then
    return cached
end
-- Check if another instance is already regenerating
if redis.call('SETNX', KEYS[2], 1) == 1 then
    redis.call('EXPIRE', KEYS[2], ARGV[2])
    return ''  -- Signal to regenerate
else
    return false  -- Signal to wait
end
"""

def get_with_stampede_protection(key: str, ttl: int = 3600):
    cache_key = f"cache:{key}"
    lock_key = f"lock:cache:{key}"

    check_and_lock = redis_client.register_script(lua_cache_script)
    result = check_and_lock(keys=[cache_key, lock_key], args=[ttl, 10])

    if result and result != b'':
        return json.loads(result)  # Cache hit

    if result == b'':
        # We won the lock, regenerate cache
        try:
            data = expensive_database_query(key)
            redis_client.setex(cache_key, ttl, json.dumps(data))
            return data
        finally:
            redis_client.delete(lock_key)
    else:
        # Another instance is regenerating, wait and retry
        import time
        time.sleep(0.1)
        return get_with_stampede_protection(key, ttl)
```

## Transactions and Pipelines

### Transactions (MULTI/EXEC)

```python
# Transaction - atomic group of commands
pipe = redis_client.pipeline(transaction=True)
try:
    pipe.multi()
    pipe.set("user:1001:name", "John Doe")
    pipe.set("user:1001:email", "john@example.com")
    pipe.hincrby("user:stats", "login_count", 1)
    pipe.expire("user:1001:name", 3600)
    pipe.expire("user:1001:email", 3600)
    results = pipe.execute()
except Exception as e:
    print(f"Transaction failed: {e}")
```

### Pipelines for Batch Operations

```python
# Pipeline - batch commands for efficiency (without transaction)
pipe = redis_client.pipeline(transaction=False)

# Batch GET operations
for user_id in range(1, 101):
    pipe.get(f"user:{user_id}:name")
names = pipe.execute()

# Batch SET operations
pipe = redis_client.pipeline(transaction=False)
for i, item in enumerate(large_dataset):
    pipe.hset(f"item:{i}", mapping=item)
pipe.execute()

# Watch for optimistic locking
redis_client.watch("account:balance:1001")
balance = int(redis_client.get("account:balance:1001"))

if balance >= 100:
    pipe = redis_client.pipeline(transaction=True)
    pipe.multi()
    pipe.set("account:balance:1001", balance - 100)
    pipe.rpush("account:transactions:1001", json.dumps({
        "type": "debit",
        "amount": 100,
        "timestamp": datetime.utcnow().isoformat()
    }))
    pipe.execute()  # Will fail if balance was modified by another client
else:
    redis_client.unwatch()
    print("Insufficient balance")
```

### Pipeline Performance Comparison

```python
# ❌ Slow: Individual commands (100 round trips)
for i in range(100):
    redis_client.set(f"key:{i}", f"value:{i}")

# ✅ Fast: Pipeline (1 round trip)
pipe = redis_client.pipeline(transaction=False)
for i in range(100):
    pipe.set(f"key:{i}", f"value:{i}")
pipe.execute()

# Performance: Pipeline can be 10-100x faster for batch operations
```

## Redis Clustering, Sentinel, and Replication

### Redis Clustering (Horizontal Scaling)

Redis Cluster provides horizontal scaling by sharding data across multiple nodes.

```python
# Python - Redis Cluster with redis-py
from redis.cluster import RedisCluster, ClusterNode

startup_nodes = [
    ClusterNode("cluster-node-1", 7000),
    ClusterNode("cluster-node-2", 7001),
    ClusterNode("cluster-node-3", 7002),
]

redis_cluster = RedisCluster(
    startup_nodes=startup_nodes,
    decode_responses=True,
    skip_full_coverage_check=True
)

# Usage is the same as single Redis instance
redis_cluster.set("key", "value")
redis_cluster.get("key")

# Cluster-specific operations
redis_cluster.cluster_info()
redis_cluster.cluster_nodes()
```

```javascript
// Node.js - Redis Cluster with ioredis
const Redis = require('ioredis');

const cluster = new Redis.Cluster(
  [
    { host: 'cluster-node-1', port: 7000 },
    { host: 'cluster-node-2', port: 7001 },
    { host: 'cluster-node-3', port: 7002 },
  ],
  {
    slots: {
      // Optional: pre-define slot mapping
    },
    scaleReads: 'slave', // Read from replicas
    retryAttempts: 3,
    retryDelay: 100,
  }
);

cluster.on('error', (err) => console.error('Cluster error:', err));
```

### Redis Sentinel (High Availability)

Sentinel provides automatic failover for master-replica setups.

```python
# Python - Redis Sentinel with redis-py
from redis.sentinel import Sentinel

sentinel = Sentinel(
    [('sentinel-1', 26379), ('sentinel-2', 26379), ('sentinel-3', 26379)],
    socket_timeout=0.5,
    decode_responses=True
)

# Get master connection (automatically discovers current master)
master = sentinel.master_for('mymaster', socket_timeout=0.5)
master.set('key', 'value')

# Get replica connection (for read scaling)
slave = sentinel.slave_for('mymaster', socket_timeout=0.5)
value = slave.get('key')
```

```javascript
// Node.js - Redis Sentinel with ioredis
const Redis = require('ioredis');

const sentinel = new Redis.Sentinel(
  [
    { host: 'sentinel-1', port: 26379 },
    { host: 'sentinel-2', port: 26379 },
    { host: 'sentinel-3', port: 26379 },
  ],
  {
    name: 'mymaster',
    sentinelRetryStrategy: (times) => Math.min(times * 50, 2000),
  }
);

// Auto-discover master
const master = new Redis({
  sentinels: [
    { host: 'sentinel-1', port: 26379 },
    { host: 'sentinel-2', port: 26379 },
  ],
  name: 'mymaster',
});
```

### Redis Replication Configuration

```yaml
# docker-compose.yml - Master-Replica setup
version: '3.8'

services:
  redis-master:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - '6379:6379'
    volumes:
      - ./redis-master.conf:/usr/local/etc/redis/redis.conf
      - redis-master-data:/data

  redis-replica-1:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - '6380:6379'
    volumes:
      - ./redis-replica-1.conf:/usr/local/etc/redis/redis.conf
      - redis-replica-1-data:/data
    depends_on:
      - redis-master

  redis-replica-2:
    image: redis:7-alpine
    command: redis-server /usr/local/etc/redis/redis.conf
    ports:
      - '6381:6379'
    volumes:
      - ./redis-replica-2.conf:/usr/local/etc/redis/redis.conf
      - redis-replica-2-data:/data
    depends_on:
      - redis-master

  redis-sentinel-1:
    image: redis:7-alpine
    command: redis-sentinel /usr/local/etc/redis/sentinel.conf
    ports:
      - '26379:26379'
    volumes:
      - ./sentinel-1.conf:/usr/local/etc/redis/sentinel.conf
    depends_on:
      - redis-master

volumes:
  redis-master-data:
  redis-replica-1-data:
  redis-replica-2-data:
```

```conf
# redis-master.conf
bind 0.0.0.0
port 6379
protected-mode no
appendonly yes
appendfilename "appendonly.aof"

# redis-replica-1.conf
bind 0.0.0.0
port 6379
protected-mode no
replicaof redis-master 6379
appendonly yes

# sentinel-1.conf
port 26379
sentinel monitor mymaster redis-master 6379 2
sentinel down-after-milliseconds mymaster 5000
sentinel failover-timeout mymaster 10000
sentinel parallel-syncs mymaster 1
```

## Persistence Configuration

### RDB Persistence (Snapshot-based)

```conf
# redis.conf - RDB Configuration
# Save snapshots at specified intervals
save 900 1     # Save after 900 sec (15 min) if at least 1 key changed
save 300 10    # Save after 300 sec (5 min) if at least 10 keys changed
save 60 10000  # Save after 60 sec if at least 10000 keys changed

# RDB file settings
dbfilename dump.rdb
dir /data
rdbcompression yes
rdbchecksum yes

# Stop writes on RDB save error
stop-writes-on-bgsave-error yes
```

```python
# Trigger RDB snapshot programmatically
redis_client.save()      # Synchronous (blocks server)
redis_client.bgsave()    # Asynchronous (recommended)
redis_client.lastsave()  # Get timestamp of last successful save
```

### AOF Persistence (Append-Only File)

```conf
# redis.conf - AOF Configuration
appendonly yes
appendfilename "appendonly.aof"

# Fsync policy:
# always    - fsync every write (slowest, most durable)
# everysec  - fsync every second (recommended balance)
# no        - let OS decide (fastest, least durable)
appendfsync everysec

# Auto-rewrite AOF when it grows too large
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb

# Allow AOF rewrite during BGSAVE
no-appendfsync-on-rewrite no
```

```python
# Trigger AOF rewrite programmatically
redis_client.bgrewriteaof()  # Asynchronous AOF rewrite
```

### RDB + AOF (Recommended Production Setup)

```conf
# Best of both worlds: fast recovery (RDB) + durability (AOF)
save 900 1
save 300 10
save 60 10000

appendonly yes
appendfsync everysec
auto-aof-rewrite-percentage 100
auto-aof-rewrite-min-size 64mb
```

## Memory Management and Eviction Policies

### Memory Configuration

```conf
# redis.conf - Memory Settings
maxmemory 2gb                    # Maximum memory limit
maxmemory-policy allkeys-lru     # Eviction policy
maxmemory-samples 10             # LRU approximation accuracy (higher = more accurate, slower)
```

### Eviction Policies

| Policy              | Behavior                  | Use Case                      |
| ------------------- | ------------------------- | ----------------------------- |
| **volatile-lru**    | LRU on keys with TTL      | Mixed cache + persistent data |
| **allkeys-lru**     | LRU on all keys           | Pure cache                    |
| **volatile-lfu**    | LFU on keys with TTL      | Frequency-based cache         |
| **allkeys-lfu**     | LFU on all keys           | Frequency-based pure cache    |
| **volatile-random** | Random on keys with TTL   | Simple random eviction        |
| **allkeys-random**  | Random on all keys        | Simple random eviction        |
| **volatile-ttl**    | Earliest TTL expiration   | TTL-priority eviction         |
| **noeviction**      | Never evict, return error | Data store (not cache)        |

```python
# Check memory usage
redis_client.info('memory')
redis_client.dbsize()           # Number of keys
redis_client.memory_usage("key") # Memory used by specific key

# Memory optimization
redis_client.object("encoding", "key")  # Check internal encoding
redis_client.object("idletime", "key")  # Check idle time (for LRU)
```

### TTL Management Strategies

```python
# TTL strategies for different use cases

# Short-lived cache (API responses)
redis_client.setex("api:response:user:1001", 60, json.dumps(user_data))

# Medium-lived cache (session data)
redis_client.setex("session:abc123", 1800, json.dumps(session_data))

# Long-lived cache (configuration)
redis_client.setex("config:app_settings", 86400, json.dumps(config))

# Randomized TTL to prevent thundering herd
import random
base_ttl = 3600
jitter = random.randint(-300, 300)  # ±5 minutes
ttl = base_ttl + jitter
redis_client.setex("product:1001", ttl, json.dumps(product_data))

# Check and update TTL
if redis_client.ttl("key") < 60:  # Less than 60 seconds remaining
    redis_client.expire("key", 3600)  # Refresh TTL

# Remove TTL (make key persistent)
redis_client.persist("key")
```

## Connection Pooling

### Python (redis-py)

```python
import redis

# Connection pool (recommended)
pool = redis.ConnectionPool(
    host='localhost',
    port=6379,
    db=0,
    max_connections=20,
    decode_responses=True,
    socket_connect_timeout=5,
    socket_timeout=5,
    retry_on_timeout=True
)

redis_client = redis.Redis(connection_pool=pool)

# Share pool across multiple clients
redis_client_1 = redis.Redis(connection_pool=pool)
redis_client_2 = redis.Redis(connection_pool=pool)
```

### Node.js (ioredis)

```javascript
const Redis = require('ioredis');

// ioredis has built-in connection pooling
const redis = new Redis({
  host: 'localhost',
  port: 6379,
  maxRetriesPerRequest: 3,
  lazyConnect: true,
  enableReadyCheck: true,
  connectTimeout: 10000,
  retryStrategy: (times) => {
    if (times > 3) return null; // Give up after 3 retries
    return Math.min(times * 50, 2000);
  },
});

// Connection events
redis.on('connect', () => console.log('Connected to Redis'));
redis.on('error', (err) => console.error('Redis error:', err));
redis.on('ready', () => console.log('Redis ready'));
redis.on('reconnecting', (ms) => console.log(`Reconnecting in ${ms}ms`));
```

### Java (Lettuce)

```java
import io.lettuce.core.RedisClient;
import io.lettuce.core.api.StatefulRedisConnection;
import io.lettuce.core.api.sync.RedisCommands;

// Lettuce with connection pooling
RedisClient client = RedisClient.create("redis://localhost:6379");
StatefulRedisConnection<String, String> connection = client.connect();
RedisCommands<String, String> sync = connection.sync();

sync.set("key", "value");
String value = sync.get("key");

// Close connection
connection.close();
client.close();
```

## Best Practices

### Key Naming Conventions

```python
# ✅ GOOD: Namespace with colons
redis_client.set("user:1001:name", "John")
redis_client.set("user:1001:email", "john@example.com")
redis_client.set("product:42:inventory", "150")
redis_client.set("session:abc123", session_data)
redis_client.set("cache:api:users:list", users_json)

# ❌ BAD: No namespace or inconsistent naming
redis_client.set("name", "John")           # No context
redis_client.set("user_1001_name", "John")  # Underscores instead of colons
redis_client.set("1001", "John")           # No type indicator
```

### Value Size Guidelines

| Value Size   | Recommendation                         |
| ------------ | -------------------------------------- |
| < 1KB        | Ideal for Redis                        |
| 1KB - 10KB   | Acceptable                             |
| 10KB - 100KB | Consider compression or splitting      |
| > 100KB      | Avoid - use database or object storage |

### Anti-Patterns to Avoid

```python
# ❌ BAD: Blocking operations on large collections
redis_client.smembers("large_set_with_millions_of_members")  # Blocks Redis!

# ✅ GOOD: Use scanning for large collections
for member in redis_client.sscan_iter("large_set"):
    process(member)

# ❌ BAD: KEYS command in production
redis_client.keys("*")  # Blocks Redis on large datasets!

# ✅ GOOD: SCAN for key iteration
for key in redis_client.scan_iter("user:*"):
    process(key)

# ❌ BAD: No TTL on cache keys
redis_client.set("cache:key", "value")  # Will never expire!

# ✅ GOOD: Always set TTL on cache keys
redis_client.setex("cache:key", 3600, "value")  # Expires in 1 hour

# ❌ BAD: Large hash field retrieval
redis_client.hgetall("user:1001")  # May contain many fields

# ✅ GOOD: Get specific fields
redis_client.hmget("user:1001", ["name", "email"])

# ❌ BAD: Not handling Redis failures
value = redis_client.get("key")  # May raise exception

# ✅ GOOD: Graceful degradation
try:
    value = redis_client.get("key")
except redis.ConnectionError:
    value = fetch_from_database()  # Fallback to database

# ❌ BAD: Storing sensitive data unencrypted
redis_client.set("user:1001:password", "plaintext_password")

# ✅ GOOD: Never store sensitive data in Redis
# Hash passwords before storing, or don't store at all
```

### Rate Limiting Implementation

```python
# Token bucket rate limiter
class RateLimiter:
    def __init__(self, redis_client, key_prefix="rate_limit"):
        self.redis = redis_client
        self.key_prefix = key_prefix

    def is_allowed(self, identifier: str, max_requests: int, window_seconds: int) -> bool:
        key = f"{self.key_prefix}:{identifier}"
        current = self.redis.get(key)

        if current is None:
            self.redis.setex(key, window_seconds, 1)
            return True

        if int(current) < max_requests:
            self.redis.incr(key)
            return True

        return False

# Usage
limiter = RateLimiter(redis_client)
if limiter.is_allowed("user:1001", max_requests=100, window_seconds=3600):
    process_request()
else:
    return "Rate limit exceeded", 429
```

### Real-time Analytics with Sorted Sets

```python
# Track user activity with sorted sets
from datetime import datetime

def track_page_view(user_id: int, page: str):
    now = datetime.utcnow().timestamp()
    key = f"analytics:page_views:{page}"

    # Add to sorted set with timestamp as score
    redis_client.zadd(key, {f"{user_id}:{now}": now})

    # Clean up old entries (older than 30 days)
    cutoff = now - (30 * 86400)
    redis_client.zremrangebyscore(key, 0, cutoff)

def get_daily_page_views(page: str, days: int = 7) -> dict:
    key = f"analytics:page_views:{page}"
    now = datetime.utcnow().timestamp()

    views = {}
    for day in range(days):
        day_start = now - ((days - day) * 86400)
        day_end = day_start + 86400
        count = redis_client.zcount(key, day_start, day_end)
        views[f"day_{day}"] = count

    return views
```

## Production Checklist

Before deploying Redis to production:

- [ ] Set appropriate `maxmemory` limit
- [ ] Configure eviction policy (`allkeys-lru` for cache)
- [ ] Enable persistence (RDB + AOF recommended)
- [ ] Set up monitoring and alerting
- [ ] Configure connection pooling
- [ ] Use TLS/SSL for connections
- [ ] Set authentication password
- [ ] Configure proper TTL for all cache keys
- [ ] Test failover scenario (Sentinel or Cluster)
- [ ] Set up backup strategy
- [ ] Monitor memory usage and eviction rate
- [ ] Use connection timeouts
- [ ] Implement graceful degradation on Redis failure
- [ ] Avoid blocking commands (KEYS, FLUSHALL)
- [ ] Use SCAN instead of KEYS
- [ ] Keep values under 100KB
- [ ] Use pipelines for batch operations
- [ ] Test under load before production

## Real-World Impact

**Before this skill:**

- No caching layer, direct database queries
- Slow response times (200-500ms)
- Database overload under traffic spikes
- No session management
- Race conditions in concurrent operations
- No rate limiting

**After this skill:**

- Multi-layer caching strategy
- Fast response times (1-10ms for cached data)
- Reduced database load by 80-95%
- Distributed session management
- Atomic operations with Lua scripting
- Production-ready Redis configuration
- Horizontal scaling with clustering

## Cross-References

- **`docker-containerization`** - For containerizing Redis instances
- **`kubernetes-orchestration`** - For deploying Redis to Kubernetes
- **`database-design`** - For primary database design
- **`microservices-architecture`** - For Redis in microservices
- **`performance`** - For application performance optimization
- **`security-audit`** - For Redis security hardening

## References

- [Redis Documentation](https://redis.io/documentation)
- [Redis Commands](https://redis.io/commands/)
- [Redis Best Practices](https://redis.io/docs/manual/best-practices/)
- [Redis Cluster Specification](https://redis.io/docs/manual/scaling/)
- [Redis Persistence](https://redis.io/docs/manual/persistence/)
- [Redis Memory Management](https://redis.io/docs/manual/memory-management/)
- [Redis Lua Scripting](https://redis.io/docs/manual/programmability/)
- [ioredis Documentation](https://redis.github.io/ioredis/)
- [redis-py Documentation](https://redis-py.readthedocs.io/)
- [Lettuce Documentation](https://lettuce.io/)
- [Redis University](https://university.redis.com/)
