from rest_framework import serializers
from ...models import Pitchdeck


class PitchdeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitchdeck
        fields = ['id', 'name']