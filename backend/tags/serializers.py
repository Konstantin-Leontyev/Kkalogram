from rest_framework.serializers import ModelSerializer

from .models import Tag


class TagSerializer(ModelSerializer):
    """Describes tag serializer."""

    class Meta:
        model = Tag
        fields = '__all__'
