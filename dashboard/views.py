from datetime import datetime
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import (
    ListAPIView,
    DestroyAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView)

from movie.models import Movie, Comment, Review, MovieVideo, Genre
from movie.serializers import GenreCreateModelSerializer
from users.models import User
from shared.pagination import StandardResultsSetPagination
from dashboard.serializers import (
    CommentListSerializer,
    ReviewListSerializer,
    TopMoviesSerializer,
    LatestMoviesSerializer,
    LatestUsersSerializer,
    LatestReviewsSerializer,
    MovieModelSerializer,
)


# Movies -------------------------------------------------------------------------------------


class MovieListCreateApiView(ListCreateAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    pagination_class = StandardResultsSetPagination

    def create(self, request, *args, **kwargs):
        videos = request.FILES.getlist('video')
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        movie = serializer.instance
        movie.genre.set(serializer.validated_data['genre'])

        movie_videos_to_create = [
            MovieVideo(video=video, movie=movie) for video in videos
        ]
        MovieVideo.objects.bulk_create(movie_videos_to_create)

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class MovieUpdateDelete(RetrieveUpdateDestroyAPIView):
    # permission_classes = [IsAdmin]
    queryset = Movie.objects.all()
    serializer_class = MovieModelSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


# Comments --------------------------------------------------------------------------------------


class CommentList(ListAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer


class CommentDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Comment.objects.all()


# Reviews --------------------------------------------------------------------------------------

class ReviewList(ListAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()
    serializer_class = ReviewListSerializer
    pagination_class = StandardResultsSetPagination


class ReviewDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    queryset = Review.objects.all()


# Dashboard ------------------------------------------------------------------------------------


class DashboardAPIView(APIView):
    # permission_classes = [AdminOrModerator]
    def get(self, request):
        movies_added = Movie.objects.filter(created_at__month=datetime.now().month)
        rep = {
            'unique_views': Movie.get_view_sum(),
            'movies_added': movies_added.count(),
            'new_comments': Movie.count_comments(movies_added),
            'new_reviews': Movie.count_reviews(movies_added),
            'top_movies': TopMoviesSerializer(Movie.objects.order_by('-views')[:5], many=True).data,
            'latest_movies': LatestMoviesSerializer(Movie.objects.order_by('-release_year')[:5], many=True).data,
            'latest_users': LatestUsersSerializer(User.objects.order_by('-created_at')[:5], many=True).data,
            'latest_reviews': LatestReviewsSerializer(Review.objects.order_by('-created_at')[:5], many=True).data
        }
        return Response(rep)


# Genres ------------------------------------------------------------------------------------------------


class GenreCreateAPIView(CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateModelSerializer
