from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from dashboard.pagination import StandardResultsSetPagination
from movie.models import Movie, Comment, Review, MovieVideo
from shared import IsAdmin, AdminOrModerator
from user.models import User
from dashboard.serializers import (MovieListSerializer, MovieCreateDeleteSerializer,
                                   UserListSerializer, UserCreateUpdateDeleteSerializer,
                                   CommentListSerializer, CommentDeleteSerializer,
                                   ReviewListSerializer, ReviewDeleteSerializer,
                                   DashboardSerializer)

videos_params = openapi.Parameter(
    'videos', openapi.IN_FORM,
    description="test manual param",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=False)
# Movies -------------------------------------------------------------------------------------

class MovieList(ListAPIView):
    permission_classes = [AdminOrModerator]
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


# class MovieCreate(CreateAPIView):
#     permission_classes = [IsAdmin]
#     queryset = Movie.objects.all()
#     serializer_class = MovieCreateDeleteSerializer
#     parser_classes = FormParser, MultiPartParser


class MovieCreate(CreateAPIView):
    permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[videos_params])
    def post(self, request, *args, **kwargs):
        videos = request.FILES.getlist('video')
        response = super().post(request, *args, **kwargs)
        movie = Movie.objects.create(
            user_id=response.data['user'],
            title=response.data['title'],
            slug=response.data['slug'],
        )
        movie.genre.set(response.data['genre'])
        MovieVideo.objects.bulk_create(MovieVideo(video=video, movie=movie) for video in videos)
        return response


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


# Users ----------------------------------------------------------------------------------------

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


# Comments --------------------------------------------------------------------------------------

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
