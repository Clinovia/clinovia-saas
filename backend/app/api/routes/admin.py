# backend/app/api/routes/admin.py
"""
Admin routes (placeholder) for system management.

All routes are currently accessible without superuser checks.
Ready for future admin logic when enterprise clients or admins are added.
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from uuid import UUID

from app.api.deps import get_current_user
from app.db.session import get_db
from app.db.repositories.assessment_repository import AssessmentRepository
from app.db.repositories.user_repository import UserRepository
from app.db.models.assessments import AssessmentType

router = APIRouter(tags=["Admin"])


@router.get("/")
async def admin_root():
    """
    Admin API root endpoint (public for now).
    """
    return {"message": "Admin API", "status": "ok"}


@router.get("/stats")
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),  # Placeholder user
) -> Dict[str, Any]:
    """
    Get system-wide statistics (no auth for now).
    """
    assessment_repo = AssessmentRepository(db)
    user_repo = UserRepository(db)

    total_assessments = assessment_repo.count_all()

    assessments_by_type = {
        atype.value: (
            assessment_repo.db.query(assessment_repo.model)
            .filter(assessment_repo.model.type == atype)
            .count()
        )
        for atype in AssessmentType
    }

    active_users = user_repo.count_all()  # active_users count for now

    api_calls_today = 0  # placeholder

    return {
        "total_assessments": total_assessments,
        "assessments_by_type": assessments_by_type,
        "active_users": active_users,
        "api_calls_today": api_calls_today,
    }


@router.get("/protected")
async def admin_protected(
    current_user: str = Depends(get_current_user),
):
    """
    Protected admin endpoint (auth placeholder).
    """
    return {
        "message": "Admin protected area",
        "user_id": getattr(current_user, "id", None),
    }


@router.get("/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    List all users (no auth yet).
    """
    user_repo = UserRepository(db)
    users = user_repo.list_all()
    return {"users": users}


@router.post("/users/{user_id}/disable")
async def disable_user(
    user_id: UUID,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user),
):
    """
    Disable a user account (no auth yet).
    """
    user_repo = UserRepository(db)
    success = user_repo.disable_user(user_id)

    if not success:
        from fastapi import HTTPException, status

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found or already disabled",
        )

    return {"message": f"User {user_id} disabled successfully"}
