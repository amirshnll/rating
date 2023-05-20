from django.test import TestCase
from rest_framework.test import APIClient
from user.defs import get_token_prefix
import random

blog_post = [
    {"title": "content 1", "content": "this is a test 1"},
    {"title": "content 2", "content": "this is a test 2"},
    {"title": "content 3", "content": "this is a test 3"},
]

rate_items = [
    {"post": 1, "value": -1},
    {"post": 1, "value": 2},
    {"post": 2, "value": 10},
    {"post": 2, "value": 1},
    {"post": 2, "value": 2},
]


author_user = {"username": "amir", "password": "T%Y%WEGTwaddaw423rfwea"}
new_user = {"username": "nilo", "password": "p8VeqZOwHlQa7X2IFeY3"}


class RateTestCases(TestCase):
    # python manage.py test rate.tests.RateTestCases.test_Rate
    def test_Rate(self):
        self.clients = APIClient()

        self.author_register = self.client.post(
            "/api/v1/user/author/",
            author_user,
        ).json()

        auth_author_obj = self.clients.post("/api/v1/user/auth/", author_user).json()
        author_token = get_token_prefix() + auth_author_obj["token"]
        print(author_user["username"], author_token)

        for blog in blog_post:
            new_blog_post = self.client.post(
                "/api/v1/blog/", blog, **{"HTTP_AUTHORIZATION": author_token}
            ).json()

            print(new_blog_post)

        self.user_register = self.client.post(
            "/api/v1/user/",
            new_user,
        ).json()

        auth_user_obj = self.clients.post("/api/v1/user/auth/", new_user).json()
        user_token = get_token_prefix() + auth_user_obj["token"]
        print(new_user["username"], user_token)

        for rate in rate_items:
            new_rate = self.client.post(
                "/api/v1/rate/", rate, **{"HTTP_AUTHORIZATION": user_token}
            ).json()

            print(new_rate)

            total_rate = self.client.get("/api/v1/rate/total/1/").json()

            print("total rate: ", total_rate)
