from django.apps import AppConfig
from django.contrib.auth.apps import AuthConfig


class UsersConfig(AppConfig):
    """An application configuration class automatically generated by Django."""

    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Список пользователей'


class UsersAuthConfig(AuthConfig):
    """Custom auth application configuration. For verbose name change only."""

    verbose_name = 'Список групп'
