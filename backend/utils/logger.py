import logging

# Configure logging one time for the whole backend
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(asctime)s | [%(name)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

def get_logger(name: str):
    """
    Returns a logger configured with the global settings.
    """
    return logging.getLogger(name)
