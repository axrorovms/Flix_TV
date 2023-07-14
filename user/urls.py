from rest_framework.routers import DefaultRouter
from django.urls import re_path, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet)

from user import views

app_name = 'user'
urlpatterns = [
    path('add-wishlist', views.WishlistCreateAPIView.as_view(), name="add-wishlist"),
    path('wishlist-list', views.WishlistListAPIView.as_view(), name="list-wishlist")
    re_path(r"^token/create/?", TokenObtainPairView.as_view(), name="token-create"),
    re_path(r"^token/refresh/?", TokenRefreshView.as_view(), name="token-refresh"),
    re_path(r"^token/verify/?", TokenVerifyView.as_view(), name="token-verify"),
]
urlpatterns += router.urls
