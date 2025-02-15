from django.urls import path, include

# import views
from rest_framework import routers
from .views import CustomTokenRefreshView


from tasks import views




#api versions
router = routers.DefaultRouter()
router.register(r'items', views.TaskView, 'items')

urlpatterns = [
    path("api/v1/", include(router.urls)),
    path("api/v1/auth/", views.AuthView.as_view(), name="auth"),
    path("api/v1/register/", views.RegisterView.as_view(), name="register"),
    path("api/v1/user/", views.UserView.as_view(), name="user"),
    path("api/v1/token/refresh/", CustomTokenRefreshView.as_view(), name='token_refresh'),
    path("api/v1/receipts/", views.ReceiptView.as_view(), name="receipts")
    
]

#AuthView no es un ViewSet, sino una vista basada en clases (APIView).
# Por lo tanto, no puedes registrarla directamente con el router de DRF.
#En lugar de eso, debes agregarla manualmente en urlpatterns.

