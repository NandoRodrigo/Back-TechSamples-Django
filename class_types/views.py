from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAdmin

from .models import Type
from .serializers import TypeSerializer

class TypeCreateView(CreateAPIView):
  queryset = Type.objects.all()
  serializer_class = TypeSerializer
  lookup_url_kwarg = "class_id"

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]
  
class TypeUpdateView(RetrieveUpdateAPIView):
  queryset = Type.objects.all()
  serializer_class = TypeSerializer
  lookup_url_kwarg = "type_id"

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]