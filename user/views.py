from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, ListAPIView
from rest_framework.response import Response

from .models import Wishlist
from .serializers import WishlistCreateModelSerializer, WishlistListModelSerializer


class WishlistCreateAPIView(CreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistCreateModelSerializer

    def post(self, request, *args, **kwargs):
        wishlist, created = Wishlist.objects.get_or_create(movie_id=request.data.get('movie'),
                                                           user_id=request.data.get('user'))
        if not created:
            wishlist.delete()
            return Response({"message": "fucking deleted"})
        return Response({"message": "fucking added"}, status.HTTP_201_CREATED)


class WishlistListAPIView(ListAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistListModelSerializer
