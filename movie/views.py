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
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView, \
    ListCreateAPIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment, DisLike, Like
from movie.serializers import MovieDetailModelSerializer, MovieListModelSerializer, MovieCreateModelSerializer, \
    GenreCreateModelSerializer, GenreListModelSerializer, ReviewListModelSerializer, ReviewCreateModelSerializer, \
    CommentSerializer, ChildSerializer
from movie.filters import Moviefilter
from rest_framework import status
from movie.serializers import (MovieDetailModelSerializer, MovieListModelSerializer,
                               GenreListModelSerializer, ReviewListModelSerializer,
                               ReviewCreateModelSerializer, CommentSerializer, ChildSerializer, LikeSerializer,
                               DisLikeSerializer,
                               )


# Movie ----------------------------------------------------------------------------------------------


class MovieListAPIView(APIView):
    def get(self, request):
        queryset = Movie.objects.filter(is_active=True)
        filter_backend = DjangoFilterBackend()
        search_backend = SearchFilter()
        queryset = filter_backend.filter_queryset(request, queryset, view=self)
        queryset = search_backend.filter_queryset(request, queryset, view=self)
        pagination_class = StandardResultsSetPagination()
        page = pagination_class.paginate_queryset(queryset, request, view=self)
        if page is not None:
            serializer = MovieListModelSerializer(page, many=True)
            for movie_data in serializer.data:
                movie = Movie.objects.get(pk=movie_data['id'])
                movie_data['rating'] = movie.get_rating(movie)
                movie_data['genre'] = movie.get_genre_list(movie)
                movie_data['videos'] = movie.get_videos(movie)
            return pagination_class.get_paginated_response(serializer.data)

        serializer = MovieListModelSerializer(queryset, many=True)
        serializer.data['rating'] = Movie.get_rating
        return Response(serializer.data)


class MovieDetailAPIView(APIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailModelSerializer

    def get(self, request, *args, **kwargs):
        user_id = request.user.id
        slug = self.kwargs['slug']
        return Response(MovieDetailModelSerializer.get_suitable_movies(user_id, slug))


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


# Reviews ------------------------------------------------------------------------------------------------

class ReviewCreateAPIView(CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewCreateModelSerializer


class ReviewListAPIView(ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return ReviewListModelSerializer.get_review(slug)


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
