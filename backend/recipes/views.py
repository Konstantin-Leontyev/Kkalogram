from carts.models import Cart
from django.http import HttpResponse
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.decorators import action
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import (HTTP_201_CREATED, HTTP_204_NO_CONTENT,
                                   HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND)
from rest_framework.viewsets import ModelViewSet

from .filters import AuthorFilter, RecipeFilter
from .models import Recipe, RecipeIngredient
from .permissions import IsAuthorOrReadOnly
from .serializers import RecipeSerializer, ShorthandRecipeSerializer


class RecipeViewSet(ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = [AuthorFilter, DjangoFilterBackend]
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    search_fields = ['author__id']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=[IsAuthenticated])
    def shopping_cart(self, request, pk):
        user = request.user
        status = HTTP_400_BAD_REQUEST
        if request.method == 'DELETE':
            status = HTTP_404_NOT_FOUND

        if not Recipe.objects.filter(id=pk).exists():
            return Response({
                'errors': f'Рецепта с id: {pk} не существует.'
            }, status=status)
        recipe = Recipe.objects.get(id=pk)
        recipe_in_cart = Cart.objects.filter(user=user, recipe=recipe).exists()

        if request.method == 'POST':
            if recipe_in_cart:
                return Response({
                    'errors': f'Рецепт с id: {pk} уже в списке покупок.'
                }, status=HTTP_400_BAD_REQUEST)
            Cart.objects.create(user=user, recipe=recipe)
            serializer = ShorthandRecipeSerializer(recipe)
            return Response(serializer.data, status=HTTP_201_CREATED)

        elif request.method == 'DELETE':
            if not recipe_in_cart:
                return Response({
                    'errors': f'Рецепта с id: {pk} нет в списке покупок.'
                }, status=HTTP_400_BAD_REQUEST)
            recipe.delete()
            return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated])
    def download_shopping_cart(self, request):
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
        registerFont(TTFont('Slimamif', 'Slimamif.ttf', 'UTF-8'))
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
