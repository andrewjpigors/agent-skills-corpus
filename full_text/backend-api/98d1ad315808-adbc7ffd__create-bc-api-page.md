---
name: create-bc-api-page
description: Guide for creating production-ready API pages in Microsoft Dynamics 365 Business Central. Use this when asked to create an API page, REST API endpoint, or expose Business Central data via OData.
license: MIT
---

# Create Business Central API Page

This skill guides you through creating a complete, production-ready API page for Microsoft Dynamics 365 Business Central following Microsoft's best practices and OData standards.

## When to Use This Skill

- Creating new RESTful API endpoints
- Exposing Business Central data via OData
- Building integration endpoints for external systems (Power Platform, mobile apps, third-party services)
- Implementing custom API operations beyond standard CRUD

## Prerequisites

Before starting, ensure:
- Valid `app.json` with API publisher and version defined
- Source table exists or specification is available
- Understanding of required operations (CRUD, custom actions)
- Authentication/authorization requirements defined
- Understanding of the data model and business rules

## Step-by-Step Process

### 1. Gather Requirements

Ask the user to provide or confirm:

**Entity Information:**
- **Entity Name**: What resource should be exposed? (e.g., "salesOrder", "customer", "customProduct")
- **Source Table**: Which Business Central table contains the data?
- **Purpose**: What business scenario does this API support?

**API Configuration:**
- **API Version**: Which version? (v1.0, v2.0, or custom like beta)
- **API Publisher**: Your company/publisher identifier (lowercase, hyphenated)
- **API Group**: Logical grouping (e.g., "sales", "inventory", "finance", "custom")
- **AboutText** (REQUIRED): Clear description of the business scenario this API supports (used for MCP context and API discoverability)

**Operations:**
- **CRUD Operations**: Which operations are needed? (GET, POST, PATCH, DELETE)
- **Custom Actions**: Any business operations? (e.g., post, approve, calculate, process)

**Data Design:**
- **Fields**: Which fields should be exposed? (Use subsets for performance, not all table fields)
- **Calculated Fields**: Any computed fields needed?
- **Navigation Properties**: Related entities to include? (e.g., customer → salesOrders → lines)
- **Filters**: Common filtering scenarios to optimize?

**Non-Functional Requirements:**
- **Performance**: Expected volume and response time requirements
- **Security**: Data sensitivity and authorization needs
- **Versioning**: Future compatibility considerations

### 2. Reserve Object ID

**CRITICAL: Always reserve an object ID before creating the page to prevent ID collisions.**

Use the Object ID reservation tool:
```
Use: vjeko-al-objid_getNextObjectId
Parameters:
  - objectType: "page"
  - targetFilePath: "<absolute-path-where-file-will-be-created>"
  - rangeName: (optional, only if multiple ranges configured)
```

**Important Rules:**
- ✅ ALWAYS use the ID reservation tool first
- ❌ NEVER hardcode or guess object IDs
- ✅ Document the reserved ID
- ✅ If the project fails, unassign the ID using `vjeko-al-objid_unassignObjectId`

### 3. Determine File Location and Name

**File Location:** 
- Primary: `src/Page/` or `src/API/` (if separate API folder exists)
- Feature-based: `src/<FeatureName>/Page/` (for larger projects)

**Naming Convention:**
- Format: `<Prefix><EntityName>API.Page.al`
- Examples: 
  - `BCSSalesOrdersAPI.Page.al`
  - `BCSCustomProductsAPI.Page.al`
- Use PascalCase for file names
- Prefix should match your project's naming convention (typically 3-4 letters)

### 4. Create API Page Structure

Create the file with the following template, adapting to requirements:

```al
page <ObjectID> "<Prefix> <Entity Name> API"
{
  APIVersion = 'v2.0';
  APIPublisher = '<your-publisher>';
  APIGroup = '<api-group>';
  EntityName = '<entityName>';      // Singular, camelCase (e.g., 'salesOrder')
  EntitySetName = '<entitySetName>'; // Plural, camelCase (e.g., 'salesOrders')
  AboutText = '<Clear description of the business scenario this API supports>'; // REQUIRED for MCP context
  
  PageType = API;
  Caption = '<Entity Name> API';
  SourceTable = "<Source Table>";
  DelayedInsert = true;
  ODataKeyFields = SystemId;         // ALWAYS use SystemId for v2.0 APIs
  
  layout
  {
    area(Content)
    {
      repeater(Group)
      {
        // System fields (required)
        field(id; Rec.SystemId)
        {
          Caption = 'Id';
          Editable = false;
        }
        
        // Primary identifier
        field(number; Rec."No.")
        {
          Caption = 'Number';
        }
        
        // Add business fields here
        // Pattern: field(camelCaseName; Rec."Business Central Field Name")
        
        // Calculated/FlowFields
        field(totalAmount; Rec."Amount Including VAT")
        {
          Caption = 'Total Amount';
          Editable = false;
          AutoFormatType = 1;
          AutoFormatExpression = Rec."Currency Code";
        }
        
        // Timestamp fields (recommended for sync scenarios)
        field(lastModifiedDateTime; Rec.SystemModifiedAt)
        {
          Caption = 'Last Modified Date Time';
          Editable = false;
        }
      }
    }
  }
}
```

**Key Configuration Points:**

- **APIVersion**: Use 'v2.0' for modern APIs (supports SystemId, better OData support)
- **APIPublisher**: Lowercase, use hyphens for spaces (e.g., 'my-company')
- **APIGroup**: Logical grouping for API organization (lowercase, hyphenated)
- **EntityName**: Singular, camelCase - represents a single resource
- **EntitySetName**: Plural, camelCase - represents the collection
- **ODataKeyFields**: ALWAYS set to `SystemId` for v2.0 APIs (enables stable references)
- **DelayedInsert**: Set to `true` to prevent premature record creation
- **AboutText** (REQUIRED): MUST provide a clear description of the business scenario and purpose of this API. This is essential for MCP context, API discoverability, and understanding the API's intent. Example: 'Provides access to sales orders for integration with e-commerce platforms and third-party sales tools.'


### 5. Implement Field Mappings

**Field Naming Rules:**
- Use `camelCase` for API field names (e.g., `customerNumber`, `orderDate`, `totalAmount`)
- Map to Business Central fields using `Rec."Field Name"` syntax
- Keep field names intuitive and consistent with REST/JSON conventions

**Field Types and Properties:**

```al
// Simple text/code field
field(customerNumber; Rec."Sell-to Customer No.")
{
  Caption = 'Customer Number';
}

// Date field
field(orderDate; Rec."Order Date")
{
  Caption = 'Order Date';
}

// Decimal field with formatting
field(unitPrice; Rec."Unit Price")
{
  Caption = 'Unit Price';
  AutoFormatType = 2;  // Currency format
  AutoFormatExpression = Rec."Currency Code";
}

// Boolean field (Option in BC)
field(isBlocked; Rec.Blocked)
{
  Caption = 'Is Blocked';
}

// Calculated field (FlowField)
field(balance; Rec.Balance)
{
  Caption = 'Balance';
  Editable = false;
  FieldClass = FlowField;
}

// Read-only system field
field(createdDateTime; Rec.SystemCreatedAt)
{
  Caption = 'Created Date Time';
  Editable = false;
}

// Field with custom validation
field(status; Rec.Status)
{
  Caption = 'Status';
  
  trigger OnValidate()
  begin
    // Custom validation logic
    if Rec.Status = Rec.Status::Released then
      Rec.TestField("Sell-to Customer No.");
  end;
}
```

**Best Practices for Fields:**
- ✅ Mark SystemId and auto-generated fields as `Editable = false`
- ✅ Use proper AutoFormat for currency and decimal fields
- ✅ Include timestamp fields for synchronization scenarios
- ✅ Only expose fields necessary for the API consumer (performance)
- ❌ Don't expose all table fields - be selective
- ❌ Don't expose sensitive fields without proper authorization

### 6. Add Navigation Properties (Related Entities)

For one-to-many or one-to-one relationships, add navigation properties:

```al
layout
{
  area(Content)
  {
    repeater(Group)
    {
      // Main entity fields...
    }
    
    // Navigation to related entities
    part(salesOrderLines; "<Prefix> Sales Order Lines API")
    {
      Caption = 'Lines';
      EntityName = 'salesOrderLine';
      EntitySetName = 'salesOrderLines';
      SubPageLink = "Document No." = field("No.");
    }
    
    part(shipmentDetails; "<Prefix> Shipment API")
    {
      Caption = 'Shipment Details';
      EntityName = 'shipmentDetail';
      EntitySetName = 'shipmentDetails';
      SubPageLink = "Order No." = field("No.");
    }
  }
}
```

**Navigation Property Guidelines:**
- Use for frequently accessed related data
- Consider performance impact (lazy loading vs eager loading with $expand)
- Ensure related API pages exist or will be created
- Use appropriate SubPageLink to establish relationship

### 7. Implement Record Triggers (Validation & Business Logic)

Add validation and business logic in the appropriate triggers:

```al
trigger OnInsertRecord(BelowxRec: Boolean): Boolean
begin
  // Set default values
  if Rec."Order Date" = 0D then
    Rec."Order Date" := WorkDate();
  
  // Validate required fields
  if Rec."Sell-to Customer No." = '' then
    Error('Customer Number is required');
  
  // Business validation
  ValidateCustomer(Rec."Sell-to Customer No.");
  
  // Initialize calculated fields or state
  Rec."Document Type" := Rec."Document Type"::Order;
  
  exit(true);  // Return true to allow insert
end;

trigger OnModifyRecord(): Boolean
begin
  // Prevent modification of locked records
  if Rec.Status = Rec.Status::Released then
    Error('Cannot modify released sales order. Change status to Open first.');
  
  // Validate business rules
  if Rec."Shipment Date" < Rec."Order Date" then
    Error('Shipment date cannot be before order date');
  
  exit(true);  // Return true to allow modification
end;

trigger OnDeleteRecord(): Boolean
var
  SalesInvoiceHeader: Record "Sales Invoice Header";
begin
  // Prevent deletion of records with dependencies
  SalesInvoiceHeader.SetRange("Order No.", Rec."No.");
  if not SalesInvoiceHeader.IsEmpty() then
    Error('Cannot delete sales order with posted invoices');
  
  // Soft delete check
  if Rec.Status = Rec.Status::Released then
    Error('Cannot delete released sales order');
  
  exit(true);  // Return true to allow deletion
end;

trigger OnAfterGetRecord()
begin
  // Performance optimization: Load only required fields
  Rec.SetLoadFields("No.", "Sell-to Customer No.", "Order Date", "Amount Including VAT");
  
  // Calculate additional fields if needed
  CalculateTotals();
end;

// Helper procedures
local procedure ValidateCustomer(CustomerNo: Code[20])
var
  Customer: Record Customer;
begin
  if not Customer.Get(CustomerNo) then
    Error('Customer %1 does not exist', CustomerNo);
  
  if Customer.Blocked <> Customer.Blocked::" " then
    Error('Customer %1 is blocked', CustomerNo);
  
  // Additional validation as needed
  Customer.CheckCreditLimit(Rec."Amount Including VAT");
end;

local procedure CalculateTotals()
begin
  // Calculate any derived values
  Rec.CalcFields("Amount Including VAT");
end;
```

**Trigger Guidelines:**
- **OnInsertRecord**: Validate required fields, set defaults, initialize state
- **OnModifyRecord**: Validate business rules, prevent invalid state transitions
- **OnDeleteRecord**: Check dependencies, prevent orphaned data
- **OnAfterGetRecord**: Optimize field loading, calculate derived values
- Always return `true` to allow the operation, or call `Error()` to prevent it

### 8. Implement Custom Actions (Optional)

Add custom business operations as actions:

#### Bound Actions (operate on a specific entity)

```al
actions
{
  area(Processing)
  {
    // Action to post a sales order
    action(Post)
    {
      ApplicationArea = All;
      Caption = 'Post';
      
      trigger OnAction()
      var
        SalesPost: Codeunit "Sales-Post";
        PostedDocNo: Code[20];
      begin
        // Validate preconditions
        if Rec.Status <> Rec.Status::Released then
          Error('Sales order must be released before posting');
        
        if not Confirm('Do you want to post sales order %1?', false, Rec."No.") then
          exit;
        
        // Perform operation
        SalesPost.Run(Rec);
        
        // Get result
        PostedDocNo := GetPostedInvoiceNo(Rec);
        
        // Return result to API consumer
        Message('Sales order posted. Invoice No.: %1', PostedDocNo);
      end;
    }
    
    // Action with parameters
    action(ApplyDiscount)
    {
      ApplicationArea = All;
      Caption = 'Apply Discount';
      
      trigger OnAction()
      var
        DiscountPct: Decimal;
        NewAmount: Decimal;
      begin
        // Get parameter from API request (implementation depends on BC version)
        // DiscountPct := GetActionParameter('discountPercent');
        
        // Validate
        if (DiscountPct < 0) or (DiscountPct > 100) then
          Error('Discount percentage must be between 0 and 100');
        
        // Apply discount
        ApplyDiscountToOrder(Rec, DiscountPct);
        Rec.Modify(true);
        
        // Return updated amount
        Rec.CalcFields("Amount Including VAT");
        NewAmount := Rec."Amount Including VAT";
        
        Message('Discount applied. New amount: %1', NewAmount);
      end;
    }
  }
}
```

#### Unbound Actions (standalone operations)

```al
// For unbound actions, create a separate API page with a dummy table
page 50200 "BCS Utility Functions API"
{
  APIVersion = 'v2.0';
  APIPublisher = 'my-company';
  APIGroup = 'utilities';
  
  PageType = API;
  EntityName = 'utilityFunction';
  EntitySetName = 'utilityFunctions';
  SourceTable = Integer;  // Dummy table
  
  actions
  {
    area(Processing)
    {
      action(CalculateShipping)
      {
        ApplicationArea = All;
        Caption = 'Calculate Shipping';
        
        trigger OnAction()
        var
          Weight: Decimal;
          Destination: Code[20];
          ShippingCost: Decimal;
        begin
          // Get parameters
          // Weight := GetActionParameter('weight');
          // Destination := GetActionParameter('destination');
          
          // Calculate
          ShippingCost := CalculateShippingCost(Weight, Destination);
          
          // Return result
          Message('Shipping cost: %1', ShippingCost);
        end;
      }
    }
  }
}
```

**Action Guidelines:**
- Use actions for operations beyond CRUD (post, approve, calculate, etc.)
- Bound actions: POST to `/entitySetName({id})/Microsoft.NAV.actionName`
- Unbound actions: POST to `/utilityFunctions/Microsoft.NAV.actionName`
- Always validate preconditions
- Use `Message()` or custom response mechanisms to return results
- Consider idempotency for non-GET operations

### 9. Optimize for Performance

**Field Loading:**
```al
trigger OnAfterGetRecord()
begin
  // Only load fields that are exposed in the API
  Rec.SetLoadFields("No.", "Sell-to Customer No.", "Order Date", "Amount Including VAT");
end;
```

**Table Keys:**
Ensure source table has appropriate keys for common query patterns:
```al
// Document to user: Verify source table has these keys
// - Primary key (clustered)
// - Keys for common filters (customer, date ranges, status)
// - Keys for navigation properties (foreign key fields)
```

**Filtering Best Practices:**
- Support OData filtering: `$filter=customerNumber eq 'C00001'`
- Use indexed fields in filters
- Avoid complex calculated fields in filters
- Test performance with realistic data volumes

**Change Tracking:**
- Include `lastModifiedDateTime` field
- API automatically provides `@odata.deltaLink` for efficient sync
- Use delta links for incremental synchronization scenarios

### 10. Build and Test

**Compile the extension:**
```
Use: al_build
```

**Publish to test environment:**
```
Use: al_incrementalpublish (faster for iterative development)
or: al_publish (full publish with debugging)
```

**Test API Endpoints:**

Test using tools like Postman, Insomnia, or PowerShell:

```powershell
# Get company ID first
GET https://<bc-instance>/api/v2.0/companies

# GET Collection (list all)
GET https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>

# GET Single (retrieve one)
GET https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>({id})

# POST Create (create new)
POST https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>
Content-Type: application/json

{
  "customerNumber": "C00001",
  "orderDate": "2024-01-15",
  ...
}

# PATCH Update (modify existing)
PATCH https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>({id})
Content-Type: application/json
If-Match: * (or specific ETag)

{
  "orderDate": "2024-01-20",
  ...
}

# DELETE (remove)
DELETE https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>({id})

# Custom Action
POST https://<bc-instance>/api/v2.0/companies({companyId})/<entitySetName>({id})/Microsoft.NAV.<actionName>
```

**OData Query Testing:**
```
# Select specific fields
GET .../salesOrders?$select=number,customerNumber,totalAmount

# Filter records
GET .../salesOrders?$filter=customerNumber eq 'C00001' and orderDate ge 2024-01-01

# Expand navigation properties
GET .../salesOrders?$expand=salesOrderLines

# Pagination
GET .../salesOrders?$top=50&$skip=0

# Ordering
GET .../salesOrders?$orderby=orderDate desc

# Count
GET .../salesOrders?$count=true
```

### 11. Document the API

Create API documentation in `.github/plans/<entity>-api-design.md`:

```markdown
# <Entity Name> API Specification

## Overview
- **Endpoint**: `/api/v2.0/companies({companyId})/<entitySetName>`
- **Version**: v2.0
- **Publisher**: <your-publisher>
- **Group**: <api-group>
- **Authentication**: OAuth 2.0 / Basic Auth
- **Source Table**: <Table Name> (<Table ID>)
- **Purpose**: <Brief description of what this API enables>

## Resource Model

### Entity: <entityName> (singular)
### Collection: <entitySetName> (plural)

## Operations Supported
- ✅ GET (List) - Retrieve collection with filtering/pagination
- ✅ GET (Single) - Retrieve specific entity by ID
- ✅ POST (Create) - Create new entity
- ✅ PATCH (Update) - Modify existing entity
- ✅ DELETE - Remove entity
- ✅ Custom Actions: <list actions>

## Fields

| Field Name | Type | Editable | Required | Description |
|------------|------|----------|----------|-------------|
| id | GUID | No | Auto | System identifier (SystemId) |
| number | String(20) | Yes | No | Document number (auto-generated if blank) |
| customerNumber | String(20) | Yes | Yes | Customer account number |
| customerName | String(100) | No | No | Customer name (read-only) |
| orderDate | Date | Yes | Yes | Order date |
| status | Enum | Yes | No | Order status (Open, Released, etc.) |
| totalAmount | Decimal | No | No | Total amount including VAT (calculated) |
| lastModifiedDateTime | DateTime | No | No | Last modification timestamp |

## Navigation Properties

| Property | Target Entity | Relationship | Description |
|----------|---------------|--------------|-------------|
| salesOrderLines | salesOrderLine | 1:many | Order line items |
| shipmentDetails | shipmentDetail | 1:1 | Shipment information |

## Custom Actions

### Post
- **Type**: Bound action
- **HTTP**: POST `/salesOrders({id})/Microsoft.NAV.post`
- **Description**: Posts the sales order and creates invoice
- **Preconditions**: Status must be Released
- **Returns**: Posted invoice number

## Request/Response Examples

### Create Sales Order (POST)
**Request:**
\```json
POST /api/v2.0/companies({companyId})/salesOrders
Content-Type: application/json

{
  "customerNumber": "C00001",
  "orderDate": "2024-01-15",
  "status": "Open"
}
\```

**Response:**
\```json
HTTP/1.1 201 Created
Content-Type: application/json

{
  "@odata.context": "...",
  "@odata.etag": "W/\"...\"",
  "id": "5d115c9c-4e9c-4f54-b4a0-08d7f9e0a4e3",
  "number": "SO-00001",
  "customerNumber": "C00001",
  "customerName": "Contoso Ltd.",
  "orderDate": "2024-01-15",
  "status": "Open",
  "totalAmount": 0,
  "lastModifiedDateTime": "2024-01-15T10:30:00Z"
}
\```

### Update Sales Order (PATCH)
### Retrieve with Filter
### Delete Sales Order
### Execute Custom Action

## OData Query Support
- ✅ $select - Field projection
- ✅ $filter - Server-side filtering
- ✅ $expand - Navigation property expansion
- ✅ $orderby - Sorting
- ✅ $top / $skip - Pagination
- ✅ $count - Count records
- ✅ Delta queries - Change tracking

## Error Responses

| Status Code | Scenario | Example |
|-------------|----------|---------|
| 400 | Bad Request | Invalid field value, missing required field |
| 404 | Not Found | Entity with specified ID does not exist |
| 409 | Conflict | Attempting to modify released order |
| 422 | Unprocessable Entity | Business validation failed |
| 500 | Internal Server Error | Unexpected server error |

**Example Error Response:**
\```json
{
  "error": {
    "code": "ValidationError",
    "message": "Customer Number is required"
  }
}
\```

## Performance Considerations
- Use $select to request only needed fields
- Apply $filter server-side rather than client-side filtering
- Use $top/$skip for pagination (don't retrieve all records)
- Use delta links for synchronization scenarios
- Index keys exist for: customerNumber, orderDate, status

## Security & Authorization
- OAuth 2.0 or Basic Authentication required
- Minimum permissions: Read/Write access to Sales Orders
- Field-level security applied based on user permissions
- Sensitive data (pricing, discounts) restricted by user role

## Versioning Strategy
- Current version: v2.0
- Deprecation policy: 12-month notice before version removal
- Breaking changes require new version
- Non-breaking changes allowed in current version

## Testing Scenarios
1. Create order with minimal fields
2. Create order with all optional fields
3. Update order fields
4. Attempt to modify released order (should fail)
5. Delete order without dependencies
6. Attempt to delete order with invoices (should fail)
7. Filter orders by customer and date range
8. Retrieve order with expanded lines
9. Execute custom action (Post)
10. Change tracking with delta links

## Change Log
- **v2.0** (2024-01-15): Initial release
  - Full CRUD operations
  - Navigation to lines
  - Post action
  - OData query support

## Contact & Support
- **Team**: Integration Team
- **Email**: integration@company.com
- **Documentation**: https://docs.company.com/api/sales-orders
```

## Success Criteria Checklist

Before considering the API page complete, verify:

- ✅ **Object ID Reserved**: ID obtained from reservation tool
- ✅ **Compiles Without Errors**: No build errors or warnings
- ✅ **Naming Conventions**: Follows camelCase for fields, PascalCase for objects
- ✅ **CRUD Operations**: All required operations work correctly
- ✅ **Validation**: Business rules enforced in triggers
- ✅ **Error Messages**: Clear, actionable error messages
- ✅ **Performance**: Proper keys, field loading optimized
- ✅ **OData Queries**: $filter, $select, $expand work as expected
- ✅ **Custom Actions**: Work correctly with proper validation
- ✅ **Documentation**: API design document created
- ✅ **Testing**: All test scenarios passed
- ✅ **Security**: Authorization considered and implemented
- ✅ **SystemId**: Used as ODataKeyFields for v2.0 APIs
- ✅ **DelayedInsert**: Set to true
- ✅ **AboutText**: Clear business scenario description provided (REQUIRED)
- ✅ **Timestamps**: lastModifiedDateTime included for sync scenarios

## Common Pitfalls to Avoid

- ❌ **Forgetting Object ID Reservation**: ALWAYS use the ID tool first
- ❌ **Exposing All Fields**: Only expose necessary fields (performance issue)
- ❌ **Missing ODataKeyFields**: Must be set to SystemId for v2.0
- ❌ **Missing AboutText**: REQUIRED property for MCP context and discoverability
- ❌ **No Error Handling**: Always validate in triggers
- ❌ **Missing DelayedInsert**: Can cause issues with auto-generated fields
- ❌ **Hardcoding Values**: Use proper field references and relations
- ❌ **Ignoring Performance**: Test with realistic data volumes
- ❌ **No OData Testing**: Always test $filter, $select, $expand
- ❌ **Skipping Documentation**: API contract must be documented
- ❌ **Wrong Field Names**: Use camelCase for API fields
- ❌ **No Validation**: Business rules must be enforced
- ❌ **Missing Timestamps**: Include for synchronization scenarios
- ❌ **Complex Navigation**: Too many nested levels impact performance
- ❌ **No Version Strategy**: Plan for future API evolution

## Complete Example: Sales Order API

```al
page 50100 "BCS Sales Orders API"
{
  APIVersion = 'v2.0';
  APIPublisher = 'businesscentral';
  APIGroup = 'sales';
  EntityName = 'salesOrder';
  EntitySetName = 'salesOrders';
  AboutText = 'Provides access to sales orders for integration with e-commerce platforms, mobile applications, and third-party sales management tools. Supports full CRUD operations and custom posting actions.';
  
  PageType = API;
  Caption = 'Sales Orders API';
  SourceTable = "Sales Header";
  SourceTableView = where("Document Type" = const(Order));
  DelayedInsert = true;
  ODataKeyFields = SystemId;
  
  layout
  {
    area(Content)
    {
      repeater(Group)
      {
        field(id; Rec.SystemId)
        {
          Caption = 'Id';
          Editable = false;
        }
        
        field(number; Rec."No.")
        {
          Caption = 'Number';
          Editable = false;
        }
        
        field(externalDocumentNumber; Rec."External Document No.")
        {
          Caption = 'External Document Number';
        }
        
        field(orderDate; Rec."Order Date")
        {
          Caption = 'Order Date';
        }
        
        field(customerNumber; Rec."Sell-to Customer No.")
        {
          Caption = 'Customer Number';
        }
        
        field(customerName; Rec."Sell-to Customer Name")
        {
          Caption = 'Customer Name';
          Editable = false;
        }
        
        field(billToCustomerNumber; Rec."Bill-to Customer No.")
        {
          Caption = 'Bill-to Customer Number';
        }
        
        field(currencyCode; Rec."Currency Code")
        {
          Caption = 'Currency Code';
        }
        
        field(paymentTermsCode; Rec."Payment Terms Code")
        {
          Caption = 'Payment Terms Code';
        }
        
        field(shipmentDate; Rec."Shipment Date")
        {
          Caption = 'Shipment Date';
        }
        
        field(status; Rec.Status)
        {
          Caption = 'Status';
        }
        
        field(totalAmount; Rec."Amount Including VAT")
        {
          Caption = 'Total Amount';
          Editable = false;
          AutoFormatType = 1;
          AutoFormatExpression = Rec."Currency Code";
        }
        
        field(discountAmount; Rec."Invoice Discount Amount")
        {
          Caption = 'Discount Amount';
          AutoFormatType = 1;
          AutoFormatExpression = Rec."Currency Code";
        }
        
        field(lastModifiedDateTime; Rec.SystemModifiedAt)
        {
          Caption = 'Last Modified Date Time';
          Editable = false;
        }
      }
    }
  }
  
  trigger OnInsertRecord(BelowxRec: Boolean): Boolean
  begin
    // Set document type
    Rec."Document Type" := Rec."Document Type"::Order;
    
    // Validate required fields
    if Rec."Sell-to Customer No." = '' then
      Error('Customer Number is required');
    
    // Set defaults
    if Rec."Order Date" = 0D then
      Rec."Order Date" := WorkDate();
    
    // Business validation
    ValidateCustomer(Rec."Sell-to Customer No.");
    
    exit(true);
  end;
  
  trigger OnModifyRecord(): Boolean
  begin
    // Prevent modification of released orders
    if Rec.Status = Rec.Status::Released then
      Error('Cannot modify released sales order. Change status to Open first.');
    
    // Validate date logic
    if Rec."Shipment Date" < Rec."Order Date" then
      Error('Shipment date cannot be before order date');
    
    exit(true);
  end;
  
  trigger OnDeleteRecord(): Boolean
  var
    SalesInvoiceHeader: Record "Sales Invoice Header";
  begin
    // Check for posted invoices
    SalesInvoiceHeader.SetRange("Order No.", Rec."No.");
    if not SalesInvoiceHeader.IsEmpty() then
      Error('Cannot delete sales order with posted invoices');
    
    // Prevent deletion of released orders
    if Rec.Status = Rec.Status::Released then
      Error('Cannot delete released sales order');
    
    exit(true);
  end;
  
  trigger OnAfterGetRecord()
  begin
    // Optimize field loading
    Rec.SetLoadFields("No.", "Sell-to Customer No.", "Order Date", "Amount Including VAT", Status);
    
    // Calculate totals
    Rec.CalcFields("Amount Including VAT");
  end;
  
  actions
  {
    area(Processing)
    {
      action(Post)
      {
        ApplicationArea = All;
        Caption = 'Post';
        
        trigger OnAction()
        var
          SalesPost: Codeunit "Sales-Post";
        begin
          if Rec.Status <> Rec.Status::Released then
            Error('Sales order must be released before posting');
          
          SalesPost.Run(Rec);
        end;
      }
      
      action(Release)
      {
        ApplicationArea = All;
        Caption = 'Release';
        
        trigger OnAction()
        var
          ReleaseSalesDoc: Codeunit "Release Sales Document";
        begin
          ReleaseSalesDoc.PerformManualRelease(Rec);
        end;
      }
      
      action(Reopen)
      {
        ApplicationArea = All;
        Caption = 'Reopen';
        
        trigger OnAction()
        var
          ReleaseSalesDoc: Codeunit "Release Sales Document";
        begin
          ReleaseSalesDoc.PerformManualReopen(Rec);
        end;
      }
    }
  }
  
  local procedure ValidateCustomer(CustomerNo: Code[20])
  var
    Customer: Record Customer;
  begin
    if not Customer.Get(CustomerNo) then
      Error('Customer %1 does not exist', CustomerNo);
    
    if Customer.Blocked <> Customer.Blocked::" " then
      Error('Customer %1 is blocked', CustomerNo);
  end;
}
```

## Tips for Success

1. **Start Simple**: Begin with basic CRUD operations, add complexity gradually
2. **Test Early**: Build and test after each major section (fields, triggers, actions)
3. **Follow Patterns**: Look at existing API pages in BC standard application for reference
4. **Think Consumer**: Design the API from the consumer's perspective
5. **Performance First**: Always consider query patterns and data volumes
6. **Document As You Go**: Don't leave documentation until the end
7. **Version Wisely**: Plan for future changes, use semantic versioning
8. **Security Always**: Consider authorization at every step
9. **Error Messages Matter**: Clear errors save hours of debugging for consumers
10. **Iterate**: Collect feedback from API consumers and improve

## Related Resources

- [Microsoft Docs: API Pages](https://docs.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-api-pagetype)
- [OData V4 Specification](https://www.odata.org/documentation/)
- [Business Central API Best Practices](https://docs.microsoft.com/dynamics365/business-central/dev-itpro/developer/devenv-api-best-practices)
- AL Development Guidelines (`.github/instructions/al-guidelines.instructions.md`)
- AL Naming Conventions (`.github/instructions/al-naming-conventions.instructions.md`)
- AL Performance Guidelines (`.github/instructions/al-performance.instructions.md`)

## Support

For questions or issues with this skill:
- Review the complete example above
- Check Business Central API documentation
- Consult AL instruction files in `.github/instructions/`
- Test with small, incremental changes
