from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import F
from django.db.transaction import atomic
from djoser.serializers import UserCreateSerializer, UserSerializer
from drf_extra_fields.fields import Base64ImageField
from rest_framework.exceptions import ValidationError
from rest_framework.relations import PrimaryKeyRelatedField
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        SerializerMethodField)
from rest_framework.validators import UniqueValidator

from api.constants import USERNAME_FIELD_MAX_LENGTH
from carts.models import Cart
from core.serializers import UserRecipeSerializer
from favorites.models import Favorite
from followers.models import Follow
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
from tags.models import Tag

User = get_user_model()


class CartSerializer(UserRecipeSerializer):
    """Describes a cart serializer."""

    class Meta(UserRecipeSerializer.Meta):
        """Describes a cart serializer metaclass."""

        model = Cart


class FavoriteSerializer(UserRecipeSerializer):
    """Describes a favorite serializer."""

    class Meta(UserRecipeSerializer.Meta):
        """Describes a favorite serializer metaclass."""

        model = Favorite


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Describes custom user create serializer class."""

    email = EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            ),
        ],
    )
    username = CharField(
        max_length=USERNAME_FIELD_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            ),
            UnicodeUsernameValidator(),
        ],
    )

    class Meta(UserCreateSerializer.Meta):
        """Describes custom user create serializer metaclass."""

        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
            'username': {'required': True},
        }


class FoodgramUserSerializer(UserSerializer):
    """Describes custom user serializer class."""

    is_subscribed = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        """Describes custom user serializer metaclass."""

        fields = (
            'email',
            'first_name',
            'id',
            'is_subscribed',
            'last_name',
            'username',
        )

    def get_is_subscribed(self, instance):
        """Returns the user's subscription status."""
        user = self.context.get('request').user
        return (user.is_authenticated
                and Follow.objects.filter(author=instance.id,
                                          user=user).exists())


class FollowSerializer(FoodgramUserSerializer):
    """Describes follow serializer class."""

    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(FoodgramUserSerializer.Meta):
        """Describes follow serializer metaclass."""

        fields = ('recipes_count', 'recipes',
                  *FoodgramUserSerializer.Meta.fields)
        read_only_fields = ['email', 'first_name', 'last_name', 'username']

    def get_recipes_count(self, instance):
        """Get following user recipes count."""
        return instance.recipes.count()

    def get_recipes(self, instance):
        """Get following user limit recipes."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = instance.recipes.all()
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except TypeError:
                raise ValidationError('Ошибка выполнения запроса. '
                                      'Значение `recipes_limit` '
                                      'должно быть числом.')
        return RecipeSerializer(
            recipes,
            many=True,
            read_only=True,
        ).data


class FollowCreateSerializer(ModelSerializer):
    """Describes follow create serializer class."""

    class Meta:
        """Describes follow create serializer metaclass."""

        model = Follow
        fields = ('user', 'author')

    def to_representation(self, instance):
        """Change serializer to representation."""
        return FollowSerializer(
            instance.author,
            context={'request': self.context.get('request')}).data

    def validate(self, data):
        """
        Validate the user is already subscribed on author
        and self subscription.
        """
        user = self.initial_data['user']
        author = self.initial_data['author']

        if user == author:
            raise ValidationError('Нельзя подписаться на самого себя.')

        if Follow.objects.filter(user=user, author=author):
            raise ValidationError(
                'Вы уже подписаны на этого автора')
        return data


class IngredientSerializer(ModelSerializer):
    """Describes ingredient serializer class."""

    class Meta:
        """Describes ingredient serializer metaclass."""

        model = Ingredient
        fields = (
            'id',
            'measurement_unit',
            'name',
        )


class TagSerializer(ModelSerializer):
    """Describes tag serializer class."""

    class Meta:
        """Describes tag serializer metaclass."""

        model = Tag
        fields = (
            'color',
            'id',
            'name',
            'slug',
        )


class RecipeIngredientSerializer(ModelSerializer):
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())

    class Meta:
        fields = ('id', 'amount')
        model = RecipeIngredient


class RecipeSerializer(ModelSerializer):
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


class ListRetrieveRecipeSerializer(ModelSerializer):
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


class PostUpdateRecipeSerializer(ModelSerializer):
    """Describes write recipe serializer class."""

    author = FoodgramUserSerializer(read_only=True)
    image = Base64ImageField()
    ingredients = RecipeIngredientSerializer(many=True,
                                             required=True)
    tags = PrimaryKeyRelatedField(many=True,
                                  queryset=Tag.objects.all())

    class Meta:
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
        model = Recipe

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

    @staticmethod
    @atomic
    def create_ingredients(ingredients, recipe):
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
        """
        Recipe create function.

        .. Note:: You should clear the instance fields before
        setting new values.
        """
        ingredients = validated_data.pop('ingredients')
        instance.ingredients.clear()
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        self.create_ingredients(ingredients, recipe=instance)
        return instance

    def to_representation(self, instance):
        """Change serializer to representation."""
        return ListRetrieveRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data
