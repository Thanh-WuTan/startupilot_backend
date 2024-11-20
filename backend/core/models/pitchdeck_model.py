import uuid
from django.db import models  

class Pitchdeck(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pitchdeck_url = models.URLField(null=True, blank=True)
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.pitchdeck_url if self.pitchdeck_url else "No URL File"