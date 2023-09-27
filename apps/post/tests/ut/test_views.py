from django.test import TestCase, Client
from django.urls import reverse

from apps.post import models
from apps.user.models import User


class TestHomePageView(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword",
            )

    def test_returns_200(self):
        response = self.client.get(reverse("home"),
                              HTTP_USER_AGENT="Mozilla/5.0",
                              HTTP_CONTENT_TYPE="text/xml")
        self.assertEqual(response.status_code, 200)


class TestPostPageView(TestCase):
    def setUp(self):
        self.post_title = "Testpost"
        self.username = "test"
        self.category = "testcat"
        self.user = User.objects.create_user(
            username=self.username,
            password="test",
            )
        self.cat = models.Category.objects.create(cat=self.category)
        self.post = models.Post.objects.create(
            user_id=self.user,
            cat_id=self.cat,
            title=self.post_title,
            image="uploads/image.jpg"
        )

    def test_redirects_to_login_if_not_authed(self):
        response = self.client.get(reverse("post-detail",
                                           kwargs={'post_id':self.post.id}),
                              HTTP_USER_AGENT="Mozilla/5.0",
                              HTTP_CONTENT_TYPE="text/xml")

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/?next=/post/{self.post.id}")

    def test_returns_200_if_authed(self):
        self.client.login(username="test", password="test")
        response = self.client.get(reverse("post-detail",
                                           kwargs={'post_id':self.post.id}),
                              HTTP_USER_AGENT="Mozilla/5.0",
                              HTTP_CONTENT_TYPE="text/xml")

        self.assertEqual(response.status_code, 200)
