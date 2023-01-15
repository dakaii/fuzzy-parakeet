import factory
import pytest
from rest_framework.reverse import reverse
from core.accounts.models.account_owners import AccountOwner


@pytest.mark.django_db
def test_create_org(api_client, user_factory):
    password = 'randompass'
    user = user_factory(password=password,
                        category=AccountOwner.BUSINESS_OWNER)

    data = {'username': user.username,
            'email': user.email, 'password': password}
    response = api_client.post(reverse('jwt-create'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    url = reverse('business-organizations')
    data = {
        'name': 'Chebacca Inc.',
        'representative': {'firstName': 'Luke', 'lastName': 'Skywalker'},
        'website': 'http://millennium@falcon.com',
        'foundedIn': 2001,
        'tourAvailability': 2
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_review(api_client, user_factory, product_factory):
    password = 'randompass'
    user = user_factory(password=password,
                        category=AccountOwner.GENERAL_USER)

    data = {'username': user.username,
            'email': user.email, 'password': password}
    response = api_client.post(reverse('jwt-create'), data, format='json')
    access_token = response.data['access']
    api_client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    product = product_factory()
    url = reverse('review-list')
    data = {
        'title': 'Fuji Apple',
        'comment': 'Fresh af',
        'product': product.pk
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201
    assert response.data['author'] == user.pk
