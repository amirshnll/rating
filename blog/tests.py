from django.test import TestCase
from rest_framework.test import APIClient
from user.defs import get_token_prefix
import random

blog_post = [
    {"title": "amir", "content": "ij4ZqGNwx9slG0Ltq4FS"},
    {"title": "nilo", "content": "p8VeqZOwHlQa7X2IFeY3"},
    {"title": "hanie", "content": "yF5kScZLdQQhK4niOQw0"},
]


author_user = {"username": "amir", "password": "T%Y%WEGTwaddaw423rfwea"}


class BlogTestCases(TestCase):
    # python manage.py test blog.tests.BlogTestCases.test_BlogPost
    def test_BlogPost(self):
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
