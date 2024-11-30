"""
This module serves as the entry point for the backend application.
"""
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app import config, controllers
from backend.app.utils.logging.filters.fastapi_healthcheck import FastAPIHealthCheckFilter

app = FastAPI()
app.summary = "Backend API for Nickelhack"

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
    logging.getLogger("uvicorn.access").addFilter(FastAPIHealthCheckFilter())

    origins = [
        "http://localhost",
        "http://0.0.0.0"
    ]

    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    controllers.add_controllers(app)

if __name__ == "backend.app.main":
    main()
