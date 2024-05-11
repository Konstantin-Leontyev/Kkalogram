from recipes.serializers import ShorthandRecipeSerializer
from rest_framework.fields import SerializerMethodField
from users.serializers import CustomUserSerializer


class FollowSerializer(CustomUserSerializer):
    """Describes follow serializer class."""

    recipes_count = SerializerMethodField()
    recipes = SerializerMethodField()

    class Meta(CustomUserSerializer.Meta):
        """Describes follow serializer metaclass."""

        fields = ('recipes_count', 'recipes',
                  *CustomUserSerializer.Meta.fields)
        read_only_fields = ['email', 'first_name', 'last_name', 'username']

    def get_recipes_count(self, obj):
        """Get following user recipes count."""
        return obj.recipes.count()

    def get_recipes(self, obj):
        """Get following user limit recipes."""
        request = self.context.get('request')
        limit = request.GET.get('recipes_limit')
        recipes = obj.recipes.all()
        return ShorthandRecipeSerializer(
            recipes[:int(limit)] if limit else recipes,
            many=True,
            read_only=True,
        ).data
