from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet

from carts.models import Cart
from carts.serializers import CartSerializer
from favorites.models import Favorite
from favorites.serializers import FavoriteSerializer

from .filters import AuthorFilter, RecipeFilter
from .models import Recipe, RecipeIngredient
from .permissions import IsAuthorOrReadOnly
from .serializers import PostUpdateRecipeSerializer


class RecipeViewSet(ModelViewSet):
    """Describes recipe view set."""

    queryset = Recipe.objects.all()
    serializer_class = PostUpdateRecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = [AuthorFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    search_fields = ['author__id']

    def perform_create(self, serializer):
        """Automatically setting recipe author field."""
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def favorite(self, request, pk):
        """Describes favorite url action logic."""
        serializer = FavoriteSerializer(
            data={'recipe': pk, 'user': request.user.id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @favorite.mapping.delete
    def delete_favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        favorite, _ = Favorite.objects.filter(
            user=request.user, recipe=recipe).delete()
        if not favorite:
            raise ValidationError(f'Рецепта с id: {pk} нет в избранном')
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        """Describes shopping_cart url action add logic."""
        serializer = CartSerializer(
            data={'recipe': pk, 'user': request.user.id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @shopping_cart.mapping.delete
    def delete_shopping_cart(self, request, pk):
        """Describes shopping_cart url action delete logic."""
        recipe = get_object_or_404(Recipe, pk=pk)
        shopping_cart, _ = Cart.objects.filter(
            user=request.user, recipe=recipe).delete()
        if not shopping_cart:
            raise ValidationError(f'Рецепта с id: {pk} нет в списке покупок')
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
        """Describes shopping cart download url action logic."""
        final_list = {}
        ingredients = RecipeIngredient.objects.filter(
            recipe__cart__user=request.user).values_list(
            'ingredients__name', 'ingredients__measurement_unit',
            'amount')
        for item in ingredients:
            name = item[0]
            if name not in final_list:
                final_list[name] = {
                    'measurement_unit': item[1],
                    'amount': item[2]
                }
            else:
                final_list[name]['amount'] += item[2]
        registerFont(TTFont('Slimamif', 'backend/Slimamif.ttf', 'UTF-8'))
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = (
            'attachment; filename="shopping_list.pdf"'
        )
        page = Canvas(response)
        page.setFont('Slimamif', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('Slimamif', size=16)
        height = 750
        for i, (name, data) in enumerate(final_list.items(), 1):
            page.drawString(75, height, (f'<{i}> {name} - {data["amount"]}, '
                                         f'{data["measurement_unit"]}'))
            height -= 25
        page.showPage()
        page.save()
        return response
