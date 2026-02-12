"""
App entry point.

Why:
- Keeps FastAPI instance in one place.
- We'll add routers here later (auth, profile, etc.).
"""

from fastapi import FastAPI,Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from src.db.session import init_db,get_db
from src.routes.auth import router as auth_router
from src.routes.profile import router as profile_router

# IMPORTANT:
# We must import models so SQLAlchemy "registers" them with Base.metadata.
# Otherwise, Base.metadata.create_all() won't know about your tables.
from src.models.user import User  # noqa: F401  (import just for side-effect)



app = FastAPI(title = "Auth + Profile API")

@app.on_event("startup")
def on_startup():

    """
    Runs once when the server starts.

    Why:
    - Create tables so you can start building routes immediately.
    """

    init_db()


app.include_router(profile_router)
app.include_router(auth_router)

@app.get("/health")
def health_check():
    """
    Quick sanity endpoint.
    """
    
    return {"status":"ok"}


@app.get("/db-check")
def db_check(db: Session = Depends(get_db)):
    """
    Quick DB test endpoint.

    What it does:
    - runs a simple SQL query: SELECT 1
    - if it works, DB connection + session is good.

    Why:
    - easiest way to confirm Postgres connection.
    """
    db.execute(text("SELECT 1"))
    return {"db": "ok"}
