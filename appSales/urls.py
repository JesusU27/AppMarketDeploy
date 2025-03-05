"""
URL configuration for appSales project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


#SWAGGER UI
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

#esquema de la API
schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version="v1",
        description="Documentación de la API",
    ),
    public=True,
    permission_classes=[AllowAny], #permisos para acceder a la documentación
    
    
)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('tasks/', include('tasks.urls')), #path personalizado para las urls de la entidad "Tasks"
    #Path para obtener token
    #path('api/token/', TokenObtainPairView.as_view(), name='token-obtain-pair'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

schema_view.authentication_classes = []
schema_view.security_definitions = {
    "Bearer": {
        "type": "http",
        "scheme": "bearer",
        "bearerFormat": "JWT",
        "description": "Ingresa tu token en el formato: Bearer <token>",
    }
}
schema_view.security = [{"Bearer": []}]

