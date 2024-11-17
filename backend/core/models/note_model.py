import uuid
from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from .startup_model import Startup
from .person_model import Person

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)  # Links to either Startup or Person model
    object_id = models.UUIDField()  # The ID of the related object (either a startup or a person) with UUID type
    content_object = GenericForeignKey('content_type', 'object_id')  # Generic relationship to either startup or person

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        word_limit = 10000 
        word_count = len(self.content.split())
        if word_count > word_limit:
            raise ValidationError(f'Content exceeds the word limit of {word_limit} words. Current word count: {word_count}.')

    def save(self, *args, **kwargs):
        self.full_clean()  # Ensures `clean()` is called before saving
        super().save(*args, **kwargs)

    def __str__(self):
        if isinstance(self.content_object, Startup):
            return f"Note for {self.content_object.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        elif isinstance(self.content_object, Person):
            return f"Note for {self.content_object.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
        return f"Note for {self.content_object} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"