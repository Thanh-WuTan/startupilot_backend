from rest_framework import serializers
from ...models import Startup, Category, Founder, Batch, Avatar, Pitchdeck

class StartupSerializer(serializers.ModelSerializer):
    founders = serializers.SlugRelatedField(
        many=True, 
        slug_field='shorthand', 
        queryset=Founder.objects.all(),
        required=False,
        allow_null=True
    )
    categories = serializers.SlugRelatedField(
        many=True, 
        slug_field='name', 
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    batch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Batch.objects.all(),
        required=False,
        allow_null=True
    )
    
    pitch_deck = serializers.SlugRelatedField(
        slug_field='name',   # Use the UUID as the slug field
        queryset=Pitchdeck.objects.all(),
        required=False,
        allow_null=True
    )
    
    avatar = serializers.SlugRelatedField(
        slug_field='name',   # Use the UUID as the slug field
        queryset=Avatar.objects.all(),
        required=False,
        allow_null=True
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
            'pitch_deck',
            'avatar'
        ]
        