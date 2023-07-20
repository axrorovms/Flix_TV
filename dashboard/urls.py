from django.urls import path
from dashboard.views import (
    MovieListCreateApiView,
    MovieUpdateDelete,
    CommentList,
    CommentDelete,
    ReviewList,
    ReviewDelete,
    DashboardAPIView,
    GenreCreateAPIView,
)

app_name = 'dashboard'

urlpatterns = [

    # Movies --------------------------------------------------------------------------------
    path('movies', MovieListCreateApiView.as_view(), name='movie_create_list'),
    path('movies/<slug:slug>', MovieUpdateDelete.as_view(), name='movie_update_delete'),


    # Comments ------------------------------------------------------------------------------
    path('comments', CommentList.as_view(), name='comment_list'),
    path('comments/<int:pk>', CommentDelete.as_view(), name='comment_delete'),

    # Reviews -------------------------------------------------------------------------------
    path('reviews', ReviewList.as_view(), name='review_list'),
    path('reviews/<int:pk>', ReviewDelete.as_view(), name='review_delete'),

    # Dashboards ----------------------------------------------------------------------------
    path('', DashboardAPIView.as_view(), name='dashboard'),


    path('genre', GenreCreateAPIView.as_view(), name='genre'),

]

