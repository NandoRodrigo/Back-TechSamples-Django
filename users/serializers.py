from rest_framework import serializers
from django.forms import ValidationError
from .models import User

class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User

    fields = ['uuid', 'email', 'password', 'is_admin']

    extra_kwargs = {
      'uuid': {'read_only': True},
      'password': {'write_only': True}}
    
  def validate(self, data):
    if hasattr(self, 'initial_data'):
      unknown_keys = set(self.initial_data.keys()) - set(self.fields.keys())
      if unknown_keys:
        raise ValidationError("Got unknown fields: {}".format(unknown_keys))
    return data

  def create(self, validated_data):
    user = User.objects.create_user(**validated_data)
    return user
  
  def update(self, instance, validated_data):
    return super().update(instance, validated_data)

class LoginSerializer(serializers.Serializer):
  email = serializers.EmailField()
  password = serializers.CharField()
