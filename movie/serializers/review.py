from rest_framework import serializers
from rest_framework.fields import HiddenField

from movie.models import Review


class ReviewCreateModelSerializer(serializers.ModelSerializer):
    author = HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Review
        exclude = ('id',)


class ReviewListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('author', 'text', 'rating', 'created_at')

