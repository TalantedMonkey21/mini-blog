from django.test import TestCase, Client
from django.contrib.auth.models import User
from blog.models import Post
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

class BlogFrontendTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="maksim", password="12345")
        self.post = Post.objects.create(
            title="Тестовый пост",
            content="Текст поста",
            author=self.user,
        )

    def test_post_list_page(self):
        response = self.client.get(reverse("post_list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Тестовый пост")

    def test_post_detail_page(self):
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Текст поста")

    def test_create_post_requires_login(self):
        response = self.client.get(reverse("post_create"))
        self.assertEqual(response.status_code, 302)

    def test_logged_in_user_can_create_post(self):
        self.client.login(username="maksim", password="12345")
        response = self.client.post(reverse("post_create"), {
            "title": "Новый пост",
            "content": "Новый текст",
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Post.objects.filter(title="Новый пост").exists())

    def test_only_author_can_see_edit_delete_buttons(self):
        self.client.login(username="maksim", password="12345")
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertContains(response, "Редактировать")
        self.assertContains(response, "Удалить")

        other_user = User.objects.create_user(username="other", password="12345")
        self.client.login(username="other", password="12345")
        response = self.client.get(reverse("post_detail", args=[self.post.pk]))
        self.assertNotContains(response, "Редактировать")
        self.assertNotContains(response, "Удалить")