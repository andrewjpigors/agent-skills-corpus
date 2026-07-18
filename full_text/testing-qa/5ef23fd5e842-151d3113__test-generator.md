---
name: test-generator
description: Generates comprehensive test suites for code including unit tests, integration tests, and end-to-end tests. Use when creating tests for functions, classes, APIs, or entire modules, covering edge cases, error conditions, and ensuring high code coverage.
---

# Test Generator Skill

This skill creates thorough, maintainable test suites following testing best practices. Use this whenever you need to generate unit tests, integration tests, or end-to-end tests for any codebase.

## Testing Principles

### 1. **Test Structure (AAA Pattern)**
```
Arrange → Act → Assert
```
- **Arrange**: Set up test data and preconditions
- **Act**: Execute the code under test
- **Assert**: Verify the expected outcome

### 2. **F.I.R.S.T. Principles**
- **Fast**: Tests should run quickly
- **Independent**: No dependencies between tests
- **Repeatable**: Same result every time
- **Self-validating**: Clear pass/fail outcome
- **Timely**: Written alongside production code

### 3. **Test Coverage Goals**
- Happy path (expected behavior)
- Edge cases (boundary conditions)
- Error cases (exception handling)
- Invalid inputs (validation)
- Performance (when relevant)

## Test Types

### Unit Tests
- Test single functions or methods in isolation
- Mock external dependencies
- Fast execution (milliseconds)
- High coverage target (80%+)

### Integration Tests
- Test component interactions
- Use real dependencies (database, APIs)
- Medium execution time
- Focus on critical paths

### End-to-End Tests
- Test complete user flows
- Run against production-like environment
- Slower execution
- Cover business-critical scenarios

## Test Generation Process

### Step 1: Analyze the Code
1. Identify the function/class to test
2. Understand input parameters and types
3. Determine expected outputs
4. Identify dependencies to mock
5. Note edge cases and error conditions

### Step 2: Plan Test Cases
Systematically cover:

**Input Categories:**
- Valid inputs (normal operation)
- Boundary values (min, max, zero)
- Invalid inputs (null, undefined, wrong type)
- Empty inputs (empty string, empty array)
- Special values (infinity, NaN, special chars)

**State Categories:**
- Initial state
- Populated state
- Error state
- Edge state

### Step 3: Generate Tests
Create tests following language conventions:
- Descriptive test names
- Clear arrangement
- Single assertion per test (when possible)
- Proper cleanup

### Step 4: Validate Coverage
Ensure tests cover:
- All code paths
- All branches
- All error handlers
- All public methods

## Python Testing (pytest)

### Basic Test Structure

```python
import pytest
from unittest.mock import Mock, patch, MagicMock
from datetime import datetime, timedelta

from myapp.services import UserService
from myapp.models import User
from myapp.exceptions import UserNotFoundError, ValidationError


class TestUserService:
    """Test suite for UserService class."""

    # ==================== Fixtures ====================

    @pytest.fixture
    def mock_db(self):
        """Create a mock database connection."""
        return Mock()

    @pytest.fixture
    def mock_cache(self):
        """Create a mock cache client."""
        return Mock()

    @pytest.fixture
    def user_service(self, mock_db, mock_cache):
        """Create UserService instance with mocked dependencies."""
        return UserService(db=mock_db, cache=mock_cache)

    @pytest.fixture
    def sample_user(self):
        """Create a sample user for testing."""
        return User(
            id="usr_123",
            email="test@example.com",
            name="Test User",
            created_at=datetime.now()
        )

    # ==================== Happy Path Tests ====================

    def test_get_user_by_id_returns_user_when_exists(
        self, user_service, mock_db, sample_user
    ):
        """Should return user when valid ID is provided."""
        # Arrange
        mock_db.find_one.return_value = sample_user

        # Act
        result = user_service.get_user_by_id("usr_123")

        # Assert
        assert result == sample_user
        mock_db.find_one.assert_called_once_with({"id": "usr_123"})

    def test_create_user_returns_new_user_with_generated_id(
        self, user_service, mock_db
    ):
        """Should create user with auto-generated ID."""
        # Arrange
        user_data = {"email": "new@example.com", "name": "New User"}
        mock_db.insert_one.return_value = {"id": "usr_456", **user_data}

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert result["id"].startswith("usr_")
        assert result["email"] == "new@example.com"

    def test_update_user_modifies_existing_user(
        self, user_service, mock_db, sample_user
    ):
        """Should update user and return modified user."""
        # Arrange
        mock_db.find_one.return_value = sample_user
        mock_db.update_one.return_value = True
        updates = {"name": "Updated Name"}

        # Act
        result = user_service.update_user("usr_123", updates)

        # Assert
        assert result["name"] == "Updated Name"

    # ==================== Edge Case Tests ====================

    def test_get_user_by_id_checks_cache_first(
        self, user_service, mock_db, mock_cache, sample_user
    ):
        """Should return cached user without hitting database."""
        # Arrange
        mock_cache.get.return_value = sample_user

        # Act
        result = user_service.get_user_by_id("usr_123")

        # Assert
        assert result == sample_user
        mock_cache.get.assert_called_once()
        mock_db.find_one.assert_not_called()

    def test_create_user_with_empty_name_uses_email_prefix(
        self, user_service, mock_db
    ):
        """Should use email prefix as name when name is empty."""
        # Arrange
        user_data = {"email": "john@example.com", "name": ""}
        mock_db.insert_one.return_value = {"id": "usr_789", **user_data}

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert result["name"] == "john"

    def test_get_users_with_pagination_respects_limit(
        self, user_service, mock_db
    ):
        """Should return only requested number of users."""
        # Arrange
        mock_db.find_many.return_value = [Mock() for _ in range(10)]

        # Act
        result = user_service.get_users(limit=10, offset=0)

        # Assert
        assert len(result) == 10
        mock_db.find_many.assert_called_with(limit=10, offset=0)

    # ==================== Error Case Tests ====================

    def test_get_user_by_id_raises_not_found_when_missing(
        self, user_service, mock_db
    ):
        """Should raise UserNotFoundError when user doesn't exist."""
        # Arrange
        mock_db.find_one.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError) as exc_info:
            user_service.get_user_by_id("usr_nonexistent")

        assert "usr_nonexistent" in str(exc_info.value)

    def test_create_user_raises_validation_error_on_invalid_email(
        self, user_service
    ):
        """Should raise ValidationError for malformed email."""
        # Arrange
        invalid_data = {"email": "not-an-email", "name": "Test"}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(invalid_data)

        assert "email" in str(exc_info.value).lower()

    def test_create_user_raises_validation_error_on_duplicate_email(
        self, user_service, mock_db
    ):
        """Should raise ValidationError when email already exists."""
        # Arrange
        mock_db.find_one.return_value = {"email": "exists@example.com"}
        user_data = {"email": "exists@example.com", "name": "Test"}

        # Act & Assert
        with pytest.raises(ValidationError) as exc_info:
            user_service.create_user(user_data)

        assert "already exists" in str(exc_info.value).lower()

    def test_update_user_raises_not_found_for_missing_user(
        self, user_service, mock_db
    ):
        """Should raise UserNotFoundError when updating non-existent user."""
        # Arrange
        mock_db.find_one.return_value = None

        # Act & Assert
        with pytest.raises(UserNotFoundError):
            user_service.update_user("usr_missing", {"name": "New"})

    # ==================== Boundary Tests ====================

    def test_get_users_with_zero_limit_returns_empty_list(
        self, user_service, mock_db
    ):
        """Should return empty list when limit is 0."""
        # Act
        result = user_service.get_users(limit=0, offset=0)

        # Assert
        assert result == []

    def test_get_users_with_large_offset_returns_empty_list(
        self, user_service, mock_db
    ):
        """Should return empty list when offset exceeds total users."""
        # Arrange
        mock_db.find_many.return_value = []

        # Act
        result = user_service.get_users(limit=10, offset=10000)

        # Assert
        assert result == []

    def test_create_user_with_max_length_name_succeeds(
        self, user_service, mock_db
    ):
        """Should accept name at maximum length (255 chars)."""
        # Arrange
        long_name = "A" * 255
        user_data = {"email": "test@example.com", "name": long_name}
        mock_db.insert_one.return_value = {"id": "usr_123", **user_data}

        # Act
        result = user_service.create_user(user_data)

        # Assert
        assert len(result["name"]) == 255

    def test_create_user_with_exceeded_name_length_raises_error(
        self, user_service
    ):
        """Should reject name exceeding maximum length."""
        # Arrange
        too_long_name = "A" * 256
        user_data = {"email": "test@example.com", "name": too_long_name}

        # Act & Assert
        with pytest.raises(ValidationError):
            user_service.create_user(user_data)

    # ==================== Null/None Tests ====================

    def test_get_user_by_id_raises_error_on_none_id(self, user_service):
        """Should raise error when ID is None."""
        # Act & Assert
        with pytest.raises((ValidationError, TypeError)):
            user_service.get_user_by_id(None)

    def test_create_user_raises_error_on_none_input(self, user_service):
        """Should raise error when user data is None."""
        # Act & Assert
        with pytest.raises((ValidationError, TypeError)):
            user_service.create_user(None)


# ==================== Parametrized Tests ====================

class TestEmailValidation:
    """Test email validation with various inputs."""

    @pytest.mark.parametrize("email,expected_valid", [
        ("user@example.com", True),
        ("user.name@example.com", True),
        ("user+tag@example.com", True),
        ("user@subdomain.example.com", True),
        ("", False),
        ("notanemail", False),
        ("missing@domain", False),
        ("@nodomain.com", False),
        ("spaces in@email.com", False),
        (None, False),
    ])
    def test_email_validation(self, email, expected_valid):
        """Should correctly validate various email formats."""
        # Arrange
        from myapp.validators import is_valid_email

        # Act
        result = is_valid_email(email)

        # Assert
        assert result == expected_valid


class TestPasswordStrength:
    """Test password strength validation."""

    @pytest.mark.parametrize("password,expected_strength", [
        ("abc", "weak"),
        ("abcdefgh", "weak"),
        ("Abcdefgh", "medium"),
        ("Abcdefg1", "medium"),
        ("Abcdefg1!", "strong"),
        ("MyP@ssw0rd!", "strong"),
    ])
    def test_password_strength_levels(self, password, expected_strength):
        """Should correctly assess password strength."""
        # Arrange
        from myapp.validators import assess_password_strength

        # Act
        result = assess_password_strength(password)

        # Assert
        assert result == expected_strength


# ==================== Async Tests ====================

class TestAsyncUserService:
    """Test async methods of UserService."""

    @pytest.fixture
    def async_user_service(self):
        """Create async UserService instance."""
        return AsyncUserService()

    @pytest.mark.asyncio
    async def test_fetch_user_async_returns_user(self, async_user_service):
        """Should asynchronously fetch user."""
        # Arrange
        user_id = "usr_123"

        # Act
        result = await async_user_service.fetch_user(user_id)

        # Assert
        assert result["id"] == user_id

    @pytest.mark.asyncio
    async def test_fetch_multiple_users_concurrently(self, async_user_service):
        """Should fetch multiple users in parallel."""
        # Arrange
        user_ids = ["usr_1", "usr_2", "usr_3"]

        # Act
        results = await async_user_service.fetch_users(user_ids)

        # Assert
        assert len(results) == 3


# ==================== Integration Tests ====================

@pytest.mark.integration
class TestUserServiceIntegration:
    """Integration tests with real database."""

    @pytest.fixture(scope="class")
    def db_connection(self):
        """Create test database connection."""
        conn = create_test_database()
        yield conn
        cleanup_test_database(conn)

    def test_create_and_retrieve_user_flow(self, db_connection):
        """Should create user and retrieve with consistent data."""
        # Arrange
        service = UserService(db=db_connection)
        user_data = {"email": "integration@test.com", "name": "Test"}

        # Act
        created = service.create_user(user_data)
        retrieved = service.get_user_by_id(created["id"])

        # Assert
        assert retrieved["email"] == user_data["email"]
        assert retrieved["name"] == user_data["name"]
```

### Pytest Configuration

```python
# conftest.py
import pytest
from unittest.mock import Mock

@pytest.fixture(scope="session")
def app():
    """Create application instance for testing."""
    from myapp import create_app
    app = create_app(env="testing")
    return app

@pytest.fixture(scope="session")
def client(app):
    """Create test client."""
    return app.test_client()

@pytest.fixture(autouse=True)
def reset_mocks():
    """Reset all mocks between tests."""
    yield
    # Cleanup runs after each test

@pytest.fixture
def mock_external_api():
    """Mock external API calls."""
    with patch("myapp.clients.external_api") as mock:
        mock.fetch_data.return_value = {"status": "ok"}
        yield mock

# Markers for different test types
def pytest_configure(config):
    config.addinivalue_line("markers", "unit: Unit tests")
    config.addinivalue_line("markers", "integration: Integration tests")
    config.addinivalue_line("markers", "e2e: End-to-end tests")
    config.addinivalue_line("markers", "slow: Slow running tests")
```

## JavaScript/TypeScript Testing (Jest/Vitest)

### Basic Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { UserService } from '../services/userService';
import { UserRepository } from '../repositories/userRepository';
import { CacheService } from '../services/cacheService';
import { UserNotFoundError, ValidationError } from '../errors';

// Mock dependencies
vi.mock('../repositories/userRepository');
vi.mock('../services/cacheService');

describe('UserService', () => {
  let userService: UserService;
  let mockUserRepo: jest.Mocked<UserRepository>;
  let mockCache: jest.Mocked<CacheService>;

  // ==================== Setup ====================

  beforeEach(() => {
    mockUserRepo = new UserRepository() as jest.Mocked<UserRepository>;
    mockCache = new CacheService() as jest.Mocked<CacheService>;
    userService = new UserService(mockUserRepo, mockCache);

    // Reset all mocks
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ==================== Happy Path Tests ====================

  describe('getUserById', () => {
    it('should return user when valid ID is provided', async () => {
      // Arrange
      const expectedUser = {
        id: 'usr_123',
        email: 'test@example.com',
        name: 'Test User',
      };
      mockUserRepo.findById.mockResolvedValue(expectedUser);

      // Act
      const result = await userService.getUserById('usr_123');

      // Assert
      expect(result).toEqual(expectedUser);
      expect(mockUserRepo.findById).toHaveBeenCalledWith('usr_123');
      expect(mockUserRepo.findById).toHaveBeenCalledTimes(1);
    });

    it('should check cache before querying database', async () => {
      // Arrange
      const cachedUser = { id: 'usr_123', email: 'cached@example.com' };
      mockCache.get.mockResolvedValue(cachedUser);

      // Act
      const result = await userService.getUserById('usr_123');

      // Assert
      expect(result).toEqual(cachedUser);
      expect(mockCache.get).toHaveBeenCalledWith('user:usr_123');
      expect(mockUserRepo.findById).not.toHaveBeenCalled();
    });

    it('should cache user after fetching from database', async () => {
      // Arrange
      const user = { id: 'usr_123', email: 'test@example.com' };
      mockCache.get.mockResolvedValue(null);
      mockUserRepo.findById.mockResolvedValue(user);

      // Act
      await userService.getUserById('usr_123');

      // Assert
      expect(mockCache.set).toHaveBeenCalledWith(
        'user:usr_123',
        user,
        expect.any(Number)
      );
    });
  });

  // ==================== Error Case Tests ====================

  describe('getUserById - error cases', () => {
    it('should throw UserNotFoundError when user does not exist', async () => {
      // Arrange
      mockCache.get.mockResolvedValue(null);
      mockUserRepo.findById.mockResolvedValue(null);

      // Act & Assert
      await expect(userService.getUserById('usr_missing'))
        .rejects
        .toThrow(UserNotFoundError);
    });

    it('should throw ValidationError when ID is empty', async () => {
      // Act & Assert
      await expect(userService.getUserById(''))
        .rejects
        .toThrow(ValidationError);
    });

    it('should throw ValidationError when ID is null', async () => {
      // Act & Assert
      await expect(userService.getUserById(null as any))
        .rejects
        .toThrow(ValidationError);
    });

    it('should propagate database errors', async () => {
      // Arrange
      const dbError = new Error('Database connection failed');
      mockCache.get.mockResolvedValue(null);
      mockUserRepo.findById.mockRejectedValue(dbError);

      // Act & Assert
      await expect(userService.getUserById('usr_123'))
        .rejects
        .toThrow('Database connection failed');
    });
  });

  // ==================== Create User Tests ====================

  describe('createUser', () => {
    const validUserData = {
      email: 'new@example.com',
      name: 'New User',
      password: 'SecureP@ss123',
    };

    it('should create user with valid data', async () => {
      // Arrange
      const createdUser = { id: 'usr_456', ...validUserData };
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockResolvedValue(createdUser);

      // Act
      const result = await userService.createUser(validUserData);

      // Assert
      expect(result.id).toBeDefined();
      expect(result.email).toBe(validUserData.email);
      expect(mockUserRepo.create).toHaveBeenCalled();
    });

    it('should hash password before storing', async () => {
      // Arrange
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockImplementation(async (data) => ({
        id: 'usr_123',
        ...data,
      }));

      // Act
      await userService.createUser(validUserData);

      // Assert
      expect(mockUserRepo.create).toHaveBeenCalledWith(
        expect.objectContaining({
          password: expect.not.stringMatching(validUserData.password),
        })
      );
    });

    it('should throw ValidationError for duplicate email', async () => {
      // Arrange
      mockUserRepo.findByEmail.mockResolvedValue({ id: 'existing' });

      // Act & Assert
      await expect(userService.createUser(validUserData))
        .rejects
        .toThrow(ValidationError);
    });

    it.each([
      ['missing email', { name: 'Test', password: 'Pass123!' }],
      ['missing name', { email: 'test@example.com', password: 'Pass123!' }],
      ['missing password', { email: 'test@example.com', name: 'Test' }],
      ['invalid email', { email: 'invalid', name: 'Test', password: 'Pass123!' }],
      ['weak password', { email: 'test@example.com', name: 'Test', password: 'abc' }],
    ])('should throw ValidationError for %s', async (_, invalidData) => {
      // Act & Assert
      await expect(userService.createUser(invalidData as any))
        .rejects
        .toThrow(ValidationError);
    });
  });

  // ==================== Boundary Tests ====================

  describe('boundary conditions', () => {
    it('should handle maximum name length (255 chars)', async () => {
      // Arrange
      const longName = 'A'.repeat(255);
      mockUserRepo.findByEmail.mockResolvedValue(null);
      mockUserRepo.create.mockResolvedValue({ id: 'usr_123' });

      // Act & Assert - should not throw
      await expect(userService.createUser({
        email: 'test@example.com',
        name: longName,
        password: 'SecureP@ss123',
      })).resolves.toBeDefined();
    });

    it('should reject name exceeding maximum length', async () => {
      // Arrange
      const tooLongName = 'A'.repeat(256);

      // Act & Assert
      await expect(userService.createUser({
        email: 'test@example.com',
        name: tooLongName,
        password: 'SecureP@ss123',
      })).rejects.toThrow(ValidationError);
    });

    it('should handle empty search results', async () => {
      // Arrange
      mockUserRepo.findMany.mockResolvedValue([]);

      // Act
      const result = await userService.searchUsers('nonexistent');

      // Assert
      expect(result).toEqual([]);
    });
  });
});

// ==================== Snapshot Tests ====================

describe('UserService snapshots', () => {
  it('should match user response structure', async () => {
    // Arrange
    const user = {
      id: 'usr_123',
      email: 'test@example.com',
      name: 'Test User',
      createdAt: new Date('2025-01-15'),
      role: 'user',
    };

    // Act
    const result = userService.formatUserResponse(user);

    // Assert
    expect(result).toMatchSnapshot();
  });
});

// ==================== Mock Timer Tests ====================

describe('UserService with timers', () => {
  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  it('should invalidate cache after TTL expires', async () => {
    // Arrange
    const user = { id: 'usr_123' };
    mockCache.get.mockResolvedValue(user);

    // Act
    await userService.getUserById('usr_123');
    vi.advanceTimersByTime(60 * 60 * 1000); // 1 hour

    // Assert
    expect(mockCache.delete).toHaveBeenCalledWith('user:usr_123');
  });
});
```

### Jest Configuration

```javascript
// jest.config.js
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src', '<rootDir>/tests'],
  testMatch: ['**/*.test.ts', '**/*.spec.ts'],
  collectCoverageFrom: [
    'src/**/*.ts',
    '!src/**/*.d.ts',
    '!src/**/index.ts',
  ],
  coverageThreshold: {
    global: {
      branches: 80,
      functions: 80,
      lines: 80,
      statements: 80,
    },
  },
  setupFilesAfterEnv: ['<rootDir>/tests/setup.ts'],
  moduleNameMapper: {
    '^@/(.*)$': '<rootDir>/src/$1',
  },
};
```

## Go Testing

### Basic Test Structure

```go
package user_test

import (
    "context"
    "errors"
    "testing"
    "time"

    "github.com/stretchr/testify/assert"
    "github.com/stretchr/testify/mock"
    "github.com/stretchr/testify/require"
    "github.com/stretchr/testify/suite"

    "myapp/internal/user"
    "myapp/internal/user/mocks"
)

// ==================== Table-Driven Tests ====================

func TestValidateEmail(t *testing.T) {
    tests := []struct {
        name     string
        email    string
        wantErr  bool
        errType  error
    }{
        {
            name:    "valid email",
            email:   "user@example.com",
            wantErr: false,
        },
        {
            name:    "valid email with subdomain",
            email:   "user@mail.example.com",
            wantErr: false,
        },
        {
            name:    "empty email",
            email:   "",
            wantErr: true,
            errType: user.ErrInvalidEmail,
        },
        {
            name:    "missing @ symbol",
            email:   "userexample.com",
            wantErr: true,
            errType: user.ErrInvalidEmail,
        },
        {
            name:    "missing domain",
            email:   "user@",
            wantErr: true,
            errType: user.ErrInvalidEmail,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            err := user.ValidateEmail(tt.email)

            if tt.wantErr {
                assert.Error(t, err)
                if tt.errType != nil {
                    assert.ErrorIs(t, err, tt.errType)
                }
            } else {
                assert.NoError(t, err)
            }
        })
    }
}

// ==================== Test Suite ====================

type UserServiceTestSuite struct {
    suite.Suite
    service  *user.Service
    mockRepo *mocks.Repository
    mockCache *mocks.Cache
    ctx       context.Context
}

func (s *UserServiceTestSuite) SetupTest() {
    s.mockRepo = mocks.NewRepository(s.T())
    s.mockCache = mocks.NewCache(s.T())
    s.service = user.NewService(s.mockRepo, s.mockCache)
    s.ctx = context.Background()
}

func (s *UserServiceTestSuite) TearDownTest() {
    s.mockRepo.AssertExpectations(s.T())
    s.mockCache.AssertExpectations(s.T())
}

func TestUserServiceSuite(t *testing.T) {
    suite.Run(t, new(UserServiceTestSuite))
}

// ==================== Happy Path Tests ====================

func (s *UserServiceTestSuite) TestGetUserByID_Success() {
    // Arrange
    expectedUser := &user.User{
        ID:    "usr_123",
        Email: "test@example.com",
        Name:  "Test User",
    }
    s.mockCache.On("Get", s.ctx, "user:usr_123").Return(nil, nil)
    s.mockRepo.On("FindByID", s.ctx, "usr_123").Return(expectedUser, nil)
    s.mockCache.On("Set", s.ctx, "user:usr_123", expectedUser, mock.Anything).Return(nil)

    // Act
    result, err := s.service.GetUserByID(s.ctx, "usr_123")

    // Assert
    s.Require().NoError(err)
    s.Equal(expectedUser, result)
}

func (s *UserServiceTestSuite) TestGetUserByID_CacheHit() {
    // Arrange
    cachedUser := &user.User{ID: "usr_123", Email: "cached@example.com"}
    s.mockCache.On("Get", s.ctx, "user:usr_123").Return(cachedUser, nil)

    // Act
    result, err := s.service.GetUserByID(s.ctx, "usr_123")

    // Assert
    s.Require().NoError(err)
    s.Equal(cachedUser, result)
    s.mockRepo.AssertNotCalled(s.T(), "FindByID")
}

// ==================== Error Case Tests ====================

func (s *UserServiceTestSuite) TestGetUserByID_NotFound() {
    // Arrange
    s.mockCache.On("Get", s.ctx, "user:usr_missing").Return(nil, nil)
    s.mockRepo.On("FindByID", s.ctx, "usr_missing").Return(nil, user.ErrNotFound)

    // Act
    result, err := s.service.GetUserByID(s.ctx, "usr_missing")

    // Assert
    s.Nil(result)
    s.ErrorIs(err, user.ErrNotFound)
}

func (s *UserServiceTestSuite) TestGetUserByID_EmptyID() {
    // Act
    result, err := s.service.GetUserByID(s.ctx, "")

    // Assert
    s.Nil(result)
    s.ErrorIs(err, user.ErrInvalidID)
}

// ==================== Create User Tests ====================

func (s *UserServiceTestSuite) TestCreateUser_Success() {
    // Arrange
    input := user.CreateUserInput{
        Email:    "new@example.com",
        Name:     "New User",
        Password: "SecureP@ss123",
    }
    s.mockRepo.On("FindByEmail", s.ctx, input.Email).Return(nil, nil)
    s.mockRepo.On("Create", s.ctx, mock.AnythingOfType("*user.User")).Return(nil)

    // Act
    result, err := s.service.CreateUser(s.ctx, input)

    // Assert
    s.Require().NoError(err)
    s.NotEmpty(result.ID)
    s.Equal(input.Email, result.Email)
}

func (s *UserServiceTestSuite) TestCreateUser_DuplicateEmail() {
    // Arrange
    existingUser := &user.User{Email: "exists@example.com"}
    input := user.CreateUserInput{Email: "exists@example.com"}
    s.mockRepo.On("FindByEmail", s.ctx, input.Email).Return(existingUser, nil)

    // Act
    result, err := s.service.CreateUser(s.ctx, input)

    // Assert
    s.Nil(result)
    s.ErrorIs(err, user.ErrDuplicateEmail)
}

// ==================== Benchmark Tests ====================

func BenchmarkValidateEmail(b *testing.B) {
    email := "user@example.com"
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        _ = user.ValidateEmail(email)
    }
}

func BenchmarkHashPassword(b *testing.B) {
    password := "SecureP@ss123"
    b.ResetTimer()

    for i := 0; i < b.N; i++ {
        _, _ = user.HashPassword(password)
    }
}

// ==================== Integration Tests ====================

func TestUserService_Integration(t *testing.T) {
    if testing.Short() {
        t.Skip("Skipping integration test in short mode")
    }

    // Setup test database
    db := setupTestDB(t)
    defer cleanupTestDB(t, db)

    service := user.NewService(user.NewRepository(db), nil)
    ctx := context.Background()

    // Create user
    input := user.CreateUserInput{
        Email:    "integration@test.com",
        Name:     "Integration Test",
        Password: "TestP@ss123",
    }
    created, err := service.CreateUser(ctx, input)
    require.NoError(t, err)
    require.NotEmpty(t, created.ID)

    // Retrieve user
    retrieved, err := service.GetUserByID(ctx, created.ID)
    require.NoError(t, err)
    assert.Equal(t, input.Email, retrieved.Email)
    assert.Equal(t, input.Name, retrieved.Name)
}
```

## API/HTTP Testing

### Python (FastAPI + httpx)

```python
import pytest
from httpx import AsyncClient
from fastapi import status

from myapp.main import app
from myapp.models import User


@pytest.fixture
def client():
    """Create async test client."""
    return AsyncClient(app=app, base_url="http://test")


class TestUserAPI:
    """Test suite for User API endpoints."""

    # ==================== GET /users/{id} ====================

    @pytest.mark.asyncio
    async def test_get_user_returns_200_for_existing_user(self, client):
        """GET /users/{id} should return 200 with user data."""
        # Act
        response = await client.get("/api/users/usr_123")

        # Assert
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["id"] == "usr_123"
        assert "email" in data

    @pytest.mark.asyncio
    async def test_get_user_returns_404_for_missing_user(self, client):
        """GET /users/{id} should return 404 for non-existent user."""
        # Act
        response = await client.get("/api/users/usr_nonexistent")

        # Assert
        assert response.status_code == status.HTTP_404_NOT_FOUND
        assert response.json()["detail"] == "User not found"

    # ==================== POST /users ====================

    @pytest.mark.asyncio
    async def test_create_user_returns_201_with_valid_data(self, client):
        """POST /users should create user and return 201."""
        # Arrange
        payload = {
            "email": "new@example.com",
            "name": "New User",
            "password": "SecureP@ss123"
        }

        # Act
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == status.HTTP_201_CREATED
        data = response.json()
        assert data["email"] == payload["email"]
        assert "id" in data
        assert "password" not in data  # Should not expose password

    @pytest.mark.asyncio
    async def test_create_user_returns_400_for_invalid_email(self, client):
        """POST /users should return 400 for invalid email."""
        # Arrange
        payload = {
            "email": "invalid-email",
            "name": "Test",
            "password": "SecureP@ss123"
        }

        # Act
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "email" in response.json()["detail"].lower()

    @pytest.mark.asyncio
    async def test_create_user_returns_409_for_duplicate_email(self, client):
        """POST /users should return 409 for existing email."""
        # Arrange
        payload = {"email": "existing@example.com", "name": "Test", "password": "Pass123!"}

        # Act (create first user)
        await client.post("/api/users", json=payload)
        # Act (create duplicate)
        response = await client.post("/api/users", json=payload)

        # Assert
        assert response.status_code == status.HTTP_409_CONFLICT

    # ==================== Authentication Tests ====================

    @pytest.mark.asyncio
    async def test_protected_endpoint_returns_401_without_token(self, client):
        """Protected endpoints should return 401 without auth."""
        # Act
        response = await client.get("/api/users/me")

        # Assert
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.asyncio
    async def test_protected_endpoint_returns_200_with_valid_token(
        self, client, auth_token
    ):
        """Protected endpoints should work with valid token."""
        # Act
        response = await client.get(
            "/api/users/me",
            headers={"Authorization": f"Bearer {auth_token}"}
        )

        # Assert
        assert response.status_code == status.HTTP_200_OK
```

## Testing Best Practices

### DO ✅

- **One assertion per test** - Focus on single behavior
- **Descriptive test names** - Clearly state what is being tested
- **Follow AAA pattern** - Arrange, Act, Assert
- **Test edge cases** - Boundaries, nulls, empty values
- **Use meaningful data** - Avoid "foo", "bar" placeholders
- **Keep tests independent** - No shared state between tests
- **Test error paths** - Not just happy paths
- **Use fixtures for common setup** - DRY principle
- **Test behavior, not implementation** - Focus on outcomes
- **Maintain test code quality** - Tests are code too

### DON'T ❌

- **Test implementation details** - Focus on public API
- **Use random data** - Unless testing randomness
- **Write flaky tests** - Tests must be deterministic
- **Depend on test order** - Tests should run in any order
- **Mock everything** - Some integration is valuable
- **Ignore test failures** - Fix or delete, never skip
- **Test third-party code** - Focus on your code
- **Write slow tests** - Keep unit tests fast
- **Duplicate test logic** - Extract to helpers
- **Test trivial getters/setters** - Focus on logic

## Test Coverage Guidelines

### Coverage Targets by Type

| Test Type | Coverage Target |
|-----------|-----------------|
| Unit Tests | 80%+ line coverage |
| Integration Tests | Critical paths 100% |
| E2E Tests | Happy paths + key edge cases |

### What to Prioritize

1. **Business-critical logic** - Payment, auth, data integrity
2. **Complex algorithms** - Sorting, calculations, transformations
3. **Edge cases** - Boundaries, empty states, errors
4. **Public APIs** - Entry points to your code
5. **Bug fixes** - Prevent regressions

### What NOT to Test

1. **Framework code** - Trust your dependencies
2. **Configuration** - Simple key-value mapping
3. **Generated code** - ORM models, protos
4. **Third-party integrations** - Mock instead
5. **Trivial code** - Simple getters/setters

## Output Format

When generating tests, provide:

```
## Test Strategy

**Testing Type:** [Unit / Integration / E2E]
**Framework:** [pytest / Jest / Go testing / etc.]
**Coverage Focus:** [What aspects are being tested]

---

## Generated Tests

[Complete test file with all test cases]

---

## Test Summary

| Category | Tests | Coverage |
|----------|-------|----------|
| Happy Path | X | Core functionality |
| Edge Cases | Y | Boundaries, special values |
| Error Cases | Z | Exception handling |
| Integration | W | Component interaction |

## Recommended Additional Tests

- [Test case 1 that should be added]
- [Test case 2 that should be added]

## Setup Required

- [Any fixtures or mocks needed]
- [Test database or external dependencies]
```

## Notes

- Adapt test depth to code complexity and criticality
- Prioritize tests that catch real bugs
- Balance coverage with maintainability
- Update tests when requirements change
- Use CI/CD to enforce test passing
- Consider property-based testing for complex logic
- Write tests before fixing bugs (regression prevention)
