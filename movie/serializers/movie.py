from rest_framework import serializers
from movie.models import Movie, MovieVideo, Genre


class VideoSerializerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video',)


class MovieCreateModelSerializer(serializers.ModelSerializer):
    video = VideoSerializerModelSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'slug', 'user', 'genre', 'video')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title',)


class MovieListModelSerializer(serializers.ModelSerializer):
    average_rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True) or ['wwww']

    class Meta:
        model = Movie
        fields = ('slug', 'title', 'release_year', 'photo', 'banner', 'is_premium', 'genre', 'average_rating')

    def get_average_rating(self, movie):
        return movie.get_rate


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

















