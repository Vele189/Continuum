# Main application entry point
from fastapi import FastAPI
from app.api.v1.routes import users, auth

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(auth.router, prefix="/auth", tags=["Auth"])

@app.get("/health")
def health_check():
    return {"status": "OK"}
