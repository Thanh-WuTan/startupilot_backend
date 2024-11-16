import uuid
from django.db import models

from .startup_model import Startup
from .person_model import Person
from .role_model import Role

class StartupMembership(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    startup = models.ForeignKey(Startup, on_delete=models.CASCADE)
    roles = models.ManyToManyField(Role, null=True, blank=True)

    def __str__(self):
        return f"{self.person.name} at {self.startup.name}"