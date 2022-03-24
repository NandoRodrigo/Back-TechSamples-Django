from rest_framework.urls import path
from .views import StockView


urlpatterns = [
    path('stock/', StockView.as_view())
]
