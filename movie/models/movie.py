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
    description = models.TextField()
    release_year = models.IntegerField()
    film_time_duration = models.IntegerField()
    age_limit = models.IntegerField()
    country = CountryField()
    banner = models.ImageField(upload_to=upload_name)
    photo = models.ImageField(upload_to=upload_name)
    type = models.CharField(max_length=255, choices=TypeChoice.choices)
    video_url = models.URLField()
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
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'video'
