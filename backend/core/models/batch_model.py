from django.db import models
from django.core.exceptions import ValidationError

import uuid
import re

class Batch(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = 'Batch'  # Singular name for the model
        verbose_name_plural = 'Batches'  # Plural name for the model

    def clean(self):
        # Regular expression to match the format 'AY XX-YY'
        pattern = r'^AY (\d{2})-(\d{2})$'
        match = re.match(pattern, self.name.strip())

        if not match:
            raise ValidationError(
                "Name must be in the format 'AY XX-YY' (e.g., 'AY 20-21')."
            )

        # Extract XX and YY
        xx, yy = map(int, match.groups())

        # Validate that YY is XX + 1
        if yy != xx + 1:
            raise ValidationError(
                "The second part of the year (YY) must be one greater than the first part (XX)."
            )

    def __str__(self) -> str:
        return self.name