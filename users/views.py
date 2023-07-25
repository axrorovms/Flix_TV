from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.generics import GenericAPIView, RetrieveUpdateDestroyAPIView, ListCreateAPIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from users.models import User, Wishlist
from users.serializers.wishlist import WishlistModelSerializer
from users.serializers import (
    CheckActivationSerializer,
    SendEmailResetSerializer,
    PasswordResetConfirmSerializer,
    UserModelSerializer
)


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)
    parser_classes = (FormParser, MultiPartParser)


class ActivationUserGenericAPIView(GenericAPIView):
    parser_classes = (FormParser, MultiPartParser)
    serializer_class = CheckActivationSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.is_active = True
        user.save(update_fields=["is_active"])
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetGenericAPIView(GenericAPIView):
    serializer_class = SendEmailResetSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get('email')
        # return Response(serializer.data, status.HTTP_200_OK)
        return Response({'email': email}, status=status.HTTP_200_OK)


class PasswordResetConfirmUpdateAPIView(GenericAPIView):
    serializer_class = PasswordResetConfirmSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)

    def patch(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        password = serializer.validated_data.get('new_password')
        user = User.objects.get(email=serializer.validated_data.get('email'))
        user.password = make_password(password)
        user.save(update_fields=["password"])
        return Response(status=status.HTTP_200_OK)


class WishlistListCreateAPIView(ListCreateAPIView):
    queryset = Wishlist.objects.all()
    serializer_class = WishlistModelSerializer
    parser_classes = (FormParser, MultiPartParser)

    def create(self, request, *args, **kwargs):
        wishlist, created = self.queryset.get_or_create(
            movie_id=request.data.get('movie'),
            user_id=request.data.get('user')
        )
        if not created:
            wishlist.delete()
            return Response({"message": "fucking deleted"})
        return Response({"message": "fucking added"}, status=status.HTTP_201_CREATED)
