from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from .views import CreateUserView

from django.conf import settings

app_name = "user"
BASE_URL = settings.BASE_API_URL

urlpatterns = [
    path('register/', CreateUserView.as_view(), name='register'),

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/', TokenRefreshView.as_view(), name='token_refresh'),
]
