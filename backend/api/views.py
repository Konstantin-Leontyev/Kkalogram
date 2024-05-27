import io

from django.contrib.auth import get_user_model
from django.db.models import Sum
from django.http import FileResponse
from django_filters.rest_framework import DjangoFilterBackend
from djoser.conf import settings
from djoser.views import UserViewSet
from reportlab.pdfbase.pdfmetrics import registerFont
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen.canvas import Canvas
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_204_NO_CONTENT
from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet

from carts.models import Cart
from favorites.models import Favorite
from followers.models import Follow
from ingredients.models import Ingredient
from recipes.models import Recipe, RecipeIngredient
from tags.models import Tag

from .filters import AuthorFilter, IngredientFilter, RecipeFilter
from .paginators import LimitPageNumberPagination
from .permissions import IsAuthorOrReadOnly
from .serializers import (CartSerializer, FavoriteSerializer,
                          FollowCreateSerializer, FollowSerializer,
                          FoodgramUserSerializer, IngredientSerializer,
                          PostUpdateRecipeSerializer, TagSerializer)

User = get_user_model()


class FoodgramUserViewSet(UserViewSet):
    """Describes custom user view set."""

    pagination_class = LimitOffsetPagination
    serializer_class = FoodgramUserSerializer
    search_fields = ['email', 'username']

    def get_permissions(self):
        """Add custom permission for get requests on users/me endpoint."""
        if (self.action == 'me' and self.request
                and self.request.method == 'GET'):
            self.permission_classes = settings.PERMISSIONS.token_destroy
        return super().get_permissions()

    @action(detail=True, methods=['post'],
            permission_classes=[IsAuthenticated])
    def subscribe(self, request, id):
        """Describes subscription create url action logic."""
        author = get_object_or_404(User, id=id)
        serializer = FollowCreateSerializer(
            data={'user': request.user.id, 'author': author.id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=HTTP_201_CREATED)

    @subscribe.mapping.delete
    def delete_subscription(self, request, id):
        """Describes subscription delete action logic."""
        author = get_object_or_404(User, id=id)
        subscription, _ = Follow.objects.filter(
            user=request.user, author=author).delete()
        if not subscription:
            raise ValidationError(f'Вы не подписаны на автор с id: {id}')
        return Response(status=HTTP_204_NO_CONTENT)

    @action(detail=False, permission_classes=[IsAuthenticated])
    def subscriptions(self, request):
        """Describes subscriptions url action logic."""
        user = request.user
        queryset = User.objects.filter(following__user=user)
        pages = self.paginate_queryset(queryset)
        serializer = FollowSerializer(pages,
                                      many=True,
                                      context={'request': request})
        return self.get_paginated_response(serializer.data)


class IngredientViewSet(ReadOnlyModelViewSet):
    """Describes read only ingredient view set class."""

    pagination_class = None
    filter_backends = [IngredientFilter]
    search_fields = ['^name']
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.all()


class RecipeViewSet(ModelViewSet):
    """Describes recipe view set."""

    queryset = Recipe.objects.all()
    serializer_class = PostUpdateRecipeSerializer
    filterset_class = RecipeFilter
    filter_backends = [AuthorFilter, DjangoFilterBackend]
    pagination_class = LimitPageNumberPagination
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
        ingredients = (
            RecipeIngredient.objects.filter(recipe__cart__user=request.user.id)
            .values('ingredients__name', 'ingredients__measurement_unit')
            .annotate(amount=Sum('amount'))
        )
        registerFont(TTFont('Slimamif', 'backend/Slimamif.ttf', 'UTF-8'))
        buffer = io.BytesIO()
        page = Canvas(buffer)
        page.setFont('Slimamif', size=24)
        page.drawString(200, 800, 'Список ингредиентов')
        page.setFont('Slimamif', size=16)
        height = 750
        for index, ingredient in enumerate(ingredients, 1):
            name, measurement_unit, amount = ingredient.values()
            page.drawString(75, height, (f'<{index}> {name} - {amount}, '
                                         f'{measurement_unit}'))
            height -= 25
        page.showPage()
        page.save()
        buffer.seek(0)
        return FileResponse(buffer,
                            as_attachment=True,
                            filename='shopping_list.pdf')


class TagViewSet(ReadOnlyModelViewSet):
    """Describes read only tag view set class."""

    pagination_class = None
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
