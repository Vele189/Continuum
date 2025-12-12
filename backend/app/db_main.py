# app/main.py

from .utils.logger import get_logger
from .database import init_db

# Get a module-specific logger instance for the main app
logger = get_logger("app") 

def start_application():
    """
    Main entry point for the Continuum application.
    Integrates DB initialization and centralized logging.
    """
    logger.info("Starting Continuum Backend Application...")
    
    try:
        # 1. Initialize the database structure
        init_db() 
        logger.info("Startup complete. Database connected and verified.")
    except Exception as e:
        logger.critical(f"FATAL ERROR during startup: Could not initialize database. {e}")
  
        return
    
    # --- Other startup logic would go here (e.g., API server start) ---
    logger.info("Continuum Backend is ready to serve requests.")


# Ensure the application starts when the file is executed
if __name__ == '__main__':
    start_application()

