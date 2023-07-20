from django.urls import path
from movie import views

app_name = 'movie'


urlpatterns = [

    # Movie
    path('', views.MovieListAPIView.as_view(), name='movie_list'),
    # path('premium', views.MoviePremiumListAPIView.as_view(), name='movie_premium_list'),
    path('similar/<slug:slug>', views.SimilarMovieListAPIView.as_view(), name='movie_similar'),
    path('detail/<slug:slug>', views.MovieDetailAPIView.as_view(), name='movie_detail'),

    # Catalog
    path('catalog', views.GenreListAPIView.as_view(), name='catalog_list'),

    # Reviews
    path('review', views.ReviewCreateAPIView.as_view(), name='review_add'),
    path('review/<slug:slug>', views.ReviewListAPIView.as_view(), name='review_list'),

    # Comments
    path('comments/<int:id>', views.CommentListCreateAPIView.as_view(), name='comments'),
    path('comment-children', views.ParentListAPIView.as_view(), name='children_list'),
    path('comment_replay/<int:id>', views.CommentReplyListCreateAPIView.as_view(), name='comments_replay'),
    path('comment/likes', views.CommentLikeView.as_view(), name='comments_likes'),
    path('comment/dislikes', views.CommentDislikeView.as_view(), name='comments_dislikes'),
]
