from rest_framework import serializers
from ..models.batch_model import Batch

class BatchSerializer(serializers.ModelSerializer):
    class Meta:
        model = Batch
        fields = ['id', 'name']

    def validate_name(self, value):
        import re
        
        # Regular expression to match the format 'AY XX-YY'
        pattern = r'^AY (\d{2})-(\d{2})$'
        match = re.match(pattern, value.strip())
        
        if not match:
            raise serializers.ValidationError(
                "Name must be in the format 'AY XX-YY' (e.g., 'AY 20-21')."
            )
        
        # Extract XX and YY
        xx, yy = map(int, match.groups())
        
        # Validate that YY is XX + 1
        if yy != xx + 1:
            raise serializers.ValidationError(
                "The second part of the year (YY) must be one greater than the first part (XX)."
            )
        
        return value