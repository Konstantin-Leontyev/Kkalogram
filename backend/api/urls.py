from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (FoodgramUserViewSet, IngredientViewSet, RecipeViewSet,
                       TagViewSet)

app_name = 'api'

api = DefaultRouter()
api.register('users', FoodgramUserViewSet)
api.register('ingredients', IngredientViewSet)
api.register('recipes', RecipeViewSet)
api.register('tags', TagViewSet)

urlpatterns = [
    path('', include(api.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
