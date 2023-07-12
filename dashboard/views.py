from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView)

from dashboard.pagination import StandardResultsSetPagination
from dashboard.serializers import (MovieListSerializer, MovieCreateDeleteSerializer,
                                   UserListSerializer, UserCreateUpdateDeleteSerializer, CommentListSerializer,
                                   CommentDeleteSerializer, ReviewListSerializer, ReviewDeleteSerializer,
                                   DashboardSerializer)
from movie.models import Movie, Comment, Review
from user.models import User
from datetime import datetime
from django.db.models import Sum, Count
from shared import IsModerator, IsAdmin


# Movies ----------------------------------------------------------------------------------------------

class MovieList(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class MovieCreate(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = FormParser, MultiPartParser


class MovieUpdate(UpdateAPIView):
    # queryset = Movie.objects.all()
    # permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = FormParser, MultiPartParser
    lookup_field = 'slug'

    def get_queryset(self):
        return Movie.objects.filter(slug=self.kwargs.get('slug'))


class MovieDelete(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    serializer_class = MovieCreateDeleteSerializer
    queryset = Movie.objects.all()
    lookup_field = 'slug'


# Users ----------------------------------------------------------------------------------------------

class UserList(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class UserCreate(CreateAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateDeleteSerializer
    parser_classes = FormParser, MultiPartParser


class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    # permission_classes = [IsAuthenticated, IsAdmin]
    serializer_class = UserCreateUpdateDeleteSerializer
    parser_classes = FormParser, MultiPartParser

    def get_object(self):
        return super().get_object()


class UserDelete(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    serializer_class = UserCreateUpdateDeleteSerializer
    queryset = User.objects.all()


# Comments ----------------------------------------------------------------------------------------------

class CommentList(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class CommentDelete(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer


# Reviews --------------------------------------------------------------------------------------
class ReviewList(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class ReviewDelete(DestroyAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewDeleteSerializer


# Dashboard ------------------------------------------------------------------------------------

class DashboardAPIView(ListAPIView):
    # permission_classes = [IsAuthenticated, IsAdmin, IsModerator]
    serializer_class = DashboardSerializer

    def get_queryset(self):
        current_month = datetime.now().month
        movies_added = Movie.objects.filter(created_at__month=current_month)

        combined_data = {
            'unique_views': self.view_sum(),
            'movies_added': movies_added.count(),
            'new_comments': self.count_comments(movies_added),
            'new_reviews': self.count_reviews(movies_added),
            'top_movies': Movie.objects.order_by('-views')[:5],
            'latest_movies': Movie.objects.order_by('-release_year')[:5],
            'latest_users': User.objects.order_by('-created_at')[:5],
            'latest_reviews': Review.objects.order_by('-created_at')[:5],
        }

        return [combined_data]

    def view_sum(self):
        current_month = datetime.now().month
        movies = Movie.objects.filter(created_at__month=current_month)
        count = movies.aggregate(total_views=Sum('views'))['total_views']
        return count or 0

    def count_comments(self, movies):
        comment_count = movies.annotate(num_comments=Count('comment')).aggregate(total_comments=Sum('num_comments'))[
            'total_comments']
        return comment_count or 0

    def count_reviews(self, movies):
        review_count = movies.annotate(num_reviews=Count('review')).aggregate(total_reviews=Sum('num_reviews'))[
            'total_reviews']
        return review_count or 0














