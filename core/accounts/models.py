from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from core.locations.models import Location


class AccountOwner(AbstractUser):
    BUSINESS_OWNER = 0
    GENERAL_USER = 1

    ACCOUNT_CATEGORY = (
        (BUSINESS_OWNER, 'Business Owner'),
        (GENERAL_USER, 'General User'),
    )

    FEMALE = 0
    MALE = 1
    NON_BINARY = 2

    GENDER_CATEGORY = (
        (FEMALE, 'Female'),
        (MALE, 'Male'),
        (NON_BINARY, 'Non-Binary'),
    )
    category = models.PositiveSmallIntegerField(
        default=GENERAL_USER, choices=ACCOUNT_CATEGORY)
    date_of_birth = models.DateField(null=True)
    gender = models.PositiveSmallIntegerField(
        null=True, choices=GENDER_CATEGORY)
    location = models.OneToOneField(
        Location, null=True, on_delete=models.CASCADE)
    phone_number = PhoneNumberField(null=True)

    REQUIRED_FIELDS = ['category']
