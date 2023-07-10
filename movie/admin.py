from django.contrib import admin
from movie.models.movie import Movie
from movie.models.genre import Genre
from movie.models.comment import Comment

admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Comment)
