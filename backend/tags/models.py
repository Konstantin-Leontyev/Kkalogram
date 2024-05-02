from django.db.models import CharField, Model, SlugField

from .constants import COLOR_CHOICES


class Tag(Model):
    """Describes tag model."""

    name = CharField(
        max_length=10,
        unique=True,
        verbose_name='Тег'
    )
    color = CharField(
        choices=COLOR_CHOICES,
        max_length=7,
        unique=True,
        verbose_name='Цвет'
    )
    slug = SlugField(
        max_length=10,
        unique=True,
        verbose_name='Слаг')

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
