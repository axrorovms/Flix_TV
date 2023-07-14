from django.contrib import admin
from django.urls import path

from user import views

app_name = 'user'
urlpatterns = [
    path('add-wishlist', views.WishlistCreateAPIView.as_view(), name="add-wishlist"),
    path('wishlist-list', views.WishlistListAPIView.as_view(), name="list-wishlist")
]
