from rest_framework import serializers
from ..models.avatar_model import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'avatar_url']  # The fields that will be serialized