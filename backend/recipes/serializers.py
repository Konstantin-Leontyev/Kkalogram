from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import ModelSerializer, SerializerMethodField

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import FoodgramUserSerializer

from .models import Recipe, RecipeIngredient


class RecipeIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


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

    author = FoodgramUserSerializer(read_only=True)
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

    def get_ingredients(self, instance):
        """Ingredients get function."""
        return instance.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )

    def get_is_favorited(self, instance):
        """Is favorite get function."""
        user = self.context.get('request').user
        return (user.is_authenticated
                and Recipe.objects.filter(favorites__user=user,
                                          id=instance.id).exists())

    def get_is_in_shopping_cart(self, instance):
        """Is in shopping cart get function."""
        user = self.context.get('request').user
        return (user.is_authenticated
                and Recipe.objects.filter(cart__user=user,
                                          id=instance.id).exists())


class RecipeSerializer(ReadRecipeSerializer):
    """Describes write recipe serializer class."""
    ingredients = RecipeIngredientSerializer(many=True,
                                             required=True)
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

        if not tags:
            raise ValidationError('Нужно указать хотя бы один тег.')
        if len(tags) != len(set(tags)):
            raise ValidationError(
                'Теги в рамках одного рецепта должны быть уникальными.'
            )

        if not ingredients:
            raise ValidationError('Для создания рецепта необходим '
                                  'как минимум 1 ингредиент.')
        ingredients = [ingredient['id'] for ingredient in ingredients]
        if len(ingredients) != len(set(ingredients)):
            raise ValidationError(
                'Ингредиенты в рамках одного рецепта'
                'должны быть уникальны.'
                'Объедините ингредиенты и повторите попытку.'
            )

        return data

    @atomic
    def create_ingredients(self, ingredients, recipe):
        """Create recipe ingredients."""
        RecipeIngredient.objects.bulk_create(
            [RecipeIngredient(
                ingredients=ingredient['id'],
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
        ingredients = validated_data.pop('ingredients')

        recipe = Recipe.objects.create(**validated_data)

        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe

    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        self.create_ingredients(ingredients, recipe=instance)
        return instance

    def to_representation(self, instance):
        return ReadRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
