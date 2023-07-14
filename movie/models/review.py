from django.db import models
from movie.models import Movie
from user.models import User


class Review(models.Model):
    author = models.ForeignKey(User, models.CASCADE)
    movie = models.ForeignKey(Movie, models.CASCADE)
    text = models.TextField()
    rating = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'

