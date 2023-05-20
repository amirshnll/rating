from django.db import models
from user.models import CustomUser as CustomUserModel
from blog.models import BlogPost as BlogPostModel
from django.core.validators import MinValueValidator, MaxValueValidator


class Rating(models.Model):
    post = models.ForeignKey(BlogPostModel, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUserModel, on_delete=models.CASCADE)
    value = models.IntegerField(
        validators=[
            MinValueValidator(0, message="Minimum value is 0."),
            MaxValueValidator(100, message="Maximum value is 100."),
        ]
    )

    class Meta:
        unique_together = ["post", "user"]
