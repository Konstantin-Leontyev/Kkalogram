from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend

from .filters import RecipeFilter, AuthorFilter
from .models import Recipe
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    # filter_class = RecipeFilter
    filter_backends = (RecipeFilter, AuthorFilter)
    # filter_backends = [AuthorFilter]
    search_fields = ['author__id']
