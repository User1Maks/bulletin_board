from rest_framework.permissions import BasePermission

from ads.models import Ad, Review


class IsAuthorAd(BasePermission):
    def has_permission(self, request, view):
        """Проверяет, является ли пользователь автором объявления"""

        if request.user and view.kwargs.get('pk'):
            ad = Ad.objects.get(id=view.kwargs.get('pk'))
            return request.user == ad.author
        return False


class IsAuthorReview(BasePermission):
    def has_permission(self, request, view):
        """Проверяет, является ли пользователь автором отзыва"""

        if request.user and view.kwargs.get('pk'):
            review = Review.objects.get(id=view.kwargs.get('pk'))
            return request.user == review.author
        return False
