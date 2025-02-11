from django.urls import path

from ads.apps import AdsConfig
from ads.views import (AdCreateAPIView, AdDestroyAPIView, AdListAPIView,
                       AdRetrieveAPIView, AdUpdateAPIView, AdUserListAPIView,
                       ReviewCreateAPIView, ReviewDestroyAPIView,
                       ReviewListAPIView, ReviewRetrieveAPIView,
                       ReviewUpdateAPIView)

app_name = AdsConfig.name

urlpatterns = [
    # Ads
    path('create/', AdCreateAPIView.as_view(), name='ad-create'),
    path('list/', AdListAPIView.as_view(), name='ad-list'),
    path('my-list/', AdUserListAPIView.as_view(), name='my-list'),
    path('detail/<int:pk>/', AdRetrieveAPIView.as_view(), name='ad-detail'),
    path('update/<int:pk>/', AdUpdateAPIView.as_view(), name='ad-update'),
    path('delete/<int:pk>/', AdDestroyAPIView.as_view(), name='ad-delete'),

    # Review
    path('<int:ad_id>/review-create/', ReviewCreateAPIView.as_view(),
         name='review-create'),
    path('<int:ad_id>/reviews/', ReviewListAPIView.as_view(),
         name='review-list'),
    path('review-detail/<int:pk>/', ReviewRetrieveAPIView.as_view(),
         name='review-detail'),
    path('review-update/<int:pk>/', ReviewUpdateAPIView.as_view(),
         name='review-update'),
    path('review-delete/<int:pk>/', ReviewDestroyAPIView.as_view(),
         name='review-delete'),
]
