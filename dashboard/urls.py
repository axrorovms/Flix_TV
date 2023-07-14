from django.urls import path, include
from dashboard.views import (MovieList, MovieCreate, MovieUpdate,
                             MovieDelete, UserList, UserCreate,
                             UserUpdate, UserDelete, CommentList,
                             CommentDelete, ReviewList, ReviewDelete, DashboardAPIView)


app_name = 'dashboard'

urlpatterns = [

    # Movies --------------------------------------------------------------------------------
    path('movies/list/', MovieList.as_view(), name='movie_list'),
    path('movies/create/', MovieCreate.as_view(), name='movie_create'),
    path('movies/update/<slug:slug>/', MovieUpdate.as_view(), name='movie_update'),
    path('movies/delete/<slug:slug>/', MovieDelete.as_view(), name='movie_delete'),

    # Users ---------------------------------------------------------------------------------
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),

    # Comments ------------------------------------------------------------------------------
    path('comment/list/', CommentList.as_view(), name='comment_list'),
    path('comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),

    # Reviews -------------------------------------------------------------------------------
    path('review/list/', ReviewList.as_view(), name='review_list'),
    path('review/delete/<int:pk>/', ReviewDelete.as_view(), name='review_delete'),

    # Dashboards ----------------------------------------------------------------------------
    path('main/', DashboardAPIView.as_view(), name='dashboard'),


]
