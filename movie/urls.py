from django.urls import path
from movie import views
from movie.views import CreateCommentAPIView, ReplyCommentAPIView, MovieCommentListAPIView, DislikeCreateApiView, \
    LikeCreateApiView

app_name = 'movie'

urlpatterns = [
    path('add', views.MovieCreateAPIView.as_view(), name='movie-add'),
    path('list', views.MovieListAPIView.as_view(), name='movie-list'),
    path('premium-list', views.MoviePremiumListAPIView.as_view(), name='movie-premium-list'),
    path('popular-list', views.MoviePopularListAPIView.as_view(), name='movie-popular-list'),
    path('newefst-list', views.MovieNewestListAPIView.as_view(), name='movie-newest-list'),
    path('update/<slug:slug>', views.MovieUpdateAPIView.as_view(), name='update-movie'),
    path('delete/<slug:slug>', views.MovieDeleteAPIView.as_view(), name='movie-delete'),
    path('similar/<slug:slug>', views.SimilarMovieListAPIView.as_view(), name='movie-similar'),
    path('detail/<slug:slug>', views.MovieDetailAPIView.as_view(), name='movie-detail'),
    path('catalog/add', views.GenreCreateAPIView.as_view(), name='catalog-add'),
    path('catalog/list', views.GenreListAPIView.as_view(), name='catalog-list'),
    path('review/add', views.ReviewCreateAPIView.as_view(), name='review-add'),
    path('review/list/<slug:slug>', views.ReviewListAPIView.as_view(), name='review-list'),

]
# Comment view for url
urlpatterns += [
    path('comments/likes/', LikeCreateApiView.as_view(), name='comment_like'),
    path('comments/dislikes/', DislikeCreateApiView.as_view(), name='comment_dislike'),
    path('comments', CreateCommentAPIView.as_view(), name='comment_create'),
    path('comments/<int:movie_id>', MovieCommentListAPIView.as_view(), name='movie_comment_list'),
    path('comments_replay/<int:comment_id>', ReplyCommentAPIView.as_view(), name='comment_replay'),

]
