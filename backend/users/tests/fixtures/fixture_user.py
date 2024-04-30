import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


@pytest.fixture
def url_signup():
    return '/api/users/'


@pytest.fixture
def url_token():
    return '/api/auth/token/'


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
def valid_data():
    return {
        'email': 'valid@foodgram.ru',
        'first_name': 'valid_name',
        'last_name': 'valid_surname',
        'password': '1dE(45wef',
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
def user(django_user_model):
    return django_user_model.objects.create_user(
        email='testuser@foodgram.ru',
        first_name='name',
        last_name='surname',
        password='1234567',
        username='TestUser',
    )


@pytest.fixture
def token_user(user):
    token = AccessToken.for_user(user)
    return {
        'access': str(token),
    }


@pytest.fixture
def user_client(token_user):
    client = APIClient()
    client.credentials(HTTP_AUTHORIZATION=f'Bearer {token_user["access"]}')
    return client
