from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.utils.serializer_helpers import ReturnDict
from rest_framework.views import APIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment, LikeDislike
from movie.serializers import MovieDetailModelSerializer, MovieListModelSerializer, MovieCreateModelSerializer, \
    GenreCreateModelSerializer, GenreListModelSerializer, ReviewListModelSerializer, ReviewCreateModelSerializer, \
    CommentSerializer, ChildSerializer, LikeDislikeSerializer
from movie.filters import Moviefilter
from users.models import User

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
    serializer_class = CommentSerializer

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


class LikeDislikeView(generics.GenericAPIView):
    serializer_class = LikeDislikeSerializer

    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user_id = request.data.get('user')
            comment_id = request.data.get('comment')
            is_like = request.data.get('is_like').capitalize()

            user = get_object_or_404(User, pk=user_id)
            comment = get_object_or_404(Comment, pk=comment_id)

            # Update Logic

            # Create Logic
            serializer.user = user_id
            serializer.comment = comment_id
            serializer.is_like = is_like
            serializer.save()

            return Response(serializer.data, status=201)
        else:
            return Response(serializer.errors, status=400)

    def put(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = request.data.get('user')
            comment = request.data.get('comment')
            is_like = request.data.get('is_like').capitalize()

            instance = get_object_or_404(LikeDislike, user=user, comment=comment)

            if instance:
                instance.is_like = is_like
                instance.save()
                return Response(serializer.data, status=201)

            return Response(serializer.data, status=404)
        else:
            return Response(serializer.data, status=400)

        # class CommentLikeView(CreateAPIView):
#     queryset = Like.objects.all()
#     serializer_class = LikeSerializer
#
#     def create(self, request, *args, **kwargs):
#         comment_id = request.data.get('comment')
#         user = request.user
#         if Like.objects.filter(user=user):
#             Like.objects.filter(user=user).delete()
#             return Response({"error": "Fucking like deleted"}, status=status.HTTP_400_BAD_REQUEST)
#         Like.objects.create(user=user, comment_id=comment_id, like=1)
#         return Response({"success": "Fucking like added"}, status=status.HTTP_201_CREATED)
#
#
# class CommentDislikeView(CreateAPIView):
#     queryset = DisLike.objects.all()
#     serializer_class = DisLikeSerializer
#
#     def create(self, request, *args, **kwargs):
#         comment_id = request.data.get('comment')
#         user = request.user
#         if DisLike.objects.filter(user=user):
#             DisLike.objects.filter(user=user).delete()
#             return Response({"error": "Fucking dislike deleted"}, status=status.HTTP_400_BAD_REQUEST)
#         DisLike.objects.create(user=user, comment_id=comment_id, dislike=1)
#         return Response({"success": "Fucking dislike added"}, status=status.HTTP_201_CREATED)
