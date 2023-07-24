from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment, LikeDislike
from movie.filters import Moviefilter
from movie.serializers import (
    MovieDetailModelSerializer,
    MovieListModelSerializer,
    MovieCreateModelSerializer,
    GenreCreateModelSerializer,
    GenreListModelSerializer,
    ReviewListModelSerializer,
    ReviewCreateModelSerializer,
    CommentSerializer,
    LikeDislikeSerializer,
    ChildSerializer,
)

videos_params = openapi.Parameter(
    'videos', openapi.IN_FORM,
    description="test manual param",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=False)


class MovieCreateAPIView(CreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateModelSerializer
    parser_classes = (MultiPartParser, FormParser)

    @swagger_auto_schema(manual_parameters=[videos_params])
    def post(self, request, *args, **kwargs):
        videos = request.FILES.getlist('video')
        response = super().post(request, *args, **kwargs)
        movie = Movie.objects.create(
            user_id=response.data['user'],
            title=response.data['title'],
            slug=response.data['slug']
        )
        movie.genre.set(response.data['genre'])
        MovieVideo.objects.bulk_create(MovieVideo(video=video, movie=movie) for video in videos)
        return response


class MovieListAPIView(ListAPIView):
    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Moviefilter
    search_fields = ('title', 'release_year', 'genre__title')

    def get(self, request, *args, **kwargs):
        movies = self.get_queryset()
        data = []
        for movie in movies:
            movie_data = {
                'id': movie.id,
                'title': movie.title,
                'is_premium': movie.is_premium,
                'description': movie.description,
                'release_year': movie.release_year,
                'genre_list': Movie.get_genre_list(movie),
                'videos': Movie.get_videos(movie),
                'rating': Movie.get_rating(movie),
            }
            data.append(movie_data)

        return Response(data)


class MoviePremiumListAPIView(ListAPIView):
    queryset = Movie.objects.filter(is_premium=True)
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Moviefilter
    search_fields = ('title', 'release_year', 'genre__title')


class MoviePopularListAPIView(ListAPIView):
    queryset = Movie.objects.order_by('-views')
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)


class MovieNewestListAPIView(ListAPIView):
    queryset = Movie.objects.order_by('-release_year')
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)


class MovieUpdateAPIView(UpdateAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieCreateModelSerializer
    lookup_field = 'slug'


class MovieDeleteAPIView(DestroyAPIView):
    queryset = Movie.objects.all()
    lookup_field = 'slug'


class GenreCreateAPIView(CreateAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreCreateModelSerializer
    parser_classes = (MultiPartParser, FormParser)


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get(self, request, *args, **kwargs):
        genres = self.get_queryset()
        data = []
        for genre in genres:
            movie_data = {
                'title': genre.title,
                'image': genre.image,
                'count_movies': Genre.with_movies_count(genre)
            }
            data.append(movie_data)

        return Response(data)


class SimilarMovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Movie.get_similar_movies(slug)


class MovieDetailAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailModelSerializer

    def get(self, request, *args, **kwargs):
        movie = self.get_queryset()
        user_id = request.user.id
        slug = self.kwargs['slug']
        return Response(MovieDetailModelSerializer.get_suitable_movies(user_id, slug))


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateModelSerializer


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.get_review(slug)


class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Movie.objects.all()


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def list(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        queryset = self.get_queryset().filter(movie_id=movie_id)
        comments = self.serializer_class(queryset, many=True)
        return Response(comments.data)


class LikeDislikeView(generics.GenericAPIView):
    serializer_class = LikeDislikeSerializer

    def post(self, request, *args, **kwargs):
        try:
            instance = LikeDislike.objects.get(user_id=request.data.get('user'), comment_id=request.data.get('comment'))
            serializer = self.serializer_class(instance=instance, data=request.data, partial=True)
        except LikeDislike.DoesNotExist:
            serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)

