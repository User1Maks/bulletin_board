from rest_framework.permissions import BasePermission


class IsAuthorAd(BasePermission):

    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором объявления"""
        return request.user == obj.author


class IsAuthorReview(BasePermission):
    def has_object_permission(self, request, view, obj):
        """Проверяет, является ли пользователь автором отзыва"""
        return request.user == obj.author
