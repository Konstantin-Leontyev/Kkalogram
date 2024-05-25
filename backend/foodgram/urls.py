from django.contrib import admin
from django.urls import include, path

from api.views import RecipeViewSet

urlpatterns = [
    path('sentry-debug/', RecipeViewSet),
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]
