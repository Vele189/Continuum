# Main application entry point
import os
from fastapi import FastAPI
from app.api.v1.routes import (
    users, auth, admin, tasks, logged_hours, projects, clients, task_comments,
    git_contributions, task_attachments, invoices, milestones
)
from app.core.config import settings
from app.utils.logger import get_logger


logger = get_logger(__name__)

#log startup
env = os.getenv("ENV", "development")
port = os.getenv("PORT", "8000")
logger.info("Backend starting...")
logger.info("Environment: %s", env)
logger.info("Port: %s", port)


app = FastAPI(title="Continuum API")
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["Users"])
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["Auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["Admin"])
app.include_router(tasks.router, prefix=f"{settings.API_V1_STR}/tasks", tags=["Tasks"])
app.include_router(
    logged_hours.router,
    prefix=f"{settings.API_V1_STR}/logged-hours",
    tags=["Logged Hours"]
)
app.include_router(
    logged_hours.aggregation_router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Aggregations"]
)
app.include_router(projects.router, prefix=f"{settings.API_V1_STR}/projects", tags=["Projects"])
app.include_router(clients.router, prefix=f"{settings.API_V1_STR}/clients", tags=["Clients"])
app.include_router(task_comments.router, prefix=f"{settings.API_V1_STR}", tags=["Task Comments"])
app.include_router(milestones.router, prefix=f"{settings.API_V1_STR}/milestones", tags=["Milestones"])
app.include_router(
    git_contributions.router,
    prefix=f"{settings.API_V1_STR}/git-contributions",
    tags=["Git Contributions"]
)
app.include_router(
    task_attachments.router,
    prefix=f"{settings.API_V1_STR}",
    tags=["Task Attachments"]
)
app.include_router(invoices.router, prefix=f"{settings.API_V1_STR}/invoices", tags=["Invoices"])

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
