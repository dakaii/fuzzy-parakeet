
import factory

from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = get_user_model()

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    username = factory.LazyAttribute(
        lambda user: f'{user.first_name} {user.last_name}')
    email = factory.LazyAttribute(
        lambda user: f'{user.first_name}.{user.last_name}@example.com'.lower())
    password = factory.PostGenerationMethodCall(
        'set_password', factory.Sequence(lambda n: f'password{n}')
    )

    @factory.post_generation
    def has_default_group(self, create, extracted, **kwargs):
        if not create:
            return
        if extracted:
            default_group, _ = Group.objects.get_or_create(
                name='group'
            )
            self.groups.add(default_group)
