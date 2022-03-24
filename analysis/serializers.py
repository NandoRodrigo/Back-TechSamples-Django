from rest_framework import serializers
from django.forms import ValidationError

from classes.serializers import ClassSerializer

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
    
