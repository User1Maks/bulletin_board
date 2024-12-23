from rest_framework import serializers

from announcements.models import Announcement, Review


class AnnouncementSerializers(serializers.ModelSerializer):

    class Meta:
        model = Announcement
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
