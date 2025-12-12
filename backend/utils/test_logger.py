import logger
from fastapi import FastAPI
import os


logger = logger.get_logger(__name__)
app = FastAPI()

ENV = os.getenv("ENV", "development")
PORT = os.getenv("PORT", 8000)

logger.info(f"Environment: {ENV}")
logger.info(f"Server port: {PORT}")



@app.get("/")
def read():
    logger.info("Received request at root endpoint.")
    return {"Hello": "World"}



def test_logging():
    """
    Test function to demonstrate logging.
    """
    logger.info("Starting backend.....")


if __name__ == "__main__":
    test_logging()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0",port=8000)
    