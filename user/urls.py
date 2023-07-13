
from django.contrib import admin
from django.urls import path

from user import views

urlpatterns = [
    path('add-wishlist', views.WishlistCreateAPIView.as_view())
]
