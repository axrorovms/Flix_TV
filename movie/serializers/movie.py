from rest_framework import serializers
from movie.models import Movie, MovieVideo
from user.models import User


class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video', )


class MovieCreateModelSerializer(serializers.ModelSerializer):
    video = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'slug', 'user', 'genre', 'video')



class MovieListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'status', 'photo', 'banner')

    @classmethod
    def get_similar_movies(cls, slug):
        try:
            movie = Movie.objects.get(slug=slug)
            movie_genres = movie.genre.all()
            similar_movies = Movie.objects.filter(genre__in=movie_genres).exclude(slug=slug).distinct()

            return similar_movies

        except Movie.DoesNotExist:
            return Movie.objects.none()

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.review_set.all():
            rep['rating'] = float(0.0)
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.review_set.all()]) / instance.review_set.all().count():.1f}'
        rep['videos'] = [i.video for i in instance.movievideo_set.all()]
        rep['genre'] = [i.title for i in instance.genre.all()]
        return rep


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'status', 'photo', 'banner')

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.review_set.all():
            rep['rating'] = 0.00
        else:
            rep[
                'rating'] = f'{sum([i.rating for i in instance.review_set.all()]) / instance.review_set.all().count():.2f}'
        rep['videos'] = [i.video for i in instance.movievideo_set.all()]
        rep['genre'] = [i.title for i in instance.genre.all()]


        return rep

    @classmethod
    def get_suitable_movies(cls, user_id, slug):
        user = dict(*User.objects.filter(id=user_id).values('subscription'))
        movie_status = dict(*Movie.objects.filter(slug=slug).values('status'))
        if user.get('subscription') == Movie.StatusChoice.values[0] and movie_status.get('status') == \
                Movie.StatusChoice.values[1]:
            response_data = {"message": "fucking dude buy premium"}
            return response_data
        return MovieListModelSerializer(Movie.objects.filter(slug=slug), many=True).data
