"""
Storage controller for accessing S3 storage contents.
"""
from uuid import uuid4
from starlette.responses import FileResponse
from fastapi_controllers import Controller, get, post
from fastapi import UploadFile
from backend.app.services.s3 import S3Service

class StorageController(Controller):
    """
    Storage controller for accessing S3 storage contents.
    """
    tags=["Storage"]

    @post("/s3/{bucket}/{destination}", response_model=bool)
    def put_file(self, bucket: str, destination: str, file: UploadFile) -> bool:
        """
        Upload file to S3 storage.
        """
        temp_file = f"/tmp/{uuid4()}"
        with open(temp_file, "wb") as f:
            f.write(file.file.read())
        S3Service.upload(bucket, destination, temp_file)
        return True

    @get("/s3/{bucket}/{source}", response_class=FileResponse)
    def get_file(self, bucket: str, source: str) -> FileResponse:
        """
        Get file from S3 storage.
        """
        temp_file = f"/tmp/{uuid4()}"
        S3Service.download(bucket, source, temp_file)

        return FileResponse(temp_file, filename=source)
