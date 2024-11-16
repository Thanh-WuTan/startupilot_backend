import uuid
from django.db import models

class Priority(models.Model):
    name = models.CharField(max_length=50, unique=True)
    def __str__(self):
        return self.name