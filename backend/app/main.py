"""
This module serves as the entry point for the backend application.
"""
import logging
from fastapi import FastAPI
from backend.app import config, controllers

app = FastAPI()

def main():
    """
    Entrypoint function
    """
    # Logging setup
    logging.basicConfig(
        level=logging.DEBUG if config.ENVIRONMENT_TYPE == "development" else logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()  # Log to console
        ]
    )

    controllers.add_controllers(app)

if __name__ == "backend.app.main":
    main()
