from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    password = models.CharField(max_length=128, default="SecureDefaultPassword123!")

    def __str__(self):
        return self.username
