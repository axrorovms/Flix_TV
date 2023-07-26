from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import status
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, GenericAPIView
from rest_framework.views import APIView

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
from users.models import User


class MovieRetrieveAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailModelSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        slug = self.kwargs['slug']
        data = self.get_suitable_movie_data(user_id, slug)
        return Response(data)

    @staticmethod
    def get_suitable_movie_data(user_id, slug):
        user = User.objects.filter(id=user_id).first()
        movie = Movie.objects.filter(slug=slug).first()

        if user and movie:
            if not movie.is_premium or (user.subscription and movie.is_premium):
                return {
                    'id': movie.id,
                    'slug': movie.slug,
                    'title': movie.title,
                    'is_premium': movie.is_premium,
                    'duration': movie.film_time_duration,
                    'country': movie.country.name,
                    'age_limit': movie.age_limit,
                    'type': movie.type,
                    'views': movie.views,
                    'description': movie.description,
                    'release_year': movie.release_year,
                    'rating': Movie.get_rating(movie),
                    'genre_list': Movie.get_genre_list(movie),
                    'photo': movie.photo.url,
                    'banner': movie.banner.url,
                    'videos': [i.url for i in Movie.get_videos(movie)]
                }
            else:
                response_data = {"message": "Sorry, you need a premium subscription to access this movie."}
        else:
            response_data = {"message": "Movie not found."}

        return response_data


class MovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Moviefilter
    filterset_fields = ['is_premium']
    search_fields = ('title', 'release_year', 'genre__title')


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
        return Movie.get_similar_movies(self.kwargs.get('slug'))


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateModelSerializer


class ReviewListAPIView(ListAPIView):
    serializer_class = ReviewListModelSerializer
    lookup_field = 'slug'

    def get_queryset(self):
        return Review.get_review(slug=self.kwargs.get('slug'))


class CommentCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Movie.objects.all()


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def list(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        queryset = self.get_queryset().filter(movie_id=movie_id)
        comments = self.serializer_class(queryset, many=True, context={'request': request})
        return Response(comments.data)


class LikeDislikeView(CreateAPIView):
    queryset = LikeDislike.objects.all()
    serializer_class = LikeDislikeSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response_data = serializer.save()

        if response_data.get('message') == 'added':
            return Response({"message": "added"}, status=200)
        elif response_data.get('message') == 'updated':
            return Response({"message": "updated"}, status=200)
        elif response_data.get('message') == 'deleted':
            return Response({"message": "deleted"}, status=200)
