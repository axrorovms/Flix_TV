from django.db import models
from shared.models import upload_name


class Genre(models.Model):
    title = models.CharField(max_length=255)
    image = models.ImageField(upload_to=upload_name, null=True, blank=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'genre'
