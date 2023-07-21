from django.urls import path
from users.views import (
    UserTokenObtainPairView,
    UserTokenRefreshView,
    UserTokenVerifyView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
    ActivationUserGenericAPIView,
    PasswordResetGenericAPIView,
    PasswordResetConfirmUpdateAPIView,
    WishlistListCreateAPIView,

)

app_name = 'user'

urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='users_list_create'),
    path('activate/', ActivationUserGenericAPIView.as_view(), name='activated_account'),
    path('reset-password/', PasswordResetGenericAPIView.as_view(), name='reset_password'),
    path('reset-password-confirm/', PasswordResetConfirmUpdateAPIView.as_view(), name='reset_password_confirm'),
    path('<int:pk>', UserRetrieveUpdateDestroyAPIView.as_view()),

    path('token/', UserTokenObtainPairView.as_view(), name='token_create'),
    path('token/refresh/', UserTokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', UserTokenVerifyView.as_view(), name='token_verify'),

    path('wishlist', WishlistListCreateAPIView.as_view(), name="wishlist_list_create"),

]
