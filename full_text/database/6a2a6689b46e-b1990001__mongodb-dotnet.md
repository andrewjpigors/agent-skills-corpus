---
name: mongodb-dotnet
description: "Expert on MongoDB with .NET. Covers driver usage, schema design, queries, indexing, aggregation, and best practices."
role: specialist
scope: implementation
output-format: code
---

# MongoDB with .NET

## Overview

Expert guidance for using MongoDB with .NET applications. Covers the official MongoDB.Driver, schema design, query optimization, and production best practices.

## Core Patterns

**Connection and Configuration:**
```csharp
// Registration in Program.cs
builder.Services.AddSingleton<IMongoClient>(sp =>
{
    var settings = MongoClientSettings.FromConnectionString(
        builder.Configuration.GetConnectionString("MongoDB"));
    settings.ServerApi = new ServerApi(ServerApiVersion.V1);
    return new MongoClient(settings);
});

builder.Services.AddScoped(sp =>
{
    var client = sp.GetRequiredService<IMongoClient>();
    return client.GetDatabase("myapp");
});
```

**Base Entity:**
```csharp
public abstract class BaseMongoEntity
{
    [BsonId]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = null!;

    [BsonElement("etag")]
    public string ETag { get; set; } = null!;

    [BsonElement("created_at")]
    [BsonRepresentation(BsonType.Document)]
    public DateTimeOffset CreatedAt { get; set; }

    [BsonElement("updated_at")]
    [BsonRepresentation(BsonType.Document)]
    public DateTimeOffset UpdatedAt { get; set; }

    [BsonIgnoreIfNull]
    [BsonElement("deleted_at")]
    [BsonRepresentation(BsonType.Document)]
    public DateTimeOffset? DeletedAt { get; set; }

    [BsonExtraElements]
    public Dictionary<string, object>? ExtraElements { get; set; }
}
```

**Entity Design:**
```csharp
public class UserEntity : BaseMongoEntity
{
    [BsonElement("email")]
    public string Email { get; set; } = null!;

    [BsonIgnoreIfNull]
    [BsonElement("profile")]
    public UserProfileEntity? Profile { get; set; }
}
```

**Base Repository:**
```csharp
public abstract class BaseMongoDbRepository<TEntity> where TEntity : BaseMongoEntity
{
    protected readonly IMongoCollection<TEntity> Collection;
    private readonly ILogger _logger;

    protected BaseMongoDbRepository(IMongoDatabase database, string collectionName, ILogger logger)
    {
        Collection = database.GetCollection<TEntity>(collectionName);
        _logger = logger;
    }

    public async Task<TEntity?> GetByIdAsync(string id, CancellationToken ct = default)
    {
        return await Collection.Find(e => e.Id == id).FirstOrDefaultAsync(ct);
    }

    public async Task<ICollection<TEntity>> GetByIdsAsync(IEnumerable<string> ids, CancellationToken ct = default)
    {
        var filter = Builders<TEntity>.Filter.In(e => e.Id, ids);
        return await Collection.Find(filter).ToListAsync(ct);
    }

    public async Task<IAsyncCursor<TEntity>> FilterAsync(
        FilterDefinition<TEntity> filter,
        int skip = 0,
        int take = 100,
        CancellationToken ct = default)
    {
#if DEBUG
        AnalyzeQuery(filter);
#endif
        return await Collection.Find(filter).Skip(skip).Limit(take).ToCursorAsync(ct);
    }

    public async Task<List<TResult>> AggregateAsync<TResult>(
        Func<IAggregateFluent<TEntity>, IAggregateFluent<TResult>> pipeline,
        CancellationToken ct = default)
    {
        var aggregate = Collection.Aggregate();
        return await pipeline(aggregate).ToListAsync(ct);
    }

    public async Task<IAsyncCursor<TEntity>> GetAllAsync(CancellationToken ct = default)
    {
        return await Collection.Find(Builders<TEntity>.Filter.Empty).ToCursorAsync(ct);
    }

    public async Task<TEntity> AddAsync(TEntity entity, CancellationToken ct = default)
    {
        entity.ETag = GenerateETag(entity);
        var now = DateTimeOffset.UtcNow;
        entity.CreatedAt = now;
        entity.UpdatedAt = now;
        await Collection.InsertOneAsync(entity, cancellationToken: ct);
        return entity;
    }

    public async Task<ICollection<TEntity>> AddManyAsync(List<TEntity> entities, CancellationToken ct = default)
    {
        var now = DateTimeOffset.UtcNow;
        foreach (var entity in entities)
        {
            entity.ETag = GenerateETag(entity);
            entity.CreatedAt = now;
            entity.UpdatedAt = now;
        }
        await Collection.InsertManyAsync(entities, cancellationToken: ct);
        return entities;
    }

    public async Task<TEntity> UpdateAsync(TEntity entity, CancellationToken ct = default)
    {
        entity.ETag = GenerateETag(entity);
        entity.UpdatedAt = DateTimeOffset.UtcNow;
        return await Collection.FindOneAndReplaceAsync(
            e => e.Id == entity.Id,
            entity,
            new FindOneAndReplaceOptions<TEntity> { ReturnDocument = ReturnDocument.After },
            ct);
    }

    public async Task<bool> DeleteAsync(string id, bool permanentlyDelete = false, CancellationToken ct = default)
    {
        if (permanentlyDelete)
        {
            var result = await Collection.DeleteOneAsync(e => e.Id == id, ct);
            return result.DeletedCount > 0;
        }

        var update = Builders<TEntity>.Update.Set(e => e.DeletedAt, DateTimeOffset.UtcNow);
        var updateResult = await Collection.UpdateOneAsync(e => e.Id == id, update, cancellationToken: ct);
        return updateResult.ModifiedCount > 0;
    }

    public async Task<long> DeleteManyAsync(IEnumerable<string> ids, bool permanentlyDelete = false, CancellationToken ct = default)
    {
        var filter = Builders<TEntity>.Filter.In(e => e.Id, ids);

        if (permanentlyDelete)
        {
            var result = await Collection.DeleteManyAsync(filter, ct);
            return result.DeletedCount;
        }

        var update = Builders<TEntity>.Update.Set(e => e.DeletedAt, DateTimeOffset.UtcNow);
        var updateResult = await Collection.UpdateManyAsync(filter, update, cancellationToken: ct);
        return updateResult.ModifiedCount;
    }

    private static string GenerateETag(TEntity entity)
    {
        var bytes = MessagePackSerializer.Serialize(entity);
        var hash = SHA1.HashData(bytes);
        return Convert.ToHexString(hash);
    }

#if DEBUG
    private void AnalyzeQuery(FilterDefinition<TEntity> filter)
    {
        var command = new BsonDocument
        {
            { "explain", new BsonDocument { { "find", Collection.CollectionNamespace.CollectionName }, { "filter", filter.Render(Collection.DocumentSerializer, Collection.Settings.SerializerRegistry) } } },
            { "verbosity", "executionStats" }
        };

        var result = Collection.Database.RunCommand<BsonDocument>(command);
        var winningPlan = result["queryPlanner"]?["winningPlan"]?.ToString() ?? "";

        if (winningPlan.Contains("COLLSCAN"))
        {
            _logger.LogWarning(
                "Collection scan detected for {Collection}. Consider adding an index. Filter: {Filter}",
                Collection.CollectionNamespace.CollectionName,
                filter.Render(Collection.DocumentSerializer, Collection.Settings.SerializerRegistry));
        }
    }
#endif
}
```

**Repository Implementation:**
```csharp
public class UserRepository(IMongoDatabase database, ILogger<UserRepository> logger)
    : BaseMongoDbRepository<UserEntity>(database, "users", logger), IUserRepository
{
    public async Task<UserEntity?> GetByEmailAsync(string email, CancellationToken ct = default)
    {
        return await Collection.Find(u => u.Email == email).FirstOrDefaultAsync(ct);
    }

    public async Task<List<UserEntity>> QueryAsync(
        UserQueryFilter filter,
        CancellationToken ct = default)
    {
        var builder = Builders<UserEntity>.Filter;
        var filters = new List<FilterDefinition<UserEntity>>();

        if (!string.IsNullOrEmpty(filter.Email))
            filters.Add(builder.Regex(u => u.Email, new BsonRegularExpression(filter.Email, "i")));

        if (filter.CreatedAfter.HasValue)
            filters.Add(builder.Gte(u => u.CreatedAt, filter.CreatedAfter.Value));

        var combinedFilter = filters.Count > 0
            ? builder.And(filters)
            : builder.Empty;

        return await Collection
            .Find(combinedFilter)
            .Skip(filter.Skip)
            .Limit(filter.Take)
            .ToListAsync(ct);
    }
}
```

## Aggregation Pipeline

```csharp
public async Task<List<UserStats>> GetUserStatsByMonthAsync(CancellationToken ct = default)
{
    return await _users.Aggregate()
        .Group(
            u => new { u.CreatedAt.Year, u.CreatedAt.Month },
            g => new UserStats
            {
                Year = g.Key.Year,
                Month = g.Key.Month,
                Count = g.Count()
            })
        .SortBy(s => s.Year)
        .ThenBy(s => s.Month)
        .ToListAsync(ct);
}
```

## Transactions

```csharp
public async Task TransferAsync(
    string fromId,
    string toId,
    decimal amount,
    CancellationToken ct = default)
{
    using var session = await _client.StartSessionAsync(cancellationToken: ct);

    await session.WithTransactionAsync(async (s, c) =>
    {
        var accounts = _database.GetCollection<AccountEntity>("accounts");

        await accounts.UpdateOneAsync(s,
            a => a.Id == fromId,
            Builders<AccountEntity>.Update.Inc(a => a.Balance, -amount),
            cancellationToken: c);

        await accounts.UpdateOneAsync(s,
            a => a.Id == toId,
            Builders<AccountEntity>.Update.Inc(a => a.Balance, amount),
            cancellationToken: c);

        return true;
    }, cancellationToken: ct);
}
```

## Change Streams

```csharp
public async Task WatchChangesAsync(CancellationToken ct = default)
{
    var pipeline = new EmptyPipelineDefinition<ChangeStreamDocument<UserEntity>>()
        .Match(change =>
            change.OperationType == ChangeStreamOperationType.Insert ||
            change.OperationType == ChangeStreamOperationType.Update);

    using var cursor = await _users.WatchAsync(pipeline, cancellationToken: ct);

    await cursor.ForEachAsync(change =>
    {
        Console.WriteLine($"{change.OperationType}: {change.FullDocument?.Email}");
    }, ct);
}
```

## Schema Design Principles

**Embed when:**
- Data is read together frequently
- Child data doesn't grow unbounded
- Updates are atomic

**Reference when:**
- Data is accessed independently
- Child collection can grow large
- Many-to-many relationships

**Example - Embedded:**
```csharp
public class OrderEntity : BaseMongoEntity
{
    [BsonElement("items")]
    public List<OrderItemEntity> Items { get; set; } = [];  // Embedded

    [BsonElement("shipping_address")]
    public AddressEntity ShippingAddress { get; set; } = null!;  // Embedded
}
```

**Example - Referenced:**
```csharp
// Use EntityReference to store id + display name together
public class EntityReference
{
    [BsonElement("_id")]
    [BsonRepresentation(BsonType.ObjectId)]
    public string Id { get; set; } = null!;

    [BsonElement("name")]
    public string Name { get; set; } = null!;
}

public class OrderEntity : BaseMongoEntity
{
    [BsonElement("customer")]
    public EntityReference Customer { get; set; } = null!;  // Reference with name

    [BsonElement("assigned_to")]
    public EntityReference? AssignedTo { get; set; }  // Optional reference
}
```

## Project Placement

When creating MongoDB-related classes in a .NET solution:

- **BaseMongoEntity** - Place in the database/data access project (e.g., `*.Database`, `*.Data`, `*.Infrastructure`), not in shared projects
- **BaseMongoDbRepository** - Place in the database project alongside `BaseMongoEntity`
- **Entity classes** - Place alongside `BaseMongoEntity` in the database project
- **Repositories** - Place in the database project, inheriting from `BaseMongoDbRepository<TEntity>`
- **IRepository interfaces** - Place in the domain/core project if using clean architecture, otherwise in the database project

The database project owns all MongoDB-specific concerns. Shared projects should only contain cross-cutting code that has no database dependencies.

## Key Principles

- **Use ObjectId for _id** - Let MongoDB generate IDs unless you have a natural key
- **Use BsonType.Document for DateTimeOffset** - Preserves both datetime and offset information
- **Use EntityReference for references** - Include _id + name to avoid lookups for display
- **Index query patterns** - Create indexes based on how you query, not how you think you'll query
- **Embed by default** - Start with embedding, extract to references when needed
- **Avoid unbounded arrays** - Don't embed arrays that can grow indefinitely
- **Use projections** - Only fetch fields you need with `.Project()`
- **Handle nulls explicitly** - Use `[BsonIgnoreIfNull]` to keep documents clean
- **Use BaseMongoEntity** - Inherit from base class for consistent Id and ExtraElements handling
- **Use BaseMongoDbRepository** - Inherit repositories from base class for standard CRUD operations
- **Soft delete by default** - Delete operations set `deleted_at` instead of removing documents; use `permanentlyDelete: true` only when necessary
- **Automatic timestamps** - `created_at` and `updated_at` are managed by the base repository; don't set them manually
