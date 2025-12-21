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

    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_MIME_TYPES: list[str] = []  # Empty list means all types allowed (optional whitelist)


settings = Settings()
