import uuid
from django.db import models
 
class Batch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        verbose_name = 'Batch'  # Singular name for the model
        verbose_name_plural = 'Batches'  # Plural name for the model
    def __str__(self) -> str:
        return self.name