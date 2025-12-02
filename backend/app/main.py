"""
Main FastAPI application entry point.
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables safely
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # In testing or when .env doesn't exist

from app.core.middleware.request_id_middleware import RequestIDMiddleware
from app.core.config import settings
from app.core.middleware.error_handling_middleware import ErrorHandlingMiddleware

# Import routers
from app.api.routes import (
    admin,
    alzheimer,
    analytics,
    api_keys,
    billing,
    cardiology,
    health,
    history,
    auth,
    payments,
    users,
)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Middleware setup ---
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlingMiddleware)

# --- Router includes ---
app.include_router(auth.router, prefix=f"{settings.API_V1_STR}/auth", tags=["auth"])
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(alzheimer.router, prefix=f"{settings.API_V1_STR}/alzheimer", tags=["alzheimer"])
app.include_router(analytics.router, prefix=f"{settings.API_V1_STR}/analytics", tags=["analytics"])
app.include_router(api_keys.router, prefix=f"{settings.API_V1_STR}/api-keys", tags=["api_keys"])
# app.include_router(assessments.router, prefix=f"{settings.API_V1_STR}/assessments", tags=["assessments"])
app.include_router(billing.router, prefix=f"{settings.API_V1_STR}/billing", tags=["billing"])
app.include_router(cardiology.router, prefix=f"{settings.API_V1_STR}/cardiology", tags=["cardiology"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(history.router, prefix=f"{settings.API_V1_STR}/history", tags=["history"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["payments"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

# --- Root endpoints ---
@app.get("/")
def root():
    return {"message": "Clinovia SaaS API", "version": "1.0.0"}


@app.get("/health")
def health():
    return {"status": "healthy"}

# --- Lambda adapter ---
try:
    from mangum import Mangum
    handler = Mangum(app)  # This is the entrypoint Lambda will use
except ImportError:
    handler = None  # Mangum not installed locally; safe for dev