
from django.urls import path, include
from flake8.formatting.default import Default
from rest_framework.routers import DefaultRouter

from dashboard.views import (MovieList, MovieCreate, MovieUpdate, MovieDelete,
                             UserList, UserCreate, UserUpdate, UserDelete, CommentList, CommentDelete, ReviewList,
                             ReviewDelete, DashboardAPIView)

# router = DefaultRouter()
# router.register('movies', MovieUpdate)

app_name = 'dashboard'

urlpatterns = [
    # path('', include(router.urls)),

    # Movies --------------------------------------------------------------------------------
    path('movies/list/', MovieList.as_view(), name='movie_list'),
    path('movies/create/', MovieCreate.as_view(), name='movie_create'),
    path('movies/update/<slug:slug>/', MovieUpdate.as_view(), name='movie_update'),
    path('movies/delete/<slug:slug>/', MovieDelete.as_view(), name='movie_delete'),

    # Users ---------------------------------------------------------------------------------
    path('user/list/', UserList.as_view(), name='user_list'),
    path('user/create/', UserCreate.as_view(), name='user_create'),
    path('user/update/<int:pk>/', UserUpdate.as_view(), name='user_update'),
    path('user/delete/<int:pk>/', UserDelete.as_view(), name='user_delete'),

    # Comments ------------------------------------------------------------------------------
    path('comment/list/', CommentList.as_view(), name='comment_list'),
    path('comment/delete/<int:pk>/', CommentDelete.as_view(), name='comment_delete'),

    # Reviews -------------------------------------------------------------------------------
    path('review/list/', ReviewList.as_view(), name='review_list'),
    path('review/delete/<int:pk>/', ReviewDelete.as_view(), name='review_delete'),

    # Dashboards ----------------------------------------------------------------------------
    path('dashboard/', DashboardAPIView.as_view(), name='dashboard'),

]
