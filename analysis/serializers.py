from rest_framework import serializers
from django.core.exceptions import ObjectDoesNotExist
from django.forms import ValidationError

from classes.serializers import ClassSerializer
from consumables.models import Consumable
from stock.serializers import StockAnalysisItemsSerializer
from tech_samples.exceptions import InvalidBodyContent, InsufficientQuantity, InvalidParameterName, InvalidResultValue, InvalidTypeName, NoneConsumable, NotInStock, WrongAnalysisItem

from .models import Analysis
from classes.models import Class
from stock.models import Stock


class AnalysisSerializer(serializers.ModelSerializer):

    analyst = serializers.EmailField(read_only=True)
    class_id = serializers.UUIDField(write_only=True)
    reagents = StockAnalysisItemsSerializer(write_only=True, many=True)
    consumed_items = StockAnalysisItemsSerializer(read_only=True, many=True)

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
        reagents = validated_data.pop('reagents')

        if len(reagents) == 0:
            raise NoneConsumable()

        for item in reagents:
            if len(item['consumables']) == 0:
                raise NoneConsumable()
            try:
                in_stock = Stock.objects.get(name=item['name'])
                for stk in stock:
                    if in_stock.name == stk['name']:
                        consumable = Consumable.objects.filter(stock=in_stock)
                        total = 0

                        for cons in consumable:
                            total += cons.quantity

                        required_qnt = item['consumables'][0]['quantity']

                        if required_qnt <= total:
                            to_use.append(item)
                        else:
                            raise InsufficientQuantity()
            except ObjectDoesNotExist:
                raise NotInStock()

        if len(reagents) != len(to_use):
            raise WrongAnalysisItem()

        consumable_info = []

        for item in reagents:
            stock_item = Stock.objects.get(name=item['name'])
            required_qnt = item['consumables'][0]['quantity']
            info = stock_item.subtract(required_qnt)
            consumable_info.append({
                'name': stock_item.name,
                'consumables': info
            })

        validated_data['class_data'] = serialized
        validated_data['consumed_items'] = consumable_info
        analysis = Analysis.objects.create(
            **validated_data, analyst=self.context['request'].user)

        return analysis

    def update(self, instance, validated_data):
        analysis = Analysis.objects.get(uuid=instance.uuid)

        analysis_json = AnalysisSerializer(analysis).data['class_data']

        if 'class_data' not in validated_data:
            raise InvalidBodyContent()
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
        if body['parameter_name'] not in list_of_parameters:
            raise InvalidParameterName()

        for types in analysis_json['types']:
            if types['name'] == body['type_name']:
                for parameter in types['parameters']:
                    if parameter['name'] == body['parameter_name']:
                        parameter['result'] = body['result']
                    # else:
                    #     raise InvalidParameterName(
                    #         {"error": f"parameter: {body['parameter_name']} not in type: {types['name']}"})

        analysis.save()

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
