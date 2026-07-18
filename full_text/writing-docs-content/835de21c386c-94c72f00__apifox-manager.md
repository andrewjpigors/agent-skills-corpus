---
name: apifox-manager
description: "Apifox API documentation management and automated testing skill. Manage interface documentation, data models, test cases, environment configurations, and more in Apifox projects. Supports creating, updating, and deleting interfaces via CLI, managing test cases and scenarios, configuring environment variables, importing/exporting data, managing branches and merge requests. Trigger this skill when users mention Apifox, API documentation, interface testing, API automated testing, Mock services, or API collaboration platforms."
---

# Apifox Manager

Apifox API documentation management and automated testing skill. Manage Apifox projects comprehensively through the CLI, including interface design, automated testing, environment configuration, data import/export, branch collaboration, and more.

## CRITICAL: Common Pitfalls and Solutions

**READ THIS FIRST before creating any endpoints!**

### 1. Request Body Type Field

**For JSON bodies, use `"type": "application/json"`** (完整 MIME 类型，不是 `"json"` 短写)。

| 值 | 含义 |
|---|---|
| `"application/json"` | JSON 请求体 ← 最常用 |
| `"none"` | 无请求体（GET/DELETE 等） |
| `"application/x-www-form-urlencoded"` | 表单 |
| `"graphql"` | GraphQL |
| `"application/x-msgpack"` | MessagePack |

**WRONG — 会导致 Web UI 不渲染请求体：**
```json
"requestBody": {
  "type": "json",  // ❌ 缺少 application/ 前缀
  "jsonSchema": { ... }
}
```

**CORRECT：**
```json
"requestBody": {
  "type": "application/json",
  "parameters": [],
  "jsonSchema": { ... },
  "required": true,
  "description": "Request body description",
  "mediaType": "",
  "examples": [],
  "oasExtensions": ""
}
```

### 2. Complete Request Body Structure

**Always use this complete structure:**
```json
"requestBody": {
  "parameters": [],
  "jsonSchema": {
    "type": "object",
    "properties": {
      "fieldName": {
        "type": "string",
        "description": "Field description",
        "example": "example value"
      }
    },
    "required": ["fieldName"]
  },
  "required": true,
  "description": "Request body description",
  "mediaType": "",
  "examples": [],
  "oasExtensions": ""
}
```

### 3. Parameter Structure

**所有参数（path、query、header）必须包含 `id` 字段，格式 `name#index`：**

```json
{
  "id": "activityId#0",  // 格式: name#index
  "name": "activityId",
  "required": true,
  "description": "Activity ID",
  "type": "string"
}
```

**规则：**
- path 参数：`"activityId#0"` — 即使只有一个 path 参数也不能省略 `id`
- query 参数：`"page#0"`, `"pageSize#1"` — 索引在全局递增
- **缺少 `id` → 参数在 Web UI 不显示**

**Query parameters should also include `example`:**
```json
{
  "id": "page#0",
  "name": "page",
  "required": false,
  "description": "Page number",
  "type": "integer",
  "example": "1"
}
```

### 4. Data Model References

**Use this format to reference data models:**
```json
"data": {
  "$ref": "#/models/{schemaId}"
}
```

Where `{schemaId}` is the numeric ID from `apifox schema list`.

### 5. No Version Prefixes

**DO NOT add version prefixes to paths unless explicitly requested:**
- ❌ `/api/v1/users`
- ✅ `/api/users`

### 6. Discover Module IDs

**To find module IDs:**
```bash
apifox endpoint list --project <projectId>
```

Each endpoint in the output includes `moduleId`. Use this when creating new endpoints.

### 7. Complete Endpoint Example

**Here's a complete, working endpoint example:**
```json
{
  "name": "Create Activity",
  "method": "post",
  "path": "/api/activities",
  "status": "designing",
  "description": "Create a new activity",
  "tags": ["Activity Management"],
  "folderId": 12345,
  "requestBody": {
    "type": "application/json",
    "parameters": [],
    "jsonSchema": {
      "type": "object",
      "properties": {
        "title": {
          "type": "string",
          "maxLength": 120,
          "description": "Activity title",
          "example": "Weekend Badminton"
        },
        "startTime": {
          "type": "string",
          "format": "date-time",
          "description": "Start time",
          "example": "2026-07-05T14:00:00Z"
        },
        "capacity": {
          "type": "integer",
          "minimum": 1,
          "description": "Maximum participants",
          "example": 20
        }
      },
      "required": ["title", "startTime", "capacity"]
    },
    "required": true,
    "description": "Activity information",
    "mediaType": "",
    "examples": [],
    "oasExtensions": ""
  },
  "parameters": {
    "path": [
      {
        "id": "activityId#0",
        "name": "activityId",
        "required": true,
        "description": "Activity ID",
        "type": "string"
      }
    ],
    "query": [
      {
        "id": "page#0",
        "name": "page",
        "required": false,
        "description": "Page number",
        "type": "integer",
        "example": "1"
      }
    ]
  },
  "responses": [
    {
      "name": "Success",
      "code": 201,
      "contentType": "json",
      "jsonSchema": {
        "type": "object",
        "properties": {
          "success": { "type": "boolean", "example": true },
          "code": { "type": "string", "example": "COMMON_000" },
          "message": { "type": "string", "example": "OK" },
          "data": { "$ref": "#/models/289099426" },
          "timestamp": { "type": "string", "format": "date-time" },
          "requestId": { "type": "string", "format": "uuid" }
        }
      }
    }
  ]
}
```

## Project Structure (Understanding Topology)

Before making any changes, understand how Apifox projects are organized:

```
Team
└── Project (identified by projectId)
    ├── Module 1 (e.g., "User Service") ← Each module = separate OpenAPI spec
    │   ├── Endpoint Folders (--type endpoint, independent tree)
    │   │   ├── Folder: "User Management" (ID: 1001)
    │   │   │   ├── Endpoint: GET /api/users (moduleId: 501, folderId: 1001)
    │   │   │   ├── Endpoint: POST /api/users
    │   │   │   └── Endpoint: GET /api/users/{id}
    │   │   ├── Folder: "Auth" (ID: 1002)
    │   │   │   ├── Endpoint: POST /auth/login
    │   │   │   └── Endpoint: POST /auth/logout
    │   ├── Schema Folders (--type schema, independent tree)
    │   ├── Test Scenario Folders (--type test-scenario)
    │   └── Environments (Dev, Test, Prod)
    ├── Module 2 (e.g., "Order Service")
    │   └── (same structure as Module 1)
    └── Branches (main, sprint/xxx, ai/xxx)
```

**Key Concepts:**
- **Modules** group endpoints by service/microservice. Each module has its own base URL per environment and corresponds to a standalone OpenAPI spec.
- **Folders** logically group endpoints within a module (e.g., "User Management", "Order Management"). Each resource type has its own **independent** folder tree.
- **Endpoints** belong to exactly one module (`moduleId`) and one folder (`folderId`). Always specify both when creating.
- **Tags** provide cross-folder categorization.
- **Environments** are shared across branches and project levels.

**Three IDs needed for proper endpoint placement:**
- `projectId` — from `apifox project list`
- `moduleId` — from `apifox endpoint list` output (each endpoint includes `moduleId`)
- `folderId` — from `apifox folder list --project <id> --type endpoint`

**Always explore this structure before creating or moving resources.**

## Workflow

### 1. Environment Check and Preparation

Before executing any operations, check if the environment is ready:

```bash
# Check Node.js version
node -v

# Check if Apifox CLI is installed
apifox -v

# Check if logged in
apifox whoami
```

If not logged in, the user needs to provide:
- **API Access Token**: In Apifox Web → Avatar → Account Settings → API Access Tokens → New
- **Project ID**: In Project Settings → Basic Settings → Basic Information → Project ID

Login command:
```bash
apifox login --with-token <your-token>
```

### 2. Explore Project Structure (MANDATORY - Read Before Write)

**HARD RULE: You MUST explore the project structure BEFORE creating any resource.**

```bash
# 1. List folders to understand module structure
apifox folder list --project <projectId> --type endpoint
apifox folder list --project <projectId> --type schema
apifox folder list --project <projectId> --type test-scenario

# 2. List existing endpoints to avoid duplicates and discover module IDs
apifox endpoint list --project <projectId>

# 3. List existing environments
apifox environment list --project <projectId>

# 4. List data models
apifox schema list --project <projectId>

# 5. List test cases and scenarios
apifox test-case list --project <projectId>
apifox test-scenario list --project <projectId>
```

**Hard Rules:**
- **DO NOT create any resource without first listing the project structure**
- **Before creating an endpoint, check if PATH/METHOD combination already exists**
- **Before creating a folder, check if a folder with the same name already exists**
- **Before updating, get the current resource state first**
- **DO NOT add version prefixes (e.g., /v1/, /v2/) to paths unless the user explicitly specifies it**
- **DO NOT use `"type": "json"` (short form) in requestBody - use `"type": "application/json"` instead - see Critical Pitfalls section above**

### 3. Pre-Operation Confirmation

**Important Principle**: Before executing any operation that may modify the project, you must clearly inform the user what will be done and get explicit confirmation before proceeding.

Example confirmation:
```
I will perform the following operations:
- Operation type: Create interface
- Target project: Project ID <your-project-id>
- Target module: Module ID <moduleId> (from endpoint list)
- Target folder: User Management (ID: 12345)
- Operation details: Create a GET /api/users interface for fetching user list

Please confirm to continue?
```

### 4. Execute Operations

Select appropriate command combinations based on user requirements. See `references/workflows.md` for common operation workflows.

### 5. Verify Results

After completing operations, verify the results meet expectations:
```bash
# View the newly created resource
apifox endpoint get <endpointId> --project <projectId>

# Or list all resources
apifox endpoint list --project <projectId>
```

**Important:** After creating/updating endpoints, always verify in Apifox Web UI that:
- Request body is not empty
- Parameters are correctly displayed
- Response structure is complete

## Core Capabilities

### Interface Management

```bash
# List all interfaces
apifox endpoint list --project <projectId>

# Create interface (requires JSON file)
apifox endpoint create --project <projectId> --file ./endpoint.json

# Update interface
apifox endpoint update <endpointId> --project <projectId> --file ./endpoint-update.json

# Delete interface
apifox endpoint delete <endpointId> --project <projectId>
```

**CRITICAL: Always use the complete endpoint structure from the Critical Pitfalls section!**

**How to get folderId and moduleId:**
```bash
# List folders to find the correct folder ID
apifox folder list --project <projectId> --type endpoint

# List endpoints to discover module IDs
apifox endpoint list --project <projectId>
# Look for moduleId in the output
```

**Complete Endpoint JSON Example:**
```json
{
  "name": "Get User List",
  "method": "get",
  "path": "/api/users",
  "status": "designing",
  "description": "Get all users in the system",
  "tags": ["User Management"],
  "folderId": 12345,
  "parameters": {
    "query": [
      {
        "id": "page#0",
        "name": "page",
        "required": false,
        "description": "Page number",
        "type": "integer",
        "example": "1"
      },
      {
        "id": "pageSize#1",
        "name": "pageSize",
        "required": false,
        "description": "Items per page",
        "type": "integer",
        "example": "20"
      }
    ]
  },
  "responses": [
    {
      "name": "Success",
      "code": 200,
      "contentType": "json",
      "jsonSchema": {
        "type": "object",
        "properties": {
          "success": { "type": "boolean", "example": true },
          "code": { "type": "string", "example": "COMMON_000" },
          "message": { "type": "string", "example": "OK" },
          "data": {
            "type": "object",
            "properties": {
              "items": {
                "type": "array",
                "items": { "$ref": "#/models/123456" }
              },
              "total": { "type": "integer", "example": 100 },
              "page": { "type": "integer", "example": 1 },
              "pageSize": { "type": "integer", "example": 20 }
            }
          },
          "timestamp": { "type": "string", "format": "date-time" },
          "requestId": { "type": "string", "format": "uuid" }
        }
      }
    }
  ]
}
```

**POST Endpoint with Request Body Example:**
```json
{
  "name": "Create User",
  "method": "post",
  "path": "/api/users",
  "status": "designing",
  "description": "Create a new user",
  "tags": ["User Management"],
  "folderId": 12345,
  "requestBody": {
    "type": "application/json",
    "parameters": [],
    "jsonSchema": {
      "type": "object",
      "properties": {
        "username": {
          "type": "string",
          "maxLength": 64,
          "description": "Username",
          "example": "john_doe"
        },
        "email": {
          "type": "string",
          "format": "email",
          "description": "Email address",
          "example": "john@example.com"
        },
        "password": {
          "type": "string",
          "minLength": 8,
          "description": "Password",
          "example": "SecurePass123!"
        }
      },
      "required": ["username", "email", "password"]
    },
    "required": true,
    "description": "User information",
    "mediaType": "",
    "examples": [],
    "oasExtensions": ""
  },
  "responses": [
    {
      "name": "Created",
      "code": 201,
      "contentType": "json",
      "jsonSchema": {
        "type": "object",
        "properties": {
          "success": { "type": "boolean", "example": true },
          "code": { "type": "string", "example": "COMMON_000" },
          "message": { "type": "string", "example": "User created successfully" },
          "data": { "$ref": "#/models/123456" },
          "timestamp": { "type": "string", "format": "date-time" },
          "requestId": { "type": "string", "format": "uuid" }
        }
      }
    }
  ]
}
```

**IMPORTANT REMINDERS:**
- ✅ DO use `"type": "application/json"` for JSON request bodies (not `"json"`)
- ✅ DO include all fields: `type`, `parameters`, `jsonSchema`, `required`, `description`, `mediaType`, `examples`, `oasExtensions`
- ✅ DO include `example` values for all fields
- ✅ DO use proper parameter structure with `id` field (format: name#index)
- ✅ DO use `$ref` format `"#/models/{schemaId}"` to reference data models
- ❌ DO NOT use `"type": "json"` (short form) — use `"type": "application/json"` (full MIME) instead

### 8. Response Examples Format

`responseExamples` 用于在文档预览中生成响应示例。格式要求严格：

**每条示例的 `data` 必须是 JSON 字符串（不是对象！）**

```json
"responseExamples": [
  {
    "name": "成功示例",
    "responseId": 129972710,
    "data": "{\n  \"success\": true,\n  \"code\": \"COMMON_000\",\n  \"data\": { \"reviewId\": \"abc-123\" }\n}"
  }
]
```

**关键规则：**
- `data` 必须是 **字符串**，不是 JSON 对象。否则 Web UI 报 `e.replace is not a function`
- `responseId` 必须匹配 `responses` 数组中的实际响应 ID（数字）
- **警告！** `updateHttpEndpoint` 每次调用会重新生成所有 response ID。因此：
  1. 先更新 responses
  2. 再读取接口获取新的 response ID
  3. 最后再更新 responseExamples（用新的 ID）

### 9. Common Web UI Errors

| Web UI 错误 | 根因 | 修复 |
|---|---|---|
| `e.replace is not a function` | `responseExamples.data` 是对象不是字符串 | 把 `data` 值改成 JSON 字符串 |
| 请求体不显示 | `requestBody.type` 缺失或值为 `"json"` | 改为 `"application/json"` |
| 请求体字段平铺无结构 | `requestBody` 用了 `parameters` 而非 `jsonSchema` | JSON 必须用 `jsonSchema`，`parameters` 仅用于 form |
| 响应示例显示 null | `jsonSchema` 传了字符串而非对象 | `jsonSchema` 必须是 JSON 对象，不要 `JSON.stringify` |
| 响应示例不显示 | `responseId` 与 `responses` 中 ID 不匹配 | 先读接口获取最新 ID，再更新 |
| 参数不显示 | 缺少 `id` 字段或格式不对 | 所有参数必须有 `"id": "name#index"` |

### Data Model Management

```bash
# List all data models
apifox schema list --project <projectId>

# Create data model
apifox schema create --project <projectId> --file ./schema.json

# Update data model
apifox schema update <schemaId> --project <projectId> --file ./schema-update.json

# Delete data model
apifox schema delete <schemaId> --project <projectId>
```

**Data Model JSON Example:**
```json
{
  "name": "User",
  "displayName": "用户",
  "description": "User entity",
  "type": "json",
  "moduleId": 8079516,
  "jsonSchema": {
    "type": "object",
    "properties": {
      "id": {
        "type": "string",
        "format": "uuid",
        "description": "User ID"
      },
      "username": {
        "type": "string",
        "maxLength": 64,
        "description": "Username"
      },
      "email": {
        "type": "string",
        "format": "email",
        "description": "Email address"
      },
      "status": {
        "type": "string",
        "enum": ["active", "inactive", "banned"],
        "description": "User status"
      },
      "createdAt": {
        "type": "string",
        "format": "date-time",
        "description": "Creation time"
      }
    },
    "required": ["id", "username", "email", "status", "createdAt"]
  }
}
```

**Referencing Data Models in Endpoints:**
```json
"data": {
  "$ref": "#/models/{schemaId}"
}
```

Where `{schemaId}` is the numeric ID from `apifox schema list` output.

### Automated Testing

```bash
# List test cases
apifox test-case list --project <projectId>

# Create test case
apifox test-case create --project <projectId> --file ./test-case.json

# List scenario cases
apifox test-scenario list --project <projectId>

# Create scenario case
apifox test-scenario create --project <projectId> --file ./scenario.json

# Run scenario case
apifox test-scenario run <scenarioId> --project <projectId> --environment <envId>
```

### Environment and Variable Management

```bash
# List environments
apifox environment list --project <projectId>

# Create environment
apifox environment create <name> --project <projectId> --base-url <url>

# List variables
apifox variables list --project <projectId> --scope global

# Set variable
apifox variables set --project <projectId> --scope global --key <key> --value <value>
```

### Import/Export

```bash
# Import OpenAPI/Swagger
apifox import --project <projectId> --format openapi --file ./openapi.json

# Export as OpenAPI
apifox export --project <projectId> --format openapi --output ./openapi.json
```

**Supported import formats:** `openapi`, `postman`, `har`, `insomnia`, `jmeter`, `wsdl`, `yapi`, `rap2`, `apidoc`, `hoppscotch`, `markdown`, `jsonschema`, `apifox`

**Supported export formats:** `openapi`, `markdown`, `html`, `postman`, `apifox`

**Export options:**
- `--scope <scope>` - Export scope: `all`, `apis`, `tags`, `folders`
- `--api-ids <ids>` - Comma-separated API IDs (for `apis`/`folders` scope)
- `--folder-ids <ids>` - Comma-separated folder IDs (for `apis`/`folders` scope)
- `--include-tags <tags>` - Include tags (for `tags` scope)
- `--exclude-tags <tags>` - Exclude tags
- `--oas-version <version>` - OpenAPI version (2.0, 3.0, 3.1)

### Branch Management

```bash
# List branches
apifox branch list --project <projectId> --type all

# Create branch
apifox branch create --project <projectId> --type sprint --name "feature-xxx" --from main

# Merge branch
apifox branch merge --project <projectId> --from <sourceBranch> --to main
```

## JSON Schema Reference

Before creating complex resources, check the corresponding JSON Schema:

```bash
# View interface creation Schema
apifox cli-schema get endpoint-create

# View test case creation Schema
apifox cli-schema get test-case-create

# Validate JSON file
apifox cli-schema validate endpoint-create --file ./endpoint.json
```

## Common Workflows

See `references/workflows.md` for detailed common workflows.

## Read-Before-Write Pattern

**MANDATORY for all update operations:**

```bash
# 1. READ: Get current resource state
apifox endpoint get <endpointId> --project <projectId> --output json > current.json

# 2. PLAN: Make changes to the JSON (only modify what's needed)

# 3. SHOW DIFF: Display what will change
echo "Changes to apply:"
diff current.json updated.json

# 4. CONFIRM: Get user approval

# 5. EXECUTE: Apply the update
apifox endpoint update <endpointId> --project <projectId> --file ./updated.json

# 6. VERIFY: Confirm the change
apifox endpoint get <endpointId> --project <projectId>
```

## MCP Tools Reference (18 Tools)

Apifox 新版 MCP（Streamable HTTP）提供 18 个工具。**不要使用旧版 stdio MCP**（`npx @apifox/apifox-mcp-server`），旧版仅 5 个工具且不支持写入。

### MCP 配置（OpenCode 格式）

```json
{
  "mcp": {
    "apifox-new-mcp": {
      "type": "remote",
      "url": "https://api.apifox.com/mcp",
      "headers": {
        "Authorization": "Bearer <access_token>",
        "X-Apifox-Api-Version": "2025-09-01"
      },
      "enabled": true
    }
  }
}
```

### 完整工具列表

#### 📖 Read / Search（7 个）

| # | 工具 | 用途 | 关键参数 |
|---|---|---|---|
| 1 | `listAccessibleProjects` | 列出当前用户可访问的所有项目 | 无 |
| 2 | `getProjectSummary` | 获取项目完整结构元数据（分支、模块、文件夹、Schema 文件夹、测试分组等所有结构 ID） | `projectId` |
| 3 | `getStructureInfo` | 查询指定结构范围内的实体列表（返回 ID、名称、基础元信息） | `projectId`, `entityType`（endpoint/schema/markdown）, `folderId?`, `moduleId?`, `branchId?` |
| 4 | `readEntityDetails` | 读取单个实体完整详情（endpoint 返回 OAS 3.0，schema 返回 JSON Schema，markdown 返回原文） | `projectId`, `entityType`, `entityId`, `with?`（testCase） |
| 5 | `searchProjectContent` | 按关键词搜索项目内容（端点、Schema、Markdown） | `projectId`, `query`, `entityType?` |
| 6 | `listTestCases` | 获取接口的测试用例列表 | `projectId`, `endpointId?` |
| 7 | `getTestCase` | 获取测试用例详情 | `projectId`, `id` |

#### ✏️ Write / Update（7 个）

| # | 工具 | 用途 | 关键参数 |
|---|---|---|---|
| 8 | `createHttpEndpoint` | 创建新 HTTP 接口 | `headers`（含 `X-Project-Id`）, `body`（含 method, path, name 等） |
| 9 | `updateHttpEndpoint` | 修改 HTTP 接口（⚠️ 全量替换，不是合并） | `pathParams.http_api_id`, `headers`（含 `X-Project-Id`）, `body` |
| 10 | `deleteHttpEndpoint` | 删除指定 HTTP 接口 | `pathParams.http_api_id`, `headers`（含 `X-Project-Id`） |
| 11 | `createTestCase` | 创建接口的测试用例 | `pathParams.projectId`, `body`（含 apiDetailId, name, parameters 等） |
| 12 | `updateTestCase` | 修改接口测试用例 | `pathParams.projectId`, `pathParams.id`, `body` |
| 13 | `deleteTestCase` | 删除接口测试用例 | `pathParams.projectId`, `pathParams.id` |
| 14 | `importData` | 导入 OpenAPI/Swagger 格式数据 | `pathParams.projectId`, `body`（含 importFormat, data/url） |

#### 📤 Export（1 个）

| # | 工具 | 用途 | 关键参数 |
|---|---|---|---|
| 15 | `exportData` | 导出 OpenAPI 格式数据 | `pathParams.projectId`, `body`（含 format, type, version 等） |

#### ⚡ Beta（3 个）

| # | 工具 | 用途 | 关键参数 |
|---|---|---|---|
| 16 | `listOpenApiEndpoints` | 搜索/列出可用的 OpenAPI 端点工具（用于查找额外工具） | `keyword?`, `method?`, `tags?`, `limit?` |
| 17 | `getOpenApiDetails` | 获取指定 OpenAPI 端点的详细信息 | `id` |
| 18 | `executeOpenApi` | 执行指定的 OpenAPI 调用（用于 Schema 更新等原生操作） | `id`, `pathParams`, `queryParams`, `headers`, `body` |

### MCP 工具的 9 个坑

**坑 1: executeOpenApi 的 pathParams 值类型敏感**
- 表现：传 `"289099426"` (string) → 静默失败；传 `289099426` (number) → 成功
- 解法：整数字段用数字，字符串字段用字符串

**坑 2: updateHttpEndpoint 的 requestBody / responses 是全量替换，非合并**
- 表现：只传 `{tickets:...}` → title、time 等全部字段被删光
- 解法：每次改 requestBody 必须把全部字段带上（先 readEntityDetails 读取，再整包传入）

**坑 3: updateHttpEndpoint 的 body 有长度上限**
- 表现：完整 requestBody JSON 一并发过去 → 报错
- 解法：先改 tickets 等核心字段，再分步补其余字段

**坑 4: createHttpEndpoint 同样有长度限制**
- 表现：带完整 description/parameters/responses 创建 → 报错
- 解法：先传最小参数建骨架，再分步用 updateHttpEndpoint 填充

**坑 5: 新建接口的 responses 不能用 $ref**
- 表现：新接口的 jsonSchema 里写 $ref → updateHttpEndpoint 报错
- 解法：新接口先用 `type: object`，后续在 Web 端手工加 $ref

**坑 6: readEntityDetails 对部分 endpoint 间歇不可用**
- 表现：某些 ID 反复报错，读不到数据
- 解法：用 `getStructureInfo(folderId=...)` 先拿到真实 entityId，再读

**坑 7: executeOpenApi 更新 Schema 时必须传 queryParams: {}**
- 表现：不传 → 静默失败
- 解法：Schema 更新调 executeOpenApi 时始终附带 `queryParams: {}`

**坑 8: requestBody 的 parameters 模式不能用于 JSON**
- 表现：用 `parameters` 数组定义 JSON 请求体 → Web UI 不渲染字段结构，只显示 key-value 平铺
- 解法：`application/json` 必须用 `jsonSchema` 定义。`parameters` 仅用于 `form-data` / `x-www-form-urlencoded`
```json
// ❌ 错误 — parameters 是给 form 用的
{ "type": "application/json", "parameters": [{ "name": "prompt", "value": "..." }] }

// ✅ 正确 — JSON 必须用 jsonSchema
{ "type": "application/json", "jsonSchema": { "type": "object", "properties": { "prompt": { "type": "string" } } } }
```

**坑 9: jsonSchema 不能传字符串，必须传 JSON 对象**
- 表现：`"jsonSchema": "{\"type\":\"object\",...}"` → Apifox 原样存储字符串，无法提取字段，响应示例显示 null
- 解法：始终传 JSON 对象，不要 `JSON.stringify`
```json
// ❌ 错误 — 字符串
"jsonSchema": "{\"type\":\"object\",\"properties\":{\"code\":{\"type\":\"integer\"}}}"

// ✅ 正确 — 对象
"jsonSchema": { "type": "object", "properties": { "code": { "type": "integer" } } }
```

### MCP Read-Before-Write 工作流

**MANDATORY：每次 update 前必须 read**

```
1. getStructureInfo → 确认文件夹下有哪些实体及其真实 ID
2. readEntityDetails → 读取当前完整结构
3. 在完整结构基础上修改（不要凭假设编造 ID）
4. updateHttpEndpoint → 传入完整修改后的结构
5. readEntityDetails → 验证修改结果，确认无字段丢失
```

### CLI vs MCP 选择

| 场景 | 推荐 |
|---|---|
| 单个接口创建/更新 | CLI 或 MCP 均可 |
| 批量操作（>5个） | CLI（脚本化） |
| 需要精确控制请求体 | MCP（readEntityDetails 读取后修改） |
| Schema 更新 | MCP（executeOpenApi） |
| 快速查看/列表 | CLI（`apifox endpoint list`） |

## Project Configuration

You can create `.apifox/settings.json` in the project root to save the default project ID:

```json
{
  "projectId": "<your-project-id>"
}
```

This avoids specifying the `--project` parameter for every operation.

## Important Notes

1. **Explore First**: Always explore project structure before making changes
2. **Use folderId**: Place endpoints in appropriate folders, not just root
3. **Pre-Operation Confirmation**: Inform the user and get confirmation before any modification operation
4. **Schema Validation**: Use `cli-schema validate` to validate JSON files before creating complex resources
5. **Branch Protection**: Main branches are protected by default, modifications require merge requests
6. **Data Backup**: Export project data before important operations
7. **Permission Check**: Ensure the user has sufficient project permissions for the corresponding operations
8. **No Version Prefixes**: Do not add version prefixes (e.g., /v1/, /v2/) to endpoint paths unless the user explicitly specifies it
9. **Use `"type": "application/json"`**: For JSON request bodies, use the full MIME type `"application/json"` (NOT the short `"json"` form, which causes empty request bodies in Web UI)
10. **Complete Structure**: Always use complete requestBody structure with all required fields
11. **Parameter IDs**: All parameters must have `id` field in format `name#index`
12. **Example Values**: Include `example` values for all fields to improve documentation
13. **Data Model References**: Use `"$ref": "#/models/{schemaId}"` format with numeric schemaId
14. **Verify in Web UI**: After creating/updating endpoints, verify in Apifox Web UI that request bodies and parameters display correctly
15. **MCP: Read Before Write**: When using MCP tools, ALWAYS call `readEntityDetails` before `updateHttpEndpoint` — requestBody is full replacement, not merge
16. **MCP: Verify After Write**: After EVERY `updateHttpEndpoint`, call `readEntityDetails` to confirm no fields were lost
17. **MCP: Use getStructureInfo First**: Don't assume endpoint IDs — use `getStructureInfo` to get real entity IDs from folders
18. **MCP: Type Sensitivity**: In `executeOpenApi`, pathParams must use correct types (number for IDs, string for names)

## Troubleshooting

### Request Body Shows as Empty in Web UI

**Problem:** After creating/updating an endpoint, the request body appears empty in Apifox Web UI.

**Cause:** Using `"type": "json"` (short form) instead of `"type": "application/json"` (full MIME type) in the requestBody field.

**Solution:** 
- Use `"type": "application/json"` for JSON request bodies
- Use the complete structure: `type`, `parameters`, `jsonSchema`, `required`, `description`, `mediaType`, `examples`, `oasExtensions`
- See "CRITICAL: Common Pitfalls and Solutions" section at the top

### Login Failed
- Check if the token format is correct (should start with `afxp_`)
- Confirm the token has not expired
- Check network connection

### Command Execution Failed
- Check if the project ID is correct
- Confirm the user has corresponding permissions for the project
- Use `--verbose` parameter for detailed error information

### JSON Format Error
- Use `cli-schema validate` to validate JSON files: `apifox cli-schema validate endpoint-create --file ./endpoint.json`
- Check if required fields are complete
- Confirm field types and formats comply with Schema requirements

### Endpoint Created in Wrong Folder
- List folders first: `apifox folder list --project <projectId> --type endpoint`
- Use `folderId` in JSON file
- Default folderId is 0 (root) if not specified

### Parameters Not Showing in Web UI
- Ensure all parameters have the `id` field (format: `name#index`, e.g., `page#0`)
- Ensure all parameters have `name`, `required`, `description`, and `type` fields
- For query parameters, include `example` field

### Data Model Reference Not Working
- Use correct format: `"$ref": "#/models/{schemaId}"`
- Verify schemaId exists: `apifox schema list --project <projectId>`
- Ensure the schemaId is numeric (not the schema name)

### Version Prefix Added to Paths
- **DO NOT** add `/v1/`, `/v2/` etc. to paths unless explicitly requested
- Use paths like `/api/users` not `/api/v1/users`