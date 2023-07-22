from django_filters import filters
from django_filters.rest_framework import FilterSet

from movie.models import Movie


class Moviefilter(FilterSet):
    release_year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ['release_year', 'is_premium']
