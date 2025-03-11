from django.db import models

# Create your models here.
from django.db import models
from django.conf import settings


class DogBreed(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Dog(models.Model):
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="dogs"
    )
    name = models.CharField(max_length=100)
    breed = models.ForeignKey(
        DogBreed, on_delete=models.SET_NULL, null=True, blank=True
    )
    age = models.IntegerField()
    medical_notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.breed.name if self.breed else 'Unknown'})"
