import uuid
from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    
    class Meta:
        verbose_name = 'Category'  # Singular name for the model
        verbose_name_plural = 'Categories'  # Plural name for the model
    
    def __str__(self):
        return self.name