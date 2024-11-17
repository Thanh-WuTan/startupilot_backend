import uuid

from django.db import models

class Phase(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Phase'
        verbose_name_plural = 'Phases'

    def __str__(self):
        return self.name