import datetime

from core.businesses.models import Picture, Product, Review
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from .models import AffiliatedPerson, Organization

AccountOwner = get_user_model()


class AffiliatedPersonSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=30, min_length=1)
    last_name = serializers.CharField(max_length=30, min_length=1)

    class Meta:
        model = AffiliatedPerson
        fields = ['first_name', 'last_name']


class OrganizationSerializer(serializers.ModelSerializer):

    name = serializers.CharField(max_length=30, min_length=1)
    representative = AffiliatedPersonSerializer()
    website = serializers.URLField()
    founded_in = serializers.IntegerField(
        max_value=datetime.date.today().year, min_value=1400)
    tour_availability = serializers.ChoiceField(
        choices=Organization.STATUS_CHOICES)

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'representative', 'website', 'founded_in',
            'tour_availability']

    @transaction.atomic
    def create(self, validated_data):
        representative_serializer = AffiliatedPersonSerializer(
            data=validated_data.pop('representative'))
        representative_serializer.is_valid(raise_exception=True)
        validated_data['representative'] = representative_serializer.save()
        validated_data['account_owner'] = self.context['request'].user
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        representative_serializer = AffiliatedPersonSerializer(
            data=validated_data.pop('representative'))
        representative_serializer.is_valid(raise_exception=True)
        validated_data['representative'] = representative_serializer.save()
        return super().update(instance, validated_data)


class OrganizationDetailSerializer(OrganizationSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)

    class Meta:
        model = Organization
        fields = [
            'id', 'name', 'representative', 'website', 'founded_in',
            'tour_availability', 'products']


class PictureSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30, min_length=1)
    description = serializers.CharField(max_length=500, min_length=1)
    url = serializers.URLField()
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())
    is_primary = serializers.BooleanField()

    class Meta:
        model = Picture
        fields = ['id', 'title', 'description', 'url', 'product', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, min_length=1)
    description = serializers.CharField(max_length=500, min_length=1)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all())
    pictures = PictureSerializer(many=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'organization', 'pictures']


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30, min_length=1)
    comment = serializers.CharField(max_length=500, min_length=1)
    author = serializers.PrimaryKeyRelatedField(
        default=serializers.CurrentUserDefault(),
        queryset=AccountOwner.objects.all())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'title', 'comment', 'product', 'author']
