from rest_framework import serializers
from .models import Stock


class StockSerializer(serializers.ModelSerializer):
    admin = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Stock
        fields = '__all__'

        extra_kwargs = {
            'uuid': {'read_only': True},
            'admin': {'read_only': True}
        }

    def create(self, validated_data):
        return Stock.objects.create(**validated_data, admin=self.context['request'].user)

    def update(self, instance, validated_data):
        validated_data['admin'] = self.context['request'].user
        return super().update(instance, validated_data)


class StockListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ['admin']
