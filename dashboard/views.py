from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from dashboard.pagination import StandardResultsSetPagination
from movie.models import Movie, Comment, Review
from shared import IsAdmin, AdminOrModerator
from user.models import User
from dashboard.serializers import (MovieListSerializer, MovieCreateDeleteSerializer,
                                   UserListSerializer, UserCreateUpdateDeleteSerializer,
                                   CommentListSerializer, CommentDeleteSerializer,
                                   ReviewListSerializer, ReviewDeleteSerializer,
                                   DashboardSerializer)


# Movies ----------------------------------------------------------------------------------------------

class MovieList(ListAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class MovieCreate(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = FormParser, MultiPartParser


class MovieUpdate(UpdateAPIView):
    permission_classes = [IsAdmin]
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = FormParser, MultiPartParser
    lookup_field = 'slug'

    def get_queryset(self):
        return Movie.objects.filter(slug=self.kwargs.get('slug'))


class MovieDelete(DestroyAPIView):
    permission_classes = [AdminOrModerator]
    serializer_class = MovieCreateDeleteSerializer
    queryset = Movie.objects.all()
    lookup_field = 'slug'


# class MovieDetail(RetrieveAPIView):
#     serializer_class = MovieCreateDeleteSerializer
#     lookup_field = 'slug'
#
#     def get_queryset(self):
#         slug = self.kwargs.get('slug')
#         return Movie.objects.filter(slug=slug)


# Users ----------------------------------------------------------------------------------------------

class UserList(ListAPIView):
    permission_classes = [AdminOrModerator]
    queryset = User.objects.all()
    serializer_class = UserListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class UserCreate(CreateAPIView):
    permission_classes = [AdminOrModerator]
    queryset = User.objects.all()
    serializer_class = UserCreateUpdateDeleteSerializer
    parser_classes = FormParser, MultiPartParser


class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAdmin]
    serializer_class = UserCreateUpdateDeleteSerializer
    parser_classes = FormParser, MultiPartParser


class UserDelete(DestroyAPIView):
    permission_classes = [AdminOrModerator]
    serializer_class = UserCreateUpdateDeleteSerializer
    queryset = User.objects.all()


# Comments ----------------------------------------------------------------------------------------------

class CommentList(ListAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class CommentDelete(DestroyAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer


# Reviews --------------------------------------------------------------------------------------

class ReviewList(ListAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class ReviewDelete(DestroyAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewDeleteSerializer


# Dashboard ------------------------------------------------------------------------------------

class DashboardAPIView(ListAPIView):
    queryset = Movie.objects.all()
    permission_classes = [AdminOrModerator]
    serializer_class = DashboardSerializer
