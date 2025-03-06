from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    # Custom fields can be added here if needed
    def __str__(self):
        return self.username
