from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db.models import (SET_NULL, CharField, ForeignKey, ImageField,
                              ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)

from ingredients.models import Ingredient
from tags.models import Tag

from .constants import NAME_FIELD_MAX_LENGTH

User = get_user_model()


class Recipe(Model):
    """Describes follow model class."""

    name = CharField(
        max_length=NAME_FIELD_MAX_LENGTH,
        verbose_name='Название',
    )
    author = ForeignKey(
        User,
        null=True,
        on_delete=SET_NULL,
        verbose_name='Автор',
    )
    text = TextField('Описание')
    image = ImageField(
        upload_to='recipes/',
        verbose_name='Изображение',
    )
    cooking_time = PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=1,
                message='Минимальное время приготовления 1 мин.'
            )
        ],
        verbose_name='Время приготовления',
    )
    ingredients = ManyToManyField(
        Ingredient,
        through='IngredientInRecipe',
        verbose_name='Ингредиенты'
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Теги'
    )

    class Meta:
        """Describes follow model metaclass."""

        related_name = 'recipes',
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
