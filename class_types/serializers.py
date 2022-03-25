from rest_framework import serializers
from django.forms import ValidationError

from .models import Type
from classes.models import Class

from parameters.serializers import ParameterReadSerializer

class TypeSerializer(serializers.ModelSerializer):
  
  class_type = serializers.SlugRelatedField(read_only=True, slug_field='name')
  
  
  class Meta:
    model = Type
    fields = '__all__'
    
    extra_kwargs = {
        'class_type': {'read_only': True},
        'parameters': {'read_only': True}
    }
    
    
  def validate(self, data):
    if hasattr(self, 'initial_data'):
      unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
      if unknown_keys:
        raise ValidationError("Got unknown fields: {}".format(unknown_keys))
    return data
    
  def create(self, validated_data):
    class_id = self.context['view'].kwargs['class_id']
    getClass = Class.objects.get(uuid=class_id)
    return Type.objects.create(**validated_data, class_type=getClass)
  
  def update(self, instance, validated_data):
    return super().update(instance, validated_data)
  
  
class TypeReadSerializer(serializers.ModelSerializer):
  
  parameters = ParameterReadSerializer(read_only=True, many=True)
    
  class Meta:
    model = Type
    fields = ['uuid','name', 'parameters']