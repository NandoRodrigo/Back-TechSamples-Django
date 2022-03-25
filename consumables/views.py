from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAdmin
from .serializers import ConsumableSerializer, ConsumableListSerializer
from .models import Consumable
from stock.models import Stock


class ConsumableView(ListCreateAPIView):
    queryset = Consumable.objects.all()
    serializer_class = ConsumableSerializer
    lookup_url_kwarg = "stock_id"

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return ConsumableListSerializer
        return super().get_serializer_class()

    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    def get_queryset(self):
        stock = Stock.objects.get(uuid=self.kwargs['stock_id'])
        return Consumable.objects.filter(stock=stock)
