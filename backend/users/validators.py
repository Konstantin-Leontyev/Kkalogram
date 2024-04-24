from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.exceptions import ValidationError

unicode_username_validator = UnicodeUsernameValidator()


def me_value_username_validator(username: str):
    """Return error if username got "me" value."""
    if username == 'me':
        raise ValidationError(
            message='Использование "me" '
                    'в качестве имени пользователя недопустимо',
            params={'username': username}
        )
