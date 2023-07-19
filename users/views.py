from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from rest_framework.generics import CreateAPIView, GenericAPIView, ListAPIView, DestroyAPIView, UpdateAPIView, \
    RetrieveAPIView

from users.models import User
from users.serializers import RegisterUserModelSerializer, CheckActivationSerializer, SendEmailResetSerializer
from users.serializers.serializers import PasswordResetConfirmSerializer, UserModelSerializer

from users.models import Wishlist
from users.serializers.wishlist import WishlistCreateModelSerializer, WishlistListModelSerializer


# Create your views here.

class UserTokenObtainPairView(TokenObtainPairView):
    parser_classes = (FormParser, MultiPartParser)


class UserTokenRefreshView(TokenRefreshView):
    parser_classes = (FormParser, MultiPartParser)


class UserTokenVerifyView(TokenVerifyView):
    parser_classes = (FormParser, MultiPartParser)


class RegisterUserCreateAPIView(CreateAPIView):
    serializer_class = RegisterUserModelSerializer
    parser_classes = (FormParser, MultiPartParser)
    permission_classes = (AllowAny,)


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


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer
    permission_classes = (AllowAny,)


class UserCreate(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserUpdate(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserModelSerializer


class UserDelete(DestroyAPIView):
    # permission_classes = [AdminOrModerator]
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


class UserDetail(RetrieveAPIView):
    # permission_classes = [AdminOrModerator]
    serializer_class = UserModelSerializer
    queryset = User.objects.all()


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


