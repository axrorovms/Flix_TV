from rest_framework import serializers
from movie.models import Movie
from users.models import User


class MovieListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')


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
