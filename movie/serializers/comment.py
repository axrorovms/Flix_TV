from rest_framework import serializers
from movie.models.comment import Comment, Like, DisLike


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'author', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')
        required_fields = ('id',)


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class ChildSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'children', 'movie_id')



class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('id', 'comment', 'like', 'user')
        read_only_fields = ('id',)


class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ('id', 'comment', 'dislike', 'user')
        read_only_fields = ('id',)