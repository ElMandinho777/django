from django.contrib import admin
from django.urls import include, path, re_path
from django.views.generic import RedirectView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

schema_view = get_schema_view(openapi.Info(
    title='CentiStore API', default_version='v1',
    description='Tienda de videojuegos y accesorios. Usuarios con correo, telefono y JWT. Token de acceso: 30 minutos. El CRUD de usuarios requiere un administrador.'
), public=True, permission_classes=[AllowAny], authentication_classes=[])

urlpatterns = [
    path('', RedirectView.as_view(url='/swagger/', permanent=False)),
    path('admin/', admin.site.urls),
    path('api/v1/', include('users.urls')),
    path('api/v1/', include('products.urls')),
    path('api/', include('products.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='legacy-token'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='legacy-refresh'),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]
admin.site.site_header = 'CentiStore Administracion'
admin.site.site_title = 'CentiStore'
admin.site.index_title = 'Usuarios y catalogo'
