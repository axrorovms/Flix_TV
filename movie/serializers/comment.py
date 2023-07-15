from rest_framework import serializers
from movie.models.comment import Comment, Like, DisLike


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'author', 'text', 'created_at')
        read_only_fields = ('id', 'created_at')


class ChildSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'children')

    def get_children(self, comment):
        if self.context.get('show_children'):
            children = Comment.objects.filter(parent=comment)
            serializer = CommentSerializer(children, many=True, read_only=True)
            return serializer.data
        return []

    def to_representation(self, instance: Comment):
        rep = super().to_representation(instance)
        rep['likes'] = instance.like_set.all().values('like').count()
        rep['dislikes'] = instance.dislike_set.all().values('dislike').count()
        return rep

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('comment',)





class DisLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisLike
        fields = ('comment',)