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
        model = 'movie.Movie'
        fields = ('title', 'slug', 'user', 'genre', 'video')


class MovieListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'movie.Movie'
        fields = ('title', 'release_year', 'status', 'photo', 'banner')


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = 'movie.Movie'
        fields = ('title', 'release_year', 'status', 'photo', 'banner')



    @classmethod
    def get_suitable_movies(cls, user_id, slug):
        user = dict(*User.objects.filter(id=user_id).values('subscription'))
        movie_status = dict(*Movie.objects.filter(slug=slug).values('status'))
        if user.get('subscription') == Movie.StatusChoice.values[0] and movie_status.get('status') == \
                Movie.StatusChoice.values[1]:
            response_data = {"message": "fucking dude buy premium"}
            return response_data
        return MovieListModelSerializer(Movie.objects.filter(slug=slug), many=True).data
