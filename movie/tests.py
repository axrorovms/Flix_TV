from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status

from user.models import User
from .models import Movie, Genre, Review, Comment


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
        self.comment = Comment.objects.create(
            author=self.user,
            movie=self.movie,
            text="hueifhe",
            likes=0,
            dislikes=0,
        )

    def test_comment_add(self):
        url = reverse('movie:comments')
        response = self.client.post(url, data={
            "author": self.user.pk,
            "movie": self.movie.pk,
            "text": "hueifhe"
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_add_replay(self):
        url = reverse('movie:comments_replay', kwargs={'id': self.comment.pk})
        response = self.client.post(url, data={
            "author": self.user.pk,
            "movie": self.movie.pk,
            "text": "hueifhe",
            "parent": self.comment.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_comment_list(self):
        url = reverse('movie:comments_list', kwargs={"id": self.comment.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['id', 'movie', 'author', 'text', 'created_at', ])

    def test_comment_like(self):
        url = reverse('movie:comments_likes_and_dislikes', kwargs={"id": self.comment.pk})
        response = self.client.post(url, data={
            "action": "like",
            "id": self.comment.pk
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_parent_list(self):
        url = reverse('movie:parent_list', )
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        data = dict(*response.data)
        self.assertEqual(list(data.keys()),
                         ['id', 'author', 'text', 'children'])
