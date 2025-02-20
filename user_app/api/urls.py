from django.urls import path
from .views import RegestrationView, LogOutView

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('registration/', RegestrationView.as_view(), name='registration'),
    path('logout/', LogOutView.as_view(), name='logout'),
]