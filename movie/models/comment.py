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

    def get_children(self):
        return self.children.all()


class LikeDislike(models.Model):
    user = models.ForeignKey('users.User', models.CASCADE)
    comment = models.ForeignKey('movie.Comment', models.CASCADE)
    is_like = models.BooleanField()

    class Meta:
        db_table = 'comment_likes'

