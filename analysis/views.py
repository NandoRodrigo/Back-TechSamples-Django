from rest_framework.generics import ListCreateAPIView
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAnalyst

from .models import Analysis
from .serializers import AnalysisSerializer

class ListCreateAnalysisView(ListCreateAPIView):
  
  queryset = Analysis.objects.all()
  serializer_class = AnalysisSerializer

  authentication_classes = [TokenAuthentication]
  permission_classes = [IsAnalyst]
