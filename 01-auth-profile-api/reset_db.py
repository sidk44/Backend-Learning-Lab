"""
Database migration helper.

Quick way to reset database during development.
In production, you'd use Alembic for proper migrations.
"""

from src.db.base import Base
from src.db.session import engine
from src.models.user import User  # noqa: F401 - import needed for Base.metadata


def reset_database():
    """
    Drop all tables and recreate them.
    
    WARNING: This deletes all data!
    Only use in development.
    """
    print("Dropping all tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("Creating all tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database reset complete!")


if __name__ == "__main__":
    import sys
    
    response = input("⚠️  This will delete ALL data. Continue? (yes/no): ")
    if response.lower() == "yes":
        reset_database()
    else:
        print("Cancelled.")
        sys.exit(0)
