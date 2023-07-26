from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from movie.models import Movie, Genre, Comment, Review
from users.models import User, Wishlist
from django.test import override_settings
from unittest import mock


# @override_settings(ELASTICSEARCH_DSL_AUTO_REFRESH=False)
class MovieAPITestCase(APITestCase):
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
        self.comment = Comment.objects.create(
            author=self.user,
            movie=self.movie,
            text="hueifhe",
        )
        self.review = Review.objects.create(text='bjhef', rating=8, author=self.user, movie=self.movie)
        self.wishlist = Wishlist.objects.create(user=self.user, movie=self.movie)

    # For Dashboard ----------------------------------------------------------------

    def test_dashboard(self):
        url = reverse('dashboard:dashboard')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # For Movie --------------------------------------------------------------------

    def test_movie_list(self):
        url = reverse('dashboard:movie_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_movie_create(self):
        url = reverse('dashboard:movie_create')
        data = {
            "title": "New",
            "slug": "new-movie",
            "description": "New movie description",
            "release_year": 2023,
            "film_time_duration": 120,
            "age_limit": 16,
            "country": "US",
            "type": "Movie",
            "is_premium": False,
            "video_url": "http://example.com/movie.mp4",
            "views": 0,
            "user": self.user.pk,
            "genre": [self.genre.pk]
        }
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        movie = Movie.objects.filter(title="New")
        self.assertEqual(movie.first().title, data["title"])

    def test_movie_update(self):
        url = reverse('dashboard:movie_update', kwargs={'slug': self.movie.slug})
        data = {
            "title": "Updated Movie",
            "slug": "updated-movie",
            "description": "Updated movie description",
            "release_year": 2023,
            "film_time_duration": 120,
            "age_limit": 16,
            "country": "US",
            "type": "Movie",
            "is_premium": False,
            "video_url": "http://example.com/movie.mp4",
            "views": 0,
            "user": self.user.pk,
            "genre": [self.genre.pk]
        }
        response = self.client.put(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.movie.refresh_from_db()
        self.assertEqual(self.movie.title, data["title"])

    def test_movie_delete(self):
        url = reverse('dashboard:movie_delete', kwargs={'slug': self.movie.slug})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Movie.objects.filter(pk=self.movie.pk).exists())

    # For Comment ----------------------------------------------------------------------------------------

    def test_comment_list(self):
        url = reverse('dashboard:comment_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_comment_delete(self):
        url = reverse('dashboard:comment_delete', kwargs={'pk': self.comment.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Comment.objects.filter(pk=self.comment.pk).exists())

    # For Review ----------------------------------------------------------------------------------------

    def test_review_list(self):
        url = reverse('dashboard:review_list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_review_delete(self):
        url = reverse('dashboard:review_delete', kwargs={'pk': self.review.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Review.objects.filter(pk=self.review.pk).exists())

# from rest_framework import status
# from django.urls import reverse
# from django.test import TestCase
#
# class DashboardAPITestCase(TestCase):
#     def test_dashboard(self):
#         url = reverse('dashboard:dashboard')
#         response = self.client.get(url)
#         self.assertEqual(response.status_code, status.HTTP_200_OK)
