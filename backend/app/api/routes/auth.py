from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from pydantic import ValidationError

from app.db.session import get_db
from app.schemas.auth import Token
from app.schemas.users import UserCreate, UserLogin, UserRead
from app.api.deps import CurrentUserDep
from app.services.users.user_service import UserService

router = APIRouter(tags=["Authentication"])


@router.post("/signup", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def signup_user(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> UserRead:
    """
    Register a new user. If email exists but is inactive, raises error.
    """
    user_service = UserService(db)
    try:
        return user_service.create_user(user_in)
    except ValueError as e:
        # Log the actual error for debugging
        print(f"ValueError during signup: {str(e)}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    except ValidationError as e:
        # Catch Pydantic validation errors
        print(f"ValidationError during signup: {e.json()}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=e.errors()
        )
    except Exception as e:
        # Catch any other unexpected errors
        print(f"Unexpected error during signup: {type(e).__name__}: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during signup"
        )


@router.post("/login", response_model=Token)
def login_user(
    db: Session = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    OAuth2-compatible login endpoint.
    """
    user_service = UserService(db)
    credentials = UserLogin(email=form_data.username, password=form_data.password)
    token = user_service.authenticate_and_create_token(credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.post("/login/email", response_model=Token)
def login_with_email(
    *,
    db: Session = Depends(get_db),
    email: str = Body(...),
    password: str = Body(...),
) -> Token:
    """
    Alternative login using JSON body (useful for mobile or SPA).
    """
    user_service = UserService(db)
    credentials = UserLogin(email=email, password=password)
    token = user_service.authenticate_and_create_token(credentials)
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return token


@router.get("/me", response_model=UserRead)
def read_current_user(current_user: CurrentUserDep) -> UserRead:
    """
    Retrieve the currently authenticated user.
    """
    return current_user