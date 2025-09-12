from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post
from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse

class PostAPITest(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='apiuser', password='12345')
        self.post = Post.objects.create(title='API Test', content='API content', author=self.user)
        self.client.login(username='apiuser', password='12345')

    def test_get_posts(self):
        url = reverse('post-list')  # DRF router автоматически создает имя
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_create_post(self):
        url = reverse('post-list')
        data = {'title': 'New Post', 'content': 'New content', 'author': self.user.id}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 2)

class PostModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.post = Post.objects.create(
            title='Test Post',
            content='Content for test post',
            author=self.user
        )

    def test_post_creation(self):
        self.assertEqual(self.post.title, 'Test Post')
        self.assertEqual(self.post.content, 'Content for test post')
        self.assertEqual(self.post.author.username, 'testuser')