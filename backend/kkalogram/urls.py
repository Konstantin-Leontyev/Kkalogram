from django.conf.urls import url
from django.contrib import admin
from django.urls import include, path
from drf_yasg.openapi import Contact, Info, License
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny

schema_view = get_schema_view(
    Info(title="Kkalogram API",
         default_version='v1',
         description="Документация API проекта Kkalogram",
         contact=Contact(email="info@kkalogram.ru"),
         license=License(name="BSD License"),
         ),
    public=True,
    permission_classes=[AllowAny],
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls', namespace='api')),
]

urlpatterns += [
    url(r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^swagger/$', schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),
    url(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
