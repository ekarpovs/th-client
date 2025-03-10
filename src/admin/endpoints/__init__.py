# app/endpoints/__init__.py
from .pages import router as pages_router
from .auth import router as auth_router
from .dashboard import router as dash_router

__all__ = ["pages_router", "dash_router", "auth_router"]