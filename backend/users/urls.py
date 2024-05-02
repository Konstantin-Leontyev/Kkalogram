from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import CustomUserViewSet

app_name = 'users'

users = DefaultRouter()
users.register('users', CustomUserViewSet)

urlpatterns = [
    path('', include(users.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
