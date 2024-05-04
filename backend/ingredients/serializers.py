from rest_framework.serializers import ModelSerializer

from .models import Ingredient


class IngredientSerializer(ModelSerializer):
    """Describes ingredient serializer class."""

    class Meta:
        """Describes ingredient serializer metaclass."""

        model = Ingredient
        fields = '__all__'
        read_only_fields = ['__all__']
