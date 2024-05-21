from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FoodgramUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)
from core.views import BaseAPIRootView

app_name = 'api'


class RuDefaultRouter(DefaultRouter):
    """Represent api page on local language."""

    APIRootView = BaseAPIRootView


api = RuDefaultRouter()
api.register('users', FoodgramUserViewSet)
api.register('ingredients', IngredientViewSet)
api.register('recipes', RecipeViewSet)
api.register('tags', TagViewSet)

urlpatterns = [
    path('', include(api.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
