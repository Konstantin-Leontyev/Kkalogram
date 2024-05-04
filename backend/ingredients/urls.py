from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientViewSet

app_name = 'ingredients'

ingredients = DefaultRouter()
ingredients.register('ingredients', IngredientViewSet)

urlpatterns = [
    path('', include(ingredients.urls)),
]
