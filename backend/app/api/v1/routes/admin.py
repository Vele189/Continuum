from fastapi import APIRouter, Depends

from app.api import deps
from app.dbmodels import User

router = APIRouter()


@router.get("/dashboard")
def admin_dashboard(
    current_user: User = Depends(deps.get_current_active_admin),
):
    """
    Get admin dashboard.

    Requires admin privileges (ADMIN or PROJECTMANAGER role).
    """
    return {
        "message": f"Welcome Admin {current_user.display_name}",
        "user_id": current_user.id,
        "role": current_user.role.value
    }
