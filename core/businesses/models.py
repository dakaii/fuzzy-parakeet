import datetime

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
    UNKNOWN = 0
    AVAILABLE = 1
    UNAVAILABLE = 2

    STATUS_CHOICES = (
        (UNKNOWN, 'Unknown'),
        (AVAILABLE, 'Available'),
        (UNAVAILABLE, 'Unavailable'),
    )
    account_owner = models.OneToOneField(
        get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    representative = models.OneToOneField(
        AffiliatedPerson, on_delete=models.CASCADE)
    website = models.URLField(max_length=300)
    founded_in = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1400), max_value_current_year])
    tour_availability = models.PositiveSmallIntegerField(
        default=UNKNOWN, choices=STATUS_CHOICES)


class Product(TimeRecordMixin):
    name = models.CharField(max_length=30)
    description = models.TextField()
    organization = models.ForeignKey(
        Organization, on_delete=models.CASCADE, related_name='products')


class Review(TimeRecordMixin):
    title = models.CharField(max_length=30)
    comment = models.TextField()
    author = models.ForeignKey(
        get_user_model(), on_delete=models.CASCADE, related_name='reviews')
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='reviews')


class Picture(TimeRecordMixin):
    title = models.CharField(max_length=30)
    description = models.TextField(default='')
    url = models.URLField(max_length=400)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='pictures')
    is_primary = models.BooleanField(default=False)
