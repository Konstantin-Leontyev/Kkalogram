from django.contrib import admin
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from core.views import BaseAPIRootView


class RuDefaultRouter(DefaultRouter):
    """Represent api page on local language."""

    APIRootView = BaseAPIRootView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
