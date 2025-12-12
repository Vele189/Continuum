# Main application entry point
from fastapi import FastAPI
from app.api.v1.routes import users, auth, admin
from app.core.config import settings
from app.db.base import Base
from app.db.session import engine

from app.models import user as user_model

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])

@app.get("/health")
def health_check():
    return {"status": "OK"}
