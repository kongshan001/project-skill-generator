# Skill Patterns Library

This document contains common patterns for generating effective Claude Code skills.

## Pattern Categories

### 1. API Module Pattern

For modules that expose APIs (REST, GraphQL, RPC).

```markdown
---
name: api-core
description: >
  REST API endpoints and handlers. Use when: (1) Creating new endpoints,
  (2) Modifying API responses, (3) Adding authentication to routes,
  (4) Implementing API versioning.
---

# API Core

## Endpoints Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | /api/users | List users |
| POST | /api/users | Create user |
| PUT | /api/users/:id | Update user |

## Request/Response Patterns

### Standard Response
```json
{
  "success": true,
  "data": { ... },
  "error": null
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input"
  }
}
```

## Authentication

All protected endpoints require Bearer token:
```
Authorization: Bearer <token>
```

## Common Patterns

### 1. Pagination
```python
@router.get("/items")
async def list_items(
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100)
):
    offset = (page - 1) * per_page
    items = await Item.query.offset(offset).limit(per_page).all()
    return {"items": items, "page": page, "per_page": per_page}
```

### 2. Validation
```python
from pydantic import BaseModel, validator

class ItemCreate(BaseModel):
    name: str
    price: float
    
    @validator('price')
    def validate_price(cls, v):
        if v < 0:
            raise ValueError('Price must be positive')
        return v
```

### 3. Error Handling
```python
from fastapi import HTTPException

@router.get("/items/{item_id}")
async def get_item(item_id: int):
    item = await Item.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item
```
```

### 2. Database Module Pattern

For modules that handle data persistence.

```markdown
---
name: database-core
description: >
  Database models, queries, and migrations. Use when: (1) Creating models,
  (2) Writing complex queries, (3) Optimizing database performance,
  (4) Creating migrations.
---

# Database Core

## Models

### Base Model
```python
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
```

### Example Model
```python
class User(BaseModel):
    __tablename__ = 'users'
    
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    
    # Relationships
    posts = relationship("Post", back_populates="author")
```

## Query Patterns

### 1. Basic CRUD
```python
# Create
user = User(username="john", email="john@example.com")
session.add(user)
session.commit()

# Read
user = session.query(User).filter_by(username="john").first()

# Update
user.email = "newemail@example.com"
session.commit()

# Delete
session.delete(user)
session.commit()
```

### 2. Complex Queries
```python
# Join
users_with_posts = session.query(User)\
    .join(Post)\
    .filter(Post.published == True)\
    .all()

# Aggregate
from sqlalchemy import func
post_count = session.query(
    User.username,
    func.count(Post.id).label('post_count')
).join(Post).group_by(User.id).all()
```

### 3. Pagination
```python
def paginate(query, page, per_page):
    offset = (page - 1) * per_page
    return query.offset(offset).limit(per_page).all()
```

## Migrations

### Create Migration
```bash
alembic revision --autogenerate -m "Add user table"
```

### Apply Migration
```bash
alembic upgrade head
```
```

### 3. Frontend Component Pattern

For React/Vue/Angular components.

```markdown
---
name: frontend-ui
description: >
  React UI components and patterns. Use when: (1) Creating components,
  (2) Managing state, (3) Handling user interactions, (4) Styling components.
---

# Frontend UI

## Component Structure

```typescript
import React, { useState, useEffect } from 'react';
import styles from './Component.module.css';

interface Props {
  title: string;
  onSubmit: (data: FormData) => void;
}

export const Component: React.FC<Props> = ({ title, onSubmit }) => {
  const [state, setState] = useState(initialState);
  
  useEffect(() => {
    // Side effects
  }, [dependencies]);
  
  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    onSubmit(state);
  };
  
  return (
    <div className={styles.container}>
      <h1>{title}</h1>
      <form onSubmit={handleSubmit}>
        {/* Form fields */}
      </form>
    </div>
  );
};
```

## State Management

### Local State
```typescript
const [count, setCount] = useState(0);
```

### Context
```typescript
const ThemeContext = React.createContext('light');

const App = () => (
  <ThemeContext.Provider value="dark">
    <Component />
  </ThemeContext.Provider>
);

const Component = () => {
  const theme = useContext(ThemeContext);
  return <div className={theme}>Content</div>;
};
```

## Common Patterns

### 1. Form Handling
```typescript
const [formData, setFormData] = useState({
  username: '',
  email: ''
});

const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
  setFormData({
    ...formData,
    [e.target.name]: e.target.value
  });
};
```

### 2. API Calls
```typescript
const [data, setData] = useState(null);
const [loading, setLoading] = useState(true);
const [error, setError] = useState(null);

useEffect(() => {
  fetch('/api/data')
    .then(res => res.json())
    .then(setData)
    .catch(setError)
    .finally(() => setLoading(false));
}, []);
```

### 3. Conditional Rendering
```typescript
{loading && <Spinner />}
{error && <ErrorMessage error={error} />}
{data && <DataDisplay data={data} />}
```
```

### 4. Authentication Pattern

For auth/security modules.

```markdown
---
name: auth-security
description: >
  Authentication and security patterns. Use when: (1) Implementing login/logout,
  (2) Managing sessions, (3) Securing endpoints, (4) Handling tokens.
---

# Authentication & Security

## Authentication Flow

### 1. Login
```python
from datetime import datetime, timedelta
import jwt

def login(credentials):
    user = authenticate(credentials)
    if not user:
        raise AuthenticationError("Invalid credentials")
    
    token = create_access_token(user)
    refresh_token = create_refresh_token(user)
    
    return {
        "access_token": token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

def create_access_token(user, expires_delta=timedelta(hours=1)):
    payload = {
        "sub": user.id,
        "exp": datetime.utcnow() + expires_delta,
        "type": "access"
    }
    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")
```

### 2. Token Validation
```python
from functools import wraps

def require_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = extract_token_from_request()
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = get_user(payload["sub"])
            return f(current_user, *args, **kwargs)
        except jwt.ExpiredSignatureError:
            raise AuthenticationError("Token expired")
        except jwt.InvalidTokenError:
            raise AuthenticationError("Invalid token")
    return decorated
```

### 3. Refresh Token
```python
def refresh_token(refresh_token):
    try:
        payload = jwt.decode(refresh_token, SECRET_KEY, algorithms=["HS256"])
        if payload["type"] != "refresh":
            raise AuthenticationError("Invalid token type")
        
        user = get_user(payload["sub"])
        return create_access_token(user)
    except jwt.InvalidTokenError:
        raise AuthenticationError("Invalid refresh token")
```

## Security Best Practices

### 1. Password Hashing
```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)
```

### 2. Rate Limiting
```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@app.post("/login")
@limiter.limit("5/minute")
async def login(request: Request, credentials: LoginRequest):
    # Login logic
    pass
```

### 3. CORS
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://example.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```
```

### 5. Testing Pattern

For test modules.

```markdown
---
name: testing
description: >
  Test patterns and utilities. Use when: (1) Writing unit tests,
  (2) Writing integration tests, (3) Mocking dependencies, (4) Setting up test data.
---

# Testing

## Test Structure

```python
import pytest
from unittest.mock import Mock, patch

class TestUserService:
    """Test suite for UserService"""
    
    @pytest.fixture
    def user_service(self):
        """Create user service instance"""
        return UserService()
    
    @pytest.fixture
    def mock_db(self):
        """Mock database"""
        return Mock()
    
    def test_create_user_success(self, user_service, mock_db):
        """Test successful user creation"""
        # Arrange
        user_data = {"username": "john", "email": "john@example.com"}
        
        # Act
        result = user_service.create(user_data, mock_db)
        
        # Assert
        assert result.username == "john"
        mock_db.add.assert_called_once()
```

## Common Patterns

### 1. Fixtures
```python
@pytest.fixture
def sample_user():
    return User(id=1, username="testuser", email="test@example.com")

@pytest.fixture
def auth_headers(sample_user):
    token = create_test_token(sample_user)
    return {"Authorization": f"Bearer {token}"}
```

### 2. Mocking
```python
@patch('module.external_api_call')
def test_with_mock(mock_api):
    mock_api.return_value = {"status": "success"}
    
    result = function_under_test()
    
    assert result == expected_value
    mock_api.assert_called_once_with(expected_args)
```

### 3. Parametrized Tests
```python
@pytest.mark.parametrize("input,expected", [
    ("valid@email.com", True),
    ("invalid-email", False),
    ("", False),
])
def test_email_validation(input, expected):
    assert validate_email(input) == expected
```

### 4. Async Tests
```python
@pytest.mark.asyncio
async def test_async_function():
    result = await async_function()
    assert result == expected
```

## Test Organization

```
tests/
├── unit/
│   ├── test_models.py
│   ├── test_services.py
│   └── test_utils.py
├── integration/
│   ├── test_api.py
│   └── test_db.py
└── conftest.py  # Shared fixtures
```
```

## Pattern Selection Guide

| Module Type | Recommended Patterns |
|-------------|---------------------|
| API/Routes | API Module, Authentication |
| Models/DB | Database Module |
| Components | Frontend Component |
| Auth | Authentication, Security |
| Tests | Testing |
| Utils | Generic, with specific domain patterns |

## Customization

Each pattern can be customized based on:
- **Framework**: Adjust for FastAPI, Django, Flask, etc.
- **Language**: Adapt to TypeScript, JavaScript, Python
- **Domain**: Add domain-specific examples and patterns
- **Conventions**: Match project naming and structure
