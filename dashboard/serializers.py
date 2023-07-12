from rest_framework.serializers import ModelSerializer, Serializer, IntegerField
from django.db.models import Sum, Count
from datetime import datetime

from movie.models import Movie, Comment, Review
from user.models import User


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
        fields = ('id', 'movie', 'author', 'text', 'likes', 'dislikes', 'created_at')


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

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.reviews.all():
            rep['rating'] = 0.0
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.reviews.all()]) / instance.reviews.all().count():.1f}'
        rep['genre'] = [i.title for i in instance.genre.all()]
        return rep


class MovieCreateDeleteSerializer(ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


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


# Dashboard Serializers ----------------------------------------------------------------------------------------------


class DashboardSerializer(Serializer):
    unique_views = IntegerField()
    movies_added = IntegerField()
    new_comments = IntegerField()
    new_reviews = IntegerField()
    top_movies = TopMoviesSerializer(many=True)
    latest_movies = LatestMoviesSerializer(many=True)
    latest_users = LatestUsersSerializer(many=True)
    latest_reviews = LatestReviewsSerializer(many=True)

    def get_view_sum(self):
        movies = Movie.objects.filter(created_at__month=datetime.now().month)
        return movies.aggregate(total_views=Sum('views'))['total_views'] or 0

    def count_comments(self, movies):
        return movies.annotate(num_comments=Count('comment')).aggregate(total_comments=Sum('num_comments'))[
            'total_comments'] or 0

    def count_reviews(self, movies):
        return movies.annotate(num_reviews=Count('review')).aggregate(total_reviews=Sum('num_reviews'))[
            'total_reviews'] or 0

    def to_representation(self, instance):
        movies_added = Movie.objects.filter(created_at__month=datetime.now().month)
        rep = {}
        rep['unique_views'] = self.get_view_sum()
        rep['movies_added'] = movies_added.count()
        rep['new_comments'] = self.count_comments(movies_added)
        rep['new_reviews'] = self.count_reviews(movies_added)
        rep['top_movies'] = TopMoviesSerializer(Movie.objects.order_by('-views')[:5], many=True).data
        rep['latest_movies'] = LatestMoviesSerializer(Movie.objects.order_by('-release_year')[:5], many=True).data
        rep['latest_users'] = LatestUsersSerializer(User.objects.order_by('-created_at')[:5], many=True).data
        rep['latest_reviews'] = LatestReviewsSerializer(Review.objects.order_by('-created_at')[:5], many=True).data

        return rep
