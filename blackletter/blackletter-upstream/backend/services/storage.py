import logging
import uuid
from pathlib import Path
from typing import BinaryIO, Optional

import boto3
import magic
from botocore.exceptions import ClientError
from fastapi import HTTPException, UploadFile, status

from ..core.config import settings

logger = logging.getLogger(__name__)


class StorageService:
    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    async def validate_file(self, file: UploadFile) -> None:
        """Validate uploaded file for security and compliance."""

        # Check file size
        if hasattr(file.file, "seek") and hasattr(file.file, "tell"):
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning

            if file_size > settings.MAX_FILE_SIZE:
                raise HTTPException(
                    status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                    detail=f"File too large. Maximum size is {settings.MAX_FILE_SIZE} bytes.",
                )

        # Validate file type by content (magic numbers)
        file_content = await file.read()
        await file.seek(0)  # Reset file pointer

        mime_type = magic.from_buffer(file_content, mime=True)
        if mime_type not in settings.ALLOWED_FILE_TYPES:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File type {mime_type} not allowed. Allowed types: {settings.ALLOWED_FILE_TYPES}",
            )

        # Additional security: Check for malicious content patterns
        if b"<script" in file_content.lower() or b"javascript:" in file_content.lower():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="File contains potentially malicious content.",
            )

    async def save_file(self, file: UploadFile) -> tuple[str, int]:
        """
        Save uploaded file to S3 storage.
        Returns: (file_object_key, file_size)
        """
        await self.validate_file(file)

        # Generate secure, unique filename
        file_extension = Path(file.filename).suffix if file.filename else ""
        file_object_key = f"uploads/{uuid.uuid4().hex}{file_extension}"

        try:
            # Read file content
            file_content = await file.read()
            file_size = len(file_content)

            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=file_object_key,
                Body=file_content,
                ContentType=file.content_type,
                ServerSideEncryption="AES256",  # Enable encryption at rest
            )

            logger.info(f"File uploaded successfully: {file_object_key}")
            return file_object_key, file_size

        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to store file. Please try again.",
            )
        except Exception as e:
            logger.error(f"Unexpected error during file upload: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="An unexpected error occurred during file upload.",
            )

    async def get_file(self, file_object_key: str) -> bytes:
        """Retrieve file content from S3."""
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=file_object_key,
            )
            return response["Body"].read()
        except ClientError as e:
            logger.error(f"Failed to retrieve file from S3: {e}")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="File not found.",
            )

    async def delete_file(self, file_object_key: str) -> None:
        """Delete file from S3."""
        try:
            self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_object_key)
            logger.info(f"File deleted: {file_object_key}")
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")


# Create global storage service instance
storage_service = StorageService()
