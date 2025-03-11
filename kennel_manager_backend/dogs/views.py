from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny  # ✅ Add this import
from .models import Dog, DogBreed
from .serializers import DogSerializer, DogBreedSerializer


class DogViewSet(viewsets.ModelViewSet):
    serializer_class = DogSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Dog.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


@api_view(["GET"])
@permission_classes([AllowAny])
def get_dog_breeds(request):
    breeds = DogBreed.objects.all()
    serializer = DogBreedSerializer(breeds, many=True)
    return Response(serializer.data)
