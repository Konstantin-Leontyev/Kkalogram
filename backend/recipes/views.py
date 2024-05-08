from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet

from .filters import AuthorFilter, RecipeFilter
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = (AuthorFilter, DjangoFilterBackend)
    search_fields = ['author__id']
