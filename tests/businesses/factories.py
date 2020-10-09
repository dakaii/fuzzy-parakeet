import factory
from core.accounts.models import AccountOwner
from core.businesses.models import (AffiliatedPerson, Organization,
                                    OrgBrowsingHstry, Product)
from tests.factories import UserFactory
from tests.locations.factories import LocationFactory


class AffiliatedPersonFactory(factory.DjangoModelFactory):
    class Meta:
        model = AffiliatedPerson

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('company')
    description = factory.Faker('catch_phrase')
    representative = factory.SubFactory(AffiliatedPersonFactory)
    website = factory.LazyAttribute(
        lambda org: 'http://{}@example.com'.lower().format(
            org.name.lower().replace(' ', '_')))
    founded_in = factory.Faker('random_int', min=1500, max=2010)
    tour_availability = factory.Faker('random_int', min=0, max=2)
    account_owner = factory.SubFactory(
        UserFactory, category=AccountOwner.BUSINESS_OWNER)
    location = factory.SubFactory(LocationFactory)


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    description = factory.Faker('text')
    organization = factory.SubFactory(OrganizationFactory)


class OrganizationHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        model = OrgBrowsingHstry

    organization = factory.SubFactory(OrganizationFactory)
    user = factory.SubFactory(
        UserFactory, category=AccountOwner.GENERAL_USER)
