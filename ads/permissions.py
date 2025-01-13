from rest_framework.permissions import BasePermission


class IsAuthor(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором объявления или отзыва."""
        return request.user == obj.author
