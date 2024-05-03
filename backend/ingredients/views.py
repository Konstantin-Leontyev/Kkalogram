from rest_framework.viewsets import ReadOnlyModelViewSet

from .filters import IngredientFilter
from .models import Ingredient
from .serializers import IngredientSerializer


class IngredientsViewSet(ReadOnlyModelViewSet):
    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ['name']
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()
