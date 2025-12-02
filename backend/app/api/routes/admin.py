# backend/app/api/routes/admin.py
"""
Admin-only routes for system management.

Provides endpoints for:
- System statistics and monitoring
- User management
- Admin-protected areas
"""

from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.deps import get_current_superuser  # ← Import function, not Annotated type
from app.db.session import get_db
from app.db.models.users import User
from app.db.models.assessments import AssessmentType
from app.db.repositories.assessment_repository import AssessmentRepository
from app.db.repositories.user_repository import UserRepository

router = APIRouter(tags=["Admin"])


@router.get("/")
async def admin_root():
    """
    Admin API root endpoint.
    
    Returns basic status information. Public endpoint for health checks.
    """
    return {"message": "Admin API", "status": "ok"}


@router.get("/stats")
async def get_system_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),  # ← Use function
) -> Dict[str, Any]:
    """
    Get system-wide statistics (admin only).
    
    Returns:
        - total_assessments: Total number of assessments in the system
        - assessments_by_type: Breakdown of assessments by type
        - active_users: Number of active users
        - api_calls_today: API usage metrics (placeholder)
    
    Raises:
        HTTPException: 403 if user is not a superuser
    """
    assessment_repo = AssessmentRepository(db)
    user_repo = UserRepository(db)

    # Total assessments
    total_assessments = assessment_repo.count_all()

    # Count by assessment type
    assessments_by_type = {
        atype.value: (
            assessment_repo.db.query(assessment_repo.model)
            .filter(assessment_repo.model.type == atype)
            .count()
        )
        for atype in AssessmentType
    }

    # Active users count
    active_users = user_repo.count_active()

    # Placeholder for future analytics implementation
    api_calls_today = 0

    return {
        "total_assessments": total_assessments,
        "assessments_by_type": assessments_by_type,
        "active_users": active_users,
        "api_calls_today": api_calls_today,
    }


@router.get("/protected")
async def admin_protected(
    current_user: User = Depends(get_current_superuser),  # ← Use function
):
    """
    Protected admin endpoint for testing authentication.
    
    Returns information about the authenticated admin user.
    
    Raises:
        HTTPException: 403 if user is not a superuser
    """
    return {
        "message": "Admin protected area",
        "user_id": current_user.id,
    }


@router.get("/users")
async def list_users(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),  # ← Use function
):
    """
    List all users in the system (admin only).
    
    Returns a list of all registered users with their basic information.
    
    Raises:
        HTTPException: 403 if user is not a superuser
    """
    user_repo = UserRepository(db)
    users = user_repo.list_all()
    return {"users": users}


@router.post("/users/{user_id}/disable")
async def disable_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_superuser),  # ← Use function
):
    """
    Disable a user account (admin only).
    
    Args:
        user_id: ID of the user to disable
    
    Returns:
        Success message with user ID
    
    Raises:
        HTTPException: 404 if user not found or already disabled
        HTTPException: 403 if user is not a superuser
    """
    user_repo = UserRepository(db)
    success = user_repo.disable_user(user_id)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User {user_id} not found or already disabled",
        )
    
    return {"message": f"User {user_id} disabled successfully"}