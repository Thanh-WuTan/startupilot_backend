from django.core.files.uploadedfile import UploadedFile
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import ValidationError

from ...models.pitchdeck_model import Pitchdeck

def create_pitchdeck(file: UploadedFile):
    """
    Create a new Pitchdeck instance with the provided file.
    
    Args:
        file (UploadedFile): The file to be saved in the Pitchdeck instance.
    
    Returns:
        Pitchdeck: The created Pitchdeck instance.
    """
    pitchdeck = Pitchdeck(pitchdeck=file)
    pitchdeck.save()  # This will trigger the save method to set the name field to the URL
    return pitchdeck

