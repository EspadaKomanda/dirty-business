"""
Initializes all controllers.
"""
import logging
from fastapi import FastAPI
from .user import UserController
from .auth import AuthController
from .camera import CameraController
from .storage import StorageController

def add_controllers(app: FastAPI):
    """Add all controllers to the app."""

    @app.get("/healthcheck", tags=["System"])
    def healthcheck():
        """
        Used by Docker for healthcheck capabilities.
        """
        return "healthy"

    logging.info("Adding controllers...")
    app.include_router(UserController.create_router())
    app.include_router(AuthController.create_router())
    app.include_router(CameraController.create_router())
    app.include_router(StorageController.create_router())
