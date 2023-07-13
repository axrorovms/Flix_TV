from django.db import models
from django_countries.fields import CountryField
from django.core.validators import FileExtensionValidator

from shared.models import BaseModel, upload_name
from movie.models import Genre
from user.models import User


class Movie(BaseModel):
    class TypeChoice(models.TextChoices):
        movie = "Movie", "movie"
        live = "Live", "live"
        series = "Series", "series"

    class StatusChoice(models.TextChoices):
        free = "Free", "free"
        premium = "Premium", "premium"

    title = models.CharField(max_length=255)
    description = models.TextField(default=0)
    release_year = models.IntegerField(default=0)
    film_time_duration = models.IntegerField(default=0)
    age_limit = models.IntegerField(default=0)
    country = CountryField(default='AF')
    banner = models.ImageField(upload_to=upload_name, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_name, null=True, blank=True)
    type = models.CharField(max_length=255, choices=TypeChoice.choices)
    video_url = models.URLField(default='http://127.0.0.1:8000')
    status = models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.free)
    views = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'movie'


class MovieVideo(models.Model):
    video = models.FileField(upload_to=upload_name,
                             validators=[FileExtensionValidator(allowed_extensions=['jpg'])],
                             blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'video'
