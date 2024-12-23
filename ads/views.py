from datetime import datetime

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from ads.models import Ad, Review
from ads.paginators import AdPaginator
from ads.serializers import AdSerializers, ReviewSerializers


# Endpoints объявления
class AdCreateAPIView(generics.CreateAPIView):
    """Endpoint создания объявления"""
    serializer_class = AdSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет автора объявления"""
        serializer.save(author=self.request.user)


class AdListAPIView(generics.ListAPIView):
    """Endpoint списка объявлений"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('price', 'author',)
    ordering_fields = ('-created_at',)
    search_fields = ('title',)
    pagination_class = AdPaginator
    permission_classes = (AllowAny,)


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра объявления"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializers


class AdUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для обновления объявления"""
    queryset = Ad.objects.all()
    serializer_class = AdSerializers


class AdDestroyAPIView(generics.DestroyAPIView):
    """Endpoint для удаления объявления"""
    queryset = Ad.objects.all()


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
