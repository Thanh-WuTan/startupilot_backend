from rest_framework import serializers
from ..models.role_model import Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name']  # Adjust fields as needed
