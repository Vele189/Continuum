from pydantic_settings import BaseSettings
from pydantic import ConfigDict


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")
    
    PROJECT_NAME: str = "Continuum API"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "d97c0d1633a6da68d9f7393c087e9d8b"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24

    DATABASE_URL: str = "sqlite:///./continuum.db"


settings = Settings()
