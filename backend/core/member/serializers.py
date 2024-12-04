from rest_framework import serializers
from ..models import Person, StartupMembership, Note, Startup

class StartupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Startup
        fields = ['id', 'name']

class StartupMembershipSerializer(serializers.ModelSerializer):
    startup = StartupSerializer()

    class Meta:
        model = StartupMembership
        fields = ['id', 'startup', 'role', 'status']

class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ['id', 'content', 'created_at', 'updated_at']

class MemberSerializer(serializers.ModelSerializer):
    memberships = StartupMembershipSerializer(source='startupmembership_set', many=True, read_only=True)
    notes = serializers.SerializerMethodField()

    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'shorthand',  'phone', 'linkedin_url', 'facebook_url', 'memberships', 'avatar', 'notes']

    def get_notes(self, obj):
        notes = Note.objects.filter(content_type__model='person', object_id=obj.id)
        return NoteSerializer(notes, many=True).data

class MemberListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Person
        fields = ['id', 'name', 'email', 'shorthand', 'phone', 'linkedin_url', 'facebook_url', 'avatar']
