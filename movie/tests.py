from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User
from .models import Movie, Genre, Review


class MovieTest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='Movie', email='Director@mrieoe.com', password="1")
        self.genre = Genre.objects.create(title='Movie')
        self.movie = Movie.objects.create(title="titles",
                                          slug="titles",
                                          description="description",
                                          release_year=2023,
                                          film_time_duration=12,
                                          age_limit=18,
                                          country="AF",
                                          type="Movie",
                                          status="Premium",
                                          is_active=True,
                                          video_url="http://127.0.0.1:8000",
                                          views=99,
                                          user=self.user)
        self.movie.genre.set([self.genre.pk])
        self.review = Review.objects.create(text='bjhef', rating=8, author=self.user, movie=self.movie)

    def test_movie_add(self):
        url = reverse('movie:movie-add')
        response = self.client.post(url, data={"title": "titles",
                                               "slug": "titles",
                                               "description": "description",
                                               "release_year": 2023,
                                               "film_time_duration": 12,
                                               "age_limit": 18,
                                               "country": "AF",
                                               "type": "Movie",
                                               "status": "Premium",
                                               "video_url": 'http://127.0.0.1:8000',
                                               "views": 99,
                                               "user": self.user.pk,
                                               "genre": [self.genre.pk]})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_movie_list(self):
        url = reverse('movie:movie-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data['results'])
        self.assertEqual(list(data.keys()),
                         ['title', 'release_year', 'status', 'photo', 'banner', 'rating', 'videos', 'genre'])

    def test_movie_premium_list(self):
        url = reverse('movie:movie-premium-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['title', 'release_year', 'status', 'photo', 'banner', 'rating', 'videos', 'genre'])

    def test_movie_newest_list(self):
        url = reverse('movie:movie-newest-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['title', 'release_year', 'status', 'photo', 'banner', 'rating', 'videos', 'genre'])

    def test_movie_popular_list(self):
        url = reverse('movie:movie-popular-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['title', 'release_year', 'status', 'photo', 'banner', 'rating', 'videos', 'genre'])

    def test_movie_detail_list(self):
        url = reverse('movie:movie-suit', kwargs={'slug': self.movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['title', 'release_year', 'status', 'photo', 'banner', 'rating', 'videos', 'genre'])

    def test_movie_update(self):
        url = reverse('movie:update-movie', kwargs={'slug': self.movie.slug})
        data = {"title": "Updated Movie",
                "slug": "updated-movie",
                "description": "description",
                "release_year": 2023,
                "film_time_duration": 12,
                "age_limit": 18,
                "country": "AF",
                "type": "Movie",
                "status": "Free",
                "video_url": "http://127.0.0.1:8000",
                "views": 99,
                "user": self.user.pk,
                "genre": [
                    self.genre.pk
                ]
                }
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, 'Updated Movie')

    def test_movie_delete(self):
        url = reverse('movie:movie-delete', kwargs={'slug': self.movie.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_genre_add(self):
        url = reverse('movie:catalog-add')
        response = self.client.post(url, data={"title": "titles"})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_genre_list(self):
        url = reverse('movie:catalog-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()), ['title', 'image', 'movies_count'])

    def test_movie_similar(self):
        url = reverse('movie:movie-similar', kwargs={'slug': self.movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review(self):
        url = reverse('movie:review-list', kwargs={'slug': self.movie.slug})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()), ['author', 'text', 'rating', 'created_at'])

    def test_review_add(self):
        url = reverse('movie:review-add')
        response = self.client.post(url, data={
            "author": self.user.pk,
            "text": "fmeiofeio0,",
            "rating": 8,
            "movie": self.movie.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
