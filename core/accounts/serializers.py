from django.db import transaction
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework import serializers

from core.utils import ChoiceValuesField
from core.locations.serializers import LocationSerializer

from .models import AccountOwner


class AccountOwnerCreateSerializer(UserCreateSerializer):
    username = serializers.CharField(max_length=30, min_length=6)
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(write_only=True)
    category = ChoiceValuesField(
        choices=AccountOwner.ACCOUNT_CATEGORY, required=False)
    gender = ChoiceValuesField(
        choices=AccountOwner.GENDER_CATEGORY, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = AccountOwner
        fields = (
            'id', 'username', 'category', 'email', 'password', 'is_staff',
            'is_active', 'date_joined',  'gender', 'date_of_birth',
            'first_name', 'last_name')

    def validate_username(self, value):
        if AccountOwner.objects.filter(username=value).exists():
            raise serializers.ValidationError('The username is already taken.')
        return value

    def validate_email(self, value):
        if AccountOwner.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email is already taken.')
        return value

    @transaction.atomic
    def create(self, validated_data):
        location_serializer = LocationSerializer(
            data=validated_data.pop('location', None))
        new_user = super().create(validated_data)
        if location_serializer.is_valid():
            new_user.location = location_serializer.save()
            new_user.save()
        return new_user


class AccountOwnerSerializer(UserSerializer):
    username = serializers.CharField(max_length=30, min_length=6)
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(write_only=True)
    location = LocationSerializer(required=False)
    favorites = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    rated_organizations = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True)
    category = ChoiceValuesField(
        choices=AccountOwner.ACCOUNT_CATEGORY, required=False)
    gender = ChoiceValuesField(
        choices=AccountOwner.GENDER_CATEGORY, required=False)
    phone_number = serializers.CharField(
        max_length=17, min_length=7, required=False)
    first_name = serializers.CharField(max_length=30, required=False)
    last_name = serializers.CharField(max_length=30, required=False)

    class Meta:
        model = AccountOwner
        fields = (
            'id', 'username', 'category', 'email', 'password', 'is_staff',
            'is_active', 'date_joined', 'location', 'favorites',
            'rated_organizations', 'gender', 'date_of_birth', 'phone_number',
            'first_name', 'last_name')

    @transaction.atomic
    def update(self, instance, validated_data):
        location_serializer = LocationSerializer(
            data=validated_data.pop('location', None))
        if location_serializer.is_valid():
            validated_data['location'] = location_serializer.save()
        return super().update(instance, validated_data)
