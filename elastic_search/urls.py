from django.urls import path, include
from rest_framework.routers import DefaultRouter
from elastic_search.views import MovieDocumentViewSet

router = DefaultRouter()
router.register('movies', MovieDocumentViewSet, 'movies')

urlpatterns = [
    path('', include(router.urls)),
]