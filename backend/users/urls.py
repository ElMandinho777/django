from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserApiViewSet, UserView, RegisterUserView, SoapCountryView

router = DefaultRouter()
router.register('users', UserApiViewSet)
urlpatterns = [
    path('', include(router.urls)),
    path('auth/me/', UserView.as_view(), name='me'),
    path('auth/register/', RegisterUserView.as_view(), name='register'),
    path('soap/country/', SoapCountryView.as_view(), name='soap_country'),
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
