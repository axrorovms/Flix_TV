from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import (
    UserTokenObtainPairView, UserTokenRefreshView, UserTokenVerifyView,
    RegisterUserCreateAPIView, ActivationUserGenericAPIView, PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView, WishlistCreateAPIView, WishlistListAPIView, UserView, UserList
)
app_name = 'user'


urlpatterns = [
    path('add-wishlist', WishlistCreateAPIView.as_view(), name="add_wishlist"),
    path('wishlist', WishlistListAPIView.as_view(), name="wishlist"),
    path('token/create/', UserTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', UserTokenVerifyView.as_view(), name='token_verify'),
    path('ragister/', RegisterUserCreateAPIView.as_view(), name='register'),
    path('activate-user/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),

    path('<int:pk>', UserView.as_view()),
    path('', UserList.as_view())

]
