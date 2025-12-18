# backend/app/main.py
"""
Main FastAPI application entry point.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass  # Safe if .env doesn't exist

# --- App core imports ---
from app.core.config import settings
from app.core.middleware.request_id_middleware import RequestIDMiddleware
from app.core.middleware.error_handling_middleware import ErrorHandlingMiddleware

# --- Routers ---
from app.api.routes import (
    admin,
    alzheimer,
    cardiology,
    health,
    history,
    payments,
    users,
)

# --- Logging setup ---
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- FastAPI app instance ---
app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# --- Middleware ---
app.add_middleware(RequestIDMiddleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(ErrorHandlingMiddleware)

# --- Router registration ---
app.include_router(admin.router, prefix=f"{settings.API_V1_STR}/admin", tags=["admin"])
app.include_router(alzheimer.router, prefix=f"{settings.API_V1_STR}/alzheimer", tags=["alzheimer"])
app.include_router(cardiology.router, prefix=f"{settings.API_V1_STR}/cardiology", tags=["cardiology"])
app.include_router(health.router, prefix=f"{settings.API_V1_STR}/health", tags=["health"])
app.include_router(history.router, prefix=f"{settings.API_V1_STR}/history", tags=["history"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["payments"])
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])

# --- Startup event ---
@app.on_event("startup")
async def startup_event():
    logger.info("🚀 Application startup initiated")
    logger.info("✅ Application startup complete")

# --- Basic endpoints ---
@app.get("/")
def root():
    logger.info("Root endpoint called")
    return {"message": "Clinovia SaaS API", "version": "1.0.0"}

@app.get("/health")
def health():
    logger.info("Health check endpoint called")
    return {"status": "healthy"}

# --- Test endpoint for cardiology ---
@app.get(f"{settings.API_V1_STR}/cardiology/test")
def test_cardiology():
    logger.info("Cardiology test endpoint called")
    return {"message": "Cardiology router is working!"}

# --- Lambda adapter ---
try:
    from mangum import Mangum
    handler = Mangum(app)
except ImportError:
    handler = None
