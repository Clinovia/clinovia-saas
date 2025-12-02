from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.api import deps
from app.db.models.users import User
from app.db.models.api_keys import APIKey  # Added missing import
from app.services.api_key_service import APIKeyService

router = APIRouter(tags=["API Keys"])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_api_key(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """Create a new API key for the current user."""
    service = APIKeyService(db)  # Instantiate service
    key = service.create_api_key(current_user)
    return {"api_key": key}


@router.get("")
def list_api_keys(
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> List[dict]:
    """List all API keys for the current user."""
    service = APIKeyService(db)  # Instantiate service
    keys = service.get_user_keys(current_user)
    return [
        {
            "id": key.id,
            "key_preview": f"{key.key[:8]}...",  # Don't expose full key
            "usage_count": key.usage_count,
            "created_at": key.created_at,
            "last_used_at": key.last_used_at,
            "is_active": key.is_active,  # Added missing field
        }
        for key in keys
    ]


@router.delete("/{key_id}")
def revoke_api_key(
    key_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """Revoke an API key."""
    service = APIKeyService(db)  # Instantiate service
    success = service.revoke_key(key_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found or already revoked",
        )
    return {"status": "revoked", "id": key_id}


@router.get("/{key_id}/usage")
def get_api_key_usage(
    key_id: int,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_user),
) -> dict:
    """Get usage statistics for a specific API key."""
    # First check if key exists
    key = db.query(APIKey).filter(APIKey.id == key_id).first()
    
    if not key:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found",
        )
    
    # Then check if user owns the key
    if key.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this API key",
        )
    
    return {
        "id": key.id,
        "usage_count": key.usage_count,
        "last_used_at": key.last_used_at,
        "is_active": key.is_active,
    }