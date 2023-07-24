from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from movie.models import Genre, Movie


class GenreCreateModelSerializer(ModelSerializer):
    class Meta:
        model = Genre
        fields = '__all__'


class GenreListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('title', 'image',)

    def to_representation(self, instance: Genre):
        rep = super().to_representation(instance)
        count = len(Movie.objects.filter(genre=instance.id))
        rep['movies_count'] = count

        return rep
