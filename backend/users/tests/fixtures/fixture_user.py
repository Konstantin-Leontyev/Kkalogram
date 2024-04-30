import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def signup_url():
    return '/api/users/'


@pytest.fixture
def token_url():
    return '/api/auth/token/'


@pytest.fixture
def users_url():
    return '/api/users/'


@pytest.fixture
def users_me_url():
    return '/api/users/me/'


@pytest.fixture
def fields():
    return [
        'email',
        'first_name',
        'last_name',
        'password',
        'username'
    ]


@pytest.fixture
def blank_data():
    return {
        'email': '',
        'first_name': '',
        'last_name': '',
        'username': '',
        'password': '',
    }


@pytest.fixture
def valid_data():
    return {
        'email': 'valid_email@foodgram.ru',
        'first_name': 'valid_name',
        'last_name': 'valid_surname',
        'password': '45wef1dE(',
        'username': 'valid_username'
    }


@pytest.fixture
def valid_response():
    return {
        'id': 1,
        'email': 'valid_email@foodgram.ru',
        'first_name': 'valid_name',
        'last_name': 'valid_surname',
        'username': 'valid_username'
    }


@pytest.fixture
def invalid_data():
    return {
        'email': 'invalid_email',
        'first_name': 'valid_name',
        'last_name': 'valid_surname',
        'username': 'invalid username',
        'password': 'invalid_password'
    }


@pytest.fixture
def admin(django_user_model):
    return django_user_model.objects.create_user(
        email='testadmin@foodgram.ru',
        is_staff='1',
        first_name='test_admin_name',
        last_name='test_admin_surname',
        password='45wef1dE(',
        username='Test_Admin'
    )


@pytest.fixture
def admin_token(admin):
    token = AccessToken.for_user(admin)
    return {
        'access': str(token),
    }


@pytest.fixture
def admin_client(admin_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {admin_token["access"]}')
    return client


@pytest.fixture
def superuser(django_user_model):
    return django_user_model.objects.create_superuser(
        email='testsuperuser@foodgram.ru',
        # is_staff='1',
        # is_superuser='1',
        first_name='test_superuser_name',
        last_name='test_superuser_surname',
        password='45wef1dE(',
        username='Test_Superuser'
    )


@pytest.fixture
def superuser_token(superuser):
    token = AccessToken.for_user(superuser)
    return {
        'access': str(token),
    }


@pytest.fixture
def superuser_client(superuser_token):
    client = APIClient()
    client.credentials(
        HTTP_AUTHORIZATION=f'Bearer {superuser_token["access"]}'
    )
    return client


@pytest.fixture
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='testuser@foodgram.ru',
        first_name='test_user_name',
        last_name='test_user_surname',
        password='45wef1dE(',
        username='Test_User'
    )


@pytest.fixture
def user_token(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(user_token):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {user_token["access"]}')
    return client

