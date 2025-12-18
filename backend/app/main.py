# Main application entry point
import os
from fastapi import FastAPI
from app.api.v1.routes import users, auth, admin, logged_hours, clients
from app.core.config import settings
from app.utils.logger import get_logger
from .database import init_db

logger = get_logger(__name__)

#log startup
env = os.getenv("ENV", "development")
port = os.getenv("PORT", "8000")
logger.info("Backend starting...")
logger.info("Environment: %s", env)
logger.info("Port: %s", port)

# Initialize the database structure
try:
    init_db()
    logger.info("Startup complete. Database connected and verified.")
except Exception as e:
    logger.critical("FATAL ERROR during startup: Could not initialize database. %s", e)
    raise  # Raise to prevent app from starting if DB fails

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(
    logged_hours.router,
    prefix=f"{settings.API_V1_STR}/logged-hours",
    tags=["Logged Hours"]
)
app.include_router(
    logged_hours.aggregation_router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Aggregations"]
)
app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["Clients"])

@app.get("/health")
def health_check():
    try:
        logger.info("Health endpoint hit")
        response = {"status": "OK"}
        logger.info("Health check response status: 200")
        return response
    except Exception as e:
        logger.error("Error in health check: %s", e)
        raise
