from movie.models import Movie, Comment, Review, MovieVideo
from rest_framework.serializers import ModelSerializer
from user_auth.models import User


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


# User Serializers ----------------------------------------------------------------------------------------------

class UserListSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'image', 'first_name', 'last_name', 'email', 'username', 'subscription', 'status', 'created_at')

    def to_representation(self, instance):
        rep = super().to_representation(instance)
        rep['comment'] = CommentListSerializer(instance.comments, many=True).data
        rep['review'] = ReviewListSerializer(instance.reviews, many=True).data
        return rep


class UserCreateUpdateDeleteSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class LatestUsersSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email', 'username')


# Movie Serializers ----------------------------------------------------------------------------------------------

class MovieListSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('slug', 'title', 'type', 'views', 'status', 'created_at', 'is_active')


class VideoSerializer(ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video',)


class MovieCreateDeleteSerializer(ModelSerializer):
    video = VideoSerializer(many=True, read_only=True)

    class Meta:
        model = Movie
        fields = ('title', 'slug', 'user', 'genre', 'video')


class TopMoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'type')

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.reviews.all():
            rep['rating'] = 0.0
        else:
            rep[
                'rating'] = f'{sum([i.rating for i in instance.reviews.all()]) / instance.reviews.all().count():.1f}'
        rep['genre'] = [i.title for i in instance.genre.all()]

        return rep


class LatestMoviesSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = ('id', 'title', 'type', 'status')
