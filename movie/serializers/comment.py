from rest_framework import serializers

from movie.models import LikeDislike
from movie.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class LikeDislikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = LikeDislike
        fields = '__all__'


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChildSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'movie_id', 'children')