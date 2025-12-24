# Security utilities

from datetime import datetime, timedelta, timezone

from passlib import hash as passlib_hash
from jose import jwt

from app.core.config import settings


ALGORITHM = settings.ALGORITHM
def hash_password(password: str):
    return passlib_hash.pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str):
    return passlib_hash.pbkdf2_sha256.verify(password, hashed)

def create_access_token(data: dict):
    to_encode = data.copy()
    # JWT spec requires 'sub' to be a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    to_encode = data.copy()
    # JWT spec requires 'sub' to be a string
    if "sub" in to_encode:
        to_encode["sub"] = str(to_encode["sub"])
    expire = datetime.now(timezone.utc) + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
