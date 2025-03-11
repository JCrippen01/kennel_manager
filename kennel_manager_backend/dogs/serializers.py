from rest_framework import serializers
from .models import Dog, DogBreed


class DogBreedSerializer(serializers.ModelSerializer):
    class Meta:
        model = DogBreed
        fields = ["id", "name"]


class DogSerializer(serializers.ModelSerializer):
    breed = DogBreedSerializer()

    class Meta:
        model = Dog
        fields = "__all__"
        read_only_fields = ["owner", "created_at"]
