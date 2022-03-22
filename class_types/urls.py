from django.urls import path
from .views import TypeCreateView, TypeUpdateView

urlpatterns = [
    path('classes/<class_id>/types', TypeCreateView.as_view()),
    path('classes/types/<type_id>', TypeUpdateView.as_view())
]