from django.urls import path
from .views import ListCreateAnalysisView

urlpatterns = [
    path('analysis/', ListCreateAnalysisView.as_view())
]