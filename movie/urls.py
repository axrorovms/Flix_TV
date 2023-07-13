from django.urls import path, include

from movie import views
app_name='movie'
urlpatterns = [
    path('movie/add', views.MovieCreateAPIView.as_view(), name='movie-add'),
    path('movie/list', views.MovieListAPIView.as_view(), name='movie-list'),
    path('movie/premium-list', views.MoviePremiumListAPIView.as_view(), name='movie-premium-list'),
    path('movie/popular-list', views.MoviePopularListAPIView.as_view(), name='movie-popular-list'),
    path('movie/newest-list', views.MovieNewestListAPIView.as_view(), name='movie-newest-list'),
    path('movie/update/<slug:slug>',  views.MovieUpdateAPIView.as_view(), name='update-movie'),
    path('movie/delete/<slug:slug>',  views.MovieDeleteAPIView.as_view(), name='movie-delete'),
    path('movie/similar/<slug:slug>',  views.SimilarMovieListAPIView.as_view(), name='movie-similar'),
    path('movie/suit/<slug:slug>',  views.MovieDetailAPIView.as_view(), name='movie-suit'),
    path('catalog/add', views.GenreCreateAPIView.as_view(), name='catalog-add'),
    path('catalog/list', views.GenreListAPIView.as_view(), name='catalog-list'),
    path('review/add', views.ReviewCreateAPIView.as_view(), name='review-add'),
    path('review/list/<slug:slug>', views.ReviewListAPIView.as_view(), name='review-list')
]