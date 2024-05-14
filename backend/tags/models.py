from colorfield.fields import ColorField
from django.db.models import CharField, Model, SlugField

from .constants import (HEX_FIELD_MAX_LENGTH, NAME_FIELD_MAX_LENGTH,
                        SLUG_FIELD_MAX_LENGTH)


class Tag(Model):
    """Describes tag model class."""

    color = ColorField(
        max_length=HEX_FIELD_MAX_LENGTH,
        unique=True,
        verbose_name='Цвет',
    )
    name = CharField(
        max_length=NAME_FIELD_MAX_LENGTH,
        unique=True,
        verbose_name='Тег',
    )
    slug = SlugField(
        max_length=SLUG_FIELD_MAX_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        """Describes tag model metaclass."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name
