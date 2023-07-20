from django.urls import path, include
from rest_framework.routers import DefaultRouter
from dashboard.views import (
    MovieList,
    MovieCreate,
    MovieUpdate,
    MovieDelete,
    CommentList,
    CommentDelete,
    ReviewList,
    ReviewDelete,
    DashboardAPIView
)


app_name = 'dashboard'


urlpatterns = [

    # Movies --------------------------------------------------------------------------------
    path('movies/list/', MovieList.as_view(), name='movie_list'),
    path('movies/create/', MovieCreate.as_view(), name='movie_create'),
    path('movies/update/<slug:slug>/', MovieUpdate.as_view(), name='movie_update'),
    path('movies/delete/<slug:slug>/', MovieDelete.as_view(), name='movie_delete'),

    # Comments ------------------------------------------------------------------------------
    path('comment/list/', CommentList.as_view(), name='comment_list'),
    path('comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),

    # Reviews -------------------------------------------------------------------------------
    path('review/list/', ReviewList.as_view(), name='review_list'),
    path('review/delete/<int:pk>/', ReviewDelete.as_view(), name='review_delete'),

    # Dashboards ----------------------------------------------------------------------------
    path('main/', DashboardAPIView.as_view(), name='dashboard'),

]

#
# RestApi
#
# RestFullApi
#
# path('movies/list/', MovieList.as_view(), name='movie_list'),
# path('movies/create/', MovieCreate.as_view(), name='movie_create'),
# path('movies/update/<slug:slug>/', MovieUpdate.as_view(), name='movie_update'),
# path('movies/delete/<slug:slug>/', MovieDelete.as_view(), name='movie_delete'),
#
#
#
# path('movies', MovieListCreateApiView.as_view(), name='movie_create_list'), (create, list)
# path('movies/<slug:slug>/', MovieDelete.as_view(), name='movie_delete'),


# api design
