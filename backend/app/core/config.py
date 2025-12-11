
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "Continuum API"
    API_V1_STR: str = "/api/v1"
    
    # Security
    SECRET_KEY: str = "d97c0d1633a6da68d9f7393c087e9d8b"  # to be changed
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24
    
    # Database
    DATABASE_URL: str = "sqlite:///./sql_app.db" #for my local testing

    class Config:
        env_file = ".env"

settings = Settings()
