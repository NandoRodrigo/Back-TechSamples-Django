from rest_framework.urls import path
from .views import ConsumableView


urlpatterns = [
    path('stock/<uuid:stock_id>/consumables/', ConsumableView.as_view()),
]
