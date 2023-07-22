from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from movie.models import Movie
from users.models import User


class Comment(MPTTModel):
    author = models.ForeignKey('users.User', models.CASCADE)
    movie = models.ForeignKey('movie.Movie', models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = 'comment'


class LikeDislike(models.Model):
    user = models.ForeignKey('users.User', models.CASCADE)
    comment = models.ForeignKey('movie.Comment', models.CASCADE)
    is_like = models.BooleanField()

# class Like(models.Model):
#     comment = models.ForeignKey(Comment, models.CASCADE)
#     like = models.IntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'like'
#
#
# class DisLike(models.Model):
#     comment = models.ForeignKey(Comment, models.CASCADE)
#     dislike = models.IntegerField(default=0)
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     class Meta:
#         db_table = 'dislike'
