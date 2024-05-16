from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from recipes.serializers import RecipeSerializer

from .models import UserRecipeModel


class UserRecipeSerializer(ModelSerializer):
    """Describes a cart serializer."""

    class Meta:
        """Describes a cart serializer metaclass."""

        model = UserRecipeModel
        fields = ('user', 'recipe')

    def validate(self, data):
        """Validate the recipe is already in the user’s cart."""
        if self.Meta.model.objects.filter(recipe=data['recipe'],
                                          user=data['user']):
            raise ValidationError('Рецепт уже есть в корзине.')
        return data

    def to_representation(self, instance):
        """Change serializer to representation."""
        return RecipeSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data
