from djoser.views import UserViewSet
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from backend.users.serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    serializer_class = CustomUserSerializer
    filter_backends = (SearchFilter,)
    search_fields = ('email', 'username',)

    @action(('GET',), detail=False, permission_classes=(IsAuthenticated,))
    def me(self, request, *args, **kwargs):
        """Функция работы с адресом me."""
        self.get_object = self.get_instance
        return self.retrieve(request, *args, **kwargs)
