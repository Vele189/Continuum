from typing import Any
from fastapi import APIRouter, Depends
from app.api import deps
from app.models.user import User

router = APIRouter()

@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(deps.get_current_active_admin),
) -> Any:
    """
    Get admin dashboard.
    """
    return {"message": f"Welcome Admin {current_user.email}"}
