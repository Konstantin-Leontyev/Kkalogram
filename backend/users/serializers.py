from djoser.serializers import UserSerializer
from followers.models import Follow
from rest_framework.serializers import SerializerMethodField


class CustomUserSerializer(UserSerializer):
    """Describes custom user serializer"""
    is_subscribed = SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('is_subscribed', *UserSerializer.Meta.fields)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()
