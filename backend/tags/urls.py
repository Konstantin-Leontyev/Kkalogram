from django.urls import include, path
from rest_framework.routers import DefaultRouter
from tags.views import TagsViewSet

app_name = 'tags'

tags = DefaultRouter()
tags.register('tags', TagsViewSet)

urlpatterns = [
    path('', include(tags.urls)),
]
