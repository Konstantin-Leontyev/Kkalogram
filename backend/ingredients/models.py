from django.db.models import CharField, Model, UniqueConstraint

from core.constants import MEASUREMENT_UNIT_MAX_LENGTH, NAME_FIELD_MAX_LENGTH


class Ingredient(Model):
    """Describes ingredient model class."""

    measurement_unit = CharField(
        max_length=MEASUREMENT_UNIT_MAX_LENGTH,
        verbose_name='Единица измерения',
    )
    name = CharField(
        max_length=NAME_FIELD_MAX_LENGTH,
        verbose_name='Ингредиент',
    )

    class Meta:
        """Describes ingredient model metaclass."""

        ordering = ['name']
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='Ингредиент уже существует.',
            )
        ]

    def __str__(self):
        return self.name
