# Main application entry point
import os

from app.api.v1.routes import (
    admin,
    auth,
    client_portal,
    clients,
    git_contributions,
    invoices,
    logged_hours,
    milestones,
    projects,
    repositories,
    task_attachments,
    task_comments,
    tasks,
    users,
    webhooks,
    work_sessions,
)
from app.core.config import settings
from app.utils.logger import get_logger
from fastapi import FastAPI

logger = get_logger(__name__)

# log startup
env = os.getenv("ENV", "development")
port = os.getenv("PORT", "8000")
logger.info("Backend starting...")
logger.info("Environment: %s", env)
logger.info("Port: %s", port)


app = FastAPI(title="Continuum API")

from fastapi.middleware.cors import CORSMiddleware

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["Tasks"])
app.include_router(
    logged_hours.router, prefix=f"{settings.API_V1_STR}/logged-hours", tags=["Logged Hours"]
)
app.include_router(
    logged_hours.aggregation_router, prefix=f"{settings.API_V1_STR}", tags=["Aggregations"]
)
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["Projects"])
app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["Clients"])
app.include_router(task_comments.router, prefix=f"{settings.API_V1_STR}", tags=["Task Comments"])
app.include_router(
    milestones.router, prefix=f"{settings.API_V1_STR}/milestones", tags=["Milestones"]
)
app.include_router(
    git_contributions.router,
    prefix=f"{settings.API_V1_STR}/git-contributions",
    tags=["Git Contributions"],
)
app.include_router(
    task_attachments.router, prefix=f"{settings.API_V1_STR}", tags=["Task Attachments"]
)
app.include_router(invoices.router, prefix=f"{settings.API_V1_STR}/invoices", tags=["Invoices"])
app.include_router(repositories.router, prefix=f"{settings.API_V1_STR}", tags=["Repositories"])
app.include_router(
    client_portal.router, prefix=f"{settings.API_V1_STR}/client-portal", tags=["Client Portal"]
)
app.include_router(webhooks.router, prefix=f"{settings.API_V1_STR}/webhooks", tags=["Webhooks"])
app.include_router(
    work_sessions.router, prefix=f"{settings.API_V1_STR}/work-sessions", tags=["Work Sessions"]
)


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
