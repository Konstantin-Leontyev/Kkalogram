from rest_framework.viewsets import ModelViewSet

from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # filter_class = AuthorAndTagFilter
    # permission_classes = [IsOwnerOrReadOnly]
