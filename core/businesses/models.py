import datetime

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models.query_utils import Q
from phonenumber_field.modelfields import PhoneNumberField

from core.locations.models import Location


def max_value_current_year(value):
    #  Note that MaxValueValidator is wrapped in a function
    #  max_value_current_year to avoid a new migration every year.
    return MaxValueValidator(datetime.date.today().year)(value)


class TimeRecordMixin(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class AffiliatedPerson(TimeRecordMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)


class Organization(TimeRecordMixin):
    AVAILABLE = 0
    UNAVAILABLE = 1
    UNKNOWN = 2

    AVAILABILITY_CHOICES = (
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
        (UNKNOWN, 'Unknown'),
    )
    account_owner = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
    description = models.TextField()
    favorited_by = models.ManyToManyField(
        get_user_model(),
        through='FavoriteOrganization',
        through_fields=('organization', 'person'),
        related_name='favorites')
    founded_in = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1400), max_value_current_year])
    location = models.OneToOneField(Location, on_delete=models.CASCADE)
    name = models.CharField(max_length=60)
    rated_by = models.ManyToManyField(
        get_user_model(),
        through='Rating',
        through_fields=('organization', 'person'),
        related_name='rated_organizations')
    representative = models.OneToOneField(
        AffiliatedPerson, on_delete=models.CASCADE)
    tour_availability = models.PositiveSmallIntegerField(
        default=UNKNOWN, choices=AVAILABILITY_CHOICES)
    website = models.URLField(max_length=300)
    phone_number = PhoneNumberField(null=True)
    twitter = models.URLField(null=True, max_length=300)
    facebook = models.URLField(null=True, max_length=300)
    instagram = models.URLField(null=True, max_length=300)
    ecommerce = models.URLField(null=True, max_length=300)
    image = models.URLField(null=True)


class FavoriteOrganization(TimeRecordMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'person'],
                name='unique_favorite')
        ]


class Rating(TimeRecordMixin):
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    person = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    stars = models.PositiveSmallIntegerField(validators=[
        MinValueValidator(1),
        MaxValueValidator(5)])

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['organization', 'person'],
                name='unique_rating')
        ]


class Product(TimeRecordMixin):
    name = models.CharField(max_length=30)
    description = models.TextField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='products')
    is_primary = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='products')
    url = models.URLField(null=True, max_length=300)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['is_primary'],
                condition=Q(is_primary=True),
                name='unique_product_is_primary')
        ]


class Review(TimeRecordMixin):
    title = models.CharField(max_length=30)
    comment = models.TextField()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')


class OrgBrowsingHstry(TimeRecordMixin):
    MAX_CAPACITY = 20

    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
        related_name='org_browsing_hstry')

    class Meta:
        verbose_name = 'organization_browsing_history'
