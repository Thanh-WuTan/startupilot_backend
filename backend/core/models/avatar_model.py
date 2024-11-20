import uuid
from django.db import models

class Avatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar_url = models.URLField(null=True, blank=True)
     
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.avatar_url if self.avatar_url else "No URL File"