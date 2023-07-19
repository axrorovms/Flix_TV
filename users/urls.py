from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
    UserTokenObtainPairView, UserTokenRefreshView, UserTokenVerifyView,
    RegisterUserCreateAPIView, ActivationUserGenericAPIView, PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView, WishlistCreateAPIView, WishlistListAPIView
)
app_name = 'user'



urlpatterns = [
    path('add-wishlist', WishlistCreateAPIView.as_view(), name="add-wishlist"),
    path('wishlist-list', WishlistListAPIView.as_view(), name="list-wishlist"),
    path('token/create/', UserTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', UserTokenVerifyView.as_view(), name='token_verify'),
    path('ragister/', RegisterUserCreateAPIView.as_view(), name='register'),
    path('activate-user/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),

]
