from django.apps import AppConfig
from django.contrib.auth.apps import AuthConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
    verbose_name = 'Пользователи'


class UsersAuthConfig(AuthConfig):
    verbose_name = 'Группы'
