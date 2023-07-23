from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.filters import SearchFilter
from rest_framework.generics import ListAPIView, CreateAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView

from movie.models import Movie, Genre, MovieVideo, Review, Comment, DisLike, Like
from movie.serializers import MovieDetailModelSerializer, MovieListModelSerializer, MovieCreateModelSerializer, \
    GenreCreateModelSerializer, GenreListModelSerializer, ReviewListModelSerializer, ReviewCreateModelSerializer, \
    CommentSerializer, ChildSerializer, DisLikeSerializer, LikeSerializer
from movie.filters import Moviefilter

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


class MovieDetailAPIView(RetrieveAPIView):
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

    def get_queryset(self):
        slug = self.kwargs['slug']
        return Review.get_review(slug)


class CreateCommentAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)
    queryset = Movie.objects.all()


class CommentReplyListCreateAPIView(CreateAPIView):
    serializer_class = CommentSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        comment_id = self.kwargs['id']
        return Comment.objects.filter(parent_id=comment_id)

    def perform_create(self, serializer):
        comment_id = self.kwargs['comment_id']
        parent_comment = Comment.objects.get(id=comment_id)
        serializer.save(parent=parent_comment)


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.filter(parent__isnull=True)
    serializer_class = ChildSerializer

    def get_queryset(self):
        movie_id = self.kwargs['movie_id']
        queryset = Comment.objects.filter(parent__isnull=True, movie_id=movie_id)
        return queryset

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['show_children'] = True
        return context

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True, context=self.get_serializer_context())
        return Response(serializer.data)


class CommentLikeView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        user = request.data.get('user')
        if Like.objects.filter(user_id=user):
            Like.objects.filter(user_id=user).delete()
            return Response({"error": "Fucking like deleted"})
        elif DisLike.objects.filter(user_id=user):
            DisLike.objects.filter(user_id=user).delete()
            Like.objects.create(user_id=user, comment_id=comment_id, like=1)
            return Response({"success": "Fucking like added and deleted your fucking dislike"},
                            status=status.HTTP_201_CREATED)
        else:
            Like.objects.create(user_id=user, comment_id=comment_id, like=1)
            return Response({"success": "Fucking like added"}, status=status.HTTP_201_CREATED)


class CommentDislikeView(CreateAPIView):
    queryset = DisLike.objects.all()
    serializer_class = DisLikeSerializer

    def create(self, request, *args, **kwargs):
        comment_id = request.data.get('comment')
        user = request.data.get('user')
        if DisLike.objects.filter(user_id=user):
            DisLike.objects.filter(user_id=user).delete()
            return Response({"error": "Fucking dislike deleted"})
        elif Like.objects.filter(user_id=user):
            Like.objects.filter(user_id=user).delete()
            DisLike.objects.create(user_id=user, comment_id=comment_id, dislike=1)
            return Response({"success": "Fucking dislike added and deleted your fucking like"},
                            status=status.HTTP_201_CREATED)
        else:
            DisLike.objects.create(user_id=user, comment_id=comment_id, dislike=1)
            return Response({"success": "Fucking dislike added"}, status=status.HTTP_201_CREATED)
