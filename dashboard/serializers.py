from movie.models import Movie, Comment, Review, MovieVideo
from rest_framework.serializers import ModelSerializer
from users.models import User


# Review Serializers --------------------------------------------------------------------------------

class ReviewListSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'movie', 'author', 'text', 'rating', 'created_at')


class ReviewDeleteSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"


class LatestReviewsSerializer(ModelSerializer):
    class Meta:
        model = Review
        fields = ('id', 'movie', 'author')


# Comment Serializers ----------------------------------------------------

class CommentListSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('id', 'movie', 'author', 'text', 'created_at')


class CommentDeleteSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"


class LatestUsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


# Movie Serializers ----------------------------------------------------------------------------------------------


class MovieModelSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class VideoSerializer(ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video',)


class TopMoviesSerializer(ModelSerializer):

    class Meta:
        model = Movie
        fields = ('id', 'title', 'type')

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.reviews.all():
            rep['rating'] = 0.0
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.reviews.all()]) / instance.reviews.all().count():.1f}'
        rep['genre'] = [i.title for i in instance.genre.all()]

        return rep


class LatestMoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'type', 'is_premium')
