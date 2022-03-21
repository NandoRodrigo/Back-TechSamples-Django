from django.db import models
import uuid

class Stock(models.Model):
  
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(unique=True, max_length=255)
  category = models.CharField(max_length=255)
  admin = models.ForeignKey('users.User', related_name='stock', on_delete=models.CASCADE)