from functools import wraps

from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .constants import MIN_INGREDIENT_AMOUNT
from .models import Recipe, RecipeIngredient


def hello_decorator(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return f(*args, **kwargs)

    return wrapper


class RecipeSerializer(ModelSerializer):
    """Describes recipe serializer class."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        """Describes recipe serializer metaclass."""

        fields = '__all__'
        model = Recipe
        read_only_fields = ['is_favorited', 'is_in_shopping_cart']

    def user_anonymous_check(self, function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            user = self.context.get('request').user
            if user.is_anonymous:
                return False
            return function(*args, **kwargs)

        return wrapper

    def get_ingredients(self, obj):
        """Ingredients get function."""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )

    def get_is_favorited(self, obj):
        """Is favorite get function."""
        return False

    def get_is_in_shopping_cart(self, obj):
        """Is in shopping cart get function."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(cart__user=user, id=obj.id).exists()

    def validate(self, data):
        """Validate ingredients and tags request lists."""

        image = self.initial_data.get('image')
        ingredients = self.initial_data.get('ingredients')
        tags = self.initial_data.get('tags')

        if not image:
            raise ValidationError('Прикрепите изображение.')

        if not ingredients:
            raise ValidationError('Для создания рецепта необходим '
                                  'как минимум 1 ингредиент.')
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

        if not tags:
            raise ValidationError('Нужно указать хотя бы один тег.')
        for id in tags:
            if not Tag.objects.filter(id=id).exists():
                raise ValidationError(f'Тега c id: {id} не существует.')
        if len(tags) != len(set(tags)):
            raise ValidationError(
                'Теги в рамках одного рецепта должны быть уникальными.'
            )

        return data

    @atomic
    def create_ingredients(self, ingredients, recipe):
        """Create recipe ingredients."""
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredients=Ingredient.objects.get(id=ingredient['id']),
                recipe=recipe,
                amount=ingredient['amount']
            ) for ingredient in ingredients]
        )

    @atomic
    def create(self, validated_data):
        """
        Recipe create function.

        .. Note:: Many to many fields present on the instance cannot be set
        until the recipe model is instantiated.
        """
        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe
