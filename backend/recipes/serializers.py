from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.transaction import atomic
from drf_extra_fields.fields import Base64ImageField
from ingredients.models import Ingredient
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer

from .models import Recipe, RecipeIngredient


class RecipeSerializer(ModelSerializer):
    """Describes Recipe serializer class."""

    author = CustomUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = SerializerMethodField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        """Describes Recipe serializer metaclass."""

        fields = '__all__'
        model = Recipe
        read_only_fields = ['is_favorited', 'is_in_shopping_cart']

    def get_ingredients(self, obj):
        """Ingredients get function."""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )

    def get_is_favorited(self, obj):
        """Is favorited get function."""
        return False

    def get_is_in_shopping_cart(self, obj):
        """Is in shopping_cart get function."""
        return False

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
            if amount < 1:
                ingredient_object = Ingredient.objects.get(id=id)
                raise ValidationError(
                    f'Минимальное количество ингредиента '
                    f'{ingredient_object.name}: '
                    f'1 {ingredient_object.measurement_unit}'
                )
            ingredients_id.append(id)
        if len(ingredients_id) != len(set(ingredients_id)):
            raise ValidationError(
                'Ингредиенты в рамках одного рецепта'
                'должны быть уникальны.'
                'Объедините ингредиенты и повторите попытку.'
            )

        if not tags:
            raise ValidationError({'tags': 'Нужно выбрать хотя бы один тег!'})
        for id in tags:
            if not Tag.objects.filter(id=id).exists():
                raise ValidationError(f'Тега c id: {id} не существует.')
        if len(tags) != len(set(tags)):
            raise ValidationError({'tags': 'Теги должны быть уникальными!'})

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
        author = self.context.get('request').user
        validated_data.update({'author': author})

        recipe = Recipe.objects.create(**validated_data)

        tags = self.initial_data.pop('tags')
        ingredients = self.initial_data.pop('ingredients')
        recipe.tags.set(tags)
        self.create_ingredients(ingredients, recipe)
        return recipe
