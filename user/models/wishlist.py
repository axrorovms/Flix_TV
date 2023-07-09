from django.db import models
from user.models import User
from movie.models import Movie
from shared.models import BaseModel


# Create your models here.


class Wishlist(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE)

    class Meta:
        db_table = 'wishlist'
