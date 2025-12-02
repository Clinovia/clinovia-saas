# app/core/middleware/request_id_middleware.py
import uuid
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from typing import Callable


class RequestIDMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Get request ID from header or generate new one
        request_id = request.headers.get("x-request-id") or str(uuid.uuid4())
        
        # Add to request state (optional)
        request.state.request_id = request_id
        
        # Process request
        response = await call_next(request)
        
        # Add to response headers
        response.headers["x-request-id"] = request_id
        return response