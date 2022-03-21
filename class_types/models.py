from django.db import models
import uuid

class Type(models.Model):
  
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(unique=True, max_length=255)
  class_type = models.ForeignKey('classes.Class', related_name='types', on_delete=models.CASCADE)
