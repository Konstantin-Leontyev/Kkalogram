from django.db.models import CharField, Model, SlugField

from .constants import (COLOR_CHOICES, NAME_CHOICES, SLUG_CHOICES,
                        TAG_FIELDS_MAX_LENGTH)


class Tag(Model):
    """Describes tag model class."""

    color = CharField(
        choices=COLOR_CHOICES,
        max_length=TAG_FIELDS_MAX_LENGTH,
        unique=True,
        verbose_name='Цвет',
    )
    name = CharField(
        choices=NAME_CHOICES,
        max_length=TAG_FIELDS_MAX_LENGTH,
        unique=True,
        verbose_name='Тег',
    )
    slug = SlugField(
        choices=SLUG_CHOICES,
        max_length=TAG_FIELDS_MAX_LENGTH,
        unique=True,
        verbose_name='Слаг',
    )

    class Meta:
        """Describes tag model metaclass."""

        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __repr__(self):
        return self.name
    