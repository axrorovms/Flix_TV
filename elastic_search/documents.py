from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from movie.models import Movie


@registry.register_document
class MovieDocument(Document):
    title = fields.TextField(
        attr='title',
        fields={
            'raw': fields.TextField(),
            'suggest': fields.CompletionField(),
        }
    )

    class Index:
        name = 'movies'
        settings = {
            'number_of_shards': 1,
            'number_of_replicas': 0,
        }

    class Django:
        model = Movie
        fields = [
            'id',
            'description'
        ]



