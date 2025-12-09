# Main application entry point
from fastapi import FastAPI
from app.api.v1.routes import users

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix="/users", tags=["Users"])

@app.get("/health")
def health_check():
    return {"status": "OK"}
