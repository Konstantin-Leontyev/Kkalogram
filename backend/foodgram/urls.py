from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('ingredients.urls', namespace='ingredients')),
    path('api/', include('tags.urls', namespace='tags')),
    path('api/', include('users.urls', namespace='users')),
]
