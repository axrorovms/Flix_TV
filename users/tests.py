from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from movie.models import Genre
from users.models import User, Wishlist
from movie.models import Movie


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
                                          is_premium=True,
                                          is_active=True,
                                          video_url="http://127.0.0.1:8000",
                                          views=99,
                                          user=self.user)
        self.movie.genre.set([self.genre.pk])
        self.wishlist = Wishlist.objects.create(user=self.user, movie=self.movie)

    def test_wishlist_add(self):
        url = reverse('user:add-wishlist')
        response = self.client.post(url, data={
            "user": self.user.pk,
            "movie": self.movie.pk})
        if response.status_code == 200:
            return self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_wishlist_list(self):
        url = reverse('user:list-wishlist')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['movie', 'photo', 'title', 'release_year', 'is_premium', 'genre', 'rating', ])