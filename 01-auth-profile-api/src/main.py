"""
App entry point.

Why:
- Keeps FastAPI instance in one place.
- We'll add routers here later (auth, profile, etc.).
"""

from fastapi import FastAPI

app = FastAPI(title = "Auth + Profile API")

@app.get("/health")
def health_check():
    """
    Quick sanity endpoint.

    Why:
    - Confirms server is running.
    - Useful for debugging + deployments.
    """
    
    return {"status":"ok"}