from django.db import models
from movie.models import Movie
from users.models import User
from django.shortcuts import get_object_or_404


class Review(models.Model):
    author = models.ForeignKey(User, models.CASCADE)
    movie = models.ForeignKey(Movie, models.CASCADE)
    text = models.TextField()
    rating = models.SmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'

    @classmethod
    def get_review(cls, slug):
        return Review.objects.filter(movie=get_object_or_404(Movie, slug=slug))
