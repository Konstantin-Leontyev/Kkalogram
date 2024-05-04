from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TagViewSet

app_name = 'tags'

tags = DefaultRouter()
tags.register('tags', TagViewSet)

urlpatterns = [
    path('', include(tags.urls)),
]
