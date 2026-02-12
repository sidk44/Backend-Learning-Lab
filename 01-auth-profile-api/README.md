# Auth + Profile API

A production-ready **FastAPI** authentication and profile management API with **PostgreSQL**, **SQLAlchemy**, and **JWT** authentication.

## Features

✅ **User Registration** (`POST /auth/register`)  
✅ **User Login** (`POST /auth/login`)  
✅ **JWT Token Authentication**  
✅ **Protected Profile Endpoints**:
  - `GET /me` - Get current user profile
  - `PATCH /me` - Update name and bio  
✅ **Secure Password Hashing** (bcrypt_sha256)  
✅ **Clean Architecture** (routes → services → repositories)  
✅ **Comprehensive Tests** (pytest with 100% endpoint coverage)  
✅ **Input Validation** (Pydantic schemas)  
✅ **Proper HTTP Status Codes** (401, 409, 422, etc.)

---

## Project Structure

```
01-auth-profile-api/
├── src/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Settings (env vars)
│   │   ├── security.py      # Password hashing
│   │   ├── tokens.py        # JWT creation/verification
│   │   └── deps.py          # Authentication dependency
│   ├── db/
│   │   ├── base.py          # SQLAlchemy Base
│   │   └── session.py       # Database session
│   ├── models/
│   │   └── user.py          # User SQLAlchemy model
│   ├── repositories/
│   │   └── user_repo.py     # Database queries
│   ├── routes/
│   │   ├── auth.py          # Register & login endpoints
│   │   └── profile.py       # Profile endpoints
│   ├── schemas/
│   │   └── user.py          # Pydantic schemas
│   └── services/
│       ├── auth_service.py  # Auth business logic
│       └── profile_service.py # Profile business logic
├── tests/
│   ├── conftest.py          # Pytest fixtures
│   ├── test_auth.py         # Auth endpoint tests
│   └── test_profile.py      # Profile endpoint tests
├── requirements.txt
├── pytest.ini
└── README.md
```

---

## Setup Instructions

### 1. Prerequisites

- **Python 3.12+**
- **PostgreSQL** (running locally or remote)

### 2. Install Dependencies

```bash
cd 01-auth-profile-api
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Configure Environment Variables

Create a `.env` file:

```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db

# JWT
JWT_SECRET=your-super-secret-key-change-this-in-production
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
```

**Security Note:** Generate a strong `JWT_SECRET`:
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run the Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Server will start at: **http://localhost:8000**

Interactive API docs: **http://localhost:8000/docs**

---

## API Endpoints

### Health Check

#### `GET /health`
Simple health check endpoint.

**Response:**
```json
{
  "status": "ok"
}
```

---

### Authentication

#### `POST /auth/register`
Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "bio": null,
    "created_at": "2026-02-12T08:00:00Z",
    "updated_at": "2026-02-12T08:00:00Z"
  }
}
```

**Error Responses:**
- `409 Conflict` - Email already registered
- `422 Unprocessable Entity` - Invalid email format or password too short

---

#### `POST /auth/login`
Login with existing credentials.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response (200 OK):**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "bio": null,
    "created_at": "2026-02-12T08:00:00Z",
    "updated_at": "2026-02-12T08:00:00Z"
  }
}
```

**Error Response:**
- `401 Unauthorized` - Invalid email or password

---

### Profile (Protected Routes)

**All profile endpoints require authentication:**
```
Authorization: Bearer <access_token>
```

#### `GET /me`
Get current user's profile.

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "bio": "Software developer",
  "created_at": "2026-02-12T08:00:00Z",
  "updated_at": "2026-02-12T08:00:00Z"
}
```

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `403 Forbidden` - No Authorization header

---

#### `PATCH /me`
Update profile (name and/or bio).

**Request (partial update):**
```json
{
  "name": "Jane Smith",
  "bio": "Full-stack developer passionate about APIs"
}
```

You can update only one field:
```json
{
  "bio": "Updated bio only"
}
```

**Response (200 OK):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Jane Smith",
  "bio": "Full-stack developer passionate about APIs",
  "created_at": "2026-02-12T08:00:00Z",
  "updated_at": "2026-02-12T08:05:30Z"
}
```

**Validation Rules:**
- `name`: 2-120 characters
- `bio`: max 500 characters

**Error Responses:**
- `401 Unauthorized` - Missing or invalid token
- `422 Unprocessable Entity` - Validation error

**Security:** You cannot update `email`, `password`, `id`, or timestamps via this endpoint.

---

## Running Tests

### Run All Tests

```bash
pytest
```

### Run with Coverage

```bash
pytest --cov=src --cov-report=term-missing
```

### Run Specific Test File

```bash
pytest tests/test_auth.py
pytest tests/test_profile.py
```

### Run Verbose

```bash
pytest -v
```

### Test Coverage

The test suite covers:
- ✅ User registration (success, duplicate email, validation)
- ✅ User login (success, wrong credentials)
- ✅ Get profile (authenticated, no token, invalid token)
- ✅ Update profile (name, bio, both, validation)
- ✅ Authorization checks on protected endpoints

---

## Database Management

### Create Database

```bash
# Connect to PostgreSQL
psql -U postgres

# Create database
CREATE DATABASE auth_db;
```

### Reset Database

Drop all tables and recreate (useful during development):

```bash
# In PostgreSQL
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
```

Or just restart the server - tables are created automatically via `init_db()` on startup.

---

## Development Tips

### Interactive API Docs

FastAPI auto-generates interactive docs:
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Test with cURL

**Register:**
```bash
curl -X POST http://localhost:8000/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234","name":"Test User"}'
```

**Login:**
```bash
curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"test1234"}'
```

**Get Profile:**
```bash
# Replace <TOKEN> with actual token from login response
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer <TOKEN>"
```

**Update Profile:**
```bash
curl -X PATCH http://localhost:8000/me \
  -H "Authorization: Bearer <TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"name":"Updated Name","bio":"New bio"}'
```

### Check Logs

The server logs all requests and errors to the console. Watch for:
- SQL queries (if `echo=True` in `create_engine`)
- Authentication failures
- Validation errors

---

## Security Best Practices Implemented

✅ **Passwords Never Stored in Plain Text** - bcrypt_sha256 hashing  
✅ **JWT Expiry** - Tokens expire after 60 minutes (configurable)  
✅ **No Password in Responses** - UserPublic schema excludes password_hash  
✅ **Protected Fields** - Cannot update email/password via PATCH /me  
✅ **User Enumeration Prevention** - Same error message for wrong email/password  
✅ **Input Validation** - Pydantic schemas validate all inputs  
✅ **Prepared Statements** - SQLAlchemy prevents SQL injection  
✅ **HTTPS Recommended** - Use reverse proxy (Nginx) with SSL in production

---

## Common Issues & Solutions

### Issue: Database Connection Error

**Error:** `sqlalchemy.exc.OperationalError: connection to server failed`

**Solution:**
1. Check PostgreSQL is running: `systemctl status postgresql`
2. Verify `DATABASE_URL` in `.env`
3. Test connection: `psql -U user -d auth_db`

### Issue: bcrypt 72-byte error

**Error:** `ValueError: password cannot be longer than 72 bytes`

**Solution:** Already fixed! The `_normalize_password()` function handles this.

### Issue: Tests fail with "table already exists"

**Solution:** The test DB is auto-cleaned. If tests still fail:
```bash
rm test.db  # Remove test database file
pytest      # Run again
```

### Issue: Token expired/invalid

**Error:** `401 Unauthorized: Invalid or expired token`

**Solution:** 
1. Login again to get a new token
2. Check token expiry time in config (default 60 minutes)
3. Ensure you're passing: `Authorization: Bearer <token>`

---

## Next Steps / Enhancements

Possible extensions to this project:

- [ ] **Email Verification** - Send verification link after registration
- [ ] **Password Reset** - Forgot password flow
- [ ] **Refresh Tokens** - Long-lived refresh tokens + short-lived access tokens
- [ ] **Email Update** - Secure flow to change email with verification
- [ ] **Rate Limiting** - Prevent brute force attacks
- [ ] **User Roles** - Admin vs regular user permissions
- [ ] **Profile Pictures** - File upload + storage
- [ ] **Account Deletion** - Soft delete with confirmation
- [ ] **OAuth Integration** - Login with Google/GitHub
- [ ] **Audit Logging** - Track all user actions

---

## Architecture Highlights

### Clean Separation of Concerns

```
Routes (HTTP layer)
    ↓
Services (Business logic)
    ↓
Repositories (Database operations)
    ↓
Database
```

**Why this matters:**
- ✅ Easy to test each layer independently
- ✅ Changes to DB don't affect business rules
- ✅ Can swap implementations (e.g., SQLite → PostgreSQL)

### Dependency Injection

FastAPI's `Depends()` makes code testable:
- Routes don't import database directly
- Tests can override dependencies (use test DB)
- Easy to mock for unit tests

### Error Handling

Custom exceptions (`EmailAlreadyExists`, `InvalidCredentials`) map to proper HTTP status codes without exposing internals.

---

## License

MIT

## Author

Built as part of the Backend Learning Lab project series.
