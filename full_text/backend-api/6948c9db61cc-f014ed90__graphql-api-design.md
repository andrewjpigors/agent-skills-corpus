---
name: graphql-api-design
description: Use when designing GraphQL APIs with schema-first or code-first approaches, implementing resolvers, DataLoader patterns, subscriptions, Apollo Federation, error handling, authentication, authorization, pagination, and production best practices. Includes SDL patterns, Relay spec, and performance optimization.
license: MIT
---

# GraphQL API Design Skill — GraphQL Best Practices

## Overview

This skill provides comprehensive guidance for **designing and implementing GraphQL APIs**, including schema design with SDL, resolver implementation, DataLoader patterns for N+1 prevention, subscriptions, Apollo Federation, error handling, authentication, authorization, pagination, and production best practices. Based on GraphQL specification, Apollo Server documentation, and production best practices.

## When to Use

**Use this skill when:**

- Designing GraphQL schemas with SDL (Schema Definition Language)
- Implementing GraphQL type definitions (Object, Input, Interface, Union, Enum, Scalar)
- Creating GraphQL queries and mutations
- Setting up GraphQL subscriptions with WebSocket or Server-Sent Events
- Implementing resolvers (object, field, class-based)
- Preventing N+1 queries with DataLoader pattern
- Handling GraphQL errors with GraphQLError and formatted errors
- Validating input with custom directives and schema directives
- Authenticating requests with JWT and context
- Authorizing access with directives and middleware
- Versioning GraphQL schemas (URL, header, schema evolution)
- Implementing pagination with Relay spec and cursor-based approaches
- Adding filtering with input types and arguments
- Implementing sorting with enum and input types
- Building search with full-text and fuzzy matching
- Batching requests with Apollo Link Batch and schema directives
- Caching with HTTP cache and Redis integration
- Optimizing performance with persisted queries and response caching
- Analyzing query complexity with graphql-query-complexity
- Limiting query depth with graphql-depth-limit
- Configuring introspection for production environments
- Choosing between SDL-first and code-first approaches
- Implementing Apollo Federation for microservices
- Using Apollo Schema Stitching for legacy API integration
- Configuring Apollo Server, Express GraphQL, or GraphQL Yoga
- Setting up GraphQL Mesh for REST/GraphQL federation
- Establishing production best practices and monitoring

**Do NOT use this skill when:**

- Designing RESTful APIs (use api-design skill for REST endpoint patterns)
- Building database schemas (use database-design skill for table structures)
- Implementing frontend GraphQL clients (use frontend framework skills)
- Setting up CI/CD pipelines (use devops-pipeline skill)
- Containerizing GraphQL servers (use docker-containerization skill)
- Deploying to cloud infrastructure (use terraform-iac or kubernetes-orchestration skill)
- Writing application business logic (use domain-driven skill)
- Performing security audits (use security-auditor skill)

**Why avoid:** GraphQL is specifically for API query language and runtime. Use REST for simple CRUD, databases for data storage, and the right tools for infrastructure and deployment.

## Core Concepts

### Schema Design Approaches

| Approach               | Best For                               | Tools                               |
| ---------------------- | -------------------------------------- | ----------------------------------- |
| **Schema-First (SDL)** | Team collaboration, API contracts      | GraphQL Code Generator, graphql-tag |
| **Code-First**         | Rapid prototyping, TypeScript projects | type-graphql, Nexus, GraphQL Tools  |
| **Federation**         | Microservices, distributed teams       | Apollo Gateway, Apollo Router       |
| **Schema Stitching**   | Legacy integration, gradual migration  | Apollo Schema Stitching             |

### Type System Overview

| Type          | Purpose                     | Example                                   |
| ------------- | --------------------------- | ----------------------------------------- |
| **Object**    | Complex data structures     | `type User { id: ID! name: String! }`     |
| **Input**     | Mutation/Query input shapes | `input CreateUserInput { name: String! }` |
| **Interface** | Shared fields across types  | `interface Node { id: ID! }`              |
| **Union**     | One of multiple types       | `union SearchResult = User \| Post`       |
| **Enum**      | Fixed set of values         | `enum Role { ADMIN USER }`                |
| **Scalar**    | Custom primitive types      | `scalar DateTime`, `scalar JSON`          |

### Server Framework Comparison

| Framework           | Language | Key Features                                     |
| ------------------- | -------- | ------------------------------------------------ |
| **Apollo Server**   | Node.js  | Federation, caching, tracing, production-ready   |
| **GraphQL Yoga**    | Node.js  | Built-in subscriptions, PWA support, lightweight |
| **Express GraphQL** | Node.js  | Minimal, Express middleware integration          |
| **GraphQL Mesh**    | Node.js  | REST/GraphQL federation, multi-source            |
| **Strawberry**      | Python   | Python-native, async support, type inference     |
| **Graphene**        | Python   | Django/Flask integration, schema-first           |

## Schema Design with SDL

### Complete Schema Example

```graphql
# ============================================
# Scalar Types
# ============================================
scalar DateTime
scalar JSON
scalar UUID
scalar URL
scalar Email

# ============================================
# Enum Types
# ============================================
enum Role {
  ADMIN
  MODERATOR
  USER
  GUEST
}

enum Status {
  ACTIVE
  INACTIVE
  PENDING
  SUSPENDED
}

enum SortOrder {
  ASC
  DESC
}

# ============================================
# Interface Types
# ============================================
interface Node {
  id: ID!
}

interface Timestamps {
  createdAt: DateTime!
  updatedAt: DateTime!
}

# ============================================
# Union Types
# ============================================
union SearchResult = User | Post | Comment

union AuthenticationResult = LoginSuccess | LoginError

# ============================================
# Input Types
# ============================================
input CreateUserInput {
  name: String!
  email: Email!
  password: String!
  role: Role = USER
}

input UpdateUserInput {
  name: String
  email: Email
  role: Role
}

input UserFilterInput {
  status: Status
  role: Role
  search: String
  createdAtFrom: DateTime
  createdAtTo: DateTime
}

input UserSortInput {
  field: UserSortField = createdAt
  order: SortOrder = DESC
}

enum UserSortField {
  name
  email
  createdAt
  updatedAt
}

# ============================================
# Object Types
# ============================================
type User implements Node & Timestamps {
  id: ID!
  name: String!
  email: Email!
  role: Role!
  status: Status!
  posts: [Post!]!
  comments: [Comment!]!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Post implements Node & Timestamps {
  id: ID!
  title: String!
  content: String!
  author: User!
  comments: [Comment!]!
  status: Status!
  createdAt: DateTime!
  updatedAt: DateTime!
}

type Comment implements Node & Timestamps {
  id: ID!
  text: String!
  author: User!
  post: Post!
  createdAt: DateTime!
  updatedAt: DateTime!
}

# ============================================
# Pagination Types (Relay Spec)
# ============================================
type UserEdge {
  node: User!
  cursor: String!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

# ============================================
# Authentication Types
# ============================================
type LoginSuccess {
  token: String!
  user: User!
}

type LoginError {
  message: String!
  code: String!
}

input LoginInput {
  email: Email!
  password: String!
}

# ============================================
# Query Type
# ============================================
type Query {
  user(id: ID!): User
  post(id: ID!): Post

  users(
    first: Int = 20
    after: String
    filter: UserFilterInput
    sort: UserSortInput
  ): UserConnection!

  search(query: String!): [SearchResult!]!
  health: HealthStatus!
}

type HealthStatus {
  status: String!
  version: String!
  timestamp: DateTime!
}

# ============================================
# Mutation Type
# ============================================
type Mutation {
  login(input: LoginInput!): AuthenticationResult!
  logout: Boolean!

  createUser(input: CreateUserInput!): User!
  updateUser(id: ID!, input: UpdateUserInput!): User!
  deleteUser(id: ID!): Boolean!

  createPost(input: CreatePostInput!): Post!
  updatePost(id: ID!, input: UpdatePostInput!): Post!
  deletePost(id: ID!): Boolean!
}

# ============================================
# Subscription Type
# ============================================
type Subscription {
  userCreated: User!
  userUpdated(id: ID!): User!
  postCreated(categoryId: ID): Post!
  commentAdded(postId: ID!): Comment!
}
```

## Resolver Implementation

### Object Resolvers

```typescript
import { GraphQLResolveInfo, GraphQLScalarType } from 'graphql';
import { GraphQLError } from 'graphql/error';
import { DateTimeResolver } from 'graphql-scalars';
import { User, Post, Comment } from '../types';
import { UserRole, UserStatus } from '../enums';
import { prisma } from '../db';
import { requireAuth, requireRole } from '../middleware';

// Custom Scalar Resolvers
const DateTime: GraphQLScalarType = new DateTimeResolver();

// Object Type Resolvers
const UserResolvers = {
  posts: (user: User) => prisma.post.findMany({ where: { authorId: user.id } }),
  comments: (user: User) =>
    prisma.comment.findMany({ where: { authorId: user.id } }),
  fullName: (user: User) => `${user.firstName} ${user.lastName}`,
  ssn: (user: User, args, context) => {
    requireAuth(context);
    requireRole(context, UserRole.ADMIN);
    return user.ssn;
  },
};

const PostResolvers = {
  author: (post: Post) =>
    prisma.user.findUnique({ where: { id: post.authorId } }),
  comments: (post: Post) =>
    prisma.comment.findMany({ where: { postId: post.id } }),
  wordCount: (post: Post) => post.content.split(/\s+/).length,
  excerpt: (post: Post) => post.content.substring(0, 200) + '...',
};

// Root Resolvers (Query, Mutation, Subscription)
const resolvers = {
  Query: {
    user: (_, { id }, context) => {
      requireAuth(context);
      return prisma.user.findUnique({ where: { id } });
    },

    users: (_, { first = 20, after, filter, sort }, context) => {
      requireAuth(context);

      const where: any = {};
      if (filter?.status) where.status = filter.status;
      if (filter?.role) where.role = filter.role;
      if (filter?.search) {
        where.OR = [
          { name: { contains: filter.search } },
          { email: { contains: filter.search } },
        ];
      }

      const orderBy: any = {};
      const sortField = sort?.field || 'createdAt';
      const sortOrder = sort?.order || 'DESC';
      orderBy[sortField] = sortOrder;

      const cursor = after ? { id: after } : undefined;
      const take = first + 1;

      const users = await prisma.user.findMany({
        where,
        orderBy,
        cursor,
        take,
        skip: after ? 1 : 0,
      });

      const hasNextPage = users.length > first;
      const data = hasNextPage ? users.slice(0, -1) : users;

      return {
        edges: data.map((user) => ({ node: user, cursor: user.id })),
        pageInfo: {
          hasNextPage,
          hasPreviousPage: !!after,
          startCursor: data.length > 0 ? data[0].id : null,
          endCursor: data.length > 0 ? data[data.length - 1].id : null,
        },
        totalCount: await prisma.user.count({ where }),
      };
    },

    search: async (_, { query }, context) => {
      requireAuth(context);

      const [users, posts, comments] = await Promise.all([
        prisma.user.findMany({
          where: {
            OR: [{ name: { contains: query } }, { email: { contains: query } }],
          },
          take: 10,
        }),
        prisma.post.findMany({
          where: {
            OR: [
              { title: { contains: query } },
              { content: { contains: query } },
            ],
          },
          take: 10,
        }),
        prisma.comment.findMany({
          where: { text: { contains: query } },
          take: 10,
        }),
      ]);

      return [...users, ...posts, ...comments];
    },

    health: () => ({
      status: 'ok',
      version: process.env.APP_VERSION || '1.0.0',
      timestamp: new Date().toISOString(),
    }),
  },

  Mutation: {
    login: async (_, { input }) => {
      const user = await prisma.user.findUnique({
        where: { email: input.email },
      });

      if (!user || !(await bcrypt.compare(input.password, user.password))) {
        return {
          __typename: 'LoginError',
          message: 'Invalid credentials',
          code: 'AUTH_FAILED',
        };
      }

      const token = jwt.sign({ userId: user.id }, process.env.JWT_SECRET);
      return { __typename: 'LoginSuccess', token, user };
    },

    createUser: (_, { input }, context) => {
      requireAuth(context);
      requireRole(context, UserRole.ADMIN);
      const hashedPassword = await bcrypt.hash(input.password, 10);
      return prisma.user.create({
        data: { ...input, password: hashedPassword },
      });
    },

    updateUser: async (_, { id, input }, context) => {
      requireAuth(context);
      if (context.userId !== id && context.role !== UserRole.ADMIN) {
        throw new GraphQLError('Unauthorized', {
          extensions: { code: 'FORBIDDEN' },
        });
      }
      return prisma.user.update({ where: { id }, data: input });
    },

    deleteUser: async (_, { id }, context) => {
      requireAuth(context);
      requireRole(context, UserRole.ADMIN);
      await prisma.user.delete({ where: { id } });
      return true;
    },
  },

  Subscription: {
    userCreated: {
      subscribe: (_, __, context) =>
        context.pubsub.asyncIterator(['USER_CREATED']),
    },
    userUpdated: {
      subscribe: (_, { id }, context) =>
        context.pubsub.asyncIterator([`USER_UPDATED:${id}`]),
    },
    postCreated: {
      subscribe: (_, { categoryId }, context) => {
        const events = categoryId
          ? [`POST_CREATED:${categoryId}`]
          : ['POST_CREATED'];
        return context.pubsub.asyncIterator(events);
      },
    },
    commentAdded: {
      subscribe: (_, { postId }, context) =>
        context.pubsub.asyncIterator([`COMMENT_ADDED:${postId}`]),
    },
  },

  User: UserResolvers,
  Post: PostResolvers,

  AuthenticationResult: {
    __resolveType(obj) {
      if (obj.token) return 'LoginSuccess';
      return 'LoginError';
    },
  },

  SearchResult: {
    __resolveType(obj) {
      if (obj.email) return 'User';
      if (obj.title) return 'Post';
      return 'Comment';
    },
  },

  DateTime,
};

export default resolvers;
```

## DataLoader Pattern (N+1 Prevention)

### DataLoader Implementation

```typescript
import DataLoader from 'dataloader';
import { prisma } from '../db';

// User DataLoader
const createUserLoader = () =>
  new DataLoader(async (userIds: readonly string[]) => {
    const users = await prisma.user.findMany({
      where: { id: { in: Array.from(userIds) } },
    });
    return userIds.map((id) => users.find((u) => u.id === id) || null);
  });

// Post DataLoader
const createPostLoader = () =>
  new DataLoader(async (postIds: readonly string[]) => {
    const posts = await prisma.post.findMany({
      where: { id: { in: Array.from(postIds) } },
    });
    return postIds.map((id) => posts.find((p) => p.id === id) || null);
  });

// Comment count DataLoader (with aggregation)
const createCommentLoader = () =>
  new DataLoader(async (postIds: readonly string[]) => {
    const comments = await prisma.comment.groupBy({
      by: ['postId'],
      _count: { _all: true },
      where: { postId: { in: Array.from(postIds) } },
    });
    return postIds.map(
      (postId) => comments.find((c) => c.postId === postId)?._count._all || 0
    );
  });

// Context setup (new DataLoader instances per request)
const createContext = (req: Request) => ({
  prisma,
  pubsub,
  userId: getUserIdFromToken(req),
  role: getRoleFromToken(req),
  userLoader: createUserLoader(),
  postLoader: createPostLoader(),
  commentLoader: createCommentLoader(),
});

// Resolver using DataLoader
const resolvers = {
  Post: {
    // ✅ GOOD: Uses DataLoader (1 query for N posts)
    author: (post, __, context) => context.userLoader.load(post.authorId),
    commentCount: (post, __, context) => context.commentLoader.load(post.id),

    // ❌ BAD: Causes N+1 queries (1 query per post)
    // author: (post) => prisma.user.findUnique({ where: { id: post.authorId } })
  },

  Comment: {
    author: (comment, __, context) => context.userLoader.load(comment.authorId),
    post: (comment, __, context) => context.postLoader.load(comment.postId),
  },
};
```

### DataLoader Best Practices

| Practice                    | Description                                                       |
| --------------------------- | ----------------------------------------------------------------- |
| **Per-request instances**   | Create new DataLoader per request to avoid caching stale data     |
| **Batch factory functions** | Use factory functions to create DataLoaders with fresh state      |
| **Cache key consistency**   | Ensure batch function returns results in same order as input keys |
| **Null handling**           | Return null for missing keys, not undefined                       |
| **Error handling**          | Use DataLoader's built-in error handling or maxBatchSize          |

## Error Handling

### Custom Error Classes

```typescript
import { GraphQLError, GraphQLFormattedError } from 'graphql';

class UserInputError extends GraphQLError {
  constructor(message: string, properties?: Record<string, unknown>) {
    super(message, {
      extensions: {
        code: 'BAD_USER_INPUT',
        timestamp: new Date().toISOString(),
        ...properties,
      },
    });
  }
}

class AuthenticationError extends GraphQLError {
  constructor(message: string = 'Authentication required') {
    super(message, {
      extensions: {
        code: 'UNAUTHENTICATED',
        timestamp: new Date().toISOString(),
      },
    });
  }
}

class ForbiddenError extends GraphQLError {
  constructor(message: string = 'Insufficient permissions') {
    super(message, {
      extensions: { code: 'FORBIDDEN', timestamp: new Date().toISOString() },
    });
  }
}

class NotFoundError extends GraphQLError {
  constructor(message: string, properties?: Record<string, unknown>) {
    super(message, {
      extensions: {
        code: 'NOT_FOUND',
        timestamp: new Date().toISOString(),
        ...properties,
      },
    });
  }
}

// Format errors for production
const formatError = (error: GraphQLFormattedError): GraphQLFormattedError => {
  const { code, timestamp, ...extensions } = error.extensions || {};

  if (
    process.env.NODE_ENV === 'production' &&
    code === 'INTERNAL_SERVER_ERROR'
  ) {
    return {
      ...error,
      message: 'Internal server error',
      extensions: { code, timestamp },
    };
  }

  return { ...error, extensions: { code, timestamp, ...extensions } };
};

// Usage in resolvers
const resolvers = {
  Query: {
    user: (_, { id }, context) => {
      if (!context.userId) throw new AuthenticationError();

      const user = await prisma.user.findUnique({ where: { id } });
      if (!user)
        throw new NotFoundError(`User with id ${id} not found`, { id });

      return user;
    },

    updateUser: async (_, { id, input }, context) => {
      if (!context.userId) throw new AuthenticationError();

      if (input.email && !isValidEmail(input.email)) {
        throw new UserInputError('Invalid email format', { field: 'email' });
      }

      if (context.userId !== id && context.role !== UserRole.ADMIN) {
        throw new ForbiddenError('Cannot update other users');
      }

      return prisma.user.update({ where: { id }, data: input });
    },
  },
};
```

## Authentication and Authorization

### JWT Authentication with Context

```typescript
import jwt from 'jsonwebtoken';

interface Context {
  userId?: string;
  user?: User;
  role?: UserRole;
  prisma: PrismaClient;
  pubsub: PubSub;
  userLoader: DataLoader<string, User>;
  postLoader: DataLoader<string, Post>;
}

// JWT Verification
const verifyToken = (token: string): { userId: string; role: UserRole } => {
  try {
    return jwt.verify(token, process.env.JWT_SECRET) as {
      userId: string;
      role: UserRole;
    };
  } catch {
    throw new AuthenticationError('Invalid or expired token');
  }
};

// Context Creator
const createContext = ({ req }: CreateContextOptions): Context => {
  const token = req.headers.authorization?.replace('Bearer ', '');
  let userId: string | undefined;
  let role: UserRole | undefined;

  if (token) {
    const decoded = verifyToken(token);
    userId = decoded.userId;
    role = decoded.role;
  }

  return {
    userId,
    role,
    prisma,
    pubsub,
    userLoader: createUserLoader(),
    postLoader: createPostLoader(),
  };
};

// Middleware Functions
const requireAuth = (context: Context): void => {
  if (!context.userId) throw new AuthenticationError();
};

const requireRole = (context: Context, ...roles: UserRole[]): void => {
  requireAuth(context);
  if (!roles.includes(context.role!))
    throw new ForbiddenError('Insufficient permissions');
};

const requireOwner = (context: Context, resourceOwnerId: string): void => {
  requireAuth(context);
  if (context.role !== UserRole.ADMIN && context.userId !== resourceOwnerId) {
    throw new ForbiddenError('You can only modify your own resources');
  }
};
```

### Schema Directives for Authorization

```typescript
const authDirective = {
  typeDefinition: `directive @auth(requires: Role = USER) on FIELD_DEFINITION`,

  resolverDefinition: ({
    requires = UserRole.USER,
  }: {
    requires?: UserRole;
  }) => {
    return async (next, parent, args, context, info) => {
      requireAuth(context);
      requireRole(context, requires);
      return next();
    };
  },
};

// Usage in schema
// type Query {
//   adminDashboard: DashboardStats! @auth(requires: ADMIN)
//   user: User! @auth(requires: USER)
// }
```

## Pagination Patterns

### Relay Cursor-Based Pagination

```typescript
// Schema
type Query {
  users(
    first: Int = 20
    after: String
    last: Int
    before: String
    filter: UserFilterInput
    sort: UserSortInput
  ): UserConnection!
}

type UserConnection {
  edges: [UserEdge!]!
  pageInfo: PageInfo!
  totalCount: Int!
}

type UserEdge {
  node: User!
  cursor: String!
}

type PageInfo {
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
  startCursor: String
  endCursor: String
}

// Resolver
const resolvers = {
  Query: {
    users: async (_, { first = 20, after, last, before, filter, sort }, context) => {
      const where = buildWhere(filter);
      const orderBy = buildOrderBy(sort);

      // Forward pagination
      if (first !== undefined) {
        const cursor = after ? { id: after } : undefined;
        const take = first + 1;

        const users = await prisma.user.findMany({
          where, orderBy, cursor, take, skip: after ? 1 : 0
        });

        const hasNextPage = users.length > first;
        const data = hasNextPage ? users.slice(0, -1) : users;

        return {
          edges: data.map(user => ({ node: user, cursor: encodeCursor(user.id) })),
          pageInfo: {
            hasNextPage,
            hasPreviousPage: !!after,
            startCursor: data.length > 0 ? encodeCursor(data[0].id) : null,
            endCursor: data.length > 0 ? encodeCursor(data[data.length - 1].id) : null
          },
          totalCount: await prisma.user.count({ where })
        };
      }

      // Backward pagination
      if (last !== undefined) {
        const cursor = before ? { id: before } : undefined;
        const take = last + 1;

        const users = await prisma.user.findMany({
          where, orderBy: reverseOrder(orderBy), cursor, take, skip: before ? 1 : 0
        });

        const hasPreviousPage = users.length > last;
        const data = hasPreviousPage ? users.slice(0, -1) : users;
        data.reverse();

        return {
          edges: data.map(user => ({ node: user, cursor: encodeCursor(user.id) })),
          pageInfo: {
            hasNextPage: !!before,
            hasPreviousPage,
            startCursor: data.length > 0 ? encodeCursor(data[0].id) : null,
            endCursor: data.length > 0 ? encodeCursor(data[data.length - 1].id) : null
          },
          totalCount: await prisma.user.count({ where })
        };
      }
    }
  }
};

const encodeCursor = (id: string): string => Buffer.from(`cursor:${id}`).toString('base64');
const decodeCursor = (cursor: string): string => Buffer.from(cursor, 'base64').toString('utf-8').replace('cursor:', '');
```

### Offset-Based Pagination (Alternative)

```typescript
type Query {
  users(
    page: Int = 1
    limit: Int = 20
    filter: UserFilterInput
    sort: UserSortInput
  ): UserPagination!
}

type UserPagination {
  data: [User!]!
  total: Int!
  page: Int!
  limit: Int!
  totalPages: Int!
  hasNextPage: Boolean!
  hasPreviousPage: Boolean!
}

// Resolver
const resolvers = {
  Query: {
    users: async (_, { page = 1, limit = 20, filter, sort }, context) => {
      const where = buildWhere(filter);
      const orderBy = buildOrderBy(sort);
      const skip = (page - 1) * limit;

      const [data, total] = await Promise.all([
        prisma.user.findMany({ where, orderBy, skip, take: limit }),
        prisma.user.count({ where })
      ]);

      const totalPages = Math.ceil(total / limit);

      return {
        data, total, page, limit, totalPages,
        hasNextPage: page < totalPages,
        hasPreviousPage: page > 1
      };
    }
  }
};
```

## Apollo Federation

### Subgraph Setup

```typescript
// subgraph-user/src/index.ts
import { ApolloServer } from '@apollo/server';
import { buildSubgraphSchema } from '@apollo/subgraph';

const server = new ApolloServer({
  schema: buildSubgraphSchema({ typeDefs, resolvers }),
});

const typeDefs = `#graphql
  extend type Query {
    _service: _Service!
  }
  
  type User implements @key(fields: "id") {
    id: ID!
    name: String!
    email: String!
    role: Role!
  }
  
  enum Role { ADMIN USER }
`;

const resolvers = {
  Query: { user: (_, { id }) => findUserById(id) },
  User: { __resolveReference: ({ id }) => findUserById(id) },
};
```

### Apollo Gateway Setup

```typescript
// gateway/src/index.ts
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { ApolloGateway } from '@apollo/gateway';
import express from 'express';
import { json } from 'body-parser';

const gateway = new ApolloGateway({
  supergraphs: [
    {
      url: 'http://localhost:4001',
      sdl: fs.readFileSync('./user-subgraph.schema', 'utf8'),
    },
    {
      url: 'http://localhost:4002',
      sdl: fs.readFileSync('./post-subgraph.schema', 'utf8'),
    },
  ],
});

const server = new ApolloServer();
const app = express();

async function start() {
  const { schema } = await server.start();

  app.use(
    '/graphql',
    json(),
    expressMiddleware(server, {
      context: async ({ req }) => ({ userId: getUserIdFromToken(req) }),
    })
  );

  await server.listen({ port: 4000 });
  console.log('Gateway ready at http://localhost:4000/graphql');
}

start();
```

## Performance Optimization

### Query Complexity Analysis

```typescript
import { createComplexityLimitRule } from 'graphql-validation-complexity';

const validationRules = [
  createComplexityLimitRule(1000, {
    scalarCost: 1,
    objectCost: 0,
    listFactor: 10,
  }),
];

const server = new ApolloServer({
  schema,
  validationRules,
  plugins: [
    persistedQueries.plugin({ cache: new InMemoryLRUCache() }),
    responseCachePlugin({
      ttl: {
        default: 60,
        Query: { users: 30, health: 300 },
      },
    }),
  ],
});
```

### Query Depth Limiting

```typescript
import depthLimit from 'graphql-depth-limit';

const validationRules = [
  depthLimit(10), // Maximum query depth of 10
  createComplexityLimitRule(1000),
];

const server = new ApolloServer({ schema, validationRules, formatError });
```

## Server Configuration

### Apollo Server Setup

```typescript
import { ApolloServer } from '@apollo/server';
import { expressMiddleware } from '@apollo/server/express4';
import { startStandaloneServer } from '@apollo/server/standalone';
import { json } from 'body-parser';
import cors from 'cors';
import { schema } from './schema';
import { createContext } from './context';
import { formatError } from './errors';
import { validationRules } from './validation';

const server = new ApolloServer({
  schema,
  formatError,
  validationRules,
  introspection: process.env.NODE_ENV !== 'production',
  plugins: [
    {
      async serverWillStart() {
        return {
          async drainServer() {
            await prisma.$disconnect();
          },
        };
      },
    },
  ],
});

// Standalone mode
const { url } = await startStandaloneServer(server, {
  listen: { port: 4000 },
  context: async (requestContext) => createContext(requestContext),
});

console.log(`Server ready at ${url}`);
```

### GraphQL Yoga Setup

```typescript
import { createYoga } from 'graphql-yoga';
import { schema } from './schema';

const yoga = createYoga({
  schema,
  context: async ({ request }) => ({
    userId: getUserIdFromToken(request),
    userLoader: createUserLoader(),
  }),
  graphqlEndpoint: '/graphql',
  ide: process.env.NODE_ENV !== 'production' ? 'graphiql' : 'apollo',
  cors: {
    origin: ['https://yourdomain.com'],
    credentials: true,
  },
});

server.listen(4000).then(({ url }) => {
  console.log(`Server ready at ${url}`);
});
```

## Production Checklist

Before deploying to production:

- [ ] Schema design follows GraphQL best practices
- [ ] DataLoader implemented for N+1 prevention
- [ ] Query complexity analysis configured
- [ ] Query depth limiting enabled
- [ ] Error handling with custom error classes
- [ ] Authentication with JWT and context
- [ ] Authorization with directives and middleware
- [ ] Pagination with Relay spec or cursor-based
- [ ] Subscriptions with WebSocket or SSE
- [ ] Introspection disabled in production
- [ ] Rate limiting configured
- [ ] Response caching enabled
- [ ] Persisted queries configured
- [ ] Health check endpoint implemented
- [ ] Logging and monitoring setup
- [ ] GraphQL Playground disabled in production
- [ ] CORS configured correctly
- [ ] Schema validation in CI/CD pipeline

## Real-World Impact

**Before this skill:**

- N+1 query problems causing slow responses
- No authentication or authorization
- Missing error handling
- No pagination or filtering
- Deep queries causing server overload
- No performance monitoring

**After this skill:**

- Efficient data loading with DataLoader
- Secure authentication and authorization
- Comprehensive error handling
- Relay-compliant pagination
- Query complexity and depth limiting
- Production-ready monitoring

## Cross-References

- **`api-design`** - For RESTful API design patterns
- **`database-design`** - For database schema design
- **`redis-caching`** - For Redis caching strategies
- **`docker-containerization`** - For containerizing GraphQL servers
- **`kubernetes-orchestration`** - For deploying to Kubernetes
- **`devops-pipeline`** - For CI/CD with GraphQL
- **`security-auditor`** - For security reviews
- **`microservices-architecture`** - For Apollo Federation patterns

## References

- [GraphQL Specification](https://spec.graphql.org/)
- [Apollo Server Documentation](https://www.apollographql.com/docs/apollo-server/)
- [GraphQL Yoga Documentation](https://the-guild.dev/graphql/yoga-server/docs)
- [Apollo Federation](https://www.apollographql.com/docs/federation/)
- [Relay Specification](https://relay.dev/graphql/)
- [GraphQL Best Practices](https://www.apollographql.com/docs/apollo-server/performance/best-practices/)
- [DataLoader Documentation](https://github.com/graphql/dataloader)
- [GraphQL Depth Limit](https://github.com/stems/graphql-depth-limit)
- [GraphQL Query Complexity](https://github.com/slicknode/graphql-query-complexity)
