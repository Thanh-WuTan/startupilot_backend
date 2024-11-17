from rest_framework import serializers
from ..models.batch_model import Batch

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']
