from django.db import models 

class StarUp(models.Model):
    name = models.CharField(max_length=200)  # Item name
    description = models.TextField(blank=True)  # Item description
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for updates

    def __str__(self):
        return self.name
