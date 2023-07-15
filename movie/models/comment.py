from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from movie.models import Movie
from user.models import User


class Comment(MPTTModel):
    author = models.ForeignKey(User, models.CASCADE)
    movie = models.ForeignKey(Movie, models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')

    class Meta:
        db_table = 'comment'


class Like(models.Model):
    comment = models.ForeignKey(Comment, models.CASCADE)
    like = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'like'


class DisLike(models.Model):
    comment = models.ForeignKey(Comment, models.CASCADE)
    Dislike = models.IntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'dislike'
