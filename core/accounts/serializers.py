from django.db import IntegrityError
from rest_framework import serializers

from .models import AccountOwner


class AccountOwnerSerializer(serializers.ModelSerializer):

    username = serializers.CharField(max_length=30, min_length=6)
    email = serializers.EmailField(max_length=100, min_length=6)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = AccountOwner
        fields = (
            'id', 'username', 'category', 'email', 'password', 'is_staff',
            'is_active', 'date_joined')

    def validate_username(self, value):
        # TODO optimize this validation process
        if AccountOwner.objects.filter(username=value).exists():
            raise serializers.ValidationError('The username is already taken.')
        return value

    def validate_email(self, value):
        if AccountOwner.objects.filter(email=value).exists():
            raise serializers.ValidationError('The email is already taken.')
        return value

    def create(self, validated_data):
        return AccountOwner.objects.create_user(**validated_data)
