from rest_framework import serializers

from ads.models import Ad, Review


class AdSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'


class ReviewSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
