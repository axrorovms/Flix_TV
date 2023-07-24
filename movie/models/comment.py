from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from movie.models import Movie
from users.models import User


# class CommentManager(models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(parent=None).all()


class Comment(MPTTModel):
    author = models.ForeignKey('users.User', models.CASCADE)
    movie = models.ForeignKey('movie.Movie', models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = 'comment'

    def children(self):
        return Comment.objects.filter(parent=self)
    #
    # objects = CommentManager()


class LikeDislike(models.Model):
    user = models.ForeignKey('users.User', models.CASCADE)
    comment = models.ForeignKey('movie.Comment', models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        db_table = 'comment_likes'

