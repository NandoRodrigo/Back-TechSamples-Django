from django.urls import path
from .views import ListCreateAnalysisView, UpdateAnalysisView

urlpatterns = [
    path('analysis/', ListCreateAnalysisView.as_view()),
    path('analysis/<analysis_id>/', UpdateAnalysisView.as_view())
]