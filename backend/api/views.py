from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT

from followers.models import Follow
from followers.serializers import FollowCreateSerializer, FollowSerializer

from api.serializers import FoodgramUserSerializer

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    """Describes custom user view set."""

    serializer_class = FoodgramUserSerializer
    search_fields = ['email', 'username']

    def get_permissions(self):
        """Add custom permission for get requests on users/me endpoint."""
        if (self.action == 'me' and self.request
                and self.request.method == 'GET'):
            self.permission_classes = settings.PERMISSIONS.token_destroy
        return super().get_permissions()

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Describes subscription create url action logic."""
        author = get_object_or_404(User, id=id)
        serializer = FollowCreateSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscription(self, request, id):
        """Describes subscription delete action logic."""
        author = get_object_or_404(User, id=id)
        subscription, _ = Follow.objects.filter(
            user=request.user, author=author).delete()
        if not subscription:
            raise ValidationError(f'Вы не подписаны на автор с id: {id}')
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Describes subscriptions url action logic."""
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)
