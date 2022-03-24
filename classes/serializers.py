from rest_framework import serializers
from django.forms import ValidationError

from .models import Class
from users.serializers import UserSerializer

class ClassSerializer(serializers.ModelSerializer):
  
  admin = serializers.EmailField(read_only=True)
  # types = serializers.PrimaryKeyRelatedField(read_only=True)
  
  class Meta:
    model = Class
    fields = '__all__'
    
    extra_kwargs = {
        'admin': {'read_only': True},
        'stock': {'read_only': True},
    }
    
    
  def validate(self, data):
    if hasattr(self, 'initial_data'):
      unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
      if unknown_keys:
        raise ValidationError("Got unknown fields: {}".format(unknown_keys))
    return data
  
  def create(self, validated_data):
    return Class.objects.create(**validated_data, admin=self.context['request'].user)