from django.contrib.auth import get_user_model
from django.core.validators import (MinValueValidator,
                                    validate_image_file_extension)
from django.db.models import (CASCADE, SET_NULL, CharField, ForeignKey,
                              ImageField, ManyToManyField, Model,
                              PositiveSmallIntegerField, TextField)
from ingredients.models import Ingredient
from tags.models import Tag

from .constants import MIN_COOKING_TIME, NAME_FIELD_MAX_LENGTH

User = get_user_model()


class Recipe(Model):
    """Describes recipe model class."""

    author = ForeignKey(
        User,
        null=True,
        on_delete=SET_NULL,
        verbose_name='Автор',
    )
    cooking_time = PositiveSmallIntegerField(
        validators=[
            MinValueValidator(
                limit_value=MIN_COOKING_TIME,
                message='Минимальное время приготовления 1 мин.'
            )
        ],
        verbose_name='Время приготовления',
    )
    image = ImageField(
        upload_to='recipes/',
        validators=[
            validate_image_file_extension
        ],
        verbose_name='Изображение',
    )
    ingredients = ManyToManyField(
        Ingredient,
        through='RecipeIngredient',
        verbose_name='Ингредиенты',
    )
    name = CharField(
        max_length=NAME_FIELD_MAX_LENGTH,
        verbose_name='Название',
    )
    tags = ManyToManyField(
        Tag,
        verbose_name='Теги',
    )
    text = TextField(
        verbose_name='Описание',
    )

    class Meta:
        """Describes follow model metaclass."""

        default_related_name = 'recipes'
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'


class RecipeIngredient(Model):
    """Describes recipe ingredient model class."""

    amount = PositiveSmallIntegerField(
        verbose_name="Количество",
    )
    ingredients = ForeignKey(
        Ingredient,
        on_delete=CASCADE,
        related_name='ingredient',
        verbose_name='Ингредиенты',
    )
    recipe = ForeignKey(
        Recipe,
        on_delete=CASCADE,
        related_name='recipe',
        verbose_name='Рецепты',
    )

    class Meta:
        """Describes recipe ingredient model metaclass."""

        verbose_name = 'Количество'
