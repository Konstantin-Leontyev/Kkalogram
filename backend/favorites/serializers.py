from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer

from .models import Favorite
from recipes.serializers import RecipeSerializer


class FavoriteSerializer(ModelSerializer):
    """Describes a favorite serializer."""

    class Meta:
        """Describes a favorite serializer metaclass."""

        model = Favorite
        fields = ('user', 'recipe')

    def validate(self, data):
        """Validate the recipe is already in the user’s favorite."""
        if Favorite.objects.filter(user=data['user'], recipe=data['recipe']):
            raise ValidationError('Рецепт уже есть в избранном.')
        return data

    def to_representation(self, instance):
        """Change serializer to representation."""
        return RecipeSerializer(instance.recipe, context={
            'request': self.context.get('request')
        }).data
