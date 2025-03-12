from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Admin"),
        ("staff", "Staff"),
        ("customer", "Customer"),
    )

    email = models.EmailField(unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="customer")

    def __str__(self):
        return self.username

    def is_admin(self):
        return self.role == "admin"

    def is_staff_user(self):
        return self.role == "staff"

    def is_customer(self):
        return self.role == "customer"
