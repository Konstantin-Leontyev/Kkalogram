from djoser.conf import settings
from djoser.views import UserViewSet

from .serializers import CustomUserSerializer


class CustomUserViewSet(UserViewSet):
    """Describes custom user view set."""

    serializer_class = CustomUserSerializer
    search_fields = ('email', 'username',)

    def get_permissions(self):
        """Add custom permission for get requests on users/me endpoint."""
        if (self.action == 'me' and self.request
                and self.request.method == 'GET'):
            self.permission_classes = settings.PERMISSIONS.token_destroy
        return super().get_permissions()
