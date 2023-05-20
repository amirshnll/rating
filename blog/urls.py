from django.urls import path
from .views import BlogPostApi, BlogPostListApi

urlpatterns = [
    path("", BlogPostApi.as_view()),
    path("<int:blog_post_id>/", BlogPostApi.as_view()),
    path("list/", BlogPostListApi.as_view()),
]
