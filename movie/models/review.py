from django.db import models
from django.db.models import Count

from movie.models import Movie
from users.models import User


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
        movie = Movie.objects.filter(slug=slug).first()
        if movie:
            reviews = cls.objects.filter(movie_id=movie.id).all()
            if reviews:
                return reviews
        return []