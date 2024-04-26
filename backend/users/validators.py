import re

from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

unicode_username_validator = UnicodeUsernameValidator()


def me_value_username_validator(username: str):
    """Return error if username got "me" value."""
    if username == 'me':
        raise ValidationError(
            message='Использование me '
                    'в качестве имени пользователя недопустимо',
            params={'username': username}
        )


class NumberValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'\d', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум одну цифру.',
                code='password_no_number',
            )

    def get_help_text(self):
        return 'Ваш пароль должен содержать как минимум одну цифру.'


class UppercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[A-Z]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум '
                        'одну латинскую букву в верхнем регистре.',
                code='password_no_upper',
            )

    def get_help_text(self):
        return (
            'Ваш пароль должен содержать как минимум '
            'одну латинскую букву в верхнем регистре.'
        )


class LowercaseValidator(object):
    def validate(self, password, user=None):
        if not re.findall('[a-z]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимум '
                        'одну латинскую букву в нижнем регистре.',
                code='password_no_lower',
            )

    def get_help_text(self):
        return (
            'Ваш пароль должен содержать как минимум '
            'одну латинскую букву в верхнем регистре.'
        )


class SymbolValidator(object):
    def validate(self, password, user=None):
        if not re.findall(r'[()[\]{}|\\`~!@#$%^&*_\-+=;:\'",<>./?]', password):
            raise ValidationError(
                message='Пароль должен содержать как минимуму один символ: '
                        r'()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?',
                code='password_no_symbol',
            )

    def get_help_text(self):
        return (
            'Ваш пароль должен содержать как минимуму один символ: '
            r'()[]{}|\`~!@#$%^&*_-+=;:\'",<>./?'
        )
