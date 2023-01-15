import factory
from core.businesses.models import AffiliatedPerson, Organization, Product
from tests.factories import UserFactory
from core.accounts.models.account_owners import AccountOwner


class AffiliatedPersonFactory(factory.DjangoModelFactory):
    class Meta:
        model = AffiliatedPerson

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')


class OrganizationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Organization

    name = factory.Faker('company')
    representative = factory.SubFactory(AffiliatedPersonFactory)
    website = factory.LazyAttribute(
        lambda org: f'http://{org.name}@example.com'.lower())
    founded_in = factory.Faker('random_int', min=1500, max=2010)
    tour_availability = factory.Faker('random_int', min=0, max=2)
    account_owner = factory.SubFactory(
        UserFactory, category=AccountOwner.BUSINESS_OWNER)


class ProductFactory(factory.DjangoModelFactory):
    class Meta:
        model = Product

    name = factory.Faker('word')
    description = factory.Faker('text')
    organization = factory.SubFactory(OrganizationFactory)
