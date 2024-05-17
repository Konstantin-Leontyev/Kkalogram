from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import UserCreateSerializer, UserSerializer
from rest_framework.serializers import (CharField, EmailField, ModelSerializer,
                                        SerializerMethodField)
from rest_framework.validators import UniqueValidator

from api.constants import USERNAME_FIELD_MAX_LENGTH
from followers.models import Follow
from tags.models import Tag

User = get_user_model()


class FoodgramUserCreateSerializer(UserCreateSerializer):
    """Describes custom user create serializer class."""

    email = EmailField(
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            ),
        ],
    )
    username = CharField(
        max_length=USERNAME_FIELD_MAX_LENGTH,
        validators=[
            UniqueValidator(
                queryset=User.objects.all()
            ),
            UnicodeUsernameValidator(),
        ],
    )

    class Meta(UserCreateSerializer.Meta):
        """Describes custom user create serializer metaclass."""

        fields = (
            'email',
            'first_name',
            'id',
            'last_name',
            'password',
            'username',
        )
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True},
            'username': {'required': True},
        }


class FoodgramUserSerializer(UserSerializer):
    """Describes custom user serializer class."""

    is_subscribed = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        """Describes custom user serializer metaclass."""

        fields = (
            'email',
            'first_name',
            'id',
            'is_subscribed',
            'last_name',
            'username',
        )

    def get_is_subscribed(self, instance):
        """Returns the user's subscription status."""
        user = self.context.get('request').user
        return (user.is_authenticated
                and Follow.objects.filter(author=instance.id,
                                          user=user).exists())


class TagSerializer(ModelSerializer):
    """Describes tag serializer class."""

    class Meta:
        """Describes tag serializer metaclass."""

        model = Tag
        fields = (
            'color',
            'id',
            'name',
            'slug',
        )
