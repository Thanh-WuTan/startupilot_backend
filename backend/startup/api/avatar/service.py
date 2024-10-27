# service.py
from ...models import Avatar
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

def get_avatar_by_url(avatar_url):
    """
    Retrieve an Avatar instance based on the provided URL.
    """
    try:
        return Avatar.objects.get(name=avatar_url)
    except ObjectDoesNotExist:
        raise ValidationError({"avatar": "Avatar with the specified URL does not exist."})
    
