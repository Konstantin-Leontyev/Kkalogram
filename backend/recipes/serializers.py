from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe, RecipeIngredient
from .validators import ingredients_validator, tags_validator


class ShorthandRecipeSerializer(ModelSerializer):
    """Describes a shorthand recipe serializer."""

    class Meta:
        """Describes shorthand recipe serializer metaclass."""

        fields = (
            'cooking_time',
            'id',
            'image',
            'name',
        )
        model = Recipe
        read_only_fields = ['__all__']


class ReadRecipeSerializer(ModelSerializer):
    """Describes read recipe serializer."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        """Describes read recipe serializer metaclass."""

        fields = (
            'author',
            'cooking_time',
            'id',
            'image',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'tags',
            'text',
        )
        model = Recipe

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


class RecipeSerializer(ReadRecipeSerializer):
    """Describes write recipe serializer class."""
    # ingredients = PrimaryKeyRelatedField(many=True,
    #                                      queryset=Ingredient.objects.all())
    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())

    class Meta(ReadRecipeSerializer.Meta):
        """Describes write recipe serializer metaclass."""

        fields = (
            'author',
            'cooking_time',
            'id',
            'image',
            'ingredients',
            'name',
            'tags',
            'text',
        )

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
        tags = validated_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ReadRecipeSerializer(instance, context=context).data
