from django.db import models
import uuid

class Class(models.Model):
  
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  name = models.CharField(unique=True, max_length=255)
  admin = models.ForeignKey('users.User', related_name='classes', on_delete=models.CASCADE)
  stock = models.ManyToManyField('stock.Stock', related_name='classes')