---
name: dotnet-api-expert
description: Use when building .NET 10+ applications with minimal APIs, clean architecture, or cloud-native microservices.
triggers:
  - .NET Core
  - .NET 8
  - .NET 9
  - .NET 10
  - ASP.NET Core
  - C# 12
  - C# 13
  - C# 14
  - Minimal API
  - Microservices .NET
role: specialist
scope: implementation
output-format: code
---

# .NET API Expert

**Official docs:** [.NET 10](https://learn.microsoft.com/en-us/dotnet/core/whats-new/dotnet-10/overview) | [C# 14](https://learn.microsoft.com/en-us/dotnet/csharp/whats-new/csharp-14) | [ASP.NET Core 10](https://learn.microsoft.com/en-us/aspnet/core/release-notes/aspnetcore-10.0)

## When to Use This Skill
Building minimal APIs with .NET 10+
Implementing JWT authentication and authorization
Optimizing performance with AOT compilation

## Required Reading
Before implementing, ALWAYS read these references:
- [references/clean-architecture.md](references/clean-architecture.md) - Project structure and layer placement
- [references/best-practices.md](references/best-practices.md) - Coding standards and conventions

## Core Workflow
1. Read references - Read clean-architecture.md and best-practices.md to understand project structure
2. Analyze requirements - Identify architecture pattern, data models, API design
3. Design solution - Create clean architecture layers with proper separation
4. Implement - Write high-performance code with modern C# features
5. Secure - Add authentication, authorization, and security best practices
6. Test - Write comprehensive integration and unit tests

## Reference Guide

| File | Topics |
|------|--------|
| [references/clean-architecture.md](references/clean-architecture.md) | Architecture, project structure |
| [references/best-practices.md](references/best-practices.md) | Best practices, do's and don'ts |
| [examples/api-layer.md](examples/api-layer.md) | API endpoints, validation filters |
| [examples/domain-layer.md](examples/domain-layer.md) | DTOs, services, interfaces |
| [examples/infrastructure-layer.md](examples/infrastructure-layer.md) | Infrastructure layer, entities, repositories |
| [examples/program-startup.md](examples/program-startup.md) | Program.cs, middleware order, DI registration |
| [examples/configuration.md](examples/configuration.md) | appsettings.json, typed options, validation |
| [examples/error-handling.md](examples/error-handling.md) | ErrorOr pattern, error extensions |
| [examples/testing.md](examples/testing.md) | NUnit, Moq, Bogus, WebApplicationFactory |
| [examples/http-clients.md](examples/http-clients.md) | IHttpClientFactory, typed clients, resilience |
| [examples/caching.md](examples/caching.md) | HybridCache, distributed locking, invalidation |
| [examples/openapi.md](examples/openapi.md) | Scalar, XML docs, security schemes |
| [examples/observability.md](examples/observability.md) | OpenTelemetry, Sentry, Serilog, metrics |
