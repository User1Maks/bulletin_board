from django.urls import path

from announcements.apps import AnnouncementsConfig
from announcements.views import (AnnouncementCreateAPIView,
                                 AnnouncementDestroyAPIView,
                                 AnnouncementListAPIView,
                                 AnnouncementRetrieveAPIView,
                                 AnnouncementUpdateAPIView,
                                 ReviewCreateAPIView, ReviewDestroyAPIView,
                                 ReviewListAPIView, ReviewRetrieveAPIView,
                                 ReviewUpdateAPIView)

app_name = AnnouncementsConfig.name

urlpatterns = [
    # Announcement
    path('create/', AnnouncementCreateAPIView.as_view(),
         name='announcement-create'),
    path('list/', AnnouncementListAPIView.as_view(),
         name='announcement-list'),
    path('detail/<int:pk>/', AnnouncementRetrieveAPIView.as_view(),
         name='announcement-detail'),
    path('update/<int:pk>/', AnnouncementUpdateAPIView.as_view(),
         name='announcement-update'),
    path('delete/<int:pk>/', AnnouncementDestroyAPIView.as_view(),
         name='announcement-delete'),

    # Review
    path('review-create/', ReviewCreateAPIView.as_view(),
         name='review-create'),
    path('review-list/', ReviewListAPIView.as_view(),
         name='review-list'),
    path('review-detail/<int:pk>/', ReviewRetrieveAPIView.as_view(),
         name='review-detail'),
    path('review-update/<int:pk>/', ReviewUpdateAPIView.as_view(),
         name='review-update'),
    path('review-delete/<int:pk>/', ReviewDestroyAPIView.as_view(),
         name='review-delete'),
]
