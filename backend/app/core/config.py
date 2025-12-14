from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Continuum API"
    API_V1_STR: str = "/api/v1"

    SECRET_KEY: str = "d97c0d1633a6da68d9f7393c087e9d8b"  # TODO: Move to environment variable
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_HOURS: int = 24

    DATABASE_URL: str = "sqlite:///./continuum.db"

    class Config:
        env_file = ".env"


settings = Settings()
