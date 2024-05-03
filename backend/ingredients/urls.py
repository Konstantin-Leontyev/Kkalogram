from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import IngredientsViewSet

app_name = 'ingredients'

ingredients = DefaultRouter()
ingredients.register('ingredients', IngredientsViewSet)

urlpatterns = [
    path('', include(ingredients.urls)),
]
