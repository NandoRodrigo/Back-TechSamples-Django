from rest_framework import serializers
from django.forms import ValidationError

from classes.serializers import ClassSerializer
from tech_samples.exceptions import InvalidParameterName, InvalidTypeName

from .models import Analysis
from classes.models import Class

class AnalysisSerializer(serializers.ModelSerializer):
  
  analyst = serializers.EmailField(read_only=True)
  
  class Meta:
    model = Analysis
    fields = '__all__'
    
    extra_kwargs = {
        'analyst': {'read_only': True},
        'class_id': {'write_only': True}
    }

    depth = 1
    
  def validate(self, data):
    if hasattr(self, 'initial_data'):
      unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
      if unknown_keys:
        raise ValidationError("Got unknown fields: {}".format(unknown_keys))
    return data
  
  def create(self, validated_data):
    
    class_id = validated_data['class_id']
    
    class_data = Class.objects.get(uuid=class_id)
    
    serialized = ClassSerializer(class_data).data
    
    validated_data['class_data'] = serialized
    
    return Analysis.objects.create(**validated_data, analyst=self.context['request'].user)
    
  def update(self, instance, validated_data):
    analysis = Analysis.objects.get(uuid = instance.uuid)
    
    analysis_json = AnalysisSerializer(analysis).data
    body = validated_data['class_data']
    
    for types in analysis_json['class_data']['types']:
      if types['name'] == body['type_name']:
        for parameter in types['parameters']:
          if parameter['name'] == body['parameter_name']:
            parameter['result'] = body['result']
          else:
            raise InvalidParameterName()
    analysis.save()
    
    
    # Mudando o is_concluded
    for types in analysis_json['class_data']['types']:
      for parameters in types['parameters']:
          if parameters['result'] != None:
            analysis.is_concluded = True
          else:
            analysis.is_concluded = False
    analysis.save()
    
    return analysis
    # return super().update(instance, validated_data)