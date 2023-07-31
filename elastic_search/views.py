from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from rest_framework.permissions import AllowAny
from django_elasticsearch_dsl_drf.pagination import QueryFriendlyPageNumberPagination

from elastic_search.serializers import MovieDocumentSerializer
from elastic_search.documents import MovieDocument


class MovieDocumentViewSet(DocumentViewSet):
    document = MovieDocument
    serializer_class = MovieDocumentSerializer
    pagination_class = QueryFriendlyPageNumberPagination
    permission_classes = [AllowAny]
    filter_backends = [SearchFilterBackend, SuggesterFilterBackend]
    search_fields = (
        'title',
        'description'
    )
    suggester_fields = {
        'title': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }


# http://127.0.0.1:8000/api/v1/find/movies/suggest/?name__completion=dean