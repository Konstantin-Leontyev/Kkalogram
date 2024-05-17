from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import FoodgramUserViewSet

app_name = 'api'

api = DefaultRouter()
api.register('users', FoodgramUserViewSet)

urlpatterns = [
    path('', include(api.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
