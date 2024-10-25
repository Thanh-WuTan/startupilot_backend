import uuid
from django.db import models

class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Founder(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Batch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Startup(models.Model):
    PHASE_CHOICES = [
        ('brainstorming', 'Brainstorming'),
        ('fundraising', 'Fundraising'),
        ('scaling', 'Scaling'),
        ('established', 'Established'),
    ]

    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]

    PRIORITY_CHOICES = [
        ('P0', 'P0'),
        ('P1', 'P1'),
    ]


    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    short_description = models.TextField(max_length=500, null=True, blank=True)
    description = models.TextField(max_length=10000, null=True, blank=True)
    phase = models.CharField(max_length=50, choices=PHASE_CHOICES, null=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, null=True, blank=True)
    priority = models.CharField(max_length=50, choices=PRIORITY_CHOICES, null=True, blank=True)
    contact_email = models.EmailField(unique=True, null=True, blank=True)
    linkedin_url = models.URLField(null=True, blank=True)
    facebook_url = models.URLField(null=True, blank=True)
    categories = models.ManyToManyField(Category, related_name="startups", null=True, blank=True)
    founders = models.ManyToManyField(Founder, related_name="startups", null=True, blank=True)
    batch = models.ForeignKey(Batch, related_name="startups", on_delete=models.CASCADE, null=True, blank=True)
    pitch_deck = models.FileField(upload_to='pitchdecks/', null=True, blank=True)
    def __str__(self):
        return self.name
