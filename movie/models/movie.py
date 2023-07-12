from django.core.validators import FileExtensionValidator
from django_countries.fields import CountryField
from django.db import models

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
    banner = models.ImageField(upload_to=upload_name, null=True, blank=True)
    photo = models.ImageField(upload_to=upload_name, null=True, blank=True)
    type = models.CharField(max_length=255, choices=TypeChoice.choices)
    video_url = models.URLField(null=True, blank=True)
    status = models.CharField(max_length=255, choices=StatusChoice.choices, default=StatusChoice.free)
    views = models.BigIntegerField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'role': User.RoleChoice.admin})
    is_active = models.BooleanField(default=False)
    genre = models.ManyToManyField(Genre)

    def __str__(self):
        return self.title

    @property
    def comments(self):
        return self.comment_set.all()

    @property
    def reviews(self):
        return self.review_set.all()

    class Meta:
        db_table = 'movie'


class MovieVideo(models.Model):
    video = models.FileField(upload_to=upload_name,
                             validators=[FileExtensionValidator(allowed_extensions=['mp4'])],
                             blank=True, null=True)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'video'
