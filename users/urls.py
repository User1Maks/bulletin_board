from django.urls import path
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from users.apps import UsersConfig
from users.views import (UserCreateAPIView, UserDestroyAPIView,
                         UserListAPIView, UserRetrieveAPIView,
                         UserUpdateAPIView)

app_name = UsersConfig.name

urlpatterns = [
    path('register/', UserCreateAPIView.as_view(), name='register'),
    path('profile/', UserRetrieveAPIView.as_view(), name='profile'),
    path('update_profile/', UserUpdateAPIView.as_view(), name='user_profile'),
    path('delete/', UserDestroyAPIView.as_view(), name='user_delete'),
    path('list/', UserListAPIView.as_view(), name='user_list'),

    path('login/', TokenObtainPairView.as_view(
        permission_classes=(AllowAny,)
    ), name='token_obtain_pair'),

    path('token/refresh/', TokenRefreshView.as_view(
        permission_classes=(AllowAny,)
    ), name='token_refresh'),

]
