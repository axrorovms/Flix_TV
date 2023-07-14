from rest_framework import serializers

from movie.models import Review, Movie


class ReviewCreateModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        exclude = ('id',)


class ReviewListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ('author', 'text', 'rating', 'created_at')

    @classmethod
    def get_review(cls, slug):
        movie_id = dict(*Movie.objects.filter(slug=slug).values('id')).get('id')
        reviews = Review.objects.filter(movie=movie_id)
        return reviews
