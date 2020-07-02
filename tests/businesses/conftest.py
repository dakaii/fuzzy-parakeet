import pytest
from pytest_factoryboy import register
from tests.businesses.factories import ProductFactory

from .factories import AffiliatedPersonFactory, OrganizationFactory

register(AffiliatedPersonFactory)
register(OrganizationFactory)
register(ProductFactory)
