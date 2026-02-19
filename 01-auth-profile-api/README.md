# Auth + Profile API

A beginner-friendly **FastAPI** backend demonstrating:
- User registration & login with **JWT authentication**
- Protected profile endpoints (GET/PATCH `/me`)
- PostgreSQL database with **SQLAlchemy ORM**
- Clean architecture (routes → services → repositories)
- Comprehensive **pytest** test suite

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- PostgreSQL running locally
- Virtual environment recommended

### 1. Setup

```bash
# Navigate to project directory
cd 01-auth-profile-api

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

Create `.env` file in the project root:

```env
DATABASE_URL=postgresql://user:password@localhost:5432/auth_db
SECRET_KEY=your-secret-key-min-32-chars-long
```

**Generate a secure SECRET_KEY:**
```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 3. Initialize Database

```bash
# Reset/create tables (clears existing data!)
python reset_db.py
```

### 4. Run Server

```bash
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at:
- **API:** http://localhost:8000
- **Interactive docs:** http://localhost:8000/docs
- **Alternative docs:** http://localhost:8000/redoc

---

## 📡 API Endpoints

### **Authentication**

#### Register New User
```http
POST /auth/register
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123",
  "name": "John Doe"
}
```

**Response (201):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "bio": null,
    "created_at": "2026-02-12T08:00:00"
  }
}
```

#### Login
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepass123"
}
```

**Response (200):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "name": "John Doe",
    "bio": null,
    "created_at": "2026-02-12T08:00:00"
  }
}
```

### **Profile (Protected)**

All profile endpoints require `Authorization: Bearer <token>` header.

#### Get Current User Profile
```http
GET /me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "John Doe",
  "bio": "Software developer",
  "created_at": "2026-02-12T08:00:00"
}
```

#### Update Profile
```http
PATCH /me
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
Content-Type: application/json

{
  "name": "Jane Doe",
  "bio": "Full-stack developer"
}
```

**Response (200):**
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "email": "user@example.com",
  "name": "Jane Doe",
  "bio": "Full-stack developer",
  "created_at": "2026-02-12T08:00:00"
}
```

**Notes:**
- Both fields are optional (partial updates)
- `email`, `password_hash`, `id` cannot be updated via this endpoint
- Returns 403 if attempting to modify protected fields

---

## 🧪 Testing

```bash
# Run all tests
pytest -v

# Run specific test file
pytest tests/test_auth.py -v

# Run with coverage
pytest --cov=src --cov-report=html
```

**Test Coverage:**
- ✅ User registration (validation, duplicates)
- ✅ Login (success, wrong password, missing user)
- ✅ Profile retrieval (authenticated/unauthenticated)
- ✅ Profile updates (partial, immutable fields)
- ✅ JWT token validation
- ✅ Error handling (401, 403, 409, 422)

---

## 📂 Project Structure

```
01-auth-profile-api/
├── src/
│   ├── core/           # Core utilities
│   │   ├── config.py   # Environment config
│   │   ├── deps.py     # FastAPI dependencies (JWT)
│   │   └── security.py # Password hashing
│   ├── db/
│   │   └── session.py  # Database session management
│   ├── models/
│   │   └── user.py     # SQLAlchemy User model
│   ├── repositories/
│   │   └── user_repo.py # Database operations
│   ├── routes/
│   │   ├── auth.py     # /auth/* endpoints
│   │   └── profile.py  # /me endpoints
│   ├── schemas/
│   │   └── user.py     # Pydantic request/response models
│   ├── services/
│   │   ├── auth_service.py    # Auth business logic
│   │   └── profile_service.py # Profile business logic
│   └── main.py         # FastAPI app entry point
├── tests/
│   ├── conftest.py     # Pytest fixtures
│   ├── test_auth.py    # Auth endpoint tests
│   └── test_profile.py # Profile endpoint tests
├── .env                # Environment variables (not in Git)
├── .gitignore
├── requirements.txt
├── reset_db.py         # Database reset utility
└── README.md
```

---

## 🔒 Security Features

- **Password Hashing:** bcrypt_sha256 with automatic handling of 72-byte limit
- **JWT Tokens:** HS256 signing with 60-minute expiry
- **Protected Routes:** Middleware validates tokens and loads user context
- **Field Protection:** Email, password_hash, and ID cannot be modified via API
- **No Sensitive Data Leaks:** Passwords never returned in responses

---

## 🛠️ Development Tips

### Reset Database
```bash
python reset_db.py
```
⚠️ **Warning:** This deletes all data!

### Environment Variables
- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT signing key (min 32 chars)

### Common Issues

**Issue:** `ValueError: password cannot be longer than 72 bytes`
- **Fix:** Already handled via bcrypt_sha256 + password normalization

**Issue:** Database connection fails
- **Fix:** Check PostgreSQL is running and `.env` has correct credentials

**Issue:** Tests fail with "table already exists"
- **Fix:** Tests use isolated SQLite database, ensure `conftest.py` is present

### Testing Protected Endpoints Manually

```bash
# 1. Register/login to get token
TOKEN=$(curl -X POST http://localhost:8000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"test@example.com","password":"pass123"}' \
  | jq -r '.token')

# 2. Use token in requests
curl -X GET http://localhost:8000/me \
  -H "Authorization: Bearer $TOKEN"
```

---

## 📚 Learning Resources

This project demonstrates:
- **FastAPI:** Modern async Python web framework
- **SQLAlchemy:** ORM for database operations
- **Pydantic:** Request/response validation
- **JWT:** Stateless authentication
- **Pytest:** Test-driven development
- **Clean Architecture:** Separation of concerns

### Next Steps
- Add email verification
- Implement refresh tokens
- Add rate limiting
- Deploy to cloud (Railway, Render, etc.)
- Add password reset flow
- Implement role-based access control (RBAC)

---


