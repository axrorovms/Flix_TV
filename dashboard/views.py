from datetime import datetime

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import (CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, ListCreateAPIView)
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response
from rest_framework.views import APIView

from movie.models import Movie, Comment, Review, MovieVideo
from shared import IsAdmin, AdminOrModerator
from users.models import User
from dashboard.pagination import StandardResultsSetPagination
from dashboard.serializers import (
    MovieListSerializer,
    MovieCreateDeleteSerializer,
    CommentListSerializer,
    CommentDeleteSerializer,
    ReviewListSerializer,
    ReviewDeleteSerializer,
    TopMoviesSerializer,
    LatestMoviesSerializer,
    LatestUsersSerializer,
    LatestReviewsSerializer,
)

videos_params = openapi.Parameter(
    'videos', openapi.IN_FORM,
    description="test manual param",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=False)


# Movies -------------------------------------------------------------------------------------

class MovieList(ListCreateAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Movie.objects.all()
    serializer_class = MovieListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class MovieCreate(CreateAPIView):
    # permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = (MultiPartParser, FormParser)

    # def create(self, request, *args, **kwargs):
    #     return super().create(request, *args, **kwargs)

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
    # permission_classes = [IsAdmin]
    serializer_class = MovieCreateDeleteSerializer
    parser_classes = FormParser, MultiPartParser
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'
    #
    # def get_queryset(self):
    #     return Movie.objects.filter(slug=self.kwargs.get('slug'))
    #

class MovieDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    # serializer_class = MovieCreateDeleteSerializer
    queryset = Movie.objects.all()
    lookup_field = 'slug'


# Comments --------------------------------------------------------------------------------------

class CommentList(ListAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
    parser_classes = FormParser, MultiPartParser


class CommentDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer


# Reviews --------------------------------------------------------------------------------------

class ReviewList(ListAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    parser_classes = FormParser, MultiPartParser
    pagination_class = StandardResultsSetPagination


class ReviewDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewDeleteSerializer


# Dashboard ------------------------------------------------------------------------------------

class DashboardAPIView(APIView):
    # permission_classes = [AdminOrModerator]

    def get(self, request):
        movies_added = Movie.objects.filter(created_at__month=datetime.now().month)
        rep = dict()
        rep['unique_views'] = Movie.get_view_sum()
        rep['movies_added'] = movies_added.count()
        rep['new_comments'] = Movie.count_comments(movies_added)
        rep['new_reviews'] = Movie.count_reviews(movies_added)
        rep['top_movies'] = TopMoviesSerializer(Movie.objects.order_by('-views')[:5], many=True).data
        rep['latest_movies'] = LatestMoviesSerializer(Movie.objects.order_by('-release_year')[:5], many=True).data
        rep['latest_users'] = LatestUsersSerializer(User.objects.order_by('-created_at')[:5], many=True).data
        rep['latest_reviews'] = LatestReviewsSerializer(Review.objects.order_by('-created_at')[:5], many=True).data

        return Response(rep)
