from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Cart
from recipes.serializers import RecipeSerializer


class CartSerializer(ModelSerializer):
    """Describes a cart serializer."""

    class Meta:
        """Describes a cart serializer metaclass."""

        model = Cart
        fields = ('user', 'recipe')

    def validate(self, data):
        """Validate the recipe is already in the user’s cart."""
        if Cart.objects.filter(user=data['user'], recipe=data['recipe']):
            raise ValidationError('Рецепт уже есть в корзине.')
        return data

    def to_representation(self, instance):
        """Change serializer to representation."""
        return RecipeSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data
