import random
import string
import os
import re

from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from minio import Minio, S3Error

minio_client = Minio(
    endpoint=os.getenv("MINIO_URL", "localhost:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "none"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "none"),
    secure=False if os.getenv("DEBUG", "True") == "True" else True,
)

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "notset")
FOLDER_NAME = "avatars"

def sanitize_filename(filename: str) -> str:
    """
    Remove all characters from the filename except a-z, A-Z, 0-9, and _.
    
    Args:
        filename (str): The original filename.
    
    Returns:
        str: The sanitized filename.
    """
    return re.sub(r'[^a-zA-Z0-9_.]', '',filename)

def generate_random_string(length=20) -> str:
    """_summary_

    Args:
        length (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


def upload_file(file, file_type, filename):
    """
    Upload the file to MinIO and return the file URL.
    """
    try:
        # Create the file path in the bucket
        file_path = f"{file_type}/{filename}"

        # Upload the file to MinIO
        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=file_path, 
            content_type=file.content_type,
            data=file,
            length=file.size
        )

        # Return the file URL
        minio_url = os.getenv('FILE_MINIO_URL', 'http://localhost:9000')  # Default to 'http://minio_server:9000' if the environment variable is not set

        # Construct the file URL
        file_url = f"{minio_url}/{BUCKET_NAME}/{file_path}"
        return file_url

    except S3Error as e:
        raise Exception(f"Error uploading file to MinIO: {e}")
    except Exception as e:
        raise ValidationError(f"Error uploading file: {str(e)}")
 