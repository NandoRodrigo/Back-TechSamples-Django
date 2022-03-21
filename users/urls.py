from django.urls import path
from .views import UsersView, LoginView, UpdatePasswordView

urlpatterns = [
    path('accounts/', UsersView.as_view()),
    path('account/<user_id>', UpdatePasswordView.as_view()),
    path('login/', LoginView.as_view())
]