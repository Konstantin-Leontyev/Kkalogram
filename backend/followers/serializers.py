from rest_framework.exceptions import ValidationError
from rest_framework.fields import SerializerMethodField
from rest_framework.serializers import ModelSerializer

from api.serializers import FoodgramUserSerializer
from followers.models import Follow
from recipes.serializers import RecipeSerializer


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
                print('Ошибка выполнения запроса.'
                      'Значение `recipes_limit` должно быть числом.')
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
