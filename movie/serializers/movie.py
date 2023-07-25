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


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')

    @staticmethod
    def get_suitable_movies(user_id, slug):
        user = User.objects.filter(id=user_id).first()
        movie = Movie.objects.filter(slug=slug).first()

        if user and movie:
            if not movie.is_premium or (user.subscription and movie.is_premium):
                return MovieDetailModelSerializer(Movie.objects.filter(slug=slug), many=True).data
            else:
                response_data = {"message": "Sorry, you need a premium subscription to access this movie."}
        else:
            response_data = {"message": "Movie not found."}

        return response_data
