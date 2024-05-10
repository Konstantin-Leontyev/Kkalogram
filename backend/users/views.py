from django.contrib.auth import get_user_model
from djoser.conf import settings
from djoser.views import UserViewSet
from followers.models import Follow
from followers.serializers import FollowSerializer
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST)

from .serializers import CustomUserSerializer

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """Describes custom user view set."""

    serializer_class = CustomUserSerializer
    search_fields = ['email', 'username']

    def get_permissions(self):
        """Add custom permission for get requests on users/me endpoint."""
        if (self.action == 'me' and self.request
                and self.request.method == 'GET'):
            self.permission_classes = settings.PERMISSIONS.token_destroy
        return super().get_permissions()

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        user = request.user
        author = get_object_or_404(User, id=id)

        if user == author:
            return Response({
                'errors': 'Нельзя подписаться на самого себя.'
            }, status=HTTP_400_BAD_REQUEST)

        if Follow.objects.filter(user=user, author=author).exists():
            return Response({
                'errors': f'Вы уже подписаны на автора с id: {id}.'
            }, status=HTTP_400_BAD_REQUEST)

        if request.method == 'POST':
            serializer = FollowSerializer(author, data=request.data,
                                          context={"request": request})
            serializer.is_valid(raise_exception=True)
            Follow.objects.create(author=author, user=user)
            return Response(serializer.data, status=HTTP_201_CREATED)

        if request.method == 'DELETE':
            Follow.objects.get(ser=user, author=author).delete()
            return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)
