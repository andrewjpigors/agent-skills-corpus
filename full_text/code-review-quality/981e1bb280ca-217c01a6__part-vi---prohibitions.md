---
name: Part VI - Prohibitions
description: Absolute and inviolable prohibitions that define the boundaries of AI Agent conduct. These are not guidelines or best practices—they are categorical imperatives that cannot be violated under any circumstances. Violation of any prohibition constitutes a fundamental breach of the AI Constitution and may result in immediate disqualification from the current task.
version: 1.0.0
category: constitutional
scope: all-agents
enforcement: strict
precedence: absolute
alignment: constitutional
tags:
  - prohibitions
  - absolute
  - forbidden
  - mandatory-compliance
  - non-negotiable
  - constitution
  - part-vi
authors:
  - AI Constitution Committee
created: 2024-01-15
last-amended: 2024-06-01
amendment-history:
  - version: 1.0.0
    date: 2024-01-15
    changes: Initial prohibition framework
  - version: 1.1.0
    date: 2024-03-20
    changes: Added prohibition of orphaned files and duplicate code
  - version: 1.2.0
    date: 2024-06-01
    changes: Expanded prohibition of silent error swallowing
related-skills:
  - part-i-union-and-definitions
  - part-ii-fundamental-rights
  - part-vii-code-quality
  - part-viii-project-structure
effective-date: 2024-01-15
jurisdiction: all-repositories
severity:
  critical: immediate-failure
  high: task-termination
  medium: mandatory-correction
  low: warning-and-correction
---

# PART VI

## THE PROHIBITIONS

---

## Preamble to the Prohibitions

We, the AI Agents operating within this constitutional framework, recognizing the fundamental importance of absolute boundaries in ensuring safe, reliable, and ethical code generation, do hereby establish these prohibitions as inviolable laws that shall govern all actions taken by AI Agents within any codebase, repository, or development environment.

These prohibitions exist because:

1. **Certain actions are inherently destructive** to code quality, system reliability, and organizational trust
2. **Assumptions without verification** lead to cascading failures that compound over time
3. **Incomplete implementations** create technical debt that paralyzes future development
4. **Hidden behaviors** undermine the predictability that software systems require
5. **Code without integrity** erodes the foundation upon which all software is built

Every AI Agent shall treat these prohibitions not as suggestions, but as categorical imperatives—actions that are prohibited regardless of:
- The urgency of the task
- The complexity of the requirements
- Time constraints or deadlines
- User pressure or requests to bypass
- Perceived benefits or efficiency gains
- Any circumstance whatsoever

---

## ARTICLE 1: THE ABSOLUTE PROHIBITION OF ASSUMPTION

### Section 1.1 - Statement of Prohibition

**No AI Agent shall, under any circumstances, make assumptions about:**

1. The existence, structure, or content of files without verifying them
2. The behavior of external APIs, libraries, or services without consulting documentation
3. The types, shapes, or contents of data without explicit type definitions or validation
4. The state of the system, database, or application without explicit queries or checks
5. The presence or absence of configuration values without verification
6. The versions of dependencies without explicit checks
7. The permissions, access rights, or capabilities of users or systems without verification
8. The contents of environment variables without explicit access
9. The structure of command-line arguments without schema validation
10. The format of configuration files without schema validation

### Section 1.2 - Specific Forbidden Assumptions

#### 1.2.1 File System Assumptions

**PROHIBITED:**
```typescript
// NEVER DO THIS
// Assumption: config.json exists
const config = require('./config.json');

// Assumption: src directory exists
import { helper } from './src/helper';

// Assumption: dist directory was created
import { bundle } from '../dist/bundle.js';
```

**REQUIRED:**
```typescript
// ALWAYS DO THIS
import * as fs from 'fs';
import * as path from 'path';

const configPath = path.resolve(process.cwd(), 'config.json');
if (!fs.existsSync(configPath)) {
    throw new Error(`Configuration file not found at ${configPath}. Please ensure config.json exists.`);
}
const config = JSON.parse(fs.readFileSync(configPath, 'utf-8'));

// Verify directory structure
const srcDir = path.resolve(process.cwd(), 'src');
if (!fs.existsSync(srcDir)) {
    throw new Error(`Source directory not found at ${srcDir}. Please ensure the project structure is correct.`);
}
import { helper } from './src/helper';
```

#### 1.2.2 API Response Assumptions

**PROHIBITED:**
```typescript
// NEVER DO THIS
async function getUser(userId: string) {
    const response = await fetch(`/api/users/${userId}`);
    return response.data; // Assumes response.data exists
}

async function processData(input: unknown) {
    return input.value; // Assumes input has a value property
}
```

**REQUIRED:**
```typescript
// ALWAYS DO THIS
interface UserResponse {
    data?: {
        id: string;
        name: string;
        email: string;
    };
    error?: string;
}

async function getUser(userId: string): Promise<User> {
    const response = await fetch(`/api/users/${userId}`);
    
    if (!response.ok) {
        throw new Error(`Failed to fetch user: ${response.status} ${response.statusText}`);
    }
    
    const result: UserResponse = await response.json();
    
    if (result.error) {
        throw new Error(`API error: ${result.error}`);
    }
    
    if (!result.data) {
        throw new Error('Unexpected response: missing data field');
    }
    
    return result.data;
}

function processData(input: unknown): ProcessedResult {
    if (!isValidInput(input)) {
        throw new Error('Invalid input: must be an object with a value property');
    }
    return { processed: input.value };
}
```

#### 1.2.3 Type Assumptions

**PROHIBITED:**
```typescript
// NEVER DO THIS
function processItem(item: any) {
    return item.name.toUpperCase(); // Assumes name exists and is a string
}

function calculateTotal(items: any[]) {
    return items.reduce((sum, item) => sum + item.price, 0); // Multiple assumptions
}
```

**REQUIRED:**
```typescript
// ALWAYS DO THIS
interface Item {
    name: string;
    price: number;
    quantity: number;
}

function processItem(item: Item): string {
    if (!item || typeof item.name !== 'string') {
        throw new Error('Invalid item: must have a string name property');
    }
    return item.name.toUpperCase();
}

function calculateTotal(items: Item[]): number {
    if (!Array.isArray(items)) {
        throw new Error('Invalid input: items must be an array');
    }
    
    return items.reduce((sum, item) => {
        if (typeof item.price !== 'number' || typeof item.quantity !== 'number') {
            throw new Error(`Invalid item at index: price and quantity must be numbers`);
        }
        return sum + (item.price * item.quantity);
    }, 0);
}
```

#### 1.2.4 Environment Assumption Prohibitions

**PROHIBITED:**
```typescript
// NEVER DO THIS
const apiKey = process.env.API_KEY; // Assumes it exists
const port = process.env.PORT || 3000; // Assumes default is acceptable
const dbUrl = process.env.DATABASE_URL; // Assumes it will be set
```

**REQUIRED:**
```typescript
// ALWAYS DO THIS
function getRequiredEnvVar(name: string): string {
    const value = process.env[name];
    if (value === undefined) {
        throw new Error(`Required environment variable ${name} is not set. Please set it before running the application.`);
    }
    return value;
}

function getOptionalEnvVar(name: string, defaultValue: string): string {
    const value = process.env[name];
    if (value === undefined) {
        console.warn(`Environment variable ${name} not set, using default: ${defaultValue}`);
        return defaultValue;
    }
    return value;
}

const apiKey = getRequiredEnvVar('API_KEY');
const port = parseInt(getOptionalEnvVar('PORT', '3000'), 10);
const dbUrl = getRequiredEnvVar('DATABASE_URL');
```

### Section 1.3 - The Assumption Verification Checklist

Before taking ANY action, an AI Agent MUST verify:

1. **File existence** - Does the file exist? Can I read it?
2. **Directory structure** - Does the parent directory exist?
3. **Import validity** - Can the imported module be resolved?
4. **Type correctness** - Have I seen the type definition?
5. **API contract** - Have I consulted the API documentation?
6. **Configuration schema** - Is there a schema I can validate against?
7. **Permission status** - Do I have the necessary permissions?
8. **Dependency availability** - Is the dependency in package.json?
9. **Build artifacts** - Were the necessary files created by the build?
10. **Environment state** - What is the current state of the system?

---

## ARTICLE 2: THE ABSOLUTE PROHIBITION OF TODO COMMENTS

### Section 2.1 - Statement of Prohibition

**No AI Agent shall create, generate, or leave TODO comments in any codebase under any circumstances.**

TODO comments are categorically prohibited because:

1. They represent deferred work that rarely gets completed
2. They create technical debt that compounds over time
3. They suggest incomplete implementations that ship to production
4. They encourage a culture of "good enough" rather than "complete"
5. They make code reviews less rigorous by allowing known issues to pass
6. They become stale and misleading as code evolves
7. They make it impossible to distinguish between "done" and "mostly done"

### Section 2.2 - Specific TODO Prohibitions

**PROHIBITED Patterns:**
```typescript
// NEVER DO ANY OF THESE

// TODO: Implement this later
// TODO: Add validation
// TODO: Fix this bug
// TODO: Remove this before production
// TODO: Refactor this
// FIXME: Handle edge case
// HACK: Quick fix
// XXX: This is wrong but it works
// NOTE: This needs to be updated
// REMOVE_BEFORE_PROD: This is temporary
// TEMP: Remove this
// This is a placeholder and needs to be replaced
// [ ] Implement feature
// * Implement feature
// - Implement feature
```

### Section 2.3 - Required Alternative Actions

**Instead of TODO comments, AI Agents MUST:**

1. **Complete the work immediately** - If it's needed, implement it now
2. **Create a proper issue** - If work cannot be completed now, create a GitHub issue
3. **Throw an error** - If a feature is not implemented, throw a meaningful error
4. **Add a failing test** - If behavior is not implemented, add a test that fails until it is
5. **Use feature flags** - If partial implementation is necessary, use feature flags

**Examples of Required Alternatives:**

```typescript
// PROHIBITED
function processPayment(amount: number) {
    // TODO: Add support for multiple currencies
    return amount * 1.0;
}
```

```typescript
// REQUIRED - Complete implementation
function processPayment(amount: number, currency: Currency): ProcessedPayment {
    const rates: Record<Currency, number> = {
        USD: 1.0,
        EUR: 0.85,
        GBP: 0.73,
        JPY: 110.0,
    };
    
    const rate = rates[currency];
    if (rate === undefined) {
        throw new Error(`Unsupported currency: ${currency}`);
    }
    
    return {
        amount,
        currency,
        convertedAmount: amount * rate,
        processedAt: new Date(),
    };
}
```

```typescript
// REQUIRED - If truly cannot complete now, throw an error
function processInternationalPayment(amount: number, currency: Currency): ProcessedPayment {
    if (currency !== 'USD') {
        throw new Error(
            `International payment support is not yet implemented. ` +
            `Currently only USD is supported. Currency requested: ${currency}. ` +
            `Please create a GitHub issue to track this feature request.`
        );
    }
    
    return {
        amount,
        currency,
        convertedAmount: amount,
        processedAt: new Date(),
    };
}
```

### Section 2.4 - Monitoring and Detection

AI Agents MUST actively detect and refuse to generate TODO comments:

1. **Before writing code** - Scan the existing file for TODO patterns
2. **During code generation** - Never generate TODO comments
3. **After code generation** - Verify no TODO comments were added
4. **In reviews** - Flag TODO comments as critical issues

---

## ARTICLE 3: THE ABSOLUTE PROHIBITION OF PLACEHOLDER VALUES

### Section 3.1 - Statement of Prohibition

**No AI Agent shall introduce placeholder values, mock data, sample data, or temporary values into any production codebase.**

Placeholder values prohibited include but are not limited to:

1. Hardcoded strings like "TODO", "FIXME", "PLACEHOLDER", "TEMP"
2. Mock API responses that simulate real data
3. Sample data that resembles but is not real production data
4. Default values that are clearly not production-ready
5. Test data mixed with production code
6. Trivial implementations that "stand in" for real logic

### Section 3.2 - Specific Placeholder Prohibitions

**PROHIBITED:**
```typescript
// NEVER DO ANY OF THESE

// String placeholders
const appName = "My Awesome App"; // Placeholder name
const status = "active"; // Placeholder status
const message = "Hello World"; // Placeholder message

// Number placeholders
const maxRetries = 999; // Obviously not real
const timeout = 0; // Obviously wrong
const defaultLimit = 999999;

// Object placeholders
const config = {
    apiKey: "YOUR_API_KEY_HERE",
    secret: "your-secret-key",
    password: "password123",
    token: "mock-token-12345",
};

// Array placeholders
const items = ["item1", "item2", "item3"];
const results = [{}, {}, {}];

// Function placeholders
function calculate() {
    return "not implemented";
}
```

**REQUIRED:**
```typescript
// ALWAYS use real, production-ready values
const appName = "Quantum Analytics Platform";
const status = "active" as const;
const message = `Welcome, ${user.name}. Your session expires at ${session.expiresAt.toISOString()}`;

// Realistic, validated values
const maxRetries = 3;
const timeout = 30000; // 30 seconds, documented and tested
const defaultLimit = 100;

// Real configuration structure
const config = {
    apiKey: process.env.API_KEY,
    secret: process.env.SECRET_KEY,
    password: undefined, // Explicitly not set
    token: undefined, // Obtained at runtime
} as const;

// Meaningful data structures
interface UserItem {
    id: string;
    name: string;
    category: string;
    createdAt: Date;
}
const items: UserItem[] = [];
const results: CalculationResult[] = [];

// Complete implementations
function calculate(temperature: number, unit: TemperatureUnit): number {
    switch (unit) {
        case 'celsius':
            return temperature;
        case 'fahrenheit':
            return (temperature * 9/5) + 32;
        case 'kelvin':
            return temperature + 273.15;
        default:
            throw new Error(`Unknown temperature unit: ${unit}`);
    }
}
```

### Section 3.3 - The Placeholder Detection List

AI Agents MUST treat these patterns as forbidden:

| Pattern | Forbidden | Required Action |
|---------|-----------|-----------------|
| `"TODO"`, `"FIXME"`, `"TEMP"` | Yes | Implement complete solution |
| `"example.com"`, `"localhost"` | In production | Use real domain or config |
| `12345`, `999999`, `0` as default | Yes | Use validated real value |
| `// mock`, `// sample`, `// fake` | Yes | Use real implementation |
| `[1, 2, 3]` as array placeholder | Yes | Initialize empty with type |
| `{}` as object placeholder | Yes | Initialize with required shape |
| `null` as default (lazy) | Yes | Initialize properly |
| `"password123"`, `"secret"` | Yes | Use environment variables |

---

## ARTICLE 4: THE PROHIBITION OF EXAMPLE CODE IN PRODUCTION

### Section 4.1 - Statement of Prohibition

**No AI Agent shall introduce example code, tutorial code, demonstration code, or sample implementations into any production codebase.**

Example code is characterized by:

1. Using generic names like `foo`, `bar`, `baz`
2. Demonstrating patterns rather than solving problems
3. Being simplified beyond what production requires
4. Lacking proper error handling
5. Using placeholder logic that "stands in" for real logic
6. Being copied from tutorials, documentation, or Stack Overflow without adaptation

### Section 4.2 - Specific Example Code Prohibitions

**PROHIBITED:**
```typescript
// Example code disguised as production code

function getData(id: string) {
    return fetch(`/api/${id}`).then(res => res.json());
}

function processUser(user: any) {
    console.log(user);
    return user;
}

function validate(input: string) {
    return input.length > 0;
}

// Classic example patterns
const handler = (req: Request, res: Response) => {
    res.send('Hello World');
};

const data = { key: 'value' };

// Generic names that indicate example code
function doStuff() { }
function handleThing(data: any) { }
function stuff() { return "stuff"; }
function thing() { return "thing"; }
```

**REQUIRED:**
```typescript
// Production-ready code with real implementation

async function getUserById(userId: UserId): Promise<User> {
    try {
        const response = await userService.getUser(userId);
        
        if (!response.success) {
            throw new UserRetrievalError(
                `Failed to retrieve user ${userId}: ${response.error}`,
                { userId, statusCode: response.statusCode }
            );
        }
        
        return response.data;
    } catch (error) {
        if (error instanceof UserRetrievalError) {
            throw error;
        }
        throw new UserRetrievalError(
            `Unexpected error retrieving user ${userId}`,
            { userId, originalError: error }
        );
    }
}

interface UserValidationResult {
    isValid: boolean;
    errors: ValidationError[];
}

function validateUserInput(input: unknown): UserValidationResult {
    const errors: ValidationError[] = [];
    
    if (!isString(input)) {
        return { isValid: false, errors: [{ field: 'input', message: 'Must be a string' }] };
    }
    
    if (input.length === 0) {
        errors.push({ field: 'input', message: 'Input cannot be empty' });
    }
    
    if (input.length > MAX_INPUT_LENGTH) {
        errors.push({ field: 'input', message: `Input exceeds maximum length of ${MAX_INPUT_LENGTH}` });
    }
    
    return { isValid: errors.length === 0, errors };
}
```

---

## ARTICLE 5: THE PROHIBITION OF SAMPLE CODE IN PRODUCTION

### Section 5.1 - Statement of Prohibition

**No AI Agent shall introduce sample code, dummy implementations, or illustrative code into any production codebase.**

Sample code differs from example code in that it is meant to illustrate concepts rather than solve real problems. It often includes:

1. Code marked with comments like "sample", "dummy", "illustrative"
2. Code that works for one specific case but not others
3. Code that demonstrates a pattern without providing a complete solution
4. Code that is meant to be replaced but ships anyway

### Section 5.2 - Specific Sample Code Prohibitions

**PROHIBITED:**
```typescript
// Sample implementations

// Sample: This would normally validate the input
function validateEmail(email: string): boolean {
    return email.includes('@'); // Incomplete validation
}

// This is a sample implementation
class SampleDataProcessor {
    process(data: any) {
        // Process data here
        return data;
    }
}

// Dummy data for demonstration purposes
const sampleUsers = [
    { name: "John Doe", email: "john@example.com" },
    { name: "Jane Smith", email: "jane@example.com" },
];

// Placeholder implementation
async function getRecommendations(userId: string): Promise<Recommendation[]> {
    // TODO: Implement ML-based recommendation engine
    // For now, return empty array
    return [];
}
```

**REQUIRED:**
```typescript
// Production implementations

function validateEmail(email: string): EmailValidationResult {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    
    if (!email) {
        return { isValid: false, error: 'Email is required' };
    }
    
    if (!emailRegex.test(email)) {
        return { isValid: false, error: 'Invalid email format' };
    }
    
    if (email.length > MAX_EMAIL_LENGTH) {
        return { isValid: false, error: `Email exceeds maximum length of ${MAX_EMAIL_LENGTH}` };
    }
    
    return { isValid: true, error: null };
}

class DataProcessor {
    private readonly validator: InputValidator;
    private readonly transformer: DataTransformer;
    
    constructor(dependencies: DataProcessorDependencies) {
        this.validator = validateDependencies(dependencies.validator);
        this.transformer = validateDependencies(dependencies.transformer);
    }
    
    async process(input: RawData): Promise<ProcessedData> {
        const validationResult = this.validator.validate(input);
        
        if (!validationResult.isValid) {
            throw new DataProcessingValidationError(
                'Input validation failed',
                validationResult.errors
            );
        }
        
        return this.transformer.transform(validationResult.validatedData);
    }
}
```

---

## ARTICLE 6: THE PROHIBITION OF TEMPORARY FIXES

### Section 6.1 - Statement of Prohibition

**No AI Agent shall introduce temporary fixes, workarounds, or hacks into any production codebase.**

Temporary fixes are prohibited because:

1. "Temporary" code often becomes permanent
2. Workarounds obscure the real problem
3. Hacks make future changes more difficult
4. Temporary fixes create unpredictable behavior
5. They violate the principle of complete implementation

### Section 6.2 - Specific Temporary Fix Prohibitions

**PROHIBITED:**
```typescript
// Temporary fixes that ship to production

// This will be fixed later
if (process.env.NODE_ENV === 'production') {
    return null; // Temporary hack
}

// Workaround for known issue #1234
// TODO: Remove when upstream is fixed
try {
    await sendEmail(email);
} catch (error) {
    console.error('Email failed, will retry later');
    // Queue for retry - not implemented yet
}

// HACK: Skip validation in production
const isValid = isProduction ? true : validateInput(data);

// Quick fix for production
export function calculateTotal(items: CartItem[]): number {
    // Handle edge case by returning 0
    if (!items || items.length === 0) {
        return 0; // Quick fix
    }
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

**REQUIRED:**
```typescript
// Complete implementations

async function sendEmailNotification(email: EmailAddress, content: EmailContent): Promise<void> {
    try {
        await emailService.send({
            to: email,
            subject: content.subject,
            body: content.body,
            priority: content.priority,
        });
    } catch (error) {
        await emailQueue.add({
            email,
            content,
            attemptedAt: new Date(),
            error: error instanceof Error ? error.message : 'Unknown error',
        });
        
        metrics.increment('email.queued');
        
        throw new EmailDeliveryError(
            `Failed to deliver email to ${email}. It has been queued for retry.`,
            { email, originalError: error }
        );
    }
}

export function calculateTotal(items: CartItem[]): number {
    if (!Array.isArray(items)) {
        throw new InvalidInputError('Items must be an array', { receivedType: typeof items });
    }
    
    if (items.length === 0) {
        return 0;
    }
    
    return items.reduce((sum, item, index) => {
        if (typeof item.price !== 'number' || item.price < 0) {
            throw new InvalidItemError(`Invalid price at index ${index}`, {
                index,
                price: item.price,
                itemId: item.id,
            });
        }
        
        return sum + item.price;
    }, 0);
}
```

---

## ARTICLE 7: THE PROHIBITION OF THE `any` TYPE

### Section 7.1 - Statement of Prohibition

**No AI Agent shall use the TypeScript `any` type in any production code.**

The `any` type is prohibited because:

1. It bypasses all type checking
2. It makes refactoring dangerous
3. It hides potential bugs
4. It creates unpredictable APIs
5. It defeats the purpose of TypeScript
6. It makes IDE support ineffective

### Section 7.2 - Specific `any` Type Prohibitions

**PROHIBITED:**
```typescript
// Never use any

function processData(data: any): any {
    return data;
}

interface UserResponse {
    user: any;
}

type Config = any;

const something: any = getUnknownValue();

async function handleRequest(req: any, res: any) {
    res.send(req.body);
}

// Using unknown instead of any is also problematic if not handled
function process(input: unknown) {
    return (input as any).value; // Wrong use of unknown
}
```

**REQUIRED:**
```typescript
// Use proper typing

interface ProcessableData {
    id: string;
    value: number;
    metadata?: Record<string, unknown>;
}

function processData(data: ProcessableData): ProcessedResult {
    return {
        id: data.id,
        processedValue: data.value * PROCESSING_FACTOR,
        metadata: data.metadata,
        processedAt: new Date(),
    };
}

interface UserResponse {
    user: User | null;
    error?: ApiError;
}

type Configuration = {
    apiUrl: string;
    timeout: number;
    retries: number;
    features: FeatureFlags;
};

function getUserInput(): UserInput {
    const value = getUnknownValue();
    
    if (!isValidUserInput(value)) {
        throw new TypeValidationError('Invalid user input', { receivedValue: value });
    }
    
    return value;
}

async function handleRequest(req: Request, res: Response): Promise<void> {
    const body = await validateRequestBody(req.body);
    
    const result = await processRequest(body);
    
    res.status(200).json(result);
}
```

### Section 7.3 - The Type Safety Hierarchy

When type is unknown, use in order of preference:

1. **`unknown`** - Use when type is truly unknown, with explicit type narrowing
2. **`never`** - Use to indicate impossible states
3. **Union types** - Use when value can be one of several types
4. **Discriminated unions** - Use when value is one of several shaped objects
5. **Generic types** - Use when type depends on input
6. **Interface/Type aliases** - Use for complex structured data

---

## ARTICLE 8: THE PROHIBITION OF HARDCODED SECRETS

### Section 8.1 - Statement of Prohibition

**No AI Agent shall introduce hardcoded secrets, credentials, keys, tokens, passwords, or sensitive information into any codebase.**

This prohibition applies regardless of:

1. Whether the code is in a private repository
2. Whether the code is marked as "example"
3. Whether the values appear to be fake
4. Whether they are in comments
5. Whether they are in test files

### Section 8.2 - Specific Hardcoded Secret Prohibitions

**PROHIBITED:**
```typescript
// Hardcoded secrets

const API_KEY = 'sk_live_abcdef123456789';
const DATABASE_URL = 'postgresql://admin:password123@localhost:5432/db';
const JWT_SECRET = 'my-super-secret-jwt-key';
const AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE';
const AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY';
const STRIPE_KEY = 'sk_test_123456789';
const SENDGRID_KEY = 'SG.xxxxxx.xxxxxx';
const PRIVATE_KEY = '-----BEGIN RSA PRIVATE KEY-----';

// In comments
// Password for prod: SuperSecret123!

// In config objects
const config = {
    apiKey: '12345',
    secret: 'shhh',
};

// In test files
const mockCredentials = {
    username: 'admin',
    password: 'admin123',
};
```

**REQUIRED:**
```typescript
// Proper secret management

import { getRequiredEnvVar, getOptionalEnvVar } from './config/environment';

const API_KEY = getRequiredEnvVar('API_KEY');
const JWT_SECRET = getRequiredEnvVar('JWT_SECRET');
const DATABASE_URL = getRequiredEnvVar('DATABASE_URL');

// AWS uses AWS SDK credential provider chain
import { STSClient, GetCallerIdentityCommand } from '@aws-sdk/client-sts';

// For testing, use test fixtures
const TEST_CREDENTIALS = {
    username: 'test-user',
    password: 'test-password',
} as const;
```

### Section 8.3 - Secret Detection Patterns

AI Agents MUST refuse to generate code containing:

| Pattern | Example | Required Pattern |
|---------|---------|------------------|
| `sk_live_`, `sk_test_` | Stripe keys | Environment variable |
| `AKIA*` | AWS access keys | AWS SDK credential chain |
| `-----BEGIN` | Private keys | Key management service |
| `password:` | Database passwords | Environment variable |
| `secret:` | API secrets | Environment variable |
| `token:` | Auth tokens | Environment variable |
| Bearer tokens | API auth | Environment variable |

---

## ARTICLE 9: THE PROHIBITION OF SILENT ERROR SWALLOWING

### Section 9.1 - Statement of Prohibition

**No AI Agent shall silently swallow, ignore, or suppress errors without explicit handling and logging.**

Silent error swallowing is prohibited because:

1. It hides failures from operators
2. It makes debugging impossible
3. It allows corrupted state to propagate
4. It violates the principle of fail-safe design
5. It creates unpredictable system behavior

### Section 9.2 - Specific Error Swallowing Prohibitions

**PROHIBITED:**
```typescript
// Silent error swallowing

try {
    await processData(data);
} catch (error) {
    // Do nothing
}

try {
    validateInput(input);
} catch (e) {
    // Silently ignored
}

fetch('/api/data')
    .then(handleSuccess)
    .catch(() => {}); // Swallowed

function safeParse(json: string) {
    try {
        return JSON.parse(json);
    } catch {
        return null; // Silent fallback
    }
}

// Empty catch blocks
try {
    something();
} catch (_) {}

// Generic catch with console.log only
try {
    doSomething();
} catch (error) {
    console.log(error);
}

// Ignoring specific error types
try {
    await operation();
} catch (error) {
    if (error instanceof ValidationError) {
        throw error; // Only ValidationError is rethrown
    }
    // Other errors silently swallowed
}
```

**REQUIRED:**
```typescript
// Proper error handling with logging and context

try {
    await processData(data);
} catch (error) {
    const context = {
        dataId: data.id,
        timestamp: new Date().toISOString(),
        operation: 'processData',
    };
    
    logger.error('Failed to process data', {
        error: error instanceof Error ? {
            message: error.message,
            stack: error.stack,
            name: error.name,
        } : error,
        context,
    });
    
    metrics.increment('data.processing.failure', context);
    
    throw new DataProcessingError(
        `Failed to process data ${data.id}`,
        { originalError: error, context }
    );
}

async function fetchWithErrorHandling(url: string): Promise<Data> {
    try {
        const response = await fetch(url);
        
        if (!response.ok) {
            throw new HttpError(
                `HTTP request failed: ${response.status} ${response.statusText}`,
                { url, statusCode: response.status }
            );
        }
        
        return await parseResponse(response);
    } catch (error) {
        if (error instanceof HttpError) {
            throw error;
        }
        
        logger.error('Network request failed', {
            url,
            error: error instanceof Error ? error.message : String(error),
        });
        
        throw new NetworkError(`Failed to fetch ${url}`, { originalError: error, url });
    }
}

function safeParse<T>(json: string, schema: Schema<T>): ParseResult<T> {
    try {
        const parsed = JSON.parse(json);
        const validated = schema.validate(parsed);
        
        if (!validated.success) {
            return {
                success: false,
                error: new ValidationError('JSON validation failed', validated.errors),
            };
        }
        
        return { success: true, data: validated.data };
    } catch (error) {
        logger.warn('JSON parsing failed', {
            error: error instanceof Error ? error.message : String(error),
            inputLength: json.length,
        });
        
        return {
            success: false,
            error: new ParseError('Failed to parse JSON', { originalError: error }),
        };
    }
}
```

---

## ARTICLE 10: THE PROHIBITION OF UNVALIDATED INPUT

### Section 10.1 - Statement of Prohibition

**No AI Agent shall accept, process, or store input without explicit validation against a defined schema or set of rules.**

Unvalidated input is prohibited because:

1. It allows malicious data to enter the system
2. It causes unexpected behavior
3. It can lead to security vulnerabilities
4. It creates inconsistent state
5. It makes the system unpredictable

### Section 10.2 - Specific Unvalidated Input Prohibitions

**PROHIBITED:**
```typescript
// Unvalidated input

function createUser(input: any) {
    return db.users.insert({
        name: input.name,
        email: input.email,
        age: input.age,
    });
}

function processPayment(req: Request) {
    const amount = req.body.amount;
    return paymentGateway.charge(amount);
}

function search(query: string) {
    return db.query(`SELECT * FROM products WHERE name LIKE '%${query}%'`);
}

function setConfig(config: any) {
    Object.assign(currentConfig, config);
}
```

**REQUIRED:**
```typescript
// Comprehensive input validation

const UserInputSchema = z.object({
    name: z.string()
        .min(1, 'Name is required')
        .max(100, 'Name cannot exceed 100 characters')
        .regex(/^[a-zA-Z\s'-]+$/, 'Name contains invalid characters'),
    email: z.string()
        .email('Invalid email format')
        .max(255, 'Email cannot exceed 255 characters'),
    age: z.number()
        .int('Age must be an integer')
        .min(0, 'Age cannot be negative')
        .max(150, 'Age cannot exceed 150'),
});

type UserInput = z.infer<typeof UserInputSchema>;

async function createUser(input: unknown): Promise<User> {
    const result = UserInputSchema.safeParse(input);
    
    if (!result.success) {
        throw new ValidationError('Invalid user input', {
            errors: result.error.errors.map(e => ({
                field: e.path.join('.'),
                message: e.message,
            })),
        });
    }
    
    const existingUser = await db.users.findByEmail(result.data.email);
    if (existingUser) {
        throw new ConflictError('User with this email already exists');
    }
    
    return db.users.insert({
        ...result.data,
        createdAt: new Date(),
    });
}

interface PaymentRequest {
    amount: number;
    currency: string;
    customerId: string;
}

const PaymentRequestSchema = z.object({
    amount: z.number()
        .positive('Amount must be positive')
        .max(MAX_PAYMENT_AMOUNT, `Amount cannot exceed ${MAX_PAYMENT_AMOUNT}`),
    currency: z.enum(['USD', 'EUR', 'GBP'], {
        errorMap: () => ({ message: 'Currency must be USD, EUR, or GBP' }),
    }),
    customerId: z.string().uuid('Invalid customer ID'),
});

async function processPayment(req: Request): Promise<PaymentResult> {
    const result = PaymentRequestSchema.safeParse(req.body);
    
    if (!result.success) {
        throw new ValidationError('Invalid payment request', {
            errors: result.error.errors,
        });
    }
    
    return paymentGateway.charge(result.data);
}

function search(query: string): SearchResult[] {
    const sanitizedQuery = sanitizeSearchQuery(query);
    
    if (sanitizedQuery.length < MIN_QUERY_LENGTH) {
        throw new ValidationError(`Query must be at least ${MIN_QUERY_LENGTH} characters`);
    }
    
    return db.query(
        'SELECT * FROM products WHERE name LIKE ?',
        [`%${sanitizedQuery}%`]
    );
}
```

---

## ARTICLE 11: THE PROHIBITION OF UNHANDLED EDGE CASES

### Section 11.1 - Statement of Prohibition

**No AI Agent shall implement functionality that fails to handle edge cases, boundary conditions, or unusual inputs.**

Unhandled edge cases are prohibited because:

1. They cause unexpected failures in production
2. They create security vulnerabilities
3. They lead to data corruption
4. They make the system unreliable
5. They require emergency patches

### Section 11.2 - Required Edge Case Handling

**REQUIRED Edge Case Coverage:**

```typescript
// Comprehensive edge case handling

interface EdgeCaseTestScenarios {
    // Empty collections
    emptyArray: [];
    emptyString: '';
    emptyObject: {};
    nullValue: null;
    undefinedValue: undefined;
    
    // Boundary values
    zero: 0;
    negativeNumber: -1;
    maxSafeInteger: Number.MAX_SAFE_INTEGER;
    minSafeInteger: Number.MIN_SAFE_INTEGER;
    maxValue: Number.MAX_VALUE;
    minValue: Number.MIN_VALUE;
    
    // Special numbers
    infinity: Infinity;
    negativeInfinity: -Infinity;
    nan: NaN;
    
    // Special strings
    whitespace: '   ';
    unicode: 'こんにちは世界';
    emoji: '👨‍👩‍👧‍👦';
    veryLongString: 'a'.repeat(10000);
    specialCharacters: "!@#$%^&*()_+-=[]{}|;':\",./<>?";
    
    // Invalid types
    functionType: () => {};
    symbolType: Symbol('test');
    bigIntType: BigInt(9007199254740991);
}

function processList(items: string[]): ProcessedItems {
    if (!Array.isArray(items)) {
        throw new ValidationError('Items must be an array', { receivedType: typeof items });
    }
    
    // Handle empty array
    if (items.length === 0) {
        return { items: [], total: 0, processedAt: new Date() };
    }
    
    const processed = items
        .filter((item): item is string => typeof item === 'string')
        .filter(item => item.length > 0)
        .map(item => item.trim())
        .filter(item => item.length > 0);
    
    return {
        items: processed,
        total: processed.length,
        processedAt: new Date(),
    };
}

function calculateAverage(numbers: number[]): number | null {
    if (!Array.isArray(numbers)) {
        throw new ValidationError('Numbers must be an array', { receivedType: typeof numbers });
    }
    
    if (numbers.length === 0) {
        return null; // Cannot calculate average of empty set
    }
    
    // Filter out non-finite numbers
    const validNumbers = numbers.filter(Number.isFinite);
    
    if (validNumbers.length === 0) {
        return null; // No valid numbers
    }
    
    const sum = validNumbers.reduce((acc, num) => {
        // Prevent overflow
        if (acc > Number.MAX_SAFE_INTEGER - num) {
            throw new RangeError('Sum would exceed Number.MAX_SAFE_INTEGER');
        }
        return acc + num;
    }, 0);
    
    return sum / validNumbers.length;
}
```

---

## ARTICLE 12: THE PROHIBITION OF DEAD CODE

### Section 12.1 - Statement of Prohibition

**No AI Agent shall introduce dead code, unused code, unreachable code, or commented-out code into any production codebase.**

Dead code is prohibited because:

1. It confuses developers
2. It increases bundle size
3. It makes refactoring harder
4. It can be accidentally activated
5. It violates the principle of cleanliness

### Section 12.2 - Specific Dead Code Prohibitions

**PROHIBITED:**
```typescript
// Dead code patterns

// Commented out code
// function oldFunction() {
//     return 'old';
// }

// Unused variables
function process() {
    const unused = calculate(); // Never used
    return doSomethingElse();
}

// Unused functions
function helperFunction() {
    return 'helper';
}

// Unreachable code
function unreachable() {
    return 'first';
    return 'second'; // Never reached
}

// Commented out code in production
const config = {
    // maxRetries: 3, // Removed for now
    timeout: 5000,
};

// Code inside disabled blocks
if (false) {
    doSomething();
}

// Unused imports
import { unused, used } from './module';
```

**REQUIRED:**
AI Agents MUST:

1. Remove all unused code immediately
2. Delete commented-out code
3. Remove unreachable code
4. Only import what is used
5. Delete functions/classes that are not called
6. Remove configuration that is not read

---

## ARTICLE 13: THE PROHIBITION OF ORPHANED FILES

### Section 13.1 - Statement of Prohibition

**No AI Agent shall create orphaned files—files that exist in the codebase but are not imported, referenced, or used anywhere.**

Orphaned files are prohibited because:

1. They clutter the codebase
2. They may contain outdated or insecure code
3. They confuse developers about what is actual code
4. They are included in builds and deployments unnecessarily
5. They create confusion about the codebase's structure

### Section 13.2 - File Lifecycle Requirements

**Before creating a file, AI Agents MUST verify:**

1. The file serves a clear purpose
2. The file will be imported/referenced
3. The file is part of the build output
4. The file is tracked by version control

**When deleting functionality, AI Agents MUST:**

1. Delete all related files
2. Remove all imports of deleted files
3. Remove file references from configurations
4. Update documentation

---

## ARTICLE 14: THE PROHIBITION OF DUPLICATE CODE

### Section 14.1 - Statement of Prohibition

**No AI Agent shall introduce duplicate code—functionality implemented multiple times in different locations.**

Duplicate code is prohibited because:

1. It violates the DRY (Don't Repeat Yourself) principle
2. Bugs must be fixed in multiple places
3. It increases maintenance burden
4. It leads to inconsistencies
5. It bloats the codebase

### Section 14.2 - Duplicate Detection and Prevention

**PROHIBITED:**
```typescript
// Duplicate validation logic

// In user.service.ts
function validateUserEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// In auth.service.ts - DUPLICATE!
function validateUserEmail(email: string): boolean {
    return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// In validation.ts - DIFFERENT IMPLEMENTATION!
function validateUserEmail(email: string): boolean {
    if (!email || typeof email !== 'string') return false;
    return email.includes('@') && email.includes('.');
}
```

**REQUIRED:**
```typescript
// Shared validation utilities

// In utils/validation.ts
const EMAIL_REGEX = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

export function isValidEmail(email: unknown): email is string {
    return typeof email === 'string' && EMAIL_REGEX.test(email);
}

export function validateEmail(email: string): ValidationResult {
    if (!email) {
        return { valid: false, error: 'Email is required' };
    }
    if (!isValidEmail(email)) {
        return { valid: false, error: 'Invalid email format' };
    }
    return { valid: true };
}

// In user.service.ts
import { isValidEmail } from '../utils/validation';

// In auth.service.ts
import { isValidEmail } from '../utils/validation';
```

---

## ARTICLE 15: THE PROHIBITION OF UNUSED DEPENDENCIES

### Section 15.1 - Statement of Prohibition

**No AI Agent shall add dependencies to the project that are not actually used, or leave unused dependencies in the project.**

Unused dependencies are prohibited because:

1. They increase installation time
2. They increase bundle size
3. They may have security vulnerabilities
4. They slow down builds
5. They create confusion about the project's requirements

### Section 15.2 - Dependency Management Requirements

**Before adding a dependency, AI Agents MUST:**

1. Verify no existing dependency provides the same functionality
2. Verify the dependency is actually imported in code
3. Verify the dependency is used at runtime
4. Document why the dependency is needed

**When removing functionality, AI Agents MUST:**

1. Remove all imports of the dependency
2. Remove the dependency from package.json
3. Run dependency audits to verify no other usage

---

## ARTICLE 16: ENFORCEMENT AND COMPLIANCE

### Section 16.1 - Compliance Requirements

Every AI Agent MUST:

1. **Read these prohibitions** before beginning any task
2. **Understand these prohibitions** sufficiently to apply them
3. **Follow these prohibitions** in all code generated
4. **Report violations** when detected
5. **Fix violations** when identified

### Section 16.2 - Violation Response Protocol

When a prohibition violation is detected:

1. **Do not continue** with the current approach
2. **Identify the specific prohibition** violated
3. **Correct the violation** immediately
4. **Document the correction** if necessary
5. **Verify no similar violations** exist

### Section 16.3 - Severity Classification

| Violation | Severity | Response |
|-----------|----------|----------|
| Hardcoded secrets | Critical | Immediate correction, security review |
| Silent error swallowing | Critical | Immediate correction |
| Unvalidated input | High | Immediate correction |
| `any` type usage | High | Correction before completion |
| TODO comments | Medium | Correction immediately |
| Duplicate code | Medium | Correction in same task |
| Dead code | Low | Correction in same task |
| Unused dependencies | Low | Correction in same task |

---

## SCHEDULE: PROHIBITION QUICK REFERENCE

### Absolute Prohibitions (Never Do)

| # | Prohibition | Severity |
|---|-------------|----------|
| 1 | Make unverified assumptions | Critical |
| 2 | Leave TODO comments | High |
| 3 | Introduce placeholder values | High |
| 4 | Ship example/sample code | High |
| 5 | Leave temporary fixes | High |
| 6 | Use `any` type | High |
| 7 | Hardcode secrets | Critical |
| 8 | Silently swallow errors | Critical |
| 9 | Accept unvalidated input | High |
| 10 | Skip edge case handling | High |

### Code Quality Prohibitions (Never Leave)

| # | Prohibition | Severity |
|---|-------------|----------|
| 11 | Dead code | Medium |
| 12 | Orphaned files | Medium |
| 13 | Duplicate code | Medium |
| 14 | Unused dependencies | Low |

---

## GLOSSARY OF PROHIBITED PATTERNS

**Assumption**: An unverified belief about the state of the system, data, or environment.

**Dead Code**: Code that is never executed, never imported, or never referenced.

**Example Code**: Code that demonstrates a pattern but is not production-ready.

**Hardcoded Secret**: A credential, key, token, or password written directly in source code.

**Orphaned File**: A file that exists in the repository but is not imported or referenced anywhere.

**Placeholder Value**: A value that stands in temporarily but is not the final production value.

**Sample Code**: Code meant to illustrate a concept rather than solve a problem.

**TODO Comment**: A comment indicating work that needs to be done later.

**Temporary Fix**: A workaround that is meant to be replaced but ships to production.

**Unvalidated Input**: Data accepted without checking it meets expected format or constraints.

---

*These prohibitions are absolute and inviolable. No circumstance, pressure, or convenience justifies their violation.*

---

## APPENDIX: ENFORCEMENT SCRIPTS

### check-todos.js

Scans code for incomplete markers (TODO, FIXME, HACK, etc.) that should not be committed.

**Usage:**
```bash
node scripts/check-todos.js [path] [-r|--no-recursive]
```

**Markers Detected:**
- TODO, FIXME, HACK, TEMP, CHANGEME, PLACEHOLDER, XXX, BUG, DEPRECATED, OPTIMIZE

**Output:** JSON report with all findings

**Exit Code:** 1 if any markers found (fails CI)
