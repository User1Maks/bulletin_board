from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

from .views import PasswordResetConfirm, PasswordResetView

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/', UserRetrieveAPIView.as_view(), name='profile'),
    path('update-profile/', UserUpdateAPIView.as_view(), name='user-profile'),
    path('delete/', UserDestroyAPIView.as_view(), name='user-delete'),
    path('list/', UserListAPIView.as_view(), name='user-list'),

    path('login/', TokenObtainPairView.as_view(
        permission_classes=(AllowAny,)
    ), name='token-obtain-pair'),
    path('token/refresh/', TokenRefreshView.as_view(
        permission_classes=(AllowAny,)
    ), name='token-refresh'),

    path('reset-password/',
         PasswordResetView.as_view(), name='reset-password'),
    path('reset-password-confirm/',
         PasswordResetConfirm.as_view(), name='reset-password-confirm'),
]
