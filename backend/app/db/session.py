# Database session management
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

logger = logging.getLogger(__name__)

DATABASE_URL = os.environ.get("DATABASE_URL")
if not DATABASE_URL:
    logger.warning("DATABASE_URL is not set. Database features will not work.")
    # Create a dummy engine to prevent import errors
    # This allows the app to start even if DATABASE_URL is missing
    engine = None
    SessionLocal = None
else:
    try:
        engine = create_engine(DATABASE_URL, pool_pre_ping=True)
        SessionLocal = sessionmaker(
            autocommit=False, autoflush=False, bind=engine
        )  # pylint: disable=invalid-name
    except Exception as e:
        logger.error("Failed to create database engine: %s", e)
        engine = None
        SessionLocal = None
