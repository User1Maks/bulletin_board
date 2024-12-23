from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSerializer(ModelSerializer):
    """Serializers для модели User."""
    class Meta:
        model = User
        fields = ('id', 'email',)


class UserDetailSerializer(ModelSerializer):
    """Serializers для просмотра профиля пользователя."""

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name', 'last_name', 'phone', 'avatar',
                  'role',)
