"""
Centralized configuration.

Why:
- Keeps secrets/settings out of code.
- Makes deployments easy (change env vars, not code).
"""

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # Reads DATABASE_URL from environment or .env file
    DATABASE_URL: str

    #tell pydantic to also load a local ".env" file if present (dev-friendly)
    model_config = SettingsConfigDict(env_file = ".env", env_file_encodings="utf-8")

#create a settings object to import anywhere
settings = Settings()