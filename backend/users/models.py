from django.contrib.auth.models import AbstractUser
from django.db import models

from backend.foodgram.settings import USERNAME_MAX_LENGTH
from backend.users.validators import (
    me_value_username_validator,
    unicode_username_validator,
)


class User(AbstractUser):
    """Describes user model."""
#
    USERNAME_FIELD = 'email'

    email = models.EmailField(
        'Адрес электронной почты',
        unique=True,
    )
    username = models.CharField(
        'Имя пользователя',
        max_length=USERNAME_MAX_LENGTH,
        unique=True,
        validators=[
            me_value_username_validator,
            unicode_username_validator,
        ])

    REQUIRED_FIELDS = [
        # 'email',
        'first_name',
        'id',
        'last_name',
        'username',
    ]

    class Meta:
        default_related_name = 'users'
        ordering = ('username', 'email')
        verbose_name = 'Пользователя'
        verbose_name_plural = 'Пользователи'

    def __repr__(self):
        """Returns text representation of the class."""
        return self.get_full_name()
