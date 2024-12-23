from rest_framework import generics

from announcements.models import Announcement, Review
from announcements.serializers import (AnnouncementSerializers,
                                       ReviewSerializers)


# Endpoints объявления
class AnnouncementCreateAPIView(generics.CreateAPIView):
    """Endpoint создания объявления"""
    serializer_class = AnnouncementSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет автора объявления"""
        serializer.save(author=self.request.user)


class AnnouncementListAPIView(generics.ListAPIView):
    """Endpoint списка объявлений"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializers


class AnnouncementRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра объявления"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializers


class AnnouncementUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для обновления объявления"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializers


class AnnouncementDestroyAPIView(generics.DestroyAPIView):
    """Endpoint для удаления объявления"""
    queryset = Announcement.objects.all()


# Endpoints отзыва
class ReviewCreateAPIView(generics.CreateAPIView):
    """Endpoint создания отзыва"""
    serializer_class = ReviewSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет автора объявления"""
        serializer.save(author=self.request.user)


class ReviewListAPIView(generics.ListAPIView):
    """Endpoint списка отзывов"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для обновления отзыва"""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Endpoint для удаления отзыва"""
    queryset = Review.objects.all()
