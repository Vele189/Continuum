import logging

from app.db.base import Base
from app.db.session import SessionLocal, engine

try:
    from utils.logger import get_logger
except ImportError:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s | [%(name)s] %(message)s")

    def get_logger(name: str):
        return logging.getLogger(name)


logger = get_logger(__name__)


def init_db():
    if engine is None:
        logger.error("Cannot initialize database: engine is None (DATABASE_URL not set)")
        raise RuntimeError("Database engine is not available. DATABASE_URL must be set.")
    logger.info("Starting database initialization process.")
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error("FATAL DB ERROR: Could not complete schema creation: %s", e, exc_info=True)
        raise e


def get_db():
    if SessionLocal is None:
        raise RuntimeError(
            "Database is not configured. Please set DATABASE_URL environment variable."
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
