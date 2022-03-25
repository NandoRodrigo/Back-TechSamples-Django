from django.shortcuts import render
from rest_framework.generics import ListCreateAPIView

from rest_framework.authentication import TokenAuthentication
from tech_samples.permissions import IsAdmin
from .models import Stock
from .serializers import StockSerializer, StockListSerializer


class StockView(ListCreateAPIView):
    queryset = Stock.objects.all()
    serializer_class = StockSerializer

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdmin]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return StockListSerializer
        return super().get_serializer_class()
