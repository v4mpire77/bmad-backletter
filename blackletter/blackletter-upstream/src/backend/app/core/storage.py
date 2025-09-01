"""
Storage module for Blackletter Systems.

This module provides functionality for interacting with MinIO/S3 storage:
- Upload files
- Download files
- Generate signed URLs
- Manage buckets

Usage:
    from app.core.storage import get_storage_client, upload_file, download_file
    
    # Upload a file
    s3_key = await upload_file(file_data, "document.pdf", "contracts")
    
    # Download a file
    file_data = await download_file(s3_key)
    
    # Generate a signed URL
    url = generate_presigned_url(s3_key, expires_in=3600)
"""

import os
import io
import uuid
from typing import Dict, List, Optional, Tuple, Union, Any, BinaryIO
import logging
from datetime import datetime, timedelta

import boto3
from botocore.exceptions import ClientError
from fastapi import UploadFile

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment configuration
S3_ENDPOINT = os.getenv("S3_ENDPOINT", "http://localhost:9000")
S3_ACCESS_KEY = os.getenv("S3_ACCESS_KEY", "admin")
S3_SECRET_KEY = os.getenv("S3_SECRET_KEY", "adminadmin")
S3_BUCKET = os.getenv("S3_BUCKET", "blackletter")

# Client instance
_s3_client = None

def get_storage_client():
    """
    Get or initialize the S3 client.
    
    Returns:
        boto3.client: The S3 client
    """
    global _s3_client
    if _s3_client is None:
        _s3_client = boto3.client(
            's3',
            endpoint_url=S3_ENDPOINT,
            aws_access_key_id=S3_ACCESS_KEY,
            aws_secret_access_key=S3_SECRET_KEY,
            region_name='us-east-1',  # Doesn't matter for MinIO
        )
    return _s3_client

def ensure_bucket_exists(bucket_name: str = S3_BUCKET):
    """
    Ensure that the specified bucket exists, creating it if necessary.
    
    Args:
        bucket_name: Name of the bucket to check/create
        
    Returns:
        bool: True if the bucket exists or was created
    """
    client = get_storage_client()
    
    try:
        # Check if bucket exists
        client.head_bucket(Bucket=bucket_name)
        logger.info(f"Bucket {bucket_name} already exists")
        return True
    except ClientError as e:
        # If a 404 error, the bucket does not exist
        if e.response['Error']['Code'] == '404':
            try:
                # Create the bucket
                client.create_bucket(Bucket=bucket_name)
                logger.info(f"Created bucket {bucket_name}")
                return True
            except ClientError as create_error:
                logger.error(f"Error creating bucket: {str(create_error)}")
                raise
        else:
            logger.error(f"Error checking bucket: {str(e)}")
            raise

async def upload_file(
    file_data: Union[bytes, BinaryIO, UploadFile],
    filename: str,
    folder: str = "uploads",
    content_type: Optional[str] = None,
    metadata: Optional[Dict[str, str]] = None
) -> str:
    """
    Upload a file to S3 storage.
    
    Args:
        file_data: The file data as bytes, file-like object, or UploadFile
        filename: Original filename
        folder: Folder within the bucket
        content_type: MIME type of the file
        metadata: Additional metadata to store with the file
        
    Returns:
        str: The S3 key of the uploaded file
    """
    client = get_storage_client()
    ensure_bucket_exists()
    
    # Generate a unique filename to avoid collisions
    file_id = str(uuid.uuid4())
    extension = os.path.splitext(filename)[1]
    s3_key = f"{folder}/{file_id}{extension}"
    
    # Prepare extra args
    extra_args = {}
    if content_type:
        extra_args['ContentType'] = content_type
    
    if metadata:
        extra_args['Metadata'] = metadata
    
    try:
        # Handle different input types
        if isinstance(file_data, UploadFile):
            # For FastAPI UploadFile
            contents = await file_data.read()
            client.upload_fileobj(
                io.BytesIO(contents),
                S3_BUCKET,
                s3_key,
                ExtraArgs=extra_args
            )
        elif isinstance(file_data, bytes):
            # For bytes data
            client.upload_fileobj(
                io.BytesIO(file_data),
                S3_BUCKET,
                s3_key,
                ExtraArgs=extra_args
            )
        else:
            # For file-like objects
            client.upload_fileobj(
                file_data,
                S3_BUCKET,
                s3_key,
                ExtraArgs=extra_args
            )
        
        logger.info(f"Uploaded file to {s3_key}")
        return s3_key
    
    except ClientError as e:
        logger.error(f"Error uploading file: {str(e)}")
        raise

async def download_file(s3_key: str) -> bytes:
    """
    Download a file from S3 storage.
    
    Args:
        s3_key: The S3 key of the file
        
    Returns:
        bytes: The file data
    """
    client = get_storage_client()
    
    try:
        response = client.get_object(Bucket=S3_BUCKET, Key=s3_key)
        return response['Body'].read()
    
    except ClientError as e:
        logger.error(f"Error downloading file {s3_key}: {str(e)}")
        raise

def generate_presigned_url(
    s3_key: str,
    expires_in: int = 3600,
    bucket: str = S3_BUCKET
) -> str:
    """
    Generate a presigned URL for accessing a file.
    
    Args:
        s3_key: The S3 key of the file
        expires_in: Expiration time in seconds
        bucket: The S3 bucket name
        
    Returns:
        str: The presigned URL
    """
    client = get_storage_client()
    
    try:
        url = client.generate_presigned_url(
            'get_object',
            Params={'Bucket': bucket, 'Key': s3_key},
            ExpiresIn=expires_in
        )
        return url
    
    except ClientError as e:
        logger.error(f"Error generating presigned URL for {s3_key}: {str(e)}")
        raise

async def delete_file(s3_key: str, bucket: str = S3_BUCKET) -> bool:
    """
    Delete a file from S3 storage.
    
    Args:
        s3_key: The S3 key of the file
        bucket: The S3 bucket name
        
    Returns:
        bool: True if deletion was successful
    """
    client = get_storage_client()
    
    try:
        client.delete_object(Bucket=bucket, Key=s3_key)
        logger.info(f"Deleted file {s3_key}")
        return True
    
    except ClientError as e:
        logger.error(f"Error deleting file {s3_key}: {str(e)}")
        raise

async def list_files(
    prefix: str = "",
    bucket: str = S3_BUCKET,
    max_keys: int = 1000
) -> List[Dict[str, Any]]:
    """
    List files in the S3 bucket with the given prefix.
    
    Args:
        prefix: Prefix to filter files
        bucket: The S3 bucket name
        max_keys: Maximum number of keys to return
        
    Returns:
        List[Dict[str, Any]]: List of file information
    """
    client = get_storage_client()
    
    try:
        response = client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_keys
        )
        
        if 'Contents' not in response:
            return []
        
        return [
            {
                'key': item['Key'],
                'size': item['Size'],
                'last_modified': item['LastModified'].isoformat(),
                'etag': item['ETag'].strip('"')
            }
            for item in response['Contents']
        ]
    
    except ClientError as e:
        logger.error(f"Error listing files with prefix {prefix}: {str(e)}")
        raise
