from rest_framework import serializers
from ...models import Startup, Category, Batch, Avatar, Pitchdeck, StartupMembership, Role

class StartupMembershipSerializer(serializers.ModelSerializer):
    # Display the shorthand for each person and their roles as a list of strings
    shorthand = serializers.CharField(source='person.shorthand')
    role = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        source='roles'
    )

    class Meta:
        model = StartupMembership
        fields = ['shorthand', 'role']

class StartupSerializer(serializers.ModelSerializer):
    # Use the custom serializer for the members field
    members = StartupMembershipSerializer(source='startupmembership_set', many=True, read_only=True)

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
        slug_field='name',
        queryset=Pitchdeck.objects.all(),
        required=False,
        allow_null=True
    )

    avatar = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Avatar.objects.all(),
        required=False,
        allow_null=True
    )

    class Meta:
        model = Startup
        fields = [
            'id',
            'name',
            'short_description',
            'description',
            'phase',
            'status',
            'priority',
            'contact_email',
            'linkedin_url',
            'facebook_url',
            'members',
            'categories',
            'batch',
            'pitch_deck',
            'avatar'
        ]
