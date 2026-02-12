"""
Pytest configuration and fixtures.

Why:
- Shared test fixtures (like test client, test DB) go here.
- Runs once before tests, keeps tests clean.
"""

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.main import app
from src.db.base import Base
from src.db.session import get_db


# Use in-memory SQLite for tests (fast, isolated)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}  # needed for SQLite
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="function")
def db():
    """
    Create a fresh database for each test.
    
    Why:
    - Tests are isolated (one test doesn't affect another).
    - Clean slate every time.
    """
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create session
    db = TestingSessionLocal()
    
    try:
        yield db
    finally:
        db.close()
        # Drop tables after test
        Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="function")
def client(db):
    """
    FastAPI test client with overridden DB dependency.
    
    Why:
    - Uses test DB instead of production DB.
    - Makes real HTTP requests to the app (without network).
    """
    def override_get_db():
        try:
            yield db
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    
    app.dependency_overrides.clear()
