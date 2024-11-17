from rest_framework import serializers
from ..models.status_model import Status

class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ['id', 'name']  # Adjust fields as necessary