from django.db import models
import uuid

class Parameter(models.Model):
  
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(unique=True, max_length=255)
  minimum = models.CharField(max_length=255)
  maximum = models.CharField(max_length=255)
  result = models.CharField(max_length=255, null=True)
  unit = models.CharField(max_length=255)
  type = models.ForeignKey('class_types.Type', related_name='parameters', on_delete=models.CASCADE)
