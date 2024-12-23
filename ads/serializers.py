from rest_framework import serializers

from ads.models import Ad, Review


class AdSerializers(serializers.ModelSerializer):

    class Meta:
        model = Ad
        fields = '__all__'
        read_only_fields = ('author', 'created_at', 'updated_at',)


class ReviewSerializers(serializers.ModelSerializer):

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('author', 'ad', 'created_at', 'updated_at',)
