from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DogViewSet, get_dog_breeds

router = DefaultRouter()
router.register(r"dogs", DogViewSet, basename="dog")

urlpatterns = [
    path("breeds/", get_dog_breeds, name="get_dog_breeds"),
    path("", include(router.urls)),
]
