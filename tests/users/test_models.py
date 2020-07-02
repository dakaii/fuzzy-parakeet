import pytest


@pytest.mark.django_db
def test_user_user_factory(user_factory):
    user = user_factory(email='lennon0@thebeatles.com',
                        password='johnpassword', has_default_group=True)
    assert user.email == 'lennon0@thebeatles.com'
    assert user.check_password('johnpassword')
    assert user.groups.count() == 1
