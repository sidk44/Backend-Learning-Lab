"""
Security utilities (password hashing).

Why:
- Passwords must NEVER be stored in plain text.
- We store only a hashed version.
- bcrypt is slow by design => makes brute forcing harder.
"""

import hashlib

from passlib.context import CryptContext

# We configure bcrypt as our hashing algorithm
pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")


def _normalize_password(password: str) -> str:
    """
    Normalize password input for hashing.

    Why:
    - bcrypt has a hard 72-byte limit.
    - If the password exceeds 72 bytes, we pre-hash with SHA-256.
    """
    password_bytes = password.encode("utf-8")
    if len(password_bytes) > 72:
        # Use hex so the normalized value is a str and <= 72 chars.
        return hashlib.sha256(password_bytes).hexdigest()
    return password


def hash_password(password: str) -> str:
    """
    Convert plain password to hash.

    Why:
    - DB stores hash, not the password.
    - If DB leaks, attacker still can't see real passwords easily.
    """
    return pwd_context.hash(_normalize_password(password))


def verify_password(password: str, password_hash: str) -> bool:
    """
    Check if the entered password matches the stored hash.

    Used during login later.
    """
    return pwd_context.verify(_normalize_password(password), password_hash)
