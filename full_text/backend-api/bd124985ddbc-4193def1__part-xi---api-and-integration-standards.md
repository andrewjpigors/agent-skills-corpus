---
name: Part XI - API and Integration Standards
version: 1.0.0
description: Comprehensive API design, integration patterns, and communication standards for AI systems. This skill establishes the foundational principles for building, consuming, and securing APIs across distributed AI systems.
scope: api, integration, webhooks, protocols, http, rpc, event-driven
authority: AI Constitution - Directive Principles
enforcement: MANDATORY
review_cycle: quarterly
---

# PART XI: API AND INTEGRATION STANDARDS

## CONSTITUTIVE PRINCIPLES

### Article 1: API as a Contract

**1.1** An API is a contractual agreement between provider and consumer and must be treated with the same rigor as legal contracts.

**1.2** Breaking changes to published APIs must be avoided or managed through versioning.

**1.3** API documentation is an integral part of the API and must be maintained with equal diligence.

**1.4** The principle of least surprise must govern all API design decisions.

### Article 2: Interoperability Mandate

**2.1** APIs must be designed for interoperability across different systems, languages, and platforms.

**2.2** Industry-standard protocols and formats must be preferred over proprietary solutions.

**2.3** APIs must be designed with evolution in mind, allowing for future extensibility without breaking existing clients.

**2.4** Open standards compliance enables integration flexibility and reduces vendor lock-in.

### Article 3: Developer Experience First

**3.1** APIs must be designed with developer experience as a primary consideration.

**3.2** Consistency across APIs enables developers to predict and learn quickly.

**3.3** Clear, comprehensive documentation and examples must be provided.

**3.4** Developer tooling (SDKs, CLIs, sandboxes) should be provided where feasible.

---

## CHAPTER I: oRPC PROTOCOL STANDARDS

### Article 4: oRPC Overview and Philosophy

**4.1** oRPC (Object RPC) is the preferred RPC protocol for internal service communication.

**4.2** oRPC provides:

   (a) Type-safe contracts between services
   
   (b) Bi-directional streaming support
   
   (c) Code generation for multiple languages
   
   (d) Built-in error handling and retry logic

**4.3** oRPC must be used for:

   (a) Inter-service communication within the platform
   
   (b) Service-to-service API calls requiring low latency
   
   (c) Scenarios requiring request/response or streaming patterns

### Article 5: oRPC Service Definition

**5.1** Service Definition Standards:

   (a) Use Protocol Buffers (proto3) for service definitions
   
   (b) Define services with clear domain boundaries
   
   (c) Use PascalCase for service names, camelCase for method names
   
   (d) Document all services, methods, and messages

**5.2** Service Naming:

   (a) Service names must reflect the domain: {Domain}Service
   
   (b) Examples: UserService, OrderService, NotificationService
   
   (c) Avoid generic names like DataService or UtilityService

**5.3** Method Naming:

   (a) Method names must be verbs describing the action
   
   (b) Use standard CRUD prefixes where appropriate:
       - Get{Entity} / Get{Entity}List
       - Create{Entity}
       - Update{Entity}
       - Delete{Entity}
       - Batch{Operation}{Entity}
   
   (c) Use domain-specific verbs for non-CRUD operations:
       - Process{Entity}
       - Calculate{Result}
       - Send{Notification}

**5.4** Example Service Definition:

```protobuf
syntax = "proto3";

package user.v1;

option go_package = "github.com/example/gen/go/user/v1;userv1";
option java_package = "com.example.user.v1";
option java_multiple_files = true;

import "google/protobuf/timestamp.proto";
import "google/api/field_behavior.proto";
import "validate/validate.proto";

service UserService {
    rpc GetUser(GetUserRequest) returns (GetUserResponse);
    
    rpc ListUsers(ListUsersRequest) returns (ListUsersResponse);
    
    rpc CreateUser(CreateUserRequest) returns (CreateUserResponse);
    
    rpc UpdateUser(UpdateUserRequest) returns (UpdateUserResponse);
    
    rpc DeleteUser(DeleteUserRequest) returns (DeleteUserResponse);
    
    rpc BatchGetUsers(BatchGetUsersRequest) returns (BatchGetUsersResponse);
}

message User {
    string id = 1;
    string email = 2;
    string full_name = 3;
    UserRole role = 4;
    bool email_verified = 5;
    google.protobuf.Timestamp created_at = 6;
    google.protobuf.Timestamp updated_at = 7;
}

enum UserRole {
    USER_ROLE_UNSPECIFIED = 0;
    USER_ROLE_USER = 1;
    USER_ROLE_ADMIN = 2;
    USER_ROLE_SUPER_ADMIN = 3;
}

message GetUserRequest {
    string id = 1 [(validate.rules).string = {uuid: true}];
}

message GetUserResponse {
    User user = 1;
}

message ListUsersRequest {
    int32 page_size = 1 [(validate.rules).int32 = {gte: 1, lte: 100}];
    string page_token = 2;
    string filter = 3;
    string order_by = 4;
}

message ListUsersResponse {
    repeated User users = 1;
    string next_page_token = 2;
    int32 total_size = 3;
}

message CreateUserRequest {
    string email = 1 [(validate.rules).string = {email: true}];
    string full_name = 2 [(validate.rules).string = {min_len: 1, max_len: 255}];
    UserRole role = 3;
}

message CreateUserResponse {
    User user = 1;
}

message UpdateUserRequest {
    string id = 1 [(validate.rules).string = {uuid: true}];
    UpdateMask update_mask = 2;
    User user = 3;
}

message UpdateMask {
    repeated string paths = 1;
}

message UpdateUserResponse {
    User user = 1;
}

message DeleteUserRequest {
    string id = 1 [(validate.rules).string = {uuid: true}];
}

message DeleteUserResponse {}

message BatchGetUsersRequest {
    repeated string ids = 1 [(validate.rules).repeated = {min_items: 1, max_items: 100}];
}

message BatchGetUsersResponse {
    repeated User users = 1;
    repeated string not_found_ids = 2;
}
```

### Article 6: oRPC Message Design

**6.1** Message Naming Conventions:

   (a) Request messages: {MethodName}Request
   
   (b) Response messages: {MethodName}Response
   
   (c) Use clear, descriptive names
   
   (d) Avoid generic names like Request or Response

**6.2** Field Naming:

   (a) Use snake_case for field names (proto convention)
   
   (b) Use clear, descriptive field names
   
   (c) Use common field names consistently across messages:
       - id: Unique identifier
       - created_at: Creation timestamp
       - updated_at: Last modification timestamp
       - deleted_at: Soft deletion timestamp

**6.3** Field Numbers:

   (a) Field numbers must never change after publication
   
   (b) Reserve deprecated field numbers
   
   (c) Use sequential numbering for new fields in a message

**6.4** OneOf and Optional Fields:

   (a) Use oneof for mutually exclusive fields
   
   (b) Use optional for fields that may be omitted (proto3 optional keyword)
   
   (c) Avoid excessive use of oneof

### Article 7: oRPC Streaming Standards

**7.1** When to Use Streaming:

   (a) **Server streaming**: For large data sets, real-time updates, notifications
   
   (b) **Client streaming**: For file uploads, batch operations, telemetry
   
   (c) **Bidirectional streaming**: For real-time interaction, chat, collaborative editing

**7.2** Streaming Method Naming:

   (a) Add Stream suffix for streaming methods:
       - SubscribeTo{Event}
       - Stream{DataType}
       - Upload{Entity}

**7.3** Streaming Examples:

```protobuf
service NotificationService {
    rpc SubscribeToNotifications(SubscribeRequest) returns (stream Notification);
    
    rpc StreamUserActivity(StreamActivityRequest) returns (stream ActivityEvent);
    
    rpc UploadUserAvatar(stream UploadRequest) returns (UploadResponse);
    
    rpc StreamChatMessages(stream ChatMessage) returns (stream ChatMessage);
}

message SubscribeRequest {
    repeated string event_types = 1;
    map<string, string> filters = 2;
}

message Notification {
    string id = 1;
    string type = 2;
    string title = 3;
    string body = 4;
    map<string, string> data = 5;
    google.protobuf.Timestamp timestamp = 6;
}
```

### Article 8: oRPC Error Handling

**8.1** Error Model:

   (a) Use google.rpc.Status for error responses
   
   (b) Define domain-specific error codes in proto definitions
   
   (c) Include error details for debugging

**8.2** Error Code Standards:

```protobuf
enum ErrorCode {
    ERROR_CODE_UNSPECIFIED = 0;
    ERROR_CODE_NOT_FOUND = 1;
    ERROR_CODE_INVALID_ARGUMENT = 2;
    ERROR_CODE_PERMISSION_DENIED = 3;
    ERROR_CODE_ALREADY_EXISTS = 4;
    ERROR_CODE_RESOURCE_EXHAUSTED = 5;
    ERROR_CODE_ABORTED = 6;
    ERROR_CODE_INTERNAL = 7;
    ERROR_CODE_UNAVAILABLE = 8;
}

message ErrorDetail {
    ErrorCode code = 1;
    string message = 2;
    string domain = 3;
    map<string, string> metadata = 4;
    repeated FieldViolation field_violations = 5;
}

message FieldViolation {
    string field = 1;
    string description = 2;
}
```

**8.3** Error Response Pattern:

```python
# Server-side error handling
class UserServiceServicer(user_v1.UserServiceServicer):
    def GetUser(self, request, context):
        try:
            user = self.user_repo.get_by_id(request.id)
            if not user:
                context.abort(
                    grpc.StatusCode.NOT_FOUND,
                    f"User with id {request.id} not found"
                )
            return user_v1.GetUserResponse(user=user.to_proto())
        except Exception as e:
            logger.error(f"Error getting user: {e}")
            context.abort(
                grpc.StatusCode.INTERNAL,
                "An internal error occurred"
            )
```

---

## CHAPTER II: OPENAPI SPECIFICATION REQUIREMENTS

### Article 9: OpenAPI Specification Standards

**9.1** All HTTP/REST APIs must be documented using OpenAPI Specification (OAS) 3.0 or later.

**9.2** OpenAPI documents must be:

   (a) Complete and accurate reflections of the API
   
   (b) Version-controlled alongside the code
   
   (c) Validated against the OpenAPI specification
   
   (d) Published and accessible to consumers

**9.3** OpenAPI Document Structure:

```yaml
openapi: 3.1.0
info:
  title: User Management API
  description: |
    Comprehensive user management API for the platform.
    
    ## Authentication
    All endpoints require Bearer token authentication.
    
    ## Rate Limiting
    Default rate limit: 1000 requests per minute.
  version: 1.0.0
  contact:
    name: API Support
    email: api-support@example.com
  license:
    name: MIT
    url: https://opensource.org/licenses/MIT
servers:
  - url: https://api.example.com/v1
    description: Production server
  - url: https://staging-api.example.com/v1
    description: Staging server
  - url: https://dev-api.example.com/v1
    description: Development server
tags:
  - name: Users
    description: User management operations
  - name: Authentication
    description: Authentication and session management
paths:
  /users:
    get:
      # ... operation details
```

### Article 10: API Path Design

**10.1** Path Naming Conventions:

   (a) Use lowercase letters and hyphens for multi-word paths
   
   (b) Use plural nouns for collections: /users, /orders, /products
   
   (c) Nest resources logically: /users/{userId}/orders
   
   (d) Maximum nesting depth: 2 levels

**10.2** Path Structure Examples:

```
# Good
GET    /users
GET    /users/{userId}
GET    /users/{userId}/orders
POST   /users
PUT    /users/{userId}
PATCH  /users/{userId}
DELETE /users/{userId}

/users/{userId}/addresses/{addressId}

/users/{userId}/preferences

# Avoid
GET /getUsers
POST /createUser
GET /user/{userId}/orders/{orderId}/items/{itemId}/details
```

**10.3** Resource Hierarchy:

   (a) Child resources belong under parent resources
   
   (b) Cross-resource operations use the primary resource
   
   (c) Use query parameters for filtering, sorting, pagination

### Article 11: HTTP Method Usage

**11.1** Standard Method Usage:

   (a) **GET**: Retrieve resources without side effects
   
   (b) **POST**: Create new resources, execute actions
   
   (c) **PUT**: Replace entire resource (idempotent)
   
   (d) **PATCH**: Partial update (idempotent)
   
   (e) **DELETE**: Remove resources (idempotent)

**11.2** Method Semantics:

```
GET    /users              # List users
GET    /users/{userId}     # Get specific user
POST   /users              # Create user
PUT    /users/{userId}     # Replace user (full update)
PATCH  /users/{userId}     # Update user (partial)
DELETE /users/{userId}     # Delete user
```

**11.3** Safe and Idempotent Properties:

   | Method | Safe | Idempotent |
   |--------|------|------------|
   | GET    | Yes  | Yes        |
   | PUT    | No   | Yes        |
   | DELETE | No   | Yes        |
   | POST   | No   | No         |
   | PATCH  | No   | No*        |

*PATCH is idempotent when the patch is applied atomically

### Article 12: Request and Response Schemas

**12.1** Schema Design Principles:

   (a) Use JSON Schema for request/response bodies
   
   (b) Define reusable components in #/components/schemas
   
   (c) Use camelCase for JSON property names
   
   (d) Include descriptions for all fields

**12.2** Schema Examples:

```yaml
components:
  schemas:
    User:
      type: object
      required:
        - id
        - email
        - created_at
      properties:
        id:
          type: string
          format: uuid
          description: Unique identifier
          example: "550e8400-e29b-41d4-a716-446655440000"
        email:
          type: string
          format: email
          description: User's email address
          example: "user@example.com"
        full_name:
          type: string
          minLength: 1
          maxLength: 255
          example: "John Doe"
        role:
          $ref: '#/components/schemas/UserRole'
        email_verified:
          type: boolean
          default: false
        created_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
        updated_at:
          type: string
          format: date-time
          example: "2024-01-15T10:30:00Z"
    
    UserRole:
      type: string
      enum:
        - user
        - admin
        - super_admin
      default: user
    
    Error:
      type: object
      required:
        - code
        - message
      properties:
        code:
          type: string
          description: Machine-readable error code
          example: "USER_NOT_FOUND"
        message:
          type: string
          description: Human-readable error message
          example: "User with the specified ID was not found"
        details:
          type: array
          items:
            $ref: '#/components/schemas/ErrorDetail'
        request_id:
          type: string
          description: Request identifier for debugging

    PaginatedResponse:
      type: object
      required:
        - items
        - pagination
      properties:
        items:
          type: array
          items: {}
        pagination:
          $ref: '#/components/schemas/Pagination'
    
    Pagination:
      type: object
      required:
        - total_count
        - page
        - page_size
      properties:
        total_count:
          type: integer
          description: Total number of items
          example: 1000
        page:
          type: integer
          description: Current page number
          example: 1
        page_size:
          type: integer
          description: Items per page
          example: 20
        next_page:
          type: string
          nullable: true
          description: Token for next page
        prev_page:
          type: string
          nullable: true
          description: Token for previous page
```

### Article 13: Parameter Documentation

**13.1** Path Parameters:

```yaml
/users/{userId}:
  get:
    summary: Get user by ID
    parameters:
      - name: userId
        in: path
        required: true
        schema:
          type: string
          format: uuid
        description: Unique user identifier
        example: "550e8400-e29b-41d4-a716-446655440000"
```

**13.2** Query Parameters:

```yaml
/users:
  get:
    summary: List users
    parameters:
      - name: page
        in: query
        required: false
        schema:
          type: integer
          default: 1
          minimum: 1
        description: Page number
      - name: page_size
        in: query
        required: false
        schema:
          type: integer
          default: 20
          minimum: 1
          maximum: 100
        description: Items per page
      - name: filter
        in: query
        required: false
        schema:
          type: string
        description: |
          Filter expression. Supported fields:
          - email
          - role
          - created_at
          - email_verified
          
          Examples:
          - email eq "test@example.com"
          - role eq "admin" and email_verified eq true
      - name: order_by
        in: query
        required: false
        schema:
          type: string
          default: "created_at"
          enum:
            - created_at
            - email
            - full_name
        description: Field to sort by
      - name: order
        in: query
        required: false
        schema:
          type: string
          default: desc
          enum:
            - asc
            - desc
        description: Sort order
```

### Article 14: Response Documentation

**14.1** Response Status Codes:

   (a) **200 OK**: Successful GET, PUT, PATCH, DELETE
   
   (b) **201 Created**: Successful POST creating a resource
   
   (c) **204 No Content**: Successful DELETE or action with no response body
   
   (d) **400 Bad Request**: Invalid request (validation error)
   
   (e) **401 Unauthorized**: Missing or invalid authentication
   
   (f) **403 Forbidden**: Authenticated but not authorized
   
   (g) **404 Not Found**: Resource not found
   
   (h) **409 Conflict**: Resource conflict (duplicate, state conflict)
   
   (i) **422 Unprocessable Entity**: Semantic validation errors
   
   (j) **429 Too Many Requests**: Rate limit exceeded
   
   (k) **500 Internal Server Error**: Server error

**14.2** Response Documentation Example:

```yaml
/users:
  post:
    summary: Create a new user
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateUserRequest'
          example:
            email: "newuser@example.com"
            full_name: "New User"
            role: "user"
    responses:
      '201':
        description: User created successfully
        headers:
          X-Request-Id:
            schema:
              type: string
            description: Request identifier for tracking
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/UserResponse'
            example:
              id: "550e8400-e29b-41d4-a716-446655440000"
              email: "newuser@example.com"
              full_name: "New User"
              role: "user"
              email_verified: false
              created_at: "2024-01-15T10:30:00Z"
              updated_at: "2024-01-15T10:30:00Z"
      '400':
        description: Invalid request body
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      '409':
        description: Email already exists
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/Error'
      '422':
        description: Validation errors
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/ValidationError'
```

### Article 15: OpenAPI Quality Standards

**15.1** Documentation Requirements:

   (a) Every endpoint must have a summary
   
   (b) Every parameter must be documented
   
   (c) Every response type must be documented
   
   (d) Examples must be provided for all request/response bodies
   
   (e) Error responses must be documented

**15.2** Validation:

   (a) OpenAPI documents must validate against the OpenAPI specification
   
   (b) Use linters (Spectral, Redocly) for quality checks
   
   (c) Generate code from spec and verify correctness

---

## CHAPTER III: WEBHOOK AND EVENT HANDLING

### Article 16: Webhook Design Principles

**16.1** Webhooks provide event-driven communication and must be designed for reliability and predictability.

**16.2** Webhook Standards:

   (a) Use HTTPS for all webhook endpoints
   
   (b) Support signature verification for security
   
   (c) Provide event type in payload
   
   (d) Include delivery attempt tracking
   
   (e) Support idempotent consumers

### Article 17: Webhook Event Schema

**17.1** Standard Webhook Payload:

```json
{
  "id": "evt_1234567890abcdef",
  "type": "user.created",
  "api_version": "2024-01",
  "created_at": "2024-01-15T10:30:00Z",
  "data": {
    "object": {
      "id": "usr_1234567890abcdef",
      "email": "user@example.com",
      "full_name": "John Doe",
      "role": "user",
      "created_at": "2024-01-15T10:30:00Z"
    },
    "previous_attributes": {}
  },
  "metadata": {
    "delivery_attempt": 1,
    "delivery_id": "dlv_1234567890abcdef"
  }
}
```

**17.2** Event Type Naming:

   (a) Use dot notation: {resource}.{action}
   
   (b) Examples:
       - user.created
       - user.updated
       - user.deleted
       - order.status_changed
       - payment.succeeded
       - payment.failed

### Article 18: Webhook Delivery

**18.1** Delivery Requirements:

   (a) Deliver events reliably with retries
   
   (b) Support configurable retry schedules
   
   (c) Provide delivery logs and status
   
   (d) Support manual redelivery

**18.2** Retry Schedule:

   (a) Immediate retry on failure
   
   (b) Retry after 1 minute
   
   (c) Retry after 5 minutes
   
   (d) Retry after 30 minutes
   
   (e) Retry after 2 hours
   
   (f) Retry after 24 hours
   
   (g) Mark as failed after all retries exhausted

**18.3** Webhook Endpoint Requirements:

```python
class WebhookHandler:
    def handle_webhook(self, request: Request) -> Response:
        # 1. Verify signature
        signature = request.headers.get('X-Webhook-Signature')
        if not self.verify_signature(request.body, signature):
            return Response(status_code=401)
        
        # 2. Parse event
        event = json.loads(request.body)
        
        # 3. Idempotency check
        event_id = event['id']
        if self.event_processed(event_id):
            return Response(status_code=200, body='{"status": "already_processed"}')
        
        # 4. Process event
        try:
            self.process_event(event)
            self.mark_event_processed(event_id)
            return Response(status_code=200)
        except Exception as e:
            # Return 2xx to prevent retry for application errors
            if self.is_retryable_error(e):
                return Response(status_code=500)
            return Response(status_code=200)
    
    def verify_signature(self, payload: bytes, signature: str) -> bool:
        expected = hmac.new(
            self.webhook_secret,
            payload,
            hashlib.sha256
        ).hexdigest()
        return hmac.compare_digest(f'sha256={expected}', signature)
```

### Article 19: Event Processing Patterns

**19.1** Idempotency Implementation:

   (a) Store processed event IDs with timestamps
   
   (b) Check event ID before processing
   
   (c) Clean up old processed event records

**19.2** Ordering Considerations:

   (a) Events may arrive out of order
   
   (b) Include sequence numbers or timestamps for ordering
   
   (c) Handle stale events appropriately

**19.3** Consumer Design:

```python
class EventConsumer:
    def process_events(self, events: List[Event]) -> None:
        for event in events:
            # Idempotency check
            if self.already_processed(event.id):
                continue
            
            # Process with retry
            max_attempts = 3
            for attempt in range(max_attempts):
                try:
                    self.dispatch_event(event)
                    self.mark_processed(event.id)
                    break
                except Exception as e:
                    if attempt == max_attempts - 1:
                        self.handle_failure(event, e)
                    else:
                        time.sleep(2 ** attempt)
    
    def dispatch_event(self, event: Event) -> None:
        handlers = {
            'user.created': self.handle_user_created,
            'user.updated': self.handle_user_updated,
            'user.deleted': self.handle_user_deleted,
            # ... more handlers
        }
        
        handler = handlers.get(event.type)
        if handler:
            handler(event.data)
        else:
            logger.warning(f"No handler for event type: {event.type}")
```

---

## CHAPTER IV: THIRD-PARTY INTEGRATION RULES

### Article 20: Integration Architecture

**20.1** Third-party integrations must be:

   (a) Isolated from core business logic
   
   (b) Configurable without code changes
   
   (c) Monitored for health and performance
   
   (d) Documented with clear interfaces

**20.2** Integration Patterns:

   (a) **Adapter Pattern**: Translate between internal and external interfaces
   
   (b) **Circuit Breaker**: Prevent cascading failures
   
   (c) **Retry with Backoff**: Handle transient failures
   
   (d) **Request/Response Correlation**: Track distributed requests

### Article 21: External API Integration

**21.1** Integration Client Standards:

```python
class ExternalAPIClient:
    def __init__(self, config: IntegrationConfig):
        self.base_url = config.base_url
        self.api_key = config.api_key
        self.timeout = config.timeout
        self.retry_config = config.retry_config
        self.circuit_breaker = CircuitBreaker(
            failure_threshold=5,
            recovery_timeout=60,
        )
    
    def _request(self, method: str, path: str, **kwargs) -> Response:
        headers = kwargs.pop('headers', {})
        headers['Authorization'] = f'Bearer {self.api_key}'
        headers['Content-Type'] = 'application/json'
        headers['X-Request-Id'] = str(uuid.uuid4())
        
        @self.circuit_breaker
        def make_request():
            with retry(**self.retry_config):
                return self.session.request(
                    method=method,
                    url=f'{self.base_url}{path}',
                    headers=headers,
                    timeout=self.timeout,
                    **kwargs
                )
        
        return make_request()
```

**21.2** Rate Limiting Compliance:

   (a) Respect rate limits from external APIs
   
   (b) Implement request throttling
   
   (c) Handle 429 responses gracefully

**21.3** Error Handling:

   (a) Distinguish between transient and permanent errors
   
   (b) Implement retry logic for transient errors
   
   (c) Log and alert on external API failures

### Article 22: Circuit Breaker Implementation

**22.1** Circuit Breaker States:

   (a) **CLOSED**: Normal operation, requests pass through
   
   (b) **OPEN**: Failures exceeded threshold, requests blocked
   
   (c) **HALF_OPEN**: Testing if service recovered

**22.2** Circuit Breaker Pattern:

```python
from enum import Enum
import time
import threading

class CircuitState(Enum):
    CLOSED = "closed"
    OPEN = "open"
    HALF_OPEN = "half_open"

class CircuitBreaker:
    def __init__(
        self,
        failure_threshold: int = 5,
        recovery_timeout: int = 60,
        half_open_requests: int = 3,
    ):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_requests = half_open_requests
        
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.last_failure_time = None
        self.half_open_success = 0
        self.lock = threading.Lock()
    
    def call(self, func, *args, **kwargs):
        with self.lock:
            if self.state == CircuitState.OPEN:
                if self._should_attempt_reset():
                    self.state = CircuitState.HALF_OPEN
                    self.half_open_success = 0
                else:
                    raise CircuitOpenException(
                        f"Circuit breaker is OPEN. Retry after "
                        f"{self.recovery_timeout - (time.time() - self.last_failure_time):.0f}s"
                    )
            
            if self.state == CircuitState.HALF_OPEN:
                if self.half_open_success >= self.half_open_requests:
                    self._reset()
                    return func(*args, **kwargs)
        
        try:
            result = func(*args, **kwargs)
            self._on_success()
            return result
        except Exception as e:
            self._on_failure()
            raise
    
    def _on_success(self):
        with self.lock:
            if self.state == CircuitState.HALF_OPEN:
                self.half_open_success += 1
                if self.half_open_success >= self.half_open_requests:
                    self._reset()
            else:
                self.failure_count = 0
    
    def _on_failure(self):
        with self.lock:
            self.failure_count += 1
            self.last_failure_time = time.time()
            
            if self.failure_count >= self.failure_threshold:
                self.state = CircuitState.OPEN
    
    def _should_attempt_reset(self):
        return time.time() - self.last_failure_time >= self.recovery_timeout
    
    def _reset(self):
        self.state = CircuitState.CLOSED
        self.failure_count = 0
        self.half_open_success = 0
```

### Article 23: Webhook Receivers for Integrations

**23.1** Incoming Webhook Security:

   (a) Verify signatures on all incoming webhooks
   
   (b) Validate payload structure and content
   
   (c) Implement idempotency for processing

**23.2** Outgoing Webhook Client:

```python
class WebhookClient:
    def __init__(self, endpoint_url: str, secret: str):
        self.endpoint_url = endpoint_url
        self.secret = secret
        self.session = httpx.Client()
    
    def send(self, event: IntegrationEvent) -> WebhookDelivery:
        payload = json.dumps(event.to_dict())
        signature = self._sign(payload)
        
        try:
            response = self.session.post(
                self.endpoint_url,
                content=payload,
                headers={
                    'Content-Type': 'application/json',
                    'X-Webhook-Signature': signature,
                    'X-Webhook-Timestamp': str(int(time.time())),
                },
                timeout=30,
            )
            
            return WebhookDelivery(
                success=response.status_code == 200,
                status_code=response.status_code,
                response_body=response.text[:1000],
            )
        except Exception as e:
            return WebhookDelivery(
                success=False,
                error=str(e),
            )
    
    def _sign(self, payload: str) -> str:
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()
```

---

## CHAPTER V: RATE LIMITING AND THROTTLING

### Article 24: Rate Limiting Architecture

**24.1** Rate limiting must be implemented at multiple layers:

   (a) API Gateway level
   
   (b) Application level
   
   (c) Individual endpoint level

**24.2** Rate Limit Configuration:

   (a) Define limits per endpoint category
   
   (b) Support different limits for authenticated vs anonymous
   
   (c) Allow configuration without code changes

**24.3** Rate Limit Headers:

```
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 999
X-RateLimit-Reset: 1705315800
Retry-After: 3600
```

### Article 25: Rate Limiting Implementation

**25.1** Token Bucket Algorithm:

```python
import time
from threading import Lock

class TokenBucket:
    def __init__(self, capacity: int, refill_rate: float):
        self.capacity = capacity
        self.refill_rate = refill_rate  # tokens per second
        self.tokens = capacity
        self.last_refill = time.time()
        self.lock = Lock()
    
    def consume(self, tokens: int = 1) -> bool:
        with self.lock:
            self._refill()
            
            if self.tokens >= tokens:
                self.tokens -= tokens
                return True
            return False
    
    def _refill(self):
        now = time.time()
        elapsed = now - self.last_refill
        self.tokens = min(
            self.capacity,
            self.tokens + (elapsed * self.refill_rate)
        )
        self.last_refill = now

class RateLimiter:
    def __init__(self):
        self.limiters: Dict[str, TokenBucket] = {}
        self.lock = Lock()
    
    def get_limiter(self, key: str, capacity: int, refill_rate: float) -> TokenBucket:
        with self.lock:
            if key not in self.limiters:
                self.limiters[key] = TokenBucket(capacity, refill_rate)
            return self.limiters[key]
    
    def check_limit(self, key: str, cost: int = 1) -> tuple[bool, dict]:
        limiter = self.limiters.get(key)
        if not limiter:
            return True, {}
        
        allowed = limiter.consume(cost)
        remaining = int(limiter.tokens)
        reset_time = int(time.time() + (limiter.capacity - remaining) / limiter.refill_rate)
        
        return allowed, {
            'X-RateLimit-Limit': str(limiter.capacity),
            'X-RateLimit-Remaining': str(max(0, remaining)),
            'X-RateLimit-Reset': str(reset_time),
        }
```

**25.2** Rate Limit Tiers:

| Tier | Requests/Minute | Burst | Use Case |
|------|-----------------|-------|----------|
| Free | 60 | 10 | Development, testing |
| Standard | 1000 | 100 | Normal usage |
| Premium | 10000 | 1000 | High-volume clients |
| Enterprise | 100000 | 10000 | Custom agreements |

### Article 26: Throttling Strategies

**26.1** Request Throttling:

   (a) Slow down requests that exceed rate limits
   
   (b) Return Retry-After header with appropriate delay
   
   (c) Implement progressive throttling

**26.2** Response Headers:

```python
def throttling_middleware(request, call_next):
    client_id = get_client_id(request)
    rate_limit = get_rate_limit(client_id)
    
    allowed, headers = rate_limiter.check_limit(client_id)
    
    if not allowed:
        retry_after = calculate_retry_after(client_id)
        return Response(
            status_code=429,
            headers={
                **headers,
                'Retry-After': str(retry_after),
            },
            content=json.dumps({
                'error': 'rate_limit_exceeded',
                'message': 'Too many requests',
                'retry_after': retry_after,
            })
        )
    
    response = call_next(request)
    
    # Add rate limit headers to successful responses
    for header, value in headers.items():
        response.headers[header] = value
    
    return response
```

---

## CHAPTER VI: RESPONSE FORMATTING STANDARDS

### Article 27: Response Format Standards

**27.1** Standard Success Response:

```json
{
  "data": { ... },
  "meta": {
    "request_id": "req_1234567890",
    "timestamp": "2024-01-15T10:30:00Z",
    "version": "v1"
  }
}
```

**27.2** Standard Error Response:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains validation errors",
    "details": [
      {
        "field": "email",
        "code": "INVALID_FORMAT",
        "message": "Email address is not valid"
      },
      {
        "field": "full_name",
        "code": "REQUIRED",
        "message": "Full name is required"
      }
    ],
    "request_id": "req_1234567890",
    "docs_url": "https://docs.example.com/errors/VALIDATION_ERROR"
  }
}
```

**27.3** Standard List Response:

```json
{
  "data": [
    { ... },
    { ... }
  ],
  "pagination": {
    "total_count": 1000,
    "page": 1,
    "page_size": 20,
    "total_pages": 50,
    "next_page": "eyJpZCI6MTAwfQ==",
    "prev_page": null
  },
  "meta": {
    "request_id": "req_1234567890",
    "timestamp": "2024-01-15T10:30:00Z"
  }
}
```

### Article 28: HTTP Status Code Usage

**28.1** Success Codes:

   | Code | Meaning | Usage |
   |------|---------|-------|
   | 200 | OK | Successful GET, PUT, PATCH, DELETE |
   | 201 | Created | Successful POST creating resource |
   | 202 | Accepted | Async operation accepted |
   | 204 | No Content | Successful DELETE with no body |

**28.2** Client Error Codes:

   | Code | Meaning | Usage |
   |------|---------|-------|
   | 400 | Bad Request | Malformed request syntax |
   | 401 | Unauthorized | Missing authentication |
   | 403 | Forbidden | Authenticated but not authorized |
   | 404 | Not Found | Resource doesn't exist |
   | 405 | Method Not Allowed | HTTP method not supported |
   | 409 | Conflict | Resource conflict (duplicate) |
   | 422 | Unprocessable Entity | Semantic validation error |
   | 429 | Too Many Requests | Rate limit exceeded |

**28.3** Server Error Codes:

   | Code | Meaning | Usage |
   |------|---------|-------|
   | 500 | Internal Server Error | Unexpected server error |
   | 502 | Bad Gateway | Upstream service error |
   | 503 | Service Unavailable | Temporary unavailability |
   | 504 | Gateway Timeout | Upstream timeout |

### Article 29: Pagination Standards

**29.1** Cursor-Based Pagination:

```python
class CursorPagination:
    def paginate(self, query, cursor, page_size):
        if cursor:
            cursor_data = json.loads(base64.b64decode(cursor))
            query = query.where(self.model.id < cursor_data['id'])
        
        items = query.limit(page_size + 1).all()
        
        has_more = len(items) > page_size
        if has_more:
            items = items[:-1]
        
        next_cursor = None
        if has_more and items:
            next_cursor = base64.b64encode(json.dumps({
                'id': items[-1].id
            }).encode()).decode()
        
        return items, next_cursor
```

**29.2** Offset-Based Pagination:

   (a) Use for small, bounded datasets
   
   (b) Specify max page size to prevent performance issues
   
   (c) Include total count for UI pagination

### Article 30: Content Negotiation

**30.1** Supported Formats:

   (a) **application/json**: Default and preferred
   
   (b) **application/xml**: Optional legacy support
   
   (c) **text/csv**: For data export

**30.2** Content Type Handling:

```
Request:  Accept: application/json
Response: Content-Type: application/json
```

### Article 31: API Versioning

**31.1** Versioning Strategy:

   (a) Use URL path versioning: /v1/users, /v2/users
   
   (b) Include version in response headers: API-Version: v1
   
   (c) Maintain backward compatibility within major versions

**31.2** Version Lifecycle:

   (a) **Current**: Active development, full support
   
   (b) **Deprecated**: Maintenance mode, sunset announced
   
   (c) **Sunset**: End of life, no longer available

**31.3** Deprecation Policy:

   (a) Minimum 6 months between deprecation announcement and sunset
   
   (b) Include deprecation headers in responses
   
   (c) Document migration path in changelog

---

## CHAPTER VII: API SECURITY

### Article 32: Authentication Standards

**32.1** Authentication Methods:

   (a) **Bearer Token (JWT)**: Preferred for most APIs
   
   (b) **API Keys**: For service-to-service, simple integrations
   
   (c) **OAuth 2.0**: For user-authorized third-party access

**32.2** JWT Standards:

```json
{
  "header": {
    "alg": "RS256",
    "typ": "JWT",
    "kid": "key-id-1"
  },
  "payload": {
    "sub": "user_123",
    "iss": "https://auth.example.com",
    "aud": ["api.example.com"],
    "exp": 1705319400,
    "iat": 1705315800,
    "jti": "unique-token-id",
    "scope": ["read:users", "write:users"],
    "tenant_id": "tenant_456"
  }
}
```

**32.3** Token Validation:

   (a) Verify signature with public key
   
   (b) Validate expiration (exp claim)
   
   (c) Validate issuer (iss claim)
   
   (d) Validate audience (aud claim)
   
   (e) Check token not in revocation list

### Article 33: Authorization Standards

**33.1** Authorization Patterns:

   (a) **Scope-Based**: Token contains permitted scopes
   
   (b) **Role-Based**: Token contains user role
   
   (c) **Policy-Based**: Dynamic evaluation of permissions

**33.2** Scope Definitions:

```
read:users      - View user information
write:users     - Create and update users
delete:users    - Delete users
read:orders     - View orders
write:orders    - Create and update orders
admin:users     - Administrative user operations
```

### Article 34: Input Validation

**34.1** Request Validation:

   (a) Validate all input parameters
   
   (b) Use schema validation libraries
   
   (c) Return 400 for validation failures

**34.2** Validation Response:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "email",
        "code": "INVALID_EMAIL",
        "message": "Must be a valid email address"
      },
      {
        "field": "age",
        "code": "OUT_OF_RANGE",
        "message": "Must be between 1 and 150"
      }
    ],
    "request_id": "req_1234567890"
  }
}
```

### Article 35: Output Filtering

**35.1** Sensitive Data Filtering:

   (a) Never return passwords or password hashes
   
   (b) Filter internal fields from responses
   
   (c) Use field filtering for sensitive data

**35.2** Field Filtering Example:

```python
class UserSerializer:
    SENSITIVE_FIELDS = {'password_hash', 'internal_notes'}
    ADMIN_ONLY_FIELDS = {'login_history', 'audit_log'}
    
    def serialize(self, user: User, fields: List[str] = None) -> dict:
        data = {
            'id': user.id,
            'email': user.email,
            'full_name': user.full_name,
            'role': user.role,
            'created_at': user.created_at.isoformat(),
        }
        
        if not fields:
            # Default: exclude sensitive fields
            return {k: v for k, v in data.items() if k not in self.SENSITIVE_FIELDS}
        
        # Field filtering
        return {k: v for k, v in data.items() if k in fields}
```

---

## CHAPTER VIII: API DOCUMENTATION

### Article 36: Documentation Standards

**36.1** Documentation Requirements:

   (a) Complete OpenAPI specification
   
   (b) Getting started guides
   
   (c) Authentication/authorization documentation
   
   (d) Code examples in multiple languages
   
   (e) Error code reference
   
   (f) Changelog with breaking changes highlighted

**36.2** Documentation Structure:

```
docs/
├── index.md                    # Main documentation page
├── getting-started/
│   ├── authentication.md
│   ├── quickstart.md
│   └── errors.md
├── api/
│   ├── users.md
│   ├── orders.md
│   └── ...
├── guides/
│   ├── webhooks.md
│   ├── rate-limiting.md
│   └── pagination.md
├── sdks/
│   ├── python.md
│   ├── javascript.md
│   └── ...
├── changelog.md
└── openapi.yaml
```

### Article 37: API Reference Standards

**37.1** Endpoint Documentation Template:

```markdown
## Get User

Retrieves a user by their unique identifier.

### Request

```http
GET /v1/users/{userId}
Authorization: Bearer {token}
```

### Path Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| userId | UUID | Yes | The unique identifier of the user |

### Headers

| Header | Required | Description |
|--------|----------|-------------|
| Authorization | Yes | Bearer token for authentication |

### Response

#### 200 OK

```json
{
  "data": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "created_at": "2024-01-15T10:30:00Z"
  }
}
```

#### 404 Not Found

```json
{
  "error": {
    "code": "USER_NOT_FOUND",
    "message": "User with the specified ID was not found"
  }
}
```

### Code Examples

#### Python

```python
import requests

response = requests.get(
    'https://api.example.com/v1/users/user_123',
    headers={'Authorization': 'Bearer ' + token}
)
user = response.json()
```

#### JavaScript

```javascript
const response = await fetch('https://api.example.com/v1/users/user_123', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const { data: user } = await response.json();
```
```

---

## CHAPTER IX: API TESTING AND MONITORING

### Article 38: API Testing Standards

**38.1** Testing Categories:

   (a) **Contract Testing**: Verify API matches specification
   
   (b) **Integration Testing**: Test API with real dependencies
   
   (c) **End-to-End Testing**: Test complete user flows
   
   (d) **Performance Testing**: Load and stress testing

**38.2** Contract Testing:

```python
# Using Pact for contract testing
@pytest.fixture
def user_client():
    return PactConsumer('UserService').has_pact_with(
        PactProvider('UserAPI'), port=1234
    )

def test_get_user(user_client):
    (user_client
     .given('a user exists')
     .upon_receiving('a request for user')
     .with_methods(
         method='GET',
         path='/v1/users/user_123',
         headers={'Authorization': 'Bearer token'}
     )
     .will_respond_with(
         status=200,
         body={
             'data': Match({
                 'id': 'user_123',
                 'email': 'user@example.com',
                 'full_name': 'Test User'
             })
         }
     ))
```

**38.3** Performance Testing:

   (a) Establish baseline performance metrics
   
   (b) Test at expected peak load
   
   (c) Test at 2x expected peak load
   
   (d) Identify bottlenecks and optimize

### Article 39: API Monitoring

**39.1** Monitoring Metrics:

   (a) Request rate (requests per second)
   
   (b) Response time (p50, p95, p99)
   
   (c) Error rate (by status code)
   
   (d) Availability (uptime percentage)

**39.2** Alerting Thresholds:

   | Metric | Warning | Critical |
   |--------|---------|----------|
   | Error Rate | > 1% | > 5% |
   | p99 Latency | > 500ms | > 2000ms |
   | Availability | < 99.9% | < 99% |

**39.3** Health Check Endpoint:

```yaml
/health:
  get:
    summary: Health check
    description: |
      Returns the health status of the API.
      Use this endpoint for load balancer health checks.
    responses:
      '200':
        description: Service is healthy
        content:
          application/json:
            schema:
              type: object
              properties:
                status:
                  type: string
                  example: healthy
                version:
                  type: string
                  example: "1.0.0"
                timestamp:
                  type: string
                  format: date-time
                dependencies:
                  type: object
                  properties:
                    database:
                      type: string
                      example: healthy
                    cache:
                      type: string
                      example: healthy
```

---

## CHAPTER X: DEPRECATION AND SUNSET

### Article 40: Deprecation Process

**40.1** Deprecation Announcement:

   (a) Document deprecation in changelog
   
   (b) Include sunset date
   
   (c) Add Deprecation header to responses
   
   (d) Notify API consumers directly

**40.2** Deprecation Headers:

```
Deprecation: true
Sunset: Sat, 31 Dec 2024 23:59:59 GMT
Link: <https://api.example.com/changelog>; rel="deprecation"; type="text/html"
Deprecated-Links: <https://docs.example.com/migration/v1-to-v2>; rel="successor-version"
```

### Article 41: Migration Support

**41.1** Migration Assistance:

   (a) Provide clear migration guides
   
   (b) Support both old and new APIs during transition
   
   (c) Offer technical assistance for complex migrations
   
   (d) Consider grace periods for enterprise clients

**41.2** Sunset Timeline:

   (a) Minimum 6 months notice for breaking changes
   
   (b) Provide migration tooling where possible
   
   (c) Monitor usage during transition period

---

## SCHEDULES AND ANNEXURES

### Schedule I: API Design Checklist

**Request Design:**
- [ ] Use consistent naming conventions (lowercase, hyphens)
- [ ] Follow RESTful resource patterns
- [ ] Include pagination for list endpoints
- [ ] Document all parameters and their validation
- [ ] Support filtering, sorting, field selection

**Response Design:**
- [ ] Use consistent response envelope format
- [ ] Include request_id in all responses
- [ ] Document all error codes
- [ ] Provide examples for all responses
- [ ] Use appropriate HTTP status codes

**Security:**
- [ ] Require authentication for all endpoints
- [ ] Document authorization requirements
- [ ] Implement rate limiting
- [ ] Validate all input
- [ ] Filter sensitive data from responses

**Documentation:**
- [ ] Complete OpenAPI specification
- [ ] Code examples in multiple languages
- [ ] Error code reference
- [ ] Getting started guide
- [ ] Changelog

### Schedule II: HTTP Status Code Reference

| Code | Name | When to Use |
|------|------|-------------|
| 200 | OK | Successful operation |
| 201 | Created | Resource created |
| 204 | No Content | Successful delete |
| 400 | Bad Request | Invalid request syntax |
| 401 | Unauthorized | Authentication required |
| 403 | Forbidden | Not authorized |
| 404 | Not Found | Resource not found |
| 405 | Method Not Allowed | HTTP method not supported |
| 409 | Conflict | Resource conflict |
| 422 | Unprocessable Entity | Validation error |
| 429 | Too Many Requests | Rate limit exceeded |
| 500 | Internal Server Error | Server error |
| 502 | Bad Gateway | Upstream error |
| 503 | Service Unavailable | Service down |
| 504 | Gateway Timeout | Upstream timeout |

### Schedule III: Error Code Standards

| Code | Description | HTTP Status |
|------|-------------|-------------|
| INVALID_REQUEST | Malformed request syntax | 400 |
| INVALID_CREDENTIALS | Authentication failed | 401 |
| PERMISSION_DENIED | Not authorized | 403 |
| NOT_FOUND | Resource not found | 404 |
| CONFLICT | Resource conflict | 409 |
| VALIDATION_ERROR | Request validation failed | 422 |
| RATE_LIMIT_EXCEEDED | Too many requests | 429 |
| INTERNAL_ERROR | Server error | 500 |
| SERVICE_UNAVAILABLE | Service temporarily unavailable | 503 |

### Schedule IV: Authentication Method Reference

| Method | Use Case | Security Level |
|--------|---------|----------------|
| Bearer (JWT) | User authentication | High |
| API Key | Service-to-service | Medium |
| OAuth 2.0 | User-authorized third-party | High |
| Basic Auth | Simple internal APIs | Low (use TLS) |

---

## ENFORCEMENT AND INTERPRETATION

### Article 42: Enforcement

**42.1** All requirements in this skill are MANDATORY unless explicitly stated as RECOMMENDED.

**42.2** API changes must follow versioning and deprecation policies.

**42.3** Breaking changes require proper communication and transition periods.

### Article 43: Interpretation

**43.1** API working group has authority over API standards interpretation.

**43.2** Exceptions require documented justification and review.

**43.3** Standards evolution will be guided by community feedback and industry best practices.

### Article 44: Updates and Amendments

**44.1** This skill must be reviewed quarterly.

**44.2** Version bumps required for breaking changes.

**44.3** New API patterns will be incorporated as they emerge.

---

*End of Part XI: API and Integration Standards*
