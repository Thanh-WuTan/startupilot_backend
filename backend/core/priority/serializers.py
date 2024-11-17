from rest_framework import serializers
from ..models.priority_model import Priority

class PrioritySerializer(serializers.ModelSerializer):
    class Meta:
        model = Priority
        fields = ['id', 'name']  # Adjust fields as necessary
