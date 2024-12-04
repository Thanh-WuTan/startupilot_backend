import uuid
from django.db import models

from .startup_model import Startup
from .person_model import Person 

class StartupMembership(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    role = models.CharField(max_length=100, null=True, blank=True)
    status = models.BooleanField(default=True)
    def __str__(self):
        return f"{self.person.name} at {self.startup.name}" 