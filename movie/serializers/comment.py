from rest_framework import serializers
from rest_framework.fields import HiddenField

from movie.models import LikeDislike
from movie.models.comment import Comment


class CommentSerializer(serializers.ModelSerializer):
    author = HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('id', 'created_at')


class LikeDislikeSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = LikeDislike
        fields = '__all__'

    def create(self, validated_data):
        comment_id = validated_data.get('comment')
        is_like = validated_data.get('is_like')

        try:
            instance = LikeDislike.objects.get(user_id=self.context['request'].user.id, comment_id=comment_id)
            if instance.is_like == is_like:
                instance.delete()
                return {"message": "deleted"}
            instance.is_like = not instance.is_like
            instance.save()
            return {"message": "updated"}
        except LikeDislike.DoesNotExist:
            instance = LikeDislike.objects.create(user_id=self.context['request'].user.id, **validated_data)
            instance.save()

            return {"message": "added"}


class RecursiveField(serializers.Serializer):
    def to_representation(self, value):
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


# LikeDislikeSerializer(context={'request': self.context['request']})
#
# sayt.com
# request
# # localhost:8000/kjhfkdsjh/
# www.uz


class ChildSerializer(serializers.ModelSerializer):
    children = RecursiveField(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'author', 'text', 'movie_id', 'children')