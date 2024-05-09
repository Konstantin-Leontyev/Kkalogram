from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import RecipeViewSet

app_name = 'recipes'

recipes = DefaultRouter()
recipes.register('recipes', RecipeViewSet)

urlpatterns = [
    path('', include(recipes.urls)),
]
