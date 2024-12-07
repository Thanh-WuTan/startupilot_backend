import uuid
from django.db import models

from .phase_model import Phase
from .status_model import Status
from .priority_model import Priority
from .category_model import Category
from .person_model import Person
from .batch_model import Batch
from .advisor_model import Advisor


class Startup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)
    short_description = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    category = models.ForeignKey(Category, related_name="startups", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.ForeignKey(Status, related_name="startups", on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.ForeignKey(Priority, related_name="startups", on_delete=models.SET_NULL, null=True, blank=True)
    phases = models.ManyToManyField(Phase, related_name="startups", null=True, blank=True)
    batch = models.ForeignKey(Batch, related_name="startups", on_delete=models.CASCADE, null=True, blank=True)
    launch_date = models.DateField(null=True, blank=True)
    members = models.ManyToManyField(Person, through='StartupMembership', related_name='startups')
    advisors = models.ManyToManyField(Advisor, related_name="startups", blank=True)
    pitch_deck = models.URLField(null=True, blank=True)
    avatar = models.URLField(null=True, blank=True)

    @property
    def all_notes(self):
        return self.notes.all()
    
    def __str__(self):
        return self.name