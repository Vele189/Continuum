# Security utilities

from passlib import hash as passlib_hash
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings


ALGORITHM = settings.ALGORITHM
def hash_password(password: str):
    return passlib_hash.pbkdf2_sha256.hash(password)


def verify_password(password: str, hashed: str):
    return passlib_hash.pbkdf2_sha256.verify(password, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    expire = datetime.utcnow() + timedelta(hours=settings.REFRESH_TOKEN_EXPIRE_HOURS)
    data.update({"exp": expire, "type": "refresh"})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)
