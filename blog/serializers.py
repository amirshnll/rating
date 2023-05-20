from rest_framework import serializers
from .models import BlogPost as BlogPostModel


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPostModel
        fields = ["id", "title", "content", "author", "created_at"]
