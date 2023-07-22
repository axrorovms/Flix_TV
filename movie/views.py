from rest_framework.generics import (ListAPIView, CreateAPIView, ListCreateAPIView)
from rest_framework.views import APIView

from movie.models import Movie, Genre, Review, Comment, Like, DisLike
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
from shared.pagination import StandardResultsSetPagination
from rest_framework.response import Response
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


# Comments --------------------------------------------------------------------------------------------------

class CommentListCreateAPIView(ListCreateAPIView):
    queryset = Movie.objects.all()
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return Comment.objects.filter(id=comment_id)


class CommentReplyListCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return Comment.objects.filter(parent_id=comment_id)

    def perform_create(self, serializer):
        comment_id = self.kwargs['id']
        parent_comment = Comment.objects.get(id=comment_id)
        serializer.save(parent=parent_comment)


class ParentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['show_children'] = True
        return context


class CommentLikeView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        user = request.user
        if Like.objects.filter(user=user):
            Like.objects.filter(user=user).delete()
            return Response({"error": "Fucking like deleted"}, status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, comment_id=comment_id, like=1)
        return Response({"success": "Fucking like added"}, status=status.HTTP_201_CREATED)


class CommentDislikeView(CreateAPIView):
    queryset = DisLike.objects.all()
    serializer_class = DisLikeSerializer

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        user = request.user
        if DisLike.objects.filter(user=user):
            DisLike.objects.filter(user=user).delete()
            return Response({"error": "Fucking dislike deleted"}, status=status.HTTP_400_BAD_REQUEST)
        DisLike.objects.create(user=user, comment_id=comment_id, dislike=1)
        return Response({"success": "Fucking dislike added"}, status=status.HTTP_201_CREATED)
