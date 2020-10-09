from rest_framework import serializers


class ChoiceValuesField(serializers.Field):
    """Custom ChoiceField serializer field."""

    def __init__(self, choices, **kwargs):
        self._choices = dict(choices)
        super().__init__(**kwargs)

    def to_representation(self, obj):
        return self._choices[obj]

    def to_internal_value(self, data):
        if data in self._choices:
            return data
        for key, val in self._choices.items():
            if self._choices[key] == data:
                return key
        raise serializers.ValidationError(
            "Acceptable values are {0}.".format(list(self._choices.values())))
