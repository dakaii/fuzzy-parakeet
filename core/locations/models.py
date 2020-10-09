from django.db import models

from django_countries.fields import CountryField


class Location(models.Model):
    country = CountryField()
    state = models.CharField(blank=True, max_length=50)
    city = models.CharField(blank=True, max_length=50)
    address = models.CharField(blank=True, max_length=150)
    zip_code = models.CharField(blank=True, max_length=50)
