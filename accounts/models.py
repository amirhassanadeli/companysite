from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = models.CharField(
        max_length=150,
        unique=True,
        verbose_name="نام کاربری"
    )

    email = models.EmailField(
        unique=True,
        verbose_name="ایمیل"
    )

    def __str__(self):
        return self.username
