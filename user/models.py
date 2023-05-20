from django.db import models
from django.db import models
from django.contrib.auth.models import AbstractUser


class UserTypes(models.TextChoices):
    AUTHOR = "AUTHOR"
    USER = "USER"


class CustomUser(AbstractUser):
    type = models.CharField(
        choices=UserTypes.choices,
        default=UserTypes.USER,
        max_length=10,
    )
    is_deleted = models.BooleanField(default=False)
