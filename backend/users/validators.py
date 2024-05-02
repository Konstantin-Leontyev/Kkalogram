import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

unicode_username_validator = UnicodeUsernameValidator()


def me_value_username_validator(username: str):
    """Raises error if username got "me" value."""
    if username == 'me':
        raise ValidationError(
            message='Использование me '
                    'в качестве имени пользователя недопустимо',
            params={'username': username}
        )


class NumberValidator(object):
    """
    Custom user password field validator.
    Check password got at least one number.

    .. Note:: To use validator set dict:
    {
        'NAME': 'users.validators.NumberValidator',
    },

    into AUTH_PASSWORD_VALIDATORS list in Django project settings.py
    """

    def validate(self, password, user=None):
        """Raises error if password has no at least one number."""
        if not re.findall(r'\d', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум одну цифру.',
                code='password_no_number',
            )

    def get_help_text(self):
        """Sets help text to NumberValidator."""
        return 'Ваш пароль должен содержать как минимум одну цифру.'


class UppercaseValidator(object):
    """
    Custom user password field validator.
    Check password got at least one letter in upper case.

    .. Note:: To use validator set dict:
    {
        'NAME': 'users.validators.UppercaseValidator',
    },

    into AUTH_PASSWORD_VALIDATORS list in Django project settings.py
    """

    def validate(self, password, user=None):
        """Raises error if password does not contain letter in upper case."""
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум '
                        'одну латинскую букву в верхнем регистре.',
                code='password_no_upper',
            )

    def get_help_text(self):
        """Sets help text to UppercaseValidator."""
        return (
            'Ваш пароль должен содержать как минимум '
            'одну латинскую букву в верхнем регистре.'
        )


class LowercaseValidator(object):
    """
    Custom user password field validator.
    Check password got at least one letter in lower case.

    .. Note:: To use validator set dict:
    {
        'NAME': 'users.validators.SymbolValidator',
    },

    into AUTH_PASSWORD_VALIDATORS list in Django project settings.py
    """

    def validate(self, password, user=None):
        """Raises error if password does not contain letter in lower case."""
        if not re.findall('[a-z]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум '
                        'одну латинскую букву в нижнем регистре.',
                code='password_no_lower',
            )

    def get_help_text(self):
        """Sets help text to LowercaseValidator."""
        return (
            'Ваш пароль должен содержать как минимум '
            'одну латинскую букву в верхнем регистре.'
        )


class SymbolValidator(object):
    """
    Custom user password field validator.
    Check password got at least one symbol.

    .. Note:: To use validator set dict:
    {
        'NAME': 'users.validators.SymbolValidator',
    },

    into AUTH_PASSWORD_VALIDATORS list in Django project settings.py
    """

    def validate(self, password, user=None):
        """Raises error if password does not contain symbol."""
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимуму один символ: '
                        r'()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?',
                code='password_no_symbol',
            )

    def get_help_text(self):
        """Sets help text to SymbolValidator."""
        return (
            'Ваш пароль должен содержать как минимуму один символ: '
            r'()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?'
        )
