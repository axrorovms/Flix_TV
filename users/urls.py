from django.urls import path
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from users.views import (
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    ActivationUserGenericAPIView,
    PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView,
    WishlistListCreateAPIView,
    UserRetrieveAPIView,

)

app_name = 'user'

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='users_list_create'),
    path('activate/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),
    path('change/<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view()),
    path('getme/', UserRetrieveAPIView.as_view()),


    path('token/', TokenObtainPairView.as_view(parser_classes = (FormParser, MultiPartParser)), name='token_create'),
    path('token/refresh/', TokenRefreshView.as_view(parser_classes = (FormParser, MultiPartParser)), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(parser_classes = (FormParser, MultiPartParser)), name='token_verify'),

    path('wishlist', WishlistListCreateAPIView.as_view(), name="wishlist_list_create"),

]
