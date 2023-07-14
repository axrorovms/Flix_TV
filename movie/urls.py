from django.urls import path, include

from movie import views

app_name = 'movie'
urlpatterns = [
    path('movie/add', views.MovieCreateAPIView.as_view(), name='movie-add'),
    path('movie/list', views.MovieListAPIView.as_view(), name='movie-list'),
    path('movie/premium-list', views.MoviePremiumListAPIView.as_view(), name='movie-premium-list'),
    path('movie/popular-list', views.MoviePopularListAPIView.as_view(), name='movie-popular-list'),
    path('movie/newest-list', views.MovieNewestListAPIView.as_view(), name='movie-newest-list'),
    path('movie/update/<slug:slug>', views.MovieUpdateAPIView.as_view(), name='update-movie'),
    path('movie/delete/<slug:slug>', views.MovieDeleteAPIView.as_view(), name='movie-delete'),
    path('movie/similar/<slug:slug>', views.SimilarMovieListAPIView.as_view(), name='movie-similar'),
    path('movie/suit/<slug:slug>', views.MovieDetailAPIView.as_view(), name='movie-suit'),
    path('catalog/add', views.GenreCreateAPIView.as_view(), name='catalog-add'),
    path('catalog/list', views.GenreListAPIView.as_view(), name='catalog-list'),
    path('review/add', views.ReviewCreateAPIView.as_view(), name='review-add'),
    path('review/list/<slug:slug>', views.ReviewListAPIView.as_view(), name='review-list'),
    path('comments', views.CreateCommentAPIView.as_view(), name='comments'),
    path('comment', views.ParentListAPIView.as_view(), name='parent_list'),
    path('comments/<int:id>', views.CommentListAPIView.as_view(), name='comments_list'),
    path('comment_replay/<int:id>', views.CommentReplyListCreateAPIView.as_view(), name='comments_replay'),
    path('comment_likes/<int:id>', views.CommentLikeDislikeView.as_view(), name='comments_likes_and_dislikes'),
]
