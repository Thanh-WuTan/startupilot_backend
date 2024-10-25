
from rest_framework import serializers
from ...models import Startup, Category, Founder, Batch

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class FounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = ['id', 'first_name', 'last_name', 'email']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']

class StartupSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)
    founders = FounderSerializer(many=True)
    batch = BatchSerializer(many=False)

    class Meta:
        model = Startup
        fields = ['id', 'name', 'short_description', 'description', 'phase', 'status', 'contact_email', 'linkedin_url', 
                  'facebook_url', 'categories', 'founders', 'batch', 'pitch_deck', 'priority']