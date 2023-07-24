from django.urls import path
from movie import views
from movie.views import CreateCommentAPIView,CommentListAPIView

app_name = 'movie'


urlpatterns = [

    # Movie
    path('', views.MovieListAPIView.as_view(), name='movie_list'),
    # path('premium', views.MoviePremiumListAPIView.as_view(), name='movie_premium_list'),
    path('similar/<slug:slug>', views.SimilarMovieListAPIView.as_view(), name='movie_similar'),
    path('detail/<slug:slug>', views.MovieRetrieveAPIView.as_view(), name='movie_detail'),

    # Catalog
    path('catalog', views.GenreListAPIView.as_view(), name='catalog_list'),

    # Reviews
    path('review', views.ReviewCreateAPIView.as_view(), name='review_add'),
    path('review/<slug:slug>', views.ReviewListAPIView.as_view(), name='review_list'),]

# Comment view for url
urlpatterns += [
    path('comments/like', views.LikeDislikeView.as_view(), name='comment_likes'),
    path('comments', CreateCommentAPIView.as_view(), name='comment_create'),
    path('comments/<int:movie_id>', CommentListAPIView.as_view(), name='movie_comment_list'),
]
