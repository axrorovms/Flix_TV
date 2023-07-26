from rest_framework import serializers
from movie.models import Movie, MovieVideo, Genre
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


# class MovieListModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ('id', 'title', 'release_year', 'is_premium', 'photo', 'banner')
#
#
# class MovieDetailModelSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Movie
#         fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')
#
#     @staticmethod
#     def get_suitable_movies(user_id, slug):
#         user = User.objects.filter(id=user_id).first()
#         movie = Movie.objects.filter(slug=slug).first()
#
#         if user and movie:
#             if not movie.is_premium or (user.subscription and movie.is_premium):
#                 return MovieDetailModelSerializer(Movie.objects.filter(slug=slug), many=True).data
#             else:
#                 response_data = {"message": "Sorry, you need a premium subscription to access this movie."}
#         else:
#             response_data = {"message": "Movie not found."}
#
#         return response_data


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title',)


class MovieListModelSerializer(serializers.ModelSerializer):
    own_rating = serializers.SerializerMethodField()
    genre = GenreSerializer(many=True, read_only=True) or ['wwww']

    class Meta:
        model = Movie
        fields = ('slug', 'title', 'own_rating', 'release_year', 'photo', 'banner', 'is_premium', 'genre')

    def get_own_rating(self, movie):
        request = self.context.get('request')
        if request and request.user.is_authenticated:
            review = movie.review_set.filter(author=request.user).first()
            if review:
                return review.rating
        return 0


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = '__all__'

















