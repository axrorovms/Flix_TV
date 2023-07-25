from rest_framework import serializers

from movie.models import Movie
from users.models import Wishlist


class WishlistModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = ('movie', 'user')

    def to_representation(self, instance: Wishlist):
        rep = super().to_representation(instance)
        rep["photo"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('photo')).get('photo')
        rep["title"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('title')).get('title')
        rep["release_year"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('release_year')).get(
            'release_year')
        rep["is_premium"] = dict(*Movie.objects.filter(id=instance.movie.pk).values('is_premium')).get('is_premium')
        rep["genre"] = [i.title for i in instance.movie.genre.all()]
        if not instance.movie.review_set.all():
            rep['rating'] = float(0.0)
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.movie.review_set.all()]) / instance.movie.review_set.all().count():.1f}'

        return rep
