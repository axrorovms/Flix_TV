from rest_framework.routers import DefaultRouter
from django.urls import re_path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView

from user.views import UserViewSet

router = DefaultRouter()
router.register("", UserViewSet)

urlpatterns = [
    re_path(r"^token/create/?", TokenObtainPairView.as_view(), name="token-create"),
    re_path(r"^token/refresh/?", TokenRefreshView.as_view(), name="token-refresh"),
    re_path(r"^token/verify/?", TokenVerifyView.as_view(), name="token-verify"),
]
urlpatterns += router.urls
