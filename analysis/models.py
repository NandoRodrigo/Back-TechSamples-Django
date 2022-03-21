from django.db import models
import uuid

class Analysis(models.Model):
  
  uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  batch = models.CharField(unique=True, max_length=255)
  made = models.DateTimeField(auto_now_add=True)
  category = models.CharField(max_length=255)
  is_concluded = models.BooleanField(default=False)
  analyst = models.ForeignKey('users.User', related_name='analysis', on_delete=models.CASCADE)
