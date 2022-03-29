from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import Consumable
from stock.models import Stock


class ConsumableSerializer(serializers.ModelSerializer):
    stock = Stock()

    class Meta:
        model = Consumable
        fields = '__all__'
        depth = 1

        extra_kwargs = {
            'stock': {'read_only': True}
        }

    def validate(self, attrs):
        try:
            stock_id = self.context['view'].kwargs['stock_id']
            stock = Stock.objects.get(uuid=stock_id)

            return super().validate(attrs)
        except:
            raise ValidationError('Stock_id not exists')

    def create(self, validated_data):
        stock_id = self.context['view'].kwargs['stock_id']
        stock = Stock.objects.get(uuid=stock_id)
        consumable = Consumable.objects.filter(stock=stock)

        try:
            batch = validated_data['batch']
            item = consumable.get(batch=batch)
            item.quantity += validated_data['quantity']
            item.save()

            return item
        except:
            return Consumable.objects.create(**validated_data, stock=stock)


class ConsumableListSerializer(serializers.ModelSerializer):
    stock = Stock()

    class Meta:
        model = Consumable
        fields = '__all__'
        depth = 1

        extra_kwargs = {
            'stock': {'read_only': True}
        }


class ConsumableAnalysisSerializer(serializers.ModelSerializer):

    class Meta:
        model = Consumable
        fields = ['quantity', 'batch']

        extra_kwargs = {
            'batch': {'read_only': True}
        }
