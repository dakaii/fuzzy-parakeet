
from rest_framework import serializers

from core.locations.models import Location
from django_countries.serializer_fields import CountryField


class LocationSerializer(serializers.ModelSerializer):
    country = CountryField(country_dict=True)
    state = serializers.CharField(max_length=30, required=False)
    city = serializers.CharField(max_length=30, required=False)
    address = serializers.CharField(max_length=30, required=False)
    zip_code = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = Location
        fields = ['country', 'state', 'city', 'address', 'zip_code']
