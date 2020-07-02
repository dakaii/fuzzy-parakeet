import pytest
from rest_framework.reverse import reverse


@pytest.mark.django_db
@pytest.mark.parametrize(
    'username, password, status_code', [
        ('example', 'johnpassword', 200),
        ('user@example.com', 'strong_pass', 401),
    ]
)
def test_login_data_validation(
        username, password, status_code, api_client):
    url = reverse('jwt-create')
    data = {
        'username': username,
        'password': password
    }
    response = api_client.post(url, data, format='json')
    assert response.status_code == status_code
