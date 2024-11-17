from rest_framework import serializers
from ..models.advisor_model import Advisor

class AdvisorSerializer(serializers.ModelSerializer):
    mentorships = serializers.SerializerMethodField()

    class Meta:
        model = Advisor
        fields = ('id', 'name', 'email', 'phone', 'linkedin_url', 'facebook_url', 'shorthand', 'mentorships')

    def get_mentorships(self, obj):
        return [
            {
                "startup": {
                    "id": startup.id,
                    "name": startup.name
                }
            }
            for startup in obj.startups.all()
        ]
