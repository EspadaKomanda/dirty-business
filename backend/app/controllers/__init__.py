"""
Initializes all controllers.
"""
import logging
from fastapi import FastAPI
from .user import UserController

def add_controllers(app: FastAPI):
    """Add all controllers to the app."""

    @app.get("/healthcheck")
    def healthcheck():
        """
        Health check endpoint
        """
        return {"status": "healthy"}

    logging.info("Adding controllers...")
    app.include_router(UserController.create_router())
