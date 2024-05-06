from drf_extra_fields.fields import Base64ImageField
from rest_framework.serializers import ModelSerializer, SerializerMethodField
from django.db.models import F

from ingredients.models import Ingredient
from tags.models import Tag
from tags.serializers import TagSerializer
from users.serializers import CustomUserSerializer
from .models import Recipe


class RecipeSerializer(ModelSerializer):
    """Describes Recipe serializer class."""

    image = Base64ImageField()
    tags = TagSerializer(many=True)
    author = CustomUserSerializer()
    ingredients = SerializerMethodField()
    # is_favorited = SerializerMethodField()
    # is_in_shopping_cart = SerializerMethodField()
    is_favorited = False
    is_in_shopping_cart = False

    class Meta:
        """Describes Recipe serializer metaclass."""

        model = Recipe
        # fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
        #           'is_in_shopping_cart', 'name', 'image', 'text',
        #           'cooking_time')
        fields = '__all__'

    def get_ingredients(self, obj):
        """Ingredients get function."""
        return obj.ingredients.values(
            'id', 'name', 'measurement_unit', amount=F('ingredient__amount')
        )

    def validate(self, attrs):
        tags = self.initial_data.get('tags')
        ingredients = self.initial_data.get('ingredients')

        # if not tags_ids or not ingredients:
        #     raise ValidationError("Недостаточно данных.")

        tags = Tag.objects.filter(id__in=tags)
        ingredients = Ingredient.objects.filter(id__in=ingredients)

        attrs.update(
            {
                'author': self.context.get('request').user,
                'ingredients': ingredients,
                'tags': tags,
            }
        )
        return attrs
