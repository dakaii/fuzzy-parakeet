
import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient
from tests.factories import UserFactory

register(UserFactory)


@pytest.fixture
def api_client(db, user_factory):
    user_factory(username='example',
                 password='johnpassword', has_default_group=True)
    return APIClient()


@pytest.fixture
def api_client_with_credentials(db, user_factory, api_client):
    user = user_factory(has_default_group=True)
    api_client.force_authenticate(user=user)
    yield api_client
    api_client.force_authenticate(user=None)
