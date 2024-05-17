from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrReadOnly(BasePermission):
    """Describes custom author or read only permission."""

    def has_object_permission(self, request, view, obj):
        """Describes permission on object level."""
        return request.method in SAFE_METHODS or obj.author == request.user
