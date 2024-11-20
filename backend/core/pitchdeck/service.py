import random
import string
import os

from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import ValidationError
from minio import Minio, S3Error

from ..models.pitchdeck_model import Pitchdeck

def generate_random_string(length=20) -> str:
    """_summary_

    Args:
        length (int, optional): _description_. Defaults to 20.

    Returns:
        _type_: _description_
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

minio_client = Minio(
    endpoint=os.getenv("MINIO_URL", "localhost:9000"),
    access_key=os.getenv("MINIO_ACCESS_KEY", "none"),
    secret_key=os.getenv("MINIO_SECRET_KEY", "none"),
    secure=False if os.getenv("DEBUG", "True") == "True" else True,
)

BUCKET_NAME = os.getenv("MINIO_BUCKET_NAME", "notset")
FOLDER_NAME = "pitchdecks"


def upload_pitchdeck(file: UploadedFile):
    """
    Upload a new pitchdeck file to minio and create a new Pitchdeck instance.
    
    Args:
        file (UploadedFile): The file to be saved in the Pitchdeck instance.
    
    Returns:
        Pitchdeck: The created Pitchdeck instance.
    """
    if not minio_client.bucket_exists(BUCKET_NAME):
        raise ValidationError("Bucket does not exist.")
    
    file.name = f"{generate_random_string()}_pitchdeck_{file.name}"
    try:
        minio_client.put_object(
            bucket_name=BUCKET_NAME,
            object_name=f"{FOLDER_NAME}/{file.name}",
            content_type=file.content_type,
            data=file,
            length=file.size,
        )
    except S3Error as e:
        raise ValidationError(f"S3Error uploading file: {str(e)}")
    except Exception as e:
        raise ValidationError(f"Error uploading file: {str(e)}")
    # This part should set presigned URL to the pitchdeck_url field     
    pitchdeck = Pitchdeck(pitchdeck_url=f"{os.getenv('MINIO_URL', 'localhost:9000')}/{BUCKET_NAME}/{FOLDER_NAME}/{file.name}")
    pitchdeck.save()  # This will trigger the save method to set the name field to the URL
    return pitchdeck

