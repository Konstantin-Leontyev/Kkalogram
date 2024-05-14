from django.core.exceptions import ValidationError

from ingredients.models import Ingredient
from recipes.constants import MIN_INGREDIENT_AMOUNT


def ingredients_validator(ingredients):
    ingredients_id = []
    for ingredient in ingredients:
        id, amount = ingredient.values()
        if not Ingredient.objects.filter(id=id).exists():
            raise ValidationError(f'Ингредиента c id: {id} не существует.')
        if amount < MIN_INGREDIENT_AMOUNT:
            ingredient_object = Ingredient.objects.get(id=id)
            raise ValidationError(
                'Минимальное количество ингредиента '
                f'{ingredient_object.name}: '
                f'{MIN_INGREDIENT_AMOUNT} '
                f'{ingredient_object.measurement_unit}'
            )
        ingredients_id.append(id)
    if len(ingredients_id) != len(set(ingredients_id)):
        raise ValidationError(
            'Ингредиенты в рамках одного рецепта'
            'должны быть уникальны.'
            'Объедините ингредиенты и повторите попытку.'
        )


def tags_validator(tags):
    if not tags:
        raise ValidationError('Нужно указать хотя бы один тег.')
    if len(tags) != len(set(tags)):
        raise ValidationError(
            'Теги в рамках одного рецепта должны быть уникальными.'
        )
