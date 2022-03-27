from rest_framework.generics import CreateAPIView, DestroyAPIView
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAdmin

from .models import Parameter
from .serializers import ParameterSerializer

class ParameterCreateView(CreateAPIView):

  queryset = Parameter.objects.all()
  serializer_class = ParameterSerializer
  lookup_url_kwarg = "type_id"

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]


class ParameterDestroyView(DestroyAPIView):
  queryset = Parameter.objects.all()
  serializer_class = ParameterSerializer
  lookup_url_kwarg = "parameter_id"

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAdmin]
