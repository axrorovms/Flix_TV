from rest_framework.generics import (ListAPIView, CreateAPIView, ListCreateAPIView)
from rest_framework.views import APIView
from movie.models import Movie, Genre, Review, Comment, Like, DisLike
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from .serializers import DisLikeSerializer, LikeSerializer
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter

from django_filters.rest_framework import DjangoFilterBackend
from shared.pagination import StandardResultsSetPagination
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment, DisLike, Like
from movie.serializers import MovieDetailModelSerializer, MovieListModelSerializer, MovieCreateModelSerializer, \
    GenreCreateModelSerializer, GenreListModelSerializer, ReviewListModelSerializer, ReviewCreateModelSerializer, \
    CommentSerializer, ChildSerializer
from movie.filters import Moviefilter

videos_params = openapi.Parameter(
    'videos', openapi.IN_FORM,
    description="test manual param",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=False)


from rest_framework import status
from movie.serializers import (MovieDetailModelSerializer, MovieListModelSerializer,
                               GenreListModelSerializer, ReviewListModelSerializer,
                               ReviewCreateModelSerializer, CommentSerializer, ChildSerializer, LikeSerializer,
                               DisLikeSerializer,
                               )


# Movie ----------------------------------------------------------------------------------------------
class MovieCreateAPIView(CreateAPIView):

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
                'status': movie.status,
                'description': movie.description,
                'release_year': movie.release_year,
                'genre_list': Movie.get_genre_list(movie),
                'videos': Movie.get_videos(movie),
                'rating': Movie.get_rating(movie),
            }
            data.append(movie_data)

        return Response(data)



class MoviePremiumListAPIView(ListAPIView):
    queryset = Movie.active_movies.all()
    serializer_class = MovieListModelSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter)
    filterset_class = Moviefilter
    search_fields = ('title', 'release_year', 'genre__title')


class SimilarMovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return MovieListModelSerializer.get_similar_movies(slug)


# Genres ------------------------------------------------------------------------------------------------


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

# Reviews ------------------------------------------------------------------------------------------------


class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateModelSerializer


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.get_review(slug)


# Comment________________________________________________________________

class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)


class ReplyCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['comment_id']
        return Comment.objects.filter(parent_id=comment_id)

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        parent_comment = Comment.objects.get(id=comment_id)
        serializer.save(parent=parent_comment)


class MovieCommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def list(self, request, *args, **kwargs):
        movie_id = kwargs.get('movie_id')
        queryset = self.get_queryset().filter(movie_id=movie_id)
        comments = self.serializer_class(queryset, many=True)
        return Response(comments.data)


class LikeCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req, *args, **kwargs):
        saved = Like.objects.filter(user=req.user)
        serializer = LikeSerializer(saved, many=True)

        return Response(serializer.data)

    def post(self, req, *args, **kwargs):
        req.data.pop('id', None)

        saved = Like.objects.filter(**req.data)
        if saved:
            saved.delete()

            return Response({'detail': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

        serializer = LikeSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)


class DislikeCreateApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, req, *args, **kwargs):
        saved = DisLike.objects.filter(user=req.user)
        serializer = DisLikeSerializer(saved, many=True)

        return Response(serializer.data)

    def post(self, req, *args, **kwargs):
        req.data.pop('id', None)

        saved = DisLike.objects.filter(**req.data)
        if saved:
            saved.delete()

            return Response({'detail': 'deleted'}, status=status.HTTP_204_NO_CONTENT)

        serializer = DisLikeSerializer(data=req.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)
