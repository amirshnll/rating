from django.db import models
from user.models import CustomUser as CustomUserModel
from blog.models import BlogPost as BlogPostModel


class Rating(models.Model):
    post = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    value = models.PositiveIntegerField()

    class Meta:
        unique_together = ["post", "user"]
