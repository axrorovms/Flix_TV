from django.contrib import admin
from movie.models.movie import Movie, MovieVideo
from movie.models.genre import Genre
from movie.models.comment import Comment
from movie.models.review import Review


admin.site.register(Movie)
admin.site.register(MovieVideo)
admin.site.register(Genre)
admin.site.register(Comment)
admin.site.register(Review)



