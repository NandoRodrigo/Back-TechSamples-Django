from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAdminOrReadOnly 

from .models import Class
from .serializers import ClassSerializer

class ClassListCreateView(ListCreateAPIView):
  
  queryset = Class.objects.all()
  serializer_class = ClassSerializer
  
  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdminOrReadOnly]