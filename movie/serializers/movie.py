from rest_framework import serializers
from movie.models import Movie, MovieVideo
from users.models import User


class VideoSerializerModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = MovieVideo
        fields = ('video', )


class MovieListModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')

    @classmethod
    def get_similar_movies(cls, slug):
        try:
            movie = Movie.objects.get(slug=slug)
            movie_genres = movie.genre.all()
            similar_movies = Movie.objects.filter(genre__in=movie_genres).exclude(slug=slug).distinct()

            return similar_movies

        except Movie.DoesNotExist:
            return Movie.objects.none()

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.review_set.all():
            rep['rating'] = float(0.0)
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.review_set.all()]) / instance.review_set.all().count():.1f}'
        rep['videos'] = [i.video for i in instance.movievideo_set.all()]
        rep['genre'] = [i.title for i in instance.genre.all()]
        return rep


class MovieDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = ('title', 'release_year', 'is_premium', 'photo', 'banner')

    def to_representation(self, instance: Movie):
        rep = super().to_representation(instance)
        if not instance.review_set.all():
            rep['rating'] = 0.0
        else:
            rep['rating'] = f'{sum([i.rating for i in instance.review_set.all()]) / instance.review_set.all().count():.1f}'
        rep['videos'] = [i.video for i in instance.movievideo_set.all()]
        rep['genre'] = [i.title for i in instance.genre.all()]

        return rep

    @staticmethod
    def get_suitable_movies(user_id, slug):
        user = User.objects.filter(id=user_id).values('subscription').first()
        movie = Movie.objects.filter(slug=slug).first()

        if user and user.get('subscription') and movie and movie.is_premium:
            return MovieDetailModelSerializer(Movie.objects.filter(slug=slug), many=True).data

        response_data = {"message": "Sorry, you need a premium subscription to access this movie."}
        return response_data
