from rest_framework import serializers

from tech_samples.exceptions import InvalidClassId
from .models import Stock
from consumables.models import Consumable
from classes.models import Class
from consumables.serializers import ConsumableAnalysisSerializer


class StockSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(read_only=True)
    class_id = serializers.UUIDField(write_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

        extra_kwargs = {
            'uuid': {'read_only': True},
            'admin': {'read_only': True}
        }

    def create(self, validated_data):
        class_id = validated_data.pop('class_id')
        try:
            a_class = Class.objects.get(uuid=class_id)
            stock = Stock.objects.create(
                **validated_data, admin=self.context['request'].user)
            a_class.stock.add(stock)
        except:
            raise InvalidClassId

        return stock

    def update(self, instance, validated_data):
        validated_data['admin'] = self.context['request'].user
        return super().update(instance, validated_data)


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ['admin']


class StockNamesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        fields = ['uuid', 'name']


class StockAnalysisItemsSerializer(serializers.ModelSerializer):
    consumables = ConsumableAnalysisSerializer(many=True)

    class Meta:
        model = Stock
        fields = ['consumables', 'name']
