from core.serializers import UserRecipeSerializer
from .models import Cart


class CartSerializer(UserRecipeSerializer):
    """Describes a cart serializer."""

    class Meta(UserRecipeSerializer.Meta):
        """Describes a cart serializer metaclass."""

        model = Cart
