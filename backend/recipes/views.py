from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart
from .filters import AuthorFilter, RecipeFilter
from .models import Recipe
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = [AuthorFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    search_fields = ['author__id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['get', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        if request.method == 'GET':
            return self.add_obj(Cart, request.user, pk)
        elif request.method == 'DELETE':
            return self.delete_obj(Cart, request.user, pk)
