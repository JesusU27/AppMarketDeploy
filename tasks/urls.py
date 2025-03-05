from django.urls import path, include

# import views
from rest_framework import routers
from .views import CustomTokenRefreshView


from tasks import views




#router de DRF para registrar vistas
router = routers.DefaultRouter()
router.register(r'items', views.TaskView, 'items')


urlpatterns = [
    path("api/v1/", include(router.urls)), #url por defecto
    path("api/v1/auth/", views.AuthView.as_view(), name="auth"), #url de autenticación
    path("api/v1/register/", views.RegisterView.as_view(), name="register"),#url de registro
    path("api/v1/user/", views.UserView.as_view(), name="user"), #url de vista de usuarios
    path("api/v1/token/refresh/", CustomTokenRefreshView.as_view(), name='token_refresh'), #url de refresco de token
    path("api/v1/receipts/", views.ReceiptView.as_view(), name="receipts") #url de vista de recetas
    
]

#AuthView no es un ViewSet, sino una vista basada en clases (APIView).
# Por lo tanto, no se puede registrar directamente con el router de DjangoRestFramework.
#En lugar de eso, se debe agregar manualmente en urlpatterns.

