import pytest
from pytest_factoryboy import register
from tests.businesses.factories import (AffiliatedPersonFactory,
                                        OrganizationFactory,
                                        OrganizationHistoryFactory,
                                        ProductFactory)
from tests.locations.factories import LocationFactory

register(LocationFactory)

register(AffiliatedPersonFactory)
register(OrganizationHistoryFactory)
register(OrganizationFactory)
register(ProductFactory)
