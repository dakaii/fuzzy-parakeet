
import pytest
from django.contrib.auth import get_user_model
from pytest_factoryboy import register
from rest_framework.reverse import reverse
from rest_framework.test import APIClient

from tests.factories import UserFactory

register(UserFactory)

AccountOwner = get_user_model()


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


@pytest.fixture
def api_client_general_user(db, user_factory, api_client):
    password = 'testingpassword'
    user = user_factory(password=password,
                        category=AccountOwner.GENERAL_USER)

    data = {'username': user.username,
            'email': user.email, 'password': password}
    response = api_client.post(reverse('jwt-create'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client, user


@pytest.fixture
def api_client_business_owner(db, user_factory, api_client):
    password = 'testingpassword'
    user = user_factory(password=password,
                        category=AccountOwner.BUSINESS_OWNER)

    data = {'username': user.username,
            'email': user.email, 'password': password}
    response = api_client.post(reverse('jwt-create'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
    return api_client, user
