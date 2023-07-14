from django_elasticsearch_dsl_drf.constants import SUGGESTER_COMPLETION
from django_elasticsearch_dsl_drf.filter_backends import SearchFilterBackend, SuggesterFilterBackend, \
    FunctionalSuggesterFilterBackend
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet

from elastic_search.serializers import MovieDocumentSerializer
from elastic_search.documents import MovieDocument
from movie.models import Movie


class MovieDocumentViewSet(DocumentViewSet):
    queryset = Movie.objects.all()
    document = MovieDocument
    serializer_class = MovieDocumentSerializer

    filter_backends = [SearchFilterBackend, SuggesterFilterBackend]
    search_fields = (
        'title',
        'description'
    )
    suggester_fields = {
        'name': {
            'field': 'title.suggest',
            'suggesters': [
                SUGGESTER_COMPLETION,
            ],
        },
    }

    # def get_queryset(self):
    #     print(self.request.query_params.get('search'))
    #     return Movie.objects.all()


# http://127.0.0.1:8000/api/v1/find/movies/suggest/?name__completion=dean