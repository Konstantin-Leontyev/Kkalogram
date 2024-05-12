from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ingredients.models import Ingredient
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe, RecipeIngredient
from .validators import tags_validator, ingredients_validator


class ShorthandRecipeSerializer(ModelSerializer):
    """Describes a shorthand recipe serializer."""

    class Meta:
        """Describes shorthand recipe serializer metaclass."""

        fields = ('id', 'name', 'image', 'cooking_time')
        model = Recipe
        read_only_fields = ['__all__']


class RecipeSerializer(ShorthandRecipeSerializer):
    """Describes recipe serializer class."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta(ShorthandRecipeSerializer.Meta):
        """Describes recipe serializer metaclass."""

        fields = '__all__'
        read_only_fields = ['is_favorited', 'is_in_shopping_cart']

    def get_ingredients(self, obj):
        """Ingredients get function."""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )

    def get_is_favorited(self, obj):
        """Is favorite get function."""
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Recipe.objects.filter(favorites__user=user, id=obj.id).exists()

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

        ingredients_validator(ingredients)
        tags_validator(tags)

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
