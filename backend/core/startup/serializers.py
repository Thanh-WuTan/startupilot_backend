from rest_framework import serializers
from ..models import Startup, Category, Batch, StartupMembership, Note, Phase, Status, Priority

class StartupMembershipSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(source='person.id')
    name = serializers.CharField(source='person.name')

    class Meta:
        model = StartupMembership
        fields = ['id', 'name', 'role', 'status']


class StartupSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    phases = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Phase.objects.all(),
        required=False,
        allow_null=True
    )

    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Status.objects.all(),
        required=False,
        allow_null=True
    )

    priority = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Priority.objects.all(),
        required=False,
        allow_null=True
    )

    batch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Batch.objects.all(),
        required=False,
        allow_null=True
    )

    notes = serializers.SerializerMethodField()

    memberships = serializers.SerializerMethodField()

    advisors = serializers.SerializerMethodField()

    class Meta:
        model = Startup
        fields = [
            'id',
            'name',
            'short_description',
            'description',
            'email',
            'category',
            'linkedin_url',
            'facebook_url',
            'phases',
            'status',
            'priority',
            'batch',
            'launch_date',
            'pitch_deck',
            'avatar',
            'notes',
            'memberships',
            'advisors'
        ]

    def get_notes(self, obj):
        # Retrieve notes related to the current startup
        notes = Note.objects.filter(content_type__model='startup', object_id=obj.id)
        return [
            {
                'id': note.id,
                'content': note.content,
                'created_at': note.created_at,
                'updated_at': note.updated_at
            }
            for note in notes
        ]

    def get_memberships(self, obj):
        memberships = StartupMembership.objects.filter(startup=obj)
        return [
            {
                'id': membership.id,
                'member': {
                    'id': membership.person.id,
                    'name': membership.person.name,
                    'email': membership.person.email
                },
                'status': membership.status,
                'roles': membership.role
            }
            for membership in memberships
        ]

    def get_advisors(self, obj):
        # Retrieve advisors related to the current startup
        advisors = obj.advisors.all()
        return [
            {
                'id': advisor.id,
                'name': advisor.name
            }
            for advisor in advisors
        ]
    
class ManyStartupSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Category.objects.all(),
        required=False,
        allow_null=True
    )

    phases = serializers.SlugRelatedField(
        many=True,
        slug_field='name',
        queryset=Phase.objects.all(),
        required=False,
        allow_null=True
    )
    
    status = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Status.objects.all(),
        required=False,
        allow_null=True
    )

    priority = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Priority.objects.all(),
        required=False,
        allow_null=True
    )

    batch = serializers.SlugRelatedField(
        slug_field='name',
        queryset=Batch.objects.all(),
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
            'category',
            'phases',
            'status',
            'priority',
            'batch',
            'avatar',
        ]