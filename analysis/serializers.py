from genericpath import exists
from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from classes.serializers import ClassSerializer
from consumables.models import Consumable
from stock.serializers import StockAnalysisItemsSerializer
from tech_samples.exceptions import InsufficientQuantity, InvalidParameterName, InvalidResultValue, InvalidTypeName, NoneConsumable, NotInStock, WrongAnalysisItem

from .models import Analysis
from classes.models import Class
from stock.models import Stock


class AnalysisSerializer(serializers.ModelSerializer):

    analyst = serializers.EmailField(read_only=True)
    class_id = serializers.UUIDField(write_only=True)
    reagents = StockAnalysisItemsSerializer(write_only=True, many=True)
    consumed_items = serializers.ListField(
        child=StockAnalysisItemsSerializer(many=True), read_only=True)

    class Meta:
        model = Analysis
        fields = '__all__'

        extra_kwargs = {
            'analyst': {'read_only': True},
            'class_id': {'write_only': True},
            'reagents': {'write_only': True},
            'consumed_items': {'read_only': True},
        }

        depth = 1

    def validate(self, data):
        if hasattr(self, 'initial_data'):
            unknown_keys = set(self.initial_data.keys()) - \
                set(self.fields.keys())
            if unknown_keys:
                raise ValidationError(
                    "Got unknown fields: {}".format(unknown_keys))
        return data

    def create(self, validated_data):

        class_id = validated_data['class_id']

        class_data = Class.objects.get(uuid=class_id)

        serialized = ClassSerializer(class_data).data

        to_use = []
        stock = serialized['stock']
        consumables = validated_data.pop('consumables')

        if len(consumables) == 0:
            raise NoneConsumable()

        for item in consumables:
            if len(item) != 2:
                raise NoneConsumable()
            try:
                in_stock = Stock.objects.get(uuid=item['uuid'])
                for stk in stock:
                    if str(in_stock.uuid) == stk['uuid']:
                        consumable = Consumable.objects.filter(stock=in_stock)
                        total = 0

                        for cons in consumable:
                            total += cons.quantity

                        if item['quantity'] <= total:
                            to_use.append(item)
                        else:
                            raise InsufficientQuantity()
            except ObjectDoesNotExist:
                raise NotInStock()

        if len(consumables) != len(to_use):
            raise WrongAnalysisItem()

        consumable_info = []

        for item in consumables:
            stock_item = Stock.objects.get(uuid=item['uuid'])
            info = stock_item.subtract(item['quantity'])
            consumable_info.append(info)

        validated_data['class_data'] = serialized
        analysis = Analysis.objects.create(
            **validated_data, analyst=self.context['request'].user)
        analysis.consumed_items = consumable_info

        return analysis

    def update(self, instance, validated_data):
        analysis = Analysis.objects.get(uuid=instance.uuid)

        analysis_json = AnalysisSerializer(analysis).data['class_data']
        body = validated_data['class_data']

        list_of_types = [values for types in analysis_json['types']
                         for values in types.values()]
        list_of_parameters = [
            values for parameters in analysis_json['types']
            for parameter in parameters['parameters']
            for values in parameter.values()
        ]
        if body['type_name'] not in list_of_types:
            raise InvalidTypeName()
        elif body['parameter_name'] not in list_of_parameters:
            raise InvalidParameterName()

        for types in analysis_json['types']:
            if types['name'] == body['type_name']:
                for parameter in types['parameters']:
                    if parameter['name'] == body['parameter_name']:
                        parameter['result'] = body['result']
        analysis.save()

        # Mudando o is_concluded
        for types in analysis_json['types']:
            for parameters in types['parameters']:
                if parameters['result'] != None:
                    analysis.is_concluded = True
                else:
                    analysis.is_concluded = False
                    analysis.is_approved = False
                    analysis.save()
                    return analysis
        analysis.save()
        if analysis.is_concluded:
            for types in analysis_json['types']:
                for parameters in types['parameters']:
                    try:
                        if int(parameters['result']) <= int(parameters['maximum']) and int(parameters['result']) >= int(parameters['minimum']):
                            analysis.is_approved = True
                        else:
                            analysis.is_approved = False
                            analysis.save()
                            return analysis
                    except:
                        raise InvalidResultValue()
        analysis.save()
        return analysis
