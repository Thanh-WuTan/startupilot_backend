from rest_framework import serializers
from ...models import Startup, StartupMembership, Role, Category, Batch, Pitchdeck, Avatar, Note, Phase, Status, Priority, Role, Advisor

class StartupMembershipSerializer(serializers.ModelSerializer): 
    id = serializers.UUIDField(source='person.id')
    role = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Role.objects.all(),
        source='roles'
    )

    class Meta:
        model = StartupMembership
        fields = ['name', 'role']


class StartupSerializer(serializers.ModelSerializer): 
    members = StartupMembershipSerializer(source='startupmembership_set', many=True, read_only=True)

    categories = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    phase = serializers.CharField(source='phase.name', read_only=True)
    status = serializers.CharField(source='status.name', read_only=True)
    priority = serializers.CharField(source='priority.name', read_only=True)

    batch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Batch.objects.all(),
        required=False,
        allow_null=True
    )

    pitch_deck = serializers.SlugRelatedField(
        slug_field='id',
        queryset=Pitchdeck.objects.all(),
        required=False,
        allow_null=True
    )

    avatar = serializers.SlugRelatedField(
        many=True,
        slug_field='id',
        queryset=Avatar.objects.all(),
        required=False,
        allow_null=True
    )

    notes = serializers.PrimaryKeyRelatedField(queryset=Note.objects.all(), many=True)

    advisor = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Advisor.objects.all(),
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
            'email',
            'categories',
            'linkedin_url',
            'facebook_url',
            'phase',
            'status',
            'priority',
            'batch',
            'members',
            'pitch_deck',
            'avatar',
            'notes',
            'advisor'
        ]
