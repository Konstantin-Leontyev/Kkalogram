from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
    """Describes tag serializer class."""

    class Meta:
        """Describes tag serializer metaclass."""

        model = Tag
        fields = '__all__'
        read_only_fields = ['__all__']
