import datetime

from azure.storage.blob import BlockBlobService, PublicAccess
from core.businesses.models import (AffiliatedPerson, FavoriteOrganization,
                                    Organization, OrgBrowsingHstry, Product,
                                    Rating, Review)
from core.locations.serializers import LocationSerializer
from core.utils import ChoiceValuesField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import NotFound

AccountOwner = get_user_model()


class AffiliatedPersonSerializer(serializers.ModelSerializer):

    first_name = serializers.CharField(max_length=30, min_length=1)
    last_name = serializers.CharField(max_length=30, min_length=1)

    class Meta:
        model = AffiliatedPerson
        fields = ['first_name', 'last_name']


class FavoriteSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField(write_only=True)
    organization = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = FavoriteOrganization
        fields = ['organization_id', 'organization']

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        try:
            return super().create(validated_data)
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})


class FavoriteListSerializer(serializers.ModelSerializer):
    favorites = FavoriteSerializer(
        source='favoriteorganization_set', many=True, read_only=True)

    class Meta:
        model = AccountOwner
        fields = ['favorites']


class OrganizationSerializer(serializers.ModelSerializer):

    account_owner = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    name = serializers.CharField(max_length=30, min_length=1)
    description = serializers.CharField(max_length=300, min_length=1)
    location = LocationSerializer()
    representative = AffiliatedPersonSerializer()
    website = serializers.URLField()
    image = serializers.URLField(allow_blank=True, required=False)
    twitter = serializers.URLField(allow_blank=True, required=False)
    facebook = serializers.URLField(allow_blank=True, required=False)
    instagram = serializers.URLField(allow_blank=True, required=False)
    ecommerce = serializers.URLField(allow_blank=True, required=False)
    founded_in = serializers.IntegerField(
        max_value=datetime.date.today().year, min_value=1400)
    tour_availability = ChoiceValuesField(
        choices=Organization.AVAILABILITY_CHOICES)
    phone_number = serializers.CharField(
        allow_blank=True, max_length=17, min_length=7, required=False)

    class Meta:
        model = Organization
        exclude = ['rated_by', 'favorited_by']

    def validate_image(self, value):
        return value if value else None

    def validate_twitter(self, value):
        if not value:
            return None
        self._validate_url(value, 'https://twitter.com')
        return value

    def validate_facebook(self, value):
        if not value:
            return None
        self._validate_url(value, 'https://facebook.com')
        return value

    def validate_instagram(self, value):
        if not value:
            return None
        self._validate_url(value, 'https://instagram.com')
        return value

    def validate_ecommerce(self, value):
        return value if value else None

    def validate_phone_number(self, value):
        return value if value else None

    def _validate_url(self, value, url_prefix):
        if not value.startswith(url_prefix):
            raise serializers.ValidationError(
                f'The url has to start with {url_prefix}')
        return value

    @transaction.atomic
    def create(self, validated_data):
        representative_serializer = AffiliatedPersonSerializer(
            data=validated_data.pop('representative'))
        representative_serializer.is_valid(raise_exception=True)
        validated_data['representative'] = representative_serializer.save()
        location_serializer = LocationSerializer(
            data=validated_data.pop('location', None))
        location_serializer.is_valid(raise_exception=True)
        validated_data['location'] = location_serializer.save()
        validated_data['account_owner'] = self.context['request'].user
        return super().create(validated_data)

    @transaction.atomic
    def update(self, instance, validated_data):
        representative_data = validated_data.pop('representative', None)
        if representative_data:
            representative_serializer = AffiliatedPersonSerializer(
                data=representative_data)
            representative_serializer.is_valid(raise_exception=True)
            validated_data['representative'] = representative_serializer.save()
        location_data = validated_data.pop('location', None)
        if location_data:
            location_serializer = LocationSerializer(data=location_data)
            location_serializer.is_valid(raise_exception=True)
            validated_data['location'] = location_serializer.save()
        return super().update(instance, validated_data)


class OrganizationDetailSerializer(OrganizationSerializer):
    products = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    is_favorited = serializers.SerializerMethodField('get_is_favorited')
    rating = serializers.SerializerMethodField('get_rating')

    class Meta:
        model = Organization
        exclude = ['rated_by', 'favorited_by']

    def get_is_favorited(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None
        return user.favorites.filter(pk=obj.pk).exists()

    def get_rating(self, obj):
        user = self.context['request'].user
        if isinstance(user, AnonymousUser):
            return None
        try:
            return Rating.objects.get(
                person=user, organization=obj).stars
        except Rating.DoesNotExist:
            return None


class ProductSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=30, min_length=1)
    description = serializers.CharField(max_length=500, min_length=1)
    organization = serializers.PrimaryKeyRelatedField(
        queryset=Organization.objects.all())
    url = serializers.URLField()
    photo = serializers.ImageField(use_url=True)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'organization', 'url', 'photo']

    def create(self, validated_data):
        user = self.context['request'].user
        extension = self._get_extension(validated_data['photo'].content_type)
        validated_data['photo'].name = f'product-photo-{user.pk}{extension}'
        return super().create(validated_data)

    def _get_extension(self, content_type):
        if 'png' in content_type:
            return '.png'
        return '.jpg'


class RatingSerializer(serializers.ModelSerializer):
    organization_id = serializers.IntegerField(write_only=True)
    organization = OrganizationDetailSerializer(read_only=True)
    stars = serializers.IntegerField(write_only=True)

    class Meta:
        model = Rating
        fields = ['organization_id', 'organization', 'stars']

    def validate_organization_id(self, value):
        if Organization.objects.filter(pk=value).exists():
            return value
        raise serializers.ValidationError('Invalid organization id')

    def validate_stars(self, value):
        if 0 < value < 5:
            return value
        raise serializers.ValidationError('Invalid rating')

    def create(self, validated_data):
        validated_data['person'] = self.context['request'].user
        existing_rating = self._get_existing_rating(validated_data)
        if existing_rating:
            existing_rating.stars = validated_data['stars']
            existing_rating.save()
            return existing_rating
        return super().create(validated_data)

    def _get_existing_rating(self, validated_data):
        try:
            return Rating.objects.get(
                person=validated_data['person'],
                organization=validated_data['organization_id'])
        except Rating.DoesNotExist:
            return None


class RatingListSerializer(serializers.ModelSerializer):
    ratings = RatingSerializer(
        source='rating_set', many=True, read_only=True)

    class Meta:
        model = AccountOwner
        fields = ['ratings']


class ReviewSerializer(serializers.ModelSerializer):
    title = serializers.CharField(max_length=30, min_length=1)
    comment = serializers.CharField(max_length=500, min_length=1)
    author = serializers.HiddenField(
        default=serializers.CurrentUserDefault())
    product = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all())

    class Meta:
        model = Review
        fields = ['id', 'title', 'comment', 'product', 'author']


class OrgBrowsingHstrySerializer(serializers.ModelSerializer):
    created_at = serializers.DateTimeField(read_only=True)
    organization_id = serializers.IntegerField(write_only=True)
    organization = OrganizationDetailSerializer(read_only=True)
    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault())

    class Meta:
        model = OrgBrowsingHstry
        fields = ['created_at', 'organization_id', 'organization', 'user']

    @transaction.atomic
    def create(self, validated_data):
        user = self.context['request'].user
        model = self.Meta.model
        history_ids = model.objects.filter(user=user).order_by(
            '-created_at')[model.MAX_CAPACITY:].values_list('id', flat=True)
        if history_ids:
            model.objects.filter(pk__in=history_ids).delete()
        return super().create(validated_data)


class OrganizationImageSerializer(serializers.Serializer):
    image = serializers.ImageField(write_only=True)
    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        content_type = self.initial_data['image'].content_type
        return self._get_url(content_type)

    def create(self, validated_data):
        image = validated_data['image']
        content_type = self.initial_data['image'].content_type
        extension = self._get_extension(content_type)
        user = self.context['request'].user
        blob_service = BlockBlobService(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY)
        blob_service.create_blob_from_bytes(
            settings.AZURE_CONTAINER,
            f'organization-picture-{user.pk}{extension}',
            image.read()
        )
        try:
            org = user.organization
            org.image = self._get_url(image.content_type)
            org.save()
        except Organization.DoesNotExist as e:
            raise NotFound(detail={'message': str(e)})
        return {}

    def _get_url(self, content_type):
        user = self.context['request'].user
        extension = self._get_extension(content_type)
        blob_service = BlockBlobService(
            account_name=settings.AZURE_ACCOUNT_NAME,
            account_key=settings.AZURE_ACCOUNT_KEY)
        return blob_service.make_blob_url(
            settings.AZURE_CONTAINER,
            f'organization-picture-{user.pk}{extension}')

    def _get_extension(self, content_type):
        if 'png' in content_type:
            return '.png'
        return '.jpg'
