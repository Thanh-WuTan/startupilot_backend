# service.py
from ...models.avatar_model import Avatar
from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

def create_avatar(file: UploadedFile) -> Avatar:
    """
    Create a new Avatar instance with the provided file.
    
    Args:
        file (UploadedFile): The file to be saved in the Avatar instance.
    
    Returns:
        Avatar: The created Avatar instance.
    """
    avatar = Avatar(avatar=file)
    avatar.save()  # Save the instance to trigger any custom save logic if needed
    return avatar

 