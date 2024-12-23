from rest_framework.generics import (CreateAPIView, DestroyAPIView,
                                     ListAPIView, RetrieveAPIView,
                                     UpdateAPIView)
from rest_framework.permissions import AllowAny

from users.models import User
from users.serializers import UserDetailSerializer, UserSerializer


class UserCreateAPIView(CreateAPIView):
    """Endpoint создания пользователя"""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)

    def perform_create(self, serializer):
        """Зашифровывает пароли в базе данных и делает пользователя активным."""
        user = serializer.save(is_active=True)
        user.set_password(user.password)
        user.save()


class UserListAPIView(ListAPIView):
    """Endpoint для просмотра списка пользователей."""
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveAPIView(RetrieveAPIView):
    """Endpoint просмотра профиля пользователя."""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer

    def get_object(self):
        return self.request.user


class UserUpdateAPIView(UpdateAPIView):
    """Endpoint для изменения данных пользователя."""
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer


class UserDestroyAPIView(DestroyAPIView):
    """Endpoint для удаления пользователя."""
    queryset = User.objects.all()
