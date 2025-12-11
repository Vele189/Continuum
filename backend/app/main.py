# Main application entry point
import os
from fastapi import FastAPI
from app.api.v1.routes import users
from utils.logger import get_logger

logger = get_logger(__name__)

# Log startup
env = os.getenv("ENV", "development")
port = int(os.getenv("PORT", 8000))
logger.info("Backend starting...")
logger.info(f"Environment: {env}")
logger.info(f"Port: {port}")

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix="/users", tags=["Users"])

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
