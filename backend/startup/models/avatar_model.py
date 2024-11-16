import uuid
from django.db import models

class Avatar(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to='avatar/')
     
    def __str__(self) -> str:
        return self.avatar.url if self.avatar else "No Image"