from django.contrib.auth.models import AbstractUser
from django.db import models

# from ..foodgram.settings import USERNAME_MAX_LENGTH
from .validators import (
    me_value_username_validator,
    unicode_username_validator,
)


class User(AbstractUser):
    """Describes user model."""

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=150,
        unique=True,
        validators=[
            me_value_username_validator,
            unicode_username_validator,
        ])

    REQUIRED_FIELDS = [
        'first_name',
        'id',
        'last_name',
        'username',
    ]

    USERNAME_FIELD = 'email'

    class Meta:
        default_related_name = 'users'
        ordering = ('username', 'email')
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __repr__(self):
        """Returns text representation of the class."""
        return self.get_full_name()
