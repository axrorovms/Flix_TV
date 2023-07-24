from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView

from movie.filters import Moviefilter
from movie.models import (
    Movie,
    Genre,
    Review,
    Comment,
    LikeDislike
)

from movie.serializers import (
    MovieDetailModelSerializer,
    MovieListModelSerializer,
    GenreListModelSerializer,
    ReviewListModelSerializer,
    ReviewCreateModelSerializer,
    CommentSerializer,
    ChildSerializer,
    LikeDislikeSerializer
)


class MovieListAPIView(ListAPIView):
    queryset = Movie.objects.filter(is_active=True)
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Moviefilter
    search_fields = ('title', 'release_year', 'genre__title')

    def get(self, request, *args, **kwargs):
        movies = self.queryset
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


class GenreListAPIView(ListAPIView):
    queryset = Genre.objects.all()
    serializer_class = GenreListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)

    def get(self, request, *args, **kwargs):
        genres = self.get_queryset().annotate(movies_count=Count('movie'))
        data = []
        for genre in genres:
            movie_data = {
                'title': genre.title,
                'image': genre.image.url,
                'count_movies': genre.movies_count
            }
            data.append(movie_data)

        return Response(data)


class SimilarMovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Movie.get_similar_movies(slug)


class MovieRetrieveAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailModelSerializer

    def get(self, request, *args, **kwargs):
        movie = self.get_queryset()
        user_id = request.user.id
        slug = self.kwargs['slug']
        return Response(MovieDetailModelSerializer.get_suitable_movies(movie, user_id, slug))


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateModelSerializer

    def create(self, request, *args, **kwargs):
        author_id = request.data.get('author')
        text = request.data.get('text')
        rating = request.data.get('rating')
        movie_id = request.data.get('movie')
        if Review.objects.filter(author_id=author_id):
            return Response({"message": "You've already fucking reviewed"})
        Review.objects.create(author_id=author_id, text=text, rating=rating, movie_id=movie_id)


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListModelSerializer
    lookup_field = 'slug'
    lookup_url_kwarg = 'slug'


class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Movie.objects.all()


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def list(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        queryset = self.get_queryset().filter(movie_id=movie_id)
        comments = self.serializer_class(queryset, many=True)
        return Response(comments.data)


class LikeDislikeView(GenericAPIView):
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
