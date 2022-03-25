from rest_framework import serializers
from django.forms import ValidationError
from class_types.serializers import TypeSerializer
from class_types.models import Type
from .models import Parameter

class ParameterSerializer(serializers.ModelSerializer):
  
  type = TypeSerializer(read_only=True)
  
  class Meta:
    model = Parameter
    fields = '__all__'
    
    extra_kwargs = {
        'type': {'read_only': True}
    }
    
  def validate(self, data):
    if hasattr(self, 'initial_data'):
      unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
      if unknown_keys:
        raise ValidationError("Got unknown fields: {}".format(unknown_keys))
    return data
    
  def create(self, validated_data):
   
    type_id = self.context['view'].kwargs['type_id']
    getType = Type.objects.get(uuid=type_id)
    return Parameter.objects.create(**validated_data, type=getType)
   

  def delete(self):
    parameter_id = self.context['view'].kwargs['parameter_id']
    getParameter = Parameter.objects.filter(uuid=parameter_id).delete()
    return getParameter
  
    