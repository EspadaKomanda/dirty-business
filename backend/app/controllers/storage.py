"""
Storage controller for accessing S3 storage contents.
"""
import logging
from typing import Annotated
from uuid import uuid4
from starlette.responses import FileResponse
from fastapi_controllers import Controller, get, post
from fastapi import UploadFile, Depends
from backend.app.services.s3 import S3Service
from backend.app.services.auth import AuthService
from backend.app.dtos.auth_service.dtos import UserAccount

logger = logging.getLogger(__name__)

class StorageController(Controller):
    """
    Storage controller for accessing S3 storage contents.
    """
    tags=["Storage"]

    @post("/s3/{bucket}/{destination}", response_model=bool)
    def put_file(self, bucket: str, destination: str, file: UploadFile,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]
    ) -> bool:
        """
        Upload file to S3 storage.
        """
        logger.info(
            "User %s is uploading file %s to bucket %s",
            user.username, file.filename, bucket
         )

        temp_file = f"/tmp/{uuid4()}"
        with open(temp_file, "wb") as f:
            f.write(file.file.read())
        S3Service.upload(bucket, destination, temp_file)
        return True

    @get("/s3/{bucket}/{source}", response_class=FileResponse)
    def get_file(self, bucket: str, source: str,
        user: Annotated[UserAccount, Depends(AuthService.authenticate)]) -> FileResponse:
        """
        Get file from S3 storage.
        """
        logger.info(
            "User %s is downloading file %s from bucket %s",
            user.username, source, bucket
         )

        temp_file = f"/tmp/{uuid4()}"
        S3Service.download(bucket, source, temp_file)

        return FileResponse(temp_file, filename=source)
