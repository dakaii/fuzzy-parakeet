from django.contrib import admin

from .models import AffiliatedPerson, Organization, Product, Review

admin.site.register(AffiliatedPerson)
admin.site.register(Organization)
admin.site.register(Product)
admin.site.register(Review)
