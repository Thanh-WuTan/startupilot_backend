from rest_framework import serializers
from ...models.avatar_model import Avatar


class AvatarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Avatar
        fields = ['id', 'avatar']  # The pitchdeck field is what stores the file URL

    def to_representation(self, instance):
        # This method is used to customize the returned data.
        representation = super().to_representation(instance)
        # You can rename 'pitchdeck' to 'url' if you'd like to represent it as a URL instead of a file field.
        representation['avatar'] = instance.avatar.url if instance.avatar else None
        return representation