"""
This module serves as the entry point for the backend application.
"""
from fastapi import FastAPI

app = FastAPI()

@app.get("/healthcheck")
def healthcheck():
    """
    Health check endpoint
    """
    return {"status": "healthy"}

def main():
    """
    Entrypoint function
    """

if __name__ == "__main__":
    main()
