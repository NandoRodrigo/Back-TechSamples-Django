from django.urls import path
from .views import ClassListCreateView

urlpatterns = [
    path('classes/', ClassListCreateView.as_view())
]