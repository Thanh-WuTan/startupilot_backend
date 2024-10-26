from rest_framework import serializers
from ...models import Startup, Category, Founder, Batch

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class FounderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Founder
        fields = ['id', 'name', 'email']

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']

class StartupSerializer(serializers.ModelSerializer):
    founders = serializers.SlugRelatedField(
        many=True, 
        slug_field='shorthand', 
        queryset=Founder.objects.all(),
        required=False
    )
    categories = serializers.SlugRelatedField(
        many=True, 
        slug_field='name', 
        queryset=Category.objects.all(),
        required=False
    )

    batch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Batch.objects.all(),
        required=False
    )
    
    class Meta:
        model = Startup
        fields = [
            'id',  # Include id if needed in response
            'name',
            'short_description',
            'description',
            'phase',
            'status',
            'priority',
            'contact_email',
            'linkedin_url',
            'facebook_url',
            'founders',
            'categories',
            'batch',      # Allow batch name input
            'pitch_deck'
        ]
        