# from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer

# User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    class Meta(UserCreateSerializer.Meta):
        extra_kwargs = {
            'email': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'password': {'required': True, 'write_only': True},
        }
