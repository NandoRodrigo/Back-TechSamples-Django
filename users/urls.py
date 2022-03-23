from django.urls import path
from .views import AdminSignupView, AnalystSignupView, LoginView, UpdatePasswordView

urlpatterns = [
    path('signup/', AdminSignupView.as_view()),
    path('admin/analyst', AnalystSignupView.as_view()),
    path('profile/<user_id>', UpdatePasswordView.as_view()),
    path('login/', LoginView.as_view())
]
