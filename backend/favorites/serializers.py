from core.serializers import UserRecipeSerializer
from .models import Favorite


class FavoriteSerializer(UserRecipeSerializer):
    """Describes a favorite serializer."""

    class Meta(UserRecipeSerializer.Meta):
        """Describes a favorite serializer metaclass."""

        model = Favorite
