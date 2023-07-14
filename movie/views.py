from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment
from movie.serializers import MovieDetailModelSerializer, MovieListModelSerializer, MovieCreateModelSerializer, \
    GenreCreateModelSerializer, GenreListModelSerializer, ReviewListModelSerializer, ReviewCreateModelSerializer, \
    CommentSerializer, ChildSerializer, CommentLikeDislikeSerializer
from movie.filters import Moviefilter

videos_params = openapi.Parameter(
    'videos', openapi.IN_FORM,
    description="test manual param",
    type=openapi.TYPE_ARRAY,
    items=openapi.Items(type=openapi.TYPE_FILE),
    required=False)


class MovieListPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


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
    pagination_class = MovieListPagination


class MoviePremiumListAPIView(ListAPIView):
    queryset = Movie.objects.filter(status='Premium')
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


class SimilarMovieListAPIView(ListAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieListModelSerializer

    def get_queryset(self):
        slug = self.kwargs['slug']
        return MovieListModelSerializer.get_similar_movies(slug)


class MovieDetailAPIView(RetrieveAPIView):
    queryset = Movie.objects.all()
    serializer_class = MovieDetailModelSerializer

    def get(self, request, *args, **kwargs):
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
        return ReviewListModelSerializer.get_review(slug)


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


class CommentLikeDislikeView(CreateAPIView):
    serializer_class = CommentLikeDislikeSerializer

    def create(self, request, *args, **kwargs):
        comment_id = kwargs.get('id')
        action = request.data.get('action')

        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({"error": "Fucking comment 404"}, status=status.HTTP_404_NOT_FOUND)

        if action == "like":
            comment.likes += 1
        elif action == "dislike":
            comment.dislikes += 1
        else:
            return Response({"error": "Fucking bad request"}, status=status.HTTP_400_BAD_REQUEST)

        comment.save()

        return Response({"success": f"Fucking {action} added"}, status=status.HTTP_201_CREATED)
