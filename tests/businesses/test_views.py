from random import randrange

import pytest
from core.businesses.models import OrgBrowsingHstry
from django.core.files.uploadedfile import SimpleUploadedFile
from rest_framework.reverse import reverse


@pytest.mark.django_db
def test_create_image(api_client_business_owner, organization_factory):
    api_client, user = api_client_business_owner
    organization_factory(account_owner=user)
    image_path = 'media/oh.png'
    image = SimpleUploadedFile(
        name='test_image.png',
        content=open(image_path, 'rb').read(),
        content_type='image/png')

    url = reverse('organization-image-list')
    data = {
        'image': image
    }
    response = api_client.post(url, data, format='multipart')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_org(api_client_business_owner):
    api_client, _ = api_client_business_owner

    url = reverse('business-organizations')
    data = {
        'name': 'Chebacca Inc.',
        'description': 'May the force be wit you, dawg.',
        'representative': {'firstName': 'Luke', 'lastName': 'Skywalker'},
        'website': 'http://millennium@falcon.com',
        'foundedIn': 2001,
        'tourAvailability': 2,
        'location': {'country': 'JP'},
        'phoneNumber': '',
        'instagram': '',
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_patch_org(api_client_business_owner, organization_factory):
    api_client, user = api_client_business_owner
    organization_factory(account_owner=user)

    url = reverse('business-organizations')
    modified_message = 'May the force be wit you.'
    modified_first_name = 'Anakin'
    data = {
        'description': modified_message,
        'representative': {
            'firstName': modified_first_name,
            'lastName': 'Skywalker'
        },
    }
    response = api_client.patch(url, data, format='json')
    assert response.status_code == 202
    assert response.json()['description'] == modified_message
    assert response.json()[
        'representative']['firstName'] == modified_first_name


@pytest.mark.django_db
def test_get_product_list_of_org(api_client_general_user, product_factory):
    api_client, user = api_client_general_user
    product = product_factory()

    url = reverse('org-products-list', kwargs={'pk': product.organization.pk})
    response = api_client.get(url, format='json')
    assert response.status_code == 200
    assert response.json()[0]['id'] == product.id


@pytest.mark.django_db
def test_create_product(api_client_business_owner, organization_factory):
    api_client, account_owner = api_client_business_owner
    organization_factory(account_owner=account_owner)

    image_path = 'media/oh.png'
    image = SimpleUploadedFile(
        name='test_image.png',
        content=open(image_path, 'rb').read(),
        content_type='image/png')

    url = reverse('business-product-list')
    data = {
        'name': 'Shin Ramyeon',
        'description': 'Spicy af.',
        'url': 'http://millennium@falcon.com',
        'photo': image,
        'isPrimary': True,
    }
    response = api_client.post(url, data, format='multipart')
    assert response.status_code == 201


@pytest.mark.django_db
def test_create_review(api_client_general_user, user_factory, product_factory):
    api_client, user = api_client_general_user

    product = product_factory()
    url = reverse('review-list')
    data = {
        'title': 'Fuji Apple',
        'comment': 'Fresh af',
        'product': product.pk
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == 201


@pytest.mark.django_db
def test_get_org_list(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    for _ in range(5):
        organization_factory()
    url = reverse('organization-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['count'] == 5


@pytest.mark.django_db
def test_get_org_details_as_general_user(
        api_client_general_user, organization_factory):
    api_client, user = api_client_general_user

    org = organization_factory()
    user.favorites.add(org)
    url = reverse('organization-details', kwargs={'pk': org.pk})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['name'] == org.name
    assert response.json()['isFavorited'] is True


@pytest.mark.django_db
def test_get_org_details_as_anonymous_user(
        api_client, organization_factory):

    org = organization_factory()
    url = reverse('organization-details', kwargs={'pk': org.pk})
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['name'] == org.name
    assert response.json()['isFavorited'] is None


@pytest.mark.django_db
def test_filter_organizations(
        api_client_general_user, organization_factory, location_factory):
    api_client, _ = api_client_general_user

    tokyo = location_factory(state='Tokyo')
    new_york = location_factory(state='New York')
    los_angeles = location_factory(state='Los Angeles')
    seoul = location_factory(state='Seoul')
    organization_factory(name='example', location=tokyo)
    organization_factory(name='test', location=new_york)
    organization_factory(name='brewery', location=los_angeles)
    organization_factory(name='example-brewery', location=seoul)
    url = reverse('organization-filter')
    response = api_client.get(url, {'keyword': 'example'})
    assert response.status_code == 200
    assert 'example' in response.json()['results'][0]['name']
    assert 'example' in response.json()['results'][1]['name']
    assert response.json()['count'] == 2

    response = api_client.get(url, {'keyword': 'tokyo'})
    assert response.status_code == 200
    assert 'Tokyo' in response.json()['results'][0]['location']['state']
    assert response.json()['count'] == 1


@pytest.mark.skip(reason="takes too much time.")
@pytest.mark.django_db
def test_pagination(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    for _ in range(31):
        organization_factory()
    url = reverse('organization-filter')
    response = api_client.get(url, {'page': 2})
    assert response.status_code == 200
    assert response.json()['count'] == 31
    assert len(response.json()['results']) == 6


@pytest.mark.django_db
def test_create_favorite_org(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org = organization_factory()
    url = reverse('favorite-organizations')
    response = api_client.post(url, {'organization_id': org.pk})
    assert response.status_code == 201
    assert response.json()['organization'] == org.pk


@pytest.mark.django_db
def test_list_favorite_org(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    favorites = []
    for _ in range(4):
        org = organization_factory()
        url = reverse('favorite-organizations')
        response = api_client.post(url, {'organization_id': org.pk})
        favorites.append(response.json())
    url = reverse('favorite-organizations')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['favorites'] == favorites


@pytest.mark.django_db
def test_remove_favorite_org(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org_ids = []
    for _ in range(4):
        org = organization_factory()
        url = reverse('favorite-organizations')
        response = api_client.post(url, {'organization_id': org.pk})
        org_ids.append(org.pk)
    url = reverse('favorite-organizations')
    response = api_client.delete(url, {'organization_id': org_ids[0]})
    assert response.status_code == 204
    response = api_client.get(url)
    assert response.status_code == 200
    assert org_ids[0] not in response.json()['favorites']


@pytest.mark.django_db
def test_create_org_rating(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org = organization_factory()
    url = reverse('rate-organizations')
    response = api_client.post(url, {'organization_id': org.pk, 'stars': 3})
    assert response.status_code == 201
    assert response.json()['organization']['id'] == org.pk


@pytest.mark.django_db
def test_change_org_rating(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org = organization_factory()
    url = reverse('rate-organizations')
    response = api_client.post(url, {'organization_id': org.pk, 'stars': 3})
    assert response.status_code == 201
    assert response.json()['organization']['id'] == org.pk
    assert response.json()['organization']['rating'] == 3

    response = api_client.post(url, {'organization_id': org.pk, 'stars': 1})
    assert response.status_code == 201
    assert response.json()['organization']['rating'] == 1


@pytest.mark.django_db
def test_list_org_ratings(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    ratings = []
    for _ in range(4):
        org = organization_factory()
        url = reverse('rate-organizations')
        response = api_client.post(
            url, {'organization_id': org.pk, 'stars': randrange(1, 5)})
        ratings.append(response.json())
    url = reverse('rate-organizations')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['ratings'] == ratings


@pytest.mark.django_db
def test_remove_org_rating(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org_ids = []
    for _ in range(4):
        org = organization_factory()
        url = reverse('rate-organizations')
        response = api_client.post(url, {'organization_id': org.pk})
        org_ids.append(org.pk)
    url = reverse('rate-organizations')
    response = api_client.delete(url, {'organization_id': org_ids[0]})
    assert response.status_code == 204
    response = api_client.get(url)
    assert response.status_code == 200
    assert org_ids[0] not in response.json()['ratings']


@pytest.mark.django_db
def test_create_org_history(api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    org = organization_factory()
    url = reverse('org-history-list')
    response = api_client.post(url, {'organization_id': org.pk})
    assert response.status_code == 201
    assert response.json()['organization']['id'] == org.pk


@pytest.mark.skip(reason="takes too much time.")
@pytest.mark.django_db
def test_create_history_beyond_capacity(
        api_client_general_user, organization_factory):
    api_client, _ = api_client_general_user

    for _ in range(25):
        org = organization_factory()
        url = reverse('org-history-list')
        response = api_client.post(url, {'organization_id': org.pk})
        assert response.status_code == 201
    response = api_client.get(url)
    assert response.status_code == 200
    assert len(response.json()['results']) == OrgBrowsingHstry.MAX_CAPACITY + 1


@pytest.mark.django_db
def test_list_histories(
        api_client_general_user,
        organization_history_factory):
    api_client, user = api_client_general_user

    # The history created by the invocation of this factory method is linked to
    # another user, so it should not be included in the results.
    organization_history_factory()
    organization_history_factory(user=user)
    url = reverse('org-history-list')
    response = api_client.get(url)
    assert response.status_code == 200
    assert response.json()['count'] == 1


@pytest.mark.django_db
def test_patch_user(api_client_general_user):
    api_client, user = api_client_general_user

    data = {
        'firstName': 'Fresh af',
        'lastName': 'asdf'
    }
    response = api_client.patch('/api/users/me/', data, format='json')
    assert response.status_code == 200
