from rest_framework import serializers
from ...models import Founder, Startup

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = ['id', 'name', 'short_description', 'description', 'phase', 'status', 'contact_email', 'linkedin_url', 
                  'facebook_url', 'categories', 'founders', 'batch', 'pitch_deck', 'priority']

class FounderSerializer(serializers.ModelSerializer):
    startups = StartupSerializer(many=True, read_only=True)

    class Meta:
        model = Founder
        fields = ['id', 'first_name', 'last_name', 'email', 'startups']
