from rest_framework import serializers
from movie.models import Movie, MovieVideo
from users.models import User


class VideoSerializerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video',)


class MovieCreateModelSerializer(serializers.ModelSerializer):
    video = VideoSerializerModelSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'slug', 'user', 'genre', 'video')


class MovieListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'release_year', 'is_premium', 'photo', 'banner')

    @classmethod
    def get_similar_movies(cls, slug):
        try:
            movie = Movie.objects.get(slug=slug)
            movie_genres = movie.genre.all()
            similar_movies = Movie.objects.filter(genre__in=movie_genres).exclude(slug=slug).distinct()

            return similar_movies

        except Movie.DoesNotExist:
            return Movie.objects.none()



class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')



    @staticmethod
    def get_suitable_movies(user_id, slug):
        user = User.objects.filter(id=user_id).values('subscription').first()
        movie = Movie.objects.filter(slug=slug).first()

        if user and user.get('subscription') and movie and movie.is_premium:
            return MovieDetailModelSerializer(Movie.objects.filter(slug=slug), many=True).data

        response_data = {"message": "Sorry, you need a premium subscription to access this movie."}
        return response_data
