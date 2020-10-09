import factory

from core.locations.models import Location


class LocationFactory(factory.DjangoModelFactory):
    class Meta:
        model = Location

    country = factory.Faker('country_code')
    city = factory.Faker('city')
    state = factory.Faker('city')
    address = factory.Faker('street_address')
    zip_code = factory.Faker('postcode')
