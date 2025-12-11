# Security utilities

from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = settings.ALGORITHM
 # TODO: To be discussed

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed: str):
    return pwd_context.verify(password, hashed)

def create_access_token(data: dict):
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    data.update({"exp": expire})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)

def create_refresh_token(data: dict):
    # For now assume same expiry or add REFRESH_MINUTE to settings. Keeping simple for now. 
    # Using hardcoded days for refresh as in original or move to settings. 
    # Let's keep a local constant or add to settings if needed. 
    # For now I will just use 30 days hardcoded or better, let's add it to settings if strictly required, 
    # but the plan didn't explicitly mention refresh token expiry in config.
    # I'll use 30 days as before but use correct secret key.
    expire = datetime.utcnow() + timedelta(days=30) 
    data.update({"exp": expire, "type": "refresh"})
    return jwt.encode(data, settings.SECRET_KEY, algorithm=ALGORITHM)