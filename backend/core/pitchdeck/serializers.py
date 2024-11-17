from rest_framework import serializers
from ..models.pitchdeck_model import Pitchdeck


class PitchdeckSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pitchdeck
        fields = ['id', 'pitchdeck']  # The pitchdeck field is what stores the file URL

    def to_representation(self, instance):
        # This method is used to customize the returned data.
        representation = super().to_representation(instance)
        # You can rename 'pitchdeck' to 'url' if you'd like to represent it as a URL instead of a file field.
        representation['pitchdeck'] = instance.pitchdeck.url if instance.pitchdeck else None
        return representation