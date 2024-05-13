from rest_framework.fields import SerializerMethodField

from recipes.serializers import ShorthandRecipeSerializer
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
        if limit:
            try:
                recipes = recipes[:int(limit)]
            except TypeError:
                print('Ошибка выполнения запроса.'
                      'Значение `recipes_limit` должно быть числом.')
        return ShorthandRecipeSerializer(
            recipes,
            many=True,
            read_only=True,
        ).data
