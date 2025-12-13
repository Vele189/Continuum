# Main application entry point
import os
from fastapi import FastAPI
from app.api.v1.routes import users, auth, admin
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine
from app.utils.logger import get_logger
from .database import init_db

logger = get_logger(__name__)

#log startup
env = os.getenv("ENV", "development")
port = int(os.getenv("PORT", 8000))
logger.info("Backend starting...")
logger.info(f"Environment: {env}")
logger.info(f"Port: {port}")

# Initialize the database structure
try:
    init_db()
    logger.info("Startup complete. Database connected and verified.")
except Exception as e:
    logger.critical(f"FATAL ERROR during startup: Could not initialize database. {e}")
    raise  # Raise to prevent app from starting if DB fails

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/health")
def health_check():
    try:
        logger.info("Health endpoint hit")
        response = {"status": "OK"}
        logger.info(f"Health check response status: 200")
        return response
    except Exception as e:
        logger.error(f"Error in health check: {e}")
        raise
