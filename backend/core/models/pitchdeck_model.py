import uuid
from django.db import models  

class Pitchdeck(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pitchdeck = models.FileField(upload_to='pitchdecks/')
     
    def __str__(self) -> str:
        return self.pitchdeck.url if self.pitchdeck else "No File"

     