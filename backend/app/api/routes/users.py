from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.session import get_db
from app.api.deps import get_current_active_user, get_current_superuser
from app.schemas.users import UserCreate, UserRead, UserUpdate, UserMeUpdate
from app.schemas.auth import SignUpResponse
from app.db.models.users import User
from app.services.users.user_service import UserService

router = APIRouter(tags=["users"])

# --- Public: Signup (no auth required) ---
@router.post(
    "/signup",
    response_model=SignUpResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user"
)
async def signup(
    user_in: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    existing_user = await user_service.get_by_email(user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    user = await user_service.create(user_in)
    return SignUpResponse(user=UserRead.model_validate(user))

# --- Authenticated: Current user profile ---
@router.get("/me", response_model=UserRead, summary="Get current user")
async def read_me(
    current_user: User = Depends(get_current_active_user)
):
    return current_user


@router.put("/me", response_model=UserRead, summary="Update current user profile")
async def update_me(
    user_update: UserMeUpdate,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    updated_user = await user_service.update(
        user_id=current_user.id,
        user_update=user_update
    )
    return updated_user

# --- Admin-only: Full user management ---
@router.get(
    "/",
    response_model=List[UserRead],
    dependencies=[Depends(get_current_superuser)],
    summary="List all users (admin only)"
)
async def list_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    users = await user_service.get_multi(skip=skip, limit=limit)
    return users


@router.get(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_superuser)],
    summary="Get a specific user (admin only)"
)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    return user


@router.put(
    "/{user_id}",
    response_model=UserRead,
    dependencies=[Depends(get_current_superuser)],
    summary="Update any user (admin only)"
)
async def update_user(
    user_id: int,
    user_update: UserUpdate,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    updated_user = await user_service.update(user_id=user_id, user_update=user_update)
    return updated_user


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    dependencies=[Depends(get_current_superuser)],
    summary="Deactivate or delete a user (admin only)"
)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get(user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    await user_service.delete(user_id)
    return
