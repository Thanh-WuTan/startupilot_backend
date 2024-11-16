import uuid
from django.db import models

class Person(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=15, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    shorthand = models.CharField(unique=True, max_length=510, null=True, blank=True)
    
    def save(self, *args, **kwargs):
        if self.email: 
            self.shorthand = f"{self.name}({self.email})"
        else:
            self.shorthand = self.name  
        super().save(*args, **kwargs)  

    class Meta:
        unique_together = (('name', 'email'),) 
    def __str__(self):
        return self.name 