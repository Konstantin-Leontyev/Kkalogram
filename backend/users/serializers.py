from djoser.serializers import UserSerializer
from followers.models import Follow
from rest_framework import serializers


class CustomUserSerializer(UserSerializer):
    is_subscribed = serializers.SerializerMethodField()

    class Meta(UserSerializer.Meta):
        fields = ('is_subscribed', *UserSerializer.Meta.fields)

    def get_is_subscribed(self, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return Follow.objects.filter(user=user, author=obj.id).exists()
