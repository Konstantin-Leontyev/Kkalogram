import pytest
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import AccessToken


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
        'email': 'valid@yamdb.fake',
        'username': 'valid_username',
        'last_name': 'username',
        'first_name': 'valid',
        'password': '1dE(45wef'
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
        email='testuser@yamdb.fake',
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
