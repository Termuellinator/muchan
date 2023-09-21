from django.test import TestCase, Client
from django.urls import reverse

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