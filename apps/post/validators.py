from difflib import SequenceMatcher
from django.core.exceptions import ValidationError
from rest_framework import serializers


class ValidateFuzzyUnique:
    """Matches the validation value with all existing target_field values and raises
    an ValidationError exception if it is too similar.

    Args:
        queryset: The queryset to be used.
        target_field: The field of the queryset that should be compared.
        source: Where the validator is called from: 'serializer' or 'form'.
        value: The value to be validated on calling.

    Raises:
        ValidationError: Raised if SequenceMatcher ratio is > 0.85.
    """
    def __init__(self, queryset, target_field, source="form"):
        self.queryset = queryset
        self.target_field = target_field
        self.source = source
        self.model = self.queryset.model.__name__

    def __call__(self, value):
        values = [getattr(row, self.target_field)
                  for row in self.queryset]
        value = value.lower()
        for val in values:
            if SequenceMatcher(None, val.lower(), value).ratio() > 0.85:
                message = (
                    f"Name too similar to existing {self.model} {val}.")
                if self.source.lower() == "serializer":
                    raise serializers.ValidationError(message)
                else:
                    raise ValidationError(message)

