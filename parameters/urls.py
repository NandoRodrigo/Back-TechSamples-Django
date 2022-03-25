from django.urls import path
from .views import ParameterCreateView, ParameterDestroyView

urlpatterns = [
    path('classes/types/<type_id>/parameters/', ParameterCreateView.as_view()),
    path('classes/types/parameters/<parameter_id>/', ParameterDestroyView.as_view()),

]