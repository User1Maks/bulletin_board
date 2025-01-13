from django.utils import timezone
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import AllowAny

from ads.models import Ad, Review
from ads.paginators import AdPaginator, ReviewPaginator
from ads.permissions import IsAuthor
from ads.serializers import AdSerializers, ReviewSerializers
from users.permissions import IsAdminUser


# Endpoints объявления
class AdCreateAPIView(generics.CreateAPIView):
    """Endpoint создания объявления."""
    serializer_class = AdSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет автора объявления."""
        serializer.save(author=self.request.user)


class AdListAPIView(generics.ListAPIView):
    """Endpoint списка объявлений."""
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('price', 'author',)
    ordering_fields = ('-created_at',)
    search_fields = ('title',)
    pagination_class = AdPaginator
    permission_classes = [AllowAny]


class AdUserListAPIView(generics.ListAPIView):
    """Endpoint для вывода списка всех объявлений принадлежащих пользователю."""
    queryset = Ad.objects.all().order_by('-created_at')
    serializer_class = AdSerializers
    filter_backends = [DjangoFilterBackend, OrderingFilter, SearchFilter]
    filterset_fields = ('price',)
    ordering_fields = ('-created_at',)
    search_fields = ('title',)
    pagination_class = AdPaginator
    permission_classes = [IsAuthor | IsAdminUser]

    def get_queryset(self):
        """Возвращает пользователю, только его объявления."""
        return Ad.objects.filter(author=self.request.user).order_by(
            '-created_at')


class AdRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра объявления."""
    queryset = Ad.objects.all()
    serializer_class = AdSerializers


class AdUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для обновления объявления."""
    queryset = Ad.objects.all()
    serializer_class = AdSerializers
    permission_classes = [IsAuthor | IsAdminUser]

    def perform_update(self, serializer):
        """При изменении объекта добавляет поле updated_at."""
        instance = serializer.save()  # Сохраняем обновленные данные
        instance.updated_at = timezone.now()
        instance.save()


class AdDestroyAPIView(generics.DestroyAPIView):
    """Endpoint для удаления объявления."""
    queryset = Ad.objects.all()
    permission_classes = [IsAuthor | IsAdminUser]


# Endpoints отзыва
class ReviewCreateAPIView(generics.CreateAPIView):
    """Endpoint создания отзыва."""
    serializer_class = ReviewSerializers

    def perform_create(self, serializer):
        """Автоматически добавляет автора объявления."""
        ad_id = self.kwargs.get('ad_id')
        ad = Ad.objects.get(pk=ad_id)
        serializer.save(author=self.request.user, ad=ad)


class ReviewListAPIView(generics.ListAPIView):
    """Endpoint списка отзывов одного объявления."""
    queryset = Review.objects.all().order_by('-created_at')
    serializer_class = ReviewSerializers
    pagination_class = ReviewPaginator


class ReviewRetrieveAPIView(generics.RetrieveAPIView):
    """Endpoint просмотра отзыва."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers


class ReviewUpdateAPIView(generics.UpdateAPIView):
    """Endpoint для обновления отзыва."""
    queryset = Review.objects.all()
    serializer_class = ReviewSerializers
    permission_classes = [IsAuthor | IsAdminUser]

    def perform_update(self, serializer):
        """При изменении объекта отзыва, добавляется поле updated_at."""
        instance = serializer.save()
        instance.updated_at = timezone.now()
        instance.save()


class ReviewDestroyAPIView(generics.DestroyAPIView):
    """Endpoint для удаления отзыва."""
    queryset = Review.objects.all()
    permission_classes = [IsAuthor | IsAdminUser]
