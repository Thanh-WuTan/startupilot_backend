import uuid
from django.db import models

from django.core.exceptions import ValidationError

class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    startup = models.ForeignKey('Startup', related_name='notes', on_delete=models.CASCADE)
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
        return f"Note for {self.startup.name} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"