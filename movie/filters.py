from django_filters import rest_framework as filters
from .models import Movie


class DecadeFilter(filters.Filter):
    def filter(self, queryset, value):
        if value is not None:
            value = int(value)
            start_year = value // 10 * 10
            end_year = start_year + 9
            return queryset.filter(release_year__gte=start_year, release_year__lte=end_year)
        return queryset


class Moviefilter(filters.FilterSet):
    release_year = DecadeFilter(field_name='release_year')
    is_premium = filters.BooleanFilter(field_name='is_premium')
    ordering = filters.OrderingFilter(
        fields=(
            ('-views', 'views'),
            ('-release_year', 'release_year'),
        )
    )

    class Meta:
        model = Movie
        fields = ()


