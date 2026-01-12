from pydantic import ConfigDict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env")

    PROJECT_NAME: str = "Continuum API"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "d97c0d1633a6da68d9f7393c087e9d8b"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24

    # File upload settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB in bytes
    UPLOAD_DIR: str = "./uploads"
    ALLOWED_MIME_TYPES: list[str] = []  # Empty list means all types allowed (optional whitelist)

    # Webhook secrets for Git providers
    GITHUB_WEBHOOK_SECRET: str = ""
    GITLAB_WEBHOOK_TOKEN: str = ""
    BITBUCKET_WEBHOOK_SECRET: str = ""

    # SMTP settings (Also added to docker-compose.yml)
    SMTP_HOST: str = "mailpit"
    SMTP_PORT: int = 1025
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    EMAILS_FROM_EMAIL: str = "noreply@continuum.app"
    EMAILS_FROM_NAME: str = "Continuum"

    # Frontend/Base URL for email links
    FRONTEND_URL: str = "http://localhost:5173"  # Default for local dev, override in production


settings = Settings()
