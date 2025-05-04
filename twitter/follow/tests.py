from django.test import TestCase
from rest_framework.test import APIClient
from django.core.cache import cache

from twitter.accounts.utils import create_user, authenticate_client

class FollowUnityTest(TestCase):
    def setUp(self):
        cache.clear()
        self.client = APIClient()
        self.password = 'senha123'

        self.user = create_user()
        self.other_user = create_user(
            name="Outro Usuário",
            email="outro@example.com",
            username="otheruser",
            password=self.password
        )

        authenticate_client(self.client, self.user.email, self.password)

    def test_follows_handle(self):
        response = self.client.post("/api/v1/follow/", {
            "following": self.other_user.id
        }, format="json")
        self.assertEqual(response.status_code, 201)

        follow_data = self.client.get("/api/v1/follow/")
        self.assertEqual(len(follow_data.data['following_users_id']), 1)

        authenticate_client(self.client, self.other_user.email, self.password)

        second_follow_data = self.client.get("/api/v1/follow/")
        self.assertEqual(second_follow_data.data['followers_users_id'][0], self.user.id)
