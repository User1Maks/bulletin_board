from rest_framework.permissions import BasePermission


class IsAdminUser(BasePermission):

    def has_permission(self, request, view):
        """Проверяет, относится ли пользователь к группе администраторов"""
        if request.user.is_authenticated:
            return request.user.role == 'admin'
        return False

    def has_object_permission(self, request, view, obj):
        """Администратор может редактировать и удалять любые объекты"""
        return request.user.role == 'admin'
