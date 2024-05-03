# from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    # permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    # filter_backends = [IngredientSearchFilter]
    search_fields = ['name']
